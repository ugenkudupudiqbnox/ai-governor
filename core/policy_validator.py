from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Set


SUPPORTED_VERSION = "0.1"

KNOWN_TOP_LEVEL_KEYS: Set[str] = {
    "version",
    "metadata",
    "model",
    "access",
    "data",
    "safety",
    "logging",
    "enforcement",
}

VALID_PII_ACTIONS = {"block", "redact", "allow"}
VALID_ENFORCEMENT_ACTIONS = {"block", "modify", "warn"}


@dataclass
class PolicyValidationResult:
    valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


class PolicyValidator:
    """
    Validates ai-governor policies against schema v0.1.

    This validator checks structure and semantics,
    not runtime enforcement behavior.
    """

    def validate(self, policy: Dict[str, Any]) -> PolicyValidationResult:
        errors: List[str] = []
        warnings: List[str] = []

        # --- version ---
        version = policy.get("version")
        if version != SUPPORTED_VERSION:
            errors.append(
                f"Invalid or missing policy version: expected '{SUPPORTED_VERSION}', got '{version}'"
            )

        # --- unknown top-level keys ---
        for key in policy.keys():
            if key not in KNOWN_TOP_LEVEL_KEYS:
                warnings.append(f"Unknown top-level key: '{key}'")

        # --- model section ---
        model = policy.get("model")
        if model is not None:
            if not isinstance(model, dict):
                errors.append("model must be a mapping")
            else:
                self._validate_model(model, errors, warnings)

        # --- access section ---
        access = policy.get("access")
        if access is not None:
            if not isinstance(access, dict):
                errors.append("access must be a mapping")
            else:
                roles = access.get("roles")
                if roles is not None and not isinstance(roles, list):
                    errors.append("access.roles must be a list")

        # --- data section ---
        data = policy.get("data")
        if data is not None:
            if not isinstance(data, dict):
                errors.append("data must be a mapping")
            else:
                self._validate_data(data, errors)

        # --- safety section ---
        safety = policy.get("safety")
        if safety is not None:
            if not isinstance(safety, dict):
                errors.append("safety must be a mapping")
            else:
                topics = safety.get("disallowed_topics")
                if topics is not None and not isinstance(topics, list):
                    errors.append("safety.disallowed_topics must be a list")

        # --- logging section ---
        logging_cfg = policy.get("logging")
        if logging_cfg is not None:
            if not isinstance(logging_cfg, dict):
                errors.append("logging must be a mapping")
            else:
                self._validate_logging(logging_cfg, errors)

        # --- enforcement section ---
        enforcement = policy.get("enforcement")
        if enforcement is not None:
            if not isinstance(enforcement, dict):
                errors.append("enforcement must be a mapping")
            else:
                action = enforcement.get("on_violation")
                if action is not None and action not in VALID_ENFORCEMENT_ACTIONS:
                    errors.append(
                        f"enforcement.on_violation must be one of {VALID_ENFORCEMENT_ACTIONS}"
                    )

        return PolicyValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
        )

    # ----------------- helpers -----------------

    def _validate_model(
        self,
        model: Dict[str, Any],
        errors: List[str],
        warnings: List[str],
    ) -> None:
        allow = model.get("allow")
        deny = model.get("deny")

        if allow is not None and not isinstance(allow, list):
            errors.append("model.allow must be a list")

        if deny is not None and not isinstance(deny, list):
            errors.append("model.deny must be a list")

        if allow and deny:
            overlap = set(allow) & set(deny)
            if overlap:
                warnings.append(
                    f"Models appear in both allow and deny lists: {sorted(overlap)}"
                )

        max_tokens = model.get("max_tokens")
        if max_tokens is not None:
            if not isinstance(max_tokens, int) or max_tokens <= 0:
                errors.append("model.max_tokens must be a positive integer")

    def _validate_data(self, data: Dict[str, Any], errors: List[str]) -> None:
        pii = data.get("pii")
        if pii is not None:
            if not isinstance(pii, dict):
                errors.append("data.pii must be a mapping")
            else:
                action = pii.get("action")
                if action not in VALID_PII_ACTIONS:
                    errors.append(
                        f"data.pii.action must be one of {VALID_PII_ACTIONS}"
                    )

        regions = data.get("regions")
        if regions is not None:
            if not isinstance(regions, dict):
                errors.append("data.regions must be a mapping")
            else:
                allowed = regions.get("allowed")
                if allowed is not None and not isinstance(allowed, list):
                    errors.append("data.regions.allowed must be a list")

    def _validate_logging(self, logging_cfg: Dict[str, Any], errors: List[str]) -> None:
        for key in ("store_prompts", "store_outputs"):
            if key in logging_cfg and not isinstance(logging_cfg[key], bool):
                errors.append(f"logging.{key} must be a boolean")

        retention = logging_cfg.get("retention_days")
        if retention is not None:
            if not isinstance(retention, int) or retention <= 0:
                errors.append("logging.retention_days must be a positive integer")

