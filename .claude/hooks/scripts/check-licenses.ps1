# Check Licenses  Stop hook (Windows)
# Scans installed dependencies for license compatibility.
param()

if ($env:SKIP_LICENSE_CHECK -eq "true") { exit 0 }

$Mode = if ($env:LICENSE_MODE) { $env:LICENSE_MODE } else { "warn" }
$LogDir = if ($env:LICENSE_LOG_DIR) { $env:LICENSE_LOG_DIR } else { "logs\copilot\license-checker" }

if (-not (Test-Path $LogDir)) { New-Item -ItemType Directory -Path $LogDir -Force | Out-Null }

$timestamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
$violations = @()
$exitCode = 0

# Denied license patterns
$deniedPattern = "AGPL|SSPL|EUPL|OSL-3"

#  Python: pip-licenses
if (Get-Command pip-licenses -ErrorAction SilentlyContinue) {
    try {
        $pyResult = pip-licenses --format=json 2>$null | ConvertFrom-Json
        foreach ($pkg in $pyResult) {
            if ($pkg.License -match $deniedPattern) {
                $violations += "Python: $($pkg.Name)==$($pkg.Version): $($pkg.License)"
            }
        }
    } catch {
        # pip-licenses failed, skip
    }
} elseif ((Test-Path "pyproject.toml") -and (Get-Command uv -ErrorAction SilentlyContinue)) {
    $violations += "Python: pip-licenses not installed - cannot scan"
}

#  Node.js: license-checker
if ((Get-Command npx -ErrorAction SilentlyContinue) -and (Test-Path "package.json")) {
    try {
        $nodeResult = npx license-checker --json 2>$null | ConvertFrom-Json
        $nodeResult.PSObject.Properties | ForEach-Object {
            $licenses = $_.Value.licenses
            if ($licenses -match $deniedPattern) {
                $violations += "Node: $($_.Name): $licenses"
            }
        }
    } catch {
        # license-checker failed, skip
    }
}

#  Report
if ($violations.Count -gt 0) {
    $logFile = Join-Path $LogDir "license-check-$(Get-Date -Format 'yyyyMMdd-HHmmss').json"
    $logEntry = @{
        timestamp = $timestamp
        event = "license_violations"
        mode = $Mode
        violations = $violations
    } | ConvertTo-Json -Compress
    $logEntry | Out-File -FilePath $logFile -Encoding utf8

    Write-Host "`n[License Check] Violations detected:" -ForegroundColor Yellow
    foreach ($v in $violations) {
        Write-Host "  - $v" -ForegroundColor Yellow
    }

    if ($Mode -eq "block") {
        Write-Host "[License Check] MODE=block - failing session." -ForegroundColor Red
        $exitCode = 1
    } else {
        Write-Host "[License Check] MODE=warn - review violations above." -ForegroundColor Yellow
    }
} else {
    Write-Host "[License Check] No license violations detected." -ForegroundColor Green
}

exit $exitCode
