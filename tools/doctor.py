#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VECTORS_DIR = ROOT / "test-vectors" / "vectors-v1"
PYTHON_DIR = ROOT / "reference" / "python"


@dataclass
class StepResult:
    name: str
    status: str
    detail: str


def _run_subprocess(name: str, cmd: list[str], cwd: Path) -> None:
    print(f"\n▶ {name}: {' '.join(cmd)}")
    completed = subprocess.run(cmd, cwd=cwd, check=False)
    if completed.returncode != 0:
        raise RuntimeError(f"{name} failed with exit code {completed.returncode}")


def validate_schemas() -> str:
    sys.path.insert(0, str(PYTHON_DIR))
    from pca.schemas import validate  # noqa: PLC0415

    count = 0
    for path in sorted(VECTORS_DIR.glob("T*.json")):
        vec = json.loads(path.read_text(encoding="utf-8"))
        validate(vec["pc"], "pc.schema.json")
        validate(vec["pc"]["steps"][0], "action_ir.schema.json")
        validate(
            {
                "version_id": vec["pc"]["constraints_version_id"],
                "effective_time": vec["pc"]["effective_time"],
                "payload": {"allow": ["transfer"]},
                "digest": vec["pc"]["constraints_digest"],
            },
            "constraints.schema.json",
        )
        validate(
            {
                "capsule_version": "1.0",
                "proofs": [{"type": "test", "digest": vec["expected_pc_digest"]}],
            },
            "evidence_capsule.schema.json",
        )
        count += 1
    return f"validated schema compatibility for {count} vectors"


def run_vectors() -> str:
    sys.path.insert(0, str(PYTHON_DIR))
    from pca.execute import execute_certified  # noqa: PLC0415

    seen: set[str] = set()
    count = 0
    for path in sorted(VECTORS_DIR.glob("T*.json")):
        vec = json.loads(path.read_text(encoding="utf-8"))
        expected = vec["expected"]

        if vec.get("replay"):
            _ = execute_certified(vec["pc"], vec["runtime"], seen)

        if vec["test_id"] == "T4_reason_stability":
            out1 = execute_certified(vec["pc"], vec["runtime"], set())
            out2 = execute_certified(vec["pc"], vec["runtime"], set())
            if out1 != expected or out2 != expected:
                raise RuntimeError(f"{vec['test_id']} mismatch: out1={out1}, out2={out2}, expected={expected}")
        else:
            out = execute_certified(vec["pc"], vec["runtime"], seen)
            if out != expected:
                raise RuntimeError(f"{vec['test_id']} mismatch: got {out}, expected {expected}")

        count += 1
    return f"{count} vectors matched expected outcomes"
def run_pytest() -> str:
    _run_subprocess("pytest", ["pytest", "-q"], PYTHON_DIR)
    return "pytest passed"


def run_ruff() -> str:
    _run_subprocess("ruff", ["ruff", "check", "."], PYTHON_DIR)
    return "ruff passed"


def run_node_t13_check() -> str:
    package_json = ROOT / "reference" / "node" / "package.json"
    if not package_json.exists():
        return "skipped (reference/node/package.json not found)"

    package = json.loads(package_json.read_text(encoding="utf-8"))
    scripts = package.get("scripts", {})
    if "t13:check" not in scripts:
        return "skipped (npm script t13:check not defined)"

    _run_subprocess("node-t13-check", ["npm", "run", "t13:check"], package_json.parent)
    return "node T13 check passed"


def main() -> int:
    steps = [
        ("validate-schemas", validate_schemas),
        ("run-vectors", run_vectors),
        ("pytest", run_pytest),
        ("ruff", run_ruff),
        ("node-t13-check", run_node_t13_check),
    ]

    summary: list[StepResult] = []
    for name, step in steps:
        print(f"\n=== {name} ===")
        try:
            detail = step()
        except Exception as exc:  # noqa: BLE001
            summary.append(StepResult(name=name, status="FAIL", detail=str(exc)))
            print(f"✖ {name}: {exc}")
            print("\nFinal summary:")
            for item in summary:
                print(f"- [{item.status}] {item.name}: {item.detail}")
            return 1

        status = "SKIP" if detail.startswith("skipped") else "OK"
        summary.append(StepResult(name=name, status=status, detail=detail))
        icon = "↷" if status == "SKIP" else "✔"
        print(f"{icon} {name}: {detail}")

    print("\nFinal summary:")
    for item in summary:
        print(f"- [{item.status}] {item.name}: {item.detail}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
