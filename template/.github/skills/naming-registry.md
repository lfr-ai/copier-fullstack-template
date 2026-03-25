# Skill: Naming Registry

## Purpose

Treat `registry/naming_registry.json` as the single source of truth for shared constants.

## Use This Skill When

- Adding routes, fields, enum values, service ports
- Synchronizing backend/frontend shared identifiers
- Reviewing generated-constants drift in CI

## Rules

- Never edit generated constants by hand
- Update registry first, then regenerate
- Use registry constants in code (no hardcoded identifiers)
- CI check must pass with generated outputs up to date

## Workflow

1. Edit `registry/naming_registry.json`
2. Run `task registry:validate`
3. Run `task registry:generate`
4. Run `task registry:check`
5. Run `task registry:test`
