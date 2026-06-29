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
- Agent definitions under `.claude/agents/`, `template/.claude/agents/`, and
  `template/.github/agents/` now use a unified broad tool set for all
  user-invocable agents (read, edit, execute, search, web, docs lookups).
- Alignment checks now enforce project-agnostic agentic content across
  `.agents/`, `.claude/`, `.github/` and template equivalents by scanning for
  repository- and workstation-specific tokens.
- Global safety constraints remain centralized in hook configs and runtime
  permission rules (for example, destructive operations and sensitive Git flows).
- Template-generated AGENTS guidance for downstream repositories.
- OpenSpec workflow skills for both Copilot and Claude
  (`.github/skills/openspec/`, `.claude/skills/openspec/`).
- OpenSpec prompts (`.github/prompts/openspec/`) and Claude commands
  (`.claude/commands/openspec/`).

## API endpoints or UI components

Not applicable. This is governance/policy infrastructure.

## Security and authorization

- Tool/hook governance includes safeguards against unsafe operations.
- Hook guardrails and Git safety restrictions remain authoritative even with
  broad per-agent tool enablement.
- Documentation and style constraints reduce risky or ambiguous code generation.
