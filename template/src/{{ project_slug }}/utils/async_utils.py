"""Async utility functions."""

from __future__ import annotations

import asyncio
import concurrent.futures
from collections.abc import Callable, Coroutine
from functools import wraps
from typing import TypeVar

_T = TypeVar("_T")


def run_sync(coro: Coroutine[object, object, _T]) -> _T:
    """Run async coroutine synchronously.

    Creates new event loop if none is running. When called from
    within a running loop, executes in a thread pool.

    Args:
        coro: Coroutine to execute.

    Returns:
        Coroutine result.
    """
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        with concurrent.futures.ThreadPoolExecutor() as pool:
            future = pool.submit(asyncio.run, coro)
            return future.result()
    return asyncio.run(coro)


def async_to_sync(
    func: Callable[..., Coroutine[object, object, _T]],
) -> Callable[..., _T]:
    """Decorator converting async function to sync.

    Args:
        func: Async function to wrap.

    Returns:
        Synchronous wrapper function.
    """

    @wraps(func)
    def wrapper(*args: object, **kwargs: object) -> _T:
        return run_sync(func(*args, **kwargs))

    return wrapper
