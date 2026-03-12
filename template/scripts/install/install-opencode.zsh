emulate -L zsh
setopt PIPE_FAIL ERR_EXIT

# Install OpenCode — AI-powered coding assistant
# https://opencode.ai

detect_platform() {
emulate -L zsh

local os_type
os_type="$(uname -s)"

case "${os_type}" in
Linux)
if [[ -f /proc/version ]] && grep -qi microsoft /proc/version; then
print "wsl"
else
print "linux"
fi
;;
Darwin) print "macos" ;;
*) print "unknown" ;;
esac
}

main() {
emulate -L zsh
setopt PIPE_FAIL ERR_EXIT

if command -v opencode &>/dev/null; then
print "OpenCode already installed: $(opencode --version 2>/dev/null || echo 'unknown version')"
return 0
fi

print "Installing OpenCode..."

local platform
platform="$(detect_platform)"

case "${platform}" in
linux|wsl|macos)
curl -fsSL https://opencode.ai/install | bash
;;
*)
print "Unsupported platform for OpenCode shell installer."
print "Try: npm i -g opencode-ai"
return 1
;;
esac

# Ensure it's on the PATH
if command -v opencode &>/dev/null; then
print "OpenCode installed successfully"
else
print "OpenCode installed. You may need to restart your shell or add ~/.local/bin to PATH."
fi
}

main "$@"
