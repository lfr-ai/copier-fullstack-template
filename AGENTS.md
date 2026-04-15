# Agent Configuration

This file provides instructions for AI coding agents (GitHub Copilot, Cursor, Cline,
OpenCode, etc.) working within this **template repository**.

## Important Context

This is a **Copier template repository**, NOT a generated project. All template source
files live under `template/` and use the `.jinja` suffix. The root directory contains
only template development tooling.

> **GitHub Copilot users**: See `.github/copilot-instructions.md` for detailed,
> Copilot-specific instructions including scoped instructions, hooks, and Jinja2 rules.

## Documentation and Code-Example Search Policy

- When you need official library/framework documentation, **use Context7 tools first**
- Prefer Context7 for authoritative API/reference answers
- For Copier-specific patterns, check the
  [Copier docs](https://copier.readthedocs.io/) first

## Project Structure

```text
copier-fullstack-template/
├── copier.yml                 # Copier configuration (questions, answers)
├── template/                  # Template source (rendered by Copier)
│   ├── backend/               # Python/FastAPI backend template
│   ├── frontend/              # React/TypeScript frontend template
│   ├── .github/               # GitHub config for GENERATED projects
│   └── ...                    # Other template files
├── .github/                   # GitHub config for THIS repo (subset)
│   ├── agents/                # Copilot agent definitions
│   ├── hooks/                 # Copilot coding agent hooks
│   ├── instructions/          # Scoped instructions
│   ├── skills/                # Domain knowledge playbooks
│   └── workflows/             # CI/CD for template development
├── scripts/                   # Template verification scripts
├── .pre-commit-config.yaml    # Pre-commit hooks
├── .cz.toml                   # Commitizen configuration
└── ...                        # Root documentation files
```

## Key Conventions

### Template Development

- Edit files under `template/` to change what generated projects contain
- Edit root files to change template development tooling
- Root `.github/` is a SUBSET of `template/.github/` — never duplicate
- All template files use `.jinja` suffix appended to their real extension
- Copier answer variables are defined in `copier.yml`

### Commit Format

This project uses Conventional Commits enforced by commitizen:

```text
type(scope): description

Scopes: template, backend, frontend, infra, ci, copier, hooks, agents
```

### Testing

After any template change, verify rendering:

```bash
uvx copier copy --trust --defaults --vcs-ref HEAD . /tmp/test-render
```

### Pre-commit

All commits must pass pre-commit hooks:

```bash
pre-commit run --all-files
```
