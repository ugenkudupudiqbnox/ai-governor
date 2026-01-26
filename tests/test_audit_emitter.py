from core.audit.emitter import AuditEventEmitter
from core.decision import Decision, DecisionType


def test_audit_event_emission(capsys):
    emitter = AuditEventEmitter()

    decision = Decision.block(
        reason="Test audit",
        policy_section="data.pii",
    )

    event = emitter.emit(
        decision,
        context={"request_id": "req-1", "actor": "unit-test"},
    )

    assert event.decision == DecisionType.BLOCK.value
    assert event.policy_section == "data.pii"
    assert event.context["request_id"] == "req-1"

    captured = capsys.readouterr()
    assert "llm_governance_decision" in captured.out

