# Agentic ownership map (root vs template)

This is the source-of-truth map for where agentic assets belong in this
repository.

## Principles

- Root owns template-authoring workflows and repo maintenance checks.
- `template/` owns generated-project runtime assets and user-facing scaffolding.
- Shared capabilities are mirrored in both when needed.

## Ownership matrix

| Capability | Root | Template | Notes |
| --- | --- | --- | --- |
| Agents | `.github/agents/` | `template/.github/agents/` | Keep role names project-agnostic |
| Instructions | `.github/instructions/` | `template/.github/instructions/` | Scope via `applyTo` |
| Skills | `.github/skills/` | `template/.github/skills/` | Frontend skills must exist in both |
| Prompts | `.github/prompts/` | `template/.github/prompts/` | OpenSpec/GitNexus parity required |
| Hook configs | `.github/hooks/*.json` | `template/.github/hooks/hooks.json` | Commands must target `.github/hooks/scripts/*` |
| Hook scripts | `.github/hooks/scripts/` | `template/.github/hooks/scripts/` | Cross-platform `.sh` + `.ps1` |
| MCP config | `.mcp.json`, `.vscode/mcp.json`, `.claude/mcp.json` | `template/.mcp.json.jinja`, `template/.claude/mcp.json.jinja` | Keep server set aligned |
| OpenSpec | `openspec/` | `template/openspec/` | Root for template changes, template for generated repos |
| GitNexus | `.gitnexus/`, `.gitnexusignore` | `template/{% if with_gitnexus %}.gitnexus{% endif %}/` | Generated only when enabled |

## Frontend-specific required capabilities

These must remain present and updated in root and template:

- Storybook conventions and AI manifest guidance.
- Playwright best-practice guidance.
- shadcn/ui composition guidance.
- Accessibility guidance.

## Drift checks

Use these validation commands:

- `python scripts/check-github-alignment.py`
- `python scripts/audit_reference_alignment.py`
- `python scripts/audit_golden_alignment.py`
