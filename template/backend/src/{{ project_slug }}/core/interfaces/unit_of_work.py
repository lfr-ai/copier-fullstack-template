"""Unit of Work protocol for transactional boundaries."""

from __future__ import annotations

from typing import Protocol, Self, runtime_checkable

__all__ = ["UnitOfWork"]


@runtime_checkable
class UnitOfWork(Protocol):
    """Unit of Work protocol for transactional boundaries."""

    async def __aenter__(self) -> Self:
        """Enter transactional context."""
        ...

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object,
    ) -> None:
        """Exit transactional context with auto rollback on error."""
        ...

    async def commit(self) -> None:
        """Commit current transaction."""
        ...

    async def rollback(self) -> None:
        """Rollback current transaction."""
        ...
