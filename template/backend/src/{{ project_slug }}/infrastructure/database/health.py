"""Database health check utilities."""

from __future__ import annotations

import structlog
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

logger: structlog.stdlib.BoundLogger = structlog.get_logger(__name__)


async def check_database_health(session: AsyncSession) -> bool:
    """Check if the database is reachable and responding.

    Args:
        session (AsyncSession): Active SQLAlchemy async session.

    Returns:
        bool: 'True' if the database responds to a test query.
    """
    try:
        result = await session.execute(text("SELECT 1"))
        return result.scalar() == 1
    except Exception:  # noqa: BLE001 — intentional health-check fault barrier
        logger.warning("Database health check failed", exc_info=True)
        return False
