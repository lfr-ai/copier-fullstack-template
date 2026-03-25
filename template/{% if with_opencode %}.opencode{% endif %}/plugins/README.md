# OpenCode Plugins

Local plugins that extend OpenCode's capabilities for this project.

## Included Plugins

| Plugin              | Purpose                                                                |
| ------------------- | ---------------------------------------------------------------------- |
| `env-protection.ts` | Defense-in-depth: blocks reading `.env` files that may contain secrets |

## npm Plugins (via `opencode.json`)

These are installed automatically from npm at startup:

| Plugin                             | Install Reference                                           | Purpose                                                                                                                                                                                                                                                       |
| ---------------------------------- | ----------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `oh-my-opencode`                   | `"oh-my-opencode"`                                          | Multi-model agent harness (v3.12+): Sisyphus/Hephaestus/Prometheus/Oracle/Atlas/Momus/Metis agents, background agents, hash-anchored edits, LSP/AST tools, Sisyphus Tasks, skill-embedded MCPs, `ultrawork` command. Config: `.opencode/oh-my-opencode.jsonc` |
| `superpowers`                      | `"superpowers@git+https://github.com/obra/superpowers.git"` | Skills framework (90K+ stars): brainstorming, TDD, systematic debugging, code review, git worktrees, subagent-driven development                                                                                                                              |
| `opencode-dynamic-context-pruning` | `"opencode-dynamic-context-pruning"`                        | Optimizes token usage by pruning obsolete tool outputs                                                                                                                                                                                                        |
| `opencode-shell-strategy`          | `"opencode-shell-strategy"`                                 | Prevents hangs from TTY-dependent operations in non-interactive shells                                                                                                                                                                                        |

## Companion CLI Tools (installed separately)

| Tool                   | Install           | Purpose                                                                                                                                                                                                                                                              |
| ---------------------- | ----------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **GSD-2**              | `npm i -g gsd-pi` | Autonomous spec-driven development (v2.28+): `/gsd` (step mode), `/gsd auto`, `/gsd status`, `/gsd discuss`, `/gsd doctor`, `/gsd quick`, `/gsd keys`, `/gsd export`, plus `gsd headless` for CI/scripts. See: [gsd-build/GSD-2](https://github.com/gsd-build/GSD-2) |
| **OpenAgents Control** | OAC installer     | Pattern-controlled AI development: ContextScout, approval gates, MVI token efficiency, editable agents, team patterns. See: [darrenhinde/OpenAgentsControl](https://github.com/darrenhinde/OpenAgentsControl)                                                        |

See `docs/OPENCODE.md` for full setup instructions.

## oh-my-opencode Config

Project-level config: `.opencode/oh-my-opencode.jsonc`

This template disables OmO's built-in MCPs (context7, grep_app) because we configure our
own in `opencode.json`. All other defaults are preserved.

To customize agent model assignments or categories, edit the JSONC file.

## Adding Custom Plugins

Place JavaScript or TypeScript files in this directory. They are loaded automatically at
startup, after npm plugins.

For external npm dependencies, add a `package.json` in the `.opencode/` directory:

```json
{
  "dependencies": {
    "my-dependency": "^1.0.0"
  }
}
```

See [OpenCode Plugin Docs](https://opencode.ai/docs/plugins) for the full plugin API.
