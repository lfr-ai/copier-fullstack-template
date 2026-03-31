# Install Pipeline Audit — July 2026

## Critical Fixes Applied

### install-neo4j.zsh.jinja
- **FIXED**: Syntax-breaking line wraps — `gpg --dearmor -o` and `sudo tee` were split across lines without backslash continuation
- **FIXED**: Updated GPG keyring path from `/usr/share/keyrings/neo4j-archive-keyring.gpg` to `/etc/apt/keyrings/neotechnology.gpg` (matches current Neo4j official docs 2026)
- **FIXED**: Added `sudo mkdir -p /etc/apt/keyrings`
- **FIXED**: All bare `pip` → `uv pip` with `python3 -m pip` fallback

### install-redis.zsh.jinja
- **FIXED**: Syntax-breaking line wraps in `gpg --dearmor` and `deb [...]` source lines
- **FIXED**: GNU-specific `grep -oP` → portable `sed` for version extraction
- **FIXED**: Added `sudo mkdir -p /usr/share/keyrings`

### install-faiss.zsh.jinja
- **FIXED**: Bare `pip install` → `uv pip` primary / `python3 -m pip` fallback (both Linux and macOS)
- **NOTE**: PyPI has `faiss-cpu>=1.13` (faiss-wheels project), constraint is correct

### install-linters.zsh
- **FIXED**: Hardcoded `hadolint-Linux-x86_64` → auto-detected arch (`x86_64`/`arm64`)

### install-all.zsh.jinja
- **FIXED**: Broken line wrap in `save_log()` where `>` redirect was on next line

### install-zsh.zsh
- **FIXED**: `which zsh` → `command -v zsh` (POSIX-portable)

### install-vscode.zsh
- **FIXED**: Hardcoded `/tmp/packages.microsoft.gpg` → `mktemp` for secure temp files

### install-caddy.zsh
- **FIXED**: Removed unused `CADDY_MIN_VERSION="2.9"` variable
- **FIXED**: Hardcoded `/tmp/caddy` → `mktemp` for binary download

### setup-devcontainer.zsh
- **FIXED**: `verify_devcontainer_config` returned 1 on missing config, which killed script under `ERR_EXIT`. Now returns 0 with a warning.

### install-container.zsh.jinja
- **FIXED**: Docker package removal loop always used `apt-get` regardless of distro. Now guarded with `command -v apt-get`.

### install-cloud-cli.zsh.jinja
- **FIXED**: Azure CLI Linux install was Debian-only. Added `dnf` and `pip3` fallbacks.

## Bootstrap Enhancement
- Added Playwright browser install (`pnpm exec playwright install --with-deps chromium`) to `bootstrap.zsh.jinja` when `use_playwright` is enabled

## Documentation Updates
- `ONBOARDING.md.jinja`: Added Playwright browser install to setup steps list
- `README.md` (root): Added Playwright browser install to bootstrap description

## Cross-Check: copier.yml vs Installers
- All conditional features have matching install coverage in zsh orchestrator
- PS1 orchestrator correctly delegates FAISS/Neo4j to containerized or WSL
- `use_celery` relies on Redis (no separate installer needed)
- `use_playwright` relies on `pnpm install` + `playwright install` (now in bootstrap)

## Version Info (at time of audit)
- pnpm: Latest stable v10.33 (v11 is beta)
- faiss-cpu: v1.13.2 on PyPI
- Neo4j: v2026.02.2 (requires Java 21)
