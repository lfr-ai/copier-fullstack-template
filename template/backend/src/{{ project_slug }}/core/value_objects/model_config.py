"""Model configuration value object."""

from typing import final

from dataclasses import dataclass, field

DEFAULT_MAX_TOKENS = 1024

DEFAULT_TEMPERATURE = 0.7

DEFAULT_TOP_P = 1.0

DEFAULT_MAX_RETRIES = 3

DEFAULT_TIMEOUT_SECONDS = 30.0


@dataclass(frozen=True, slots=True)
@final
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
@final
class ToolConfig:
    """Immutable configuration for an AI tool binding."""

    name: str = ""
    description: str = ""
    parameters_schema: dict[str, object] = field(default_factory=dict)
    enabled: bool = True
    max_retries: int = DEFAULT_MAX_RETRIES
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS
