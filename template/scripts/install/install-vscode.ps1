
$ErrorActionPreference = "Stop"

function Install-VSCode {
    if (Get-Command code -ErrorAction SilentlyContinue) {
        Write-Host "VS Code already installed: $(code --version | Select-Object -First 1)"
        return
    }

    Write-Host "Downloading VS Code installer..."
    $installerUrl = "https://update.code.visualstudio.com/latest/win32-x64-user/stable"
    $installerPath = Join-Path $env:TEMP "VSCodeSetup.exe"

    Invoke-WebRequest -Uri $installerUrl -OutFile $installerPath -UseBasicParsing

    Write-Host "Installing VS Code..."
    Start-Process -FilePath $installerPath -ArgumentList @(
        "/VERYSILENT",
        "/NORESTART",
        "/MERGETASKS=!runcode,addcontextmenufiles,addcontextmenufolders,associatewithfiles,addtopath"
    ) -Wait

    Remove-Item $installerPath -Force
    Write-Host "VS Code installed successfully"

    $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")
}

function Install-Extensions {
    Write-Host "Installing recommended VS Code extensions..."
    $extensions = @(
        "ms-python.python",
        "ms-python.vscode-pylance",
        "ms-python.debugpy",
        "charliermarsh.ruff",
        "ms-vscode-remote.remote-wsl",
        "ms-vscode-remote.remote-containers",
        "ms-azuretools.vscode-containers",
        "github.copilot-chat",
        "eamodio.gitlens",
        "anseki.vscode-color",
        "biomejs.biome",
        "bradlc.vscode-tailwindcss",
        "vscode-icons-team.vscode-icons",
        "tamasfe.even-better-toml",
        "redhat.vscode-yaml",
        "samuelcolvin.jinjahtml",
        "streetsidesoftware.code-spell-checker",
        "editorconfig.editorconfig",
        "exiasr.hadolint",
        "timonwong.shellcheck",
        "davidanson.vscode-markdownlint",
        "vitest.explorer",
        "task.vscode-task"
    )

    foreach ($ext in $extensions) {
        try {
            code --install-extension $ext --force 2>$null
        }
        catch {
            Write-Warning "Failed to install extension: $ext"
        }
    }
    Write-Host "Extension installation complete"
}

Install-VSCode
Install-Extensions
