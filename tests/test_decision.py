from core.decision import Decision, DecisionType


def test_block_decision_serialization():
    decision = Decision.block(
        reason="Test block",
        policy_section="test.section",
    )

    data = decision.to_dict()

    assert data["decision"] == DecisionType.BLOCK.value
    assert data["policy_section"] == "test.section"
    assert data["policy_version"] == "0.1"

