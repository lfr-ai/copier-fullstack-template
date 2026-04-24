# Feature: agent governance and instructions

## Purpose and scope

Defines coding-agent policy layers, scoped instruction files, and non-negotiable
implementation constraints for template development and generated projects.

## Analyzed files

- `.github/copilot-instructions.md`
- `.github/instructions/python.instructions.md`
- `template/.github/instructions/coding-conventions.instructions.md`
- `template/AGENTS.md.jinja`

## Business rules and constraints

- Internal constants/variables must not use `Final[...]`
  (`.github/copilot-instructions.md:141`).
- API HTTP status handling must use FastAPI status constants
  (`.github/copilot-instructions.md:143`).
- Python docstrings use single-quoted identifier references and typed Args/Returns
  (`.github/instructions/python.instructions.md:35`).
- Python modules/files require top-level module docstrings as first significant
  statement and are enforced with checker tooling
  (`.github/instructions/python.instructions.md`,
  `template/.github/instructions/coding-conventions.instructions.md`).
- Template instructions enforce underscore-prefixed internals and selective
  `Annotated[...]` usage (`template/.github/instructions/coding-conventions.instructions.md`).

## Workflows (with code references)

1. Root instructions guide template-source contributions.
2. Template instructions are rendered into generated projects for downstream policy.
3. Verification scripts + pre-commit operationalize those policies.

## Data models and dependencies

- Policy model is file-scoped via `applyTo` globs.
- Agent behavior depends on `.github/instructions` + skill packs.

## Integrations

- Copilot agents and hooks.
- Template-generated AGENTS guidance for downstream repositories.

## API endpoints or UI components

Not applicable. This is governance/policy infrastructure.

## Security and authorization

- Tool/hook governance includes safeguards against unsafe operations.
- Documentation and style constraints reduce risky or ambiguous code generation.
