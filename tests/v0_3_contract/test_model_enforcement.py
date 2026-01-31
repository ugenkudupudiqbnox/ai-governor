# DO NOT MODIFY — v0.3 CONTRACT TEST

from core.decision import DecisionType

def test_model_allow(orchestrator):
    result = orchestrator.enforce(
        {"version": "0.1", "model": {"allow": ["gpt-4.1"]}},
        requested_model="gpt-4.1",
        text="hello"
    )
    assert result["final_decision"].decision == DecisionType.ALLOW

def test_model_deny(orchestrator):
    result = orchestrator.enforce(
        {"version": "0.1", "model": {"deny": ["gpt-4.1"]}},
        requested_model="gpt-4.1",
        text="hello"
    )
    assert result["final_decision"].decision == DecisionType.BLOCK
