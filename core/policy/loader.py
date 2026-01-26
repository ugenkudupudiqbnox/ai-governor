from __future__ import annotations

import yaml
from pathlib import Path
from typing import Any, Dict, Set

from core.policy.merge import merge_policies
from core.policy.errors import (
    PolicyInheritanceError,
    PolicyCycleError,
    PolicyVersionMismatchError,
)


def load_policy(
    path: str | Path,
    *,
    _visited: Set[Path] | None = None,
) -> Dict[str, Any]:
    """
    Load a policy file, resolve inheritance, and return a merged policy.

    - Supports single inheritance via `extends`
    - Detects cycles
    - Enforces version consistency
    """

    path = Path(path).resolve()
    _visited = _visited or set()

    if path in _visited:
        cycle = " → ".join(str(p.name) for p in list(_visited) + [path])
        raise PolicyCycleError(f"Policy inheritance cycle detected: {cycle}")

    _visited.add(path)

    try:
        with open(path, "r", encoding="utf-8") as f:
            policy = yaml.safe_load(f) or {}
    except Exception as e:
        raise PolicyInheritanceError(f"Failed to load policy {path}: {e}")

    if not isinstance(policy, dict):
        raise PolicyInheritanceError(f"Policy file {path} must be a YAML mapping")

    base_policy = {}

    extends = policy.get("extends")
    if extends:
        if not isinstance(extends, str):
            raise PolicyInheritanceError(
                f"`extends` must be a string path in {path}"
            )

        base_path = (path.parent / extends).resolve()
        base_policy = load_policy(base_path, _visited=_visited)

        # Version check (must match exactly)
        base_version = base_policy.get("version")
        child_version = policy.get("version")

        if base_version != child_version:
            raise PolicyVersionMismatchError(
                f"Policy version mismatch: base={base_version}, child={child_version} ({path})"
            )

    merged = merge_policies(base_policy, policy)
    merged.pop("extends", None)

    return merged

