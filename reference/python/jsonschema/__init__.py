from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator


@dataclass
class ValidationError:
    message: str
    path: tuple[Any, ...] = ()


class Draft202012Validator:
    def __init__(self, schema: dict[str, Any]) -> None:
        self.schema = schema
        base_dir = schema.get("_base_dir")
        self.base_dir = Path(base_dir) if base_dir else None

    @staticmethod
    def check_schema(schema: dict[str, Any]) -> None:
        if not isinstance(schema, dict):
            raise ValueError("Schema must be an object")
        if schema.get("$schema") and "2020-12" not in schema["$schema"]:
            raise ValueError("Only JSON Schema draft 2020-12 is supported")

    def iter_errors(self, instance: Any) -> Iterator[ValidationError]:
        yield from self._validate(instance, self.schema, ())

    def _validate(
        self, instance: Any, schema: dict[str, Any], path: tuple[Any, ...]
    ) -> Iterator[ValidationError]:
        if "$ref" in schema:
            yield from self._validate(instance, self._resolve_ref(schema["$ref"]), path)
            return

        expected_type = schema.get("type")
        if expected_type:
            if not self._matches_type(instance, expected_type):
                yield ValidationError(f"{path or 'instance'} is not of type '{expected_type}'", path)
                return

        if "const" in schema and instance != schema["const"]:
            yield ValidationError(f"{path or 'instance'} must be equal to constant {schema['const']!r}", path)

        if "enum" in schema and instance not in schema["enum"]:
            yield ValidationError(f"{path or 'instance'} is not one of {schema['enum']}", path)

        if isinstance(instance, str):
            min_length = schema.get("minLength")
            if min_length is not None and len(instance) < min_length:
                yield ValidationError(f"{path or 'instance'} is too short", path)
            pattern = schema.get("pattern")
            if pattern and re.fullmatch(pattern, instance) is None:
                yield ValidationError(f"{path or 'instance'} does not match pattern {pattern!r}", path)

        if isinstance(instance, dict):
            required = schema.get("required", [])
            for key in required:
                if key not in instance:
                    yield ValidationError(f"{path or 'instance'} is missing required property '{key}'", path)

            props = schema.get("properties", {})
            additional_properties = schema.get("additionalProperties", True)
            if additional_properties is False:
                allowed = set(props.keys())
                for key in instance:
                    if key not in allowed:
                        yield ValidationError(
                            f"{path or 'instance'} has additional property '{key}'", path + (key,)
                        )

            for key, value in instance.items():
                if key in props:
                    yield from self._validate(value, props[key], path + (key,))

        if isinstance(instance, list):
            if schema.get("uniqueItems"):
                seen = set()
                for idx, item in enumerate(instance):
                    marker = json.dumps(item, sort_keys=True, separators=(",", ":"))
                    if marker in seen:
                        yield ValidationError(f"{path or 'instance'} has non-unique items", path + (idx,))
                        break
                    seen.add(marker)
            item_schema = schema.get("items")
            if item_schema:
                for idx, item in enumerate(instance):
                    yield from self._validate(item, item_schema, path + (idx,))

    def _resolve_ref(self, ref: str) -> dict[str, Any]:
        if ref.startswith("#"):
            raise ValueError("Local schema references are not supported")
        if self.base_dir is None:
            raise ValueError("Cannot resolve $ref without schema base directory")
        ref_path = (self.base_dir / ref).resolve()
        schema = json.loads(ref_path.read_text(encoding="utf-8"))
        schema["_base_dir"] = str(ref_path.parent)
        return schema

    @staticmethod
    def _matches_type(instance: Any, expected_type: str) -> bool:
        if expected_type == "object":
            return isinstance(instance, dict)
        if expected_type == "array":
            return isinstance(instance, list)
        if expected_type == "string":
            return isinstance(instance, str)
        if expected_type == "number":
            return isinstance(instance, (int, float)) and not isinstance(instance, bool)
        if expected_type == "integer":
            return isinstance(instance, int) and not isinstance(instance, bool)
        if expected_type == "boolean":
            return isinstance(instance, bool)
        if expected_type == "null":
            return instance is None
        return True
