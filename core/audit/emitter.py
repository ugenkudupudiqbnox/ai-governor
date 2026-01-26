from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from core.decision import Decision


@dataclass
class AuditEvent:
    """
    Immutable audit record representing a governance decision.
    """

    event_type: str
    timestamp: str
    decision: str
    reason: str
    policy_section: str
    policy_version: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    context: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_type": self.event_type,
            "timestamp": self.timestamp,
            "decision": self.decision,
            "reason": self.reason,
            "policy_section": self.policy_section,
            "policy_version": self.policy_version,
            "metadata": self.metadata,
            "context": self.context,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True)


class AuditEventEmitter:
    """
    Emits audit events for governance decisions.

    Default implementation writes to stdout.
    Storage backends can be plugged in later.
    """

    EVENT_TYPE = "llm_governance_decision"

    def emit(
        self,
        decision: Decision,
        context: Optional[Dict[str, Any]] = None,
    ) -> AuditEvent:
        """
        Create and emit an audit event from a Decision.
        """

        event = AuditEvent(
            event_type=self.EVENT_TYPE,
            timestamp=self._now(),
            decision=decision.decision.value,
            reason=decision.reason,
            policy_section=decision.policy_section,
            policy_version=decision.policy_version,
            metadata=decision.metadata,
            context=context or {},
        )

        self._write(event)
        return event

    def _write(self, event: AuditEvent) -> None:
        """
        Write audit event to the sink.

        Default: stdout (safe, visible, testable).
        """
        print(event.to_json())

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat()

