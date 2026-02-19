# Profile Government Grade (Gold Mapping)

## Required reason codes
All Baseline reason codes, plus:
- VERIFY_CONFLICT
- RISK_BLAST_RADIUS_EXCEEDED
- OOD_TRIGGERED
- DISCLOSURE_BUDGET_EXCEEDED
- EVIDENCE_HASH_MISMATCH

## Required tests
- Full T1-T13 vector set

## Required logs
- Baseline logs
- Merkle proof verification status
- OOD/disclosure enforcement decisions
- Artifact verification output (`verify_release_assets.py`)

## Recommended controls
- Independent verifier execution
- Immutable audit-log retention
- Routine release reproducibility checks (double-build hash match)
