# Feature: frontend template toolchain

## Purpose and scope

Defines generated frontend lint/format standards and React-focused quality defaults.

## Analyzed files

- `template/frontend/biome.json`
- `template/.editorconfig`
- `template/.pre-commit-config.yaml.jinja`

## Business rules and constraints

- Biome formatter line width is set to 88 (`template/frontend/biome.json:43`).
- Biome JavaScript quote style is single (`template/frontend/biome.json:48`).
- Key React safety checks remain active (`useExhaustiveDependencies`)
  (`template/frontend/biome.json:19`).
- `noExplicitAny` is error-level (`template/frontend/biome.json:22`).

## Workflows (with code references)

1. Local formatting/linting runs through Biome in hooks and tasks.
2. Frontend tests are staged to `pre-push/manual` for iterative onboarding
   (`template/.pre-commit-config.yaml.jinja:142`, `:148`).

## Data models and dependencies

- Biome config is JSON-based and deterministic.
- Frontend pre-commit uses Bun runtime for tool invocation.

## Integrations

- Bun package/runtime.
- Biome linter/formatter.
- React-focused lint domains enabled in Biome.

## API endpoints or UI components

Not defined in this file set; components and routes are in generated frontend source.

## Security and authorization

- Static quality checks reduce unsafe front-end patterns (`noExplicitAny`).
- Build artifacts and generated folders are ignored in formatter scope.
