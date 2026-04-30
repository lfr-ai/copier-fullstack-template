---
name: Commit Conventions
description: Conventional Commits format enforced on all commits
paths:
  - "**"
---

# Commit Conventions

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
type(scope): description
```

## Types

feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert

## Scopes

backend, frontend, infra, ci, registry, scripts, docs, config, ai, deps

## Rules

- Subject line: imperative mood, no period, max 72 chars
- Body: wrap at 88 chars, explain WHY not WHAT
- Breaking changes: `feat(backend)!: description` or `BREAKING CHANGE:` in footer
- Reference issues: `Closes #123` or `Fixes #456` in footer
