"""Timing / performance measurement utilities."""

from __future__ import annotations

import time
from collections.abc import Generator
from contextlib import contextmanager

import structlog

from {{ project_slug }}.config.constants import MS_PER_SECOND

__all__ = ["timed_block"]

logger: structlog.stdlib.BoundLogger = structlog.get_logger(__name__)


@contextmanager
def timed_block(label: str) -> Generator[None, None, None]:
    """Context manager that logs elapsed wall-clock time for a code block.

    Args:
        label (str): Descriptive name for the timed block.

    Yields:
        None: Control is returned to the caller inside the timed block.

    Usage::

        with timed_block("fetch_users"):
            users = await repo.list()
    """
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed_ms = (time.perf_counter() - start) * MS_PER_SECOND
        logger.debug("timed_block", label=label, elapsed_ms=round(elapsed_ms, 2))
