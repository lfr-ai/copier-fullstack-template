"""Mock builder.

Builder for creating configured mock objects.
"""

from collections.abc import Callable
from unittest.mock import MagicMock, Mock


class MockBuilder:
    """Builder for creating configured mock objects.

    Example::

        mock = (
            MockBuilder(spec=UserRepository)
            .with_method("find_by_id", return_value=user)
            .with_attribute("connected", True)
            .build()
        )
    """

    def __init__(self, spec: type | None = None) -> None:
        self._spec = spec
        self._attributes: dict[str, object] = {}
        self._methods: dict[str, Callable[..., object]] = {}
        self._properties: dict[str, object] = {}
        self._side_effects: dict[str, Exception] = {}

    def with_attribute(self, name: str, value: object) -> MockBuilder:
        """Add attribute to mock."""
        self._attributes[name] = value
        return self

    def with_method(
        self,
        name: str,
        return_value: object | None = None,
        side_effect: Exception | None = None,
    ) -> MockBuilder:
        """Add method to mock.

        Args:
            return_value (object): Method return value.
            side_effect (Exception | None): Exception to raise.
        """
        if side_effect:
            self._side_effects[name] = side_effect
        else:
            self._methods[name] = lambda *args, **kwargs: return_value
        return self

    def with_property(self, name: str, value: object) -> MockBuilder:
        """Add property to mock."""
        self._properties[name] = value
        return self

    def build(self) -> Mock:
        """Build configured mock."""
        mock = Mock(spec=self._spec) if self._spec else MagicMock()

        for name, value in self._attributes.items():
            setattr(mock, name, value)

        for name, func in self._methods.items():
            method_mock = Mock(side_effect=func)
            setattr(mock, name, method_mock)

        for name, exception in self._side_effects.items():
            method_mock = Mock(side_effect=exception)
            setattr(mock, name, method_mock)

        for name, value in self._properties.items():
            setattr(type(mock), name, _PropertyMock(return_value=value))

        return mock


class _PropertyMock:
    """Mock property descriptor."""

    def __init__(self, return_value: object) -> None:
        self._return_value = return_value

    def __get__(self, instance: object, owner: type) -> object:
        return self._return_value
