# PCA FAQ

## How is PCA/CAE different from guardrails?

Guardrails are often runtime filters. PCA/CAE adds cryptographic binding between plan intent, policy constraints, and execution checks, producing auditable deterministic evidence.

## What is TOCTOU in this context?

TOCTOU means an action passed checks on one observed state but is used later on a materially changed state. PCA/CAE requires fail-closed fallback when this drift is detected.

## Why does canonical encoding matter?

Without canonical encoding, semantically equivalent JSON can hash differently across implementations. PCA/CAE requires canonicalization to guarantee reproducible digests and interoperable certification.
