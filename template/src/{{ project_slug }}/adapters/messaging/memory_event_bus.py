"""In-memory event bus for development and testing."""

from __future__ import annotations

import logging
from collections import defaultdict
from collections.abc import Callable, Coroutine


logger = logging.getLogger(__name__)

EventHandler = Callable[..., Coroutine[object, object, None]]


class MemoryEventBus:
    """In-memory event bus implementing EventBus protocol.

    Dispatches events to registered async handlers.
    Suitable for development and single-process deployments.
    """

    def __init__(self) -> None:
        """Initialize empty event bus."""
        self._handlers: dict[str, list[EventHandler]] = defaultdict(list)

    async def publish(self, event_type: str, payload: object) -> None:
        """Publish event to all registered handlers.

        Args:
            event_type: Event type identifier.
            payload: Event payload data.
        """
        handlers = self._handlers.get(event_type, [])
        logger.debug(
            "Publishing event %s to %d handlers",
            event_type,
            len(handlers),
        )
        for handler in handlers:
            try:
                await handler(payload)
            except Exception:
                logger.exception(
                    "Handler failed for event %s",
                    event_type,
                )

    def subscribe(self, event_type: str, handler: EventHandler) -> None:
        """Register handler for event type.

        Args:
            event_type: Event type to listen for.
            handler: Async callable to invoke on event.
        """
        self._handlers[event_type].append(handler)
        logger.debug("Subscribed handler for %s", event_type)
