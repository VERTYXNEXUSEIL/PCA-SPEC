from __future__ import annotations

from copy import deepcopy

from .hashing import ds_hash


HASH_LABELS = {
    "state": "STATEv1",
    "goal": "GOALv1",
    "constraints": "CONSv1",
    "policy": "POLv1",
    "config": "CFGv1",
    "step": "STEPv1",
    "plan": "PLANv1",
    "pc": "PCv1",
    "air": "AIRv1",
}


def build_step_digest(step: dict) -> str:
    bundle = {
        "state_digest": ds_hash(HASH_LABELS["state"], step.get("state", {})),
        "goal_digest": ds_hash(HASH_LABELS["goal"], step.get("goal", {})),
        "constraints_digest": ds_hash(HASH_LABELS["constraints"], step.get("constraints", {})),
        "policy_digest": ds_hash(HASH_LABELS["policy"], step.get("policy", {})),
        "config_digest": ds_hash(HASH_LABELS["config"], step.get("config", {})),
        "air_digest": ds_hash(HASH_LABELS["air"], step["action_ir"]),
    }
    return ds_hash(HASH_LABELS["step"], bundle)


def build_plan_digest(steps: list[dict]) -> tuple[str, list[str]]:
    step_digests = [build_step_digest(step) for step in steps]
    return ds_hash(HASH_LABELS["plan"], {"step_digests": step_digests}), step_digests


def build_merkle_root(step_digests: list[str]) -> str:
    if not step_digests:
        return ds_hash(HASH_LABELS["plan"], {"empty": True})
    layer = step_digests[:]
    while len(layer) > 1:
        nxt = []
        for i in range(0, len(layer), 2):
            left = layer[i]
            right = layer[i + 1] if i + 1 < len(layer) else left
            nxt.append(ds_hash(HASH_LABELS["plan"], {"left": left, "right": right}))
        layer = nxt
    return layer[0]


def build_pc_digest(pc: dict) -> str:
    copy = deepcopy(pc)
    copy.pop("signature", None)
    return ds_hash(HASH_LABELS["pc"], copy)
