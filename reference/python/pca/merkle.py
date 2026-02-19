from __future__ import annotations

from .hashing import LABELS, ds_hash


def build_merkle_root(step_digests: list[str]) -> str:
    if not step_digests:
        return ds_hash(LABELS["plan"], {"empty": True})

    layer = step_digests[:]
    while len(layer) > 1:
        next_layer: list[str] = []
        for index in range(0, len(layer), 2):
            left = layer[index]
            right = layer[index + 1] if index + 1 < len(layer) else left
            next_layer.append(ds_hash(LABELS["plan"], {"left": left, "right": right}))
        layer = next_layer
    return layer[0]


__all__ = ["build_merkle_root"]
