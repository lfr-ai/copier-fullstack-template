# Dependency License Checker — Stop hook (Windows)
# Scans newly added dependencies for license compliance.
param()

if ($env:SKIP_LICENSE_CHECK -eq "true") { exit 0 }

$LicenseMode = if ($env:LICENSE_MODE) { $env:LICENSE_MODE } else { "warn" }
$LogDir = if ($env:LICENSE_LOG_DIR) { $env:LICENSE_LOG_DIR } else { "logs\copilot\license-checker" }
$Allowlist = if ($env:LICENSE_ALLOWLIST) { $env:LICENSE_ALLOWLIST -split ',' | ForEach-Object { $_.Trim() } } else { @() }

if (-not (Test-Path $LogDir)) { New-Item -ItemType Directory -Path $LogDir -Force | Out-Null }

$timestamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")

# Default blocked licenses
$blockedLicenses = if ($env:BLOCKED_LICENSES) {
  $env:BLOCKED_LICENSES -split ',' | ForEach-Object { $_.Trim().ToLower() }
} else {
  @(
    "gpl-2.0", "gpl-2.0-only", "gpl-2.0-or-later", "gpl-3.0", "gpl-3.0-only", "gpl-3.0-or-later",
    "agpl-1.0", "agpl-3.0", "agpl-3.0-only", "agpl-3.0-or-later",
    "lgpl-2.0", "lgpl-2.1", "lgpl-2.1-only", "lgpl-2.1-or-later", "lgpl-3.0", "lgpl-3.0-only", "lgpl-3.0-or-later",
    "sspl-1.0", "eupl-1.1", "eupl-1.2", "osl-3.0", "cpal-1.0", "cpl-1.0",
    "cc-by-sa-4.0", "cc-by-nc-4.0", "cc-by-nc-sa-4.0"
  )
}

# Detect new dependencies from git diff
$newDeps = @()

# npm/bun: package.json
try {
  $npmDiff = git diff HEAD -- package.json 2>$null
  if ($npmDiff) {
    $npmDiff -split "`n" | Where-Object { $_ -match '^\+\s*"([^"]+)"\s*:' -and $_ -notmatch '^\+\+\+' } | ForEach-Object {
      $pkg = $Matches[1]
      $skip = @("name","version","description","main","scripts","devDependencies","dependencies","peerDependencies","optionalDependencies","engines","type","private","workspaces","repository","author","license","bugs","homepage","keywords","files","publishConfig")
      if ($pkg -notin $skip) { $newDeps += @{ package = $pkg; ecosystem = "npm" } }
    }
  }
} catch {}

# pip: pyproject.toml
try {
  $pipDiff = git diff HEAD -- pyproject.toml 2>$null
  if ($pipDiff) {
    $pipDiff -split "`n" | Where-Object { $_ -match '^\+.*"([a-zA-Z][a-zA-Z0-9_-]*)' -and $_ -notmatch '^\+\+\+' } | ForEach-Object {
      $pkg = $Matches[1]
      $skip = @("name","version","description","authors","readme","requires","build","project","tool","python","classifiers","urls","scripts","optional","include","exclude","packages","hatchling","setuptools")
      if ($pkg -notin $skip) { $newDeps += @{ package = $pkg; ecosystem = "pip" } }
    }
  }
} catch {}

if ($newDeps.Count -eq 0) {
  $logEntry = @{ timestamp = $timestamp; event = "license_check_complete"; mode = $LicenseMode; status = "clean"; dependencies_checked = 0 } | ConvertTo-Json -Compress
  Add-Content -Path "$LogDir\check.log" -Value $logEntry
  exit 0
}

# Check licenses
$violations = @()
foreach ($dep in $newDeps) {
  if ($dep.package -in $Allowlist) { continue }

  $license = "UNKNOWN"
  switch ($dep.ecosystem) {
    "npm" {
      $localPkg = "node_modules\$($dep.package)\package.json"
      if (Test-Path $localPkg) {
        try {
          $pkgJson = Get-Content $localPkg -Raw | ConvertFrom-Json
          $license = if ($pkgJson.license) { $pkgJson.license } else { "UNKNOWN" }
        } catch { $license = "UNKNOWN" }
      } elseif (Get-Command npm -ErrorAction SilentlyContinue) {
        try { $license = npm view $dep.package license 2>$null } catch { $license = "UNKNOWN" }
      }
    }
    "pip" {
      if (Get-Command pip -ErrorAction SilentlyContinue) {
        try {
          $info = pip show $dep.package 2>$null
          $license = ($info | Select-String "^License:\s*(.+)" | ForEach-Object { $_.Matches[0].Groups[1].Value.Trim() })
          if (-not $license) { $license = "UNKNOWN" }
        } catch { $license = "UNKNOWN" }
      }
    }
  }

  $isBlocked = $false
  $licLower = $license.ToLower()
  foreach ($bl in $blockedLicenses) {
    if ($licLower -like "*$bl*") { $isBlocked = $true; break }
  }

  if ($isBlocked) {
    $violations += @{ package = $dep.package; ecosystem = $dep.ecosystem; license = $license }
  }
}

if ($violations.Count -gt 0) {
  $logEntry = @{
    timestamp = $timestamp; event = "license_check_complete"; mode = $LicenseMode
    dependencies_checked = $newDeps.Count; violation_count = $violations.Count; violations = $violations
  } | ConvertTo-Json -Compress
  Add-Content -Path "$LogDir\check.log" -Value $logEntry

  if ($LicenseMode -eq "block") {
    @{ continue = $false; stopReason = "License Checker: $($violations.Count) dependency license violation(s) found" } | ConvertTo-Json -Compress
    exit 2
  } else {
    @{ systemMessage = "License Checker: $($violations.Count) dependency license violation(s) found (warn mode)" } | ConvertTo-Json -Compress
  }
} else {
  $logEntry = @{ timestamp = $timestamp; event = "license_check_complete"; mode = $LicenseMode; status = "clean"; dependencies_checked = $newDeps.Count } | ConvertTo-Json -Compress
  Add-Content -Path "$LogDir\check.log" -Value $logEntry
}

exit 0
