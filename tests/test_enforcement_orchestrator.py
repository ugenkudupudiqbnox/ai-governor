from core.enforcement.orchestrator import EnforcementOrchestrator
from core.decision import DecisionType


BASE_POLICY = {
    "version": "0.1",
    "model": {
        "allow": ["gpt-4.1"],
        "deny": ["*-preview"],
        "max_tokens": 4096,
    },
    "data": {
        "pii": {"action": "redact"},
    },
}


def test_orchestrator_allow_flow():
    orchestrator = EnforcementOrchestrator()

    result = orchestrator.enforce(
        policy=BASE_POLICY,
        requested_model="gpt-4.1",
        requested_max_tokens=1024,
        text="Hello world",
        context={"request_id": "1"},
    )

    assert result["final_decision"].decision == DecisionType.ALLOW
    assert len(result["decisions"]) == 2


def test_orchestrator_modify_flow():
    orchestrator = EnforcementOrchestrator()

    result = orchestrator.enforce(
        policy=BASE_POLICY,
        requested_model="gpt-4.1",
        requested_max_tokens=1024,
        text="Contact me at test@example.com",
    )

    assert result["final_decision"].decision == DecisionType.MODIFY


def test_orchestrator_block_short_circuit():
    orchestrator = EnforcementOrchestrator()

    result = orchestrator.enforce(
        policy=BASE_POLICY,
        requested_model="gpt-4.1-preview",
        text="Contact me at test@example.com",
    )

    assert result["final_decision"].decision == DecisionType.BLOCK
    assert len(result["decisions"]) == 1

