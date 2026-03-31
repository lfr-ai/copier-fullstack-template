# GitHub Copilot Agent Skills

This folder contains focused agent skills for Copilot-driven workflows in this
repository. Each skill is a directory containing a `SKILL.md` file following the
[Agent Skills standard](https://agentskills.io/).

## Included Skills

| Skill                     | Description                                                                                    |
| ------------------------- | ---------------------------------------------------------------------------------------------- |
| `clean-architecture/`     | Enforce Clean Architecture boundaries, Dependency Rule, and UoW-with-repos pattern             |
| `python-conventions/`     | Enforce Python standards, typing, logging, and signatures                                      |
| `testing-conventions/`    | Apply test structure, markers, and coverage expectations                                       |
| `naming-registry/`        | Registry-first workflow for shared constants and CI checks                                     |

## How to Use

Skills are loaded automatically by VS Code when relevant to your task. You can
also invoke them explicitly as slash commands: type `/` in chat and select a skill.

When working on a task, apply skills in this order:

1. Architecture / Clean Architecture (`clean-architecture`)
2. Implementation (`python-conventions`)
3. Registry contract (`naming-registry`)
4. Verification (`testing-conventions`)

Global rules are loaded from:

- `.github/copilot-instructions.md`
- `AGENTS.md`
- `docs/conventions/*.md`
