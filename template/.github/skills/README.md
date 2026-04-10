# Skills Index

This folder contains reusable Copilot skill packs included in generated projects.

## Available skills

- `clean-architecture/` — enforce dependency boundaries and layer direction.
- `frontend-react-stack/` — frontend stack conventions and implementation guidance.
- `naming-registry/` — shared names/constants from `registry/naming_registry.json`.
- `python-conventions/` — Python typing, logging, and coding standards.
- `testing-conventions/` — test structure, markers, and coverage expectations.

## Maintenance rules

- Keep this list aligned with actual subfolders.
- Do not keep legacy skill paths after migrations.
- Update `Taskfile.yml` alignment checks if skill names change.
# Skills Index

This folder contains reusable Copilot skill packs included in generated projects.

## Available skills

- `clean-architecture/` — enforce dependency boundaries and layer direction.
- `frontend-react-stack/` — frontend stack conventions and implementation guidance.
- `naming-registry/` — shared names/constants from `registry/naming_registry.json`.
- `python-conventions/` — Python typing, logging, and coding standards.
- `testing-conventions/` — test structure, markers, and coverage expectations.

## Maintenance rules

- Keep this list aligned with actual subfolders.
- Do not keep legacy skill paths after migrations.
- Update `Taskfile.yml` alignment checks if skill names change.
# Skills

This directory contains **Skill Packs** — deep domain knowledge that agents reference
when working on specific topics.

Each skill is a directory containing a `SKILL.md` file. This structure allows VS Code
Copilot to discover skills automatically and attach supplementary resources (examples,
templates, schemas) alongside the skill definition.

## Available Skills

| Skill | Path | Domain |
|-------|------|--------|
| **Clean Architecture** | `clean-architecture/SKILL.md` | Layer boundaries, dependency rules, DI patterns |
| **Python Conventions** | `python-conventions/SKILL.md` | Type hints, dataclasses, enums, logging, constants |
| **Testing Conventions** | `testing-conventions/SKILL.md` | Pytest patterns, fixtures, hypothesis, naming |
| **Naming Registry** | `naming-registry/SKILL.md` | Registry-first constant generation workflow |

## How Skills Work

Skills are referenced by agents in their instructions. When an agent encounters a
task in a skill's domain, it reads the `SKILL.md` file for authoritative guidance.

Skills are NOT applied automatically — they are pulled on demand by agents that
need them.

## Adding a New Skill

1. Create a new directory: `.github/skills/<skill-name>/`
2. Add a `SKILL.md` file with the skill documentation
3. Optionally add supplementary files (examples, schemas) in the same directory
4. Update this README table
5. Reference the skill in relevant agent `.agent.md` files# Skills

This directory contains **Skill Packs** — deep domain knowledge that agents reference
when working on specific topics.

Each skill is a directory containing a `SKILL.md` file. This structure allows VS Code
Copilot to discover skills automatically and attach supplementary resources (examples,
templates, schemas) alongside the skill definition.

## Available Skills

| Skill | Path | Domain |
|-------|------|--------|
| **Clean Architecture** | `clean-architecture/SKILL.md` | Layer boundaries, dependency rules, DI patterns |
| **Python Conventions** | `python-conventions/SKILL.md` | Type hints, dataclasses, enums, logging, constants |
| **Testing Conventions** | `testing-conventions/SKILL.md` | Pytest patterns, fixtures, hypothesis, naming |
| **Naming Registry** | `naming-registry/SKILL.md` | Registry-first constant generation workflow |
| **Frontend React Stack** | `frontend-react-stack/SKILL.md` | React + TypeScript + Router + shadcn/ui standards |

## How Skills Work

Skills are referenced by agents in their instructions. When an agent encounters a
task in a skill's domain, it reads the `SKILL.md` file for authoritative guidance.

Skills are NOT applied automatically — they are pulled on demand by agents that
need them.

## Adding a New Skill

1. Create a new directory: `.github/skills/<skill-name>/`
2. Add a `SKILL.md` file with the skill documentation
3. Optionally add supplementary files (examples, schemas) in the same directory
4. Update this README table
5. Reference the skill in relevant agent `.agent.md` files
