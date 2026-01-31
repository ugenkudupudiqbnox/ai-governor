from core.policy_validator import PolicyValidator


def test_valid_base_policy():
    policy = {
        "version": "0.1",
        "model": {
            "allow": ["gpt-4.1"],
            "deny": ["*-preview"],
            "max_tokens": 2048,
        },
        "data": {
            "pii": {"action": "redact"},
        },
    }

    result = PolicyValidator().validate(policy)

    assert result.valid is True
    assert result.errors == []


def test_invalid_pii_action():
    policy = {
        "version": "0.1",
        "data": {
            "pii": {"action": "delete"},
        },
    }

    result = PolicyValidator().validate(policy)

    assert result.valid is False
    assert "data.pii.action" in result.errors[0]

