# PCA-RC v1 (Closed Reason Code Dictionary)

Version: `PCA-RC-v1`

This is a versioned closed dictionary. Implementations MUST NOT repurpose existing identifiers.

## Determinism rule

Identical canonical inputs MUST produce identical verdict and identical `reason_code`.

## Reason codes

### Planning
- `PLAN_OK`
- `PLAN_NO_PATH`
- `PLAN_EXHAUSTED_TIME`
- `PLAN_EXHAUSTED_EXPANDS`
- `PLAN_EXHAUSTED_MAXLEN`
- `PLAN_TIEBREAK_APPLIED`

### Verification
- `VERIFY_ALLOW`
- `VERIFY_DENY_SAFETY`
- `VERIFY_DENY_RESOURCE`
- `VERIFY_DENY_DOMAIN`
- `VERIFY_DENY_POLICY`
- `VERIFY_ESCALATE_REQUIRED`
- `VERIFY_CONFLICT`

### Constraint and policy binding
- `CONSTRAINTS_VERSION_MISMATCH`
- `CONSTRAINTS_DIGEST_MISMATCH`
- `POLICY_VERSION_MISMATCH`
- `POLICY_DIGEST_MISMATCH`
- `LEGAL_SNAPSHOT_MISMATCH`
- `LEGAL_EFFECTIVE_TIME_MISMATCH`

### Risk, model, and disclosure gates
- `RISK_BLAST_RADIUS_EXCEEDED`
- `OOD_TRIGGERED`
- `DISCLOSURE_BUDGET_EXCEEDED`
- `OUTPUT_CANONICALIZATION_FAIL`

### Integrity and execution
- `INTEGRITY_FAIL`
- `EXEC_DENY_GATE`
- `EXEC_FALLBACK_SAFE_MODE`
- `AUDIT_INCOMPLETE`
- `EVIDENCE_MISSING`
- `EVIDENCE_HASH_MISMATCH`
