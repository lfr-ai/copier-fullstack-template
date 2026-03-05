#!/usr/bin/env zsh
emulate -L zsh
setopt PIPE_FAIL ERR_EXIT

# Install Visual Studio Code on Linux/macOS/WSL

install_vscode_linux() {
    emulate -L zsh
    setopt PIPE_FAIL ERR_EXIT

    local arch
    arch="$(dpkg --print-architecture 2>/dev/null || echo amd64)"

    if command -v code &>/dev/null; then
        echo "VS Code already installed: $(code --version | head -1)"
        return 0
    fi

    echo "Installing VS Code for Linux (${arch})..."

    if command -v apt-get &>/dev/null; then
        sudo apt-get update -qq
        sudo apt-get install -y -qq wget gpg apt-transport-https
        wget -qO- https://packages.microsoft.com/keys/microsoft.asc \
            | gpg --dearmor > /tmp/packages.microsoft.gpg
        sudo install -D -o root -g root -m 644 /tmp/packages.microsoft.gpg \
            /etc/apt/keyrings/packages.microsoft.gpg
        echo "deb [arch=${arch} signed-by=/etc/apt/keyrings/packages.microsoft.gpg] \
            https://packages.microsoft.com/repos/code stable main" \
            | sudo tee /etc/apt/sources.list.d/vscode.list > /dev/null
        sudo apt-get update -qq
        sudo apt-get install -y -qq code
    elif command -v dnf &>/dev/null; then
        sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc
        echo -e "[code]\nname=Visual Studio Code\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\nenabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc" \
            | sudo tee /etc/yum.repos.d/vscode.repo > /dev/null
        sudo dnf install -y code
    else
        echo "ERROR: Unsupported package manager. Install VS Code manually: https://code.visualstudio.com/download"
        return 1
    fi

    echo "VS Code installed successfully: $(code --version | head -1)"
}

install_vscode_macos() {
    emulate -L zsh
    setopt PIPE_FAIL ERR_EXIT

    if command -v code &>/dev/null; then
        echo "VS Code already installed: $(code --version | head -1)"
        return 0
    fi

    echo "Installing VS Code for macOS..."

    if command -v brew &>/dev/null; then
        brew install --cask visual-studio-code
    else
        echo "ERROR: Homebrew not found. Install from: https://code.visualstudio.com/download"
        return 1
    fi

    echo "VS Code installed successfully"
}

main() {
    emulate -L zsh
    setopt PIPE_FAIL ERR_EXIT

    local os_type
    os_type="$(uname -s)"

    case "${os_type}" in
        Linux)  install_vscode_linux ;;
        Darwin) install_vscode_macos ;;
        *)
            echo "ERROR: Unsupported OS: ${os_type}"
            echo "Download VS Code from: https://code.visualstudio.com/download"
            return 1
            ;;
    esac

    echo "Installing recommended VS Code extensions..."
    local extensions=(
        ms-python.python
        ms-python.vscode-pylance
        charliermarsh.ruff
        ms-vscode-remote.remote-wsl
        ms-vscode-remote.remote-containers
        ms-azuretools.vscode-docker
        eamodio.gitlens
        dbaeumer.vscode-eslint
        esbenp.prettier-vscode
        bradlc.vscode-tailwindcss
        pkief.material-icon-theme
        tamasfe.even-better-toml
        redhat.vscode-yaml
        ms-python.debugpy
        hbenl.vscode-test-explorer
        task.vscode-task
    )

    for ext in "${extensions[@]}"; do
        code --install-extension "${ext}" --force 2>/dev/null || \
            echo "WARNING: Failed to install ${ext}"
    done

    echo "Extension installation complete"
}

main "$@"
