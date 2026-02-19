from __future__ import annotations

import re


class Draft202012Validator:
    def __init__(self, schema: dict):
        self.schema = schema

    @staticmethod
    def check_schema(schema: dict) -> None:
        if not isinstance(schema, dict) or schema.get("$schema") is None:
            raise ValueError("Invalid schema")

    def validate(self, instance):
        _validate(instance, self.schema, self.schema)


def _resolve_ref(schema: dict, root: dict) -> dict:
    ref = schema.get("$ref")
    if not ref:
        return schema
    if ref.startswith("#"):
        raise ValueError("Local refs unsupported in lightweight validator")
    # sibling file reference is handled by caller by embedding root properties.
    return root


def _validate(instance, schema: dict, root: dict):
    if "$ref" in schema:
        # Lightweight handling for this repo only: evidence ref from pc schema.
        if schema["$ref"].endswith("evidence_capsule.schema.json"):
            from pathlib import Path
            import json

            base = Path(__file__).resolve().parents[3] / "schemas" / "evidence_capsule.schema.json"
            target = json.loads(base.read_text(encoding="utf-8"))
            _validate(instance, target, target)
            return

    expected_type = schema.get("type")
    if expected_type == "object":
        if not isinstance(instance, dict):
            raise ValueError("Expected object")
        required = schema.get("required", [])
        for key in required:
            if key not in instance:
                raise ValueError(f"Missing required key: {key}")

        props = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            extras = set(instance) - set(props)
            if extras:
                raise ValueError(f"Unexpected keys: {sorted(extras)}")

        for key, value in instance.items():
            if key in props:
                _validate(value, props[key], root)
        return

    if expected_type == "array":
        if not isinstance(instance, list):
            raise ValueError("Expected array")
        item_schema = schema.get("items")
        if item_schema:
            for item in instance:
                _validate(item, item_schema, root)
        return

    if expected_type == "string":
        if not isinstance(instance, str):
            raise ValueError("Expected string")
        pattern = schema.get("pattern")
        if pattern and re.fullmatch(pattern, instance) is None:
            raise ValueError(f"Pattern mismatch: {pattern}")

    if "enum" in schema and instance not in schema["enum"]:
        raise ValueError("Enum mismatch")

    if "const" in schema and instance != schema["const"]:
        raise ValueError("Const mismatch")
