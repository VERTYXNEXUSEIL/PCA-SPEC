from __future__ import annotations

from copy import deepcopy

from .hashing import LABELS, ds_hash
from .reason_codes import VERIFY_ALLOW


def build_step_digest(step: dict) -> str:
    bundle = {
        "initial_state_digest": ds_hash(LABELS["state"], step["S0"]),
        "goal_digest": ds_hash(LABELS["goal"], step["G"]),
        "constraints_digest": ds_hash(LABELS["constraints"], step["C"]),
        "policy_digest": ds_hash(LABELS["policy"], step.get("P", {})),
        "planner_config_digest": ds_hash(LABELS["config"], step.get("CFG", {})),
        "action_ir_digest": ds_hash(LABELS["air"], step["AIR"]),
    }
    return ds_hash(LABELS["step"], bundle)


def build_plan_digest(steps: list[dict]) -> tuple[str, list[str]]:
    step_digests = [build_step_digest(s) for s in steps]
    return ds_hash(LABELS["plan"], {"step_digests": step_digests}), step_digests


def build_merkle_root(step_digests: list[str]) -> str:
    if not step_digests:
        return ds_hash(LABELS["plan"], {"empty": True})
    layer = step_digests[:]
    while len(layer) > 1:
        nxt = []
        for i in range(0, len(layer), 2):
            left = layer[i]
            right = layer[i + 1] if i + 1 < len(layer) else left
            nxt.append(ds_hash(LABELS["plan"], {"left": left, "right": right}))
        layer = nxt
    return layer[0]


def build_pc(inputs: dict, decision: str = "ALLOW", decision_reason_code: str = VERIFY_ALLOW) -> dict:
    plan_digest, step_digests = build_plan_digest(inputs["steps"])
    pc = {
        "pc_version": "1.0",
        "hash_function_id": "SHA-256",
        "canonical_encoding_id": "JCS-PCA-v1",
        "goal_digest": ds_hash(LABELS["goal"], inputs["steps"][0]["G"]),
        "initial_state_digest": ds_hash(LABELS["state"], inputs["steps"][0]["S0"]),
        "constraints_version_id": inputs["constraints_version_id"],
        "constraints_digest": inputs["constraints_digest"],
        "effective_time": inputs["effective_time"],
        "plan_digest": plan_digest,
        "planner_config_digest": ds_hash(LABELS["config"], inputs["steps"][0].get("CFG", {})),
        "action_ir_digest": ds_hash(LABELS["air"], inputs["steps"][0]["AIR"]),
        "decision": decision,
        "decision_reason_code": decision_reason_code,
        "evidence_capsule": {
            "capsule_version": "1.0",
            "proofs": [
                {
                    "proof_id": "plan-step-0",
                    "proof_digest": step_digests[0],
                    "proof_type": "STEP_DIGEST",
                    "retention": "p7y"
                }
            ]
        },
    }
    return pc


def build_pc_digest(pc: dict) -> str:
    clean = deepcopy(pc)
    clean.pop("signatures", None)
    return ds_hash(LABELS["pc"], clean)
