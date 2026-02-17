from __future__ import annotations


def _require_fields(instance: dict, fields: list[str]) -> None:
    for field in fields:
        if field not in instance:
            raise ValueError(f"Missing required field: {field}")


def validate(instance: dict, schema_name: str) -> None:
    if schema_name == "pc.schema.json":
        _require_fields(
            instance,
            [
                "pc_version",
                "pc_id",
                "issued_at",
                "planner_id",
                "constraints_version_id",
                "constraints_digest",
                "effective_time",
                "plan_digest",
                "steps",
                "nonce",
            ],
        )
        if instance["pc_version"] != "1.0":
            raise ValueError("pc_version must be 1.0")
    elif schema_name == "constraints.schema.json":
        _require_fields(instance, ["version_id", "effective_time", "payload", "digest"])
    elif schema_name == "action_ir.schema.json":
        _require_fields(instance, ["action_type", "parameters", "required_capabilities"])
    elif schema_name == "evidence_capsule.schema.json":
        _require_fields(instance, ["capsule_version", "proofs"])
        if instance["capsule_version"] != "1.0":
            raise ValueError("capsule_version must be 1.0")
    else:
        raise ValueError(f"Unknown schema: {schema_name}")
