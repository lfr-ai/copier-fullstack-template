# Comprehensive Cleanup & Simplification TODO (Exhaustive)

> **See also:** [PONYTAIL-AUDIT.md](./PONYTAIL-AUDIT.md) — ponytail over-engineering
> audit with YAGNI/KISS/DRY/SRP findings and completed simplifications.

## Scope

This is the authoritative implementation backlog for making this template
codebase simpler, more default-driven, architecture-safe, and consistently
aligned across root and `template/` assets.

It is intentionally execution-oriented and split into iterative passes so each
pass is measurable and verifiable.

## Baseline findings (current cycle)

### Verified

- `task verify-all` passes (architecture boundaries, no `Final[]` misuse,
  FastAPI status constants convention, module docstrings, and agentic
  alignment checks).
- Root and template structure are broadly coherent for current governance model.

### Gaps / opportunities

- `.pre-commit-config.yaml` had duplicate `pre-commit-hooks` repository blocks
  that can be safely consolidated.
- Existing modernization TODO included useful breadth but mixed status semantics
  and lacked explicit pass-based completion criteria.
- GitNexus index in this environment did not previously target this workspace,
      so graph-level enforcement must be tracked as a dependency (not silently
      assumed).

## Iteration status

### Pass 1 — completed in this change set

- [x] Consolidate duplicate `pre-commit-hooks` repo blocks in
      `.pre-commit-config.yaml`.
- [x] Keep functionality equivalent by moving `check-vcs-permalinks` into the
      main `pre-commit-hooks` block.
- [x] Refresh this TODO document into an executable, pass-based, exhaustive plan.

## Remaining exhaustive backlog

### Pass 2 — config simplification and default-first cleanup

- [x] Audit all root config files for explicit values equal to tool defaults:
  - `.pre-commit-config.yaml`
  - `.markdownlint-cli2.yaml`
  - `.yamllint.yaml`
  - `jscpd.json`
  - `ruff.toml`
  - `ty.toml`
- [x] Remove or collapse redundant ignore patterns while preserving behavior.
- [x] Add concise rationale comments only where explicit non-defaults are kept.
- [x] Re-run `task verify-all`.

Pass 2 completion notes:

- Removed non-standard EditorConfig `max_line_length` to keep line-length
      ownership in Ruff/markdownlint only.
- Removed redundant Ruff formatter `line-ending` default override.
- Removed explicit markdownlint defaults (`MD041: true`, `default: true`).
- Removed duplicate markdownlint ignore globs in template config.
- Removed typos locale override to rely on tool default locale.
- Removed empty typos `[default]` table (no-op metadata).
- Removed non-matching cspell ignore glob for `.lycheecache/**`.
- Removed redundant cspell override-level `language: en` entries inherited from
      global config.
- Removed root cspell top-level `language: en` override to use default locale.
- Removed default `check-added-large-files --maxkb=500` argument from
      pre-commit config.
- Applied matching simplifications to template counterparts:
      - removed redundant cspell override `language: en`
      - removed typos default locale/empty table
      - removed non-standard EditorConfig `max_line_length`
      - removed Ruff format defaults (`quote-style`, `indent-style`)
      - removed redundant Lychee `--no-progress` CLI arg (moved to config behavior)
      - removed no-op Biome `css` section and default formatter `lineEnding`
- Verified rendered outputs no longer include those removed defaults/no-op entries.

### Pass 3 — template questionnaire simplification (`copier.yml`)

- [x] Identify prompts whose defaults can be derived (avoid repeated manual
      input).
- [x] Evaluate whether high-complexity toggles should move to advanced profile
      docs vs default interactive prompts.
- [x] Ensure conditional questions rely on documented Copier `when` behavior and
      avoid duplicated validation logic.
- [x] Validate with render smoke test and generated project sanity checks.

Pass 3 completion notes (in progress):

- Removed dead `frontend_framework` copier question (`when: false`, unused by
      template files).
- Scoped `secret_backend` behind `cloud_provider == 'azure'` so non-Azure
      users are not prompted for irrelevant secret-backend choices.
