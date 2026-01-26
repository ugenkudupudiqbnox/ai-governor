from __future__ import annotations

from typing import Any, Dict, Optional

from core.decision import Decision


def enforce_region_policy(
    policy: Dict[str, Any],
    region: Optional[str],
) -> Decision:
    """
    Enforce region / jurisdiction governance rules.

    Region must be explicitly provided by the caller.
    """

    data_policy = policy.get("data", {})
    region_policy = data_policy.get("regions")

    # No region policy → allow
    if not region_policy:
        return Decision.allow(
            reason="No region policy defined",
            policy_section="data.regions",
        )

    allowed_regions = region_policy.get("allowed")

    # Invalid policy shape (should be caught by validator)
    if not isinstance(allowed_regions, list):
        return Decision.block(
            reason="Invalid region policy configuration",
            policy_section="data.regions",
        )

    # Region not provided
    if not region:
        return Decision.block(
            reason="Request region not provided but region policy is enforced",
            policy_section="data.regions",
        )

    # Region not allowed
    if region not in allowed_regions:
        return Decision.block(
            reason=f"Region '{region}' is not allowed by policy",
            policy_section="data.regions",
            metadata={
                "region": region,
                "allowed_regions": allowed_regions,
            },
        )

    # Allowed
    return Decision.allow(
        reason=f"Region '{region}' is allowed by policy",
        policy_section="data.regions",
        metadata={"region": region},
    )

