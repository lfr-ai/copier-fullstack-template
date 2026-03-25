# GitHub Copilot Skill Packs

This folder contains focused skill playbooks for Copilot-driven workflows in this
repository.

## Included Skills

- `hexagonal-architecture.md` — enforce clean / hexagonal architecture boundaries,
  Dependency Rule, and UoW-with-repos pattern
- `python-conventions.md` — enforce Python standards, typing, logging, and signatures
- `testing-conventions.md` — apply test structure, markers, and coverage expectations
- `naming-registry.md` — registry-first workflow for shared constants and CI checks

## How to Use

When working on a task, load the matching skill first, then apply global rules from:

- `.github/copilot-instructions.md`
- `AGENTS.md`
- `docs/conventions/*.md`

If a task spans multiple domains (for example, feature + tests + registry), apply skills
in this order:

1. Architecture / Clean Architecture (`hexagonal-architecture.md`)
2. Implementation (`python-conventions.md`)
3. Registry contract (`naming-registry.md`)
4. Verification (`testing-conventions.md`)
