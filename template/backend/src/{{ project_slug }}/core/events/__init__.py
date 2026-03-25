"""Domain event definitions.

Domain events (UserCreated, DocumentIngested, etc.) are published by
application services via :class:`~core.interfaces.event_bus.EventBus`.
Wire concrete handlers via the DI container in 'ports/container.py'.
"""

from __future__ import annotations
