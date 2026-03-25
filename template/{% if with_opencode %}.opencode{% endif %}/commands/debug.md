---
description: Debug an issue using systematic 4-phase methodology
agent: debug
---

Debug the following issue using the systematic 4-phase methodology:

$ARGUMENTS

Execute this workflow:

1. **Reproduce** — Confirm the issue exists with a minimal reproduction
2. **Hypothesize** — Form 2–3 ranked hypotheses for the root cause
3. **Investigate** — Examine code, recent changes, and test each hypothesis
4. **Fix and Verify** — Implement the minimal fix, run all tests, check linting

Useful diagnostic commands:

```bash
git log --oneline -20          # Recent changes
git diff HEAD~5                # Recent diffs
task test:unit -- -x -v        # Stop on first failure
ruff check .                   # Lint check
mypy backend/src/              # Type check
```

Document the root cause and fix clearly for future reference.
