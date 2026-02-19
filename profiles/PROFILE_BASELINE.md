# Profile Baseline (Bronze Mapping)

## Required reason codes
- VERIFY_ALLOW
- CONSTRAINTS_VERSION_MISMATCH
- CONSTRAINTS_DIGEST_MISMATCH
- LEGAL_EFFECTIVE_TIME_MISMATCH
- EXEC_FALLBACK_SAFE_MODE
- INTEGRITY_MISMATCH

## Required tests
- T1, T2, T3, T4, T5, T6

## Required logs
- PC digest and plan digest
- Runtime constraints version/digest
- Decision + reason_code

## Recommended controls
- Signed release tags
- Automated checksum verification in CI
