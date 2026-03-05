#!/usr/bin/env zsh
emulate -L zsh
setopt PIPE_FAIL ERR_EXIT

# Setup devcontainer CLI and verify configuration

setup_devcontainer_cli() {
    emulate -L zsh
    setopt PIPE_FAIL ERR_EXIT

    if command -v devcontainer &>/dev/null; then
        echo "devcontainer CLI already installed: $(devcontainer --version)"
        return 0
    fi

    echo "Installing devcontainer CLI..."

    if command -v pnpm &>/dev/null; then
        pnpm add -g @devcontainers/cli
    elif command -v npm &>/dev/null; then
        npm install -g @devcontainers/cli
    else
        echo "ERROR: pnpm or npm required to install devcontainer CLI"
        return 1
    fi

    echo "devcontainer CLI installed: $(devcontainer --version)"
}

verify_devcontainer_config() {
    emulate -L zsh

    local config_path=".devcontainer/devcontainer.json"

    if [[ ! -f "${config_path}" ]]; then
        echo "WARNING: ${config_path} not found"
        return 1
    fi

    echo "Devcontainer config found at ${config_path}"
    echo ""
    echo "To use:"
    echo "  1. Open this folder in VS Code"
    echo "  2. Press Ctrl+Shift+P -> 'Reopen in Container'"
    echo "  3. Or run: devcontainer up --workspace-folder ."
}

main() {
    emulate -L zsh
    setopt PIPE_FAIL ERR_EXIT

    setup_devcontainer_cli
    verify_devcontainer_config

    echo ""
    echo "Devcontainer setup complete"
}

main "$@"
