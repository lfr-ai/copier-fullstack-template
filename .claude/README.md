# Claude Code Quick Reference

**Project**: copier-fullstack-template

## Quick Stats

- **Agents**: 13 specialized agents
- **Rules**: 14 path-scoped rules
- **Commands**: 1 custom command
- **Skills**: 9 reusable skills
- **Hooks**: 4 hooks (8 script files across `.sh` + `.ps1`)
- **Plugins**: 15 enabled
- **MCP Servers**: 3 (`context7`, `shadcn`, `gitnexus`)

## Directory Structure

```text
.claude/
├── settings.json         # Main configuration
├── settings.local.json   # Local overrides (gitignored)
├── agents/               # 13 specialized agents
├── rules/                # 14 path-scoped rules
├── commands/             # 1 custom command
├── skills/               # 9 reusable skills
├── hooks/                # 4 hooks, each with .sh + .ps1 variants
├── CLAUDE.md             # Full documentation
└── README.md             # This file
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

## Agents Overview

| Agent | Purpose | Use When |
| ----- | ------- | -------- |
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
| ---- | ---------- | -------- |
| architecture | `backend/src/**/*.py` | Clean Architecture boundaries |
| cognitive-load | `**/*.py` | Readability and low cognitive complexity |
| ddd | `template/backend/src/**/core/**/*.py` | Domain-driven design boundaries |
| python | `**/*.py` | Python conventions, type hints |
| python-conventions | `**/*.py` | Python conventions alias and portability |
| frontend | `frontend/src/**/*` | React/TypeScript rules |
| prompt | `**/*.prompt.md` | Prompt authoring conventions |
| registry | `template/**/*registry*` | Registry-first naming contracts |
| sdd | `docs/**/*.md`, `template/openspec/**` | Spec-driven development workflow |
| tdd | `template/backend/tests/**/*.py` | Test-driven workflow guardrails |
| testing | `**/tests/**/*` | Test conventions, markers |
| shell | `**/*.sh`, `**/*.ps1` | Shell script standards |
| commit | Commit messages | Conventional Commits |
| docs-sync | Code changes | Keep docs updated |

## Skills Overview

| Skill | Domain | Contents |
| ----- | ------ | -------- |
| clean-architecture | Architecture | Dependency Rule, layer boundaries |
| ddd | Domain modeling | Aggregates, invariants, ubiquitous language |
| python-conventions | Python | Type hints, docstrings, patterns |
| quality-gate | Validation | Lint, tests, pre-commit, render checks |
| sdd | Spec-driven | Requirement/design/task traceability |
| tdd | Test-driven | Red-green-refactor workflow |
| testing-conventions | Testing | Markers, factories, coverage |
| naming-registry | Patterns | Registry-first constants |
| frontend-react-stack | Frontend | React + TypeScript + shadcn/ui |

## Hooks Overview

| Hook | Type | Purpose |
| ---- | ---- | ------- |
| guard-destructive | PreToolUse | Block dangerous commands |
| guard-tool | PreToolUse | Tool-specific guards |
| stop-uncommitted-reminder | Stop | Warn about uncommitted work |
| check-licenses | Stop | License compatibility check |
| [auto-lint] | PostToolUse | Lint Python files (ruff) |

## Resources

- [Full Claude configuration](./CLAUDE.md)
- [Template docs](../docs/)
- [GitHub Copilot instructions](../.github/copilot-instructions.md)

---

**Status**: ✅ Complete
**Last Updated**: 2026-06-10
