# Changelog

All notable changes to copier-fullstack-template will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- FastAPI status-code convention checker (`scripts/check-fastapi-status-codes.py`)
- Task wiring for FastAPI status-code enforcement (`conventions:fastapi-status-codes`)
- Root-level architecture and feature analysis docs under `docs/`
- OpenSpec SDD scaffolding in generated projects (`openspec/config.yaml`, baseline
  specs, and a custom `clean-arch-spec-driven` schema)
- OpenSpec task include (`tasks/openspec.yml`) with init/update/validate/schema
  commands and SDD verification alias (`test:sdd:verify`)
- OpenSpec workflow skills for both Copilot and Claude
  (`openspec-workflow/SKILL.md`)
- Copilot OPSX prompt aliases (`opsx-propose`, `opsx-apply`, `opsx-sync`,
  `opsx-archive`, `opsx-explore`)
- ADR-0009 documenting adoption of OpenSpec for spec-driven development
- Frontend-focused Copilot skill packs in root and template for accessibility,
  Playwright E2E, and shadcn/ui composition parity
- Template-scaffolded GitNexus prompt pack
  (`template/.github/prompts/gitnexus/*`)
- Template-scaffolded OpenSpec nested prompt pack
  (`template/.github/prompts/openspec/*`)
- Template-scaffolded Claude command packs for GitNexus and OpenSpec/OPSX
  (`template/.claude/commands/{gitnexus,openspec,opsx}`)
- Template-scaffolded Claude skills for DDD, DRY/jscpd, GitNexus, quality-gate,
  SDD, and TDD parity
- Root planning stubs for template-repo OpenSpec and GitNexus workflows
  (`openspec/README.md`, `.gitnexus/README.md`)
- Root `.agents/` and `.azuredevops/` governance scaffolding with baseline
  pipelines, reusable step templates, shared variables, and policy JSON examples
- Root folder policy stubs for `docker/`, `azure/`, and `caddy/` to enforce
  folder-based runtime asset layout
- Template `.agents/` scaffolding for generated-project agent workspace parity

### Changed

- Removed thin inheritance layers in template backend application code by
  deleting `BaseService`, `CommandHandler`, and `QueryHandler` base abstractions
  and simplifying services/handlers to plain classes with explicit dependencies
- Removed abstraction-only backend template unit tests tied to deleted base
  classes (`test_base_service.py.jinja`, `test_command_handler.py.jinja`,
  `test_query_handler.py.jinja`)
- Simplified `scripts/check-github-alignment.py` by replacing duplicated
  required/legacy file-existence loops with a single policy-driven helper
  (`_collect_paths_with_existence_mismatch`)
- Tightened architecture boundary policy by disallowing `ai -> infrastructure`
  imports in `scripts/check-architecture-boundaries.py` and documenting the
  rationale in quality-gate feature docs
- Simplified generated FastAPI dependency helpers to inject the container
  dependency directly into service providers in
  `presentation/api/dependencies.py.jinja`
- Reduced prompt cognitive load by showing `secret_backend` only when
  `cloud_provider == 'azure'` in `copier.yml`
- Normalized template-render verification docs to the canonical `task render`
  workflow with one consistent fallback command pattern
- Simplified `.pre-commit-config.yaml` by removing a duplicate
  `pre-commit-hooks` repository declaration and consolidating
  `check-vcs-permalinks` into the primary hooks block
- Simplified `.editorconfig` by removing file-type sections that only repeated
  global default indentation values
- Simplified `ruff.toml` by removing explicit formatter options that matched
  Ruff defaults (`quote-style`, `indent-style`)
- Simplified `.markdownlint-cli2.yaml` by removing redundant
  `config.default: true` boilerplate
- Refreshed `docs/TODO-COMPREHENSIVE-IMPLEMENTATION.md` into a pass-based,
  execution-oriented cleanup plan with explicit verification gates
- Reduced cognitive complexity in validation scripts by decomposing
  `scripts/check-architecture-boundaries.py`,
  `scripts/check-module-docstrings.py`,
  `scripts/check-fastapi-status-codes.py`, and
  `scripts/validate-template.py` into smaller SRP helpers while preserving
  behavior
- Simplified shared Python-like file traversal in
  `scripts/_python_file_utils.py` with a single candidate iterator helper to
  remove repeated scan-path branching
