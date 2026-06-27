# Claude Code Configuration - copier-fullstack-template

This directory contains comprehensive Claude Code project configuration for template development.

## Structure

```text
.claude/
├── settings.json              # Project settings (permissions, env, hooks, plugins)
├── settings.local.json        # Local overrides (gitignored)
├── agents/                    # Specialized agents (16)
├── rules/                     # Path-scoped rules (20)
├── commands/                  # Custom commands (14)
├── skills/                    # Reusable skills (14)
├── hooks/                     # Pre/Post tool-use hooks (both .sh and .ps1)
└── CLAUDE.md                  # This documentation
```

## Agents (16)

Specialized agents for template development workflows:

### Architecture & Design
- **architect.md** — System architecture and design decisions
- **backend-engineer.md** — Backend development specialist
- **frontend-engineer.md** — Frontend development specialist
- **devops.md** — Infrastructure and deployment
- **ddd.md** — Domain-Driven Design modeling

### Code Quality
- **code-reviewer.md** — Code review and quality assessment
- **refactorer.md** — Code refactoring and improvement
- **testing-specialist.md** — Test strategy and coverage
- **security-specialist.md** — Security reviews and vulnerability analysis

### Methodology
- **sdd.md** — Specification-Driven Development (SDD)
- **tdd.md** — Test-Driven Development (TDD)

### Analysis & Support
- **debug.md** — Diagnostic debugging
- **deep-thinking.md** — Extended reasoning
- **modernization.md** — Codebase modernization
- **researcher.md** — Research and exploration
- **ui-ux-frontend.md** — UI/UX interaction quality

## Rules (20)

Path-scoped rules automatically loaded for matching files:

- **agent-prompting.md** — Agent prompt quality standards
- **architecture-boundaries.md** — Cross-language architecture enforcement
- **architecture.md** — Clean Architecture boundaries (`backend/src/**/*.py`)
- **coding-conventions.md** — Cross-language coding standards
- **cognitive-load.md** — Readability and maintainability
- **commit.md** — Conventional commit format
- **ddd.md** — Domain-Driven Design (`core/**/*.py`)
- **docs-sync.md** — Keep docs updated with code
- **frontend.md** — React/TypeScript rules (`frontend/src/**/*`)
- **prompt.md** — Prompt file standards
- **python-conventions.md** — Python conventions (`**/*.py`)
- **react-conventions.md** — React component rules (`**/*.tsx`)
- **readability-and-cognitive-load.md** — Clarity-first structure
- **registry.md** — Registry-first naming patterns
- **sdd.md** — Spec-driven development
- **shell.md** — Shell script rules (`**/*.sh`, `**/*.ps1`)
- **tdd.md** — Test-driven development
- **testing.md** — Test conventions (`**/tests/**/*`)
- **typescript-conventions.md** — TypeScript standards
- **ui-ux-frontend.md** — UI/UX interaction rules

## Commands (14)

Custom commands for common workflows:

- **commit.md** — Intelligent commit message generation
- **gitnexus/debug.md** — Graph-powered debugging
- **gitnexus/impact.md** — Change impact analysis
- **openspec/apply.md** — Apply spec changes to code
- **openspec/archive.md** — Archive completed specs
- **openspec/bulk-archive.md** — Bulk archive specs
- **openspec/continue.md** — Continue spec implementation
- **openspec/explore.md** — Explore spec landscape
- **openspec/ff.md** — Fast-forward implementation
- **openspec/new.md** — Create new spec
- **openspec/onboard.md** — Onboard to OpenSpec workflow
- **openspec/propose.md** — Propose spec changes
- **openspec/sync.md** — Sync specs with implementation
- **openspec/verify.md** — Verify spec compliance

## Skills (14)

Reusable domain knowledge:

