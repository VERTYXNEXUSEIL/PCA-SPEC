from __future__ import annotations

from copy import deepcopy
from typing import Any

from .canonical import prune_optional_none
from .hashing import LABELS, ds_hash
from .merkle import build_merkle_root
from .reason_codes import VERIFY_ALLOW
from .schemas import load_schema


PC_SCHEMA = load_schema("pc.schema.json")
AIR_SCHEMA = load_schema("action_ir.schema.json")


def _compile_air(raw_step: dict[str, Any]) -> dict[str, Any]:
    air = {
        "action_type": raw_step["action_type"],
        "parameters": raw_step.get("parameters", {}),
        "required_capabilities": raw_step.get("required_capabilities", []),
        "predicted_effect": raw_step.get("predicted_effect"),
        "egress_class": raw_step.get("egress_class"),
    }
    return prune_optional_none(air, AIR_SCHEMA)


def _normalized_step(raw_step: dict[str, Any]) -> dict[str, Any]:
    if "AIR" in raw_step:
        air = raw_step["AIR"]
    else:
        air = _compile_air(raw_step)

    return {
        "S0": raw_step["S0"],
        "G": raw_step["G"],
        "C": raw_step["C"],
        "P": raw_step.get("P", {}),
        "CFG": raw_step.get("CFG", {}),
        "AIR": air,
    }


def build_step_digest(step: dict) -> str:
    normalized = _normalized_step(step)
    bundle = {
        "initial_state_digest": ds_hash(LABELS["state"], normalized["S0"]),
        "goal_digest": ds_hash(LABELS["goal"], normalized["G"]),
        "constraints_digest": ds_hash(LABELS["constraints"], normalized["C"]),
        "policy_digest": ds_hash(LABELS["policy"], normalized["P"]),
        "planner_config_digest": ds_hash(LABELS["config"], normalized["CFG"]),
        "action_ir_digest": ds_hash(LABELS["air"], normalized["AIR"]),
    }
    return ds_hash(LABELS["step"], bundle)


def build_plan_digest(steps: list[dict]) -> tuple[str, list[str]]:
    step_digests = [build_step_digest(step) for step in steps]
    return ds_hash(LABELS["plan"], {"step_digests": step_digests}), step_digests


def build_pc(pc_input: dict, decision: str = "ALLOW", decision_reason_code: str = VERIFY_ALLOW) -> dict:
    steps = [_normalized_step(step) for step in pc_input["steps"]]
    plan_digest, step_digests = build_plan_digest(steps)
    merkle_root = build_merkle_root(step_digests)

    primary_step = steps[0]
    pc = deepcopy(pc_input.get("pc", {}))
    pc.update(
        {
            "pc_version": pc.get("pc_version", "1.0"),
            "hash_function_id": pc.get("hash_function_id", "SHA-256"),
            "canonical_encoding_id": pc.get("canonical_encoding_id", "JCS-PCA-v1"),
            "goal_digest": ds_hash(LABELS["goal"], primary_step["G"]),
            "initial_state_digest": ds_hash(LABELS["state"], primary_step["S0"]),
            "constraints_version_id": pc_input["constraints_version_id"],
            "constraints_digest": pc_input["constraints_digest"],
            "effective_time": pc_input["effective_time"],
            "plan_digest": plan_digest,
            "merkle_root": merkle_root,
            "planner_config_digest": ds_hash(LABELS["config"], primary_step["CFG"]),
            "action_ir_digest": ds_hash(LABELS["air"], primary_step["AIR"]),
            "decision": decision,
            "decision_reason_code": decision_reason_code,
            "evidence_capsule": {
                "capsule_version": "1.0",
                "proofs": [
                    {
                        "proof_id": f"plan-step-{idx}",
                        "proof_digest": digest,
                        "proof_type": "STEP_DIGEST",
                        "retention": "p7y",
                    }
                    for idx, digest in enumerate(step_digests)
                ],
            },
        }
    )
    pc = prune_optional_none(pc, PC_SCHEMA)
    pc["pc_digest"] = build_pc_digest(pc)
    return pc


def build_pc_digest(pc: dict) -> str:
    clean = deepcopy(pc)
    clean.pop("signatures", None)
    clean.pop("pc_digest", None)
    clean = prune_optional_none(clean, PC_SCHEMA)
    return ds_hash(LABELS["pc"], clean)
