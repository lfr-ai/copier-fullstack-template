---
description: Prevents terminal heredoc file corruption in VS Code Copilot
applyTo: "**"
---

# No Heredoc File Operations

## Rule

**NEVER use shell heredocs (`cat << 'EOF'`, `tee << EOF`, `echo "..." > file`) to
create or modify files.** Always use file editing tools instead.

## Why

Shell heredocs through terminal commands can silently corrupt files:

- Unicode characters (box-drawing chars, em-dashes, smart quotes) get stripped
- Line endings may be mangled (CRLF vs LF)
- Indentation can shift unexpectedly
- PowerShell heredocs (`@'...'@`) strip non-ASCII characters entirely
- Encoding mismatches between shell and file system cause data loss

## Instead

| Bad (heredoc) | Good (tool) |
|---------------|-------------|
| `cat << 'EOF' > file.md` | Use file editing tools to create files |
| `echo "content" > file.sh` | Use file editing tools to write content |
| `tee << EOF > config.json` | Use file editing tools to create JSON |
| PowerShell `@'...'@ > file` | Use file editing tools for all file writes |

## Exceptions

- Single-line `echo` for trivial content (no special characters)
- `mkdir -p` for creating directories (not file content)
- Terminal commands that READ files (`cat`, `head`, `tail`) are fine