- Retained nested AI toggles behind base feature gates (`use_ai`,
      `use_knowledge_graph`, cloud-specific checks) to keep advanced options
      discoverable without introducing a second prompt profile mode.
- Validated generated output with both minimal and feature-rich render scenarios.

### Pass 4 — architecture and boundary consistency

- [x] Keep backend clean architecture rules explicit and minimal:
  - validate `scripts/check-architecture-boundaries.py` for edge cases
  - confirm dependency direction policy remains framework-agnostic
- [x] Document any intentional exceptions in a short policy section.
- [x] Ensure root and template instruction parity for architecture guidance.

Pass 4 completion notes (in progress):

- Verified architecture boundaries pass after conditionalization and config cleanup.
- Fixed a latent template bug in settings validation (`auth_enabled` reference
      removed; auth validation now environment-driven).
- Made observability bootstrap conditional (`use_observability`) to avoid runtime
      import failures when observability is disabled.

### Pass 5 — root/template drift prevention

- [x] Add or extend drift checks for critical mirrored assets:
  - `.github/instructions/*`
  - `.github/skills/*`
  - `.claude/rules/*`
- [x] Add a machine-readable ownership matrix for root-only, template-only, and
      mirrored files.
- [x] Wire drift checks into CI/pre-push path where cost is acceptable.

Pass 5 candidate alignment backlog:

- [x] Normalize Lychee hook version/id across root and template pre-commit
      configs, or document intentional divergence.
- [x] Normalize GitHub Action major versions between root and template
      workflows, or document intentional divergence.
- [x] Decide if Hadolint `DL3059` ignore should be root+template or
      template-only policy.
- [x] Define canonical markdownlint scope/rule baseline for root vs template.
- [x] Define canonical core MCP server set and document optional server deltas.

Pass 5 completion notes (in progress):

- Hadolint `DL3059` remains template-only by design (generated project
      Dockerfiles have multi-tool install readability tradeoffs; root does not).
- Lychee now uses aligned versioning (`lychee-v0.24.2`) across root/template;
      hook-id divergence is intentional (`lychee-docker` in root for deterministic
      template-authoring checks, `lychee` in template for generated-project
      contributor environments without Docker requirement).
- GitHub Actions major-version drift is now documented as intentional policy:
      root tracks newer template-authoring majors; template workflows remain on
      broader generated-project-compatible majors unless required otherwise.
- Canonical markdownlint + MCP baselines are now documented in
      `docs/cross-cuttings/README.md` with explicit optional server deltas.
- Added machine-readable mirror matrix:
      `docs/cross-cuttings/agentic-ownership-map.json`.
- `scripts/check-github-alignment.py` now validates critical mirror pairs
      for `.github/instructions`, `.github/skills`, and `.claude/rules` against
      that matrix.
- Drift checks run via existing `task verify-all` / pre-commit / CI pathways
      because alignment validation is already part of those gates.

### Pass 6 — docs coherence and operational simplicity

- [x] Normalize command examples to one canonical path per workflow.
- [x] Remove contradictory wording around prerequisites and install flow.
- [x] Ensure all code/config changes are reflected in docs in the same PR.

Pass 6 completion notes:

- Standardized root guidance around canonical template render verification via
      `task render` plus one fallback command pattern for unsupported platforms.
- Updated root docs (`README.md`, `CONTRIBUTING.md`, `AGENTS.md`, `CLAUDE.md`)
      to remove inconsistent destination-path examples.
- Synchronized implementation and documentation updates in the same pass for
      architecture, questionnaire, and dependency-helper changes.

### Pass 7 — GitNexus alignment enforcement (dependency)

- [x] Ensure this repo is indexed in GitNexus for this environment.
- [x] Add a short runbook for graph checks (query/impact usage and expected
      outputs).
- [x] Add graph-backed consistency checks to pre-merge review process where
      feasible.

Pass 7 status note:

- GitNexus now indexes both `copier-fullstack-template` and
      `copier-template-source` in this environment.
