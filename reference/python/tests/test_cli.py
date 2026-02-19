from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CLI = ROOT / "reference" / "cli" / "pca_cli.py"
VECTORS = ROOT / "test-vectors" / "vectors-v1"
SCHEMA_PC = ROOT / "schemas" / "pc.schema.json"


def _run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    env = {"PYTHONPATH": str(ROOT / "reference" / "python")}
    return subprocess.run(
        [sys.executable, str(CLI), *args],
        capture_output=True,
        text=True,
        check=False,
        env=env,
    )


def _load_vector(file_name: str) -> dict:
    return json.loads((VECTORS / file_name).read_text(encoding="utf-8"))


def test_cli_smoke_help() -> None:
    proc = _run_cli("--help")
    assert proc.returncode == 0
    assert "validate-schemas" in proc.stdout
    assert "run-vectors" in proc.stdout
    assert "build-pc" in proc.stdout
    assert "verify-pc" in proc.stdout
    assert "execute" in proc.stdout


def test_validate_schemas_code_path(tmp_path: Path) -> None:
    vec = _load_vector("T10_brs_gate.json")
    valid_pc = tmp_path / "valid_pc.json"
    invalid_pc = tmp_path / "invalid_pc.json"
    valid_pc.write_text(json.dumps(vec["pc"]), encoding="utf-8")
    invalid_payload = dict(vec["pc"])
    invalid_payload.pop("pc_id")
    invalid_pc.write_text(json.dumps(invalid_payload), encoding="utf-8")

    ok = _run_cli("validate-schemas", str(SCHEMA_PC), str(valid_pc))
    assert ok.returncode == 0
    ok_payload = json.loads(ok.stdout)
    assert ok_payload[0]["valid"] is True

    bad = _run_cli("validate-schemas", str(SCHEMA_PC), str(invalid_pc))
    assert bad.returncode == 1
    bad_payload = json.loads(bad.stdout)
    assert bad_payload[0]["valid"] is False


def test_run_vectors_code_path() -> None:
    proc = _run_cli("run-vectors")
    assert proc.returncode == 0
    payload = json.loads(proc.stdout)
    assert payload
    assert all(result["passed"] is True for result in payload)


def test_build_pc_code_path(tmp_path: Path) -> None:
    vec = _load_vector("T1_pc_replay.json")
    pc_path = tmp_path / "pc.json"
    pc_path.write_text(json.dumps(vec["pc"]), encoding="utf-8")

    proc = _run_cli("build-pc", str(pc_path))
    assert proc.returncode == 0
    payload = json.loads(proc.stdout)
    assert payload["pc_digest"] == vec["expected_pc_digest"]
    assert isinstance(payload["step_digests"], list)


def test_verify_pc_code_path(tmp_path: Path) -> None:
    vec = _load_vector("T10_brs_gate.json")
    pc_path = tmp_path / "pc.json"
    runtime_path = tmp_path / "runtime.json"
    pc_path.write_text(json.dumps(vec["pc"]), encoding="utf-8")
    runtime_path.write_text(json.dumps(vec["runtime"]), encoding="utf-8")

    proc = _run_cli("verify-pc", str(pc_path), str(runtime_path))
    assert proc.returncode == 0
    payload = json.loads(proc.stdout)
    assert payload["decision"] == "EXECUTE"
    assert payload["reason_code"] == "RC_OK"


def test_execute_code_path(tmp_path: Path) -> None:
    vec = _load_vector("T10_brs_gate.json")
    pc_path = tmp_path / "pc.json"
    runtime_path = tmp_path / "runtime.json"
    pc_path.write_text(json.dumps(vec["pc"]), encoding="utf-8")
    runtime_path.write_text(json.dumps(vec["runtime"]), encoding="utf-8")

    proc = _run_cli("execute", str(pc_path), str(runtime_path))
    assert proc.returncode == 0
    payload = json.loads(proc.stdout)
    assert payload == vec["expected"]
