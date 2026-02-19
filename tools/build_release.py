#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
FIXED_ZIP_TIME = (2000, 1, 1, 0, 0, 0)
INCLUDE_PATHS = [
    "spec",
    "schemas",
    "test-vectors",
    "reference",
    "adoption",
    "cert",
    "profiles",
    "docs",
    "README.md",
    "CHANGELOG.md",
    "CITATION.cff",
    ".zenodo.json",
    "LICENSE-CODE",
    "LICENSE-SPEC",
    "NOTICE",
    "PATENT-NOTICE.md",
]


def _sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _safe_cmd(command: list[str]) -> str | None:
    try:
        return subprocess.check_output(command, cwd=ROOT, text=True).strip()
    except Exception:
        return None


def _git_commit() -> str:
    return _safe_cmd(["git", "rev-parse", "HEAD"]) or "UNKNOWN"


def _node_version() -> str | None:
    return _safe_cmd(["node", "--version"])


def _schema_versions() -> dict[str, str | None]:
    data: dict[str, str | None] = {}
    pc_schema = json.loads((ROOT / "schemas" / "pc.schema.json").read_text(encoding="utf-8"))
    data["pc_version"] = pc_schema.get("properties", {}).get("pc_version", {}).get("const")
    data["canonical_encoding_id"] = pc_schema.get("properties", {}).get("canonical_encoding_id", {}).get("const")
    data["hash_function_id"] = pc_schema.get("properties", {}).get("hash_function_id", {}).get("const")
    for schema_file in sorted((ROOT / "schemas").glob("*.schema.json")):
        obj = json.loads(schema_file.read_text(encoding="utf-8"))
        data[f"schema_id::{schema_file.name}"] = obj.get("$id")
    return data


def _iter_release_files() -> list[Path]:
    files: list[Path] = []
    for entry in INCLUDE_PATHS:
        target = ROOT / entry
        if not target.exists():
            continue
        if target.is_file():
            files.append(target)
            continue
        for path in sorted(target.rglob("*")):
            if path.is_file() and ".git" not in path.parts and "__pycache__" not in path.parts:
                files.append(path)
    return sorted(set(files), key=lambda p: p.relative_to(ROOT).as_posix())


def _entry_mode(path: Path) -> int:
    executable = os.access(path, os.X_OK)
    return 0o755 if executable else 0o644


def build_release(tag: str) -> dict[str, Path]:
    DIST.mkdir(exist_ok=True)
    files = _iter_release_files()

    manifest_files = []
    for path in files:
        rel = path.relative_to(ROOT).as_posix()
        payload = path.read_bytes()
        manifest_files.append({"path": rel, "sha256": _sha256_bytes(payload), "size": len(payload), "mode": oct(_entry_mode(path))})

    manifest = {
        "tag": tag,
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "root": "pca-spec",
        "files": manifest_files,
    }
    manifest_path = DIST / "MANIFEST.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    buildinfo = {
        "tag": tag,
        "commit_sha": _git_commit(),
        "generated_utc": manifest["generated_utc"],
        "python_version": platform.python_version(),
        "node_version": _node_version(),
        "os": platform.system(),
        "arch": platform.machine(),
        "schema_versions": _schema_versions(),
        "workflow_run_id": os.environ.get("GITHUB_RUN_ID", "LOCAL_PLACEHOLDER"),
        "workflow_run_number": os.environ.get("GITHUB_RUN_NUMBER", "LOCAL_PLACEHOLDER"),
        "workflow_ref": os.environ.get("GITHUB_WORKFLOW_REF", "LOCAL_PLACEHOLDER"),
    }
    buildinfo_path = DIST / "BUILDINFO.json"
    buildinfo_path.write_text(json.dumps(buildinfo, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    archive_name = f"pca-spec-{tag}.zip"
    archive_path = DIST / archive_name
    with ZipFile(archive_path, "w", compression=ZIP_DEFLATED) as archive:
        for path in files:
            rel = path.relative_to(ROOT).as_posix()
            info = ZipInfo(rel)
            info.date_time = FIXED_ZIP_TIME
            info.compress_type = ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = (_entry_mode(path) & 0xFFFF) << 16
            archive.writestr(info, path.read_bytes())

    sums_path = DIST / "SHA256SUMS"
    sums_lines = [
        f"{_sha256_file(archive_path)}  {archive_name}",
        f"{_sha256_file(manifest_path)}  MANIFEST.json",
        f"{_sha256_file(buildinfo_path)}  BUILDINFO.json",
    ]
    prov = DIST / "provenance.json"
    if prov.exists():
        sums_lines.append(f"{_sha256_file(prov)}  provenance.json")
    sums_path.write_text("\n".join(sums_lines) + "\n", encoding="utf-8")

    return {"archive": archive_path, "sha256sums": sums_path, "manifest": manifest_path, "buildinfo": buildinfo_path}


def main() -> None:
    parser = argparse.ArgumentParser(description="Build reproducible PCA release artifacts")
    parser.add_argument("--tag", default=os.environ.get("GITHUB_REF_NAME", "v1.0.0"))
    args = parser.parse_args()
    artifacts = build_release(args.tag)
    print(json.dumps({k: str(v.relative_to(ROOT)) for k, v in artifacts.items()}, indent=2))


if __name__ == "__main__":
    main()
