import pytest
from core.policy.errors import PolicyValidationError

def validate_metadata_policy(policy):
    """
    Stub for metadata validation. Do not implement logic.
    """
    raise NotImplementedError("Metadata support not implemented.")

# v0.2 policy with valid metadata
policy_v2_with_metadata = {
    "version": "0.2",
    "model": {"allow": ["gpt-4"]},
    "metadata": {
        "labels": {"env": "prod", "team": "ai"}
    }
}

# v0.2 policy without metadata
policy_v2_no_metadata = {
    "version": "0.2",
    "model": {"allow": ["gpt-4"]}
}

# v0.1 policy with metadata (should fail)
policy_v1_with_metadata = {
    "version": "0.1",
    "model": {"allow": ["gpt-4"]},
    "metadata": {"labels": {"env": "prod"}}
}

# v0.2 policy with unknown metadata field (should fail)
policy_v2_with_unknown_metadata = {
    "version": "0.2",
    "model": {"allow": ["gpt-4"]},
    "metadata": {"unknown": "value"}
}

def test_v2_policy_with_metadata_labels():
    # Should pass validation
    validate_metadata_policy(policy_v2_with_metadata)

def test_v2_policy_without_metadata():
    # Should pass validation
    validate_metadata_policy(policy_v2_no_metadata)

def test_v1_policy_with_metadata_fails():
    # Should fail validation
    with pytest.raises(PolicyValidationError):
        validate_metadata_policy(policy_v1_with_metadata)

def test_v2_policy_with_unknown_metadata_fails():
    # Should fail validation
    with pytest.raises(PolicyValidationError):
        validate_metadata_policy(policy_v2_with_unknown_metadata)
