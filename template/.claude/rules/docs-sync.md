---
paths:
  - "**/*.{md,py,yml,yaml,toml,json,ts,tsx}"
---

# Documentation Sync

- Update relevant docs when setup, architecture, workflows, or commands change.
- Keep `.env.example`, `README.md`, `AGENTS.md`, and `CLAUDE.md` aligned with actual behavior.
- When adding environment variables, always add to `.env.example` with a descriptive comment.
- When modifying agent configs (`.claude/agents/`), update the corresponding agent
  table in `CLAUDE.md`.
- When adding new task commands to `Taskfile.yml`, add them to the commands section of `CLAUDE.md`.
- When adding new fields to `registry/naming_registry.json`, run `task registry:generate`
  and commit the generated constants alongside the registry change.
