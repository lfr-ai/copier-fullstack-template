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

- `task verify-all` passes:
  - architecture boundaries
  - no `Final[]` misuse
  - FastAPI status constants convention
  - module docstrings
  - `.github` alignment checks
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
- [ ] Add concise rationale comments only where explicit non-defaults are kept.
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
- [ ] Evaluate whether high-complexity toggles should move to advanced profile
      docs vs default interactive prompts.
- [ ] Ensure conditional questions rely on documented Copier `when` behavior and
      avoid duplicated validation logic.
- [x] Validate with render smoke test and generated project sanity checks.

Pass 3 completion notes (in progress):

- Removed dead `frontend_framework` copier question (`when: false`, unused by
      template files).
- Validated generated output with both minimal and feature-rich render scenarios.

### Pass 4 — architecture and boundary consistency

- [x] Keep backend clean architecture rules explicit and minimal:
  - validate `scripts/check-architecture-boundaries.py` for edge cases
  - confirm dependency direction policy remains framework-agnostic
- [ ] Document any intentional exceptions in a short policy section.
- [ ] Ensure root and template instruction parity for architecture guidance.

Pass 4 completion notes (in progress):

- Verified architecture boundaries pass after conditionalization and config cleanup.
- Fixed a latent template bug in settings validation (`auth_enabled` reference
      removed; auth validation now environment-driven).
- Made observability bootstrap conditional (`use_observability`) to avoid runtime
      import failures when observability is disabled.

### Pass 5 — root/template drift prevention

- [ ] Add or extend drift checks for critical mirrored assets:
  - `.github/instructions/*`
  - `.github/skills/*`
  - `.claude/rules/*`
- [ ] Add a machine-readable ownership matrix for root-only, template-only, and
      mirrored files.
- [ ] Wire drift checks into CI/pre-push path where cost is acceptable.

Pass 5 candidate alignment backlog:

- [ ] Normalize Lychee hook version/id across root and template pre-commit
      configs, or document intentional divergence.
- [ ] Normalize GitHub Action major versions between root and template
      workflows, or document intentional divergence.
- [x] Decide if Hadolint `DL3059` ignore should be root+template or
      template-only policy.
- [ ] Define canonical markdownlint scope/rule baseline for root vs template.
- [ ] Define canonical core MCP server set and document optional server deltas.

Pass 5 completion notes (in progress):

- Hadolint `DL3059` remains template-only by design (generated project
      Dockerfiles have multi-tool install readability tradeoffs; root does not).
- `.github` drift checks continue to pass via existing validation scripts.

### Pass 6 — docs coherence and operational simplicity

- [ ] Normalize command examples to one canonical path per workflow.
- [ ] Remove contradictory wording around prerequisites and install flow.
- [ ] Ensure all code/config changes are reflected in docs in the same PR.

### Pass 7 — GitNexus alignment enforcement (dependency)

- [ ] Ensure this repo is indexed in GitNexus for this environment.
- [ ] Add a short runbook for graph checks (query/impact usage and expected
      outputs).
- [ ] Add graph-backed consistency checks to pre-merge review process where
      feasible.

Pass 7 status note:

- GitNexus MCP is reachable, but this workspace is not in the active index for
  this session (available repos are different). Keep local validation as source
  of truth until indexing is corrected.

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

## Verification checklist (required per pass)

- [x] `task verify-all` passes.
- [x] Documentation updated for all behavior/config changes.
- [x] No new architecture-boundary violations introduced.
- [x] No accidental root/template coupling regressions introduced.

## Definition of done for this initiative

- [x] Config and setup are default-first and free of obvious redundancy.
- [x] Golden audits are stable (no noisy false positives).
- [ ] Clean architecture checks are enforced and documented.
- [ ] Root/template alignment is automated for critical governance assets.
- [x] Documentation is coherent, minimal, and current.
