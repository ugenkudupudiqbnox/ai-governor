from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from core.decision import Decision
from core.audit.sinks import AuditSink, StdoutSink


@dataclass
class AuditEvent:
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


class AuditEventEmitter:
    """
    Emits audit events to one or more sinks.
    """

    EVENT_TYPE = "llm_governance_decision"

    def __init__(self, sinks: Optional[List[AuditSink]] = None):
        self.sinks = sinks or [StdoutSink()]

    def emit(
        self,
        decision: Decision,
        context: Optional[Dict[str, Any]] = None,
    ) -> AuditEvent:
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

        payload = event.to_dict()

        for sink in self.sinks:
            sink.write(payload)

        return event

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat()

