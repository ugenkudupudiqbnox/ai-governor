from __future__ import annotations

import fnmatch
from typing import Any, Dict, Optional

from core.decision import Decision


def enforce_model_policy(
    policy: Dict[str, Any],
    requested_model: str,
    requested_max_tokens: Optional[int] = None,
) -> Decision:
    """
    Enforce model allow/deny rules defined in the policy.

    Returns a Decision indicating whether the requested model
    may be used.
    """

    model_policy = policy.get("model")

    # No model policy → allow by default
    if not model_policy:
        return Decision.allow(
            reason="No model policy defined",
            policy_section="model",
        )

    allow_list = model_policy.get("allow", [])
    deny_list = model_policy.get("deny", [])
    max_tokens = model_policy.get("max_tokens")

    # Deny always wins
    for pattern in deny_list:
        if fnmatch.fnmatch(requested_model, pattern):
            return Decision.block(
                reason=f"Model '{requested_model}' is explicitly denied by policy",
                policy_section="model.deny",
                metadata={"model": requested_model, "matched_pattern": pattern},
            )

    # If allow list exists, model must match
    if allow_list:
        allowed = any(
            fnmatch.fnmatch(requested_model, pattern)
            for pattern in allow_list
        )
        if not allowed:
            return Decision.block(
                reason=f"Model '{requested_model}' is not in allowlist",
                policy_section="model.allow",
                metadata={"model": requested_model},
            )

    # Token limit enforcement (if applicable)
    if max_tokens is not None and requested_max_tokens is not None:
        if requested_max_tokens > max_tokens:
            return Decision.block(
                reason=(
                    f"Requested max_tokens ({requested_max_tokens}) "
                    f"exceeds policy limit ({max_tokens})"
                ),
                policy_section="model.max_tokens",
                metadata={
                    "requested_max_tokens": requested_max_tokens,
                    "policy_max_tokens": max_tokens,
                },
            )

    return Decision.allow(
        reason="Model is permitted by policy",
        policy_section="model",
        metadata={"model": requested_model},
    )

