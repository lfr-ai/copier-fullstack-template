# Copier Fullstack Template

Production-ready project scaffolding for fullstack Python + TypeScript applications following clean / hexagonal architecture, modern best practices, and global standards.

---

## Quick Start

### Prerequisites

| Tool                     | Purpose                | Auto-installed?      |
| ------------------------ | ---------------------- | -------------------- |
| **Python 3.12+**         | Backend runtime        | Yes (via `uv`)       |
| **uv**                   | Python package manager | Yes                  |
| **Node.js 22 LTS**       | Frontend runtime       | Yes (via `fnm`)      |
| **pnpm**                 | Node package manager   | Yes (via `corepack`) |
| **Docker** or **Podman** | Container runtime      | Yes                  |
| **go-task**              | Task runner            | Yes                  |
| **Git**                  | Version control        | Yes                  |
| **VS Code**              | Editor                 | Yes                  |
| **zsh**                  | Shell                  | Yes                  |
| **pre-commit**           | Git hooks              | Yes (via `uv`)       |
| **WSL2** (Windows only)  | Linux on Windows       | Yes                  |

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

| Choice                          | Options                               | Default                        |
| ------------------------------- | ------------------------------------- | ------------------------------ |
| **Project name**                | Any string                            | —                              |
| **Project description**         | Any string                            | A fullstack Python application |
| **Author name**                 | Any string                            | —                              |
| **Author email**                | Valid email address                   | —                              |
| **GitHub username**             | GitHub user or org                    | _(from author)_                |
| **Python version**              | 3.12, 3.13, 3.14                      | 3.13                           |
| **Node.js version**             | 20, 22, 24                            | 22                             |
| **Frontend framework**          | Lit (Web Components), React 19        | Lit                            |
| **Database**                    | None, PostgreSQL, Azure PostgreSQL    | PostgreSQL                     |
| **API style**                   | REST only, GraphQL only, Both         | REST                           |
| **GraphQL subscriptions**       | Yes / No (requires GraphQL)           | No                             |
| **Celery**                      | Yes / No                              | Yes                            |
| **Redis**                       | Yes / No                              | Yes                            |
| **Caddy** (reverse proxy)       | Yes / No                              | Yes                            |
| **Auth** (JWT + session)        | Yes / No                              | Yes                            |
| **Playwright** (E2E tests)      | Yes / No                              | Yes                            |
| **DevContainer**                | Yes / No                              | Yes                            |
| **AI / LLM**                    | Yes / No                              | No                             |
| **FAISS** (vector store)        | Yes / No (requires AI)                | No                             |
| **pgvector**                    | Yes / No (requires AI + PostgreSQL)   | No                             |
| **LangChain**                   | Yes / No (requires AI)                | No                             |
| **LlamaIndex**                  | Yes / No (requires AI)                | No                             |
| **Knowledge graph**             | Yes / No (requires AI)                | No                             |
| **KG backend**                  | NetworkX, Neo4j, RDFLib               | NetworkX                       |
| **External KG connectors**      | Yes / No (requires KG)                | No                             |
| **MCP server**                  | Yes / No (requires AI)                | No                             |
| **RAG pipeline**                | Yes / No (requires AI)                | No                             |
| **AI agents**                   | Yes / No (requires AI)                | No                             |
| **CrewAI**                      | Yes / No (requires AI)                | No                             |
| **Anthropic**                   | Yes / No (requires AI)                | No                             |
| **Azure OpenAI**                | Yes / No (requires Azure + AI)        | No                             |
| **Azure AI Search**             | Yes / No (requires Azure + AI)        | No                             |
| **Azure Document Intelligence** | Yes / No (requires Azure + AI)        | No                             |
| **SSH / SFTP**                  | Yes / No                              | No                             |
| **OpenCode**                    | Yes / No                              | No                             |
| **GSD-2**                       | Yes / No (requires OpenCode)          | No                             |
| **Container runtime**           | Docker, Podman                        | Podman                         |
| **Cloud provider**              | None, Azure                           | None                           |
| **Azure location**              | Any Azure region (requires Azure)     | swedencentral                  |
| **Secret backend**              | Env files, Azure KV                   | Env                            |
| **License**                     | MIT, Apache-2.0, GPL-3.0, Proprietary | MIT                            |

---

## What Gets Installed

