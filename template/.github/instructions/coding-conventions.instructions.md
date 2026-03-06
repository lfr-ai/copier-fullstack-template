---
description: Coding conventions enforcement automation guidelines
applyTo: "**/*.py"
---

# Coding Conventions Enforcement Instructions

## Purpose

This document provides guidelines for automated enforcement of coding conventions
as specified in [copilot-instructions.md](../copilot-instructions.md).

## When to Use

- During code reviews to identify convention violations
- When onboarding new team members to ensure consistency
- As part of refactoring efforts
- Before major releases to ensure code quality

## Automated Enforcement Patterns

### 1. Dataclass Optimization

**Detect:**

```python
@dataclass
class MyClass:
    ...
```

**Required:**

```python
@dataclass(frozen=True, slots=True)
class MyClass:
    ...
```

**Rationale:** `frozen=True` for immutability; `slots=True` for memory reduction.

### 2. Enum Validation

**Detect:**

```python
class MyEnum(StrEnum):
    VALUE1 = auto()
```

**Required:**

```python
@unique
class MyEnum(StrEnum):
    VALUE1 = auto()
```

**Rationale:** Prevents duplicate enum values.

### 3. Type Hints - Any to object

**Detect:**

```python
from typing import Any
def func(param: Any) -> Any: ...
```

**Required:**

```python
def func(param: object) -> object: ...
```

**Rationale:** `object` provides minimal type safety; `Any` disables type checking.

### 4. Constants with Final

**Detect:**

```python
MAX_RETRIES = 3
```

**Required for public constants:**

```python
from typing import Final
MAX_RETRIES: Final[int] = 3
```

**Exception -- internal (`_`-prefixed) constants:**

Do NOT apply `Final` to internal constants prefixed with `_`.
The underscore prefix already signals non-public status.

```python
# Correct -- no Final for internal constants
_INTERNAL_BUFFER_SIZE = 4096
_DEFAULT_ENCODING = "utf-8"

# Public constants require Final
MAX_RETRIES: Final[int] = 3
```

### 5. F-String Logging (CRITICAL)

**Detect:**

```python
logger.info(f"Processing {item_id}")
```

**Required:**

```python
logger.info("Processing %s", item_id)
```

**Rationale:** Lazy evaluation, only formats if log level is active.

### 6. Exception Chaining

**Detect:**

```python
except Exception as e:
    raise NewError("Failed")
```

**Required:**

```python
except Exception as e:
    raise NewError("Failed") from e
```

### 7. Shell Script Extensions

All shell scripts must use `.zsh` extension with proper shebang:

```zsh
#!/usr/bin/env zsh
emulate -L zsh
setopt PIPE_FAIL ERR_EXIT
```

### 8. Log Message Punctuation

**Detect:**

```python
logger.info("Task completed.")
```

**Required:**

```python
logger.info("Task completed")
```

No trailing punctuation in log messages or short comments.

## Batch Enforcement Priorities

1. **Critical:** F-string logging (performance impact)
2. **High:** Dataclass slots (memory impact)
3. **High:** Enum @unique (correctness)
4. **Medium:** Type hints Any to object (type safety)
5. **Medium:** Public constants with Final (maintainability)
6. **Low:** Unused imports, punctuation (cleanliness)

## References

- Main conventions: [copilot-instructions.md](../copilot-instructions.md)
- PEP 8: https://peps.python.org/pep-0008/
- Python typing: https://docs.python.org/3/library/typing.html
