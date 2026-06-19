# Koda Alignment and Production-Readiness Deep-Dive

## Purpose

This document captures an exhaustive alignment audit between:

- `copier-fullstack-template` (this repository)
- `koda_automation` (reference implementation)

Goal: enforce consistency in naming, structure, agentic setup, and quality-gate
patterns while preserving the template-repository model (`root` vs `template/`).

## Root vs Template Ownership Model

This repository is a **template source repository**, not a generated app.
Therefore, parity is enforced with this mapping:

- **Generated runtime/project artifacts** in reference repo → `template/`
   (`*.jinja` where applicable)
- **Template-development tooling and governance** → repository `root`
- **Cross-cutting AI/agent configuration** → usually both (`root` and
   `template/`), with root as subset where intentional

### Root/template/both placement matrix (enforcement baseline)

| Capability | Root (template repo) | Template (generated project) | Policy |
| --- | --- | --- | --- |
| Playwright | Optional local MCP wiring/docs | `template/.github/workflows/{% if use_playwright %}playwright.yml{% endif %}.jinja`, `template/frontend/{% if use_playwright %}playwright.config.ts{% endif %}` | **Template-first**, root only for template-dev validation |
| shadcn/ui skills | Root assistant config/docs | `template/.mcp.json.jinja`, frontend scaffolding | **Both** (root for authoring, template for consumers) |
| MCP server wiring | `.mcp.json`, `.claude/mcp.json` | `template/.mcp.json.jinja`, `template/.claude/mcp.json.jinja` | **Both** with root as subset mirror |
| GitNexus | Root docs/tooling for template maintainers | `template/{% if with_gitnexus %}.gitnexus{% endif %}/**` | **Both**, generated artifacts live in template |
| Pipelines (GitHub/Azure) | Root CI for template repository | `template/.github/workflows/*.jinja`, `template/.azuredevops/**/*.jinja` | **Separated by runtime** |
| CodeRabbit | Root repo review policy | `template/{% if use_coderabbit %}.coderabbit.yaml{% endif %}.jinja` | **Both** |
| Codecov | Optional root reporting for template CI | `template/.codecov.yml.jinja`, template CI upload step | **Template-first** |
| Keploy | Optional maintainer docs | `template/keploy.yml.jinja`, `template/docs/KEPLOY.md.jinja` | **Template-first** |
| Testcontainers | N/A for root (except template tests) | `template/backend/pyproject.toml.jinja`, backend tests | **Template-first** |
| LiteLLM | N/A | `template/backend/src/**/litellm_*.py.jinja`, config yaml | **Template-only** |
| Grafana/Prometheus/OTel | N/A | `template/infra/grafana/**`, `template/infra/prometheus/**`, `template/infra/otel/collector.yaml`, `template/compose*.yml.jinja` | **Template-only** |
| Matomo | Optional roadmap docs | Future template optional module under `template/infra/` | **Template module when enabled** |

This matrix is the source-of-truth for deciding whether to implement changes in
`root`, `template/`, or both during parity modernization work.

## Audit Scope

### Structural and governance

- Top-level folders/files
- `.github/` structure and agentic prompt surface
- `.claude/` rules and assistant governance
- Task runner, pre-commit, and documentation alignment

### Production-readiness dimensions

- Clean Architecture enforcement hooks/scripts
- Convention checks (status codes, module docstrings, no-Final rules)
- CI-oriented validation coverage
- Configuration hygiene and naming consistency

## Findings Summary

### Strong existing alignment

- Modern tooling baseline present (`uv`, Taskfile, pre-commit, commitizen)
- Clean Architecture enforcement scripts already present
- Template includes rich generated-project scaffolding (`template/`)
- Docs and governance are already extensive

### Gaps addressed in this change

1. **No executable parity audit command** against `koda_automation`
   - Added `scripts/audit_koda_alignment.py`
   - Added `task audit:koda-alignment`

2. **Missing root prompt-library presence** (`.github/prompts/`)
   - Added `.github/prompts/README.md` to establish parity surface in root repo

3. **Missing cognitive-load governance rule in Claude rulesets**
   - Added `.claude/rules/cognitive-load.md`
   - Added `template/.claude/rules/cognitive-load.md`

