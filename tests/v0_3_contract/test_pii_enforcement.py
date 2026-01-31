
from core.decision import DecisionType

def test_pii_redact(orchestrator):
    result = orchestrator.enforce(
        {"version": "0.1", "data": {"pii": {"action": "redact"}}},
        requested_model="gpt-4.1",
        text="email me at test@example.com"
    )
    assert result["final_decision"].decision == DecisionType.MODIFY
    assert "@" not in result["output_text"]

def test_pii_block(orchestrator):
    result = orchestrator.enforce(
        {"version": "0.1", "data": {"pii": {"action": "block"}}},
        requested_model="gpt-4.1",
        text="email me at test@example.com"
    )
    assert result["final_decision"].decision == DecisionType.BLOCK
