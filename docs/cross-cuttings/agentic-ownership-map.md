# Agentic ownership map (root vs template)

This is the source-of-truth map for where agentic assets belong in this
repository.

Machine-readable mirror pairs are defined in
`docs/cross-cuttings/agentic-ownership-map.json`.

The same JSON now also owns:

- required file policy (`requiredFiles`)
- forbidden legacy file policy (`legacyFiles`)
- project-token scan scope (`agenticPathsToScan`)
- mirror policy semantics (`requiredInRoot`, `requiredInTemplate`, `optional`)

## Principles

- Root owns template-authoring workflows and repo maintenance checks.
- `template/` owns generated-project runtime assets and user-facing scaffolding.
- Shared capabilities are mirrored in both when needed.

## Ownership matrix

| Capability | Root | Template | Notes |
| --- | --- | --- | --- |
| GitHub agents | *(none)* | `template/.github/agents/` | Generated-project only; keep role names project-agnostic |
| Claude agents | `.claude/agents/` | `template/.claude/agents/` | Core role set mirrored |
| Claude commands | `.claude/commands/` | `template/.claude/commands/` | Core GitNexus/OpenSpec mirrored; template adds `opsx/*` |
| Instructions | `.github/instructions/` | `template/.github/instructions/` | Scope via `applyTo` |
| Skills | `.github/skills/` | `template/.github/skills/` | Frontend skills must exist in both |
| Prompts | `.github/prompts/` | `template/.github/prompts/` | GitNexus/OpenSpec subset mirrored; template keeps extra scaffolding prompts |
| Hook configs | `.github/hooks/*.json` | `template/.github/hooks/hooks.json` | Commands must target `.github/hooks/scripts/*` |
| Hook scripts | `.github/hooks/scripts/` | `template/.github/hooks/scripts/` | Cross-platform `.sh` + `.ps1` |
| MCP config | `.vscode/mcp.json`, `.claude/mcp.json` | `template/.vscode/mcp.json.jinja`, `template/.claude/mcp.json.jinja` | Keep core server set aligned |
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

The alignment script validates critical root↔template mirror pairs from the
JSON ownership matrix above and consumes required/legacy/scan-path policy from
the same file.

Mirror entries now use explicit policy semantics:

- `requiredInRoot`: root-side files in `pairs` must exist.
- `requiredInTemplate`: template-side files in `pairs` must exist.
- `optional`: when true, missing pair files are non-failing.

Project-agnostic token checks in `scripts/check-github-alignment.py` are now
derived dynamically from the current repository root path/name instead of
hardcoded machine-specific tokens.
