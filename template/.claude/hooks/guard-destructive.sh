#!/usr/bin/env bash
# Blocks destructive bash commands before execution.
# Reads JSON tool input from stdin, checks command against dangerous patterns.
set -euo pipefail

INPUT=$(cat)
CMD=$(echo "$INPUT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('command',''))" 2>/dev/null || echo "")

if [ -z "$CMD" ]; then
  exit 0
fi

DANGEROUS_PATTERNS=(
  "rm -rf /"
  "rm -rf ~"
  "rm -rf \*"
  "git push --force"
  "git push -f "
  "git reset --hard"
  "git clean -f"
  "git clean -fd"
  "git clean -fx"
  "DROP TABLE"
  "DROP DATABASE"
  "mkfs"
  "dd if="
  "--no-verify"
  "| bash"
  "| sh"
)

for pattern in "${DANGEROUS_PATTERNS[@]}"; do
  if echo "$CMD" | grep -qiF "$pattern"; then
    python3 -c "import json; print(json.dumps({'decision': 'block', 'reason': 'Blocked: matches destructive pattern. Confirm manually if intentional: $pattern'}))"
    exit 0
  fi
done

exit 0
