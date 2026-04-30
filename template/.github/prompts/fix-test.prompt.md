---
description: 'Fix a failing test by analyzing the error, understanding root cause, and implementing the fix'
name: 'fix-test'
argument-hint: 'Test name or error message (e.g., test_create_user_raises_on_duplicate)'
agent: 'agent'
model: 'Claude Sonnet 4'
tools:
  [
    search/codebase,
    search/fileSearch,
    search/textSearch,
    search/usages,
    read/readFile,
    read/problems,
    edit/editFiles,
    execute/runInTerminal,
    execute/getTerminalOutput,
  ]
---

# Fix Failing Test

Diagnose and fix the failing test.

## Process

1. **Reproduce** — Run the specific failing test to see the error
2. **Analyze** — Read the full traceback and understand what's expected vs. actual
3. **Investigate** — Trace the code path from test → implementation
4. **Determine root cause** — Is it:
   - A bug in the implementation? → Fix the implementation
   - An outdated test after refactoring? → Update the test
   - A missing dependency/fixture? → Add it
   - A race condition? → Add proper synchronization
5. **Fix** — Apply the minimal change that resolves the issue
6. **Verify** — Re-run the test AND the full suite to check for regressions

## Important

- NEVER skip or disable a test to make the suite pass
- If the test is wrong (e.g., testing outdated behavior), explain WHY before changing it
- If the fix requires architectural changes, flag it for discussion

## Verification

```bash
cd backend && uv run pytest {test_path} -v --tb=long
task test
```
