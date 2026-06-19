---
description: Domain-Driven Design guidance for domain and application layers
applyTo: "backend/src/**/*.py"
---

# DDD Instructions

- Keep business language in domain model names.
- Place invariants close to entities/value objects.
- Use application services for orchestration, not domain leakage from presentation.
- Use repositories/protocols for aggregate persistence boundaries.
- Prefer explicit domain events where cross-aggregate coordination is required.
