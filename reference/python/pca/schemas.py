from __future__ import annotations

REQUIRED = {
    "pc.schema.json": [
        "pc_version",
        "hash_function_id",
        "canonical_encoding_id",
        "goal_digest",
        "initial_state_digest",
        "constraints_version_id",
        "constraints_digest",
        "effective_time",
        "plan_digest",
        "decision",
        "decision_reason_code",
        "evidence_capsule",
    ],
    "constraints.schema.json": ["constraints_version_id", "effective_time", "constraints_payload"],
    "action_ir.schema.json": ["action_type", "parameters", "required_capabilities"],
    "evidence_capsule.schema.json": ["capsule_version", "proofs"],
}


def validate(instance: dict, schema_name: str) -> None:
    fields = REQUIRED[schema_name]
    missing = [x for x in fields if x not in instance]
    if missing:
        raise ValueError(f"Missing required: {missing}")
