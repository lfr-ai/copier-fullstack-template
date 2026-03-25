# Copier Fullstack Template

Production-ready project scaffolding for fullstack Python + TypeScript applications following clean / hexagonal architecture, modern best practices, and global standards.

---

## Quick Start

### Prerequisites

| Tool                     | Purpose                  | Auto-installed?      |
| ------------------------ | ------------------------ | -------------------- |
| **Python 3.12+**         | Backend runtime          | Yes (via `uv`)       |
| **uv**                   | Python package manager   | Yes                  |
| **Node.js 22 LTS**       | Frontend runtime         | Yes (via `fnm`)      |
| **pnpm**                 | Node package manager     | Yes (via `corepack`) |
| **Docker** or **Podman** | Container runtime        | Yes                  |
| **go-task**              | Task runner              | Yes                  |
| **Git**                  | Version control          | Yes                  |
| **VS Code**              | Editor                   | Yes                  |
| **WSL2** (Windows only)  | Linux on Windows         | Yes                  |
| **Redis**                | Cache and message broker | Yes (conditional)    |
| **Celery**               | Async task processing    | Yes (conditional)    |
| **Caddy**                | Reverse proxy (HTTPS)    | Yes (conditional)    |
| **Cloud CLI**            | Azure CLI (`az`)         | Yes (conditional)    |
| **zsh**                  | Shell                    | Yes                  |
| **pre-commit**           | Git hooks                | Yes (via `uv`)       |
| **hadolint**             | Containerfile linting    | Recommended          |
| **ShellCheck**           | Shell script linting     | Recommended          |

### Usage — Local-First (Recommended)

This template is designed to be used **locally** after cloning or forking — **no remote `gh:your-org/...` URL needed**.

```bash
# 1. Clone or fork the template repository
git clone https://github.com/<your-fork>/copier-fullstack-template.git
cd copier-fullstack-template

# 2. Install uv if not present
curl -LsSf https://astral.sh/uv/install.sh | sh

# 3. Generate a new project from the LOCAL template
uvx copier copy --trust . ../my-new-project

# 4. Enter the generated project
cd ../my-new-project

# 5. Install all prerequisites (if not already present)
zsh scripts/install/install-all.zsh

# 6. Bootstrap the project (install deps, pre-commit, .env)
zsh scripts/bootstrap.zsh

# 7. Start developing
task dev
```

> **Key**: `uvx copier copy --trust . <destination>` uses the **current local directory** as the template source. The `.` refers to `copier.yml` + `template/` in the current directory. No `gh:your-org/...` URL is needed.

### Windows Users

Open PowerShell as Administrator:

```powershell
# Step 1: Install all Windows prerequisites (WSL2, VS Code, Git, Python, etc.)
Set-ExecutionPolicy Bypass -Scope Process -Force
.\scripts\install\install-all.ps1

# Step 2: Restart if WSL2 was just installed

# Step 3: Generate a project
uvx copier copy --trust . ..\my-new-project

# Step 4: In WSL/Ubuntu, install the Linux toolchain
cd /mnt/c/Users/YourUser/my-new-project
zsh scripts/install/install-all.zsh
zsh scripts/bootstrap.zsh
task dev
```

### Alternative: Generate from a Remote Repository

If you prefer to use a remote URL (e.g., after publishing your fork):

```bash
uvx copier copy --trust gh:<your-username>/copier-fullstack-template my-project
```

### Update an Existing Project

```bash
cd my-existing-project
uvx copier update --trust
```

---

## Template Choices

During `copier copy`, you'll be prompted for:

| Choice                     | Options                               | Default    |
| -------------------------- | ------------------------------------- | ---------- |
| **Project name**           | Any string                            | —          |
| **Python version**         | 3.12, 3.13                            | 3.13       |
| **Node.js version**        | 20, 22                                | 22         |
| **Database**               | None, PostgreSQL, Azure PostgreSQL    | PostgreSQL |
| **Celery**                 | Yes / No                              | Yes        |
| **Redis**                  | Yes / No                              | Yes        |
| **Caddy** (reverse proxy)  | Yes / No                              | Yes        |
| **Auth** (JWT + session)   | Yes / No                              | Yes        |
| **Playwright** (E2E tests) | Yes / No                              | Yes        |
| **DevContainer**           | Yes / No                              | Yes        |
| **OpenCode**               | Yes / No                              | No         |
| **Container runtime**      | Docker, Podman                        | Podman     |
| **Cloud provider**         | None, Azure                           | None       |
| **Secret backend**         | Env files, Azure KV                   | Env        |
| **License**                | MIT, Apache-2.0, GPL-3.0, Proprietary | MIT        |

---

## What Gets Installed

The `scripts/install/install-all.zsh` script installs the **complete development environment** in order:

