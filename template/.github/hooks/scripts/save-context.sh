#!/usr/bin/env sh
# PreCompact Context Saver — PreCompact hook
# Saves important context (modified files, git status, branch info)
# before the conversation is compacted. This prevents loss of critical
# working state when conversations get long.
#
# Environment:
#   CONTEXT_LOG_DIR    — log directory (default: logs/copilot/context)
#   SKIP_CONTEXT_SAVE  — set to "true" to disable
set -eu

# ── Early exit ───────────────────────────────────────────────────
if [ "${SKIP_CONTEXT_SAVE:-}" = "true" ]; then
  exit 0
fi

LOG_DIR="${CONTEXT_LOG_DIR:-logs/copilot/context}"
mkdir -p "${LOG_DIR}"

# ── Read stdin ───────────────────────────────────────────────────
INPUT="$(cat)"

TIMESTAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date +%Y-%m-%dT%H:%M:%SZ)"

if command -v jq >/dev/null 2>&1; then
  SESSION_ID="$(printf '%s' "${INPUT}" | jq -r '.sessionId // empty' 2>/dev/null || echo "")"
  TRIGGER="$(printf '%s' "${INPUT}" | jq -r '.trigger // "unknown"' 2>/dev/null || echo "unknown")"
  TRANSCRIPT_PATH="$(printf '%s' "${INPUT}" | jq -r '.transcript_path // empty' 2>/dev/null || echo "")"
else
  SESSION_ID="$(printf '%s' "${INPUT}" | sed -n 's/.*"sessionId"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)"
  TRIGGER="$(printf '%s' "${INPUT}" | sed -n 's/.*"trigger"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)"
  TRANSCRIPT_PATH=""
fi

# ── Collect working state ────────────────────────────────────────
BRANCH="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")"
MODIFIED_FILES="$(git diff --name-only 2>/dev/null | head -20 || echo "")"
STAGED_FILES="$(git diff --cached --name-only 2>/dev/null | head -20 || echo "")"
UNTRACKED="$(git ls-files --others --exclude-standard 2>/dev/null | head -10 || echo "")"
LAST_COMMIT="$(git log --oneline -1 2>/dev/null || echo "no commits")"

# Build context summary
CONTEXT="Working state before compaction:"
CONTEXT="${CONTEXT}\n- Branch: ${BRANCH}"
CONTEXT="${CONTEXT}\n- Last commit: ${LAST_COMMIT}"
if [ -n "${MODIFIED_FILES}" ]; then
  CONTEXT="${CONTEXT}\n- Modified files: $(printf '%s' "${MODIFIED_FILES}" | tr '\n' ', ')"
fi
if [ -n "${STAGED_FILES}" ]; then
  CONTEXT="${CONTEXT}\n- Staged files: $(printf '%s' "${STAGED_FILES}" | tr '\n' ', ')"
fi
if [ -n "${UNTRACKED}" ]; then
  CONTEXT="${CONTEXT}\n- Untracked files: $(printf '%s' "${UNTRACKED}" | tr '\n' ', ')"
fi

# ── Log ──────────────────────────────────────────────────────────
LOG_ENTRY="{\"timestamp\":\"${TIMESTAMP}\",\"event\":\"pre_compact\",\"sessionId\":\"${SESSION_ID}\",\"trigger\":\"${TRIGGER}\",\"branch\":\"${BRANCH}\"}"
printf '%s\n' "${LOG_ENTRY}" >> "${LOG_DIR}/compact.log"

# Save transcript path for potential recovery
if [ -n "${TRANSCRIPT_PATH}" ]; then
  printf '%s %s\n' "${TIMESTAMP}" "${TRANSCRIPT_PATH}" >> "${LOG_DIR}/transcripts.log"
fi

# Output additionalContext so the agent retains working state after compaction
printf '{"hookSpecificOutput":{"hookEventName":"PreCompact","additionalContext":"%s"}}\n' \
  "$(printf '%b' "${CONTEXT}" | tr '\n' ' ' | sed 's/"/\\"/g')"

exit 0
