#!/usr/bin/env sh
# Secrets Scanner — Stop (end-of-session) hook
# Scans modified files for leaked secrets, credentials, and sensitive data
# before they are committed.
#
# Environment:
#   SCAN_MODE         — "warn" (default) or "block"
#   SCAN_SCOPE        — "diff" (default) or "staged"
#   SKIP_SECRETS_SCAN — set to "true" to disable
#   SECRETS_LOG_DIR   — log directory (default: logs/copilot/secrets)
#   SECRETS_ALLOWLIST — comma-separated patterns to ignore
set -eu

# ── Early exit ───────────────────────────────────────────────────
if [ "${SKIP_SECRETS_SCAN:-}" = "true" ]; then
  exit 0
fi

SCAN_MODE="${SCAN_MODE:-warn}"
SCAN_SCOPE="${SCAN_SCOPE:-diff}"
LOG_DIR="${SECRETS_LOG_DIR:-logs/copilot/secrets}"
ALLOWLIST="${SECRETS_ALLOWLIST:-}"

mkdir -p "${LOG_DIR}"

TIMESTAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date +%Y-%m-%dT%H:%M:%SZ)"

# ── Collect files to scan ────────────────────────────────────────
if [ "${SCAN_SCOPE}" = "staged" ]; then
  FILES="$(git diff --cached --name-only --diff-filter=ACMR 2>/dev/null || echo "")"
else
  FILES="$(git diff --name-only --diff-filter=ACMR HEAD 2>/dev/null || echo "")"
  # Also include untracked files
  UNTRACKED="$(git ls-files --others --exclude-standard 2>/dev/null || echo "")"
  if [ -n "${UNTRACKED}" ]; then
    FILES="$(printf '%s\n%s' "${FILES}" "${UNTRACKED}")"
  fi
fi

if [ -z "${FILES}" ]; then
  LOG_ENTRY="{\"timestamp\":\"${TIMESTAMP}\",\"event\":\"scan_complete\",\"status\":\"clean\",\"files_scanned\":0}"
  printf '%s\n' "${LOG_ENTRY}" >> "${LOG_DIR}/scan.log"
  exit 0
fi

