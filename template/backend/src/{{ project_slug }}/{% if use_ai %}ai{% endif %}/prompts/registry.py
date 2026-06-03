"""Prompt registry helpers for versioned prompt provisioning and run metadata."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, final

_DEFAULT_PROFILE = "default"
_DEFAULT_VERSION = "v1"
_MAX_RUN_NAME_LENGTH = 120
_VERSION_PATTERN = re.compile(r"^v(\d+)$")
_SAFE_RUN_CHARS = re.compile(r"[^a-zA-Z0-9._-]+")


@final
class PromptVersionResolver:
    """Resolve prompt templates from a file-backed prompt registry."""

    __slots__ = ("_overrides", "_profile", "_registry", "_versions_dir")

    def __init__(
        self,
        *,
        registry_path: str,
        versions_dir: str,
        profile: str = _DEFAULT_PROFILE,
        overrides: dict[str, str] | None = None,
    ) -> None:
        self._profile = profile or _DEFAULT_PROFILE
        self._overrides = overrides or {}
        self._registry = _load_registry(path=registry_path)
        self._versions_dir = Path(versions_dir)

    def resolve(
        self,
        *,
        name: str,
        fallback_template: str,
    ) -> tuple[str, str]:
        """Resolve template text and active version for a prompt name."""
        version = self._resolve_version(name=name)
        entry = self._registry.get("prompts", {}).get(name, {})
        versions = entry.get("versions", {})
        relative_path = versions.get(version)
        if not relative_path:
            return fallback_template, _DEFAULT_VERSION

        candidate = self._versions_dir / relative_path
        if not candidate.exists() or not candidate.is_file():
            return fallback_template, _DEFAULT_VERSION

        return candidate.read_text(encoding="utf-8"), version

    def available_versions(self, *, name: str) -> list[str]:
        """Return all known versions for a prompt name, sorted by numeric version."""
        entry = self._registry.get("prompts", {}).get(name, {})
        versions = list(entry.get("versions", {}).keys())
        versions.sort(key=_version_sort_key)
        return versions

    def _resolve_version(self, *, name: str) -> str:
        if name in self._overrides:
            return self._overrides[name]

        profiles = self._registry.get("profiles", {})
        profile_map = profiles.get(self._profile) or profiles.get(_DEFAULT_PROFILE) or {}
        version = profile_map.get(name, _DEFAULT_VERSION)
        if isinstance(version, str):
            return version
        return _DEFAULT_VERSION


@final
class PromptRegistryEditor:
    """Create new immutable prompt versions and update profile pointers."""

    __slots__ = ("_path",)

    def __init__(self, *, registry_path: str) -> None:
        self._path = Path(registry_path)

    def provision_version(
        self,
        *,
        name: str,
        template_text: str,
        versions_dir: str,
        profile: str = _DEFAULT_PROFILE,
    ) -> tuple[str, Path]:
        """Provision the next version file and update profile pointer in registry."""
        registry = _load_registry(path=str(self._path))

        prompts = registry.setdefault("prompts", {})
        prompt_entry = prompts.setdefault(name, {})
        version_map = prompt_entry.setdefault("versions", {})

        next_version = _next_version(existing=list(version_map.keys()))
        file_name = f"{name}.{next_version}.j2"
        relative_path = file_name

        versions_path = Path(versions_dir)
        versions_path.mkdir(parents=True, exist_ok=True)
        file_path = versions_path / file_name
        file_path.write_text(template_text, encoding="utf-8")

        version_map[next_version] = relative_path

        profiles = registry.setdefault("profiles", {})
        profile_map = profiles.setdefault(profile, {})
        profile_map[name] = next_version

        if "default" not in profiles:
            profiles["default"] = dict(profile_map)

        self._path.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
        return next_version, file_path


def parse_version_overrides(raw: str) -> dict[str, str]:
    """Parse JSON override map from config/env value."""
    if not raw.strip():
        return {}
    try:
        loaded = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    if not isinstance(loaded, dict):
        return {}
    out: dict[str, str] = {}
    for key, value in loaded.items():
        if isinstance(key, str) and isinstance(value, str):
            out[key] = value
    return out


def build_prompt_version_run_name(
    *,
    prefix: str,
    prompt_versions: dict[str, str],
    max_length: int = _MAX_RUN_NAME_LENGTH,
) -> str:
    """Build deterministic run name embedding active prompt versions.

    Format: ``{prefix}-{name@vX_name@vY}-{hash8}``
    """
    items = [f"{name}@{version}" for name, version in sorted(prompt_versions.items())]
    serialized = "_".join(items) if items else "unversioned"
    digest = hashlib.sha256(serialized.encode("utf-8")).hexdigest()[:8]
    normalized = _SAFE_RUN_CHARS.sub("-", serialized).strip("-._") or "unversioned"

    budget = max(max_length - len(prefix) - len(digest) - 2, 16)
    normalized = normalized[:budget]
    return f"{prefix}-{normalized}-{digest}"


def _version_sort_key(version: str) -> tuple[int, str]:
    match = _VERSION_PATTERN.fullmatch(version)
    if not match:
        return 10_000, version
    return int(match.group(1)), version


def _next_version(*, existing: list[str]) -> str:
    if not existing:
        return _DEFAULT_VERSION
    numeric = [int(m.group(1)) for item in existing if (m := _VERSION_PATTERN.fullmatch(item))]
    if not numeric:
        return _DEFAULT_VERSION
    return f"v{max(numeric) + 1}"


def _load_registry(*, path: str) -> dict[str, Any]:
    registry_path = Path(path)
    if not registry_path.exists() or not registry_path.is_file():
        return {
            "schema_version": 1,
            "profiles": {"default": {}},
            "prompts": {},
        }

    try:
        loaded = json.loads(registry_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {
            "schema_version": 1,
            "profiles": {"default": {}},
            "prompts": {},
        }

    if not isinstance(loaded, dict):
        return {
            "schema_version": 1,
            "profiles": {"default": {}},
            "prompts": {},
        }
    return loaded
