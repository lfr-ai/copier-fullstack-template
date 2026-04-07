"""Property-based tests for the registry generator.

Co-located with the registry module to test generator functions
via Hypothesis-driven invariant testing.
"""

from __future__ import annotations

import pytest
from generate_registry import (
    _to_camel_case,
    _to_pascal_case,
    _validate_registry,
)
from hypothesis import given, settings
from hypothesis import strategies as st

pytestmark = pytest.mark.property


_IDENTIFIER = st.from_regex(r"[a-z][a-z0-9_]{0,30}", fullmatch=True)
_KEBAB = st.from_regex(r"[a-z][a-z0-9\-]{0,30}", fullmatch=True)
_MIXED = st.one_of(_IDENTIFIER, _KEBAB)


class TestToPascalCase:
    """Property tests for _to_pascal_case."""

    @given(text=_MIXED)
    @settings(max_examples=200)
    def test_result_starts_with_uppercase(self, text: str) -> None:
        result = _to_pascal_case(text)
        assert result == "" or result[0].isupper()

    @given(text=_MIXED)
    @settings(max_examples=200)
    def test_result_has_no_separators(self, text: str) -> None:
        result = _to_pascal_case(text)
        assert "_" not in result
        assert "-" not in result
        assert " " not in result

    @given(text=_MIXED)
    @settings(max_examples=200)
    def test_result_is_alphanumeric(self, text: str) -> None:
        result = _to_pascal_case(text)
        assert result.isalnum() or result == ""

    @given(text=_MIXED)
    @settings(max_examples=100)
    def test_idempotent_when_already_pascal(self, text: str) -> None:
        """Applying PascalCase twice should not change the result further."""
        once = _to_pascal_case(text)
        twice = _to_pascal_case(once)
        assert once == twice


class TestToCamelCase:
    """Property tests for _to_camel_case."""

    @given(text=_MIXED)
    @settings(max_examples=200)
    def test_result_starts_with_lowercase(self, text: str) -> None:
        result = _to_camel_case(text)
        assert result == "" or result[0].islower()

    @given(text=_MIXED)
    @settings(max_examples=200)
    def test_shares_body_with_pascal(self, text: str) -> None:
        """After the first char, camelCase == PascalCase."""
        pascal = _to_pascal_case(text)
        camel = _to_camel_case(text)
        if len(pascal) > 1:
            assert camel[1:] == pascal[1:]


class TestValidateRegistry:
    """Property tests for _validate_registry."""

    _VALID_BASE: dict = {
        "schema_version": 1,
        "metadata": {
            "version": "1.0.0",
            "last_updated": "2025-01-01",
            "maintainer": "test",
        },
        "enums": {},
        "unified_fields": {},
        "ports": {},
    }

    @given(
        extra_keys=st.dictionaries(
            st.text(min_size=1, max_size=10),
            st.text(max_size=10),
            max_size=3,
        ),
    )
    @settings(max_examples=50)  
    def test_extra_keys_do_not_cause_errors(self, extra_keys: dict) -> None:
        """Unknown top-level keys should be tolerated."""
        registry = {**self._VALID_BASE, **extra_keys}
        errors = _validate_registry(registry)
        assert errors == []

    @given(version=st.integers(min_value=2, max_value=9999))
    @settings(max_examples=30)
    def test_unsupported_schema_version_always_fails(self, version: int) -> None:
        registry = {**self._VALID_BASE, "schema_version": version}
        errors = _validate_registry(registry)
        assert any("schema_version" in e for e in errors)
