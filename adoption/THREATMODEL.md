# High-Level Threat Model

## Threats addressed
- **TOCTOU drift**: certified constraints change between planning and execution.
- **Policy drift**: runtime policy material differs from certified context.
- **Tamper evidence bypass**: digest mismatch or altered evidence capsule.
- **Verifier disagreement**: conflicting verification outcomes across independent validators.

## Mitigations
- Domain-separated hashing for all critical digests.
- Mandatory fallback with reason-code outputs.
- Effective-time and constraints binding checks at execution.
- Test vectors T1-T13 for repeatable conformance checks.
