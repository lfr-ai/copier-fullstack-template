#!/usr/bin/env bash
# Reminds about uncommitted changes when Claude stops.
set -euo pipefail

if ! git rev-parse --is-inside-work-tree &>/dev/null; then
  exit 0
fi

STATUS=$(git status --porcelain 2>/dev/null || true)

if [ -n "$STATUS" ]; then
  echo ""
  echo "WARNING: Uncommitted changes detected:"
  git status --short
  echo ""
  echo "Run 'git add -p && git commit' to save your work."
fi

exit 0
