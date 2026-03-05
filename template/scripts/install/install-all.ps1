# Windows master installer
# Run from PowerShell as Administrator

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "============================================"
Write-Host "  Windows Development Environment Setup"
Write-Host "============================================"
Write-Host ""

# Step 1: Install WSL2
Write-Host "--- Step 1: WSL2 ---"
$wsl2Script = Join-Path $ScriptDir "install-wsl2.ps1"
if (Test-Path $wsl2Script) {
    & $wsl2Script
} else {
    Write-Host "WARNING: install-wsl2.ps1 not found at $wsl2Script"
}

# Step 2: Install VS Code
Write-Host ""
Write-Host "--- Step 2: VS Code ---"
$vscodeScript = Join-Path $ScriptDir "install-vscode.ps1"
if (Test-Path $vscodeScript) {
    & $vscodeScript
} else {
    Write-Host "WARNING: install-vscode.ps1 not found at $vscodeScript"
}

Write-Host ""
Write-Host "============================================"
Write-Host "  Windows setup complete"
Write-Host "============================================"
Write-Host ""
Write-Host "Next steps (run inside WSL/Ubuntu):"
Write-Host "  1. Open Ubuntu from Start Menu"
Write-Host "  2. Navigate to your project directory"
Write-Host "  3. Run: zsh scripts/install/install-all.zsh"
Write-Host ""
Write-Host "This will install Git, Zsh, Python, Node.js,"
Write-Host "pnpm, Docker, Task CLI, and VS Code extensions"
Write-Host ""
