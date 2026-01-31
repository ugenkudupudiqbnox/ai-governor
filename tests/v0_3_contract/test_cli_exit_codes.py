
import subprocess
import sys
import tempfile
import textwrap
import os

def run_cli(args):
    return subprocess.run(
        [sys.executable, "-m", "ai_governor.cli"] + args,
        capture_output=True
    )

def test_cli_allow_exit_code(tmp_path):
    policy = tmp_path / "policy.yaml"
    policy.write_text("version: 0.1")
    result = subprocess.run(
        ["ai-governor", "enforce", "--policy", str(policy), "--model", "gpt-4.1", "--text", "hi"]
    )
    assert result.returncode == 0

def test_cli_block_exit_code(tmp_path):
    policy = tmp_path / "policy.yaml"
    policy.write_text("version: 0.1\nmodel:\n  deny: [gpt-4.1]")
    result = subprocess.run(
        ["ai-governor", "enforce", "--policy", str(policy), "--model", "gpt-4.1", "--text", "hi"]
    )
    assert result.returncode == 20
