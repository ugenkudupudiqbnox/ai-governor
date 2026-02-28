import pytest
from core.policy.errors import PolicyValidationError

def enforce_tool_policy(policy, tool_name, args):
    """
    Stub for enforcement. Do not implement logic.
    """
    raise NotImplementedError("Tool argument governance not implemented.")

# Example v0.2 policy with argument-level governance
policy = {
    "version": "0.2",
    "tools": {
        "allow": [
            {
                "name": "search",
                "args": {
                    "query": {"required": True, "type": "string"},
                    "limit": {"type": "int", "min": 1, "max": 100}
                }
            }
        ],
        "deny": ["delete"]
    }
}

def test_tool_allowed_with_valid_argument():
    # Should pass enforcement
    enforce_tool_policy(policy, "search", {"query": "foo", "limit": 10})

def test_tool_allowed_but_invalid_argument_blocks():
    # Should block enforcement (invalid argument type)
    with pytest.raises(PolicyValidationError):
        enforce_tool_policy(policy, "search", {"query": "foo", "limit": "bad_type"})

def test_missing_required_argument_blocks():
    # Should block enforcement (missing required argument)
    with pytest.raises(PolicyValidationError):
        enforce_tool_policy(policy, "search", {"limit": 10})

def test_deny_overrides_allow():
    # Should block enforcement (tool is denied)
    with pytest.raises(PolicyValidationError):
        enforce_tool_policy(policy, "delete", {"query": "foo"})
