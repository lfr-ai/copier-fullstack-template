# Changelog

All notable changes to copier-fullstack-template will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- FastAPI status-code convention checker (`scripts/check-fastapi-status-codes.py`)
- Task wiring for FastAPI status-code enforcement (`conventions:fastapi-status-codes`)
- Root-level architecture and feature analysis docs under `docs/`

### Changed

- Standardized width settings to 88 for markdownlint/yamllint in root and template
- Updated and simplified root/template pre-commit baselines for iterative onboarding
- Strengthened coding instructions around internal naming, `Final[...]` avoidance,
  selective `Annotated[...]` usage, and typed docstring sections
- Updated backend template Ruff formatting to single-quote style
- Wired LightRAG and RAG-Anything into backend runtime settings, container factories,
  and environment documentation
- Added generated dependency-audit scaffolding (`tools/security/dependency_audit.py`)
  and wired it into pre-commit plus task-based security audits
- Added runtime environment invalid-value warning diagnostics in generated backend
  settings resolver
- Added module/file-level docstring enforcement checker and wired it into root
  and template pre-commit/task verification flows
- Refactored generated backend settings validation into reusable
  `config/settings/_validators.py` helpers and strengthened auth/secret checks
- Expanded generated backend config test scaffolding with runtime precedence and
  settings-mapping regression coverage
- Added combined adaptive RAG orchestration controls to generated backend API
  models/services, enabling Self-CRAG + DeepRAG + optional LightRAG execution
  with strategy-based routing and graceful fallback behavior
- Relaxed generated backend LiteLLM dependency constraint to
  `litellm>=1.83.12,<2` so AI-enabled scaffolds resolve consistently during
  smoke renders
- Fixed non-template Python sources that accidentally contained raw Jinja
  imports/placeholders, preventing syntax/runtime errors in rendered projects
- Fixed generated `VectorStoreGateway` forward-reference typing issue by
  enabling postponed annotation evaluation in `core/interfaces/vector_store.py`
- Stabilized generated adaptive-pipeline unit tests for slotted class patching,
  lazy initialization checks, and LightRAG-unavailable fallback expectations

## [0.1.0] - 2026-04-10

### Added

- Copier template engine with `copier.yml` configuration
- Clean Architecture backend scaffold (core, application, infrastructure, presentation)
- FastAPI REST API with health checks and OpenAPI docs
- SQLAlchemy async ORM with Alembic migrations
- React 19 + Vite + TypeScript frontend with Biome linting
- Optional AI/RAG layer (LiteLLM, FAISS, Neo4j, LangGraph workflows)
- Optional Playwright E2E testing setup
- Optional Storybook component development environment
- Docker/Podman containerization with multi-stage builds
- GitHub Actions CI/CD (CI, CD, CodeQL, dependency review, release)
- Azure infrastructure-as-code (Bicep) with deployment scripts
- Pre-commit hooks for code quality
- Structured logging with structlog
- VS Code workspace configuration and Copilot customizations
- GitHub Copilot agents, skills, instructions, hooks, and prompts
- Taskfile-based task runner for development workflows
- Renovate configuration for automated dependency updates
- Comprehensive test structure (unit, integration, property, performance)
- Template verification Taskfile for CI checks

### Removed

- Stale development sandbox (`src/`, `core/`, `tests/` at root)
- Build artifacts (`.coverage`, `htmlcov/`)
