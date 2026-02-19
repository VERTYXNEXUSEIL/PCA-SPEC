# PCA-SPEC

Proof-Carrying Autonomy (PCA) / Certified Agentic Execution (CAE) is a product-neutral technical standard and implementation package for deterministic, certifiable autonomous action execution.

## Authorship & First Publication

This repository publicly discloses PCA/CAE standard and reference implementation.

- **Primary Author/Inventor: ARKADIUSZ LESZO**
- First public release timestamp: `2026-02-17T21:34:ssZ`
- First signed release tag: `v1.0.0`
  

## What is in this repository

- Normative and companion specification docs in [`spec/`](spec/)
- Canonical JSON Schemas in [`schemas/`](schemas/)
- Deterministic test vectors in [`test-vectors/vectors-v1/`](test-vectors/vectors-v1/)
- Python reference implementation in [`reference/python/`](reference/python/)
- CLI helper in [`reference/cli/pca_cli.py`](reference/cli/pca_cli.py)
- CI, release, and provenance workflows in [`.github/workflows/`](.github/workflows/)

## Standard scope (v1)

PCA/CAE specifies:

1. Canonical encoding and domain-separated hashing.
2. Plan Certificate (PC) structure and digest derivation.
3. Constraint versioning (`constraints_version_id`, `constraints_digest`, `effective_time`).
4. Certified execution protocol and TOCTOU fallback behavior.
5. Deterministic reason codes and conformance profiles.
6. Conformance tests and vector-driven harness.

## Quickstart

```bash
cd reference/python
python -m pip install -e .[dev]
pytest -q
```

Full local gate (schemas, vectors, pytest, ruff, optional Node T13):

```bash
python tools/doctor.py
```

## How to Verify Integrity

1. **Verify tag signature**
   ```bash
   git fetch --tags
   git tag -v v1.0.0
   ```
2. **Verify release checksums**
   ```bash
   sha256sum -c SHA256SUMS
   ```
3. **Verify CI provenance output**
   - Inspect provenance workflow artifacts and attestation subject digests.
   - Confirm build inputs map to the signed tag commit.

## Release instructions (maintainers)

### Create a signed tag

```bash
git tag -s v1.0.0 -m "PCA/CAE v1.0.0"
git push origin v1.0.0
```

### Generate SHA256SUMS

```bash
find spec schemas reference test-vectors -type f -print0 | sort -z | xargs -0 sha256sum > SHA256SUMS
```

### Create a release bundle

```bash
mkdir -p spec-bundle
cp -r spec schemas test-vectors LICENSE-SPEC NOTICE PATENT-NOTICE.md spec-bundle/
zip -r pca-spec-bundle-v1.0.0.zip spec-bundle
sha256sum pca-spec-bundle-v1.0.0.zip >> SHA256SUMS
```

### Publish release & archive

- Create a GitHub Release for tag `v1.0.0`.
- Attach `pca-spec-bundle-v1.0.0.zip` and `SHA256SUMS`.
- Archive the release in Zenodo manually.
- Update `CITATION.cff` with the resulting DOI.

## Polish summary (PL)

PCA/CAE to neutralny produktowo standard certyfikowalnego wykonywania działań agentowych. Repozytorium zawiera normatywną specyfikację, schematy, wektory testowe, implementację referencyjną i mechanizmy provenance.
