# Claude Code Context

This directory contains Claude-native configuration files.

## Directory Structure

```
.claude/
├── settings.json          # Hooks, permissions, tool allowlists
├── settings.local.json    # Local overrides (not committed)
├── rules/                 # Scoped instructions (paths array format)
│   ├── architecture.md    # Clean Architecture boundaries
│   ├── python.md          # Python coding standards
│   ├── frontend.md        # React/TypeScript conventions
│   ├── testing.md         # Test structure and coverage
│   ├── shell.md           # zsh scripting standards
│   └── commit.md          # Conventional Commits format
└── agents/                # Claude-native agent definitions
    ├── deep-thinking.md   # Extended reasoning
    ├── debug.md           # Diagnostic debugging
    ├── tdd.md             # Test-Driven Development
    ├── sdd.md             # Spec-Driven Development
    ├── frontend-engineer.md  # React/TypeScript expert
    └── modernization.md   # Codebase upgrades
```

## Cross-Format Compatibility

VS Code discovers configuration from both locations:

| Claude Format | Copilot Equivalent |
| --- | --- |
| `.claude/rules/*.md` (paths array) | `.github/instructions/*.instructions.md` (applyTo) |
| `.claude/agents/*.md` (tools string) | `.github/agents/*.agent.md` (tools array) |
| `.claude/settings.json` (hooks) | `.github/hooks/hooks.json` |
| `CLAUDE.md` (always-on) | `.github/copilot-instructions.md` + `AGENTS.md` |

Both systems enforce identical conventions.
