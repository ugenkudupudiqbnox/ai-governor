import pytest
from core.policy_validator import validate_policy
from core.policy.errors import PolicyValidationError

# Example v0.1 policy (minimal)
v0_1_policy = {
    "version": "0.1",
    "model": {"allow": ["gpt-4"]},
}

# Example v0.2 policy (minimal, only allowed fields)
v0_2_policy = {
    "version": "0.2",
    "model": {"allow": ["gpt-4"]},
    "metadata": {"labels": {"env": "prod"}},
}

# Unknown version
unknown_version_policy = {
    "version": "9.9",
    "model": {"allow": ["gpt-4"]},
}

# v0.2 field in v0.1 policy
v0_1_with_v0_2_field = {
    "version": "0.1",
    "model": {"allow": ["gpt-4"]},
    "metadata": {"labels": {"env": "prod"}},
}

def test_v0_1_policy_validates():
    # Should pass validation
    validate_policy(v0_1_policy)

def test_v0_2_policy_validates():
    # Should pass validation
    validate_policy(v0_2_policy)

def test_unknown_version_fails():
    # Should fail validation
    with pytest.raises(PolicyValidationError):
        validate_policy(unknown_version_policy)

def test_v0_2_field_in_v0_1_fails():
    # Should fail validation
    with pytest.raises(PolicyValidationError):
        validate_policy(v0_1_with_v0_2_field)
