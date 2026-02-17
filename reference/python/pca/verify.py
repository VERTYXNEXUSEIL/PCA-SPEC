from __future__ import annotations

from datetime import datetime

from .cert import build_pc_digest
from .reason_codes import RC_CONSTRAINTS_MISMATCH, RC_DOMAIN_SEPARATION, RC_EFFECTIVE_TIME, RC_OK


def _parse_time(ts: str) -> datetime:
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def verify_pc(pc: dict, runtime: dict) -> tuple[str, str]:
    recomputed = build_pc_digest(pc)
    if runtime.get("expected_pc_digest") and runtime["expected_pc_digest"] != recomputed:
        return "FALLBACK", RC_DOMAIN_SEPARATION

    if runtime.get("constraints_version_id") != pc.get("constraints_version_id"):
        return "FALLBACK", RC_CONSTRAINTS_MISMATCH
    if runtime.get("constraints_digest") != pc.get("constraints_digest"):
        return "FALLBACK", RC_CONSTRAINTS_MISMATCH

    now = _parse_time(runtime["now"])
    nb = _parse_time(pc["effective_time"]["not_before"])
    na = _parse_time(pc["effective_time"]["not_after"])
    if not (nb <= now <= na):
        return "FALLBACK", RC_EFFECTIVE_TIME

    return "EXECUTE", RC_OK
