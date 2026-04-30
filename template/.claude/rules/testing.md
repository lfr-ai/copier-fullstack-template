---
paths:
  - "backend/tests/**/*.py"
---

# Testing Conventions

- Use pytest markers: `@pytest.mark.unit`, `@pytest.mark.integration`, `@pytest.mark.property`
- Name tests: `test_<action>_<condition>_<expected_result>`
- Group related tests in classes: `class TestServiceName:`
- Use factory-boy for test data (never hardcode fixtures)
- Use `pytest.raises` for exception testing with match patterns
- Use `respx` for mocking HTTP calls (not `unittest.mock.patch`)
- Use `freezegun` for time-dependent tests
- Use `hypothesis` for property-based testing
- Keep unit tests fast (<100ms each)
- Integration tests get their own database transaction (rollback after)
- Never mock the repository in integration tests — use real database
