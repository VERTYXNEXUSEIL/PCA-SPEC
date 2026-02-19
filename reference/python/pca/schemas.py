from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[3]
SCHEMAS_DIR = ROOT / "schemas"


def load_schema(schema_name: str) -> dict:
    return json.loads((SCHEMAS_DIR / schema_name).read_text(encoding="utf-8"))


def validate(instance: dict, schema_name: str) -> None:
    schema = load_schema(schema_name)
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(instance)


def validate_all() -> list[str]:
    validated: list[str] = []
    for schema_file in sorted(SCHEMAS_DIR.glob("*.schema.json")):
        schema = json.loads(schema_file.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        validated.append(schema_file.name)
    return validated
