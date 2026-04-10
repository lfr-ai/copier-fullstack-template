# Contributing to copier-fullstack-template

Thank you for your interest in contributing. This guide covers the development
setup and workflow for working on the **template itself**, not on projects
generated from it.

---

## Prerequisites

| Tool | Purpose |
|------|---------|
| [uv](https://docs.astral.sh/uv/) | Python package manager |
| [Copier](https://copier.readthedocs.io/) | Template engine (`uvx copier`) |
| [go-task](https://taskfile.dev/) | Task runner |
| [ripgrep](https://github.com/BurntSushi/ripgrep) | Fast search (used by verification tasks) |
| Git | Version control |

## Getting Started

```bash
# 1. Fork and clone the repository
git clone https://github.com/<your-fork>/full-stack-copier-template.git
cd full-stack-copier-template

# 2. Run template verification
task verify-all

# 3. Test a local render
uvx copier copy --trust . /tmp/test-project
```

## Repository Structure

```
copier.yml          # Copier engine configuration (questions, defaults, hooks)
Taskfile.yml        # Template verification tasks
template/           # Everything inside here gets rendered by Copier
  backend/          # Python backend (FastAPI, Clean Architecture)
  frontend/         # React + TypeScript frontend
  .github/          # GitHub Actions, Copilot customizations
  ...
```

**Key rule**: only edit files inside `template/`. Root-level files (`copier.yml`,
`Taskfile.yml`, `README.md`, etc.) are for the template repository itself.

## Development Workflow

### Making Changes

1. Create a feature branch:

   ```bash
   git checkout -b feat/your-feature-name
   ```

2. Edit template files inside `template/`.

3. Run verification to ensure nothing is broken:

   ```bash
   task verify-all
   ```

4. Test a local render to verify the generated output:

   ```bash
   uvx copier copy --trust . /tmp/test-render
   ```

5. Commit using [Conventional Commits](https://www.conventionalcommits.org/):

   ```bash
   git commit -m "feat(backend): add Redis cache adapter"
   ```

### Branch Naming

- `feat/` — new features or template capabilities
- `fix/` — bug fixes in generated output
- `docs/` — documentation changes
- `chore/` — maintenance (CI, dependencies, tooling)

### Commit Message Format

`type(scope): description`

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `perf`, `ci`, `build`, `revert`

**Scopes**: `backend`, `frontend`, `infra`, `ci`, `copier`, `docs`

## Verification Tasks

```bash
task verify-all        # Run all checks
task test              # Clean Architecture boundary check
task lint              # Coding conventions check
task docs:architecture # Architecture docs verification
task docs:conventions  # Coding conventions docs verification
```

## Code Standards

### Jinja Templates

- Use `.jinja` suffix for files that need Copier rendering
- Use conditional folder names for optional features: `{% if use_ai %}ai{% endif %}`
- Prefer `{{ project_slug }}` over hardcoded package names

### Python (inside template)

- Line length: 88 characters (Ruff/Black standard)
- Type hints on all public functions and methods
- Google-style docstrings on public interfaces
- Clean Architecture: core layer has zero framework imports

### TypeScript (inside template)

- Strict mode enabled
- No `any` — use `unknown` or proper generics
- Biome for formatting and linting

## Submitting a Pull Request

1. Push your branch and open a PR against `main`.
2. Ensure `task verify-all` passes.
3. Describe what the change does and why.
4. Link related issues if applicable.

## Reporting Issues

- Use [GitHub Issues](https://github.com/lfr-ai/full-stack-copier-template/issues)
- Include steps to reproduce and expected vs. actual behavior
- For security vulnerabilities, see [SECURITY.md](SECURITY.md)

## License

By contributing, you agree that your contributions will be licensed under the
[MIT License](LICENSE).
