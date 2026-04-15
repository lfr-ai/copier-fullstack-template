#!/usr/bin/env sh
# Check Licenses -- Stop hook
# Scans installed dependencies for license compatibility.
# Runs at the end of a Copilot coding agent session.
#
# Environment:
#   LICENSE_MODE -- "warn" (default) or "block"
#   SKIP_LICENSE_CHECK -- set to "true" to disable
#   LICENSE_LOG_DIR -- directory for structured logs
set -eu

# -- Early exit -------------------------------------------------------
if [ "${SKIP_LICENSE_CHECK:-}" = "true" ]; then
  exit 0
fi

MODE="${LICENSE_MODE:-warn}"
LOG_DIR="${LICENSE_LOG_DIR:-logs/copilot/license-checker}"
mkdir -p "${LOG_DIR}"

TIMESTAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date +%Y-%m-%dT%H:%M:%SZ)"
VIOLATIONS=""
EXIT_CODE=0

# -- Denied licenses -------------------------------------------------
# AGPL and similar copyleft licenses that are incompatible with most
# commercial projects. Extend this list per project policy.
DENIED_LICENSES="AGPL|SSPL|EUPL|OSL-3"

# -- Python: pip-licenses ---------------------------------------------
if command -v pip-licenses >/dev/null 2>&1; then
  PY_RESULT="$(pip-licenses --format=json 2>/dev/null || echo "[]")"
  PY_VIOLATIONS="$(printf '%s' "${PY_RESULT}" | \
    python3 -c "
import sys, json, re
data = json.load(sys.stdin)
denied = re.compile('${DENIED_LICENSES}', re.IGNORECASE)
violations = [p for p in data if denied.search(p.get('License',''))]
for v in violations:
    print(f\"  - {v['Name']}=={v['Version']}: {v['License']}\")
" 2>/dev/null || echo "")"
  if [ -n "${PY_VIOLATIONS}" ]; then
    VIOLATIONS="${VIOLATIONS}Python violations:\n${PY_VIOLATIONS}\n"
  fi
elif command -v uv >/dev/null 2>&1 && [ -f "pyproject.toml" ]; then
  # Fallback: check pyproject.toml exists but no scanner -- just warn
  VIOLATIONS="${VIOLATIONS}Python: pip-licenses not installed -- cannot scan\n"
fi

# -- Node.js: license-checker -----------------------------------------
if command -v npx >/dev/null 2>&1 && [ -f "package.json" ]; then
  NODE_RESULT="$(npx license-checker --json 2>/dev/null || echo "{}")"
  NODE_VIOLATIONS="$(printf '%s' "${NODE_RESULT}" | \
    python3 -c "
import sys, json, re
data = json.load(sys.stdin)
denied = re.compile('${DENIED_LICENSES}', re.IGNORECASE)
violations = [(k,v) for k,v in data.items() if denied.search(v.get('licenses',''))]
for name, info in violations:
    print(f\"  - {name}: {info.get('licenses','unknown')}\")
" 2>/dev/null || echo "")"
  if [ -n "${NODE_VIOLATIONS}" ]; then
    VIOLATIONS="${VIOLATIONS}Node violations:\n${NODE_VIOLATIONS}\n"
  fi
fi

# -- Report -----------------------------------------------------------
if [ -n "${VIOLATIONS}" ]; then
  LOG_FILE="${LOG_DIR}/license-check-$(date -u +%Y%m%d-%H%M%S 2>/dev/null || date +%s).json"
  printf '{"timestamp":"%s","event":"license_violations","mode":"%s","violations":"%s"}\n' \
    "${TIMESTAMP}" "${MODE}" "$(printf '%s' "${VIOLATIONS}" | tr '\n' ' ')" > "${LOG_FILE}"

  printf '\n[License Check] Violations detected:\n%b\n' "${VIOLATIONS}" >&2

  if [ "${MODE}" = "block" ]; then
    printf '[License Check] MODE=block -- failing session.\n' >&2
    EXIT_CODE=1
  else
    printf '[License Check] MODE=warn -- review violations above.\n' >&2
  fi
else
  printf '[License Check] No license violations detected.\n' >&2
fi

exit ${EXIT_CODE}
