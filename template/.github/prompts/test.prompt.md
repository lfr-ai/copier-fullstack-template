---
description: Test writing workflow for pytest, factory-boy, and property-based testing
name: test
argument-hint: 'Module path or description of what needs tests'
agent: ask
model: 'Claude Sonnet 4'
tools:
  [
    read/readFile,
    search/codebase,
    search/textSearch,
    search/usages,
    edit/editFiles,
    execute/runInTerminal,
    execute/getTerminalOutput,
  ]
---

# Write Tests

Write comprehensive tests for the specified module or feature.

## Test Location

Mirror source structure:
`backend/src/<slug>/application/services/order.py` → `tests/unit/test_order.py`

## Required Pytest Markers

ALL tests MUST be marked:

```python
@pytest.mark.unit           # Fast, no I/O
@pytest.mark.integration    # Database/API boundary
@pytest.mark.property       # Hypothesis property-based
```

## Factory-Boy for Test Data (MANDATORY)

```python
import factory
from factory.faker import Faker

class ItemFactory(factory.Factory):
    class Meta:
        model = Item
    id = factory.Sequence(lambda n: n)
    name = Faker("word")
    status = "pending"
```

## Test Template

```python
"""Tests for {module}."""
import pytest
from hypothesis import given, strategies as st

@pytest.mark.unit
def test_{method}_{scenario}_{expected}() -> None:
    """Behavior description."""
    # Arrange
    item = ItemFactory(status="pending")
    # Act
    result = subject.method(item)
    # Assert
    assert result.status == "approved"

@pytest.mark.unit
def test_{method}_raises_on_{condition}() -> None:
    with pytest.raises(ValueError, match="descriptive pattern"):
        subject.method(invalid_input)

@pytest.mark.property
@given(st.text(min_size=1))
def test_{method}_invariant(value: str) -> None:
    result = subject.method(value)
    assert result is not None  # invariant
```

## Coverage Gate

Run after writing tests:

```bash
uv run pytest tests/unit/ --cov --cov-fail-under=80 --cov-report=term-missing
```
