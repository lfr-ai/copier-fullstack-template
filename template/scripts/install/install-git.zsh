emulate -L zsh
setopt PIPE_FAIL ERR_EXIT


install_git() {
    emulate -L zsh
    setopt PIPE_FAIL ERR_EXIT

    if command -v git &>/dev/null; then
        print "Git already installed: $(git --version)"
        return 0
    fi

    print "Installing Git..."

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
                print "ERROR: Unsupported package manager"
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
            print "ERROR: Unsupported OS: ${os_type}"
            return 1
            ;;
    esac

    print "Git installed: $(git --version)"
}

configure_git() {
    emulate -L zsh

    print "Configuring Git recommended settings..."

    git config --global init.defaultBranch main
    git config --global core.autocrlf input
    git config --global pull.rebase true
    git config --global fetch.prune true
    git config --global diff.colorMoved zebra
    git config --global rerere.enabled true

    if [[ -z "$(git config --global user.name 2>/dev/null)" ]]; then
        print ""
        print -n "Enter your Git name: "
        local git_name
        read -r git_name
        if [[ -n "${git_name}" ]]; then
            git config --global user.name "${git_name}"
        fi
    fi

    if [[ -z "$(git config --global user.email 2>/dev/null)" ]]; then
        print -n "Enter your Git email: "
        local git_email
        read -r git_email
        if [[ -n "${git_email}" ]]; then
            git config --global user.email "${git_email}"
        fi
    fi

    print ""
    print "=== Git Configuration ==="
    print "Name:           $(git config --global user.name 2>/dev/null || print 'NOT SET')"
    print "Email:          $(git config --global user.email 2>/dev/null || print 'NOT SET')"
    print "Default branch: $(git config --global init.defaultBranch)"
    print "Pull strategy:  $(git config --global pull.rebase)"
    print ""
}

main() {
    emulate -L zsh
    setopt PIPE_FAIL ERR_EXIT

    install_git
    configure_git

    print "Git setup complete"
}

main "$@"
