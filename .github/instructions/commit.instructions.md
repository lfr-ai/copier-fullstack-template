---
description: Conventional commit message format enforced by commitizen
applyTo: "**"
---

# Commit Conventions

This project uses [Conventional Commits](https://www.conventionalcommits.org/) enforced
by commitizen.

## Format

```text
type(scope): description

[optional body]

[optional footer(s)]
```

## Types

| Type | Purpose |
|------|---------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, no logic change |
| `refactor` | Code change, no feature/fix |
| `perf` | Performance improvement |
| `test` | Adding/fixing tests |
| `build` | Build system or dependencies |
| `ci` | CI configuration |
| `chore` | Maintenance tasks |
| `revert` | Revert a previous commit |

## Scopes

`template`, `backend`, `frontend`, `infra`, `ci`, `copier`, `hooks`, `agents`

## Rules

- Description: imperative mood, lowercase, no period, max 72 chars
- Body: wrap at 100 chars, explain "what" and "why"
- Breaking changes: add `!` after type/scope or `BREAKING CHANGE:` footer
