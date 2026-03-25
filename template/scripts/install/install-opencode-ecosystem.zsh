#!/usr/bin/env zsh
emulate -L zsh
setopt PIPE_FAIL ERR_EXIT

# Install OpenCode ecosystem companion tools:
#   - GSD-2 (gsd-pi): autonomous spec-driven development workflow
#   - OpenAgents Control (OAC): pattern-controlled AI development
#   - oh-my-opencode plugins: verification & doctor check
#   - opencode-agent-skills: dynamic skill discovery
#
# Prerequisites: OpenCode must already be installed.
# Usage: zsh scripts/install/install-opencode-ecosystem.zsh [--all|--gsd|--oac|--plugins|--help]

readonly SCRIPT_NAME="${0:t}"
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly CYAN='\033[0;36m'
readonly BOLD='\033[1m'
readonly NC='\033[0m'

log_info()  { print -P "${CYAN}[INFO]${NC}  $1" }
log_ok()    { print -P "${GREEN}[ OK ]${NC}  $1" }
log_warn()  { print -P "${YELLOW}[WARN]${NC}  $1" }
log_err()   { print -P "${RED}[ERROR]${NC} $1" }
log_step()  { print -P "${BOLD}${CYAN}──▸${NC} $1" }

# Track results for summary
typeset -A INSTALL_RESULTS

check_prerequisites() {
  emulate -L zsh

  log_step "Checking prerequisites..."

  if ! command -v opencode &>/dev/null; then
    log_err "OpenCode is not installed. Run install-opencode.zsh first."
    return 1
  fi
  log_ok "OpenCode detected: $(opencode --version 2>/dev/null || echo 'version unknown')"

  # Check for Node.js toolchain (required for npm packages)
  local node_version=""
  if command -v node &>/dev/null; then
    node_version="$(node --version 2>/dev/null)"
    log_ok "Node.js detected: ${node_version}"
  fi

  if ! command -v npm &>/dev/null && ! command -v npx &>/dev/null; then
    log_err "npm/npx not found. Install Node.js 20+ first."
    return 1
  fi
  log_ok "npm/npx available"

  # Check for bunx (preferred package runner)
  if command -v bunx &>/dev/null; then
    log_ok "bunx available (preferred runner)"
  fi
}

# GSD-2 — autonomous spec-driven development
# https://www.npmjs.com/package/gsd-pi
install_gsd() {
  emulate -L zsh
  setopt PIPE_FAIL ERR_EXIT

  log_step "Installing GSD-2 (gsd-pi)..."

  if command -v gsd &>/dev/null; then
    local gsd_ver
    gsd_ver="$(gsd --version 2>/dev/null || echo 'unknown')"
    log_ok "GSD already installed: ${gsd_ver}"
    INSTALL_RESULTS[gsd]="ok"
    return 0
  fi

  # Global install via npm
  if command -v npm &>/dev/null; then
    log_info "Installing gsd-pi globally via npm..."
    if npm install -g gsd-pi@latest 2>/dev/null; then
      log_ok "GSD-2 installed globally via npm"
      INSTALL_RESULTS[gsd]="ok"
      return 0
    fi
  fi

  # Fallback: npx ephemeral run (verifies the package works)
  if command -v npx &>/dev/null; then
    log_info "Trying npx ephemeral install..."
    if npx gsd-pi@latest --version 2>/dev/null; then
      log_warn "GSD works via npx but is not globally installed"
      log_warn "  For persistent install: npm install -g gsd-pi"
      INSTALL_RESULTS[gsd]="partial"
      return 0
    fi
  fi

  log_warn "GSD install failed. Install manually:"
  log_warn "  npm install -g gsd-pi"
  INSTALL_RESULTS[gsd]="failed"
}