- Tuned `jscpd.json` ignore scope to exclude intentional mirrored governance,
  generated planning, and documentation surfaces (`.agents`, `.claude`,
  `.github`, `.azuredevops`, `.gsd`, `docs`, `openspec`) so clone detection
  reports actionable implementation duplication only
- Simplified mirror-entry validation flow in
  `scripts/check-github-alignment.py` by extracting schema validation and
  flattening missing-asset checks, resulting in an all-A complexity profile
  across the entire `scripts/` validation suite
- Simplified `.gitignore` by removing redundant duplicate ignore patterns for
  `.gsd-id` and `.bg-shell/`
- Added cross-platform `scripts/check-github-alignment.py` and switched
  `Taskfile.yml` `github:alignment` to Python execution for reliable Windows/
  Unix verification parity
- Moved `scripts/check-github-alignment.py` required/legacy/scan-path policy
  into `docs/cross-cuttings/agentic-ownership-map.json` to eliminate duplicated
  hardcoded lists in script code
- Expanded ownership-matrix drift checks to additional mirrored agentic
  surfaces (`.claude/agents`, `.claude/commands`, `.github/hooks`, and shared
  `.github/prompts` subsets)
- Narrowed internal prompt compatibility surface by switching evaluator
  backtest tooling and general prompt-template tests to
  `Jinja2PromptTemplate`, while keeping `PromptManager` as explicit legacy
  compatibility alias coverage
- Replaced integration-test placeholder `assert True` branches with explicit
  `pytest.skip(...)` semantics for unsupported backend/database variants
- Standardized ownership-matrix mirror policy schema with explicit
  `requiredInRoot`, `requiredInTemplate`, and `optional` semantics consumed by
  `scripts/check-github-alignment.py`
- Aligned root/template Lychee hook versions to `lychee-v0.24.2` and
  documented intentional hook-id divergence (`lychee-docker` for root,
  `lychee` for generated template) based on environment portability
- Documented canonical cross-cutting baselines for GitHub Actions major-version
  policy, markdownlint scope/rule baseline, and MCP core-vs-optional server set
- Added required manual pre-merge GitNexus graph-consistency checklist to
  `docs/cross-cuttings/gitnexus-runbook.md`
- Pinned `jscpd` command examples in root/template `jscpd` and
  `dry-refactoring` skill docs to `4.0.5` for compatibility with the current
  `jscpd.json` schema (`skipBlocks`)
- Renamed root/template jscpd configuration files from `.jscpd.json` to
  `jscpd.json` and updated all commands/checks for consistency across root and
  template workflows
- Aligned MCP configuration with golden-standard dual config files
  (`.vscode/mcp.json` + `.claude/mcp.json`) and added GitNexus server wiring
- Added Playwright MCP server wiring in root and template MCP configs using the
  official `@playwright/mcp` package with isolated/headless defaults
- Added file-backed AI prompt registry with immutable version files
  (`backend/prompts/versions/*`) and profile-based selection (`backend/prompts/registry.json`)
- Added prompt provisioning and backtest run metadata utilities so evaluator
  runs can include prompt-version-aware run names
- Updated template MCP scaffolding to use HTTP Context7 and stdio GitNexus
  (`gitnexus mcp`) with workspace-root cwd
- Hardened OpenAPI/OpenSpec automation by replacing unsafe CI installer piping
  with official `oasdiff` GitHub Actions and enforced breaking-change gates
- Improved generated OpenAPI task commands to use reproducible `npx -y ...@latest`
  invocation and documented safer oasdiff usage paths
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
- Switched PostgreSQL/Azure PostgreSQL template variants to local SQLite defaults,
  profile-gated server PostgreSQL containers, runtime dialect-aware migration/engine
  behavior, and added a local PostgreSQL → SQLite data migration utility task
- Removed external-reference parity audit scripts/tasks and related
  documentation links to keep repository checks self-contained

### Removed

- Removed Warp terminal optional scaffolding from the template questionnaire and
  generated assets (`with_warp`, `.warp/`, and `install-warp` installers)
- Removed OpenCode optional scaffolding from the template questionnaire and
  generated assets (`with_opencode` and `.opencode/` context files)
- Removed OpenCode mentions from root/template `AGENTS.md` documentation

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
