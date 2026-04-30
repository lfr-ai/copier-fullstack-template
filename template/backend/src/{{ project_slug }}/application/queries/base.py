"""Base query handler for CQRS read operations."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

QueryT = TypeVar("QueryT")
ResultT = TypeVar("ResultT")


class QueryHandler(ABC, Generic[QueryT, ResultT]):
    """Abstract base for query handlers.

    Implements CQRS read side without unit of work
    as reads should not modify state.
    """

    @abstractmethod
    async def handle(self, query: QueryT) -> ResultT:
        """Execute query and return result."""
        ...
