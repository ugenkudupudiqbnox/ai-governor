from __future__ import annotations

from typing import Any, Dict, List, Optional

from core.decision import Decision, DecisionType
from core.policy_validator import PolicyValidator
from core.audit.emitter import AuditEventEmitter
from core.enforcement.model import enforce_model_policy
from core.enforcement.data import enforce_pii_policy
from core.redaction.engine import RedactionEngine
from core.enforcement.region import enforce_region_policy


class EnforcementOrchestrator:
    """
    Orchestrates governance enforcement in a deterministic order.

    This is the primary runtime entry point for ai-governor.
    """

    def __init__(
        self,
        audit_emitter: Optional[AuditEventEmitter] = None,
        policy_validator: Optional[PolicyValidator] = None,
        redaction_engine: Optional[RedactionEngine] = None,
    ):
        self.audit_emitter = audit_emitter or AuditEventEmitter()
        self.policy_validator = policy_validator or PolicyValidator()
        self.redaction_engine = redaction_engine or RedactionEngine()

    def enforce(
        self,
        policy: Dict[str, Any],
        *,
        requested_model: str,
        requested_max_tokens: Optional[int] = None,
        region: Optional[str] = None,
        text: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Execute governance enforcement and return the final result.

        Returns:
        {
          "final_decision": Decision,
          "decisions": List[Decision],
          "output_text": Optional[str]
        }
        """

        # ------------------------------------------------------------------
        # 1. Validate policy
        # ------------------------------------------------------------------
        validation = self.policy_validator.validate(policy)
        if not validation.valid:
            raise ValueError(f"Invalid policy: {validation.errors}")

        decisions: List[Decision] = []
        output_text: Optional[str] = text

        # ------------------------------------------------------------------
        # 2. Model enforcement
        # ------------------------------------------------------------------
        model_decision = enforce_model_policy(
            policy=policy,
            requested_model=requested_model,
            requested_max_tokens=requested_max_tokens,
        )

        decisions.append(model_decision)
        self.audit_emitter.emit(model_decision, context)

        if model_decision.decision == DecisionType.BLOCK:
            return self._finalize(model_decision, decisions, output_text)

        # ------------------------------------------------------------------
        # 3. Region enforcement
        # ------------------------------------------------------------------
        region_decision = enforce_region_policy(
            policy=policy,
            region=region,
        )

        decisions.append(region_decision)
        self.audit_emitter.emit(region_decision, context)

        if region_decision.decision == DecisionType.BLOCK:
            return self._finalize(region_decision, decisions, output_text)

        # ------------------------------------------------------------------
        # 4. PII / data enforcement
        # ------------------------------------------------------------------
        if text is not None:
            pii_decision = enforce_pii_policy(
                policy=policy,
                text=text,
            )

            decisions.append(pii_decision)
            self.audit_emitter.emit(pii_decision, context)

            # BLOCK short-circuits
            if pii_decision.decision == DecisionType.BLOCK:
                return self._finalize(pii_decision, decisions, output_text)

            # MODIFY triggers deterministic redaction
            if pii_decision.decision == DecisionType.MODIFY:
                redaction_result = self.redaction_engine.redact(text)

                # Replace last decision with enriched MODIFY decision
                pii_decision = Decision.modify(
                    reason=pii_decision.reason,
                    policy_section=pii_decision.policy_section,
                    policy_version=pii_decision.policy_version,
                    metadata={
                        **pii_decision.metadata,
                        "redacted_entities": redaction_result.redacted_entities,
                    },
                )

                decisions[-1] = pii_decision
                output_text = redaction_result.text

                return self._finalize(pii_decision, decisions, output_text)

        # ------------------------------------------------------------------
        # 5. Resolve final decision
        # ------------------------------------------------------------------
        final_decision = self._resolve_final(decisions)
        return self._finalize(final_decision, decisions, output_text)

    # ======================================================================
    # Helper methods
    # ======================================================================

    @staticmethod
    def _resolve_final(decisions: List[Decision]) -> Decision:
        """
        Resolve the final decision from a list of decisions.

        Priority order:
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
        output_text: Optional[str],
    ) -> Dict[str, Any]:
        return {
            "final_decision": final_decision,
            "decisions": decisions,
            "output_text": output_text,
        }

