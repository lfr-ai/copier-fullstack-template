
$ErrorActionPreference = "Stop"

function Test-WSLInstalled {
    try {
        $result = wsl --status 2>$null
        return $LASTEXITCODE -eq 0
    }
    catch {
        return $false
    }
}

function Test-WindowsVersion {
    $os = Get-CimInstance Win32_OperatingSystem
    $build = [int]$os.BuildNumber
    if ($build -lt 19041) {
        Write-Warning "WSL2 requires Windows 10 version 2004 (build 19041) or later."
        Write-Warning "Current build: $build"
        return $false
    }
    return $true
}

function Install-WSL2 {
    if (Test-WSLInstalled) {
        Write-Host "WSL2 is already installed"
        wsl --version
        return
    }

    if (-not (Test-WindowsVersion)) {
        Write-Warning "Cannot install WSL2 on this Windows version."
        return
    }

    Write-Host "Installing WSL2 with Ubuntu..."
    wsl --install --distribution Ubuntu

    Write-Host ""
    Write-Host "========================================"
    Write-Host "WSL2 installation initiated."
    Write-Host "A RESTART IS REQUIRED to complete setup."
    Write-Host "========================================"
    Write-Host ""
    Write-Host "After restart:"
    Write-Host "  1. Open Ubuntu from Start Menu"
    Write-Host "  2. Create your Unix username and password"
    Write-Host "  3. Run: sudo sh -c 'echo [boot] > /etc/wsl.conf && echo systemd=true >> /etc/wsl.conf'"
    Write-Host "  4. Restart WSL: wsl --shutdown && wsl"
    Write-Host ""

    $restart = Read-Host "Restart now? (Y/n)"
    if ($restart -ne "n") {
        Write-Host "Restarting in 10 seconds. Save your work!"
        Start-Sleep -Seconds 10
        Restart-Computer
    }
}

Install-WSL2
