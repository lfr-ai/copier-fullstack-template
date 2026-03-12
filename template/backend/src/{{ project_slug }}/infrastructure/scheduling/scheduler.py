"""Simple task scheduler abstraction.

For production use, prefer Celery Beat or APScheduler.
"""

from __future__ import annotations

from collections.abc import Callable

import structlog

__all__ = ["Scheduler"]

logger: structlog.stdlib.BoundLogger = structlog.get_logger(__name__)


class Scheduler:
    """Minimal in-process scheduler for development.

    In production, use Celery Beat or a dedicated scheduling service.
    """

    __slots__ = ("_tasks",)

    def __init__(self) -> None:
        """Initialize scheduler with empty task registry."""
        self._tasks: dict[str, dict[str, Callable[..., object] | int]] = {}

    def register(
        self, name: str, func: Callable[..., object], *, interval_seconds: int
    ) -> None:
        """Register a periodic task.

        Args:
            name (str): Unique task name.
            func (Callable[..., object]): Callable to execute on each interval.
            interval_seconds (int): Seconds between executions.
        """
        self._tasks[name] = {"func": func, "interval": interval_seconds}
        logger.info("Registered scheduled task: %s (every %ss)", name, interval_seconds)

    def list_tasks(self) -> list[str]:
        """Return names of all registered tasks.

        Returns:
            list[str]: Registered task names.
        """
        return list(self._tasks)
