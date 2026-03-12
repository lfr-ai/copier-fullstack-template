---
description: Generate comprehensive tests for specified code
agent: tester
subtask: true
---

Generate comprehensive tests for:

$ARGUMENTS

Follow the project testing conventions:

1. **Unit tests** in `backend/tests/unit/` with `@pytest.mark.unit`
2. **Integration tests** in `backend/tests/integration/` with `@pytest.mark.integration`
3. **Property tests** in `backend/tests/property/` with `@pytest.mark.property` using Hypothesis
4. **Frontend tests** in `frontend/tests/unit/` using Vitest

For each function/class, cover:

- Happy path (normal expected behavior)
- Edge cases (empty inputs, boundaries, None)
- Error paths (invalid inputs, exceptions)
- Property invariants (for domain entities)

Use factories from `tests/factories/` for test data. Run all tests and report results with
coverage.