- `context`/`impact` and Cypher queries are available for graph-backed analysis.
- MCP `query` currently reports FTS warnings in this environment, so fallback is
      direct Cypher + context/impact until FTS behavior stabilizes.
- Added explicit pre-merge graph-check checklist to
      `docs/cross-cuttings/gitnexus-runbook.md` and treat it as required manual
      gate for governance/architecture touching PRs.

### Pass 8 — script suite simplification and consistency

- [x] Remove duplicated Python-file scanning logic across validation scripts.
- [x] Introduce one internal helper module (`scripts/_python_file_utils.py`) for:
      - Python/Jinja file discovery
      - UTF-8 text reads with ignored decode errors
- [x] Refactor checks to use shared helper:
      - `scripts/check-architecture-boundaries.py`
      - `scripts/check-fastapi-status-codes.py`
      - `scripts/check-module-docstrings.py`
      - `scripts/check-no-final.py`
- [x] Normalize script structure for consistency (`main()` entrypoint,
                  argument parsing, cohesive helper functions) in:
      - `scripts/check-no-final.py`
      - `scripts/copy-template-snapshot.py`
- [x] Re-run full quality gate (`task verify-all`).

Pass 8 completion notes:

- Shared logic eliminated repeated `rglob`/suffix checks and repeated
                  `read_text(..., errors='ignore')` calls.
- Script behavior remains unchanged; only implementation structure and
                  maintainability improved.
- All validation tasks pass after refactor.

### Pass 9 — backend utils ponytail cleanup

- [x] Identify dead/thin utility wrappers in backend template utils package.
- [x] Delete unused wrapper modules that only re-exposed stdlib behavior:
  - `template/backend/src/{{ project_slug }}/utils/crypto_utils.py`
  - `template/backend/src/{{ project_slug }}/utils/file_utils.py`
  - `template/backend/src/{{ project_slug }}/utils/json_utils.py`
- [x] Validate no references remained in template backend sources.
- [x] Re-run full quality gate (`task verify-all`).

Pass 9 completion notes:

- Reduced generated project surface area and maintenance burden by removing
      dead utility abstractions.
- Kept behavior unchanged for generated projects because no callers existed.

### Pass 10 — duplication-tooling hygiene

- [x] Run clone detection with `npx jscpd --config jscpd.json`.
- [x] Remove unsupported `jscpd.json` field (`skipBlocks`) to eliminate config
      warnings and keep checks deterministic.
- [x] Re-run clone detection to confirm warning removal.

Pass 10 completion notes:

- Remaining clone matches are predominantly intentional cross-tool/template
      mirrors (`.claude` ↔ `.github` ↔ `template/`) and should be handled via
      generated/synchronized source-of-truth strategy, not ad-hoc manual edits.

### Pass 11 — agent tool-permission alignment

- [x] Standardize `.claude/agents/*.md` tool access to a shared full-access set
      for all user-invocable agents.
- [x] Mirror same tool-access policy in `template/.claude/agents/*.md`.
- [x] Standardize tool lists in `template/.github/agents/*.agent.md` to the
      same comprehensive capability set.
- [x] Preserve centralized safety controls (hooks + runtime permission denies)
      instead of per-agent read-only overrides.

Pass 11 completion notes:

- Removed per-agent `disallowedTools` read-only constraints where present in
      Claude agent definitions.
- Kept hook guardrails and Git safety controls unchanged in hook/runtime policy.
- Updated governance docs to reflect broad tool enablement with central safety
      constraints.

### Pass 12 — quality-gate blocker closure

- [x] Fix `ty-check` diagnostics in `scripts/check-github-alignment.py`
      (`entries[0]` typing/narrowing issue).
- [x] Reduce xenon complexity to pass configured thresholds:
      - `scripts/check-github-alignment.py:main`
      - `scripts/check-architecture-boundaries.py:_is_violation`
- [x] Scope root Hadolint pre-commit hook to avoid false parser failures on
      Jinja Containerfile templates.
