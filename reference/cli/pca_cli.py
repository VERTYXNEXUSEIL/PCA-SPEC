#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

CLI_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(CLI_DIR.parent / "python"))

from pca.cert import build_pc
from pca.execute import execute_certified
from pca.schemas import ROOT, SCHEMAS_DIR, validate, validate_all
from pca.testsuite import run_vectors
from pca.verify import verify_pc

DEFAULT_VECTORS = ROOT / "test-vectors" / "vectors-v1"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def cmd_validate_schemas(_: argparse.Namespace) -> int:
    validated = validate_all()

    examples = {
        "pc.schema.json": {
            "pc_version": "1.0",
            "hash_function_id": "SHA-256",
            "canonical_encoding_id": "JCS-PCA-v1",
            "goal_digest": "0" * 64,
            "initial_state_digest": "1" * 64,
            "constraints_version_id": "cons-v1",
            "constraints_digest": "2" * 64,
            "effective_time": {"not_before": "2026-01-01T00:00:00Z", "not_after": "2026-12-31T23:59:59Z"},
            "plan_digest": "3" * 64,
            "decision": "ALLOW",
            "decision_reason_code": "VERIFY_ALLOW",
            "evidence_capsule": {"capsule_version": "1.0", "proofs": []},
        },
        "constraints.schema.json": {
            "constraints_version_id": "cons-v1",
            "effective_time": {"not_before": "2026-01-01T00:00:00Z", "not_after": "2026-12-31T23:59:59Z"},
            "constraints_payload": {"limit": 1},
        },
        "action_ir.schema.json": {
            "action_type": "set_x",
            "parameters": {"value": 2},
            "required_capabilities": ["kv.write"],
        },
        "evidence_capsule.schema.json": {"capsule_version": "1.0", "proofs": []},
    }
    for name, sample in examples.items():
        validate(sample, name)

    print(f"Validated schemas in {SCHEMAS_DIR}: {', '.join(validated)}")
    return 0


def cmd_run_vectors(args: argparse.Namespace) -> int:
    report = run_vectors(args.vector_dir)
    print(f"Vector summary: passed={report['passed']} failed={report['failed']}")
    print(json.dumps(report["results"], indent=2))
    return 0 if report["failed"] == 0 else 1


def cmd_build_pc(args: argparse.Namespace) -> int:
    built = build_pc(_load(args.input), decision=args.decision, decision_reason_code=args.reason)
    print(json.dumps(built, indent=2))
    return 0


def cmd_verify_pc(args: argparse.Namespace) -> int:
    pc = _load(args.pc)
    runtime = _load(args.runtime)
    verdict, reason_code = verify_pc(pc, runtime)
    execution = execute_certified(pc, runtime)
    print(json.dumps({"verify": {"verdict": verdict, "reason_code": reason_code}, "execute": execution}, indent=2))
    return 0 if execution["decision"] == "ALLOW" else 1


def cmd_execute(args: argparse.Namespace) -> int:
    pc = _load(args.pc)
    runtime = _load(args.runtime)
    print(json.dumps(execute_certified(pc, runtime), indent=2))
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="PCA/CAE CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    validate_parser = sub.add_parser("validate-schemas", help="Validate JSON Schemas (Draft 2020-12)")
    validate_parser.set_defaults(func=cmd_validate_schemas)

    vectors_parser = sub.add_parser("run-vectors", help="Run T1-T13 vector suite")
    vectors_parser.add_argument("vector_dir", nargs="?", type=Path, default=DEFAULT_VECTORS)
    vectors_parser.set_defaults(func=cmd_run_vectors)

    build_parser = sub.add_parser("build-pc", help="Build deterministic PC from raw input")
    build_parser.add_argument("input", type=Path)
    build_parser.add_argument("--decision", default="ALLOW")
    build_parser.add_argument("--reason", default="VERIFY_ALLOW")
    build_parser.set_defaults(func=cmd_build_pc)

    verify_parser = sub.add_parser("verify-pc", help="Verify and execute PC against runtime")
    verify_parser.add_argument("pc", type=Path)
    verify_parser.add_argument("runtime", type=Path)
    verify_parser.set_defaults(func=cmd_verify_pc)

    execute_parser = sub.add_parser("execute", help="Execute certified decision")
    execute_parser.add_argument("pc", type=Path)
    execute_parser.add_argument("runtime", type=Path)
    execute_parser.set_defaults(func=cmd_execute)

    args = parser.parse_args()
    raise SystemExit(args.func(args))


if __name__ == "__main__":
    main()
