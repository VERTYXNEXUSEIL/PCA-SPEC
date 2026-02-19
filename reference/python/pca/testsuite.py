from __future__ import annotations

import json
from pathlib import Path

from .execute import execute_certified


def run_vectors(vector_dir: Path) -> list[dict]:
    results = []
    seen = set()
    vector_paths = sorted(vector_dir.glob("T*.json"))
    expected_t13 = vector_dir / "T13_cross_impl_determinism.json"
    if expected_t13 not in vector_paths:
        raise FileNotFoundError(f"Missing required vector: {expected_t13.name}")

    for path in vector_paths:
        data = json.loads(path.read_text(encoding="utf-8"))
        if data["test_id"] == "T4_reason_stability":
            r1 = execute_certified(data["pc"], data["runtime"], seen)
            r2 = execute_certified(data["pc"], data["runtime"], seen)
            results.append({"test_id": data["test_id"], "run1": r1, "run2": r2})
        else:
            result = execute_certified(data["pc"], data["runtime"], seen)
            results.append({"test_id": data["test_id"], "result": result})
    return results
