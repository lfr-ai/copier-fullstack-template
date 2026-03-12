"""AI module configuration — model settings, provider defaults, etc."""

from __future__ import annotations

from typing import Final

__all__ = [
    "DEFAULT_MAX_TOKENS",
    "DEFAULT_TEMPERATURE",
    "MAX_PROMPT_LENGTH",
    "MAX_SYSTEM_PROMPT_LENGTH",
    "MAX_TOKEN_LIMIT",
]


DEFAULT_MAX_TOKENS: Final[int] = 1024
"""Default maximum tokens in a completion response."""

MAX_TOKEN_LIMIT: Final[int] = 128_000
"""Hard upper bound for max_tokens across all providers."""

MAX_PROMPT_LENGTH: Final[int] = 32_000
"""Maximum character length for user prompts."""

MAX_SYSTEM_PROMPT_LENGTH: Final[int] = 8_000
"""Maximum character length for system prompts."""


DEFAULT_TEMPERATURE: Final[float] = 0.7
"""Default sampling temperature for completions."""
