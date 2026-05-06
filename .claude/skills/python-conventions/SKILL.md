# Python Conventions Skill

## Type Hints

### Do

```python
# Builtin generics
items: list[str]
mapping: dict[str, int]
pair: tuple[str, int]
nullable: str | None

# Plain constants (no Final annotation)
MAX_RETRIES = 3

# @final for sealed classes/methods
from typing import final

@final
class ImmutableConfig: ...
```

### Do NOT

```python
# Never import generic aliases from typing
from typing import List, Dict, Tuple, Optional, Union

# Never use Any
from typing import Any
value: Any  # Use object instead
```

## Dataclasses

Always `frozen=True, slots=True`:

```python
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Config:
    host: str
    port: int
    timeout: float = 30.0
```

## Enums

Always `@unique`, use `StrEnum` or `IntEnum`:

```python
from enum import StrEnum, unique

@unique
class Status(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
```

## Logging

Use `structlog` for structured JSON logging with context binding:

```python
import structlog

logger = structlog.get_logger(__name__)

# Bind context for all subsequent log calls
logger = logger.bind(claim_id=claim_id, user_id=user_id)

logger.info("processing_claim")
logger.error("validation_failed", reason="missing_diagnosis")
logger.exception("unexpected_error", resource_id=resource_id)
```

Structured logging outputs JSON:

```json
{"event": "processing_claim", "claim_id": 123, "user_id": "abc", "timestamp": "2025-02-01T10:30:00Z"}
```

## Async SQLAlchemy

Use async session and query patterns:

```python
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import select

async def get_claim(session: AsyncSession, claim_id: int) -> Claim | None:
    """Retrieve claim by ID."""
    stmt = select(Claim).where(Claim.id == claim_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def create_claim(session: AsyncSession, claim_data: dict) -> Claim:
    """Create new claim."""
    claim = Claim(**claim_data)
    session.add(claim)
    await session.commit()
    await session.refresh(claim)
    return claim
```

## Exception Handling

Specific catches with chaining:

```python
try:
    result = process(data)
except ValidationError as e:
    logger.error("Validation failed for %s", data_id, exc_info=True)
    raise ProcessingError("Invalid data") from e
except DatabaseError as e:
    raise StorageError("Database operation failed") from e
```

## Function Signatures

Keyword-only args with `*` for 3+ params:

```python
def process_claim(
    claim_id: int,
    *,
    validate: bool = True,
    strict_mode: bool = False,
    timeout: float = 30.0,
) -> ClaimResult:
    """Process insurance claim with configurable validation."""
```

## Docstrings (Google Convention)

```python
def validate_cpr(cpr: str) -> bool:
    """Validate CPR number format and checksum.

    Args:
        cpr: Danish CPR number string.

    Returns:
        True if CPR is valid.

    Raises:
        ValueError: If CPR format is invalid.
    """
```

Rules:
- NEVER start sentences with articles ("a", "an", "the")
- Complete sentences with periods
- Short, concise — avoid redundancy

## Pydantic Models

```python
from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field

class ClaimModel(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    diagnosis: Annotated[
        str | None,
        Field(
            default=None,
            min_length=1,
            max_length=500,
            description="Primary medical diagnosis",
            examples=["Type 2 diabetes"],
        ),
    ]
```

## Naming Conventions

| Entity | Convention | Example |
|--------|-----------|---------|
| Files | snake_case | `my_module.py` |
| Classes | PascalCase | `ClaimProcessor` |
| Functions | snake_case | `process_claim` |
| Variables | snake_case | `claim_count` |
| Constants | UPPER_SNAKE_CASE | `MAX_RETRIES` |
| Private | `_` prefix | `_internal_state` |

Rule: Never use `Final[...]` for internal constants or variables.

## Caching

```python
from functools import lru_cache, cached_property

@lru_cache(maxsize=128)
def expensive_computation(key: int) -> str: ...

class Config:
    @cached_property
    def db_url(self) -> str: ...
```

## Retry Policies

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1.5, min=2, max=15),
    reraise=True,
)
def call_api() -> dict[str, object]: ...
```

## Package Management

Use `uv` for dependency management:

```bash
uv add httpx            # Add production dependency
uv add --group dev pytest  # Add dev dependency
uv sync                 # Install all dependencies
uv run pytest           # Run command in virtual environment
```
---
name: python-conventions
description: >
  Enforces project Python coding standards including type hints, structured logging,
  keyword-only args, and forbidden patterns. Use when writing or refactoring Python code.
---

# Skill: Python Conventions

## Purpose

Apply project Python standards consistently for readability, safety, and
maintainability.

## Use This Skill When

- Writing or refactoring Python code
- Adding public APIs, services, DTOs, mappers
- Fixing lint/type/documentation issues

## Rules

- Use Python {{ python_version }}+ features and full type hints
- 'from __future__ import annotations' ONLY in files with TYPE_CHECKING blocks or forward references
- Use keyword-only args ('*') for multi-parameter constructors/functions
- Use structured logging, not 'print()'
- Avoid 'Any'; prefer precise types or 'object'
- Keep line length <= 88
- Google-style docstrings on all public symbols; args/returns MUST include typehints
- StrEnum + @unique + auto() for string enums
- @final on all concrete leaf classes
- raise ... from e to preserve exception context; catch specific exceptions only
- No emojis in code, comments, logs, or documentation

## Quick Checklist

- [ ] Types complete and precise
- [ ] Docstrings present for public symbols
- [ ] Logging structured and safe
- [ ] No forbidden patterns (raw SQL, mutable defaults, unsafe eval)
