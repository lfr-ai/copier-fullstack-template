---
description: Run all linters and fix auto-fixable issues
subtask: true
---

Run the full linting and formatting pipeline, fixing auto-fixable issues:

$ARGUMENTS

Execute these steps:

1. **Python formatting**: `ruff format backend/`
2. **Python linting**: `ruff check --fix backend/`
3. **Python type checking**: `mypy backend/src/`
4. **Frontend linting**: `pnpm --filter frontend lint --fix`
5. **Frontend formatting**: `pnpm --filter frontend format`

Report:

- Number of auto-fixed issues per tool
- Remaining issues that require manual intervention
- Any type errors that need attention
