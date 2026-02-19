#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_manifest(manifest_path: Path) -> list[str]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    errors: list[str] = []
    for item in manifest["files"]:
        path = ROOT / item["path"]
        if not path.exists():
            errors.append(f"missing file: {item['path']}")
            continue
        size = path.stat().st_size
        if size != item["size"]:
            errors.append(f"size mismatch: {item['path']}")
        digest = _sha256_file(path)
        if digest != item["sha256"]:
            errors.append(f"sha mismatch: {item['path']}")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify MANIFEST.json against repository content")
    parser.add_argument("--manifest", default="dist/MANIFEST.json")
    args = parser.parse_args()
    errors = verify_manifest(ROOT / args.manifest)
    if errors:
        print("MANIFEST verification failed:")
        for err in errors:
            print(f"- {err}")
        raise SystemExit(1)
    print("MANIFEST verification OK")


if __name__ == "__main__":
    main()
