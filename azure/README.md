# Azure folder policy

Azure runtime IaC assets for generated projects should live in generated-repo
`azure/` (or `infra/` depending on profile) folders.

Template source lives under `template/{% if cloud_provider == 'azure' %}infra{% endif %}/`.

Primary Azure template sources:

- `template/{% if cloud_provider == 'azure' %}infra{% endif %}/deploy.bicep.jinja`
- `template/{% if cloud_provider == 'azure' %}infra{% endif %}/main.bicep.jinja`
- `template/{% if cloud_provider == 'azure' %}infra{% endif %}/modules/`
- `template/{% if cloud_provider == 'azure' %}infra{% endif %}/scripts/`