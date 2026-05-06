---
description: Generate conventional commit message from staged changes. Analyzes diff and git status to produce properly formatted commit.
---

## Current staged changes

!``git diff --cached``

## Git status

!``git status --short``

## Recent commits (for context)

!``git log --oneline -5``

## Instructions

Review the current git diff and create a well-structured conventional commit.

**If no changes are staged**, say so and ask if you should analyze unstaged changes instead.

**If changes are staged**, analyze and generate a commit message:

### Steps

1. Analyze the nature of changes: feat/fix/refactor/docs/test/chore/style/perf/ci/build
2. Determine the scope based on files changed:
   - **backend** — Backend Python code, services, core, infrastructure
   - **frontend** — Frontend TypeScript/React code, components, hooks
   - **infra** — Infrastructure, deployment, Docker, CI/CD
   - **registry** — Naming registry updates
   - **scripts** — Script files, tooling
   - **config** — Configuration files
   - **ai** — AI/ML model integration
   - **deps** — Dependency updates
   - **claude** — Claude Code configuration
   - **template** — Template structure changes
3. Write a concise commit message following Conventional Commits format:
   - **Subject**: `type(scope): imperative description` (max 72 chars)
   - **Body**: Explain WHY, not WHAT (wrap at 88 chars)
   - **Footer**: Reference issues if applicable (e.g., `Closes #123`, `Refs #456`)

### Commit Type Decision Tree

- **feat**: New user-visible functionality
- **fix**: Bug fix that changes behavior
- **refactor**: Code restructuring without behavior change
- **docs**: Documentation only
- **test**: Test changes only
- **chore**: Maintenance (deps, config, tooling)
- **style**: Code style/formatting only
- **perf**: Performance improvement
- **ci**: CI/CD changes
- **build**: Build system changes

### Rules

- Never combine unrelated changes in one commit
- Use `feat` only for new user-visible functionality
- Use `fix` only for bug fixes
- Use `refactor` for code restructuring without behavior change
- Use `!` suffix for breaking changes: `feat(backend)!: description`
- Do NOT suggest `--no-verify` or skipping hooks
- Verify `.env.example` is updated if new env vars were added
- Verify `registry/naming_registry.json` is updated if new field names were added

### Output Format

Present the commit message in a code block for easy copying:

```
type(scope): subject line

Body paragraph explaining why this change was made.

Footer: Closes #123
```

Then offer to execute: `git commit -m "..." -m "..."`
