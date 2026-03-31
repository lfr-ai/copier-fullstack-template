# Secrets Scanner — Stop hook (Windows)
param()

if ($env:SKIP_SECRETS_SCAN -eq "true") { exit 0 }

$ScanMode = if ($env:SCAN_MODE) { $env:SCAN_MODE } else { "warn" }
$LogDir = if ($env:SECRETS_LOG_DIR) { $env:SECRETS_LOG_DIR } else { "logs\copilot\secrets" }
if (-not (Test-Path $LogDir)) { New-Item -ItemType Directory -Path $LogDir -Force | Out-Null }

$timestamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")

# Collect modified files
$files = @()
try {
  $diffFiles = git diff --name-only --diff-filter=ACMR HEAD 2>$null
  if ($diffFiles) { $files += $diffFiles }
  $untrackedFiles = git ls-files --others --exclude-standard 2>$null
  if ($untrackedFiles) { $files += $untrackedFiles }
} catch {}

$files = $files | Where-Object {
  $_ -and (Test-Path $_) -and
  $_ -notmatch '\.(lock|min\.js|min\.css|woff|ttf|eot|ico|png|jpg|gif|svg|wasm)$' -and
  $_ -notmatch '(bun\.lock|package-lock|uv\.lock)'
}

if ($files.Count -eq 0) {
  $logEntry = @{ timestamp = $timestamp; event = "scan_complete"; status = "clean"; files_scanned = 0 } | ConvertTo-Json -Compress
  Add-Content -Path "$LogDir\scan.log" -Value $logEntry
  exit 0
}

# Secret patterns
$patterns = @(
  @("AWS_ACCESS_KEY", "critical", "AKIA[0-9A-Z]{16}"),
  @("GITHUB_PAT", "critical", "ghp_[A-Za-z0-9]{36}"),
  @("PRIVATE_KEY", "critical", "-----BEGIN\s+(RSA|EC|OPENSSH)\s+PRIVATE\s+KEY-----"),
  @("GENERIC_API_KEY", "high", "(api[_-]?key|secret[_-]?key)\s*[=:]\s*['""]?[A-Za-z0-9]{20,}"),
  @("CONNECTION_STRING", "high", "(postgresql|mysql|mongodb|redis)://[^\s""']+:[^\s""']+@"),
  @("STRIPE_KEY", "critical", "sk_live_[A-Za-z0-9]{24,}"),
  @("SLACK_TOKEN", "high", "xox[bpors]-[A-Za-z0-9-]+")
)

$findings = @()
$placeholders = @("example", "changeme", "your_", "CHANGE_ME", "placeholder", "xxx", "TODO")

foreach ($file in $files) {
  $lineNum = 0
  try {
    foreach ($line in Get-Content $file -ErrorAction SilentlyContinue) {
      $lineNum++
      $isPlaceholder = $false
      foreach ($ph in $placeholders) {
        if ($line -match [regex]::Escape($ph)) { $isPlaceholder = $true; break }
      }
      if ($isPlaceholder) { continue }

      foreach ($p in $patterns) {
        if ($line -match $p[2]) {
          $findings += @{ file = $file; line = $lineNum; pattern = $p[0]; severity = $p[1] }
        }
      }
    }
  } catch {}
}

if ($findings.Count -gt 0) {
  $logEntry = @{
    timestamp = $timestamp; event = "secrets_found"; mode = $ScanMode
    files_scanned = $files.Count; finding_count = $findings.Count; findings = $findings
  } | ConvertTo-Json -Compress
  Add-Content -Path "$LogDir\scan.log" -Value $logEntry

  if ($ScanMode -eq "block") {
    @{ continue = $false; stopReason = "Secrets Scanner: $($findings.Count) potential secret(s) found" } | ConvertTo-Json -Compress
    exit 2
  } else {
    @{ systemMessage = "Secrets Scanner: $($findings.Count) potential secret(s) found (warn mode)" } | ConvertTo-Json -Compress
  }
} else {
  $logEntry = @{ timestamp = $timestamp; event = "scan_complete"; status = "clean"; files_scanned = $files.Count } | ConvertTo-Json -Compress
  Add-Content -Path "$LogDir\scan.log" -Value $logEntry
}

exit 0
