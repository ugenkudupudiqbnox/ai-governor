from core.enforcement.tools import enforce_tool_policy
from core.decision import DecisionType


BASE_POLICY = {
    "version": "0.1",
    "tools": {
        "allow": ["search", "summarize"],
        "deny": ["execute_code"],
    },
}


def test_no_tools_policy():
    decision = enforce_tool_policy(
        policy={"version": "0.1"},
        tool_name="search",
    )
    assert decision.decision == DecisionType.ALLOW


def test_no_tool_invoked():
    decision = enforce_tool_policy(
        policy=BASE_POLICY,
        tool_name=None,
    )
    assert decision.decision == DecisionType.ALLOW


def test_tool_denied():
    decision = enforce_tool_policy(
        policy=BASE_POLICY,
        tool_name="execute_code",
    )
    assert decision.decision == DecisionType.BLOCK


def test_tool_not_in_allowlist():
    decision = enforce_tool_policy(
        policy=BASE_POLICY,
        tool_name="http_request",
    )
    assert decision.decision == DecisionType.BLOCK


def test_tool_allowed():
    decision = enforce_tool_policy(
        policy=BASE_POLICY,
        tool_name="search",
    )
    assert decision.decision == DecisionType.ALLOW

