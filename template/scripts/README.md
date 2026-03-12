
Shell scripts for project setup, bootstrap, and maintenance.


| Script | Purpose |
|--------|---------|
| `install/install-all.zsh` | Install ALL development prerequisites (Linux/macOS/WSL) |
| `install/install-all.ps1` | Install ALL prerequisites (Windows PowerShell) |
| `bootstrap.zsh` | Full project bootstrap (deps, hooks, env) |
| `setup.zsh` | Quick setup (deps + pre-commit) |
| `health-check.zsh` | Verify all services are healthy |
| `run_migrations.zsh` | Run database migrations |
| `seed_database.zsh` | Seed database with development data |


Individual installers for each tool, called by `install-all.zsh`:

| Script | Tool |
|--------|------|
| `install-git.zsh` | Git with recommended config |
| `install-zsh.zsh` | Zsh with Oh My Zsh |
| `install-python.zsh` | Python via uv |
| `install-pnpm.zsh` | Node.js via fnm + pnpm via corepack |
| `install-container-engine.zsh` | Docker or Podman |
| `install-task.zsh` | go-task CLI |
| `install-vscode.zsh` | VS Code with extensions |
| `install-hadolint.zsh` | Containerfile linter |
| `install-shellcheck.zsh` | Shell script linter |


```bash
zsh scripts/install/install-all.zsh

zsh scripts/bootstrap.zsh

zsh scripts/setup.zsh
```
