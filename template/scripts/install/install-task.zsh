emulate -L zsh
setopt PIPE_FAIL ERR_EXIT


install_task() {
    emulate -L zsh
    setopt PIPE_FAIL ERR_EXIT

    if command -v task &>/dev/null; then
        print "Task already installed: $(task --version)"
        return 0
    fi

    print "Installing Task..."

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
            print "ERROR: Unsupported OS: ${os_type}"
            print "Install from: https://taskfile.dev/installation/"
            return 1
            ;;
    esac

    print "Task installed: $(task --version)"
}

main() {
    emulate -L zsh
    setopt PIPE_FAIL ERR_EXIT

    install_task
}

main "$@"
