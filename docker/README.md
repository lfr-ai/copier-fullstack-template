# Docker folder policy

Runtime Docker assets for generated projects should live in generated-repo
`docker/` folders, not as loose files in repository root.

In this template repository, canonical source templates are under `template/`.

Primary Docker template sources:

- `template/Containerfile.jinja`
- `template/compose.yml.jinja`
- `template/compose.dev.yml.jinja`
- `template/compose.prod.yml.jinja`
- `template/docker/`