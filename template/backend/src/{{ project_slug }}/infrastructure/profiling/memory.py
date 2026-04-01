"""Memory profiling via tracemalloc."""

from __future__ import annotations

import contextlib
import tracemalloc
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, final

import structlog

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

logger: structlog.stdlib.BoundLogger = structlog.get_logger(__name__)

_TRACEBACK_FRAME_LIMIT = 25
_BYTES_PER_KB = 1024
_BYTES_PER_MB = 1024 * 1024
_SIZE_DECIMAL_PLACES = 2
_PEAK_DECIMAL_PLACES = 3
_DEFAULT_PROFILE_TOP_N = 10


@dataclass(frozen=True, slots=True)
@final
class MemoryAllocation:
    """Single memory allocation entry."""

    file: str
    line: int
    size_kb: float


@dataclass(frozen=True, slots=True)
@final
class MemoryProfileResult:
    """Result of a memory profiling session."""

    label: str
    peak_mb: float
    current_mb: float
    top_allocations: list[MemoryAllocation] = field(default_factory=list)


@contextlib.asynccontextmanager
async def memory_snapshot(
    *,
    label: str = "adhoc",
    top_n: int = _DEFAULT_PROFILE_TOP_N,
) -> AsyncIterator[MemoryProfileResult]:
    """Async context manager that captures memory usage of the enclosed block.

    Uses 'tracemalloc' (stdlib) — works on all platforms including Windows.

    Yields:
        MemoryProfileResult: Populated after the 'with' block exits.
    """
    was_tracing = tracemalloc.is_tracing()
    if not was_tracing:
        tracemalloc.start(_TRACEBACK_FRAME_LIMIT)

    tracemalloc.clear_traces()

    result = MemoryProfileResult(label=label, peak_mb=0, current_mb=0)

    try:
        yield result
    finally:
        snapshot = tracemalloc.take_snapshot()
        current, peak = tracemalloc.get_traced_memory()

        stats = snapshot.statistics("lineno")[:top_n]
        allocations = [
            MemoryAllocation(
                file=s.traceback[0].filename if s.traceback else "<unknown>",
                line=s.traceback[0].lineno if s.traceback else 0,
                size_kb=round(s.size / _BYTES_PER_KB, _SIZE_DECIMAL_PLACES),
            )
            for s in stats
        ]

        object.__setattr__(
            result, "peak_mb", round(peak / _BYTES_PER_MB, _PEAK_DECIMAL_PLACES)
        )
        object.__setattr__(
            result, "current_mb", round(current / _BYTES_PER_MB, _PEAK_DECIMAL_PLACES)
        )
        object.__setattr__(result, "top_allocations", allocations)

        logger.info(
            "memory_profile_completed",
            label=label,
            peak_mb=result.peak_mb,
            current_mb=result.current_mb,
            top_allocation_count=len(allocations),
        )

        if not was_tracing:
            tracemalloc.stop()
