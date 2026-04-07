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
