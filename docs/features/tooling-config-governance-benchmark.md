# Tooling and config governance benchmark (koda_refactor)

## Purpose and scope

This feature document captures an exhaustive comparison between this template
repository and `koda_refactor` for:

- tool/metafile structure,
- pre-commit quality gates,
- settings/runtime configuration patterns,
- naming/class conventions for environment settings.

It also records what was scaffolded in this repository based on that benchmark.

## Analyzed files

### External reference (`koda_refactor`)

- `pyproject.toml`
- `.pre-commit-config.yaml`
- `Taskfile.yml`
- `ruff.toml`, `tox.ini`, `ty.toml`, `pytest.ini`, `.cz.toml`
- `src/koda/configs/base.py`
- `src/koda/configs/runtime.py`
- `src/koda/configs/_validators.py`
- `src/koda/configs/environments/{local,dev,test,staging,prod}.py`
- `src/koda/composition/container.py`
- `.github/copilot-instructions.md`, `AGENTS.md`, `.github/instructions/*`

### Template repository (`copier-fullstack-template`)

- `template/.pre-commit-config.yaml.jinja`
- `template/Taskfile.yml.jinja`
- `template/backend/src/{{ project_slug }}/config/settings/base.py.jinja`
- `template/backend/src/{{ project_slug }}/config/settings/runtime.py.jinja`
- `template/backend/src/{{ project_slug }}/config/settings/{local,dev,test,staging,prod}.py.jinja`

## Business rules and constraints

- This repository is a Copier template source; changes must happen under
  `template/` to affect generated projects.
- Pre-commit policy must remain strict but practical: fast checks at
  `pre-commit`, expensive tests at `pre-push/manual`.
- Environment resolution must be deterministic and safe by default.
- Production-like environments must enforce secret key correctness.

## Workflows and outcomes

### 1) Dependency auditing workflow

Observed in `koda_refactor`: lock-aware dependency audit flow using `uv export`
and `pip-audit` with deterministic inputs.

Applied scaffold:

- Added generated script:
  `template/tools/security/dependency_audit.py.jinja`
  (exports from generated `backend/` project lock context)
- Wired script into generated pre-commit:
  `template/.pre-commit-config.yaml.jinja` (new `dependency-audit` local hook)
- Updated generated task runner:
  `template/Taskfile.yml.jinja` (`security:audit` now calls the script)

### 2) Runtime environment safety workflow

Observed in `koda_refactor`: explicit runtime environment selection logic and
deterministic resolution flow.

Applied scaffold:

- Enhanced `template/backend/src/{{ project_slug }}/config/settings/runtime.py.jinja`
  with structured warning logs for invalid environment values discovered in
  process env or `.env` files, while preserving existing precedence semantics.

## Data models, dependencies, integrations

- Tooling dependencies involved:
  - `uv` (lock-aware dependency export)
  - `pip-audit` (vulnerability scanning)
  - `pre-commit` (hook orchestration)
  - `go-task` (task orchestration)
- No runtime API/data contract changes introduced by this benchmark pass.

## API/UI surface

- No API endpoint changes.
- No frontend component or route changes.

## Security and authorization implications

- Improves supply-chain scanning consistency via deterministic lock export.
- Improves configuration observability with warnings for malformed runtime env
  values.
- Maintains strict production/staging secret key safeguards already present in
  settings classes.
