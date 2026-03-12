"""Unit tests for the registry generator.

These tests verify the generate_registry module functions work
correctly with known inputs and edge cases.
"""

from __future__ import annotations

import json
from unittest.mock import patch

import pytest
from generate_registry import (
    _generate_env_ports,
    _generate_python_constants,
    _generate_ts_constants,
    _to_camel_case,
    _to_pascal_case,
    _validate_registry,
    generate,
)

pytestmark = pytest.mark.unit


_MINIMAL_REGISTRY: dict[str, object] = {
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


_FULL_REGISTRY: dict[str, object] = {
    "schema_version": 1,
    "metadata": {
        "version": "0.1.0",
        "last_updated": "2025-06-01",
        "maintainer": "Dev Team",
    },
    "enums": {
        "Status": ["active", "inactive"],
        "Priority": {"LOW": 1, "HIGH": 2},
    },
    "unified_fields": {
        "User": {
            "id": {"orm": "id", "pydantic": "id", "alias": "id"},
            "email": {"orm": "email", "pydantic": "email", "alias": "email"},
        },
    },
    "routes": {
        "users": {
            "prefix": "/api/v1/users",
            "endpoints": {"list": "", "detail": "/{id}"},
        },
    },
    "ports": {"BACKEND": 8000, "FRONTEND_DEV": 5173},
}


class TestToPascalCase:
    """Unit tests for known _to_pascal_case conversions."""

    @pytest.mark.parametrize(
        ("input_str", "expected"),
        [
            ("claim_status", "ClaimStatus"),
            ("my-kebab-var", "MyKebabVar"),
            ("simple", "Simple"),
            ("a_b_c", "ABC"),
            ("hello_world", "HelloWorld"),
        ],
    )
    def test_known_conversions(self, input_str: str, expected: str) -> None:
        assert _to_pascal_case(input_str) == expected


class TestToCamelCase:
    """Unit tests for known _to_camel_case conversions."""

    @pytest.mark.parametrize(
        ("input_str", "expected"),
        [
            ("claim_status", "claimStatus"),
            ("my-kebab-var", "myKebabVar"),
            ("simple", "simple"),
        ],
    )
    def test_known_conversions(self, input_str: str, expected: str) -> None:
        assert _to_camel_case(input_str) == expected


class TestValidateRegistry:
    """Unit tests for _validate_registry."""

    def test_minimal_valid_registry(self) -> None:
        assert _validate_registry(_MINIMAL_REGISTRY) == []

    def test_missing_schema_version(self) -> None:
        bad = {**_MINIMAL_REGISTRY}
        del bad["schema_version"]
        errors = _validate_registry(bad)
        assert any("schema_version" in e for e in errors)

    def test_wrong_schema_version(self) -> None:
        bad = {**_MINIMAL_REGISTRY, "schema_version": 99}
        errors = _validate_registry(bad)
        assert any("schema_version" in e for e in errors)

    def test_missing_metadata(self) -> None:
        bad = {**_MINIMAL_REGISTRY}
        del bad["metadata"]
        errors = _validate_registry(bad)
        assert any("metadata" in e for e in errors)

    def test_empty_metadata_reports_all_fields(self) -> None:
        bad = {**_MINIMAL_REGISTRY, "metadata": {}}
        errors = _validate_registry(bad)
        assert len(errors) >= 3  # version, last_updated, maintainer

    def test_missing_enums(self) -> None:
        bad = {**_MINIMAL_REGISTRY}
        del bad["enums"]
        errors = _validate_registry(bad)
        assert any("enums" in e for e in errors)

    def test_missing_unified_fields(self) -> None:
        bad = {**_MINIMAL_REGISTRY}
        del bad["unified_fields"]
        errors = _validate_registry(bad)
        assert any("unified_fields" in e for e in errors)

    def test_missing_ports(self) -> None:
        bad = {**_MINIMAL_REGISTRY}
        del bad["ports"]
        errors = _validate_registry(bad)
        assert any("ports" in e for e in errors)


class TestGeneratePythonConstants:
    """Unit tests for Python constant generation."""

    def test_generates_header(self) -> None:
        output = _generate_python_constants(_MINIMAL_REGISTRY)
        assert "DO NOT EDIT MANUALLY" in output

    def test_generates_enum_classes(self) -> None:
        output = _generate_python_constants(_FULL_REGISTRY)
        assert "class Status" in output
        assert "class Priority" in output

    def test_generates_port_class(self) -> None:
        output = _generate_python_constants(_FULL_REGISTRY)
        assert "BACKEND" in output
        assert "8000" in output

    def test_generates_route_class(self) -> None:
        output = _generate_python_constants(_FULL_REGISTRY)
        assert "/api/v1/users" in output

    def test_generates_metadata(self) -> None:
        output = _generate_python_constants(_FULL_REGISTRY)
        assert "REGISTRY_VERSION" in output
        assert '"0.1.0"' in output


class TestGenerateTsConstants:
    """Unit tests for TypeScript constant generation."""

    def test_generates_header(self) -> None:
        output = _generate_ts_constants(_MINIMAL_REGISTRY)
        assert "DO NOT EDIT MANUALLY" in output

    def test_generates_registry_export(self) -> None:
        output = _generate_ts_constants(_FULL_REGISTRY)
        assert "export const" in output

    def test_generates_ports(self) -> None:
        output = _generate_ts_constants(_FULL_REGISTRY)
        assert "BACKEND" in output
        assert "8000" in output

    def test_generates_routes(self) -> None:
        output = _generate_ts_constants(_FULL_REGISTRY)
        assert "users" in output
        assert "/api/v1/users" in output


class TestGenerateEnvPorts:
    """Unit tests for .env.ports generation."""

    def test_header_comment(self) -> None:
        output = _generate_env_ports({"BACKEND": 8000})
        assert "AUTO-GENERATED" in output or "DO NOT EDIT" in output

    def test_port_entries(self) -> None:
        output = _generate_env_ports({"BACKEND": 8000, "REDIS": 6379})
        assert "PORT_BACKEND=8000" in output
        assert "PORT_REDIS=6379" in output

    def test_empty_ports(self) -> None:
        output = _generate_env_ports({})
        assert "PORT_" not in output


class TestGenerateFunction:
    """Tests for the top-level generate() orchestrator."""

    def test_validate_only_returns_zero_for_valid(self, tmp_path: Path) -> None:
        registry_file = tmp_path / "naming_registry.json"
        registry_file.write_text(json.dumps(_MINIMAL_REGISTRY), encoding="utf-8")
        with patch("generate_registry.REGISTRY_PATH", registry_file):
            result = generate(validate_only=True)
        assert result == 0

    def test_validate_only_returns_one_for_invalid(self, tmp_path: Path) -> None:
        registry_file = tmp_path / "naming_registry.json"
        registry_file.write_text(json.dumps({"bad": True}), encoding="utf-8")
        with patch("generate_registry.REGISTRY_PATH", registry_file):
            result = generate(validate_only=True)
        assert result == 1

    def test_missing_registry_returns_one(self, tmp_path: Path) -> None:
        missing = tmp_path / "nonexistent.json"
        with patch("generate_registry.REGISTRY_PATH", missing):
            result = generate()
        assert result == 1
