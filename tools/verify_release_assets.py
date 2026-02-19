#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
REQUIRED_BUILDINFO_FIELDS = {
    "tag",
    "commit_sha",
    "generated_utc",
    "python_version",
    "node_version",
    "os",
    "arch",
    "schema_versions",
    "workflow_run_id",
    "workflow_run_number",
    "workflow_ref",
}


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_sha256sums(sums_path: Path) -> list[str]:
    errors: list[str] = []
    for line in sums_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        expected, filename = line.split("  ", 1)
        artifact = DIST / filename
        if not artifact.exists():
            errors.append(f"Missing artifact in SHA256SUMS: {filename}")
            continue
        actual = _sha256_file(artifact)
        if actual != expected:
            errors.append(f"SHA mismatch for {filename}")
    return errors


def verify_manifest_vs_zip(manifest_path: Path, zip_path: Path) -> list[str]:
    errors: list[str] = []
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    expected = {item["path"]: item for item in manifest.get("files", [])}

    with ZipFile(zip_path, "r") as archive:
        names = sorted(info.filename for info in archive.infolist() if not info.is_dir())
        if names != sorted(expected):
            errors.append("Zip content list does not match MANIFEST file list")
        for info in archive.infolist():
            if info.is_dir() or info.filename not in expected:
                continue
            payload = archive.read(info.filename)
            sha = hashlib.sha256(payload).hexdigest()
            if sha != expected[info.filename]["sha256"]:
                errors.append(f"Manifest sha mismatch for {info.filename}")
            if len(payload) != expected[info.filename]["size"]:
                errors.append(f"Manifest size mismatch for {info.filename}")
    return errors


def verify_buildinfo(buildinfo_path: Path) -> list[str]:
    errors: list[str] = []
    buildinfo = json.loads(buildinfo_path.read_text(encoding="utf-8"))
    missing = sorted(REQUIRED_BUILDINFO_FIELDS - set(buildinfo))
    if missing:
        errors.append(f"BUILDINFO missing fields: {', '.join(missing)}")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify PCA release assets")
    parser.add_argument("--dist", default="dist")
    parser.add_argument("--tag", required=True)
    args = parser.parse_args()

    dist = ROOT / args.dist
    zip_path = dist / f"pca-spec-{args.tag}.zip"
    sums_path = dist / "SHA256SUMS"
    manifest_path = dist / "MANIFEST.json"
    buildinfo_path = dist / "BUILDINFO.json"

    failures = []
    failures += verify_sha256sums(sums_path)
    failures += verify_manifest_vs_zip(manifest_path, zip_path)
    failures += verify_buildinfo(buildinfo_path)

    if failures:
        print("Release asset verification failed:")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)
    print("Release asset verification OK")


if __name__ == "__main__":
    main()
