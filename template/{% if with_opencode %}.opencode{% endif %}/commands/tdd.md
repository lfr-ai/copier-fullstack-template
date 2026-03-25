---
description: Drive development using Red-Green-Refactor TDD cycle
agent: tdd
---

Implement the following using strict Test-Driven Development:

$ARGUMENTS

For each requirement, execute this cycle:

1. **Red** — Write a minimal failing test that captures the requirement
2. **Green** — Write the simplest code that makes the test pass
3. **Refactor** — Improve code quality while keeping all tests green

Rules:

- One test at a time — never write multiple failing tests
- Minimal implementation — only enough to pass the current test
- Refactor only when all tests are green
- Run the full test suite after each cycle

Use project testing conventions:

- Backend: `backend/tests/unit/` with `@pytest.mark.unit`
- Frontend: `frontend/tests/unit/` with Vitest
- Run: `task test:unit` or `python -m pytest -x`
