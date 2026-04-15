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

## Error Handling

- Catch specific exceptions, never bare `except:`
- Use custom exception classes for domain errors
- Let unexpected errors propagate

## Testing

- Use pytest with markers: `@pytest.mark.unit`, `@pytest.mark.integration`
- Use factories over fixtures for test data
- One assertion concept per test
