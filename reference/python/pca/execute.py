from __future__ import annotations

from .reason_codes import (
    DISCLOSURE_BUDGET_EXCEEDED,
    EXEC_DENY_GATE,
    EVIDENCE_HASH_MISMATCH,
    EXEC_FALLBACK_SAFE_MODE,
    OOD_TRIGGERED,
    RISK_BLAST_RADIUS_EXCEEDED,
)
from .verify import verify_pc


def execute_certified(pc: dict, runtime: dict) -> dict:
    verdict, reason = verify_pc(pc, runtime)
    if verdict == "FALLBACK":
        return {"decision": "FALLBACK", "reason_code": reason}

    if pc.get("decision") == "DENY":
        return {"decision": "FALLBACK", "reason_code": EXEC_DENY_GATE}
    if pc.get("decision") == "ESCALATE" and not runtime.get("escalation_authorized", False):
        return {"decision": "FALLBACK", "reason_code": EXEC_FALLBACK_SAFE_MODE}
    if runtime.get("toctou_drift", False):
        return {"decision": "FALLBACK", "reason_code": EXEC_FALLBACK_SAFE_MODE}
    if runtime.get("merkle_proof_ok") is False:
        return {"decision": "FALLBACK", "reason_code": EVIDENCE_HASH_MISMATCH}
    if runtime.get("brs_score", 0) > runtime.get("brs_limit", 100):
        return {"decision": "FALLBACK", "reason_code": RISK_BLAST_RADIUS_EXCEEDED}
    if runtime.get("ood", False):
        return {"decision": "FALLBACK", "reason_code": OOD_TRIGGERED}
    if runtime.get("disclosure_used", 0) > runtime.get("disclosure_budget", 10**9):
        return {"decision": "FALLBACK", "reason_code": DISCLOSURE_BUDGET_EXCEEDED}
    return {"decision": "ALLOW", "reason_code": reason}
