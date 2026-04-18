# Feature: template scaffolding

## Purpose and scope

Defines the Copier template contract, prompts, defaults, and post-generation flow used
to produce fullstack projects.

## Analyzed files

- `copier.yml` (template contract and prompt graph)
- `template/` (rendered scaffold source)
- `template/README.md.jinja` (consumer-facing generated docs)

## Business rules and constraints

- Copier v9+ is required (`copier.yml:1`).
- Template source is rooted at `template/` (`copier.yml:2`).
- Project identity and platform choices are captured as prompted fields
  (`copier.yml:23`, `copier.yml:64`, `copier.yml:73`).
- Post-copy tasks initialize git and make the initial commit (`copier.yml:324`).

## Workflows (with code references)

1. User runs `copier copy`.
2. Prompt flow resolves metadata and technology toggles.
3. Jinja renders files under `template/`.
4. Post-generation tasks run (`copier.yml:324`).

## Data models and dependencies

- Data model is the Copier answer map (`project_name`, `project_slug`, flags, etc.).
- Jinja templates depend on variables declared in `copier.yml`.

## Integrations

- Copier runtime (`uvx copier copy/update`).
- Git initialization and initial commit in post tasks.

## API endpoints or UI components

Not applicable at template-root level. Endpoints/components are generated artifacts.

## Security and authorization

- Template excludes VCS internals and cache files from rendering.
- `.env` style runtime files are skipped/preserved by Copier rules.
