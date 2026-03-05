#!/usr/bin/env zsh
emulate -L zsh
setopt PIPE_FAIL ERR_EXIT

# Install and configure Git

install_git() {
    emulate -L zsh
    setopt PIPE_FAIL ERR_EXIT

    if command -v git &>/dev/null; then
        echo "Git already installed: $(git --version)"
        return 0
    fi

    echo "Installing Git..."

    local os_type
    os_type="$(uname -s)"

    case "${os_type}" in
        Linux)
            if command -v apt-get &>/dev/null; then
                sudo apt-get update -qq
                sudo apt-get install -y -qq git
            elif command -v dnf &>/dev/null; then
                sudo dnf install -y git
            elif command -v pacman &>/dev/null; then
                sudo pacman -S --noconfirm git
            else
                echo "ERROR: Unsupported package manager"
                return 1
            fi
            ;;
        Darwin)
            if command -v brew &>/dev/null; then
                brew install git
            else
                xcode-select --install
            fi
            ;;
        *)
            echo "ERROR: Unsupported OS: ${os_type}"
            return 1
            ;;
    esac

    echo "Git installed: $(git --version)"
}

configure_git() {
    emulate -L zsh

    echo "Configuring Git recommended settings..."

    git config --global init.defaultBranch main
    git config --global core.autocrlf input
    git config --global pull.rebase true
    git config --global fetch.prune true
    git config --global diff.colorMoved zebra
    git config --global rerere.enabled true

    if [[ -z "$(git config --global user.name 2>/dev/null)" ]]; then
        echo ""
        echo -n "Enter your Git name: "
        read -r git_name
        if [[ -n "${git_name}" ]]; then
            git config --global user.name "${git_name}"
        fi
    fi

    if [[ -z "$(git config --global user.email 2>/dev/null)" ]]; then
        echo -n "Enter your Git email: "
        read -r git_email
        if [[ -n "${git_email}" ]]; then
            git config --global user.email "${git_email}"
        fi
    fi

    echo ""
    echo "=== Git Configuration ==="
    echo "Name:           $(git config --global user.name 2>/dev/null || echo 'NOT SET')"
    echo "Email:          $(git config --global user.email 2>/dev/null || echo 'NOT SET')"
    echo "Default branch: $(git config --global init.defaultBranch)"
    echo "Pull strategy:  $(git config --global pull.rebase)"
    echo ""
}

main() {
    emulate -L zsh
    setopt PIPE_FAIL ERR_EXIT

    install_git
    configure_git

    echo "Git setup complete"
}

main "$@"
