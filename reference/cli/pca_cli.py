#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from jsonschema import Draft202012Validator

from pca.cert import build_merkle_root, build_pc_digest, build_plan_digest
from pca.execute import execute_certified
from pca.verify import verify_pc


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_VECTOR_DIR = ROOT / "test-vectors" / "vectors-v1"


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _print_json(payload: dict | list[dict]) -> None:
    print(json.dumps(payload, indent=2))


def cmd_validate_schemas(args: argparse.Namespace) -> int:
    schema = _load_json(args.schema)
    schema["_base_dir"] = str(args.schema.parent)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)

    results: list[dict] = []
    ok = True
    for json_path in args.files:
        instance = _load_json(json_path)
        errors = sorted(validator.iter_errors(instance), key=lambda err: list(err.path))
        if errors:
            ok = False
            results.append(
                {
                    "file": str(json_path),
                    "valid": False,
                    "errors": [error.message for error in errors],
                }
            )
        else:
            results.append({"file": str(json_path), "valid": True})

    _print_json(results)
    return 0 if ok else 1


def cmd_run_vectors(args: argparse.Namespace) -> int:
    seen: set[str] = set()
    results: list[dict] = []
    ok = True

    for path in sorted(args.vector_dir.glob("T*.json")):
        vector = _load_json(path)
        if vector.get("replay"):
            execute_certified(vector["pc"], vector["runtime"], seen)
        actual = execute_certified(vector["pc"], vector["runtime"], seen)
        expected = vector["expected"]
        passed = actual == expected
        ok = ok and passed
        results.append(
            {
                "test_id": vector["test_id"],
                "passed": passed,
                "expected": expected,
                "actual": actual,
            }
        )

    _print_json(results)
    return 0 if ok else 1


def cmd_build_pc(args: argparse.Namespace) -> int:
    pc = _load_json(args.pc)
    normalized_steps = [
        step if "action_ir" in step else {"action_ir": step} for step in pc["steps"]
    ]
    plan_digest, step_digests = build_plan_digest(normalized_steps)
    merkle_root = build_merkle_root(step_digests)
    output = {
        "plan_digest": plan_digest,
        "merkle_root": merkle_root,
        "pc_digest": build_pc_digest(pc),
        "step_digests": step_digests,
    }
    _print_json(output)
    return 0


def cmd_verify_pc(args: argparse.Namespace) -> int:
    pc = _load_json(args.pc)
    runtime = _load_json(args.runtime)
    decision, reason_code = verify_pc(pc, runtime)
    _print_json({"decision": decision, "reason_code": reason_code})
    return 0


def cmd_execute(args: argparse.Namespace) -> int:
    pc = _load_json(args.pc)
    runtime = _load_json(args.runtime)
    _print_json(execute_certified(pc, runtime))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="PCA CLI verifier/executor")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser(
        "validate-schemas", help="Validate JSON files against a JSON schema"
    )
    validate_parser.add_argument("schema", type=Path, help="Path to JSON schema")
    validate_parser.add_argument("files", nargs="+", type=Path, help="JSON files to validate")
    validate_parser.set_defaults(func=cmd_validate_schemas)

    vectors_parser = subparsers.add_parser(
        "run-vectors", help="Run all vectors in test-vectors/vectors-v1"
    )
    vectors_parser.add_argument("--vector-dir", type=Path, default=DEFAULT_VECTOR_DIR)
    vectors_parser.set_defaults(func=cmd_run_vectors)

    build_parser_ = subparsers.add_parser("build-pc", help="Build deterministic PC artifacts")
    build_parser_.add_argument("pc", type=Path)
    build_parser_.set_defaults(func=cmd_build_pc)

    verify_parser = subparsers.add_parser("verify-pc", help="Verify PC and return decision")
    verify_parser.add_argument("pc", type=Path)
    verify_parser.add_argument("runtime", type=Path)
    verify_parser.set_defaults(func=cmd_verify_pc)

    execute_parser = subparsers.add_parser("execute", help="Certified execution")
    execute_parser.add_argument("pc", type=Path)
    execute_parser.add_argument("runtime", type=Path)
    execute_parser.set_defaults(func=cmd_execute)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
