---
description: Zsh shell scripting conventions and Azure CLI patterns
applyTo: "**/*.zsh, **/*.azcli, scripts/**"
---

- `.zsh` extension always — never `.sh` or `.bash`
- `.azcli` extension for Azure CLI command collections (valid zsh)
- Shebang: `#!/usr/bin/env zsh`
- Reset state at top: `emulate -L zsh`
- Safety options: `setopt PIPE_FAIL ERR_EXIT`
- `local` for all variables inside functions
- All variables double-quoted: `"${var}"`
- `zparseopts` for option parsing
- `command -v` instead of `which` for executable detection
- `mktemp` instead of hardcoded `/tmp/` paths
- ShellCheck compliant

- Each script has a main function or guard
- Source shared helpers via `source "${0:A:h}/lib/common.zsh"` pattern
- Use `printf` over `echo` for portability
- `trap` for cleanup on exit
- Heredoc for multi-line strings: `<<'EOF'`

- Never use `sudo` without explicit justification
- Never pipe curl/wget output directly to shell
- Validate checksums for downloaded binaries
- Use `/etc/apt/keyrings/` for GPG keys (not `/usr/share/keyrings/`)
- Prefer package managers over manual binary installs
