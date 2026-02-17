# PCA Reason Codes v1

## Stability rules

1. Code identifiers are immutable.
2. Semantics may be clarified but not inverted.
3. Deprecated codes remain reserved and MUST NOT be reassigned.

## Dictionary

- `RC_OK`: Verification and execution checks passed.
- `RC_PC_REPLAY`: PC replay detected.
- `RC_DOMAIN_SEPARATION`: Domain-separated digest mismatch.
- `RC_CONSTRAINTS_MISMATCH`: Constraints digest or version mismatch.
- `RC_REASON_UNSTABLE`: Non-deterministic reason generation detected.
- `RC_TOCTOU`: Time-of-check/time-of-use drift violation.
- `RC_EFFECTIVE_TIME`: Out-of-window effective time.
- `RC_CONFLICT`: Conflict detector blocked action.
- `RC_MERKLE_PROOF`: Invalid Merkle proof.
- `RC_BRS_GATE`: Behavioral risk score gate denied.
- `RC_OOD_TRIPWIRE`: Out-of-distribution tripwire triggered.
- `RC_DISCLOSURE_BUDGET`: Disclosure budget exceeded.
- `RC_UNKNOWN`: Fallback for uncategorized deterministic failure.
