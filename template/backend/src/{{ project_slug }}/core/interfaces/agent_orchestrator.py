"""Agent orchestrator gateway -- abstract interface for multi-agent workflow engines.

Concrete adapters may use LangGraph, CrewAI,
AutoGen, or custom orchestration implementations.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable, final


@dataclass(slots=True)
@final
class AgentState:
    """Shared state passed between agents in a workflow."""

    messages: list[dict[str, str]] = field(default_factory=list)
    context: dict[str, object] = field(default_factory=dict)
    current_agent: str = ""
    iteration: int = 0


@dataclass(frozen=True, slots=True)
@final
class OrchestratorResult:
    """Result from a multi-agent orchestration run."""

    answer: str
    final_state: AgentState
    agent_trace: list[dict[str, object]] = field(default_factory=list)
    total_steps: int = 0
    success: bool = True


@runtime_checkable
class AgentOrchestratorGateway(Protocol):
    """Gateway for multi-agent workflow orchestration.

    Adapters implement stateful, graph-based agent pipelines
    with durable execution, human-in-the-loop, and memory.
    """

    async def run(
        self,
        *,
        goal: str,
        state: AgentState | None = None,
        config: dict[str, object] | None = None,
    ) -> OrchestratorResult:
        """Execute a multi-agent workflow."""
        ...

    async def stream(
        self,
        *,
        goal: str,
        state: AgentState | None = None,
        config: dict[str, object] | None = None,
    ) -> AsyncIterator[dict[str, object]]:
        """Stream agent execution steps as they happen.

        Yields:
            Execution step dicts with agent name, action, and output.
        """
        ...
