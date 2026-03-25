```skill
---
name: testing-conventions
description: Guides test creation following project conventions — pytest markers, directory structure, factory patterns, property-based testing with Hypothesis, and coverage requirements
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: testing
  layer: fullstack
---

## What I do

- Guide creation of tests following project conventions
- Enforce correct directory structure and file naming
- Apply appropriate pytest markers
- Use factory_boy for test data generation
- Apply Hypothesis for property-based tests

## Test Directory Structure

```

backend/tests/ ├── conftest.py # Root-level shared fixtures ├── unit/ # Pure logic, no
I/O — mirrors src/ structure ├── integration/ # Tests with real DB / external services
├── property/ # Hypothesis property-based tests ├── performance/ # Benchmarks and
regression tests ├── factories/ # Factory classes for test data ├── fixtures/ # Shared
test data ├── mocks/ # Reusable mock objects └── utils/ # Assertion helpers

frontend/tests/ ├── setup.ts # Global test setup ├── unit/ # Vitest unit tests — mirrors
src/ └── e2e/ # Playwright end-to-end tests (optional)

````

## Pytest Markers

- `@pytest.mark.unit` — Pure logic, no I/O, fast
- `@pytest.mark.integration` — Real DB/cache/external services
- `@pytest.mark.property` — Hypothesis-based invariant testing
- `@pytest.mark.performance` — Benchmarks and regression tests
- `@pytest.mark.profiling` — CPU, memory, SQL profiling tests (see `tests/performance/test_profiling.py`)
- `@pytest.mark.slow` — Tests taking >5 seconds

## Test Patterns

### Unit Test Template
```python
from __future__ import annotations

import pytest
from tests.factories import MyEntityFactory

@pytest.mark.unit
class TestMyService:
    def test_happy_path(self) -> None:
        entity = MyEntityFactory.build()
        result = my_function(entity=entity)
        assert result is not None

    def test_edge_case_empty_input(self) -> None:
        with pytest.raises(ValueError, match="cannot be empty"):
            my_function(entity=None)
```

### Service Test Pattern (Clean Architecture)

Application services are tested by mocking the UoW protocol.
Never instantiate concrete adapters in unit tests:

```python
from __future__ import annotations
from unittest.mock import AsyncMock, MagicMock

import pytest

@pytest.mark.unit
async def test_create_user_service() -> None:
    mock_uow = MagicMock()
    mock_uow.__aenter__ = AsyncMock(return_value=mock_uow)
    mock_uow.__aexit__ = AsyncMock(return_value=None)
    mock_uow.users = MagicMock()
    mock_uow.users.add = AsyncMock(return_value=fake_user)
    mock_uow.commit = AsyncMock()

    service = UserService(uow=mock_uow)
    result = await service.create_user(dto=create_dto)
    mock_uow.users.add.assert_called_once()
````

### Property-Based Test Template

```python
from __future__ import annotations

import pytest
from hypothesis import given, strategies as st

@pytest.mark.property
def test_roundtrip_invariant(value: str) -> None:
    encoded = encode(value=value)
    decoded = decode(encoded=encoded)
    assert decoded == value
```

## Coverage Requirements

- ≥ 80% on `core` + `application` layers
- 100% on domain entities and value objects
- All error paths must have corresponding tests

## Task Commands

```bash
task test              # All tests
task test:unit         # Unit tests only
task test:integration  # Integration tests
task test:property     # Property-based tests
task test:coverage     # Tests with coverage report
```

## When to use me

Use this skill when:

- Creating new test files
- Reviewing test adequacy
- Setting up factory classes
- Writing property-based tests
- Checking coverage requirements

```

```
