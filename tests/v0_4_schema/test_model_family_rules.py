import pytest
from core.policy.errors import PolicyValidationError

def enforce_model_policy(policy, model_name):
    """
    Minimal model family evaluation for v0.2 spec.
    deny must override allow. Explicit model rules override family rules.
    """
    from core.policy.errors import PolicyValidationError
    model_section = policy.get("model", {})
    allow = set(model_section.get("allow", []))
    deny = set(model_section.get("deny", []))
    families = model_section.get("families", {})

    # Explicit deny overrides everything
    if model_name in deny:
        raise PolicyValidationError(f"Model {model_name} is explicitly denied.")
    # Explicit allow overrides family deny
    if model_name in allow:
        return None

    # Family rules
    family = None
    for fam in families:
        if model_name.startswith(fam):
            family = fam
            break
    if family:
        fam_rule = families[family]
        if fam_rule.get("deny"):
            raise PolicyValidationError(f"Model family {family} is denied.")
        if fam_rule.get("allow"):
            return None

    # Default: block if not explicitly allowed
    raise PolicyValidationError(f"Model {model_name} is not allowed.")

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
