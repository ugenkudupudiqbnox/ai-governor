from __future__ import annotations

from typing import Any, Dict, List, Optional

from core.decision import Decision, DecisionType
from core.policy_validator import PolicyValidator
from core.audit.emitter import AuditEventEmitter
from core.enforcement.model import enforce_model_policy
from core.enforcement.data import enforce_pii_policy


class EnforcementOrchestrator:
    """
    Orchestrates governance enforcement in a deterministic order.

    This is the main runtime entry point for ai-governor.
    """

    def __init__(
        self,
        audit_emitter: Optional[AuditEventEmitter] = None,
        policy_validator: Optional[PolicyValidator] = None,
    ):
        self.audit_emitter = audit_emitter or AuditEventEmitter()
        self.policy_validator = policy_validator or PolicyValidator()

    def enforce(
        self,
        policy: Dict[str, Any],
        *,
        requested_model: str,
        requested_max_tokens: Optional[int] = None,
        text: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Run governance enforcement and return final decision + trace.
        """

        # --- validate policy ---
        validation = self.policy_validator.validate(policy)
        if not validation.valid:
            raise ValueError(
                f"Invalid policy: {validation.errors}"
            )

        decisions: List[Decision] = []

        # --- 1. model enforcement ---
        model_decision = enforce_model_policy(
            policy=policy,
            requested_model=requested_model,
            requested_max_tokens=requested_max_tokens,
        )
        decisions.append(model_decision)
        self.audit_emitter.emit(model_decision, context)

        if model_decision.decision == DecisionType.BLOCK:
            return self._finalize(model_decision, decisions)

        # --- 2. PII enforcement (text optional) ---
        if text is not None:
            pii_decision = enforce_pii_policy(
                policy=policy,
                text=text,
            )
            decisions.append(pii_decision)
            self.audit_emitter.emit(pii_decision, context)

            if pii_decision.decision == DecisionType.BLOCK:
                return self._finalize(pii_decision, decisions)

        # --- final decision ---
        final_decision = self._resolve_final(decisions)
        return self._finalize(final_decision, decisions)

    # ---------------- helpers ----------------

    @staticmethod
    def _resolve_final(decisions: List[Decision]) -> Decision:
        """
        Determine the final decision from all enforcement steps.

        BLOCK > MODIFY > ALLOW
        """
        for decision in decisions:
            if decision.decision == DecisionType.BLOCK:
                return decision

        for decision in decisions:
            if decision.decision == DecisionType.MODIFY:
                return decision

        return decisions[-1]

    @staticmethod
    def _finalize(
        final_decision: Decision,
        decisions: List[Decision],
    ) -> Dict[str, Any]:
        return {
            "final_decision": final_decision,
            "decisions": decisions,
        }

