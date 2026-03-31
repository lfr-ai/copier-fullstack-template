#!/usr/bin/env sh
# Session Logger — SessionStart / UserPromptSubmit / Stop hook
# Logs Copilot coding agent session activity for audit and analysis.
# Writes structured JSON Lines to separate log files per event type.
#
# Environment:
#   SESSION_LOG_DIR — log directory (default: logs/copilot/sessions)
#   SKIP_LOGGING    — set to "true" to disable
#   LOG_LEVEL       — "DEBUG", "INFO" (default), "ERROR"
set -eu

# ── Early exit ───────────────────────────────────────────────────
if [ "${SKIP_LOGGING:-}" = "true" ]; then
  exit 0
fi

LOG_DIR="${SESSION_LOG_DIR:-logs/copilot/sessions}"
LOG_LEVEL="${LOG_LEVEL:-INFO}"

mkdir -p "${LOG_DIR}"

# ── Read stdin ───────────────────────────────────────────────────
INPUT="$(cat)"

TIMESTAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date +%Y-%m-%dT%H:%M:%SZ)"

# Extract event type
if command -v jq >/dev/null 2>&1; then
  EVENT="$(printf '%s' "${INPUT}" | jq -r '.hookEventName // empty' 2>/dev/null || echo "")"
  SESSION_ID="$(printf '%s' "${INPUT}" | jq -r '.sessionId // empty' 2>/dev/null || echo "")"
  CWD="$(printf '%s' "${INPUT}" | jq -r '.cwd // empty' 2>/dev/null || echo "")"
else
  EVENT="$(printf '%s' "${INPUT}" | sed -n 's/.*"hookEventName"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)"
  SESSION_ID="$(printf '%s' "${INPUT}" | sed -n 's/.*"sessionId"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)"
  CWD="$(printf '%s' "${INPUT}" | sed -n 's/.*"cwd"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)"
fi

# ── Log events ───────────────────────────────────────────────────
case "${EVENT}" in
  SessionStart)
    LOG_ENTRY="{\"timestamp\":\"${TIMESTAMP}\",\"event\":\"session_start\",\"sessionId\":\"${SESSION_ID}\",\"cwd\":\"${CWD}\"}"
    printf '%s\n' "${LOG_ENTRY}" >> "${LOG_DIR}/session.log"
    # Inject rich project context at session start
    BRANCH="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")"
    LAST_COMMIT="$(git log --oneline -1 2>/dev/null || echo "no commits")"
    MODIFIED_COUNT="$(git diff --name-only 2>/dev/null | wc -l | tr -d ' ')"
    STAGED_COUNT="$(git diff --cached --name-only 2>/dev/null | wc -l | tr -d ' ')"
    PY_VER="$(python3 --version 2>/dev/null | cut -d' ' -f2 || echo "unknown")"
    NODE_VER="$(node --version 2>/dev/null || echo "unknown")"
    CONTEXT="Session audit trail: ${LOG_DIR}/session.log"
    CONTEXT="${CONTEXT} | Branch: ${BRANCH} | Last commit: ${LAST_COMMIT}"
    CONTEXT="${CONTEXT} | Modified files: ${MODIFIED_COUNT} | Staged files: ${STAGED_COUNT}"
    CONTEXT="${CONTEXT} | Python: ${PY_VER} | Node: ${NODE_VER}"
    printf '{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"%s"}}\n' "${CONTEXT}"
    ;;
  UserPromptSubmit)
    if [ "${LOG_LEVEL}" = "DEBUG" ]; then
      LOG_ENTRY="{\"timestamp\":\"${TIMESTAMP}\",\"event\":\"prompt_submitted\",\"sessionId\":\"${SESSION_ID}\"}"
      printf '%s\n' "${LOG_ENTRY}" >> "${LOG_DIR}/prompts.log"
    fi
    ;;
  Stop)
    LOG_ENTRY="{\"timestamp\":\"${TIMESTAMP}\",\"event\":\"session_end\",\"sessionId\":\"${SESSION_ID}\"}"
    printf '%s\n' "${LOG_ENTRY}" >> "${LOG_DIR}/session.log"
    ;;
  PreCompact)
    TRIGGER="$(printf '%s' "${INPUT}" | jq -r '.trigger // "unknown"' 2>/dev/null || echo "unknown")"
    LOG_ENTRY="{\"timestamp\":\"${TIMESTAMP}\",\"event\":\"pre_compact\",\"sessionId\":\"${SESSION_ID}\",\"trigger\":\"${TRIGGER}\"}"
    printf '%s\n' "${LOG_ENTRY}" >> "${LOG_DIR}/session.log"
    ;;
  SubagentStart)
    AGENT_ID="$(printf '%s' "${INPUT}" | jq -r '.agent_id // empty' 2>/dev/null || echo "")"
    AGENT_TYPE="$(printf '%s' "${INPUT}" | jq -r '.agent_type // empty' 2>/dev/null || echo "")"
    LOG_ENTRY="{\"timestamp\":\"${TIMESTAMP}\",\"event\":\"subagent_start\",\"sessionId\":\"${SESSION_ID}\",\"agentId\":\"${AGENT_ID}\",\"agentType\":\"${AGENT_TYPE}\"}"
    printf '%s\n' "${LOG_ENTRY}" >> "${LOG_DIR}/session.log"
    ;;
  SubagentStop)
    AGENT_ID="$(printf '%s' "${INPUT}" | jq -r '.agent_id // empty' 2>/dev/null || echo "")"
    AGENT_TYPE="$(printf '%s' "${INPUT}" | jq -r '.agent_type // empty' 2>/dev/null || echo "")"
    LOG_ENTRY="{\"timestamp\":\"${TIMESTAMP}\",\"event\":\"subagent_stop\",\"sessionId\":\"${SESSION_ID}\",\"agentId\":\"${AGENT_ID}\",\"agentType\":\"${AGENT_TYPE}\"}"
    printf '%s\n' "${LOG_ENTRY}" >> "${LOG_DIR}/session.log"
    ;;
  PreToolUse|PostToolUse)
    if [ "${LOG_LEVEL}" = "DEBUG" ]; then
      TOOL_NAME="$(printf '%s' "${INPUT}" | jq -r '.tool_name // empty' 2>/dev/null || echo "")"
      LOG_ENTRY="{\"timestamp\":\"${TIMESTAMP}\",\"event\":\"${EVENT}\",\"sessionId\":\"${SESSION_ID}\",\"tool\":\"${TOOL_NAME}\"}"
      printf '%s\n' "${LOG_ENTRY}" >> "${LOG_DIR}/session.log"
    fi
    ;;
  *)
    LOG_ENTRY="{\"timestamp\":\"${TIMESTAMP}\",\"event\":\"unknown\",\"hookEventName\":\"${EVENT}\",\"sessionId\":\"${SESSION_ID}\"}"
    printf '%s\n' "${LOG_ENTRY}" >> "${LOG_DIR}/session.log"
    ;;
esac

exit 0
