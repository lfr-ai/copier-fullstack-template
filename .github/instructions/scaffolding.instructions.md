---
description: Copier template scaffolding conventions and Jinja2 patterns
applyTo: '**/*.jinja'
---

- Templated files MUST use '.jinja' suffix: 'pyproject.toml.jinja', 'README.md.jinja'
- Conditionally included directories use Jinja2 in folder name:
  '{% if use_devcontainer %}.devcontainer{% endif %}/'
- Static files (no Jinja2 inside) do NOT need '.jinja' suffix

```jinja2
{# CORRECT: Spaces inside delimiters #}
{{ variable_name }}
{% if condition %}
{% for item in items %}

{# INCORRECT: No spaces (hard to read) #}
{{variable_name}}
{%if condition%}
```

- Access via '{{ variable_name }}' (e.g., '{{ project_name }}', '{{ project_slug }}')
- Copier config: '{{ _copier_conf.answers_file }}'
- Boolean checks: '{% if use_celery %}', '{% if use_redis %}'
- Choice checks: '{% if database_backend == 'postgresql' %}'
- Always provide sensible defaults in 'copier.yml'
- Validate required fields in 'copier.yml' with 'validator:'

```jinja2
{# Feature flags for optional sections #}
{% if use_celery %}
[project.optional-dependencies]
celery = ["celery[redis]>=5.4"]
{% endif %}

{# Cloud provider selection #}
{% if cloud_provider == 'azure' %}
azure-identity = ">=1.17"
{% endif %}
```

```
copier-fullstack-template/
├── copier.yml              # Template configuration and variables
├── template/               # _subdirectory: "template" in copier.yml
│   ├── backend/            # Python backend (FastAPI + Clean Architecture)
│   │   ├── src/{{ project_slug }}/
│   │   │   ├── core/       # Domain layer
│   │   │   ├── application/ # Use cases
│   │   │   ├── infrastructure/   # Infrastructure
│   │   │   ├── presentation/    # Presentation
│   │   │   ├── config/     # Settings, DI
│   │   │   └── utils/      # Shared utilities
│   │   ├── tests/
│   │   └── pyproject.toml.jinja
│   ├── frontend/           # TypeScript frontend (Vite)
│   │   ├── src/
│   │   └── package.json.jinja
│   ├── .github/            # CI/CD, Copilot instructions, prompts
│   ├── docs/               # Documentation
│   ├── scripts/            # Setup and utility scripts (.zsh)
│   ├── tasks/              # Taskfile includes
│   ├── registry/           # Naming registry + generator
│   └── compose.yml.jinja   # Container orchestration
```

For every layer directory:

- '__init__.py' with module-level docstring describing purpose and dependency rules
- '__all__' exports where the package exposes a public API
- Base class inheritance, type hints, docstrings on all scaffolded modules
- Correct layer placement per architecture rules

- '_tasks' in 'copier.yml' run after generation (e.g., 'git init')
- '_message_after_copy' shows setup instructions
- 'scripts/install/' handles toolchain setup
- 'scripts/bootstrap.zsh.jinja' is the single entry point for first-time setup

- After modifying a template: 'copier copy . /tmp/test-output'
- Verify no Jinja2 syntax errors, missing variables, or broken conditionals
