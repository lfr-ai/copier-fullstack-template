#!/usr/bin/env zsh
emulate -L zsh
setopt PIPE_FAIL ERR_EXIT


install_bun() {
emulate -L zsh
setopt PIPE_FAIL ERR_EXIT

if command -v bun &>/dev/null; then
  local current_version
  current_version="$(bun --version 2>/dev/null || echo "unknown")"
  print "Bun already installed: ${current_version}"
  print "Upgrading Bun..."
  bun upgrade || true
  print "Bun version: $(bun --version)"
  return 0
fi

print "Installing Bun..."
curl -fsSL https://bun.sh/install | bash

# Source shell profile to get bun in PATH
export BUN_INSTALL="${HOME}/.bun"
export PATH="${BUN_INSTALL}/bin:${PATH}"

if ! command -v bun &>/dev/null; then
  print "ERROR: Bun installation failed"
  return 1
fi

print "Bun installed: $(bun --version)"
}

main() {
emulate -L zsh
setopt PIPE_FAIL ERR_EXIT

install_bun
}

main "$@"
