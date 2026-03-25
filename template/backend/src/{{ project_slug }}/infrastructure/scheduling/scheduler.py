"""Task scheduler abstraction.

For production use, prefer Celery Beat or APScheduler.
"""

from __future__ import annotations

from collections.abc import Callable

import structlog

logger: structlog.stdlib.BoundLogger = structlog.get_logger(__name__)


class Scheduler:
    """Minimal in-process scheduler for development.

    In production, use Celery Beat or a dedicated scheduling service.
    """

    __slots__ = ("_tasks",)

    def __init__(self) -> None:
        self._tasks: dict[str, dict[str, Callable[..., object] | int]] = {}

    def register(
        self, name: str, func: Callable[..., object], *, interval_seconds: int
    ) -> None:
        """Register a periodic task.

        Args:
            name (str): Unique task identifier.
            func (Callable[..., object]): Callable to execute.
            interval_seconds (int): Execution interval in seconds.
        """
        self._tasks[name] = {"func": func, "interval": interval_seconds}
        logger.info("Registered scheduled task: %s (every %ss)", name, interval_seconds)

    def list_tasks(self) -> list[str]:
        """Names of all registered tasks."""
        return list(self._tasks)