- [x] Resolve GraphQL auth architecture FIXME by removing presentation-layer
      direct import of infrastructure `JWTAdapter`.

Pass 12 completion notes:

- Added robust hook-entry type narrowing helper in
      `scripts/check-github-alignment.py` and consolidated failure rendering via
      a normalized message builder.
- Replaced branch-heavy `_is_violation` logic with a declarative
      `_ALLOWED_CROSS_LAYER_IMPORTS` map to lower cognitive load and complexity.
- Updated root Hadolint hook exclusion regex to skip Jinja and
      `*.containerignore` pseudo-container files.
- Introduced `TokenDecoder` core protocol and wired GraphQL auth token
      validation through DI (`GraphQLContext` → `Container.token_decoder()`),
      removing presentation→infrastructure coupling.
- Verified gates now pass for the remediated blockers:
      `ty-check`, `xenon`, and `task verify-all`.

### Pass 13 — project-agnostic agentic enforcement

- [x] Expand project-specific token scanning in
      `scripts/check-github-alignment.py` beyond `.github/*` to include all
      agentic surfaces:
      - `.agents/*`
      - `.claude/{agents,commands,skills}/*`
      - `.github/{agents,instructions,prompts,skills}/*`
      - template equivalents under `template/.agents/`, `template/.claude/`,
        and `template/.github/`
- [x] Extend token policy to detect both repository slug and local workstation
      path leaks (cross-platform path forms).
- [x] Update governance documentation to codify project-agnostic agentic
      alignment policy.

Pass 13 completion notes:

- Tightened alignment guardrails to prevent agentic assets from embedding
      repository-specific/workstation-specific strings.
- This directly enforces the requirement that agentic setup content remains
      project-agnostic.

### Pass 14 — ponytail low-risk DRY/KISS sweep

- [x] De-duplicate repeated Copier render command blocks in `Taskfile.yml`
      by centralizing shared Copier defaults into `COPIER_COMMON_ARGS`.
- [x] Replace custom ignore reimplementation in
      `scripts/copy-template-snapshot.py` with stdlib-driven
      `shutil.ignore_patterns(...)` composition.
- [x] Reduce commit-policy drift by establishing one canonical source for
      commit convention details and aligning secondary rule docs.

Pass 14 completion notes:

- `render` and `test:rendered` now share the same core Copier argument set via
      `COPIER_COMMON_ARGS`, reducing duplication and drift.
- Snapshot ignore logic is now simpler and more explicit while preserving
      full-directory exclusion behavior.
- Commit conventions are still documented in multiple places for tool
      ergonomics, but detailed type/scope policy now points to one canonical
      instruction file.

### Pass 15 — deep ponytail + GitNexus simplification hardening

- [x] Run graph-assisted hotspot/impact review in GitNexus for script-heavy
      governance flows (focus: `scripts/check-github-alignment.py`).
- [x] Remove duplicate shell implementation of alignment checks:
      `scripts/check-github-alignment.sh`.
- [x] Make agentic project-token detection project-agnostic by deriving token
      checks from the current repository root path/name at runtime (no
      hardcoded workstation/repo strings).
- [x] DRY DI dependency helpers in
      `template/backend/src/{{ project_slug }}/presentation/api/dependencies.py.jinja`
      by reusing `_get_container(...)`.
- [x] Delete dead placeholder module:
      `template/backend/src/{{ project_slug }}/application/services/`
      `{% if use_rag %}rag_service.py{% endif %}.jinja`.
- [x] Expand ownership matrix coverage from instructions/skills/rules to all
      mirrored agentic surfaces (`agents`, `prompts`, hook scripts/configs).
- [x] Evaluate manifest-driven generation for root/template mirror assets to
      reduce drift maintenance.

Pass 15 completion notes:

- GitNexus impact analysis shows alignment-check refactors are low blast-radius
      and isolated to the script execution flow.
- Project-agnostic guardrails are now path/name derived from the active repo,
      removing environment-specific tokens from enforcement logic.
