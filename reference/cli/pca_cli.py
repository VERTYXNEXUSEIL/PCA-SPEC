#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from pca.cert import build_pc
from pca.execute import execute_certified
from pca.schemas import validate
from pca.testsuite import run_vectors
from pca.verify import verify_pc


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def cmd_validate_schemas(args: argparse.Namespace) -> None:
    validate(_load(args.pc), "pc.schema.json")
    validate(_load(args.constraints), "constraints.schema.json")
    validate(_load(args.air), "action_ir.schema.json")
    validate(_load(args.evidence), "evidence_capsule.schema.json")
    print("OK")


def cmd_run_vectors(args: argparse.Namespace) -> None:
    print(json.dumps(run_vectors(args.vector_dir), indent=2))


def cmd_build_pc(args: argparse.Namespace) -> None:
    pc = build_pc(_load(args.inputs), decision=args.decision, decision_reason_code=args.reason)
    print(json.dumps(pc, indent=2))


def cmd_verify_pc(args: argparse.Namespace) -> None:
    pc = _load(args.pc)
    runtime = _load(args.runtime)
    v = verify_pc(pc, runtime)
    e = execute_certified(pc, runtime)
    print(json.dumps({"verify": {"verdict": v[0], "reason_code": v[1]}, "execute": e}, indent=2))


def main() -> None:
    p = argparse.ArgumentParser(description="PCA/CAE CLI")
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("validate-schemas")
    a.add_argument("--pc", type=Path, required=True)
    a.add_argument("--constraints", type=Path, required=True)
    a.add_argument("--air", type=Path, required=True)
    a.add_argument("--evidence", type=Path, required=True)
    a.set_defaults(func=cmd_validate_schemas)

    b = sub.add_parser("run-vectors")
    b.add_argument("vector_dir", type=Path)
    b.set_defaults(func=cmd_run_vectors)

    c = sub.add_parser("build-pc")
    c.add_argument("inputs", type=Path)
    c.add_argument("--decision", default="ALLOW")
    c.add_argument("--reason", default="VERIFY_ALLOW")
    c.set_defaults(func=cmd_build_pc)

    d = sub.add_parser("verify-pc")
    d.add_argument("pc", type=Path)
    d.add_argument("runtime", type=Path)
    d.set_defaults(func=cmd_verify_pc)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