4. **Docs not explicitly reflecting parity audit command**
   - Updated `README.md`
   - Updated `CLAUDE.md`
   - Updated `.claude/README.md`

## New Audit Script Behavior

`scripts/audit_koda_alignment.py` performs:

- Mandatory artifact checks in repo root
- Mandatory artifact checks in `template/`
- Agentic setup checks:
  - `.github/prompts` exists in root and template
  - `cognitive-load` rule exists in root and template Claude rules
- Informational structural deltas (root-only vs reference-only entries)

Exit code:

- `0`: mandatory checks pass
- `1`: mandatory checks fail

## Why this is state-of-the-art for this repo type

- Enforces parity with a real production reference repo while respecting template semantics
- Converts one-time manual review into repeatable policy-as-code
- Strengthens multi-agent governance consistency (root + template)
- Keeps quality gates discoverable via task runner and docs

## Follow-up Recommendations (Next Iteration)

1. Expand parity script to compare selected subtrees
   (`.claude/agents`, `.github/instructions`, `.github/prompts`) by filename
   sets.
2. Add optional JSON snapshot diffing for versioned governance baselines.
3. Add CI job to run `task audit:koda-alignment` in environments where
   reference path is available.
4. Add template prompt files mirroring key OPSX prompt names from reference repo.

## Phase-2 Implementation Snapshot (Current Session)

### Clean-architecture enforcement for CrewAI orchestration

- Added protocol ports in
   `template/backend/src/{{ project_slug }}/core/interfaces/crewai.py`:
   - `CrewOrchestrationSupervisor`
   - `CrewFlowRegistry`
- Updated
   `template/backend/src/{{ project_slug }}/application/services/{% if use_crewai %}crewai_service.py{% endif %}.jinja`
   to depend on these ports instead of concrete adapter imports for orchestration
   dependencies.

### CrewAI API route hardening

- Rebuilt
   `template/backend/src/{{ project_slug }}/presentation/api/routes/{% if use_crewai %}crewai.py{% endif %}.jinja`
   with valid formatting/structure and explicit request models.

### HMAS observability baseline expansion

- Updated
   `template/backend/src/{{ project_slug }}/{% if use_ai %}ai{% endif %}/{% if use_crewai %}crewai{% endif %}/hmas.py.jinja`
   with optional Prometheus metrics:
   - `hmas_orchestrations_total{status=...}`
   - `hmas_subgoals_total{state=...}`
   - `hmas_orchestration_duration_seconds`
- Fixed LLM protocol usage in HMAS planning/aggregation to call
   `complete(prompt=...)` with keyword arguments (protocol-compliant).

### LiteLLM router hardening

- Extended
   `template/backend/src/{{ project_slug }}/{% if use_ai %}ai{% endif %}/llm/litellm_router.py.jinja`
   to support advanced reliability settings from YAML:
   - `retry_after`
   - `default_max_parallel_requests`
   - `enable_pre_call_checks`
   - `enable_weighted_failover`
- Updated
   `template/backend/config/{% if use_ai %}litellm_router.yaml{% endif %}.jinja`
   with default values for these controls to improve production routing behavior.

### Local environment bootstrap for AI/provider scaffolding

- Added root `.env` placeholder file to make required local variables explicit for
   LiteLLM/provider orchestration and tracing setup.

### Local integration and analytics scaffolding

- Expanded template backend development dependencies in
   `template/backend/pyproject.toml.jinja` with:
   - `testcontainers` (generic, and postgres extra when DB backend is PostgreSQL)
   - `duckdb`
- Added `test:duckdb:smoke` task in `template/tasks/backend.yml.jinja` for quick
   local validation of DuckDB-based workflows.

### Azure container deployment guidance alignment

- Incorporated Azure ACR/App Service and Bicep best-practice references during
   implementation planning, including:
   - network-close registry placement and geo-replication strategy for ACR
   - App Service custom-container flow (build/push/deploy/restart)
   - Bicep naming, parameter, and symbolic-reference recommendations

## Validation Commands

- `task audit:koda-alignment`
- `task verify-all`
- `uvx pre-commit run --all-files`
