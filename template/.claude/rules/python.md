---
paths:
  - "**/*.py"
---

# Python Conventions

- Use `from __future__ import annotations` in every module
- Type-annotate all public functions and methods
- Use keyword-only arguments (`*,`) for functions with 2+ parameters
- Use `Annotated[T, Depends(...)]` for FastAPI dependency injection
- Use `TYPE_CHECKING` guard for import-only types
- Use `structlog` for logging, never `print()`
- Use `@final` decorator (not `Final[...]` type annotation)
- Use `NoReturn` for functions that always raise
- Prefer `dataclass(frozen=True, slots=True, kw_only=True)` for value objects
- Use `Enum` with explicit string/int values, never auto()
- Chain exceptions: `raise NewError(...) from original_error`
- Use `functools.lru_cache` or `@cache` for expensive pure computations
