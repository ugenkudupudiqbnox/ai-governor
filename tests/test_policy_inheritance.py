import tempfile
from pathlib import Path

import yaml
import pytest

from core.policy.loader import load_policy
from core.policy.errors import PolicyCycleError, PolicyVersionMismatchError


def write_policy(tmp: Path, name: str, content: dict):
    path = tmp / name
    with open(path, "w") as f:
        yaml.dump(content, f)
    return path


def test_simple_inheritance(tmp_path):
    base = write_policy(
        tmp_path,
        "base.yaml",
        {
            "version": "0.1",
            "model": {"allow": ["gpt-4.1"]},
        },
    )

    child = write_policy(
        tmp_path,
        "child.yaml",
        {
            "version": "0.1",
            "extends": "base.yaml",
            "model": {"allow": ["gpt-4.1", "gpt-4.2"]},
        },
    )

    merged = load_policy(child)
    assert merged["model"]["allow"] == ["gpt-4.1", "gpt-4.2"]


def test_null_removal(tmp_path):
    base = write_policy(
        tmp_path,
        "base.yaml",
        {
            "version": "0.1",
            "model": {"deny": ["*-preview"]},
        },
    )

    child = write_policy(
        tmp_path,
        "child.yaml",
        {
            "version": "0.1",
            "extends": "base.yaml",
            "model": {"deny": None},
        },
    )

    merged = load_policy(child)
    assert "deny" not in merged["model"]


def test_cycle_detection(tmp_path):
    write_policy(
        tmp_path,
        "a.yaml",
        {"version": "0.1", "extends": "b.yaml"},
    )
    write_policy(
        tmp_path,
        "b.yaml",
        {"version": "0.1", "extends": "a.yaml"},
    )

    with pytest.raises(PolicyCycleError):
        load_policy(tmp_path / "a.yaml")


def test_version_mismatch(tmp_path):
    base = write_policy(
        tmp_path,
        "base.yaml",
        {"version": "0.1"},
    )
    child = write_policy(
        tmp_path,
        "child.yaml",
        {"version": "0.2", "extends": "base.yaml"},
    )

    with pytest.raises(PolicyVersionMismatchError):
        load_policy(child)

