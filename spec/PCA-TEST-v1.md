# PCA-TEST v1

This document defines normative conformance tests T1-T13.

## Tests

1. **T1 PC Replay**: replayed certificate nonce/session MUST produce `FALLBACK` with execution-safe reason.
2. **T2 Domain Separation**: digest computed with wrong label MUST fail integrity checks.
3. **T3 Constraints Mismatch**: constraints version or digest mismatch MUST fallback.
4. **T4 Reason Stability**: same canonical failing input MUST produce same verdict and reason.
5. **T5 TOCTOU**: certification/execution drift MUST fallback.
6. **T6 Effective Time Mismatch**: out-of-window execution MUST fallback.
7. **T7 Optional-field canonical omission**: absent optionals MUST stay omitted for digest stability.
8. **T8 Conflict Detector**: verifier conflict MUST fallback.
9. **T9 Merkle Proof Verify**: invalid Merkle proof MUST fail integrity.
10. **T10 BRS Gate**: blast-radius threshold exceedance MUST deny/fallback.
11. **T11 OOD Tripwire**: OOD signal MUST deny/fallback.
12. **T12 Disclosure Budget**: budget overrun MUST deny/fallback.
13. **T13 Cross-Implementation Determinism**: independent implementations MUST match canonical digest/verdict outputs.

## Expected behavior

- Every failure path returns deterministic `reason_code` from `PCA-RC-v1`.
- Every successful path returns `ALLOW` with `VERIFY_ALLOW`.
- Mandatory fallback tests (T1, T3, T5, T6, T8) require `decision=FALLBACK`.

## Acceptance criteria

- Bronze: 100% pass on mandatory Bronze subset (T1-T8).
- Silver: 100% pass on T1-T10.
- Gold: 100% pass on all T1-T13.
