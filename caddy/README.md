# Caddy folder policy

Caddy runtime assets for generated projects should live in generated-repo
`caddy/` folders.

Template source lives under `template/{% if use_caddy %}caddy{% endif %}/`.

Primary Caddy template sources:

- `template/{% if use_caddy %}caddy{% endif %}/Caddyfile.jinja`
- `template/{% if use_caddy %}caddy{% endif %}/snippets/`
