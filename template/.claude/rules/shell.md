---
name: Shell Conventions
description: zsh scripting standards and Azure CLI conventions
paths:
  - "**/*.zsh"
  - "**/*.azcli"
  - "scripts/**"
---

# Shell Conventions

## zsh Requirements

- ALL scripts use `.zsh` extension (never `.sh` or `.bash`)
- Shebang: `#!/usr/bin/env zsh`
- Reset state: `emulate -L zsh` at top of every script and function
- Safety: `setopt PIPE_FAIL` and `setopt ERR_EXIT`
- Variables inside functions: always `local`
- Option parsing: `zparseopts`

## Azure CLI Scripts

- Use `.azcli` extension for Azure CLI command collections
- Must also be valid zsh (same header and idioms)
- Group related `az` commands logically
- Always check command exit codes

## Script Organization

- `scripts/install/` — one-time setup installers
- `scripts/` — operational scripts (bootstrap, health-check, seed)
- Functions should be self-contained with `emulate -L zsh`
- Prefer functions over long inline scripts

## Forbidden Patterns

- Never use `.sh` extension
- Never use bash-isms (`[[ ]]` is fine in zsh, but avoid bash-only features)
- Never use heredoc for file creation (use `print -r -- "content" > file`)
- Never source user-specific paths without checking existence
