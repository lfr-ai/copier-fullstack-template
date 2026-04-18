# Codebase analysis index

This directory contains the feature-level modernization analysis for the template
repository and generated-project scaffolding.

## Technology stack

- Template engine: Copier + Jinja templates.
- Backend template: Python, FastAPI, Pydantic Settings, SQLAlchemy, Ruff.
- Frontend template: React + TypeScript + Vite + Biome.
- Quality automation: pre-commit + go-task + custom verification scripts.

## Architecture summary

- Repository is a template-source repo (not generated runtime app).
- Root contains template-dev governance and verification pipeline.
- `template/` contains generated project source.

## Feature catalog

- `features/template-scaffolding.md`
- `features/quality-gates-and-tooling.md`
- `features/backend-runtime-and-api-template.md`
- `features/frontend-template-toolchain.md`
- `features/agent-governance-and-instructions.md`

## Frontend and cross-cutting syntheses

- `frontend/README.md`
- `cross-cuttings/README.md`

## Notable modernization outcomes in this pass

- Standardized width to 88 across markdown, YAML, Python, and frontend tooling.
- Updated pre-commit baselines and moved expensive tests to `pre-push/manual`.
- Added FastAPI status-code convention checker script and task wiring.
- Strengthened instruction governance for internal naming and default minimization.
