#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from pca.execute import execute_certified


def main() -> None:
    parser = argparse.ArgumentParser(description="PCA CLI verifier/executor")
    parser.add_argument("pc", type=Path)
    parser.add_argument("runtime", type=Path)
    args = parser.parse_args()

    pc = json.loads(args.pc.read_text(encoding="utf-8"))
    runtime = json.loads(args.runtime.read_text(encoding="utf-8"))
    print(json.dumps(execute_certified(pc, runtime), indent=2))


if __name__ == "__main__":
    main()
