"""JSON serialisation / deserialisation helpers.

Thin wrappers around :mod:`json` with :class:`AppJSONEncoder` as the
default encoder for common Python types (datetime, UUID, set).
"""

from __future__ import annotations

import datetime
import json
import uuid
from typing import Any, override

__all__ = ["AppJSONEncoder", "dumps", "loads"]


class AppJSONEncoder(json.JSONEncoder):
    """Extended encoder that handles common Python types."""

    @override
    def default(self, o: object) -> str | list[object]:
        """Serialise non-standard types to JSON-safe primitives.

        Args:
            o (object): Object to serialise.

        Returns:
            str | list[object]: JSON-serialisable representation.
        """
        if isinstance(o, datetime.datetime):
            return o.isoformat()
        if isinstance(o, datetime.date):
            return o.isoformat()
        if isinstance(o, uuid.UUID):
            return str(o)
        if isinstance(o, set):
            return sorted(o)  # type: ignore[type-var]
        return super().default(o)  # type: ignore[return-value]


def dumps(obj: object, **kwargs: Any) -> str:
    """Serialize *obj* to a JSON string using :class:`AppJSONEncoder`.

    Args:
        obj (object): Python object to serialise.
        **kwargs: Extra arguments forwarded to ``json.dumps``.

    Returns:
        str: JSON string.
    """
    return json.dumps(obj, cls=AppJSONEncoder, **kwargs)


def loads(s: str | bytes) -> Any:
    """Deserialize a JSON string.

    Args:
        s (str | bytes): JSON string or bytes to parse.

    Returns:
        Any: Parsed Python object (dict, list, str, int, float, bool, or None).
    """
    return json.loads(s)