- **clean-architecture/** — Architecture boundaries and Dependency Rule
- **ddd/** — Domain-Driven Design tactical patterns
- **dry-refactoring/** — Clone detection and elimination
- **frontend-react-stack/** — React + TypeScript + shadcn/ui
- **gitnexus/** — Graph-powered code intelligence
- **jscpd/** — Clone detection workflow
- **naming-registry/** — Registry-first constant generation
- **openspec/** — OpenSpec workflow skills
- **python-conventions/** — Python code quality standards
- **quality-gate/** — Validation gates before completion
- **sdd/** — Specification-driven implementation
- **tdd/** — Test-driven development
- **testing-conventions/** — Test strategy and markers
- **ui-ux-frontend/** — Frontend interaction quality

## Settings

### settings.json

- **Environment**: Python/UV paths, color forcing
- **Permissions**: Explicit allow/ask/deny lists
- **Hooks**:
  - **PreToolUse**: Guard against destructive commands
  - **PostToolUse**: Auto-lint Python files with ruff
  - **Stop**: Remind about uncommitted changes
- **MCP Servers**: context7, shadcn, gitnexus, playwright (via `.claude/mcp.json` and `.vscode/mcp.json`)
- **Plugins**: 15 essential plugins enabled
- **Attribution**: `chore(claude):` commits, `🤖 Claude Code:` PRs

### settings.local.json

Local overrides (gitignored):
- Environment variables
- Permission overrides
- Hook customizations

**Note**: Never commit secrets or personal config to `settings.local.json`.

## Hooks

All hooks have both `.sh` (Unix/Linux/macOS) and `.ps1` (Windows) versions:

### PreToolUse
- **guard-destructive** — Blocks dangerous bash commands
- **guard-tool** — Additional tool-specific guards

### PostToolUse
- Auto-linting for Python files (ruff)
- Format-on-save for modified files

### Stop
- **stop-uncommitted-reminder** — Warns about uncommitted work
- **check-licenses** — Scans dependencies for license compatibility

## MCP Servers

Configured in `.claude/mcp.json` (Claude Code) and `.vscode/mcp.json` (VS Code/Copilot):

- **context7** — Documentation lookup ([context7.com](https://context7.com))
- **shadcn** — shadcn/ui component management
- **gitnexus** — Graph-powered code intelligence
- **playwright** — Browser automation via Playwright MCP

## Usage

### Loading Agents

```bash
# In Claude Code chat
@architect Review this module design

@backend-engineer Implement user service

@testing-specialist Add test coverage
```

### Using Rules

Rules auto-load based on file paths:
- Edit `backend/src/core/entities.py` → `architecture.md` + `python.md` load
- Edit `frontend/src/App.tsx` → `frontend.md` loads
- Edit `tests/test_user.py` → `testing.md` + `python.md` load

### Custom Commands

```bash
# In Claude Code chat
/commit Generate commit message for staged changes
```

### Using Skills

Skills are referenced in agent frontmatter:
```yaml
skills:
  - clean-architecture
  - python-conventions
```

## Validation

Test Claude Code setup:

```bash
# Verify structure
ls -la .claude/agents/ .claude/rules/ .claude/commands/ .claude/skills/ .claude/hooks/

# Test hooks are executable
ls -la .claude/hooks/*.sh .claude/hooks/*.ps1

# Validate settings
cat .claude/settings.json | jq .

# Run pre-commit
uvx pre-commit run --all-files
```

## Maintenance

### Adding Agents

1. Create `.claude/agents/<name>.md` with frontmatter:
```yaml
---
name: agent-name
description: What this agent does
model: opus | sonnet | haiku
tools: [Read, Write, Edit, Bash, Grep, Glob]
permissionMode: ask | plan | execute
effort: low | medium | high | xhigh
maxTurns: 20
skills: [skill-1, skill-2]
---
```
2. Add to template: `template/.claude/agents/<name>.md`

### Adding Rules

1. Create `.claude/rules/<name>.md` with frontmatter:
```yaml
---
paths:
  - "path/pattern/**/*.ext"
---
```
2. Add to template: `template/.claude/rules/<name>.md`

### Adding Skills

1. Create `.claude/skills/<name>/SKILL.md`
2. Add to template: `template/.claude/skills/<name>/`
3. Reference in agent frontmatter: `skills: [new-skill]`

## Best Practices

### Agent Selection

- **Architecture changes** → `@architect`
- **Backend features** → `@backend-engineer`
- **Frontend features** → `@frontend-engineer`
- **Test coverage** → `@testing-specialist` or `@tdd`
- **Code review** → `@code-reviewer`
- **Debugging** → `@debug`
- **Refactoring** → `@refactorer`
- **Research** → `@researcher`
- **Complex reasoning** → `@deep-thinking`
- **Infrastructure** → `@devops`

### Rule Organization

- **Domain-specific** → `architecture.md`, `ddd.md`
- **Language-specific** → `python.md`, `frontend.md`
- **Process-specific** → `testing.md`, `commit.md`, `docs-sync.md`
- **Tool-specific** → `shell.md`

### Hook Safety

- Always test hooks in isolation before adding to settings
- Use explicit paths in hook commands
- Set appropriate timeouts (10-15s max)
- Exit 0 for non-blocking hooks
- Exit 1 for blocking hooks (security)

### Skill Composition

- Keep skills focused (single responsibility)
- Reference other skills instead of duplicating
- Use clear file structure (`SKILL.md` + supporting files)
- Document prerequisites and usage examples

## Troubleshooting

### Agent Not Loading

- Check frontmatter syntax (YAML)
- Verify name matches filename
- Check model is valid: opus, sonnet, haiku

### Rule Not Applying

- Verify path pattern matches file
- Check YAML frontmatter syntax
- Test with `ls -1 <path-pattern>`

### Hook Not Executing

- Check executable bit: `chmod +x .claude/hooks/*.sh`
- Verify command path exists
- Check timeout is sufficient
- Review Claude Code logs

### MCP Server Issues

- Verify `.claude/mcp.json` and `.vscode/mcp.json` syntax
- Check server is running: `npx shadcn@latest mcp --version`
- Review `enableAllProjectMcpServers: true` in settings.json

## Resources

- [Claude Code Docs](https://docs.anthropic.com/claude-code)
- [Agent Frontmatter Schema](https://json.schemastore.org/claude-code-agent.json)
- [Settings Schema](https://json.schemastore.org/claude-code-settings.json)
- [MCP Docs](https://modelcontextprotocol.org)
- [Template Docs](../docs/)

## See Also

- [.github/copilot-instructions.md](../.github/copilot-instructions.md) — GitHub Copilot config
- [.coderabbit.yaml](../.coderabbit.yaml) — CodeRabbit review config
- [.pre-commit-config.yaml](../.pre-commit-config.yaml) — Pre-commit hooks
- [docs/comprehensive-root-configuration.md](../docs/comprehensive-root-configuration.md) — Full setup guide

---

**Status**: ✅ Production-Ready
**Last Updated**: 2026-06-25
**Maintained By**: copier-fullstack-template team
