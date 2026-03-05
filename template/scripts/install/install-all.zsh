#!/usr/bin/env zsh
emulate -L zsh
setopt PIPE_FAIL ERR_EXIT

# Master installer: detect platform and run all component installers in order

SCRIPT_DIR="${0:A:h}"
LOG_DIR="${SCRIPT_DIR}/../../.bootstrap/logs"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
RESULTS=()

log_result() {
    emulate -L zsh

    local component="${1}"
    local status="${2}"
    RESULTS+=("${component}:${status}")
}

run_installer() {
    emulate -L zsh

    local component="${1}"
    local script="${2}"
    shift 2

    echo ""
    echo "════════════════════════════════════════"
    echo "  Installing: ${component}"
    echo "════════════════════════════════════════"
    echo ""

    if [[ ! -f "${script}" ]]; then
        echo "WARNING: Script not found: ${script}"
        log_result "${component}" "SKIPPED"
        return 0
    fi

    if zsh "${script}" "$@"; then
        log_result "${component}" "OK"
    else
        echo "WARNING: ${component} installation had issues"
        log_result "${component}" "FAILED"
    fi
}

detect_platform() {
    emulate -L zsh

    local os_type
    os_type="$(uname -s)"

    case "${os_type}" in
        Linux)
            if [[ -f /proc/version ]] && grep -qi microsoft /proc/version; then
                echo "wsl"
            else
                echo "linux"
            fi
            ;;
        Darwin) echo "macos" ;;
        *)      echo "unknown" ;;
    esac
}

print_summary() {
    emulate -L zsh

    echo ""
    echo "╔══════════════════════════════════════════╗"
    echo "║        Installation Summary              ║"
    echo "╠══════════════════════════════════════════╣"

    local component status
    for entry in "${RESULTS[@]}"; do
        component="${entry%%:*}"
        status="${entry##*:}"
        printf "║  %-20s  %s\n" "${component}" "${status}"
    done

    echo "╚══════════════════════════════════════════╝"
    echo ""
}

save_log() {
    emulate -L zsh

    mkdir -p "${LOG_DIR}"

    local log_file="${LOG_DIR}/install-${TIMESTAMP}.json"
    local json_entries=""

    for entry in "${RESULTS[@]}"; do
        local component="${entry%%:*}"
        local status="${entry##*:}"
        if [[ -n "${json_entries}" ]]; then
            json_entries="${json_entries},"
        fi
        json_entries="${json_entries}\"${component}\": \"${status}\""
    done

    echo "{\"timestamp\": \"${TIMESTAMP}\", \"platform\": \"$(detect_platform)\", \"results\": {${json_entries}}}" > "${log_file}"
    echo "Log saved to ${log_file}"
}

main() {
    emulate -L zsh
    setopt PIPE_FAIL ERR_EXIT

    local platform
    platform="$(detect_platform)"

    echo "╔══════════════════════════════════════════╗"
    echo "║   Full Development Environment Setup     ║"
    echo "║   Platform: ${platform}                  ║"
    echo "╚══════════════════════════════════════════╝"

    run_installer "Git"              "${SCRIPT_DIR}/install-git.zsh"
    run_installer "Zsh"              "${SCRIPT_DIR}/install-zsh.zsh"
    run_installer "Python"           "${SCRIPT_DIR}/install-python.zsh"
    run_installer "Node.js + pnpm"   "${SCRIPT_DIR}/install-pnpm.zsh"
    run_installer "Container Engine" "${SCRIPT_DIR}/install-container-engine.zsh"
    run_installer "Task CLI"         "${SCRIPT_DIR}/install-task.zsh"
    run_installer "VS Code"          "${SCRIPT_DIR}/install-vscode.zsh"
    run_installer "DevContainer"     "${SCRIPT_DIR}/setup-devcontainer.zsh"

    print_summary
    save_log

    echo "All installations complete"
}

main "$@"
