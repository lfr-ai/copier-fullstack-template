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
