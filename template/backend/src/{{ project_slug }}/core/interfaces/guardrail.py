"""Guardrail gateway — abstract interface for AI safety guardrails.

Concrete adapters may use NeMo Guardrails, custom rule-based
validators, or LLM-based content moderation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable


@dataclass(frozen=True, slots=True)
class GuardrailResult:
    """Result from a guardrail validation check."""

    allowed: bool
    reason: str = ""
    modified_content: str | None = None
    violations: list[str] = field(default_factory=list)


@runtime_checkable
class GuardrailGateway(Protocol):
    """Gateway for AI input/output safety validation."""

    async def validate_input(
        self,
        *,
        content: str,
        context: dict[str, object] | None = None,
    ) -> GuardrailResult:
        """Validate user input before processing."""
        ...

    async def validate_output(
        self,
        *,
        content: str,
        original_input: str | None = None,
        context: dict[str, object] | None = None,
    ) -> GuardrailResult:
        """Validate AI output before returning to the user.

        The result may contain 'modified_content' with a sanitized version.
        """
        ...
