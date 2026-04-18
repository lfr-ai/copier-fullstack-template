# Feature: quality gates and tooling

## Purpose and scope

Implements repository quality gates for architecture boundaries, coding conventions,
render validation, and generated-project regression checks.

## Analyzed files

- `Taskfile.yml`
- `.pre-commit-config.yaml`
- `scripts/check-architecture-boundaries.py`
- `scripts/check-no-final.py`
- `scripts/check-fastapi-status-codes.py`
- `template/.pre-commit-config.yaml.jinja`

## Business rules and constraints

- Clean Architecture guardrails are mandatory (`Taskfile.yml:13`).
- `Final[...]` is banned for module-level constants and internal variables
  (`Taskfile.yml:20`, `scripts/check-no-final.py`).
- FastAPI status-code conventions are enforced (`Taskfile.yml:25`).
- Aggregate verification runs before CI expansion (`Taskfile.yml:114`).

## Workflows (with code references)

1. Local checks run through `task verify-all` (`Taskfile.yml:114`).
2. CI extends checks to render smoke + rendered tests (`Taskfile.yml:123`).
3. Pre-commit validates hygiene and linting with modern hook versions
   (`.pre-commit-config.yaml:8`, `.pre-commit-config.yaml:51`).
4. Heavy rendered tests are deferred to `pre-push/manual`
   (`.pre-commit-config.yaml:116`, `.pre-commit-config.yaml:124`).

## Data models and dependencies

- Verification scripts scan `template/backend/src` recursively.
- Status-code verifier uses regex checks for numeric literals and Starlette imports
  (`scripts/check-fastapi-status-codes.py:16`, `:17`).

## Integrations

- `go-task` orchestrates all verification commands.
- `pre-commit` provides local and staged policy enforcement.
- External linters include Ruff, Bandit, yamllint, markdownlint, typos, actionlint.

## API endpoints or UI components

Not applicable; this feature is build/quality infrastructure.

## Security and authorization

- Secret scanning is enabled via `detect-secrets`.
- Bandit runs with TOML extra support for policy-driven checks.
- Branch protection hook blocks direct commits to `main`.
