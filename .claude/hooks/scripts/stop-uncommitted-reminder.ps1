# Reminds about uncommitted changes when Claude stops.
param()

try {
    $null = git rev-parse --is-inside-work-tree 2>&1
    if ($LASTEXITCODE -ne 0) { exit 0 }
} catch {
    exit 0
}

$status = git status --short 2>&1
if ($status) {
    Write-Host ""
    Write-Host "WARNING: Uncommitted changes detected:" -ForegroundColor Yellow
    git status --short
    Write-Host ""
    Write-Host "Run 'git add -p && git commit' to save your work." -ForegroundColor Cyan
}

exit 0
