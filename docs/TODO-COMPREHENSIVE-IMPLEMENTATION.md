# Comprehensive Modernization TODO (Exhaustive)

## Scope and intent

This document is the exhaustive, implementation-oriented modernization backlog for
this template repository, aligned with a frontend-first target profile while
preserving optional fullstack capabilities.

It combines:

- Repo audit findings in this workspace
- Golden-reference alignment analysis against `reference_automation`
- Current upstream guidance from Storybook, Playwright, LiteLLM, LangChain,
  CrewAI, OpenTelemetry, Prometheus, Grafana, and SQLite documentation

## Current baseline snapshot

### Already in good shape

- Strong template-first repository structure with `template/` as source of truth
- Existing MCP setup for `playwright`, `gitnexus`, `context7`, and `shadcn`
- Existing frontend template support including Storybook and Playwright
- Existing observability scaffolding in `template/infra` (Prometheus/Grafana/OTel)
- Existing OpenSpec and GitNexus assets and prompt/skill coverage

### Critical or high-priority deltas resolved in this cycle

- `.gitignore` conflict fixed for `.vscode` tracking behavior
- Copilot hook command paths normalized in:
  - `.github/hooks/tool-guardian.json`
  - `.github/hooks/dependency-license-checker.json`
- Duplicate `commitizen` block removed from `.pre-commit-config.yaml`
- Prompt docs made more project-agnostic in `.github/prompts/README.md`
- Root policy readmes improved with direct template path pointers:
  - `docker/README.md`
  - `azure/README.md`
  - `caddy/README.md`
- Frontend agentic coverage expanded in root repo:
  - `.github/agents/frontend-react.agent.md`
  - `.github/instructions/frontend.instructions.md`
  - `.github/skills/frontend-react-stack/SKILL.md`
- Copilot skills table updated with frontend-relevant skills in
  `.github/copilot-instructions.md`

## Exhaustive implementation backlog

## 1) Agentic setup modernization (project-agnostic + frontend-first)

- [ ] Ensure all root agent descriptions avoid repository-name coupling and prefer
      role-based, reusable wording.
- [ ] Add root-level cross-reference map for agents/skills/instructions to clarify
      what belongs to root template-authoring vs generated-project output.
- [ ] Add explicit Storybook AI-manifest guidance to root instructions:
      - write focused stories
      - add JSDoc summaries/descriptions
      - curate manifest with `!manifest` for instructional stories
- [ ] Add explicit Playwright selector priority guidance in root instructions and
      keep it consistent with skill docs.
- [ ] Add frontend UX/accessibility handoff guidance among `frontend-react`,
      `testing`, and `debug` agents.

## 2) OpenSpec + GitNexus parity and hygiene

- [ ] Validate prompt and command parity between root and template for OpenSpec and
      GitNexus workflows.
- [ ] Add a single “source-of-truth” table documenting where each OpenSpec/GitNexus
      asset is maintained (root, template, or both).
- [ ] Add CI checks that detect stale root/template drift for key agentic files.

## 3) Storybook + Playwright + shadcn production quality

- [ ] Add a dedicated “frontend agentic best practices” doc under `docs/frontend/`
      covering:
      - Storybook manifests/debug routes
      - story quality rules
      - play functions and interaction testing
      - Playwright CI strategy
- [ ] Add a task or CI step that verifies Storybook builds for template frontend
      when Storybook is enabled.
- [ ] Add Storybook AI resource links and MCP guidance into template docs.
- [ ] Add a visual regression strategy placeholder (Chromatic or equivalent)
      documented as optional.
- [ ] Keep favicon setup validated in frontend template:
      - confirm `template/frontend/public/favicon.svg`
      - confirm link in `template/frontend/index.html.jinja`

## 4) Docker / Azure / Caddy production-readiness alignment

- [ ] Add root policy doc explaining why runtime assets are template-scoped and
      root folders contain policy pointers only.
- [ ] Add checklist to validate generated runtime outputs for docker/azure/caddy
      after template changes.
- [ ] Add Azure deployment hardening checklist for generated projects:
      identity, secrets handling, health checks, staged deployment, rollback.
- [ ] Add Caddy production checklist for generated projects:
      TLS, headers, upstream health, compression, observability hooks.

## 5) Tooling + config/meta hygiene

