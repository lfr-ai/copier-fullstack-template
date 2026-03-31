#!/usr/bin/env sh
# Dependency License Checker — Stop hook
# Scans newly added dependencies for license compliance (GPL, AGPL, etc.)
# at session end. Detects changes in package.json, pyproject.toml, go.mod,
# Gemfile, and Cargo.toml.
#
# Environment:
#   LICENSE_MODE       — "warn" (default) or "block"
#   SKIP_LICENSE_CHECK — set to "true" to disable
#   LICENSE_LOG_DIR    — log directory (default: logs/copilot/license-checker)
#   BLOCKED_LICENSES   — comma-separated SPDX IDs to flag (default: copyleft set)
#   LICENSE_ALLOWLIST  — comma-separated package names to skip
set -eu

# ── Early exit ───────────────────────────────────────────────────
if [ "${SKIP_LICENSE_CHECK:-}" = "true" ]; then
  exit 0
fi

LICENSE_MODE="${LICENSE_MODE:-warn}"
LOG_DIR="${LICENSE_LOG_DIR:-logs/copilot/license-checker}"
ALLOWLIST="${LICENSE_ALLOWLIST:-}"

mkdir -p "${LOG_DIR}"

TIMESTAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date +%Y-%m-%dT%H:%M:%SZ)"

# Default blocked licenses (copyleft and restrictive)
if [ -z "${BLOCKED_LICENSES:-}" ]; then
  BLOCKED_LICENSES="GPL-2.0,GPL-2.0-only,GPL-2.0-or-later,GPL-3.0,GPL-3.0-only,GPL-3.0-or-later"
  BLOCKED_LICENSES="${BLOCKED_LICENSES},AGPL-1.0,AGPL-3.0,AGPL-3.0-only,AGPL-3.0-or-later"
  BLOCKED_LICENSES="${BLOCKED_LICENSES},LGPL-2.0,LGPL-2.1,LGPL-2.1-only,LGPL-2.1-or-later,LGPL-3.0,LGPL-3.0-only,LGPL-3.0-or-later"
  BLOCKED_LICENSES="${BLOCKED_LICENSES},SSPL-1.0,EUPL-1.1,EUPL-1.2,OSL-3.0,CPAL-1.0,CPL-1.0"
  BLOCKED_LICENSES="${BLOCKED_LICENSES},CC-BY-SA-4.0,CC-BY-NC-4.0,CC-BY-NC-SA-4.0"
fi

# ── Detect new dependencies from git diff ────────────────────────
NEW_DEPS=""

# npm/bun: package.json
if git diff HEAD -- package.json 2>/dev/null | grep -qE '^\+.*"[^"]+"\s*:\s*"' 2>/dev/null; then
  _npm_deps="$(git diff HEAD -- package.json 2>/dev/null | grep -E '^\+\s*"' | grep -vE '^\+\+\+' | sed -n 's/.*"\([^"]*\)"\s*:.*/\1/p' | grep -vE '^(name|version|description|main|scripts|devDependencies|dependencies|peerDependencies|optionalDependencies|engines|type|private|workspaces|repository|author|license|bugs|homepage|keywords|files|publishConfig)$' || true)"
  for _dep in ${_npm_deps}; do
    NEW_DEPS="${NEW_DEPS}${_dep}|npm
"
  done
fi

# pip: pyproject.toml (dependencies array)
if git diff HEAD -- pyproject.toml 2>/dev/null | grep -qE '^\+.*[a-zA-Z]' 2>/dev/null; then
  _pip_deps="$(git diff HEAD -- pyproject.toml 2>/dev/null | grep -E '^\+' | grep -vE '^\+\+\+' | sed -n 's/.*"\([a-zA-Z][a-zA-Z0-9_-]*\).*/\1/p' || true)"
  for _dep in ${_pip_deps}; do
    # Skip common pyproject.toml keys
    case "${_dep}" in
      name|version|description|authors|readme|requires|build|project|tool|python|classifiers|urls|scripts|optional|include|exclude|packages|hatchling|setuptools) continue ;;
    esac
    NEW_DEPS="${NEW_DEPS}${_dep}|pip
"
  done
fi

# Go: go.mod
if git diff HEAD -- go.mod 2>/dev/null | grep -qE '^\+\s' 2>/dev/null; then
  _go_deps="$(git diff HEAD -- go.mod 2>/dev/null | grep -E '^\+\s' | grep -vE '^\+\+\+|^+module|^+go ' | sed 's/^+[[:space:]]*//' | cut -d' ' -f1 || true)"
  for _dep in ${_go_deps}; do
    NEW_DEPS="${NEW_DEPS}${_dep}|go
"
  done
fi

if [ -z "${NEW_DEPS}" ]; then
  LOG_ENTRY="{\"timestamp\":\"${TIMESTAMP}\",\"event\":\"license_check_complete\",\"mode\":\"${LICENSE_MODE}\",\"status\":\"clean\",\"dependencies_checked\":0}"
  printf '%s\n' "${LOG_ENTRY}" >> "${LOG_DIR}/check.log"
  exit 0
fi

# ── Check licenses ───────────────────────────────────────────────
VIOLATIONS=""
VIOLATION_COUNT=0
DEP_COUNT=0
RESULTS="${LOG_DIR}/.license_results.tmp"
: > "${RESULTS}"

is_blocked() {
  _license="$1"
  OLD_IFS="${IFS}"
  IFS=','
  for _bl in ${BLOCKED_LICENSES}; do
    # Case-insensitive substring match
    _bl_lower="$(printf '%s' "${_bl}" | tr '[:upper:]' '[:lower:]')"
    _lic_lower="$(printf '%s' "${_license}" | tr '[:upper:]' '[:lower:]')"
    case "${_lic_lower}" in
      *"${_bl_lower}"*) IFS="${OLD_IFS}"; return 0 ;;
    esac
  done
  IFS="${OLD_IFS}"
  return 1
}

