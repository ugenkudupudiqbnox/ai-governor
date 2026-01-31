
import pytest
from core.policy_validator import PolicyValidator

def test_valid_minimal_policy():
    PolicyValidator().validate({"version": "0.1"})

def test_missing_version_fails():
    with pytest.raises(Exception):
        PolicyValidator().validate({})

def test_unknown_key_fails():
    with pytest.raises(Exception):
        PolicyValidator().validate({"version": "0.1", "unknown": {}})
