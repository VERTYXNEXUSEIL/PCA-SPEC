from __future__ import annotations

import json
from pathlib import Path

from pca.cert import build_pc, build_pc_digest, build_plan_digest
from pca.execute import execute_certified
from pca.schemas import validate

ROOT = Path(__file__).resolve().parents[3]
VEC = ROOT / "test-vectors" / "vectors-v1"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_vectors_match_expected() -> None:
    for path in sorted(VEC.glob("T*.json")):
        vector = _load(path)
        built = build_pc(
            vector["inputs"],
            decision=vector["pc"]["decision"],
            decision_reason_code=vector["pc"]["decision_reason_code"],
        )
        assert built["pc_digest"] == vector["expected_pc_digest"]

        assert build_pc_digest(vector["pc"]) == vector["expected_pc_digest"]
        plan_digest, _ = build_plan_digest(vector["inputs"]["steps"])
        assert plan_digest == vector["expected_plan_digest"]

        out = execute_certified(vector["pc"], vector["runtime"])
        assert out == vector["expected"], vector["test_id"]


def test_reason_stability() -> None:
    vector = _load(VEC / "T4_reason_stability.json")
    assert execute_certified(vector["pc"], vector["runtime"]) == execute_certified(vector["pc"], vector["runtime"])


def test_minimal_schema_checks() -> None:
    vector = _load(VEC / "T13_cross_impl_determinism.json")
    validate(vector["pc"], "pc.schema.json")
    validate(vector["inputs"]["steps"][0]["AIR"], "action_ir.schema.json")
    validate(
        {
            "constraints_version_id": vector["pc"]["constraints_version_id"],
            "effective_time": vector["pc"]["effective_time"],
            "constraints_payload": vector["inputs"]["steps"][0]["C"],
        },
        "constraints.schema.json",
    )
    validate(vector["pc"]["evidence_capsule"], "evidence_capsule.schema.json")
