"""Fixture Factory.

Factory for creating test fixtures.
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class BaseFixtureFactory(ABC, Generic[T]):
    """Base fixture factory.

    Creates test data fixtures with auto-incrementing sequences
    and configurable defaults.
    """

    def __init__(self) -> None:
        self._counter = 0
        self._defaults: dict[str, object] = {}

    def set_defaults(self, **kwargs: object) -> None:
        """Set default values for fixtures.

        Args:
            **kwargs: Default field values.
        """
        self._defaults.update(kwargs)

    def create(self, **overrides: object) -> T:
        """Create fixture with optional overrides.

        Args:
            **overrides: Override values for specific fields.

        Returns:
            T: Test fixture instance.
        """
        self._counter += 1
        attrs = {**self._defaults, **overrides}
        return self._build(self._counter, attrs)

    @abstractmethod
    def _build(self, sequence: int, attrs: dict[str, object]) -> T:
        """Build fixture instance.

        Args:
            sequence: Sequence number for unique values.
            attrs: Attribute values.

        Returns:
            Fixture instance.
        """

    def create_batch(self, count: int, **overrides: object) -> list[T]:
        """Create multiple fixtures.

        Args:
            count: Number of fixtures to create.
            **overrides: Override values (applied to all instances).

        Returns:
            List of fixtures.
        """
        return [self.create(**overrides) for _ in range(count)]

    def reset(self) -> None:
        """Reset factory state."""
        self._counter = 0
        self._defaults = {}