# OpenAgents Control (OAC) — pattern-controlled AI development
# https://github.com/darrenhinde/OpenAgentsControl
install_oac() {
  emulate -L zsh
  setopt PIPE_FAIL ERR_EXIT

  log_step "Installing OpenAgents Control (OAC)..."

  # Check if OAC context files already exist (local or global)
  if [[ -d ".opencode/context/core" ]] || [[ -d "${HOME}/.config/opencode/context/core" ]]; then
    log_ok "OAC context files detected (local or global install)"
    INSTALL_RESULTS[oac]="ok"
    return 0
  fi

  # Check if OAC agent files exist
  if [[ -f ".opencode/agent/core/opencoder.md" ]] || [[ -f "${HOME}/.config/opencode/agent/core/opencoder.md" ]]; then
    log_ok "OAC agents detected (local or global install)"
    INSTALL_RESULTS[oac]="ok"
    return 0
  fi

  # Download and run the OAC installer (developer mode = local project install)
  if command -v curl &>/dev/null; then
    log_info "Downloading OAC installer..."
    local installer_url="https://raw.githubusercontent.com/darrenhinde/OpenAgentsControl/main/install.sh"
    local tmp_installer
    tmp_installer="$(mktemp)"
    if curl -fsSL "${installer_url}" -o "${tmp_installer}" 2>/dev/null; then
      log_info "Running OAC installer (developer mode)..."
      if bash "${tmp_installer}" developer 2>/dev/null; then
        log_ok "OpenAgents Control installed"
        INSTALL_RESULTS[oac]="ok"
      else
        log_warn "OAC installer returned non-zero (may need interactive setup)"
        INSTALL_RESULTS[oac]="partial"
      fi
      rm -f "${tmp_installer}"
      return 0
    fi
  fi

  log_warn "OAC install failed. Install manually:"
  log_warn "  curl -fsSL https://raw.githubusercontent.com/darrenhinde/OpenAgentsControl/main/install.sh | bash -s developer"
  INSTALL_RESULTS[oac]="failed"
}