- [ ] Resolve Codecov template duplication (`template/.codecov.yml.jinja` vs
      `template/codecov.yml.jinja`) by consolidating on one canonical file and
      documenting policy.
- [ ] Add a CI safeguard that fails when duplicate tooling configs exist in
      template root.
- [ ] Re-audit `.gitignore` regularly to ensure `.secrets.baseline` remains
      tracked and not accidentally ignored.
- [ ] Add repo script/check that validates hook command paths and existing files.

## 6) Frontend structure and naming enforcement

- [ ] Add explicit frontend naming conventions doc section for files, folders,
      exports, and state/query hooks.
- [ ] Add template lint rule recommendations for import boundaries between
      frontend layers.
- [ ] Add architecture verification script extension for frontend layer boundaries
      (mirroring backend boundary checks conceptually).

## 7) LiteLLM + LangChain (scaffold plan only, frontend-first compatibility)

- [ ] Define a project-agnostic scaffold contract (document only in this repo):
      - gateway interface for model routing
      - provider-neutral model aliasing
      - optional LiteLLM Router/Proxy mode
- [ ] Define required config schema for model groups, fallback, retry, and
      timeout.
- [ ] Define observability contract for request cost, model/provider labels,
      latency, and cache-hit metrics.
- [ ] Add a staged implementation plan that keeps this template frontend-first by
      making AI backend features fully optional.

## 8) CrewAI HMAS (scaffold/migration plan)

- [ ] Create architecture decision doc comparing:
      - LangGraph orchestration
      - CrewAI crew/flow orchestration
      - hybrid delegation model
- [ ] Define mandatory safety requirements for HMAS:
      deterministic fallbacks, bounded retries, cancellation, timeout envelopes,
      structured telemetry, and audit logs.
- [ ] Define phased migration strategy with feature flags and side-by-side
      execution paths.

## 9) Database strategy plan (SQLite local, PostgreSQL dev/prod)

- [ ] Produce migration runbook for local PostgreSQL data export/import to SQLite
      for local-only mode.
- [ ] Define strict environment matrix:
      - local: SQLite
      - dev server/staging/prod: PostgreSQL
- [ ] Define compatibility checklist (migrations, constraints, datetime/JSON,
      test fixtures).
- [ ] Add rollback and verification steps for local migration.

## 10) Observability plan (OTel + Prometheus + Grafana)

- [ ] Add frontend-focused observability blueprint:
      web vitals, route timings, API latency, error rates, user journey metrics.
- [ ] Add collector security checklist based on OTel guidance:
      localhost binding/default host policy, minimal components, redaction,
      queue/memory limits, auth/TLS.
- [ ] Add Prometheus metric naming checklist (units, suffixes, cardinality
      control, counter/gauge correctness).
- [ ] Add Grafana dashboard curation checklist for frontend and orchestrator
      metrics.

## 11) RAG architecture research backlog (document-only in this repo)

- [ ] Define strict retrieval scope policy for case-handler-only data.
- [ ] Define pluggable evaluation harness for comparing DeepRAG, Self-CRAG,
      GraphRAG, and LightRAG.
- [ ] Define objective evaluation metric schema and storage format.
- [ ] Define boundaries so these remain optional modules and do not pollute
      frontend-only generated profiles.

## 12) CI/CD and dev-productivity enhancements

- [ ] Add optional Azure deployment pipeline blueprint for ACR + App Service with
      staged approvals.
- [ ] Validate CodeRabbit and Codecov end-to-end with template-generated output
      and document expected behavior.
- [ ] Validate Keploy workflow expectations and document recording/replay usage
      boundaries.
- [ ] Document optional testcontainers/duckdb usage patterns in generated projects.

## Verification checklist (for every modernization PR)

- [ ] Pre-commit passes
- [ ] Template render smoke test passes
- [ ] No root/template drift in critical agentic files
- [ ] Documentation updated with behavior/config changes
- [ ] No accidental project-specific coupling introduced
- [ ] `.secrets.baseline` remains tracked

## Notes

This repository is template-source infrastructure. Some requested items (runtime
framework rewiring, full data migration, CrewAI/LiteLLM production integrations)
are intentionally planned here as scaffolding and policy/backlog work, to be
applied in generated projects where runtime context exists.
