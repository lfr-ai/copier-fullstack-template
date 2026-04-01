---
description: Python coding conventions — enforcement patterns and modern standards
applyTo: '**/*.py'
---

```python
@dataclass
class MyClass: ...

@dataclass(frozen=True, slots=True)
class MyClass: ...
```

```python
class MyEnum(StrEnum):
    VALUE = auto()

@unique
class MyEnum(StrEnum):
    """Descriptive purpose. Never starts with articles."""
    VALUE = auto()
```

- ALL string enums: `StrEnum` + `@unique` + `auto()`
- ALL integer enums: `IntEnum` + `@unique`
- `auto()` unless exact value is external contract (comment explaining why)
- Member names: `UPPER_SNAKE_CASE`
- Defined in `utils/enums.py` or `core/enums/`
- NEVER use raw string literals where enum members should be
- Provide `from_str()` classmethod for external input parsing

```python
from typing import Any
def func(param: Any) -> Any: ...

def func(param: object) -> object: ...
```

```python
from typing import Optional, Union, List, Dict, Tuple, Set
x: Optional[str]
y: Union[int, str]
z: List[int]

x: str | None
y: int | str
z: list[int]
```

- ZERO `typing.List`, `Dict`, `Tuple`, `Set`, `Optional`, `Union`
- `typing` imports ONLY for: `TypeVar`, `Protocol`, `TypeAlias`, `Annotated`, `Literal`,
  `NoReturn`, `Generic`, `runtime_checkable`, `TypedDict`, `final`, `overload`,
  `TYPE_CHECKING`, `Self`, `override`
- ZERO `Final[type]` type annotations on constants — plain `UPPER_SNAKE_CASE` assignment
  is sufficient
- Use `match/case` for multi-branch dispatch over types, enums, literals
- Use `@override` on overriding methods
- Use `Self` for fluent/builder return types

```python
MAX_RETRIES: Final[int] = 3

MAX_RETRIES = 3

_INTERNAL_BUFFER_SIZE = 4096
```

- ZERO `Final[type]` type annotations on constants — plain `UPPER_SNAKE_CASE` is
  sufficient
- ZERO literal numbers in logic — extract to named `UPPER_SNAKE_CASE` constant
- ZERO hardcoded config strings — `AppSettings` or named constants
- ZERO hardcoded field/column names — naming registry
- ZERO hardcoded URLs/paths/timeouts/retries — named constants
- ZERO docstring comments on constants — the name and value are self-documenting

## `@final` Decorator on Classes

- Use `@final` on ALL concrete leaf classes:
  - Frozen dataclasses (`@dataclass(frozen=True)`)
  - Concrete service implementations
  - Middleware classes
  - Pydantic models
  - DTOs and mappers
  - GraphQL types
- NEVER use `@final` on:
  - `Protocol` classes
  - `ABC` abstract base classes
  - Domain entity base classes (Entity, AggregateRoot, ValueObject)
  - Extensible domain entities designed for subclassing
  - Enums
  - Exception base classes
  - Settings classes
  - `TypedDict` definitions
  - ORM base classes (declarative_base)
  - Generic base classes designed for subclassing
- Import: `from typing import final`

## Logging

```python
logger.info(f"Processing {item_id}")
logger.error("Failed: {}".format(msg))

logger.info("Processing %s", item_id)
```

- ALL log messages: `%s` formatting — ZERO f-strings, `.format()`, `+`
- ALL modules: `logger = logging.getLogger(__name__)`
- ALL exception handlers: `logger.exception()` or `logger.error(..., exc_info=True)`
- ZERO `print()` in source code (CLI `rich.console` excepted)
- ZERO sensitive data in logs (password, token, secret, key, credential)
- Log messages do NOT end with periods
- Log enum values as `.value` or `.name` explicitly

```python
except Exception as e:
    raise NewError("Failed")

except Exception as e:
    logger.error("Operation failed for %s", resource_id, exc_info=True)
    raise NewError("Failed") from e
```

- ALWAYS `raise ... from e` — chain exceptions
- ZERO bare `except:` — always specific types
- ZERO silent `except Exception:` without re-raise or explicit
  `# Explicitly silenced: <reason>`
- Exceptions logged BEFORE re-raising
- Error messages: `%s` formatting, NOT f-strings
- Domain exceptions at domain/application boundaries
- HTTP exceptions ONLY in `presentation/api/`
- `raise ... from None` ONLY with explicit justification comment

```zsh
emulate -L zsh
setopt PIPE_FAIL ERR_EXIT
```

- `.zsh` extension (never `.sh`)
- `.azcli` extension for Azure CLI scripts (valid zsh)
- `local` for all variables inside functions
- `zparseopts` for option parsing

```python
logger.info("Task completed.")

logger.info("Task completed")
```

```python
def process(data, validate=True, timeout=30.0): ...

def process(
    data: list[dict[str, object]],
    *,
    validate: bool = True,
    timeout: float = 30.0,
) -> ProcessedData: ...
```

When `*` is required:

- 3+ params (excluding self/cls) where at least one has a default
- ANY boolean flag parameter
- ANY optional/config param (timeout, retries, limit, offset, ttl, mode)
- ALL factory functions (`create_*`, `build_*`, `make_*`)
- ALL public API functions in `presentation/`
- ALL service methods in `application/services/`
- ALL utility functions in `utils/`

When `*` is NOT required:

- 0–2 params with no defaults
- ALL params required, distinct types, unambiguous ordering
- Dunder methods following Python protocols (`__eq__`, `__hash__`)
- Callbacks matching external contracts (FastAPI DI)

- `from __future__ import annotations` ONLY in files with:
  - `TYPE_CHECKING` blocks importing types
  - Forward references (types used before definition in return annotations)
- ZERO in other files — Python 3.11+ doesn't need it for most code
- EVERY function has return type (including `-> None`)
- EVERY parameter has type annotation
- EVERY `@property` has return type
- ALL class attributes typed
- Default values match their type annotation

- EVERY public module, class, method, function: docstring
- First line: imperative, ends with period, does NOT start with "A"/"An"/"The"
- `Args:` — each parameter described (NO types in docstring)
- `Returns:` — describes return value
- `Raises:` — lists exceptions
- Remove `:param:`/`@param` style — Google style only
- Use single quotes ('word') in docstrings to reference identifiers — NEVER double
  backticks

- `_` prefix on ALL non-public module-level functions, methods, attributes
- `_UPPER_SNAKE_CASE` on ALL internal-only constants
- NO `__` name mangling unless explicitly justified
- `__all__` in `__init__.py` files exporting public API

1. **Critical:** F-string logging, exception chaining (correctness + performance)
2. **High:** Dataclass slots, enum @unique, type coverage (correctness + memory)
3. **Medium:** Named constants (no Final[type]), @final on leaf classes, keyword-only
   args, modern syntax (maintainability)
4. **Low:** Unused imports, punctuation, underscore compliance (cleanliness)
