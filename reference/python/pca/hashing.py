import hashlib

from .canonical import canonical_json_bytes


def ds_hash(label: str, payload: object) -> str:
    material = label.encode("utf-8") + b":" + canonical_json_bytes(payload)
    return hashlib.sha256(material).hexdigest()
