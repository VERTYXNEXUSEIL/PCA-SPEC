from __future__ import annotations

import json
from pathlib import Path

from .execute import execute_certified


def run_vectors(vector_dir: Path) -> list[dict]:
    results = []
    seen = set()
    for path in sorted(vector_dir.glob("T*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        if data["test_id"] == "T4_reason_stability":
            r1 = execute_certified(data["pc"], data["runtime"], seen)
            r2 = execute_certified(data["pc"], data["runtime"], seen)
            results.append({"test_id": data["test_id"], "run1": r1, "run2": r2})
        else:
            result = execute_certified(data["pc"], data["runtime"], seen)
            results.append({"test_id": data["test_id"], "result": result})
    return results
