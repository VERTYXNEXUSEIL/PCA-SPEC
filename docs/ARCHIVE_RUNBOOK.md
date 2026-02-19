# Archive Runbook (Prior-Publication Packaging)

This runbook describes a repeatable publication flow for PCA/CAE release artifacts and long-term archives.

## 1) Create signed tag

```bash
git fetch --tags
git tag -s v1.0.0 -m "PCA/CAE first public release"
git push origin v1.0.0
```

## 2) Build reproducible release artifacts

```bash
python tools/build_release.py --tag v1.0.0
python tools/verify_release_assets.py --tag v1.0.0
```

Expected outputs in `dist/`:
- `pca-spec-v1.0.0.zip`
- `SHA256SUMS`
- `MANIFEST.json`
- `BUILDINFO.json`

## 3) Publish GitHub Release

1. Create release from tag `v1.0.0`.
2. Attach all files from `dist/` listed above.
3. Use `releases/RELEASE_NOTES_v1.0.0.md` as release notes.

## 4) Archive in Zenodo

1. Connect GitHub repository to Zenodo.
2. Trigger archival from the `v1.0.0` release.
3. Record minted DOI.

## 5) Update citation metadata

1. Edit `CITATION.cff` DOI placeholders.
2. Commit and publish update in a patch release.

## 6) Mirror for durability (optional but recommended)

- Upload release zip and checksums to Internet Archive.
- Keep metadata consistent with tag and SHA256 values.

## 7) Verify external archive package

```bash
sha256sum -c SHA256SUMS
```

This document is operational guidance only and not legal advice.
