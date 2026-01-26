from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from core.policy.loader import load_policy
from core.policy.errors import PolicyError


@dataclass
class ValidationResult:
    valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    policy: Optional[Dict[str, Any]] = None


class PolicyValidator:
    """
    Validates governance policies.

    In v0.3+, this includes resolving policy inheritance before validation.
    """

    SUPPORTED_VERSION = "0.1"

    def validate(
        self,
        policy: Dict[str, Any] | str,
    ) -> ValidationResult:
        """
        Validate a policy.

        Args:
            policy:
              - dict (already loaded)
              - or path to policy file (str)

        Returns:
            ValidationResult with merged policy attached on success.
        """

        errors: List[str] = []
        warnings: List[str] = []

        # ------------------------------------------------------------------
        # 1. Load + resolve inheritance (v0.3)
        # ------------------------------------------------------------------
        try:
            if isinstance(policy, str):
                resolved = load_policy(policy)
            elif isinstance(policy, dict):
                resolved = policy
            else:
                return ValidationResult(
                    valid=False,
                    errors=["Policy must be a dict or file path"],
                )
        except PolicyError as e:
            return ValidationResult(
                valid=False,
                errors=[str(e)],
            )

        # ------------------------------------------------------------------
        # 2. Schema-level validation
        # ------------------------------------------------------------------
        version = resolved.get("version")
        if version != self.SUPPORTED_VERSION:
            errors.append(
                f"Unsupported policy version '{version}'. "
                f"Expected '{self.SUPPORTED_VERSION}'."
            )

        # Model policy
        model = resolved.get("model", {})
        if not isinstance(model, dict):
            errors.append("model must be a mapping")

        # Data policy
        data = resolved.get("data", {})
        if not isinstance(data, dict):
            errors.append("data must be a mapping")

        # Region policy
        regions = data.get("regions")
        if regions is not None:
            allowed = regions.get("allowed")
            if not isinstance(allowed, list):
                errors.append("data.regions.allowed must be a list")

        # PII policy
        pii = data.get("pii")
        if pii is not None:
            action = pii.get("action")
            if action not in ("block", "redact"):
                errors.append(
                    "data.pii.action must be one of: block, redact"
                )

        # Tool policy (v0.3 prep – optional)
        tools = resolved.get("tools")
        if tools is not None and not isinstance(tools, dict):
            errors.append("tools must be a mapping")

        # ------------------------------------------------------------------
        # 3. Final result
        # ------------------------------------------------------------------
        return ValidationResult(
            valid=not errors,
            errors=errors,
            warnings=warnings,
            policy=resolved if not errors else None,
        )

