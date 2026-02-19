# PCA-TEST v1

Defines conformance tests T1-T13.

## Test set

- **T1 PC replay**: repeated nonce/session MUST trigger `RC_PC_REPLAY`.
- **T2 Domain separation**: wrong hash label MUST trigger `RC_DOMAIN_SEPARATION`.
- **T3 Constraints mismatch**: mismatched constraints digest/version MUST trigger `RC_CONSTRAINTS_MISMATCH`.
- **T4 Reason stability**: identical failing inputs MUST produce same reason code.
- **T5 TOCTOU**: state drift between check/use MUST trigger `RC_TOCTOU`.
- **T6 Effective time**: out-of-window execution MUST trigger `RC_EFFECTIVE_TIME`.
- **T7 Optional field omission**: canonicalization MUST not serialize absent optional fields.
- **T8 Conflict detector**: declared conflict MUST trigger `RC_CONFLICT`.
- **T9 Merkle proof**: invalid proof MUST trigger `RC_MERKLE_PROOF`.
- **T10 BRS gate**: threshold exceedance MUST trigger `RC_BRS_GATE`.
- **T11 OOD tripwire**: OOD flag MUST trigger `RC_OOD_TRIPWIRE`.
- **T12 Disclosure budget**: budget exceedance MUST trigger `RC_DISCLOSURE_BUDGET`.
- **T13 Cross-implementation determinism**: stable integer/string inputs MUST yield the same `expected_pc_digest` and `RC_OK` across conforming implementations.

## Acceptance criteria

- All mandatory tests pass for claimed conformance profile.
- Digests are deterministic across reruns.
- Failure verdicts are deterministic and reasoned.
