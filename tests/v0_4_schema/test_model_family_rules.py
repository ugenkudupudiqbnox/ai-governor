import pytest
from core.policy.errors import PolicyValidationError

def enforce_model_policy(policy, model_name):
    """
    Stub for enforcement. Do not implement logic.
    """
    raise NotImplementedError("Model family rules not implemented.")

# Example v0.2 policy with family rules
policy = {
    "version": "0.2",
    "model": {
        "allow": ["gpt-4"],
        "deny": ["gpt-4.1"],
        "families": {
            "gpt-4": {"allow": True},
            "gpt-3": {"deny": True}
        }
    }
}

def test_family_allow_passes():
    # Should pass enforcement (family allowed)
    enforce_model_policy(policy, "gpt-4-32k")

def test_family_deny_blocks():
    # Should block enforcement (family denied)
    with pytest.raises(PolicyValidationError):
        enforce_model_policy(policy, "gpt-3.5-turbo")

def test_explicit_deny_overrides_family_allow():
    # Should block enforcement (explicit deny overrides family allow)
    with pytest.raises(PolicyValidationError):
        enforce_model_policy(policy, "gpt-4.1")

def test_explicit_allow_overrides_family_deny():
    # Should pass enforcement (explicit allow overrides family deny)
    enforce_model_policy(policy, "gpt-4")
