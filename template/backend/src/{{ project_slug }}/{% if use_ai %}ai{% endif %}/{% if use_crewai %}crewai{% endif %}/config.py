"""CrewAI configuration — constants and defaults for crew orchestration."""

from __future__ import annotations


# ── Crew defaults ───────────────────────────────────────────────────
DEFAULT_CREW_MAX_RPM = 30
"""Default max requests-per-minute for crew-level rate limiting."""

DEFAULT_CREW_VERBOSE = False
"""Default verbosity for crew execution logging."""

DEFAULT_MANAGER_MODEL = "gpt-4o"
"""LLM used by the hierarchical manager agent."""

DEFAULT_AGENT_MODEL = "gpt-4o-mini"
"""Default LLM for crew worker agents."""

DEFAULT_AGENT_MAX_ITER = 20
"""Maximum iterations per agent before forced response."""

DEFAULT_AGENT_MAX_RPM = None
"""Default per-agent RPM limit (None = use crew limit)."""

DEFAULT_GUARDRAIL_MAX_RETRIES = 3
"""Default max retries when a task guardrail fails."""

# ── HMAS defaults ───────────────────────────────────────────────────
HMAS_MAX_DEPTH = 3
"""Maximum nesting depth for hierarchical crew delegation."""
