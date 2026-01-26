from core.enforcement.region import enforce_region_policy
from core.decision import DecisionType


BASE_POLICY = {
    "version": "0.1",
    "data": {
        "regions": {
            "allowed": ["IN", "EU"]
        }
    }
}


def test_no_region_policy():
    decision = enforce_region_policy(
        policy={"version": "0.1"},
        region="IN",
    )
    assert decision.decision == DecisionType.ALLOW


def test_region_missing():
    decision = enforce_region_policy(
        policy=BASE_POLICY,
        region=None,
    )
    assert decision.decision == DecisionType.BLOCK


def test_region_not_allowed():
    decision = enforce_region_policy(
        policy=BASE_POLICY,
        region="US",
    )
    assert decision.decision == DecisionType.BLOCK
    assert decision.metadata["region"] == "US"


def test_region_allowed():
    decision = enforce_region_policy(
        policy=BASE_POLICY,
        region="IN",
    )
    assert decision.decision == DecisionType.ALLOW

