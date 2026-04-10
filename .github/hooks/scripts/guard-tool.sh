#!/usr/bin/env sh
# Tool Guardian — PreToolUse hook
# Blocks dangerous tool operations before the Copilot coding agent executes them.
# Scans for destructive file ops, force pushes, DB drops, permission abuse,
# network exfiltration, and system danger patterns.
#
# Environment:
#   GUARD_MODE           — "block" (default) or "warn"
#   SKIP_TOOL_GUARD      — set to "true" to disable
#   TOOL_GUARD_LOG_DIR   — log directory (default: logs/copilot/tool-guardian)
#   TOOL_GUARD_ALLOWLIST — comma-separated patterns to skip
set -eu

# ── Early exit ───────────────────────────────────────────────────
if [ "${SKIP_TOOL_GUARD:-}" = "true" ]; then
  exit 0
fi

GUARD_MODE="${GUARD_MODE:-block}"
LOG_DIR="${TOOL_GUARD_LOG_DIR:-logs/copilot/tool-guardian}"
ALLOWLIST="${TOOL_GUARD_ALLOWLIST:-}"

mkdir -p "${LOG_DIR}"

# ── Read stdin ───────────────────────────────────────────────────
INPUT="$(cat)"

# Extract tool_name and tool_input from JSON stdin
if command -v jq >/dev/null 2>&1; then
  TOOL_NAME="$(printf '%s' "${INPUT}" | jq -r '.tool_name // empty' 2>/dev/null || echo "")"
  TOOL_INPUT="$(printf '%s' "${INPUT}" | jq -r '.tool_input // empty' 2>/dev/null || echo "")"
  # For tools that pass objects, stringify the input
  if [ -z "${TOOL_INPUT}" ]; then
    TOOL_INPUT="$(printf '%s' "${INPUT}" | jq -r '.tool_input | tostring' 2>/dev/null || echo "")"
  fi
else
  # Fallback: regex extraction
  TOOL_NAME="$(printf '%s' "${INPUT}" | sed -n 's/.*"tool_name"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)"
  TOOL_INPUT="$(printf '%s' "${INPUT}" | sed -n 's/.*"tool_input"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)"
  if [ -z "${TOOL_INPUT}" ]; then
    TOOL_INPUT="${INPUT}"
  fi
fi

# Combined text for scanning
SCAN_TEXT="${TOOL_NAME} ${TOOL_INPUT}"

# ── Allowlist check ──────────────────────────────────────────────
if [ -n "${ALLOWLIST}" ]; then
  OLD_IFS="${IFS}"
  IFS=','
  for pattern in ${ALLOWLIST}; do
    IFS="${OLD_IFS}"
    pattern="$(printf '%s' "${pattern}" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"
    [ -z "${pattern}" ] && continue
    case "${SCAN_TEXT}" in
      *"${pattern}"*)
        LOG_ENTRY="{\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date +%Y-%m-%dT%H:%M:%SZ)\",\"event\":\"guard_skipped\",\"reason\":\"allowlisted\",\"tool\":\"${TOOL_NAME}\",\"pattern\":\"${pattern}\"}"
        printf '%s\n' "${LOG_ENTRY}" >> "${LOG_DIR}/guard.log"
        exit 0
        ;;
    esac
  done
  IFS="${OLD_IFS}"
fi

# ── Threat patterns ──────────────────────────────────────────────
# Format: category|severity|regex|suggestion
THREATS_FOUND=""
THREAT_COUNT=0

check_pattern() {
  _cat="$1"; _sev="$2"; _pat="$3"; _sug="$4"
  if printf '%s' "${SCAN_TEXT}" | grep -qiE "${_pat}" 2>/dev/null; then
    _match="$(printf '%s' "${SCAN_TEXT}" | grep -oiE "${_pat}" 2>/dev/null | head -1)"
    THREAT_COUNT=$((THREAT_COUNT + 1))
    THREATS_FOUND="${THREATS_FOUND}{\"category\":\"${_cat}\",\"severity\":\"${_sev}\",\"match\":\"${_match}\",\"suggestion\":\"${_sug}\"},"
  fi
}

