from __future__ import annotations

import json
from pathlib import Path

from .cert import build_pc, build_pc_digest, build_plan_digest
from .execute import execute_certified


def run_vectors(vector_dir: Path) -> dict:
    results: list[dict] = []
    passed = 0
    failed = 0

    for file in sorted(vector_dir.glob("T*.json")):
        vector = json.loads(file.read_text(encoding="utf-8"))
        constructed = build_pc(
            vector["inputs"],
            decision=vector["pc"]["decision"],
            decision_reason_code=vector["pc"]["decision_reason_code"],
        )
        plan_digest, _ = build_plan_digest(vector["inputs"]["steps"])
        actual = execute_certified(vector["pc"], vector["runtime"])

        checks = {
            "expected_plan_digest": plan_digest == vector["expected_plan_digest"],
            "expected_pc_digest": build_pc_digest(vector["pc"]) == vector["expected_pc_digest"],
            "deterministic_build": constructed["pc_digest"] == vector["expected_pc_digest"],
            "execution_expected": actual == vector["expected"],
        }
        ok = all(checks.values())
        passed += int(ok)
        failed += int(not ok)
        results.append({"test_id": vector["test_id"], "ok": ok, "checks": checks, "actual": actual})

    return {"passed": passed, "failed": failed, "results": results}
