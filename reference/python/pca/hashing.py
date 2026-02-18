import hashlib

from .canonical import canonical_json_bytes

LABELS = {
    "state": "STATEv1",
    "goal": "GOALv1",
    "constraints": "CONSv1",
    "policy": "POLv1",
    "config": "CFGv1",
    "step": "STEPv1",
    "plan": "PLANv1",
    "pc": "PCv1",
    "air": "AIRv1",
}


def ds_hash(label: str, payload: object) -> str:
    return hashlib.sha256(label.encode() + b":" + canonical_json_bytes(payload)).hexdigest()
