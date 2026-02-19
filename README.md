# pca-spec

**Proof-Carrying Autonomy / Certified Agentic Execution: pre-execution deterministic verification + Plan Certificate + TOCTOU-safe execution + mandatory fallback.**

## Authorship & First Publication (Prior Art)

This repository publicly discloses PCA/CAE standard and reference implementation.

- Primary Author/Inventor: ARKADIUSZ LESZO
- First public release: v1.0.0
- Release timestamp (UTC): to be set to the actual tag creation time in `YYYY-MM-DDTHH:MM:SSZ` format (update this line after creating the signed tag)
- Signed tag: v1.0.0 (verified signature)
- Release artifacts: spec bundle + SHA256SUMS + MANIFEST.json + BUILDINFO.json
- Disclaimer: no legal advice

## How to Verify Integrity

1. Verify signed tag (platform + local):
   ```bash
   git fetch --tags
   git tag -v v1.0.0
   ```
2. Verify SHA256SUMS:
   ```bash
   sha256sum -c dist/SHA256SUMS
   ```
3. Verify release assets (checksums + manifest + buildinfo):
   ```bash
   python tools/verify_release_assets.py --tag v1.0.0
   ```

## Release & Prior-Art Packaging

```bash
# 1) Create and push signed tag
git tag -s v1.0.0 -m "PCA/CAE first public release"
git push origin v1.0.0

# 2) Build release bundle
mkdir -p dist
tmpdir="dist/pca-spec-v1.0.0"
rm -rf "$tmpdir"
mkdir -p "$tmpdir"
cp -r spec schemas test-vectors reference README.md LICENSE-CODE LICENSE-SPEC NOTICE PATENT-NOTICE.md "$tmpdir"/
(cd dist && zip -r pca-spec-v1.0.0.zip pca-spec-v1.0.0)

# 3) Generate self-verifying artifacts
python tools/build_release.py --tag v1.0.0
python tools/verify_release_assets.py --tag v1.0.0

# 4) Attach dist/pca-spec-v1.0.0.zip, dist/SHA256SUMS, dist/MANIFEST.json and dist/BUILDINFO.json to GitHub Release
```

## Conformance Profiles (CAE-Mark)

- **Bronze**: deterministic canonicalization, required digest checks, constraints enforcement, fallback reason coding.
- **Silver**: Bronze + Merkle proof support + passing T1-T10.
- **Gold**: Silver + OOD/disclosure governance + passing T1-T13.

## Repo map

- [`spec/`](spec/) - normative standard text and change template.
- [`schemas/`](schemas/) - canonical JSON Schemas (draft 2020-12).
- [`test-vectors/vectors-v1/`](test-vectors/vectors-v1/) - deterministic conformance vectors.
- [`reference/`](reference/) - Python reference implementation + CLI.
- [`adoption/`](adoption/) - procurement language, integrity checks, and threat model.
- [`cert/`](cert/) - CAE-Mark guidance, conformance checklists, and report templates.
- [`profiles/`](profiles/) - baseline and government-grade profile mappings.
- [`docs/ARCHIVE_RUNBOOK.md`](docs/ARCHIVE_RUNBOOK.md) - GitHub/Zenodo archival workflow.

## Quickstart (reference implementation)

```bash
cd reference/python
python -m pytest -q
python ../cli/pca_cli.py run-vectors ../../test-vectors/vectors-v1
```

## Streszczenie PL

- PCA/CAE definiuje certyfikowalne wykonywanie działań agentowych.
- Każdy plan ma kryptograficzny Plan Certificate (PC).
- Hashowanie jest deterministyczne i separowane domenami (`STATEv1`, `PCv1`, itd.).
- Wykonanie sprawdza wersję i skrót ograniczeń oraz okno czasu.
- Zmiana stanu typu TOCTOU wymusza bezpieczny fallback.
- Kody reason_code są zamknięte i stabilne wersyjnie.
- Wektory testowe T1-T13 zapewniają testowalną zgodność.
- Repozytorium wspiera publikację prior-art przez tagi podpisane i sumy SHA256.
