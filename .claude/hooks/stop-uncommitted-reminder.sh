#!/usr/bin/env bash
# Remind about uncommitted changes when stopping Claude Code session
# Non-blocking — just informational

set -euo pipefail

if ! command -v git &> /dev/null; then
  exit 0
fi

# Check if we're in a git repository
if ! git rev-parse --git-dir &> /dev/null; then
  exit 0
fi

# Check for uncommitted changes (staged or unstaged)
if ! git diff-index --quiet HEAD -- 2>/dev/null; then
  echo "⚠️  You have uncommitted changes in the working tree." >&2
  echo "   Run 'git status' to review, then commit or stash before closing." >&2
fi

# Always exit 0 (non-blocking)
exit 0