The `scripts/install/install-all.zsh` script installs the **complete development environment** in order:

**Always installed:**

1. **Git** — version control with recommended global config
2. **Zsh** — shell with Oh My Zsh, autosuggestions, syntax highlighting, fzf
3. **Python** — via `uv` (Astral's fast Python installer and package manager)
4. **Node.js + pnpm** — via `fnm` (Fast Node Manager) and `corepack`
5. **Container engine** — Docker or Podman (based on `copier.yml` choice)
6. **go-task** — modern task runner (`Taskfile.yml`)
7. **VS Code** — with all recommended extensions pre-installed
8. **Linters** — hadolint, shellcheck, yamllint

**Conditional (based on template choices):**

- **DevContainer** — _(if enabled)_ `@devcontainers/cli` setup
- **Caddy** — _(if enabled)_ reverse proxy with automatic HTTPS
- **Redis** — _(if enabled)_ installed as a container service for caching and message brokering
- **FAISS** — _(if enabled)_ system deps + `faiss-cpu` Python package
- **Neo4j** — _(if knowledge graph + neo4j backend)_ graph database + Python driver
- **Azure CLI + Bicep** — _(if cloud provider is Azure)_ cloud management tooling
- **OpenCode + ecosystem** — _(if enabled)_ CLI, GSD, plugins

After installation, `scripts/bootstrap.zsh` handles project-specific setup:

- Prerequisite verification (Git, Task, uv, Node, pnpm, container runtime, and conditional Caddy/Azure CLI)
- `.env` creation from `.env.example`
- `uv sync --all-groups` — install all Python dependencies
- `pnpm install` — install all frontend dependencies
- `pre-commit install` — activate Git hooks (both `pre-commit` and `commit-msg`)

---

## Features

- **Clean / hexagonal (ports-and-adapters) architecture** with the Dependency Rule enforced
- **FastAPI** backend with Pydantic v2 strict validation and SQLAlchemy 2.0 async
- **TypeScript frontend** (Lit Web Components or React 19) with Vite, Tailwind CSS v4, Vitest
- **PostgreSQL** — production-grade database via repository/unit-of-work pattern
- **Redis + Celery** — _(conditional)_ async task processing and caching
- **Caddy** — _(conditional)_ reverse proxy with auto-TLS, compression, security headers
- **GraphQL** — _(conditional)_ Strawberry GraphQL with DataLoaders, depth limiting, and error masking
- **AI/LLM abstraction** — _(conditional)_ OpenAI, Anthropic, Azure OpenAI via LiteLLM gateway
- **RAG pipeline** — _(conditional)_ ingestion, vector/graph/hybrid retrieval, reranking
- **AI agents** — _(conditional)_ ReAct, tool-calling, LangGraph workflow engine with durable checkpointing
- **Knowledge graphs** — _(conditional)_ NetworkX, Neo4j, RDFLib backends with LLM triplet extraction
- **MCP server** — _(conditional)_ Model Context Protocol with streamable-http transport
- **CrewAI** — _(conditional)_ multi-agent orchestration with HMAS hierarchical processes
- **Centralized naming registry** — JSON → generated Python constants, TypeScript enums, and `.env` keys
- **Docker Compose** with per-environment overrides (dev, test, staging, prod)
- **Azure Bicep IaC** — _(conditional)_ infrastructure as code
- **DevContainer** — _(conditional)_ reproducible development environments
- **GitHub Actions CI/CD** — lint, test, build, deploy, CodeQL security scanning
- **Renovate** for automated dependency updates
- **Pre-commit hooks** — ruff, ty, prettier, detect-secrets, typos, shellcheck, hadolint, markdownlint
- **Testing** — pytest (unit, integration, property-based, performance), Vitest, Playwright E2E
- **Full documentation** — architecture, setup, development, testing, deployment, config, ADRs, conventions

---

## Project Structure (Generated)

```text
my-project/
├── .devcontainer/            # DevContainer config (conditional: use_devcontainer)
├── .github/                  # GitHub Actions CI/CD, Dependabot, skills, agents
│   ├── workflows/            # CI, deploy, CodeQL workflows
│   └── agents/               # Copilot agent instructions
├── .gsd/                     # GSD-2 autonomous agent (conditional: with_gsd)
├── .opencode/                # OpenCode AI agent config (conditional: with_opencode)
├── backend/
│   ├── src/my_project/       # Backend (clean / hexagonal architecture)
│   │   ├── adapters/         # Outbound: DB repos, cache, email, storage, auth
│   │   ├── ai/               # LLM/agent tooling (conditional: use_ai)
│   │   ├── application/      # Use cases, services, DTOs, commands, queries
│   │   ├── config/           # Settings, constants, logging, DI container
│   │   ├── core/             # Pure domain (entities, enums, interfaces, value objects)
│   │   ├── infrastructure/   # DB engines, HTTP clients, security, profiling
│   │   ├── ports/            # Inbound: API routes, CLI, web
│   │   │   ├── api/middleware/ # CORS, auth, rate limiting, error handling
│   │   │   └── graphql/      # Strawberry schema (conditional: graphql/both)
│   │   └── utils/            # Shared utilities
│   ├── tests/                # unit, integration, property, performance
│   └── alembic/              # Database migrations
├── frontend/                 # TypeScript + Vite + Tailwind CSS
├── registry/                 # Naming registry + code generator + tests
├── docs/                     # Architecture, setup, ADRs, conventions, diagrams
├── scripts/                  # Bootstrap, install, setup, health-check
│   └── install/              # Per-tool auto-installers (zsh + ps1)
├── tasks/                    # Taskfile includes (backend, frontend, docker, infra)
├── infra/                    # IaC (Azure Bicep) — conditional: cloud_provider == azure
├── caddy/                    # Caddyfile + Containerfile — conditional: use_caddy
├── logs/                     # Runtime logs (.gitkeep)
├── compose.yml               # Base services with healthchecks
├── compose.override.yml      # Local dev overrides
├── compose.dev.yml           # Development config
├── compose.staging.yml       # Staging config
├── compose.prod.yml          # Production config
├── compose.test.yml          # CI test config
├── Containerfile             # Multi-stage production build
├── docker-bake.hcl           # Docker Buildx Bake orchestration (multi-image builds)
├── docker-bake.override.hcl  # Local Bake cache overrides
├── Taskfile.yml              # go-task commands (includes tasks/*.yml)
└── tox.ini                   # Tox configuration for backend test matrices
```

---

## Available Commands

After setup, use `task --list` to see all available commands:

**Core workflow:**

| Command             | Description                                   |
| ------------------- | --------------------------------------------- |
| `task setup`        | Full project setup (deps + pre-commit + .env) |
| `task dev`          | Start backend + frontend in dev mode          |
| `task dev:backend`  | Start backend only with hot reload            |
| `task dev:frontend` | Start frontend only with HMR                  |
| `task start`        | Start all services (compose up)               |
| `task build`        | Build everything for production               |
| `task clean`        | Remove all build artifacts and caches         |

**Testing:**

| Command                 | Description                                               |
| ----------------------- | --------------------------------------------------------- |
| `task test`             | Run default tests (registry + unit + property + frontend) |
| `task test:unit`        | Run unit tests only                                       |
| `task test:integration` | Run integration tests                                     |
| `task test:property`    | Run property-based tests (Hypothesis)                     |
| `task test:performance` | Run performance benchmarks                                |
| `task test:coverage`    | Run tests with coverage report                            |
| `task test:e2e`         | Run Playwright E2E tests _(conditional)_                  |

**Code quality:**

| Command               | Description                                |
| --------------------- | ------------------------------------------ |
| `task lint`           | Run all linters                            |
| `task format`         | Format all code                            |
| `task typecheck`      | Run type checkers                          |
| `task pre-commit`     | Run pre-commit on all files                |
| `task security:audit` | Audit all dependencies for vulnerabilities |

**Infrastructure:**

| Command                  | Description                                  |
| ------------------------ | -------------------------------------------- |
| `task docker:up`         | Start all Docker services                    |
| `task docker:down`       | Stop all Docker services                     |
| `task docker:build`      | Build container images (compose build)       |
| `task docker:bake`       | Build images via Buildx Bake _(Docker only)_ |
| `task db:migrate`        | Run database migrations (Alembic)            |
| `task db:seed`           | Seed the database with development data      |
| `task registry:generate` | Generate code from naming registry           |
| `task health`            | Check health of all running services         |
| `task worker`            | Start Celery worker _(conditional)_          |

---

## License

See [LICENSE](LICENSE) for details.
