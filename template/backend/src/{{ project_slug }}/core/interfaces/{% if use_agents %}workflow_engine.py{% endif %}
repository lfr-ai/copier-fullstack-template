"""Workflow engine gateway."""

from __future__ import annotations

from collections.abc import AsyncIterator
from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable, final

DEFAULT_MAX_ITERATIONS = 25

DEFAULT_RECURSION_LIMIT = 50

DEFAULT_TIMEOUT_SECONDS = 300.0


@dataclass(frozen=True, slots=True)
@final
class WorkflowConfig:
    """Configuration passed to a workflow execution."""

    max_iterations: int = DEFAULT_MAX_ITERATIONS
    recursion_limit: int = DEFAULT_RECURSION_LIMIT
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS
    checkpoint_id: str = ""
    thread_id: str = ""
    interrupt_before: list[str] = field(default_factory=list)
    interrupt_after: list[str] = field(default_factory=list)
    extra: dict[str, object] = field(default_factory=dict)


@dataclass(slots=True)
@final
class WorkflowResult:
    """Result from a workflow execution."""

    answer: str = ""
    final_state: dict[str, object] = field(default_factory=dict)
    trace: list[dict[str, object]] = field(default_factory=list)
    total_steps: int = 0
    total_tokens: dict[str, int] = field(default_factory=dict)
    success: bool = True
    error: str = ""


@dataclass(frozen=True, slots=True)
@final
class WorkflowStreamEvent:
    """Single event emitted during workflow streaming."""

    node: str = ""
    event_type: str = ""
    data: dict[str, object] = field(default_factory=dict)
    step_index: int = 0


@runtime_checkable
class WorkflowEngineGateway(Protocol):
    """Gateway for workflow engines that execute agent graphs.

    Supports both batch and streaming execution modes,
    with optional checkpointing for durable execution.
    """

    async def execute(
        self,
        *,
        goal: str,
        initial_state: dict[str, object] | None = None,
        config: WorkflowConfig | None = None,
    ) -> WorkflowResult:
        """Execute a workflow to completion."""
        ...

    async def stream(
        self,
        *,
        goal: str,
        initial_state: dict[str, object] | None = None,
        config: WorkflowConfig | None = None,
    ) -> AsyncIterator[WorkflowStreamEvent]:
        """Stream workflow execution events."""
        ...

    async def resume(
        self,
        *,
        checkpoint_id: str,
        input_data: dict[str, object] | None = None,
    ) -> WorkflowResult:
        """Resume a paused workflow from a checkpoint (human-in-the-loop)."""
        ...

    async def get_state(self, *, thread_id: str) -> dict[str, object]:
        """Retrieve the current state of a workflow thread."""
        ...
