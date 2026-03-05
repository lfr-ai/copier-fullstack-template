#!/usr/bin/env zsh
emulate -L zsh
setopt PIPE_FAIL ERR_EXIT

# Install Task CLI (taskfile.dev)

install_task() {
    emulate -L zsh
    setopt PIPE_FAIL ERR_EXIT

    if command -v task &>/dev/null; then
        echo "Task already installed: $(task --version)"
        return 0
    fi

    echo "Installing Task..."

    local os_type
    os_type="$(uname -s)"

    case "${os_type}" in
        Linux)
            sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d -b ~/.local/bin
            export PATH="${HOME}/.local/bin:${PATH}"
            ;;
        Darwin)
            if command -v brew &>/dev/null; then
                brew install go-task
            else
                sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d -b /usr/local/bin
            fi
            ;;
        *)
            echo "ERROR: Unsupported OS: ${os_type}"
            echo "Install from: https://taskfile.dev/installation/"
            return 1
            ;;
    esac

    echo "Task installed: $(task --version)"
}

install_task
