
from core.decision import DecisionType

def test_region_allowed(orchestrator):
    result = orchestrator.enforce(
        {"version": "0.1", "data": {"regions": {"allowed": ["IN"]}}},
        requested_model="gpt-4.1",
        region="IN",
        text="hello"
    )
    assert result["final_decision"].decision == DecisionType.ALLOW

def test_region_blocked(orchestrator):
    result = orchestrator.enforce(
        {"version": "0.1", "data": {"regions": {"allowed": ["IN"]}}},
        requested_model="gpt-4.1",
        region="US",
        text="hello"
    )
    assert result["final_decision"].decision == DecisionType.BLOCK
