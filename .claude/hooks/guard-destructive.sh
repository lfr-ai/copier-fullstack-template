#!/usr/bin/env bash
# Guard against destructive bash commands in Claude Code
# Blocks force-push, hard reset, recursive deletion, etc.
# Exit 0 = allow, Exit 1 = block

set -euo pipefail

# Read TOOL_INPUT from environment (JSON payload from Claude)
TOOL_INPUT="${TOOL_INPUT:-}"

if [ -z "$TOOL_INPUT" ]; then
  exit 0
fi

# Extract command from JSON (handle both Bash tool formats)
COMMAND=$(echo "$TOOL_INPUT" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    # Try 'command' field first (standard), then 'arguments' (alternative)
    cmd = data.get('command', data.get('arguments', ''))
    print(cmd if isinstance(cmd, str) else '')
except:
    pass
" 2>/dev/null || echo "")

if [ -z "$COMMAND" ]; then
  exit 0
fi

# Destructive patterns (case-insensitive)
DANGEROUS_PATTERNS=(
  "rm -rf /"
  "rm -rf ~"
  "rm -rf \$HOME"
  "git push --force"
  "git push -f"
  "git reset --hard"
  "git clean -fd"
  "git clean -fx"
  "git stash drop"
  "git stash clear"
  "git branch -D"
  "curl.*|.*bash"
  "wget.*|.*bash"
  "chmod 777"
  "> /dev/sda"
  "mkfs"
  "dd if="
  ":(){ :|:& };:"
)

for pattern in "${DANGEROUS_PATTERNS[@]}"; do
  if echo "$COMMAND" | grep -qiE "$pattern"; then
    echo "⛔ BLOCKED: Destructive command detected: $pattern" >&2
    echo "Command: $COMMAND" >&2
    exit 1
  fi
done

# Block operations on critical files/dirs
PROTECTED_PATHS=(
  "/.git"
  "/.env"
  "/secrets"
  "/.ssh"
)

for path in "${PROTECTED_PATHS[@]}"; do
  if echo "$COMMAND" | grep -qE "rm.*${path}"; then
    echo "⛔ BLOCKED: Attempt to delete protected path: $path" >&2
    exit 1
  fi
done

# Allow command
exit 0
