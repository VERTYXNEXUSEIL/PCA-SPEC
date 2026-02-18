from __future__ import annotations

import json
from pathlib import Path

from pca.cert import build_pc_digest, build_plan_digest
from pca.execute import execute_certified
from pca.schemas import validate

ROOT = Path(__file__).resolve().parents[3]
VEC = ROOT / "test-vectors" / "vectors-v1"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_vectors_match_expected() -> None:
    for f in sorted(VEC.glob("T*.json")):
        v = _load(f)
        assert build_pc_digest(v["pc"]) == v["expected_pc_digest"]
        pd, _ = build_plan_digest(v["inputs"]["steps"])
        assert pd == v["expected_plan_digest"]
        out = execute_certified(v["pc"], v["runtime"])
        assert out == v["expected"], v["test_id"]


def test_reason_stability() -> None:
    v = _load(VEC / "T4_reason_stability.json")
    assert execute_certified(v["pc"], v["runtime"]) == execute_certified(v["pc"], v["runtime"])


def test_minimal_schema_checks() -> None:
    v = _load(VEC / "T13_cross_impl_determinism.json")
    validate(v["pc"], "pc.schema.json")
    validate(v["inputs"]["steps"][0]["AIR"], "action_ir.schema.json")
    validate(
        {
            "constraints_version_id": v["pc"]["constraints_version_id"],
            "effective_time": v["pc"]["effective_time"],
            "constraints_payload": v["inputs"]["steps"][0]["C"],
        },
        "constraints.schema.json",
    )
    validate(v["pc"]["evidence_capsule"], "evidence_capsule.schema.json")
