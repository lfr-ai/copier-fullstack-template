# Modernization implementation plan

## Strategy

Adopt an incremental migration strategy (not big-bang):

1. Improve generated-project tooling guardrails first.
2. Harden settings/runtime observability second.
3. Expand test and governance coverage third.

This minimizes blast radius and allows rollback at each phase.

## Phase breakdown

### Phase 1 — Tooling parity uplift (completed in this pass)

- Add deterministic dependency-audit scaffolding for generated projects.
- Wire dependency audit into pre-commit local hooks.
- Align task-level security audit command to same deterministic flow.

Risk: low.

Rollback:

- Remove hook entry from `template/.pre-commit-config.yaml.jinja`.
- Revert `template/Taskfile.yml.jinja` `security:audit` command.
- Delete `template/tools/security/dependency_audit.py.jinja`.

Acceptance criteria:

- Generated project contains `tools/security/dependency_audit.py`.
- `pre-commit run --all-files` includes dependency audit hook.
- `task security:audit` invokes the new script.

### Phase 2 — Runtime config observability (completed in this pass)

- Keep current precedence semantics for runtime environment selection.
- Add warning logs when invalid env values are encountered.

Risk: low.

Rollback:

- Revert warning-log additions in
  `template/backend/src/{{ project_slug }}/config/settings/runtime.py.jinja`.

Acceptance criteria:

- Valid values resolve exactly as before.
- Invalid values are ignored but produce warning logs.

### Phase 3 — Extended governance and regression safety (next)

- Add generated tests for runtime environment parsing edge cases.
- Add generated docs for config conventions and naming contracts.
- Evaluate whether to split large settings validators into helper modules for
  maintainability (without changing behavior).

Risk: medium (test and structure refactor may touch broad surface).

Rollback:

- Keep helper-module work behind phased commits.
- Revert per module if behavior changes.

Acceptance criteria:

- Regression tests cover invalid/empty env values, precedence, hostname mapping.
- Docs reflect authoritative configuration behavior and extension points.

## Feature parity mapping

- `koda_refactor` lock-aware dependency audit flow
  → `template/tools/security/dependency_audit.py.jinja` + hook/task wiring.
- `koda_refactor` explicit runtime environment hygiene
  → warning-based observability in template runtime resolver.

## Data migration plan

No schema/data migration required. This modernization pass affects scaffolding,
automation, and runtime config diagnostics only.

## Testing strategy

- Run focused diagnostics on modified files.
- Run repository pre-commit and render smoke test before release.
- For generated-project validation, render template and execute:
  - `pre-commit run --all-files`
  - `task security:audit`

## Deployment approach

Use staged rollout:

1. Merge template changes.
2. Render canary projects from template defaults.
3. Validate hooks/tasks in canary projects.
4. Roll out to broader template consumers.
