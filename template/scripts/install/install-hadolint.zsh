emulate -L zsh
setopt PIPE_FAIL ERR_EXIT


detect_platform() {
    emulate -L zsh
    local os_type
    os_type="$(uname -s)"
    case "${os_type}" in
        Linux)  print "linux" ;;
        Darwin) print "macos" ;;
        *)      print "unknown" ;;
    esac
}

main() {
    emulate -L zsh
    setopt PIPE_FAIL ERR_EXIT

    if command -v hadolint &>/dev/null; then
        print "hadolint already installed: $(hadolint --version 2>&1 | head -1)"
        return 0
    fi

    print "Installing hadolint..."

    local platform arch
    platform="$(detect_platform)"
    arch="$(uname -m)"

    case "${platform}" in
        linux)
            if command -v apt-get &>/dev/null; then
                local hadolint_url="https://github.com/hadolint/hadolint/releases/latest/download/hadolint-Linux-${arch}"
                sudo curl -L "${hadolint_url}" -o /usr/local/bin/hadolint 2>/dev/null && \
                    sudo chmod +x /usr/local/bin/hadolint || {
                    print "WARNING: Could not install hadolint binary — install manually or use Docker"
                    return 0
                }
            elif command -v pacman &>/dev/null; then
                sudo pacman -S --noconfirm hadolint 2>/dev/null || {
                    print "WARNING: hadolint not in package manager — install from GitHub releases"
                    return 0
                }
            else
                print "WARNING: Unsupported Linux package manager — install hadolint manually"
                return 0
            fi
            ;;
        macos)
            if command -v brew &>/dev/null; then
                brew install hadolint
            else
                print "WARNING: Homebrew not found — install hadolint manually"
                return 0
            fi
            ;;
        *)
            print "WARNING: Unsupported platform for hadolint installation"
            return 0
            ;;
    esac

    print "hadolint installed: $(hadolint --version 2>&1 | head -1)"
}

main "$@"
