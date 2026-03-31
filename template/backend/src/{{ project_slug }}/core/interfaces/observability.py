"""Observability gateway — abstract interface for AI tracing and telemetry.

Concrete adapters may use LangSmith, OpenTelemetry, Phoenix (Arize),
or custom tracing backends.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable


@dataclass(slots=True)
class TraceSpan:
    """Single span in an AI execution trace."""

    name: str
    span_type: str = "generic"
    input_data: dict[str, object] = field(default_factory=dict)
    output_data: dict[str, object] = field(default_factory=dict)
    metadata: dict[str, object] = field(default_factory=dict)
    duration_ms: float = 0.0
    error: str | None = None


@runtime_checkable
class ObservabilityGateway(Protocol):
    """Gateway for AI execution tracing and telemetry."""

    async def start_trace(
        self,
        *,
        name: str,
        metadata: dict[str, object] | None = None,
    ) -> str:
        """Start a new execution trace and return its correlation ID."""
        ...

    async def log_span(
        self,
        *,
        trace_id: str,
        span: TraceSpan,
    ) -> None:
        """Log a span within an active trace."""
        ...

    async def end_trace(
        self,
        *,
        trace_id: str,
        metadata: dict[str, object] | None = None,
    ) -> None:
        """End an active trace."""
        ...
