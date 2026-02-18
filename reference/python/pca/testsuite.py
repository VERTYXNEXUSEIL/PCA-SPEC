from __future__ import annotations

import json
from pathlib import Path

from .execute import execute_certified


def run_vectors(vector_dir: Path) -> list[dict]:
    out = []
    for file in sorted(vector_dir.glob("T*.json")):
        v = json.loads(file.read_text(encoding="utf-8"))
        out.append({"test_id": v["test_id"], "result": execute_certified(v["pc"], v["runtime"])})
    return out
