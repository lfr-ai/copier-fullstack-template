#!/usr/bin/env sh
# Auto-Format — PostToolUse hook
# Runs formatters on files modified by the Copilot coding agent after edits.
# Detects file type and applies the appropriate formatter (ruff for Python,
# biome for JS/TS/CSS/JSON).
#
# Environment:
#   SKIP_AUTO_FORMAT — set to "true" to disable
set -eu

# ── Early exit ───────────────────────────────────────────────────
if [ "${SKIP_AUTO_FORMAT:-}" = "true" ]; then
  exit 0
fi

# ── Read stdin ───────────────────────────────────────────────────
INPUT="$(cat)"

# Extract tool name and file path from JSON stdin
if command -v jq >/dev/null 2>&1; then
  TOOL_NAME="$(printf '%s' "${INPUT}" | jq -r '.tool_name // empty' 2>/dev/null || echo "")"
  FILE_PATH="$(printf '%s' "${INPUT}" | jq -r '.tool_input.filePath // .tool_input.file_path // empty' 2>/dev/null || echo "")"
else
  TOOL_NAME="$(printf '%s' "${INPUT}" | sed -n 's/.*"tool_name"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)"
  FILE_PATH="$(printf '%s' "${INPUT}" | sed -n 's/.*"filePath"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)"
  if [ -z "${FILE_PATH}" ]; then
    FILE_PATH="$(printf '%s' "${INPUT}" | sed -n 's/.*"file_path"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)"
  fi
fi

# Only run for file-editing tools
case "${TOOL_NAME}" in
  create_file|replace_string_in_file|editFiles|edit_file|multi_replace_string_in_file) ;;
  *) exit 0 ;;
esac

# Skip if no file path
if [ -z "${FILE_PATH}" ]; then
  exit 0
fi

# Skip if file doesn't exist
if [ ! -f "${FILE_PATH}" ]; then
  exit 0
fi

# ── Determine formatter ──────────────────────────────────────────
case "${FILE_PATH}" in
  *.py)
    # Python — use ruff if available
    if command -v ruff >/dev/null 2>&1; then
      ruff format --quiet "${FILE_PATH}" 2>/dev/null || true
      ruff check --fix --quiet "${FILE_PATH}" 2>/dev/null || true
    fi
    ;;
  *.ts|*.tsx|*.js|*.jsx|*.css|*.json)
    # Frontend/config — use biome if available
    if command -v bunx >/dev/null 2>&1; then
      bunx biome check --write "${FILE_PATH}" 2>/dev/null || true
    fi
    ;;
esac

exit 0
