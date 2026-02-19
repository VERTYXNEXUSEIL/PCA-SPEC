from __future__ import annotations

from datetime import datetime

from .cert import build_pc_digest
from .reason_codes import (
    CONSTRAINTS_DIGEST_MISMATCH,
    CONSTRAINTS_VERSION_MISMATCH,
    LEGAL_EFFECTIVE_TIME_MISMATCH,
    RC_INTEGRITY_MISMATCH,
    VERIFY_ALLOW,
    VERIFY_CONFLICT,
)


def _dt(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def verify_pc(pc: dict, runtime: dict) -> tuple[str, str]:
    if runtime.get("expected_pc_digest") != build_pc_digest(pc):
        return "FALLBACK", RC_INTEGRITY_MISMATCH
    if runtime.get("constraints_version_id") != pc.get("constraints_version_id"):
        return "FALLBACK", CONSTRAINTS_VERSION_MISMATCH
    if runtime.get("constraints_digest") != pc.get("constraints_digest"):
        return "FALLBACK", CONSTRAINTS_DIGEST_MISMATCH

    now = _dt(runtime["now"])
    if not (_dt(pc["effective_time"]["not_before"]) <= now <= _dt(pc["effective_time"]["not_after"])):
        return "FALLBACK", LEGAL_EFFECTIVE_TIME_MISMATCH

    if runtime.get("verifier_conflict", False):
        return "FALLBACK", VERIFY_CONFLICT

    return "ALLOW", VERIFY_ALLOW
