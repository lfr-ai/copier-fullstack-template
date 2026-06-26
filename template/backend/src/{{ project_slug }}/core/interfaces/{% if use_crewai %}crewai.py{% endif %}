"""CrewAI orchestration interfaces.

Defines application-facing ports for CrewAI orchestration components so the
application layer depends on protocols instead of concrete adapter modules.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class CrewOrchestrationSupervisor(Protocol):
    """Protocol for HMAS-style goal orchestration supervisors."""

    async def orchestrate(self, goal: str) -> str:
        """Decompose and execute a high-level goal."""
        ...


@runtime_checkable
class CrewFlowRegistry(Protocol):
    """Protocol for CrewAI flow registries/executors."""

    async def run(
        self,
        flow_name: str,
        *,
        inputs: dict[str, object] | None = None,
    ) -> object:
        """Execute a named flow and return a flow result object."""
        ...
