import pytest
from core.policy.errors import PolicyValidationError

def enforce_tool_policy(policy, tool_name, args):
    """
    Minimal tool argument validation for version 0.2.
    """
    tools = policy.get("tools", {})
    deny = set(tools.get("deny", []))
    if tool_name in deny:
        raise PolicyValidationError(f"Tool '{tool_name}' is denied.")
    allow = tools.get("allow", [])
    allowed_tool = None
    for entry in allow:
        if isinstance(entry, dict) and entry.get("name") == tool_name:
            allowed_tool = entry
            break
    if allowed_tool is None:
        raise PolicyValidationError(f"Tool '{tool_name}' is not allowed.")
    arg_spec = allowed_tool.get("args", {})
    # Check required arguments
    for arg, spec in arg_spec.items():
        if spec.get("required") and arg not in args:
            raise PolicyValidationError(f"Missing required argument: {arg}")
    # Check types and min/max
    for arg, value in args.items():
        if arg not in arg_spec:
            continue  # Ignore extra args
        spec = arg_spec[arg]
        expected_type = spec.get("type")
        if expected_type == "string" and not isinstance(value, str):
            raise PolicyValidationError(f"Argument '{arg}' must be string")
        if expected_type == "int":
            if not isinstance(value, int):
                raise PolicyValidationError(f"Argument '{arg}' must be int")
            if "min" in spec and value < spec["min"]:
                raise PolicyValidationError(f"Argument '{arg}' below min")
            if "max" in spec and value > spec["max"]:
                raise PolicyValidationError(f"Argument '{arg}' above max")
    # If all checks pass, allow
    return None

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
