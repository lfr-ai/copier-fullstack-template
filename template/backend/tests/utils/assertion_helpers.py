"""Assertion helpers.

Custom assertion utilities for tests.
"""

from collections.abc import Callable
from typing import Protocol


class _HasStatusCode(Protocol):
    """Protocol for objects with a numeric status_code attribute."""

    status_code: int


def assert_dict_subset(expected: dict[str, object], actual: dict[str, object]) -> None:
    """Assert that all key-value pairs in *expected* exist in *actual*.

    Args:
        expected (dict[str, object]): Subset of expected key-value pairs.
        actual (dict[str, object]): Full dictionary to check against.

    Raises:
        AssertionError: When any expected key is missing or has wrong value.
    """
    for key, value in expected.items():
        assert key in actual, f"Missing key: {key}"
        assert actual[key] == value, f"Key {key!r}: {actual[key]!r} != {value!r}"


def assert_status_ok(response: _HasStatusCode) -> None:
    """Assert an HTTP response has a 2xx status code.

    Args:
        response (_HasStatusCode): HTTPX or similar response object with 'status_code'.
    """
    assert 200 <= response.status_code < 300, (  # noqa: PLR2004
        f"Expected 2xx, got {response.status_code}"
    )


def assert_list_equal_unordered(
    actual: list[object],
    expected: list[object],
) -> None:
    """Assert lists contain same elements regardless of order.

    Args:
        actual (list[object]): Actual list.
        expected (list[object]): Expected list.

    Raises:
        AssertionError: If lists differ.
    """
    if len(actual) != len(expected):
        raise AssertionError(
            f"List length mismatch: expected {len(expected)}, got {len(actual)}"
        )

    actual_sorted = sorted(actual, key=str)
    expected_sorted = sorted(expected, key=str)

    if actual_sorted != expected_sorted:
        raise AssertionError(
            f"Lists differ: expected {expected_sorted}, got {actual_sorted}"
        )


def assert_raises_with_message(
    exception_class: type[Exception],
    message_substring: str,
    callable_obj: Callable[..., object],
    *args: object,
    **kwargs: object,
) -> None:
    """Assert function raises exception with specific message.

    Args:
        exception_class (type[Exception]): Expected exception class.
        message_substring (str): Substring expected in exception message.
        callable_obj (Callable[..., object]): Function to call.
        *args: Positional arguments for function.
        **kwargs: Keyword arguments for function.

    Raises:
        AssertionError: If exception not raised or message doesn't match.
    """
    try:
        callable_obj(*args, **kwargs)
        raise AssertionError(f"Expected {exception_class.__name__} not raised")
    except exception_class as e:
        if message_substring not in str(e):
            raise AssertionError(
                f"Exception message '{e}' does not contain '{message_substring}'"
            ) from e
    except Exception as e:  # noqa: BLE001 — top-level error boundary
        raise AssertionError(f"Unexpected exception {type(e).__name__}: {e}") from e
