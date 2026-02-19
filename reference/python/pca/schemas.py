from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError
from referencing import Registry, Resource


SCHEMAS_DIR = Path(__file__).resolve().parents[3] / "schemas"


@lru_cache(maxsize=1)
def _schema_registry() -> tuple[dict[str, dict[str, Any]], Registry]:
    schema_map: dict[str, dict[str, Any]] = {}
    resources: list[tuple[str, Resource]] = []

    for path in SCHEMAS_DIR.glob("*.schema.json"):
        schema = json.loads(path.read_text(encoding="utf-8"))
        schema_map[path.name] = schema
        schema_id = schema.get("$id")
        if isinstance(schema_id, str):
            resources.append((schema_id, Resource.from_contents(schema)))

    return schema_map, Registry().with_resources(resources)


def validate(instance: dict, schema_name: str) -> None:
    schema_map, registry = _schema_registry()

    try:
        schema = schema_map[schema_name]
    except KeyError as exc:
        raise ValueError(f"Unknown schema: {schema_name}") from exc

    validator = Draft202012Validator(
        schema=schema,
        registry=registry,
        format_checker=Draft202012Validator.FORMAT_CHECKER,
    )


_SCHEMAS_DIR = Path(__file__).resolve().parents[3] / "schemas"


def _load_schemas() -> tuple[dict[str, dict], Registry]:
    schemas_by_name: dict[str, dict] = {}
    registry = Registry()

    for schema_path in sorted(_SCHEMAS_DIR.glob("*.schema.json")):
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        schemas_by_name[schema_path.name] = schema

        schema_id = schema.get("$id")
        if isinstance(schema_id, str) and schema_id:
            registry = registry.with_resource(uri=schema_id, resource=Resource.from_contents(schema))

        registry = registry.with_resource(
            uri=schema_path.name,
            resource=Resource.from_contents(schema),
        )

    return schemas_by_name, registry


_SCHEMAS_BY_NAME, _SCHEMA_REGISTRY = _load_schemas()


def validate(instance: dict, schema_name: str) -> None:
    schema = _SCHEMAS_BY_NAME.get(schema_name)
    if schema is None:
        raise ValueError(f"Unknown schema: {schema_name}")

    validator = Draft202012Validator(schema=schema, registry=_SCHEMA_REGISTRY)

    try:
        validator.validate(instance)
    except ValidationError as exc:
        raise ValueError(exc.message) from exc
        raise ValueError(str(exc)) from exc
