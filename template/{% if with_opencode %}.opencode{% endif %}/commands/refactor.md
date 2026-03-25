---
description: Refactor code to improve quality without changing behavior
agent: refactor
subtask: true
---

Refactor the following code, improving quality without changing external behavior:

$ARGUMENTS

Follow this protocol:

1. **Run tests first** — confirm they pass before any changes
2. **Identify** code smells, duplication, and convention violations
3. **Plan** the refactoring as safe, reversible steps
4. **Execute** each step, running tests after every change
5. **Verify** all tests pass and linting/typing are clean

Focus areas:

- Clean architecture compliance and Dependency Rule
- Type safety and missing annotations
- Duplication and code smell removal
- Naming convention alignment with registry
- `from __future__ import annotations` in every file
- Keyword-only arguments with `*` separator
- Application services using UoW repo properties (not concrete adapter imports)

Report what was changed and why for each step.
