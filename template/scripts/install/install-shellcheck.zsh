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

    if command -v shellcheck &>/dev/null; then
        print "ShellCheck already installed: $(shellcheck --version | head -2 | tail -1)"
        return 0
    fi

    print "Installing ShellCheck..."

    local platform
    platform="$(detect_platform)"

    case "${platform}" in
        linux)
            if command -v apt-get &>/dev/null; then
                sudo apt-get update -qq && sudo apt-get install -y -qq shellcheck
            elif command -v dnf &>/dev/null; then
                sudo dnf install -y shellcheck
            elif command -v pacman &>/dev/null; then
                sudo pacman -S --noconfirm shellcheck
            else
                print "WARNING: Unsupported Linux package manager — install ShellCheck manually"
                return 0
            fi
            ;;
        macos)
            if command -v brew &>/dev/null; then
                brew install shellcheck
            else
                print "WARNING: Homebrew not found — install ShellCheck manually"
                return 0
            fi
            ;;
        *)
            print "WARNING: Unsupported platform for ShellCheck installation"
            return 0
            ;;
    esac

    print "ShellCheck installed: $(shellcheck --version | head -2 | tail -1)"
}

main "$@"
