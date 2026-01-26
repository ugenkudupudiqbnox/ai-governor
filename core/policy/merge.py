from __future__ import annotations
from typing import Any, Dict


def merge_policies(base: Dict[str, Any], child: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge child policy onto base policy using v0.3 semantics.

    Rules:
    - Scalars: child overrides base
    - Dicts: deep merge
    - Lists (allow/deny): child replaces base
    - null: explicitly removes base field
    """

    result = dict(base)

    for key, child_value in child.items():
        if key == "extends":
            continue  # handled by loader

        # Explicit removal
        if child_value is None:
            result.pop(key, None)
            continue

        base_value = base.get(key)

        # Dict → deep merge
        if isinstance(base_value, dict) and isinstance(child_value, dict):
            result[key] = merge_policies(base_value, child_value)
            continue

        # List → replace
        if isinstance(child_value, list):
            result[key] = list(child_value)
            continue

        # Scalar → override
        result[key] = child_value

    return result

