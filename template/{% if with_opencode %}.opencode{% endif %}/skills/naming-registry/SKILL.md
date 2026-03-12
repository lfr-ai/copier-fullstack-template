---
name: naming-registry
description: Manages the naming registry workflow for generating Python and TypeScript constants from naming_registry.json
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: codegen
---

## What I do

- Guide updates to `registry/naming_registry.json`
- Validate registry structure against JSON Schema
- Generate Python constants → `backend/src/<project>/core/registry_constants.py`
- Generate TypeScript constants → `frontend/src/registryConstants.ts`
- Generate env ports → `.env.ports`

## Workflow

1. Edit `registry/naming_registry.json` with new or updated entries
2. Run `task registry:validate` to check JSON structure
3. Run `task registry:generate` to regenerate all constant files
4. Run `task registry:check` to verify generated files are up-to-date (CI gate)
5. Run `task registry:test` to execute registry tests

## Rules

- NEVER hand-edit generated files — always edit naming_registry.json
- NEVER hardcode field/column names — use registry constants
- All new fields, routes, ports, and enum values go in the registry
- The `--check` flag is a CI gate: fails if generated files are stale

## Registry Structure

```json
{
  "services": { "name": "...", "port": ... },
  "routes": { "/path": { "method": "...", "description": "..." } },
  "enums": { "EnumName": ["value1", "value2"] },
  "fields": { "field_name": { "type": "...", "column": "..." } }
}
```

## When to use me

Use this skill when:
- Adding new API routes or endpoints
- Adding new database fields or columns
- Creating new enum types
- Updating shared identifiers between backend and frontend
