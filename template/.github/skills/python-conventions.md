# Skill: Python Conventions

## Purpose

Apply project Python standards consistently for readability, safety, and maintainability.

## Use This Skill When

- Writing or refactoring Python code
- Adding public APIs, services, DTOs, mappers
- Fixing lint/type/documentation issues

## Rules

- Use Python {{ python_version }}+ features and full type hints
- Add `from __future__ import annotations` in each Python module
- Use keyword-only args (`*`) for multi-parameter constructors/functions
- Use structured logging, not `print()`
- Avoid `Any`; prefer precise types or `object`
- Keep line length <= 99

## Quick Checklist

- [ ] Types complete and precise
- [ ] Docstrings present for public symbols
- [ ] Logging structured and safe
- [ ] No forbidden patterns (raw SQL, mutable defaults, unsafe eval)
