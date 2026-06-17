# Reference Alignment and Production-Readiness Deep-Dive

## Purpose

This document captures an exhaustive alignment audit between:

- `copier-fullstack-template` (this repository)
- `reference_automation` (reference implementation)

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

1. **No executable parity audit command** against `reference_automation`
   - Added `scripts/audit_reference_alignment.py`
   - Added `task audit:reference-alignment`

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

`scripts/audit_reference_alignment.py` performs:

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
3. Add CI job to run `task audit:reference-alignment` in environments where
   reference path is available.
4. Add template prompt files mirroring key OPSX prompt names from reference repo.

## Validation Commands

- `task audit:reference-alignment`
- `task verify-all`
- `uvx pre-commit run --all-files`
