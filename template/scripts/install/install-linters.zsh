#!/usr/bin/env zsh
emulate -L zsh
setopt ERR_EXIT PIPE_FAIL

info() {
    emulate -L zsh
    print -f "%s→ %s%s\n" "${CYAN}" "$1" "${RESET}" | tee -a "${LOG_FILE}"
}

success() {
    emulate -L zsh
    print -f "%s✓ %s%s\n" "${GREEN}" "$1" "${RESET}" | tee -a "${LOG_FILE}"
}

warn() {
    emulate -L zsh
    print -f "%s[WARN] %s%s\n" "${YELLOW}" "$1" "${RESET}" | tee -a "${LOG_FILE}"
}

fail() {
    emulate -L zsh
    print -f "%s✗ %s%s\n" "${RED}" "$1" "${RESET}" | tee -a "${LOG_FILE}"
}

if [[ "${1:-}" == "--help" ]]; then
    print "Usage: zsh scripts/install/install-linters.zsh"
    print ""
    print "Installs linting tools: hadolint, shellcheck, yamllint."
    print "Skips tools that are already installed."
    exit 0
fi

detect_os() {
    emulate -L zsh
    case "$(uname -s)" in
        Linux*)  print "linux";;
        Darwin*) print "macos";;
        *)       print "unknown";;
    esac
}

main() {
    emulate -L zsh
    setopt PIPE_FAIL ERR_EXIT

    local SCRIPT_DIR="${0:A:h}"
    local LOG_FILE="${SCRIPT_DIR}/../../logs/install.log"
    mkdir -p "${LOG_FILE:h}"

    if [[ -n "${NO_COLOR:-}" ]]; then
        GREEN="" RED="" YELLOW="" CYAN="" RESET=""
    else
        GREEN=$'\033[0;32m' RED=$'\033[0;31m' YELLOW=$'\033[0;33m' CYAN=$'\033[0;36m' RESET=$'\033[0m'
    fi

    local OS
    OS="$(detect_os)"

    if command -v hadolint &>/dev/null; then
        success "hadolint already installed ($(hadolint --version 2>&1 | head -1))"
    else
        info "Installing hadolint..."
        if [[ "${OS}" == "macos" ]]; then
            brew install hadolint >> "${LOG_FILE}" 2>&1
        elif [[ "${OS}" == "linux" ]]; then
            local HADOLINT_URL="https://github.com/hadolint/hadolint/releases/latest/download/hadolint-Linux-x86_64"
            sudo curl -fsSL "${HADOLINT_URL}" -o /usr/local/bin/hadolint >> "${LOG_FILE}" 2>&1
            sudo chmod +x /usr/local/bin/hadolint
        fi
        if command -v hadolint &>/dev/null; then
            success "hadolint installed successfully"
        else
            fail "hadolint installation failed — see ${LOG_FILE}"
        fi
    fi

    if command -v shellcheck &>/dev/null; then
        success "shellcheck already installed ($(shellcheck --version | head -2 | tail -1))"
    else
        info "Installing shellcheck..."
        if [[ "${OS}" == "macos" ]]; then
            brew install shellcheck >> "${LOG_FILE}" 2>&1
        elif [[ "${OS}" == "linux" ]]; then
            sudo apt-get update -qq >> "${LOG_FILE}" 2>&1
            sudo apt-get install -y -qq shellcheck >> "${LOG_FILE}" 2>&1
        fi
        if command -v shellcheck &>/dev/null; then
            success "shellcheck installed successfully"
        else
            fail "shellcheck installation failed — see ${LOG_FILE}"
        fi
    fi

    if command -v yamllint &>/dev/null; then
        success "yamllint already installed"
    else
        info "Installing yamllint via uv..."
        if command -v uv &>/dev/null; then
            uv tool install yamllint >> "${LOG_FILE}" 2>&1
        elif command -v pip3 &>/dev/null; then
            pip3 install --user yamllint >> "${LOG_FILE}" 2>&1
        fi
        if command -v yamllint &>/dev/null; then
            success "yamllint installed successfully"
        else
            warn "yamllint installation failed — install manually"
        fi
    fi

    success "Linter installation complete"
}

main "$@"