- Cleanup reduced dead-code surface and kept behavior unchanged for generated
      projects.
- Extended ownership-map drift enforcement to additional mirrored surfaces:
      `.claude/agents`, `.claude/commands`, `.github/prompts` (shared subset),
      and `.github/hooks` scripts/config.
- Moved required/legacy/scan-path policy into
      `docs/cross-cuttings/agentic-ownership-map.json` so
      `scripts/check-github-alignment.py` no longer duplicates those lists.
- Evaluated manifest-driven generation for mirrored governance assets and kept
      the current matrix-driven validation approach for now due tool-specific
      frontmatter/path semantics across `.github` and `.claude` surfaces.

### Pass 16 — exhaustive backlog from deep audit (next iterations)

Quick wins (low-risk):

- [x] Consolidate `scripts/check-github-alignment.py` hardcoded required/legacy
      lists into one machine-readable source (ownership/manifest) to remove
      duplicate policy definitions.
- [x] Replace placeholder integration tests (`assert True`) for unsupported
      backend branches with explicit skip semantics or conditional file
      generation.
- [x] Evaluate whether prompt manager compatibility alias can be narrowed to
      explicit legacy paths only (reduce API surface).

Medium:

- [x] Expand ownership-matrix parity checks to cover additional agentic mirrors:
      `.claude/agents`, `.claude/commands`, `.github/prompts`,
      `.github/hooks/scripts`, and template counterparts.
- [x] Introduce one canonical source for repeated instruction/rule prose where
      tool compatibility allows generated wrappers.
- [x] Reduce duplicated OpenSpec guidance across prompts/commands/skills with a
      source-of-truth projection pattern.

Risky / coordination-heavy:

- [x] Evaluate manifest-driven generation of root/template governance assets
      (agents/instructions/skills/prompts/hooks) to minimize manual drift.
- [x] Tighten architecture-boundary exception policy around `ai` ↔
      `infrastructure` allowances with explicit rationale and tests.
- [x] Standardize mirror-policy schema (`requiredInRoot`,
      `requiredInTemplate`, `optional`) for explicit ownership semantics.

Pass 16 progress notes:

- Replaced non-informative integration placeholders (`assert True`) with
      explicit `pytest.skip(...)` semantics in unsupported backend branches:
      Alembic, database isolation, and milestone acceptance tests.
- Narrowed internal usage to canonical prompt API by moving general prompt tests
      and evaluator backtest tooling to `Jinja2PromptTemplate`; compatibility
      alias coverage remains isolated in `test_prompt_manager.py`.
- Standardized ownership-matrix mirror semantics with explicit per-mirror
      `requiredInRoot` / `requiredInTemplate` / `optional` fields and
      corresponding checker validation.
- Tightened architecture policy by removing `ai -> infrastructure` imports from
      allowed cross-layer dependencies; adapter wiring now remains in
      `composition`, and the policy rationale is documented in quality-gate
      feature docs.
- Declared canonical-source precedence for mirrored instruction/rule prose in
      `.claude/rules/*` so GitHub instruction files remain the primary policy
      source when wording diverges.
- Confirmed OpenSpec guidance already follows a projection pattern where
      generated/aliased wrappers (`template/.github/prompts/openspec/*`,
      mirrored OpenSpec skills) are sourced from canonical workflow artifacts,
      reducing manual divergence points.
- Evaluated full manifest-driven generation for all governance surfaces and
      kept matrix-driven validation as the operational default for now because
      tool-specific frontmatter and path semantics still require curated files.

## Verification checklist (required per pass)

- [x] `task verify-all` passes.
- [x] Documentation updated for all behavior/config changes.
- [x] No new architecture-boundary violations introduced.
- [x] No accidental root/template coupling regressions introduced.

## Definition of done for this initiative

- [x] Config and setup are default-first and free of obvious redundancy.
- [x] Golden audits are stable (no noisy false positives).
- [x] Clean architecture checks are enforced and documented.
- [x] Root/template alignment is automated for critical governance assets.
- [x] Documentation is coherent, minimal, and current.
