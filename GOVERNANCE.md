# Governance

## Single Source of Truth (SSOT)

`spec/` is normative. If implementation or docs conflict with `spec/`, the normative text prevails.

## Change process

1. Submit RFC based on `spec/PCA-RFC-TEMPLATE.md`.
2. Maintainer review and security assessment.
3. Apply required test updates (`PCA-TEST-v1` + vectors).
4. Approve version bump (patch/minor/major).
5. Publish signed release tag and release artifacts.

## Security fixes

Security changes follow `SECURITY.md` coordinated reporting and remediation process.
