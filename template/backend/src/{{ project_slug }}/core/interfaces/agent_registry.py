"""Agent registry gateway — abstract interface for agent discovery and management."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable


@dataclass(frozen=True, slots=True)
class RegisteredAgent:
    """Registered agent entry in the registry."""

    agent_id: str
    name: str
    description: str
    url: str
    skills: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    is_local: bool = False
    metadata: dict[str, object] = field(default_factory=dict)


@runtime_checkable
class AgentRegistryGateway(Protocol):
    """Gateway for discovering, registering, and managing agents."""

    async def register(self, agent: RegisteredAgent) -> None:
        """Register an agent in the registry.

        Args:
            agent (RegisteredAgent): Agent information to register.
        """
        ...

    async def unregister(self, agent_id: str) -> None:
        """Remove an agent from the registry.

        Args:
            agent_id (str): Unique agent identifier.
        """
        ...

    async def discover(
        self, *, query: str | None = None, tags: list[str] | None = None
    ) -> list[RegisteredAgent]:
        """Discover agents matching search criteria.

        Args:
            query (str | None): Free-text search across name/description.
            tags (list[str] | None): Filter by skill tags.

        Returns:
            list[RegisteredAgent]: Matching registered agents.
        """
        ...

    async def get(self, agent_id: str) -> RegisteredAgent | None:
        """Get a specific agent by ID.

        Args:
            agent_id (str): Unique agent identifier.

        Returns:
            RegisteredAgent | None: Agent information or 'None' if not found.
        """
        ...

    async def list_all(self) -> list[RegisteredAgent]:
        """List all registered agents.

        Returns:
            list[RegisteredAgent]: All agents in the registry.
        """
        ...
