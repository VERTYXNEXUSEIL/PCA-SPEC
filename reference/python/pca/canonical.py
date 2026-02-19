from __future__ import annotations

import json
import math
from typing import Any


def _normalize_numbers(value: Any) -> Any:
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            raise ValueError("NaN/Inf are forbidden")
        if value == 0.0:
            return 0
        return value
    if isinstance(value, list):
        return [_normalize_numbers(v) for v in value]
    if isinstance(value, dict):
        return {k: _normalize_numbers(v) for k, v in value.items()}
    return value


def prune_optional_none(data: dict[str, Any], schema: dict[str, Any]) -> dict[str, Any]:
    required = set(schema.get("required", []))
    props = schema.get("properties", {})
    out: dict[str, Any] = {}

    for key, value in data.items():
        if key not in props:
            out[key] = value
            continue

        if value is None and key not in required:
            continue

        prop_schema = props[key]
        if isinstance(value, dict) and prop_schema.get("type") == "object":
            out[key] = prune_optional_none(value, prop_schema)
        elif isinstance(value, list) and prop_schema.get("type") == "array":
            item_schema = prop_schema.get("items", {})
            if item_schema.get("type") == "object":
                out[key] = [prune_optional_none(item, item_schema) if isinstance(item, dict) else item for item in value]
            else:
                out[key] = value
        else:
            out[key] = value

    return out


def canonical_json_bytes(data: Any) -> bytes:
    normalized = _normalize_numbers(data)
    payload = json.dumps(normalized, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return payload.encode("utf-8")
