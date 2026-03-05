"""Async utility functions."""

from __future__ import annotations

import asyncio
from collections.abc import Callable, Coroutine
from functools import wraps


def run_sync(coro: Coroutine[object, object, object]) -> object:
    """Run async coroutine synchronously.

    Creates new event loop if none is running.

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
        import concurrent.futures

        with concurrent.futures.ThreadPoolExecutor() as pool:
            future = pool.submit(asyncio.run, coro)
            return future.result()
    return asyncio.run(coro)


def async_to_sync(func: Callable[..., Coroutine[object, object, object]]) -> Callable[..., object]:
    """Decorator converting async function to sync.

    Args:
        func: Async function to wrap.

    Returns:
        Synchronous wrapper function.
    """

    @wraps(func)
    def wrapper(*args: object, **kwargs: object) -> object:
        return run_sync(func(*args, **kwargs))

    return wrapper
