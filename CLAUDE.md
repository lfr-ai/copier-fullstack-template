# copier-fullstack-template

Copier template for fullstack Python (FastAPI) + React (TypeScript) applications.

## Project Type

This is a **Copier template repository**, NOT a generated project.
All template source files live under `template/` with `.jinja` suffix.

## CLAUDE.md File Scopes

Multiple `CLAUDE.md` files are intentional and scoped:

- `CLAUDE.md` (this file): concise repo-level orientation
- `.claude/CLAUDE.md`: Claude Code runtime configuration + operational details
- `template/CLAUDE.md.jinja` and `template/.claude/CLAUDE.md.jinja`: template sources
  for generated projects

## Key Paths

| Path | Purpose |
| ---- | ------- |
| `copier.yml` | Template questions and configuration |
| `template/` | Template source (rendered by Copier) |
| `template/backend/` | Python/FastAPI backend |
| `template/frontend/` | React/TypeScript frontend |
| `scripts/` | Template verification scripts |
| `.github/` | CI/CD and GitHub Copilot config |
| `.claude/` | Claude Code config (agents, rules, skills, hooks) |

## AI Assistant Configuration

| Tool | Configuration | Docs |
| ---- | ------------- | ---- |
| **Claude Code** | `.claude/` directory | `.claude/CLAUDE.md` |
| **GitHub Copilot** | `.github/copilot-instructions.md` | `.github/instructions/` |
| **MCP Servers** | `.mcp.json` (root) | context7, shadcn |

## Development Commands

```bash
# Render template locally
uvx copier copy --trust --defaults --vcs-ref HEAD . /tmp/test-render

# Run pre-commit hooks
uvx pre-commit run --all-files

# Validate template
python scripts/validate-template.py
```

## Commit Conventions

Conventional Commits enforced by commitizen:

```text
type(scope): description

Types: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert
Scopes: template, backend, frontend, infra, ci, copier, hooks, agents
```

## Non-Negotiable Rules

1. Never edit generated files — change template source under `template/`
2. Root `.github/` is a SUBSET of template's `.github/`
3. Test rendering after template changes
4. Pre-commit must pass before committing
5. All commits follow Conventional Commits format
