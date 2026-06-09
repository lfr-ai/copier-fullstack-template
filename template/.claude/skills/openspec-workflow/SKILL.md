# OpenSpec Workflow Skill

## Purpose

Use OpenSpec as the spec-driven planning and execution layer for all non-trivial
changes. Keep behavior contracts in `openspec/specs/` and work-in-progress
changes in `openspec/changes/<change-name>/`.

## Tooling

- Initialize/update OpenSpec with the `task openspec:*` commands.
- Keep project context/rules in `openspec/config.yaml`.
- Use schema `clean-arch-spec-driven` by default.

## Command Syntax by Assistant

- **Claude Code**: `/opsx:propose`, `/opsx:apply`, `/opsx:archive`
- **GitHub Copilot (IDE)**: `/opsx-propose`, `/opsx-apply`, `/opsx-archive`

## Recommended Flow

### Core profile (default)

1. `/opsx:explore` (or `/opsx-explore`) when requirements are unclear.
2. `/opsx:propose` (or `/opsx-propose`) to create planning artifacts.
3. `/opsx:apply` (or `/opsx-apply`) to implement tasks.
4. `/opsx:sync` (or `/opsx-sync`) to merge delta specs if needed.
5. `/opsx:archive` (or `/opsx-archive`) when done.

### Expanded profile (optional)

Use `/opsx:new`, `/opsx:continue`, `/opsx:ff`, `/opsx:verify`,
`/opsx:bulk-archive`, `/opsx:onboard` when you need finer control.

## Quality Requirements

Every implementation change should include:

- Unit tests for pure logic
- Integration tests for cross-boundary behavior
- Property tests for invariants where applicable
- Updated docs and ADRs when behavior/setup changes
