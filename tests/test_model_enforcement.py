from core.enforcement.model import enforce_model_policy
from core.decision import DecisionType


BASE_POLICY = {
    "version": "0.1",
    "model": {
        "allow": ["gpt-4.1", "llama-*"],
        "deny": ["*-preview"],
        "max_tokens": 4096,
    },
}


def test_allowed_model():
    decision = enforce_model_policy(
        BASE_POLICY,
        requested_model="gpt-4.1",
        requested_max_tokens=1024,
    )

    assert decision.decision == DecisionType.ALLOW


def test_denied_model_by_pattern():
    decision = enforce_model_policy(
        BASE_POLICY,
        requested_model="gpt-4.1-preview",
    )

    assert decision.decision == DecisionType.BLOCK
    assert decision.policy_section == "model.deny"


def test_model_not_in_allowlist():
    decision = enforce_model_policy(
        BASE_POLICY,
        requested_model="gpt-3.5",
    )

    assert decision.decision == DecisionType.BLOCK
    assert decision.policy_section == "model.allow"


def test_token_limit_exceeded():
    decision = enforce_model_policy(
        BASE_POLICY,
        requested_model="gpt-4.1",
        requested_max_tokens=8000,
    )

    assert decision.decision == DecisionType.BLOCK
    assert decision.policy_section == "model.max_tokens"

