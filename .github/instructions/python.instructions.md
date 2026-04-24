---
description: Python coding conventions for template source scripts and verification code
applyTo: "scripts/**/*.py"
---

# Python Conventions

## Style

- Target Python 3.12+
- Use `from __future__ import annotations` in every module
- Prefer keyword-only arguments (`*` separator) for functions with 2+ params
- Use `pathlib.Path` over `os.path`
- Use f-strings over `.format()` or `%`

## Type Annotations

- Annotate all function signatures (parameters and return types)
- Use `TYPE_CHECKING` guard for import-only types
- Prefer `collections.abc` types over `typing` equivalents (`Sequence`, `Mapping`)
- Use `X | None` union syntax (not `Optional[X]`)
- Use `Annotated[...]` only when runtime metadata is required (FastAPI `Depends`,
  Pydantic `Field` constraints, validation metadata)
- NEVER use `Annotated` for plain type hints without metadata

## Constants and Visibility — CRITICAL

- NEVER use `Final` or `Final[...]` for internal constants or internal variables
- Reserve `Final` for public module constants ONLY when truly needed
- Prefer plain `UPPER_SNAKE_CASE` assignment — the naming convention already signals
  immutability intent
- Prefix internal constants with `_UPPER_SNAKE_CASE`
- Prefix internal variables and helper functions with `_`
- A plain type annotation (e.g. `_FOO: Path = ...`) is sufficient for internal
  variables — the leading underscore already signals 'private, do not reassign'
- Prefer `_*.py` module names for non-public implementation modules

## Docstrings

- Every Python module/file MUST have a module-level docstring as the first
  significant statement (before imports), excluding shebang/encoding/comments.
- Use Google-style docstrings
- `Args:` — each parameter MUST include type: `name (Type): Description.`
- `Returns:` — MUST include type: `TypeName: Description.` (no parentheses)
- `Raises:` — format: `ExceptionName: Description.` (no parentheses)
- Use single quotes for identifier references in docstrings (not markdown backticks)
- Enforcement command: `python scripts/check-module-docstrings.py scripts template/backend/src template/tools`

## FastAPI Status Codes

- In API code, always use `from fastapi import status`
- Never use numeric literals like `status_code=200`
- Never import status from Starlette directly
- In test assertions, also use `from fastapi import status` constants

## Error Handling

- Catch specific exceptions, never bare `except:`
- Use custom exception classes for domain errors
- Let unexpected errors propagate
- Always use `raise ... from e` to chain exceptions

## Testing

- Use pytest with markers: `@pytest.mark.unit`, `@pytest.mark.integration`
- Use factories over fixtures for test data
- One assertion concept per test
