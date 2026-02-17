# PCA-SPEC v1.0 (Normative)

## 1. Status

This document defines the normative v1.0 technical standard for Proof-Carrying Autonomy (PCA) / Certified Agentic Execution (CAE).

## 2. Conformance language

The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** are normative.

## 3. Core objects

- **Action IR (AIR)**: canonical intermediate representation of an intended action.
- **Constraints**: policy-governed execution envelope identified by version and digest.
- **Plan Certificate (PC)**: signed or attestable object binding planning evidence to execution checks.
- **Evidence Capsule**: structured provenance envelope with proofs.

## 4. Canonical encoding

Implementations MUST canonicalize JSON before hashing:

1. UTF-8 encoding.
2. Object keys sorted lexicographically.
3. No NaN or Infinity numeric values.
4. Numeric `-0` normalized to `0`.
5. Optional fields absent from source data MUST be omitted (not serialized as `null`) unless schema requires explicit nullability.

## 5. Domain-separated hashing

All digests MUST use SHA-256 over `label || ":" || canonical_bytes` with labels:

`STATEv1`, `GOALv1`, `CONSv1`, `POLv1`, `CFGv1`, `STEPv1`, `PLANv1`, `PCv1`, `AIRv1`.

## 6. Digest construction

### 6.1 Step digest

`step_digest_i = H("STEPv1", {state_digest, goal_digest, constraints_digest, policy_digest, config_digest, air_digest})`

### 6.2 Plan digest (linear)

`plan_digest = H("PLANv1", {step_digest_1, ..., step_digest_n})`

Implementations MAY additionally compute Merkle roots over `step_digest_i`; if present, Merkle rules MUST be documented and deterministic.

### 6.3 PC digest

`pc_digest = H("PCv1", canonical_pc_without_signature_fields)`

Signature or attestation fields MUST NOT influence `pc_digest`.

## 7. Constraint binding

PC MUST include:

- `constraints_version_id`
- `constraints_digest`
- `effective_time` (RFC3339 interval bounds)

Execution MUST reject mismatched version/digest and out-of-window timestamps.

## 8. Certified execution protocol

1. Recompute `pc_digest`.
2. Verify constraints version and digest.
3. Verify `effective_time` validity.
4. Evaluate conflict and tripwire checks.
5. Emit deterministic verdict and reason code.

If any mandatory check fails, executor MUST output `decision = "FALLBACK"` and attach a stable reason code from `PCA-RC-v1`.

## 9. TOCTOU and fallback requirements

Executors MUST detect material state drift between plan-time assertions and execution-time observations. On drift, execution MUST fail closed to fallback.

## 10. Reason codes

Reason codes are normative identifiers and MUST be stable once published. See `PCA-RC-v1.md`.

## 11. Conformance profiles

- **Bronze**: linear plan digest, mandatory checks, reason codes.
- **Silver**: Bronze + Merkle support + vector conformance T1–T10.
- **Gold**: Silver + OOD tripwire + disclosure budget + full T1–T13.

## 12. Test harness

Implementations claiming conformance MUST run `PCA-TEST v1` and publish pass/fail evidence.
