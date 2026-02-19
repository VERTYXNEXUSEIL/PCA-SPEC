# Integrity Verification Steps

```bash
# Verify release checksums
sha256sum -c dist/SHA256SUMS

# Verify release assets end-to-end
python tools/verify_release_assets.py --tag v1.0.0

# Verify signed tag locally
git fetch --tags
git tag -v v1.0.0
```

All verification steps are deterministic and can be automated in CI/CD.
