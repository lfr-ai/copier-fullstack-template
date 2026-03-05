"""Database session factory configuration."""

from __future__ import annotations

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


def create_engine(database_url: str, *, echo: bool = False) -> AsyncEngine:
    """Create async SQLAlchemy engine.

    Args:
        database_url: Database connection URL.
        echo: Enable SQL query logging.

    Returns:
        Configured async engine instance.
    """
    return create_async_engine(database_url, echo=echo, pool_pre_ping=True)


def create_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    """Create async session factory.

    Args:
        engine: Async SQLAlchemy engine.

    Returns:
        Session factory for creating database sessions.
    """
    return async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
