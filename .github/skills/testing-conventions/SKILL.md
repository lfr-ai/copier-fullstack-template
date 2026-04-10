# Testing Conventions Skill

## Test Structure

```text
tests/
└── unit/
    ├── conftest.py          # Shared fixtures
    ├── test_services.py     # Service layer tests
    ├── test_models.py       # Model handler tests
    └── test_utils.py        # Utility function tests
```

### Source → Test Mapping

| Source | Test |
|--------|------|
| `backend/src/claim_handler/application/orchestrator.py` | `tests/unit/test_orchestrator.py` |
| `backend/src/claim_handler/ai/handlers/gpt.py` | `tests/unit/test_gpt_handler.py` |
| `backend/src/claim_handler/utils/validators.py` | `tests/unit/test_validators.py` |
| `backend/src/claim_handler/core/pydantic_models.py` | `tests/unit/test_pydantic_models.py` |

## Naming Conventions

| Element | Pattern | Example |
|---------|---------|---------|
| Test file | `test_{module}.py` | `test_orchestrator.py` |
| Test class | `Test{ClassName}` | `TestOrchestrator` |
| Test method | `test_{method}_{scenario}` | `test_process_claim_empty_input` |
| Fixture | `{noun}_fixture` or `sample_{noun}` | `sample_claim` |

## Test Template

```python
"""Tests for {module_name}."""

import pytest
from hypothesis import given, strategies as st

from claim_handler.{path} import {Symbol}


class TestSymbol:
    """Tests for Symbol."""

    def test_method_happy_path(self) -> None:
        """Method returns expected result for valid input."""
        # Arrange
        input_data = ...

        # Act
        result = Symbol().method(input_data)

        # Assert
        assert result == expected

    def test_method_empty_input(self) -> None:
        """Method handles empty input gracefully."""
        with pytest.raises(ValueError, match="cannot be empty"):
            Symbol().method("")

    @pytest.mark.parametrize(
        "input_val, expected",
        [
            (1, "one"),
            (2, "two"),
            (3, "three"),
        ],
    )
    def test_method_parametrized(
        self, input_val: int, expected: str
    ) -> None:
        """Method maps input to correct output."""
        assert Symbol().method(input_val) == expected

    @given(st.integers(min_value=0, max_value=100))
    def test_method_property(self, value: int) -> None:
        """Method output is always non-negative."""
        result = Symbol().method(value)
        assert result >= 0
```

## Fixture Patterns

### Factory Fixtures (preferred)

```python
@pytest.fixture
def claim_factory():
    """Create test claims with sensible defaults."""
    def _factory(**overrides) -> dict[str, object]:
        defaults = {
            "id": 1,
            "diagnosis": "Test diagnosis",
            "status": "pending",
        }
        return {**defaults, **overrides}
    return _factory
```

### Shared Fixtures in conftest.py

```python
# tests/unit/conftest.py

@pytest.fixture
def sample_claim() -> dict[str, object]:
    """Minimal valid claim for testing."""
    return {"id": 1, "diagnosis": "Test"}
```

## Rules

- All test functions MUST have `-> None` return type
- Use `pytest.raises(ExcType, match="pattern")` — always include `match`
- Use `pytest.mark.parametrize` for data-driven tests
- Use `monkeypatch` for environment variables (never `os.environ` directly)
- Use `tmp_path` for filesystem tests
- Mark slow tests: `@pytest.mark.slow`
- Never test private methods (underscore-prefixed)
- Never use `time.sleep()` in tests
- Never hardcode field names — use registry constants
- Never use mutable defaults in fixtures

## Anti-Patterns

| Anti-Pattern | Correct Pattern |
|-------------|----------------|
| Testing private methods | Test through public API |
| `time.sleep()` in tests | Use `pytest-timeout` or mocks |
| Shared mutable state | Factory fixtures |
| `assert True` / `assert not False` | Assert specific values |
| Exact float comparison | `pytest.approx()` |
| Ignoring test warnings | Fix root cause |
