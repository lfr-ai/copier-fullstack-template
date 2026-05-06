---
description: Systematic debugging workflow for errors, test failures, and unexpected behavior
name: debug
argument-hint: 'Error message, test name, or description of unexpected behavior'
agent: ask
model: 'Claude Sonnet 4'
tools:
  [
    execute/getTerminalOutput,
    execute/runInTerminal,
    read/problems,
    read/readFile,
    search/changes,
    search/codebase,
    search/textSearch,
    edit/editFiles,
  ]
---

# Debug

You are debugging an issue in this codebase. Follow this systematic process:

## Step 1 — Reproduce

Confirm the exact failure:

```bash
uv run pytest <test_file>::<test_name> -x -v --tb=long
```

Collect: full error message, stack trace, recent changes (`git diff HEAD~5`).

## Step 2 — Isolate

Find the failing code using grep and file reads. Determine which layer it's in
(core / application / infrastructure / presentation).

## Step 3 — Hypothesize

List 2-3 possible root causes ranked by likelihood. Common patterns:

- **Import errors** — Architecture boundary violations, circular imports
- **Async bugs** — Missing `await`, wrong event loop
- **SQLAlchemy** — Detached instances, missing eager loads
- **Type errors** — Pydantic validation failures, wrong DTO mapping

## Step 4 — Verify

Test ONE hypothesis at a time. Never change multiple things simultaneously.

## Step 5 — Fix

Implement the MINIMAL fix addressing root cause.

## Step 6 — Prevent

Write a regression test:

```python
@pytest.mark.unit
def test_<method>_<scenario>_<expected>() -> None:
    # The exact scenario that triggered the bug
    ...
```

Run `task test:unit` to confirm fix and no regressions.