# OpenCode Plugins — verify oh-my-opencode & opencode-agent-skills
# Auto-loaded from opencode.json; validates installation.
verify_plugins() {
  emulate -L zsh
  setopt PIPE_FAIL ERR_EXIT

  log_step "Verifying OpenCode plugins..."

  # Run oh-my-opencode doctor if available
  if command -v bunx &>/dev/null; then
    log_info "Running oh-my-opencode doctor..."
    if bunx oh-my-opencode doctor 2>/dev/null; then
      log_ok "oh-my-opencode: healthy"
    else
      log_warn "oh-my-opencode doctor reported issues (non-fatal)"
    fi
  elif command -v npx &>/dev/null; then
    log_info "Running oh-my-opencode doctor via npx..."
    if npx oh-my-opencode doctor 2>/dev/null; then
      log_ok "oh-my-opencode: healthy"
    else
      log_warn "oh-my-opencode doctor reported issues (non-fatal)"
    fi
  else
    log_warn "Cannot run oh-my-opencode doctor (no bunx/npx)"
  fi

  # Verify opencode.json has the expected plugins
  local config_file="opencode.json"
  if [[ -f "${config_file}" ]]; then
    local missing_plugins=()

    for plugin in "oh-my-opencode" "opencode-agent-skills" "superpowers"; do
      if ! grep -q "${plugin}" "${config_file}" 2>/dev/null; then
        missing_plugins+=("${plugin}")
      fi
    done

    if (( ${#missing_plugins[@]} == 0 )); then
      log_ok "All expected plugins found in opencode.json"
    else
      log_warn "Missing plugins in opencode.json: ${missing_plugins[*]}"
      log_warn "  Expected: oh-my-opencode, opencode-agent-skills, superpowers"
    fi
  else
    log_warn "opencode.json not found in current directory"
  fi

  # Verify .opencode/ directory structure
  if [[ -d ".opencode" ]]; then
    local dirs_found=0
    for subdir in agents commands skills plugins; do
      [[ -d ".opencode/${subdir}" ]] && (( dirs_found++ ))
    done
    log_ok ".opencode/ structure: ${dirs_found}/4 directories present"
  else
    log_warn ".opencode/ directory not found"
  fi

  # Verify oh-my-opencode.jsonc exists
  if [[ -f ".opencode/oh-my-opencode.jsonc" ]]; then
    log_ok "oh-my-opencode.jsonc configuration found"
  else
    log_warn ".opencode/oh-my-opencode.jsonc not found"
  fi

  INSTALL_RESULTS[plugins]="ok"
}

print_summary() {
  emulate -L zsh

  print ""
  print -P "${CYAN}═══════════════════════════════════════════════════════════${NC}"
  print -P "${CYAN}  OpenCode Ecosystem Setup Complete${NC}"
  print -P "${CYAN}═══════════════════════════════════════════════════════════${NC}"
  print ""
  print "  Plugins (auto-loaded via opencode.json):"
  print "    • oh-my-opencode        — Multi-model agents, ultrawork, LSP/AST"
  print "    • opencode-agent-skills — Dynamic skill discovery & injection"
  print "    • superpowers           — Agentic skills (brainstorm, TDD, review)"
  print ""
  print "  Companion CLIs:"

  # GSD status
  if [[ "${INSTALL_RESULTS[gsd]:-skip}" != "skip" ]]; then
    local gsd_icon="✗"
    [[ "${INSTALL_RESULTS[gsd]}" == "ok" ]] && gsd_icon="✓"
    [[ "${INSTALL_RESULTS[gsd]}" == "partial" ]] && gsd_icon="~"
    print "    [${gsd_icon}] GSD-2 (gsd-pi)    — Autonomous spec-driven development (v2.28+)"
  fi

  # OAC status
  if [[ "${INSTALL_RESULTS[oac]:-skip}" != "skip" ]]; then
    local oac_icon="✗"
    [[ "${INSTALL_RESULTS[oac]}" == "ok" ]] && oac_icon="✓"
    [[ "${INSTALL_RESULTS[oac]}" == "partial" ]] && oac_icon="~"
    print "    [${oac_icon}] OAC                — Pattern-controlled AI development (v0.7+)"
  fi

  print ""
  print "  Quick Start:"
  print "    1. Launch OpenCode:  opencode"
  print "    2. Plugins load automatically from opencode.json"

  if [[ "${INSTALL_RESULTS[gsd]:-skip}" != "skip" ]]; then
    print "    3. GSD-2 workflow:   gsd -> /gsd (step) or /gsd auto"
    print "       Non-interactive:  gsd headless status"
  fi

  if [[ "${INSTALL_RESULTS[oac]:-skip}" != "skip" ]]; then
    print "    4. OAC workflow:     opencode --agent OpenAgent"
    print "       Add patterns:     /add-context"
  fi

  print ""
  print "  Taskfile shortcuts:    task --list | grep -E 'opencode|gsd'"
  print ""
}

usage() {
  print "Usage: ${SCRIPT_NAME} [OPTIONS...]"
  print ""
  print "Install and verify OpenCode ecosystem companion tools."
  print ""
  print "Options:"
  print "  --all            Install everything (default)"
  print "  --gsd            Install GSD-2 only"
  print "  --oac            Install OpenAgents Control only"
  print "  --plugins        Verify plugins only (no installs)"
  print "  --help           Show this help"
  print ""
  print "Multiple flags can be combined: --gsd --oac --plugins"
}

main() {
  emulate -L zsh
  setopt PIPE_FAIL ERR_EXIT

  local install_gsd_flag=false
  local install_oac_flag=false
  local verify_plugins_flag=false
  local any_flag_set=false

  # Parse arguments (supports multiple flags)
  for arg in "$@"; do
    case "${arg}" in
      --gsd)
        install_gsd_flag=true
        any_flag_set=true
        ;;
      --oac)
        install_oac_flag=true
        any_flag_set=true
        ;;
      --plugins)
        verify_plugins_flag=true
        any_flag_set=true
        ;;
      --help|-h)
        usage
        return 0
        ;;
      --all)
        install_gsd_flag=true
        install_oac_flag=true
        verify_plugins_flag=true
        any_flag_set=true
        ;;
      *)
        log_err "Unknown option: ${arg}"
        usage
        return 1
        ;;
    esac
  done

  # Default to --all when no flags specified
  if [[ "${any_flag_set}" == false ]]; then
    install_gsd_flag=true
    install_oac_flag=true
    verify_plugins_flag=true
  fi

  check_prerequisites

  [[ "${install_gsd_flag}" == true ]] && install_gsd
  [[ "${install_oac_flag}" == true ]] && install_oac
  [[ "${verify_plugins_flag}" == true ]] && verify_plugins

  print_summary
}

main "$@"
