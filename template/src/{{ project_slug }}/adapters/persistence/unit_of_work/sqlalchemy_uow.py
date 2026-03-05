"""SQLAlchemy Unit of Work implementation."""

from __future__ import annotations

import logging

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


logger = logging.getLogger(__name__)


class SQLAlchemyUnitOfWork:
    """SQLAlchemy-based Unit of Work.

    Manages transactional boundaries using async sessions
    with automatic rollback on errors.
    """

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        """Initialize unit of work with session factory.

        Args:
            session_factory: Factory for creating async sessions.
        """
        self._session_factory = session_factory
        self._session: AsyncSession | None = None

    @property
    def session(self) -> AsyncSession:
        """Get current session, raising if not in context.

        Returns:
            Active async session.

        Raises:
            RuntimeError: If not within async context manager.
        """
        if self._session is None:
            raise RuntimeError("UnitOfWork not entered; use async with")
        return self._session

    async def __aenter__(self) -> SQLAlchemyUnitOfWork:
        """Enter transactional context."""
        self._session = self._session_factory()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object,
    ) -> None:
        """Exit transactional context with auto rollback on error."""
        if exc_type is not None:
            await self.rollback()
            logger.warning("Transaction rolled back due to %s", exc_type.__name__)
        if self._session is not None:
            await self._session.close()
            self._session = None

    async def commit(self) -> None:
        """Commit current transaction."""
        await self.session.commit()

    async def rollback(self) -> None:
        """Rollback current transaction."""
        await self.session.rollback()
