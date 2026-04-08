"""CrewAI multi-agent orchestration integration.

Provides production-ready CrewAI Crews, Flows, and hierarchical
multi-agent systems (HMAS) with:

* **Agents** -- role-based agent construction from code or YAML
* **Tasks** -- structured task definitions with guardrails
* **Crews** -- collaborative agent teams (sequential/hierarchical)
* **Flows** -- event-driven, stateful workflow orchestration
* **HMAS** -- hierarchical supervisor that decomposes goals and
  delegates across CrewAI crews
* **Knowledge** -- embedder-aware knowledge sources (string, JSON, text, PDF)
* **Memory** -- unified memory with scoring presets and scoping
* **Tools** -- bridge application callables to CrewAI tool protocol
* **YAML Config** -- declarative agent/task definitions via YAML

Integrates cleanly with the existing Clean Architecture:
  'core/interfaces' -> 'ai/crewai' -> 'application/services'
"""

