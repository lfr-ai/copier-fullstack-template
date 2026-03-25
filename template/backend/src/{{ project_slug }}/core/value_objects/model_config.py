"""Model configuration value object."""

from __future__ import annotations

from dataclasses import dataclass, field

DEFAULT_MAX_TOKENS = 1024
"""Default maximum tokens in a completion response."""

DEFAULT_TEMPERATURE = 0.7
"""Default sampling temperature for completions."""

DEFAULT_TOP_P = 1.0
"""Default top-p (nucleus sampling) value."""

DEFAULT_MAX_RETRIES = 3
"""Default maximum retry count for tool calls."""

DEFAULT_TIMEOUT_SECONDS = 30.0
"""Default timeout in seconds for tool calls."""


@dataclass(frozen=True, slots=True)
class ModelConfig:
    """Immutable configuration for an LLM provider."""

    provider: str = "openai"
    model: str = "gpt-4o"
    max_tokens: int = DEFAULT_MAX_TOKENS
    temperature: float = DEFAULT_TEMPERATURE
    top_p: float = DEFAULT_TOP_P
    endpoint: str = ""
    deployment: str = ""
    api_version: str = ""
    extra: dict[str, object] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class ToolConfig:
    """Immutable configuration for an AI tool binding."""

    name: str = ""
    description: str = ""
    parameters_schema: dict[str, object] = field(default_factory=dict)
    enabled: bool = True
    max_retries: int = DEFAULT_MAX_RETRIES
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS
