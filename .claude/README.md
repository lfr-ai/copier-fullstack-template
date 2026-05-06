# Claude Code Quick Reference

**Project**: copier-fullstack-template
**Status**: ✅ Production-Ready

## Quick Stats

- **Agents**: 13 specialized agents
- **Rules**: 7 path-scoped rules
- **Commands**: 1 custom command
- **Skills**: 5 reusable skills
- **Hooks**: 4 hooks (8 script files across .sh + .ps1)
- **Plugins**: 15 enabled
- **MCP Servers**: 2 (context7, shadcn)

## Directory Structure

```text
.claude/
├── settings.json         # Main configuration
├── settings.local.json   # Local overrides (gitignored)
├── agents/              # 13 specialized agents
├── rules/               # 7 path-scoped rules
├── commands/            # 1 custom command
├── skills/              # 5 reusable skills
├── hooks/               # 4 hooks, each with .sh + .ps1 variants
├── CLAUDE.md           # Full documentation
└── README.md           # This file
```

## Quick Commands

### Using Agents

```bash
@architect Review architecture
@backend-engineer Implement feature
@frontend-engineer Build component
@testing-specialist Add tests
@code-reviewer Review changes
@debug Diagnose issue
```

### Using Commands

```bash
/commit Generate commit message
```

### Validation

```bash
# Verify setup
ls -la .claude/agents/ .claude/rules/ .claude/hooks/

# Test hooks
chmod +x .claude/hooks/*.sh
.claude/hooks/guard-destructive.sh

# Check settings
cat .claude/settings.json | jq .
```

## Agents Overview

| Agent | Purpose | Use When |
|-------|---------|----------|
| architect | Architecture & design | System design, module boundaries |
| backend-engineer | Backend development | API, services, database |
| frontend-engineer | Frontend development | UI components, state, routing |
| testing-specialist | Test strategy | Coverage, test design |
| code-reviewer | Code review | PR review, quality checks |
| debug | Debugging | Troubleshooting, root cause |
| deep-thinking | Extended reasoning | Complex decisions |
| modernization | Modernization | Upgrades, migrations |
| refactorer | Refactoring | Code improvement |
| researcher | Research | Library evaluation, docs |
| sdd | Story-Driven Dev | User story planning |
| tdd | Test-Driven Dev | Test-first development |
| devops | Infrastructure | Deployment, CI/CD |

## Rules Overview

| Rule | Applies To | Enforces |
|------|-----------|----------|
| architecture | `backend/src/**/*.py` | Clean Architecture boundaries |
| python | `**/*.py` | Python conventions, type hints |
| frontend | `frontend/src/**/*` | React/TypeScript rules |
| testing | `**/tests/**/*` | Test conventions, markers |
| shell | `**/*.sh`, `**/*.ps1` | Shell script standards |
| commit | Commit messages | Conventional Commits |
| docs-sync | Code changes | Keep docs updated |

## Skills Overview

| Skill | Domain | Contents |
|-------|--------|----------|
| clean-architecture | Architecture | Dependency Rule, layer boundaries |
| python-conventions | Python | Type hints, docstrings, patterns |
| testing-conventions | Testing | Markers, factories, coverage |
| naming-registry | Patterns | Registry-first constants |
| frontend-react-stack | Frontend | React + TypeScript + shadcn/ui |

## Hooks Overview

| Hook | Type | Purpose |
|------|------|---------|
| guard-destructive | PreToolUse | Block dangerous commands |
| guard-tool | PreToolUse | Tool-specific guards |
| stop-uncommitted-reminder | Stop | Warn about uncommitted work |
| check-licenses | Stop | License compatibility check |
| [auto-lint] | PostToolUse | Lint Python files (ruff) |

## Settings Highlights

### Permissions

- **Allow**: Read, Write, Edit, Bash (common commands), MCP tools
- **Ask**: git commit/push/stash, rm commands
- **Deny**: Destructive ops, secret files, force push

### Environment

```json
{
  "PYTHONPATH": "scripts:template/backend/src",
  "UV_LINK_MODE": "copy",
  "PYTHONDONTWRITEBYTECODE": "1",
  "PYTHONUNBUFFERED": "1",
  "FORCE_COLOR": "1"
}
```

### Enabled Plugins (15)

- pyright-lsp, typescript-lsp
- github, commit-commands
- frontend-design, superpowers
- context7, code-review
- code-simplifier, feature-dev
- skill-creator, playwright
- claude-md-management
- repo-quality-gate
- react-testing-library

## MCP Servers

- **context7**: Documentation lookup (https://context7.com)
- **shadcn**: shadcn/ui component management

## Common Workflows

### Feature Development

```bash
@researcher Research approach
@architect Design architecture
@backend-engineer Implement backend
@frontend-engineer Implement frontend
@testing-specialist Add tests
@code-reviewer Review changes
/commit Generate commit
```

### Bug Fix

```bash
@debug Diagnose issue
@backend-engineer Fix backend
@testing-specialist Add regression test
/commit Generate commit
```

### Refactoring

```bash
@architect Evaluate approach
@refactorer Refactor code
@testing-specialist Verify tests pass
@code-reviewer Review changes
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Agent not loading | Check frontmatter syntax, verify name |
| Rule not applying | Verify path pattern, check YAML |
| Hook not executing | Check executable bit, verify path |
| MCP server offline | Check `.mcp.json` and `.vscode/mcp.json`, verify server running |

## Quick Fixes

```bash
# Fix permissions
chmod +x .claude/hooks/*.sh

# Validate JSON
cat .claude/settings.json | jq .

# Test hook
export TOOL_INPUT='{"command":"ls"}'
.claude/hooks/guard-destructive.sh

# Check MCP
npx shadcn@latest mcp --version
```

## Next Steps

- Read [CLAUDE.md](./CLAUDE.md) for full documentation
- Review [agents/](./agents/) for agent details
- Check [rules/](./rules/) for rule specifics
- Explore [skills/](./skills/) for domain knowledge
- See [docs/comprehensive-root-configuration.md](../docs/comprehensive-root-configuration.md)

## Resources

- [Claude Code Docs](https://docs.anthropic.com/claude-code)
- [Template Docs](../docs/)
- [GitHub Copilot Config](../.github/copilot-instructions.md)
- [CodeRabbit Config](../.coderabbit.yaml)

---

**Status**: ✅ Complete
**Last Updated**: 2026-05-05
