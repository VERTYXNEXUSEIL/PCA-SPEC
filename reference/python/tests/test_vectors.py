from __future__ import annotations

import json
from pathlib import Path

from pca.cert import build_pc_digest
from pca.execute import execute_certified
from pca.schemas import validate


ROOT = Path(__file__).resolve().parents[3]
VECTORS = ROOT / "test-vectors" / "vectors-v1"


def load_vector(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_vector_decisions_and_digests() -> None:
    seen: set[str] = set()
    for path in sorted(VECTORS.glob("T*.json")):
        vec = load_vector(path)
        assert build_pc_digest(vec["pc"]) == vec["expected_pc_digest"]

        if vec.get("replay"):
            _ = execute_certified(vec["pc"], vec["runtime"], seen)

        out = execute_certified(vec["pc"], vec["runtime"], seen)
        assert out == vec["expected"], f"{vec['test_id']} failed"


def test_reason_stability() -> None:
    vec = load_vector(VECTORS / "T4_reason_stability.json")
    out1 = execute_certified(vec["pc"], vec["runtime"], set())
    out2 = execute_certified(vec["pc"], vec["runtime"], set())
    assert out1 == out2


def test_schema_validation() -> None:
    vec = load_vector(VECTORS / "T10_brs_gate.json")
    validate(vec["pc"], "pc.schema.json")
    validate(
        {
            "version_id": vec["pc"]["constraints_version_id"],
            "effective_time": vec["pc"]["effective_time"],
            "payload": {"allow": ["transfer"]},
            "digest": vec["pc"]["constraints_digest"],
        },
        "constraints.schema.json",
    )
    validate(vec["pc"]["steps"][0], "action_ir.schema.json")
    validate(
        {
            "capsule_version": "1.0",
            "proofs": [{"type": "test", "digest": vec["expected_pc_digest"]}],
        },
        "evidence_capsule.schema.json",
    )


def test_schema_regression_additional_properties_pattern_and_ref() -> None:
    vec = load_vector(VECTORS / "T10_brs_gate.json")

    pc_extra = json.loads(json.dumps(vec["pc"]))
    pc_extra["unexpected"] = True
    try:
        validate(pc_extra, "pc.schema.json")
    except ValueError:
        pass
    else:
        raise AssertionError("Expected additionalProperties=false validation failure")

    pc_bad_pattern = json.loads(json.dumps(vec["pc"]))
    pc_bad_pattern["constraints_digest"] = "invalid-digest"
    try:
        validate(pc_bad_pattern, "pc.schema.json")
    except ValueError:
        pass
    else:
        raise AssertionError("Expected pattern validation failure")

    pc_bad_ref = json.loads(json.dumps(vec["pc"]))
    pc_bad_ref["steps"][0]["required_capabilities"] = "not-an-array"
    try:
        validate(pc_bad_ref, "pc.schema.json")
    except ValueError:
        pass
    else:
        raise AssertionError("Expected $ref validation failure for action_ir schema")
