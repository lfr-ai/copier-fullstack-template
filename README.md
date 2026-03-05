# Copier Fullstack Template

Production-ready project scaffolding for Python, TypeScript, and hybrid applications.

## Usage

```bash
uvx copier copy --trust gh:your-org/copier-fullstack-template my-project
```

## Project Styles

- **backend** — Python API service with clean architecture
- **frontend** — TypeScript SPA with Vite
- **hybrid** — Full-stack with backend + frontend
- **library** — Python package with minimal structure

## Features

- Clean Architecture (domain, application, infrastructure, presentation)
- FastAPI or Flask backend with Pydantic v2
- Lit, React, Svelte, or Vanilla frontend with Vite
- PostgreSQL, SQLite, or MySQL with SQLAlchemy 2.0
- Redis + Celery for async task processing
- AI/LLM provider abstraction (OpenAI, Anthropic, Azure OpenAI, Ollama)
- MCP (Model Context Protocol) server
- Centralized naming registry with code generation
- Docker Compose with Caddy reverse proxy
- DevContainer for reproducible development
- GitHub Actions, GitLab CI, or Azure Pipelines
- Pre-commit hooks, Ruff, ESLint, Prettier
- Comprehensive testing with pytest, Vitest, Playwright
- Full documentation and onboarding guides
