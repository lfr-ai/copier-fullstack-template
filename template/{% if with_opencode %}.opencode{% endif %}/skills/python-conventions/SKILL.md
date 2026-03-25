````skill
---
name: python-conventions
description: Enforces Python 3.12+ coding standards for this project — type hints, Google-style docstrings, keyword-only arguments, structured logging, and import conventions
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: coding
  layer: backend
---

## What I do

- Enforce Python 3.12+ coding conventions
- Validate type safety and annotation completeness
- Check docstring formats and completeness
- Enforce import ordering and restrictions
- Guide structured logging patterns

## Mandatory Conventions

### Every Python File Must Have
- `from __future__ import annotations` at the top
- Full type hints on ALL functions, methods, class attributes
- Google-style docstrings on all public modules, classes, functions, methods
- `__all__` in `__init__.py` where the package exposes a public API

### Function Signatures
```python
# CORRECT: keyword-only with * separator
def create_user(*, name: str, email: str, role: UserRole) -> User: ...

# INCORRECT: positional arguments
def create_user(name: str, email: str, role: UserRole) -> User: ...
````

### Dataclasses

```python
# CORRECT: Always frozen and slotted
@dataclass(frozen=True, slots=True)
class UserId:
    value: UUID
```

### Enums

```python
# CORRECT: Inherit from ParseableEnum with @unique
@unique
class Status(ParseableEnum):
    active = auto()
    inactive = auto()
```

### Logging

```python
# CORRECT: Structured logging with structlog
logger.info("user_created", user_id=user.id, role=user.role)

# INCORRECT: Never print() or f-strings in logging
print(f"User created: {user.id}")
logger.info(f"User created: {user.id}")
```

### Constants

```python
# CORRECT: Plain UPPER_SNAKE_CASE assignment (no Final annotation)
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30.0
_INTERNAL_BUFFER_SIZE = 4096
```

### Error Handling

```python
# CORRECT: Exception chaining
try:
    result = await client.fetch(url=url)
except httpx.HTTPError as exc:
    raise ServiceUnavailableError(service=service_name) from exc
```

## Prohibited Patterns

- `Any` type — use generics or `object`
- `Final` or `Final[type]` annotations on constants — plain `UPPER_SNAKE_CASE` is
  sufficient
- Double backticks in docstrings — use single quotes ('word') instead
- Relative imports outside `__init__.py`
- `print()` — use `structlog`
- `assert` for runtime validation
- `eval()`, `exec()`, `__import__()`, `pickle.loads()` on untrusted input
- Mutable default arguments
- f-strings in log calls — use `%s` formatting or structlog kwargs
- `os.path` — use `pathlib.Path`
- Importing concrete adapters in the application layer (Dependency Rule violation)
- Instantiating repositories directly in services — use UoW properties (`uow.users`)

## Style

- Line length: 99 characters
- Python 3.12+ syntax: `type` statements, `X | Y` unions, `match`
- `collections.abc` over `typing` for generic types
- `datetime.UTC` for timezone-aware datetimes
- `decimal.Decimal` for monetary values
- Context managers for all resource management

## When to use me

Use this skill when:

- Writing new Python code
- Reviewing Python code quality
- Adding type annotations
- Writing docstrings
- Setting up structured logging

```

```
