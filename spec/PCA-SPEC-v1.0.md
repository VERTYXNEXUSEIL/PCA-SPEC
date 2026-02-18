# PCA-SPEC v1.0 (Normative)

## 1. Scope

Proof-Carrying Autonomy (PCA) / Certified Agentic Execution (CAE) specifies deterministic pre-execution verification with cryptographic evidence for autonomous actions.

## 2. Normative language

The words **MUST**, **SHOULD**, and **MAY** are normative.

## 3. Deterministic canonical encoding

Implementations MUST canonicalize JSON prior to hashing:

1. UTF-8 output bytes.
2. Object keys sorted lexicographically.
3. Array/list ordering preserved exactly as provided.
4. Numeric values MUST reject NaN/Infinity.
5. Numeric `-0` MUST normalize to `0`.
6. Absent optional fields MUST be deterministically omitted (not serialized as `null` unless required by schema).

Canonical encoding identifier for this version is `JCS-PCA-v1`.

## 4. Hash function and domain separation

Hash function identifier: `SHA-256`.

Domain separation labels are fixed strings:

- `STATEv1`
- `GOALv1`
- `CONSv1`
- `POLv1`
- `CFGv1`
- `STEPv1`
- `PLANv1`
- `PCv1`
- `AIRv1`

Digest construction MUST use `SHA-256(label || ":" || canonical_json_bytes(payload))`.

## 5. Required digests

The following digests are normative:

- `initial_state_digest`
- `goal_digest`
- `constraints_digest`
- optional `policy_digest`
- `planner_config_digest`
- `step_digest(i)` for each planned step
- `plan_digest` (linear digest of ordered step digests)
- `PC_digest`

Implementations MAY include Merkle root commitments for step digests in addition to linear `plan_digest`.

## 6. Constraints Fabric

A valid Plan Certificate (PC) MUST bind:

- `constraints_version_id`
- `constraints_digest`
- `effective_time` (`not_before`, `not_after`, RFC3339 UTC)

The executor MUST enforce all three at execution time.

## 7. Plan Certificate

A PC MUST include required fields defined in `schemas/pc.schema.json`, including:

- hash/canonical algorithm identifiers
- core digests
- decision + decision reason code
- evidence capsule

`PC_digest` MUST be computed over the canonical PC object excluding mutable signature containers.

## 8. Certified Execution Protocol

Executor pipeline:

1. Parse and schema-validate inputs.
2. Recompute and verify `PC_digest`.
3. Verify constraints version and digest.
4. Verify `effective_time` window.
5. Verify decision gates (DENY/ESCALATE/ALLOW policy).
6. Detect verifier conflicts and TOCTOU drift.
7. Return deterministic verdict and reason code.

Every verdict MUST include `reason_code`.

## 9. TOCTOU requirements

The executor MUST detect constraints/state changes between certification and execution. Any material mismatch MUST return fallback safe mode.

## 10. Hard gates

If plan decision is `ESCALATE`, execution authorization MUST be present (`escalation_authorized=true`). Otherwise executor MUST fallback.

## 11. Mandatory fallback triggers

Executor MUST produce `decision = FALLBACK` for at least:

- decision is `DENY`
- `ESCALATE` without authorization
- constraints version or digest mismatch
- integrity mismatch (`PC_digest` or proof hash mismatch)
- verifier conflict or non-deterministic resolution state
- TOCTOU mismatch

## 12. Conformance profiles (CAE-Mark)

- **Bronze**: canonical encoding, digest verification, constraints fabric enforcement, deterministic reason codes.
- **Silver**: Bronze + Merkle commitment/proof support + pass T1-T10.
- **Gold**: Silver + OOD/disclosure controls + pass T1-T13.

## 13. Test harness

Conformance claims MUST reference `spec/PCA-TEST-v1.md` and vectors in `test-vectors/vectors-v1/`.
