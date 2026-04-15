---
description: Shell and PowerShell scripting conventions for hook scripts and CI tooling
applyTo: "**/*.{sh,ps1}"
---

# Shell Script Conventions

## Bash/sh Scripts

- Start with `#!/usr/bin/env sh` (POSIX) or `#!/usr/bin/env bash` (bash features)
- Use `set -eu` for strict error handling
- Quote all variable expansions: `"${VAR}"`
- Use `command -v` to check for tool availability
- Exit with appropriate codes: 0 (success), 1 (error), 2 (blocked)

## PowerShell Scripts

- Use `param()` block at top for parameters
- Use `$env:VAR` for environment variables
- Prefer cmdlets over aliases in scripts (`Write-Host` not `echo`)
- Use `Test-Path` for file existence checks
- Handle `ConvertFrom-Json` errors with try/catch

## Hook Scripts

- Read JSON from stdin (tool context)
- Parse with `jq` (sh) or `ConvertFrom-Json` (ps1)
- Log structured JSON to the designated log directory
- Exit 0 to allow, exit 2 to block (for PreToolUse hooks)

## Cross-Platform

- Every `.sh` script MUST have a matching `.ps1` equivalent
- Use the same logic and patterns in both
- Test on both Linux/macOS and Windows
