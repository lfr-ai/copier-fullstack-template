"""Base Specification pattern for composable business rule evaluation.

Specifications encapsulate a single business rule as a predicate and
can be combined with '&' (and), '|' (or), and '~' (not) operators,
allowing complex domain rules to be built from simple, testable pieces.

Example::

    active_spec = IsActiveUser()
    valid_email = HasEmailDomain("example.com")
    combined = active_spec & valid_email

    if combined.is_satisfied_by(user):
        ...
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, final

T = TypeVar("T")


class Specification(ABC, Generic[T]):
    """Abstract specification -- a predicate over domain objects."""

    @abstractmethod
    def is_satisfied_by(self, candidate: T) -> bool:
        """Return True if *candidate* satisfies this specification."""
        ...

    def __and__(self, other: Specification[T]) -> AndSpecification[T]:
        return AndSpecification(self, other)

    def __or__(self, other: Specification[T]) -> OrSpecification[T]:
        return OrSpecification(self, other)

    def __invert__(self) -> NotSpecification[T]:
        return NotSpecification(self)


@final
class AndSpecification(Specification[T]):
    """Composite: both specifications must be satisfied."""

    def __init__(self, left: Specification[T], right: Specification[T]) -> None:
        self._left = left
        self._right = right

    def is_satisfied_by(self, candidate: T) -> bool:
        return self._left.is_satisfied_by(candidate) and self._right.is_satisfied_by(
            candidate,
        )


@final
class OrSpecification(Specification[T]):
    """Composite: at least one specification must be satisfied."""

    def __init__(self, left: Specification[T], right: Specification[T]) -> None:
        self._left = left
        self._right = right

    def is_satisfied_by(self, candidate: T) -> bool:
        return self._left.is_satisfied_by(candidate) or self._right.is_satisfied_by(
            candidate,
        )


@final
class NotSpecification(Specification[T]):
    """Composite: negation of a specification."""

    def __init__(self, spec: Specification[T]) -> None:
        self._spec = spec

    def is_satisfied_by(self, candidate: T) -> bool:
        return not self._spec.is_satisfied_by(candidate)
