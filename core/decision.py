from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict


class DecisionType(str, Enum):
    """
    Canonical governance decisions.

    This enum is intentionally closed.
    """
    ALLOW = "ALLOW"
    BLOCK = "BLOCK"
    MODIFY = "MODIFY"


@dataclass(frozen=True)
class Decision:
    """
    Represents the outcome of a governance policy evaluation.

    A Decision is immutable, auditable, and serializable.
    """

    decision: DecisionType
    reason: str
    policy_section: str
    policy_version: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the Decision into a JSON-serializable dictionary.
        """
        return {
            "decision": self.decision.value,
            "reason": self.reason,
            "policy_section": self.policy_section,
            "policy_version": self.policy_version,
            "metadata": self.metadata or {},
        }

    @classmethod
    def allow(
        cls,
        reason: str,
        policy_section: str,
        policy_version: str = "0.1",
        metadata: Dict[str, Any] | None = None,
    ) -> "Decision":
        return cls(
            decision=DecisionType.ALLOW,
            reason=reason,
            policy_section=policy_section,
            policy_version=policy_version,
            metadata=metadata or {},
        )

    @classmethod
    def block(
        cls,
        reason: str,
        policy_section: str,
        policy_version: str = "0.1",
        metadata: Dict[str, Any] | None = None,
    ) -> "Decision":
        return cls(
            decision=DecisionType.BLOCK,
            reason=reason,
            policy_section=policy_section,
            policy_version=policy_version,
            metadata=metadata or {},
        )

    @classmethod
    def modify(
        cls,
        reason: str,
        policy_section: str,
        policy_version: str = "0.1",
        metadata: Dict[str, Any] | None = None,
    ) -> "Decision":
        return cls(
            decision=DecisionType.MODIFY,
            reason=reason,
            policy_section=policy_section,
            policy_version=policy_version,
            metadata=metadata or {},
        )

