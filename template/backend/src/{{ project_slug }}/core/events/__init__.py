"""Domain event definitions.

Domain events (UserCreated, etc.) are published by application services
via :class:`~core.interfaces.event_bus.EventBus`.
Wire concrete handlers via the DI container in 'composition/container.py'.
"""