1. **Git** — version control with recommended global config
2. **Zsh** — shell with Oh My Zsh, autosuggestions, syntax highlighting, fzf
3. **Python** — via `uv` (Astral's fast Python installer and package manager)
4. **Node.js + pnpm** — via `fnm` (Fast Node Manager) and `corepack`
5. **Container engine** — Docker or Podman (based on `copier.yml` choice)
6. **go-task** — modern task runner (`Taskfile.yml`)
7. **VS Code** — with all recommended extensions pre-installed
8. **DevContainer** — (conditional) for fully reproducible development environments
9. **Caddy** — (conditional) reverse proxy with automatic HTTPS
10. **Redis** — (conditional) local server as fallback to container
11. **Cloud CLI** — (conditional) Azure CLI + Bicep

After installation, `scripts/bootstrap.zsh` handles project-specific setup:

- `uv sync --all-groups` — install all Python dependencies
- `pnpm install` — install all frontend dependencies
- `pre-commit install` — activate Git hooks
- `.env` creation from `.env.example`
- Prerequisite verification (including container runtime, cloud CLI, Caddy)

---

## Features

- **Clean / hexagonal (ports-and-adapters) architecture** with the Dependency Rule enforced
- **FastAPI** backend with Pydantic v2 strict validation
- **TypeScript frontend** with Vite, Tailwind CSS, Vitest
- **PostgreSQL** — production-grade database via repository/adapter pattern
- **Redis + Celery** — (conditional) async task processing and caching
- **Caddy** — (conditional) reverse proxy with auto-TLS, compression, security headers
- **AI/LLM abstraction** — OpenAI, Anthropic, Azure OpenAI adapters
- **Centralized naming registry** with code generation
- **Docker Compose** with optional Caddy gateway profile
- **Azure Bicep IaC** — infrastructure as code (conditional on cloud provider)
- **DevContainer** for reproducible development
- **GitHub Actions CI/CD** — lint, test, build, deploy
- **Renovate** for automated dependency updates
- **Pre-commit hooks** — ruff, ty, prettier, detect-secrets, typos, shellcheck, hadolint
- **Testing** — pytest (unit, integration, property), Vitest, Playwright E2E
- **Full documentation** — architecture, setup, development, testing, deployment, ADRs

---

## Project Structure (Generated)

```
my-project/
├── src/my_project/           # Backend (clean / hexagonal architecture)
│   ├── adapters/             # External integrations (DB, cache, APIs)
│   ├── ai/                   # LLM/agent tooling
│   ├── application/          # Use cases, services, DTOs
│   ├── config/               # Settings, DI container, logging
│   ├── core/                 # Pure domain (entities, enums, interfaces)
│   ├── infrastructure/       # DB engines, HTTP clients, security
│   ├── middleware/           # Auth, CORS, rate limiting, logging
│   ├── models/               # Pydantic request/response schemas
│   ├── ports/                # API routes, CLI, webhooks
│   └── utils/                # Shared utilities
├── frontend/                 # TypeScript + Vite + Tailwind
├── tests/                    # unit, integration, e2e, property
├── data/                     # Seeds, migrations, naming registry
├── docs/                     # Architecture, setup, ADRs
├── scripts/                  # Bootstrap, install, setup
│   └── install/              # Per-tool auto-installers (zsh + ps1)
├── infra/                    # IaC (Azure Bicep / OpenTofu) — conditional
├── caddy/                    # Caddyfile + Containerfile — conditional
├── logs/                     # Runtime logs (.gitkeep)
├── compose.yml               # Base services with healthchecks
├── compose.override.yml      # Local dev overrides
├── compose.prod.yml          # Production config
├── compose.test.yml          # CI test config
├── Containerfile             # Multi-stage production build
├── Taskfile.yml              # go-task commands
├── pyproject.toml            # Python project config
└── ...                       # Config files (ruff, prettier, eslint, etc.)
```

---

## Available Commands

After setup, use `task --list` to see all available commands:

| Command                  | Description                          |
| ------------------------ | ------------------------------------ |
| `task setup`             | Full project setup                   |
| `task dev`               | Start backend + frontend in dev mode |
| `task build`             | Build everything for production      |
| `task test`              | Run all tests                        |
| `task test:unit`         | Run unit tests only                  |
| `task test:integration`  | Run integration tests                |
| `task test:e2e`          | Run Playwright E2E tests             |
| `task test:coverage`     | Run tests with coverage report       |
| `task lint`              | Run all linters                      |
| `task format`            | Format all code                      |
| `task typecheck`         | Run type checkers                    |
| `task docker:up`         | Start all Docker services            |
| `task docker:down`       | Stop all Docker services             |
| `task db:migrate`        | Run database migrations              |
| `task registry:generate` | Generate code from naming registry   |
| `task clean`             | Remove all build artifacts           |

---

## License

See [LICENSE](LICENSE) for details.
