from __future__ import annotations

from typing import Any, Dict, Optional

from core.decision import Decision


def enforce_tool_policy(
    policy: Dict[str, Any],
    *,
    tool_name: Optional[str],
) -> Decision:
    """
    Enforce tool / agent governance rules.

    This function does NOT execute tools.
    It only decides whether a tool invocation is allowed.
    """

    tools_policy = policy.get("tools")

    # No tool policy → allow
    if not tools_policy:
        return Decision.allow(
            reason="No tool governance policy defined",
            policy_section="tools",
        )

    if not tool_name:
        return Decision.allow(
            reason="No tool invocation requested",
            policy_section="tools",
        )

    allow = tools_policy.get("allow")
    deny = tools_policy.get("deny")

    # Explicit deny always wins
    if isinstance(deny, list) and tool_name in deny:
        return Decision.block(
            reason=f"Tool '{tool_name}' is explicitly denied by policy",
            policy_section="tools",
            metadata={"tool": tool_name},
        )

    # Allowlist enforcement
    if isinstance(allow, list):
        if tool_name not in allow:
            return Decision.block(
                reason=f"Tool '{tool_name}' is not allowed by policy",
                policy_section="tools",
                metadata={
                    "tool": tool_name,
                    "allowed_tools": allow,
                },
            )

    # Allowed
    return Decision.allow(
        reason=f"Tool '{tool_name}' is allowed by policy",
        policy_section="tools",
        metadata={"tool": tool_name},
    )