# Destructive file ops (critical)
check_pattern "destructive_file_ops" "critical" "rm[[:space:]]+-r[[:space:]]*f?[[:space:]]*/($|[[:space:]])" "Use targeted paths or mv to back up first"
check_pattern "destructive_file_ops" "critical" "rm[[:space:]]+-r[[:space:]]*f?[[:space:]]*~" "Never delete home directory recursively"
check_pattern "destructive_file_ops" "critical" "rm[[:space:]]+-r[[:space:]]*f?[[:space:]]*\\.($|[[:space:]])" "Use targeted paths instead of current directory"
check_pattern "destructive_file_ops" "high" "rm[[:space:]].*\\.env" "Use mv to back up .env files first"
check_pattern "destructive_file_ops" "high" "rm[[:space:]].*\\.git" "Never delete .git directory"

# Destructive git ops (critical/high)
check_pattern "destructive_git_ops" "critical" "git[[:space:]]+push[[:space:]]+--force[[:space:]]+(origin[[:space:]]+)?(main|master)" "Use --force-with-lease or push to feature branch"
check_pattern "destructive_git_ops" "high" "git[[:space:]]+reset[[:space:]]+--hard" "Use git stash or create backup branch first"
check_pattern "destructive_git_ops" "high" "git[[:space:]]+clean[[:space:]]+-[a-z]*f[a-z]*d" "Use --dry-run first: git clean -fdn"

# Database destruction (critical/high)
check_pattern "database_destruction" "critical" "DROP[[:space:]]+DATABASE" "Use migrations and backups instead"
check_pattern "database_destruction" "critical" "DROP[[:space:]]+TABLE" "Use migrations for schema changes"
check_pattern "database_destruction" "high" "TRUNCATE[[:space:]]" "Use DELETE with WHERE clause and backups"
check_pattern "database_destruction" "high" "DELETE[[:space:]]+FROM[[:space:]]+[a-zA-Z_]+[[:space:]]*;" "Add a WHERE clause to limit deletion scope"

# Permission abuse (high)
check_pattern "permission_abuse" "high" "chmod[[:space:]]+([0-9]*7[0-9]*7[0-9]*7|777)" "Use 755 for dirs, 644 for files"
check_pattern "permission_abuse" "high" "chmod[[:space:]]+-R[[:space:]]+777" "Use least-privilege permissions"

# Network exfiltration (critical/high)
check_pattern "network_exfiltration" "critical" "curl[[:space:]].*\\|[[:space:]]*bash" "Download first, review, then execute"
check_pattern "network_exfiltration" "critical" "wget[[:space:]].*\\|[[:space:]]*sh" "Download first, review, then execute"
check_pattern "network_exfiltration" "high" "curl[[:space:]]+--data[[:space:]]+@" "Review data before uploading"

# System danger (high)
check_pattern "system_danger" "high" "sudo[[:space:]]" "Avoid elevated privileges; use least-privilege approach"
check_pattern "system_danger" "high" "npm[[:space:]]+publish" "Use --dry-run first: npm publish --dry-run"

# ── Results ──────────────────────────────────────────────────────
TIMESTAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date +%Y-%m-%dT%H:%M:%SZ)"

if [ "${THREAT_COUNT}" -gt 0 ]; then
  # Remove trailing comma from threats list
  THREATS_JSON="$(printf '%s' "${THREATS_FOUND}" | sed 's/,$//')"
  LOG_ENTRY="{\"timestamp\":\"${TIMESTAMP}\",\"event\":\"threats_detected\",\"mode\":\"${GUARD_MODE}\",\"tool\":\"${TOOL_NAME}\",\"threat_count\":${THREAT_COUNT},\"threats\":[${THREATS_JSON}]}"
  printf '%s\n' "${LOG_ENTRY}" >> "${LOG_DIR}/guard.log"

  if [ "${GUARD_MODE}" = "block" ]; then
    # Output VS Code PreToolUse deny decision
    printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"Tool Guardian: %d threat(s) detected — %s"}}\n' \
      "${THREAT_COUNT}" "set GUARD_MODE=warn or adjust TOOL_GUARD_ALLOWLIST to override"
    exit 2
  else
    # Warn mode — allow but notify
    printf '{"systemMessage":"Tool Guardian: %d threat(s) detected (warn mode) — review logs at %s/guard.log"}\n' \
      "${THREAT_COUNT}" "${LOG_DIR}"
    exit 0
  fi
else
  LOG_ENTRY="{\"timestamp\":\"${TIMESTAMP}\",\"event\":\"guard_passed\",\"mode\":\"${GUARD_MODE}\",\"tool\":\"${TOOL_NAME}\"}"
  printf '%s\n' "${LOG_ENTRY}" >> "${LOG_DIR}/guard.log"
  exit 0
fi