# Filter to text files only, skip lock files and binaries
printf '%s\n' "${FILES}" | while IFS= read -r f; do
  [ -z "${f}" ] && continue
  [ ! -f "${f}" ] && continue
  # Skip lock files and binary-likely extensions
  case "${f}" in
    *.lock|*-lock.yaml|*-lock.json|*.min.js|*.min.css|*.woff*|*.ttf|*.eot|*.ico|*.png|*.jpg|*.gif|*.svg|*.wasm) continue ;;
  esac
  # Skip if file command says binary
  if command -v file >/dev/null 2>&1; then
    file_type="$(file -b --mime-type "${f}" 2>/dev/null || echo "text/plain")"
    case "${file_type}" in
      text/*|application/json|application/xml|application/javascript) ;;
      *) continue ;;
    esac
  fi
  printf '%s\n' "${f}"
done > "${LOG_DIR}/.scan_files.tmp" 2>/dev/null || true

if [ ! -s "${LOG_DIR}/.scan_files.tmp" ]; then
  LOG_ENTRY="{\"timestamp\":\"${TIMESTAMP}\",\"event\":\"scan_complete\",\"status\":\"clean\",\"files_scanned\":0}"
  printf '%s\n' "${LOG_ENTRY}" >> "${LOG_DIR}/scan.log"
  rm -f "${LOG_DIR}/.scan_files.tmp"
  exit 0
fi

FILE_COUNT="$(wc -l < "${LOG_DIR}/.scan_files.tmp" | tr -d ' ')"

# ── Secret patterns ──────────────────────────────────────────────
FINDINGS=""
FINDING_COUNT=0

scan_pattern() {
  _name="$1"; _sev="$2"; _regex="$3"
  while IFS= read -r _file; do
    [ -z "${_file}" ] && continue
    _result="$(grep -nEi "${_regex}" "${_file}" 2>/dev/null || true)"
    if [ -n "${_result}" ]; then
      printf '%s\n' "${_result}" | while IFS= read -r _line; do
        _linenum="$(printf '%s' "${_line}" | cut -d: -f1)"
        _content="$(printf '%s' "${_line}" | cut -d: -f2-)"
        # Skip placeholders
        case "${_content}" in
          *example*|*changeme*|*your_*|*CHANGE_ME*|*placeholder*|*xxx*|*TODO*|*FIXME*) continue ;;
        esac
        # Skip allowlisted
        if [ -n "${ALLOWLIST}" ]; then
          _skip=0
          OLD_IFS="${IFS}"
          IFS=','
          for _ap in ${ALLOWLIST}; do
            _ap="$(printf '%s' "${_ap}" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"
            case "${_content}" in
              *"${_ap}"*) _skip=1; break ;;
            esac
          done
          IFS="${OLD_IFS}"
          [ "${_skip}" = "1" ] && continue
        fi
        # Truncate match for log safety
        _trunc="$(printf '%.40s' "${_content}")"
        FINDING_COUNT=$((FINDING_COUNT + 1))
        printf '%s|%s|%s|%s|%s\n' "${_file}" "${_linenum}" "${_name}" "${_sev}" "${_trunc}"
      done
    fi
  done < "${LOG_DIR}/.scan_files.tmp"
}

# Run scans — output collected in temp file
SCAN_RESULTS="${LOG_DIR}/.scan_results.tmp"
: > "${SCAN_RESULTS}"

# AWS credentials
scan_pattern "AWS_ACCESS_KEY" "critical" "AKIA[0-9A-Z]{16}" >> "${SCAN_RESULTS}" 2>/dev/null || true
scan_pattern "AWS_SECRET_KEY" "critical" "aws_secret_access_key[[:space:]]*=[[:space:]]*[A-Za-z0-9/+=]{40}" >> "${SCAN_RESULTS}" 2>/dev/null || true

# Azure credentials
scan_pattern "AZURE_CLIENT_SECRET" "critical" "azure[_-]?client[_-]?secret[[:space:]]*[=:][[:space:]]*['\"]?[A-Za-z0-9~._-]{34}" >> "${SCAN_RESULTS}" 2>/dev/null || true

# GitHub tokens
scan_pattern "GITHUB_PAT" "critical" "ghp_[A-Za-z0-9]{36}" >> "${SCAN_RESULTS}" 2>/dev/null || true
scan_pattern "GITHUB_FINE_GRAINED" "critical" "github_pat_[A-Za-z0-9_]{82}" >> "${SCAN_RESULTS}" 2>/dev/null || true

# Private keys
scan_pattern "PRIVATE_KEY" "critical" "-----BEGIN[[:space:]]+(RSA|EC|OPENSSH|PGP|DSA)[[:space:]]+PRIVATE[[:space:]]+KEY-----" >> "${SCAN_RESULTS}" 2>/dev/null || true

# Generic secrets
scan_pattern "GENERIC_API_KEY" "high" "(api[_-]?key|apikey|secret[_-]?key)[[:space:]]*[=:][[:space:]]*['\"]?[A-Za-z0-9]{20,}" >> "${SCAN_RESULTS}" 2>/dev/null || true

# Connection strings
scan_pattern "CONNECTION_STRING" "high" "(postgresql|mysql|mongodb|redis|mssql)://[^[:space:]\"']+:[^[:space:]\"']+@" >> "${SCAN_RESULTS}" 2>/dev/null || true

# Platform tokens
scan_pattern "SLACK_TOKEN" "high" "xox[bpors]-[A-Za-z0-9-]+" >> "${SCAN_RESULTS}" 2>/dev/null || true
scan_pattern "STRIPE_KEY" "critical" "sk_live_[A-Za-z0-9]{24,}" >> "${SCAN_RESULTS}" 2>/dev/null || true
scan_pattern "NPM_TOKEN" "high" "npm_[A-Za-z0-9]{36}" >> "${SCAN_RESULTS}" 2>/dev/null || true

# JWT tokens
scan_pattern "JWT_TOKEN" "medium" "eyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\." >> "${SCAN_RESULTS}" 2>/dev/null || true

# ── Results ──────────────────────────────────────────────────────
RESULT_COUNT=0
if [ -s "${SCAN_RESULTS}" ]; then
  RESULT_COUNT="$(wc -l < "${SCAN_RESULTS}" | tr -d ' ')"
fi

if [ "${RESULT_COUNT}" -gt 0 ]; then
  # Build findings JSON
  FINDINGS_JSON="["
  while IFS='|' read -r f_file f_line f_pattern f_severity f_match; do
    [ -z "${f_file}" ] && continue
    FINDINGS_JSON="${FINDINGS_JSON}{\"file\":\"${f_file}\",\"line\":${f_line},\"pattern\":\"${f_pattern}\",\"severity\":\"${f_severity}\"},"
  done < "${SCAN_RESULTS}"
  FINDINGS_JSON="$(printf '%s' "${FINDINGS_JSON}" | sed 's/,$//')"]"

  LOG_ENTRY="{\"timestamp\":\"${TIMESTAMP}\",\"event\":\"secrets_found\",\"mode\":\"${SCAN_MODE}\",\"scope\":\"${SCAN_SCOPE}\",\"files_scanned\":${FILE_COUNT},\"finding_count\":${RESULT_COUNT},\"findings\":${FINDINGS_JSON}}"
  printf '%s\n' "${LOG_ENTRY}" >> "${LOG_DIR}/scan.log"

  if [ "${SCAN_MODE}" = "block" ]; then
    printf '{"continue":false,"stopReason":"Secrets Scanner: %d potential secret(s) found in modified files. Review logs at %s/scan.log"}\n' \
      "${RESULT_COUNT}" "${LOG_DIR}"
    rm -f "${LOG_DIR}/.scan_files.tmp" "${SCAN_RESULTS}"
    exit 2
  else
    printf '{"systemMessage":"Secrets Scanner: %d potential secret(s) found (warn mode). Review logs at %s/scan.log"}\n' \
      "${RESULT_COUNT}" "${LOG_DIR}"
  fi
else
  LOG_ENTRY="{\"timestamp\":\"${TIMESTAMP}\",\"event\":\"scan_complete\",\"mode\":\"${SCAN_MODE}\",\"scope\":\"${SCAN_SCOPE}\",\"status\":\"clean\",\"files_scanned\":${FILE_COUNT}}"
  printf '%s\n' "${LOG_ENTRY}" >> "${LOG_DIR}/scan.log"
fi

rm -f "${LOG_DIR}/.scan_files.tmp" "${SCAN_RESULTS}"
exit 0
