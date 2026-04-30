---
description: 'Refactor code for improved quality without changing behavior — extract, rename, simplify'
name: 'refactor'
argument-hint: 'What to refactor and why (e.g., extract payment logic from OrderService)'
agent: 'agent'
model: 'Claude Sonnet 4'
tools:
  [
    search/codebase,
    search/fileSearch,
    search/textSearch,
    search/usages,
    search/changes,
    read/readFile,
    edit/editFiles,
    execute/runInTerminal,
    execute/getTerminalOutput,
  ]
---

# Refactor

Improve code structure and quality without changing external behavior.

## Process

1. **Understand** — Read existing code and its tests thoroughly
2. **Baseline** — Run tests to confirm they pass BEFORE refactoring
3. **Plan** — Identify specific improvements (extract, rename, simplify, move)
4. **Execute** — Apply changes incrementally, running tests after each step
5. **Verify** — Full test suite must pass with identical behavior

## Refactoring Techniques

- **Extract Method** — Pull complex logic into well-named functions
- **Extract Class** — Split a class doing too much into focused classes
- **Move** — Relocate code to the correct architectural layer
- **Rename** — Improve naming for clarity
- **Simplify Conditionals** — Replace nested if/else with guard clauses or polymorphism
- **Introduce Interface** — Add abstraction at layer boundaries
- **Remove Duplication** — Extract shared logic (but only after 3+ repetitions)

## Rules

- Tests must pass after EVERY intermediate step
- Do not change test assertions (behavior must be preserved)
- If tests need updating, the behavior changed — that's a feature, not a refactor
- Commit after each logical refactoring step with message: `refactor: {what}`

## Verification

```bash
task lint && task typecheck && task test
```
