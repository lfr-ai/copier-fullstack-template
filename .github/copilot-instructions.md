---
description: Coding conventions and guidelines for template development
applyTo: "**"
---

# Copier Fullstack Template — Development Instructions

Use this file as the **repo-wide baseline** for developing the template itself.
This is NOT a generated project — this is the template source repository.

## Scope and Precedence

- This file defines cross-cutting rules for template development
- `.github/instructions/*.instructions.md` define path-specific rules and take priority
- If instructions conflict, prefer the **most specific applicable scope**

## Project Snapshot

- Repository type: [Copier](https://copier.readthedocs.io/) template
- Generates: Fullstack Python + React/TypeScript projects
- Template root: `template/`
- Config: `copier.yml` (questions, defaults, hooks)
- Rendering engine: Jinja2 (`.jinja` suffix)

### Key Paths

| Path | Purpose |
|------|---------|
| `copier.yml` | Copier configuration, questions, and answers |
| `template/` | The actual template files (rendered by Copier) |
| `template/backend/` | Backend template (Python, FastAPI, Clean Architecture) |
| `template/frontend/` | Frontend template (React, TypeScript, Vite, shadcn/ui) |
| `template/.github/` | GitHub config template (agents, hooks, instructions, workflows) |
| `.github/` | Root repo GitHub config (SUBSET of template's `.github`) |
| `scripts/` | Template verification scripts (called by `Taskfile.yml`) |
| `.pre-commit-config.yaml` | Pre-commit hooks for the root repo |

## Scoped Instructions (`.github/instructions/`)

File-scoped instructions auto-load for matching globs:

- `commit.instructions.md` — Conventional commit format for `**`
- `no-heredoc.instructions.md` — Prevents heredoc file corruption for `**`
- `prompt.instructions.md` — Guidelines for creating prompt files for `**/*.prompt.md`
- `python.instructions.md` — Python conventions for `scripts/**/*.py`
- `shell.instructions.md` — Shell/PowerShell conventions for `**/*.{sh,ps1}`
- `update-docs-on-code-change.instructions.md` — Auto-update docs when code changes

## Agent Modes (`.github/agents/`)

Specialized agents for template development:

| Agent | Purpose |
|-------|---------|
| `debug` | Diagnostic debugging with root cause analysis |
| `deep-thinking` | Extended reasoning for complex decisions |
| `modernization` | Codebase modernization and migration |

## Agent Skills (`.github/skills/`)

| Skill | Domain |
|-------|--------|
| `clean-architecture/` | Architecture boundaries and Dependency Rule |
| `python-conventions/` | Python code quality and typing standards |
| `testing-conventions/` | Test strategy, markers, and coverage gates |
| `naming-registry/` | Registry-first constant/code generation |
| `frontend-react-stack/` | React + TypeScript + Router + shadcn/ui |

## Copilot Hooks (`.github/hooks/`)

Active hooks for the Copilot coding agent:

- **tool-guardian** (PreToolUse) — Blocks dangerous operations (force push, `rm -rf`, etc.)
- **check-licenses** (Stop) — Scans dependencies for license compatibility

## File Naming Conventions

| Type | Extension | Example |
|------|-----------|---------|
| Copier template files | `*.jinja` (appended to real ext) | `pyproject.toml.jinja` |
| Copier conditional dirs | `{% if var %}dirname{% endif %}/` | `{% if use_caddy %}caddy{% endif %}/` |
| Markdown | `.md` | `README.md` |
| YAML | `.yaml` (default), `.yml` (tool-conventional exceptions) | `.yamllint.yaml`, `copier.yml` |
| JSON | `.json` | `cspell.json` |

## Jinja2 Template Rules

- Template files live under `template/` and use `.jinja` suffix
- Use `{{ variable }}` for Copier answers (defined in `copier.yml`)
- Use `{% if condition %}...{% endif %}` for conditional content
- Conditional directories use the pattern `{% if var %}dirname{% endif %}/`
- NEVER use raw Python expressions in templates — only Copier answer variables
- Test template rendering with `uvx copier copy --trust --defaults .` locally

## Copier Questions (`copier.yml`)

When adding new template variables:

1. Add the question to `copier.yml` with type, help text, and default
2. Use the variable in templates with `{{ variable_name }}`
3. Test rendering with both default and non-default values
4. Update CI render smoke test if the variable affects expected output files

## Build, Test, and Validation Workflow

Always prefer repository-native tooling:

- Pre-commit: `uvx pre-commit run --all-files`
- Render test: `uvx copier copy --trust --defaults --vcs-ref HEAD . /tmp/test-render`
- Commit-msg hook: `uvx pre-commit install --hook-type commit-msg`

Tooling conventions:

- Python runtime/packages: `uv` (via `uvx`)
- Template engine: Copier
- Git hooks: pre-commit
- Commit format: Conventional Commits (commitizen)

## Commit Conventions

This project uses [Conventional Commits](https://www.conventionalcommits.org/) enforced
by commitizen. Use the conventional-commit prompt (`.github/prompts/`) or:

```text
type(scope): description

Types: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert
Scopes: template, backend, frontend, infra, ci, copier, hooks, agents
```

## Non-Negotiable Rules

1. **Never edit generated files** — change the template source under `template/`
2. **Root `.github/` is a SUBSET** — root is for template development only;
   template `.github/` is for generated projects
3. **Test rendering** — after any template change: `uvx copier copy --trust --defaults
   --vcs-ref HEAD . /tmp/test-render`
4. **Pre-commit must pass** — `uvx pre-commit run --all-files`
5. **Conventional commits** — all commits must follow the format above

## Documentation Policy

- For library/framework/API documentation, prefer Context7 first
- If Context7 is insufficient, use official vendor docs and cite sources