is_allowlisted() {
  _pkg="$1"
  [ -z "${ALLOWLIST}" ] && return 1
  OLD_IFS="${IFS}"
  IFS=','
  for _al in ${ALLOWLIST}; do
    _al="$(printf '%s' "${_al}" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"
    [ "${_pkg}" = "${_al}" ] && IFS="${OLD_IFS}" && return 0
  done
  IFS="${OLD_IFS}"
  return 1
}

lookup_npm_license() {
  _pkg="$1"
  # Try local node_modules first
  if [ -f "node_modules/${_pkg}/package.json" ]; then
    if command -v jq >/dev/null 2>&1; then
      _lic="$(jq -r '.license // "UNKNOWN"' "node_modules/${_pkg}/package.json" 2>/dev/null || echo "UNKNOWN")"
    else
      _lic="$(sed -n 's/.*"license"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' "node_modules/${_pkg}/package.json" | head -1)"
      [ -z "${_lic}" ] && _lic="UNKNOWN"
    fi
    printf '%s' "${_lic}"
    return
  fi
  # Try npm view with timeout
  if command -v npm >/dev/null 2>&1; then
    _lic="$(timeout 5 npm view "${_pkg}" license 2>/dev/null || echo "UNKNOWN")"
    printf '%s' "${_lic}"
    return
  fi
  printf 'UNKNOWN'
}

lookup_pip_license() {
  _pkg="$1"
  if command -v pip >/dev/null 2>&1; then
    _lic="$(pip show "${_pkg}" 2>/dev/null | sed -n 's/^License:[[:space:]]*//p' | head -1)"
    [ -z "${_lic}" ] && _lic="UNKNOWN"
    printf '%s' "${_lic}"
    return
  fi
  if command -v uv >/dev/null 2>&1; then
    _lic="$(uv pip show "${_pkg}" 2>/dev/null | sed -n 's/^License:[[:space:]]*//p' | head -1)"
    [ -z "${_lic}" ] && _lic="UNKNOWN"
    printf '%s' "${_lic}"
    return
  fi
  printf 'UNKNOWN'
}

# Process each dependency
printf '%s' "${NEW_DEPS}" | while IFS='|' read -r _pkg _eco; do
  [ -z "${_pkg}" ] && continue
  DEP_COUNT=$((DEP_COUNT + 1))

  if is_allowlisted "${_pkg}"; then
    printf '%s|%s|ALLOWLISTED|OK\n' "${_pkg}" "${_eco}" >> "${RESULTS}"
    continue
  fi

  # Look up license
  case "${_eco}" in
    npm) _license="$(lookup_npm_license "${_pkg}")" ;;
    pip) _license="$(lookup_pip_license "${_pkg}")" ;;
    *)   _license="UNKNOWN" ;;
  esac

  if is_blocked "${_license}"; then
    printf '%s|%s|%s|BLOCKED\n' "${_pkg}" "${_eco}" "${_license}" >> "${RESULTS}"
  else
    printf '%s|%s|%s|OK\n' "${_pkg}" "${_eco}" "${_license}" >> "${RESULTS}"
  fi
done

# ── Results ──────────────────────────────────────────────────────
TOTAL_DEPS=0
VIOLATION_COUNT=0
if [ -s "${RESULTS}" ]; then
  TOTAL_DEPS="$(wc -l < "${RESULTS}" | tr -d ' ')"
  VIOLATION_COUNT="$(grep -c '|BLOCKED$' "${RESULTS}" 2>/dev/null || echo 0)"
fi

if [ "${VIOLATION_COUNT}" -gt 0 ]; then
  VIOLATIONS_JSON="["
  while IFS='|' read -r v_pkg v_eco v_lic v_status; do
    [ "${v_status}" = "BLOCKED" ] || continue
    VIOLATIONS_JSON="${VIOLATIONS_JSON}{\"package\":\"${v_pkg}\",\"ecosystem\":\"${v_eco}\",\"license\":\"${v_lic}\"},"
  done < "${RESULTS}"
  VIOLATIONS_JSON="$(printf '%s' "${VIOLATIONS_JSON}" | sed 's/,$//')"]"

  LOG_ENTRY="{\"timestamp\":\"${TIMESTAMP}\",\"event\":\"license_check_complete\",\"mode\":\"${LICENSE_MODE}\",\"dependencies_checked\":${TOTAL_DEPS},\"violation_count\":${VIOLATION_COUNT},\"violations\":${VIOLATIONS_JSON}}"
  printf '%s\n' "${LOG_ENTRY}" >> "${LOG_DIR}/check.log"

  if [ "${LICENSE_MODE}" = "block" ]; then
    printf '{"continue":false,"stopReason":"License Checker: %d dependency license violation(s) found. Review logs at %s/check.log"}\n' \
      "${VIOLATION_COUNT}" "${LOG_DIR}"
    rm -f "${RESULTS}"
    exit 2
  else
    printf '{"systemMessage":"License Checker: %d dependency license violation(s) found (warn mode). Review logs at %s/check.log"}\n' \
      "${VIOLATION_COUNT}" "${LOG_DIR}"
  fi
else
  LOG_ENTRY="{\"timestamp\":\"${TIMESTAMP}\",\"event\":\"license_check_complete\",\"mode\":\"${LICENSE_MODE}\",\"status\":\"clean\",\"dependencies_checked\":${TOTAL_DEPS}}"
  printf '%s\n' "${LOG_ENTRY}" >> "${LOG_DIR}/check.log"
fi

rm -f "${RESULTS}"
exit 0
