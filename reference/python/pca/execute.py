from __future__ import annotations

from .reason_codes import (
    RC_BRS_GATE,
    RC_CONFLICT,
    RC_DISCLOSURE_BUDGET,
    RC_OOD_TRIPWIRE,
    RC_PC_REPLAY,
    RC_TOCTOU,
)
from .verify import verify_pc


def execute_certified(pc: dict, runtime: dict, seen_nonces: set[str] | None = None) -> dict:
    if seen_nonces is None:
        seen_nonces = set()

    nonce = pc.get("nonce")
    if nonce in seen_nonces:
        return {"decision": "FALLBACK", "reason_code": RC_PC_REPLAY}
    seen_nonces.add(nonce)

    decision, reason = verify_pc(pc, runtime)
    if decision == "FALLBACK":
        return {"decision": decision, "reason_code": reason}

    if runtime.get("toctou_drift", False):
        return {"decision": "FALLBACK", "reason_code": RC_TOCTOU}
    if runtime.get("conflict", False):
        return {"decision": "FALLBACK", "reason_code": RC_CONFLICT}
    if runtime.get("merkle_ok") is False:
        return {"decision": "FALLBACK", "reason_code": "RC_MERKLE_PROOF"}
    if runtime.get("brs_score", 0) > runtime.get("brs_threshold", 100):
        return {"decision": "FALLBACK", "reason_code": RC_BRS_GATE}
    if runtime.get("ood", False):
        return {"decision": "FALLBACK", "reason_code": RC_OOD_TRIPWIRE}
    if runtime.get("disclosure_used", 0) > runtime.get("disclosure_budget", 999999):
        return {"decision": "FALLBACK", "reason_code": RC_DISCLOSURE_BUDGET}

    return {"decision": "EXECUTE", "reason_code": reason}
