# Comprehensive Cleanup & Simplification TODO (Exhaustive)

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

- Removed editorconfig sections that only restated global `indent_size = 2`.
- Removed redundant Ruff formatter settings that matched defaults.
- Removed markdownlint `default: true` boilerplate.
- Simplified `.gitignore` by removing redundant duplicate patterns.

### Pass 3 — template questionnaire simplification (`copier.yml`)

- [ ] Identify prompts whose defaults can be derived (avoid repeated manual
      input).
- [ ] Evaluate whether high-complexity toggles should move to advanced profile
      docs vs default interactive prompts.
- [ ] Ensure conditional questions rely on documented Copier `when` behavior and
      avoid duplicated validation logic.
- [ ] Validate with render smoke test and generated project sanity checks.

### Pass 4 — architecture and boundary consistency

- [ ] Keep backend clean architecture rules explicit and minimal:
  - validate `scripts/check-architecture-boundaries.py` for edge cases
  - confirm dependency direction policy remains framework-agnostic
- [ ] Document any intentional exceptions in a short policy section.
- [ ] Ensure root and template instruction parity for architecture guidance.

### Pass 5 — root/template drift prevention

- [ ] Add or extend drift checks for critical mirrored assets:
  - `.github/instructions/*`
  - `.github/skills/*`
  - `.claude/rules/*`
- [ ] Add a machine-readable ownership matrix for root-only, template-only, and
      mirrored files.
- [ ] Wire drift checks into CI/pre-push path where cost is acceptable.

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

## Verification checklist (required per pass)

- [ ] `task verify-all` passes.
- [ ] Documentation updated for all behavior/config changes.
- [ ] No new architecture-boundary violations introduced.
- [ ] No accidental root/template coupling regressions introduced.

## Definition of done for this initiative

- [ ] Config and setup are default-first and free of obvious redundancy.
- [ ] Golden audits are stable (no noisy false positives).
- [ ] Clean architecture checks are enforced and documented.
- [ ] Root/template alignment is automated for critical governance assets.
- [ ] Documentation is coherent, minimal, and current.
