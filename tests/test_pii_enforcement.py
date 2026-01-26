from core.enforcement.data import enforce_pii_policy
from core.decision import DecisionType


BASE_POLICY_REDACT = {
    "version": "0.1",
    "data": {
        "pii": {"action": "redact"},
    },
}

BASE_POLICY_BLOCK = {
    "version": "0.1",
    "data": {
        "pii": {"action": "block"},
    },
}


def test_no_pii_detected():
    decision = enforce_pii_policy(
        BASE_POLICY_REDACT,
        text="Hello world",
    )

    assert decision.decision == DecisionType.ALLOW


def test_pii_redaction():
    decision = enforce_pii_policy(
        BASE_POLICY_REDACT,
        text="Contact me at test@example.com",
    )

    assert decision.decision == DecisionType.MODIFY
    assert "email" in decision.metadata["detected_entities"]


def test_pii_blocking():
    decision = enforce_pii_policy(
        BASE_POLICY_BLOCK,
        text="My phone number is 9876543210",
    )

    assert decision.decision == DecisionType.BLOCK
    assert "phone" in decision.metadata["detected_entities"]

