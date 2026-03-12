"""Base query handler for CQRS read operations."""

from __future__ import annotations

from abc import ABC, abstractmethod

__all__ = ["QueryHandler"]


class QueryHandler[QueryT, ResultT](ABC):
    """Abstract base for query handlers.

    Implements CQRS read side without unit of work
    as reads should not modify state.
    """

    @abstractmethod
    async def handle(self, query: QueryT) -> ResultT:
        """Execute query and return result.

        Args:
            query (QueryT): Query parameters.

        Returns:
            ResultT: Query result.
        """
        ...
