# DO NOT MODIFY — v0.3 CONTRACT TEST

from core.decision import DecisionType

def test_determinism(orchestrator):
    policy = {"version": "0.1", "data": {"pii": {"action": "redact"}}}
    r1 = orchestrator.enforce(policy, requested_model="gpt-4.1", text="email me at a@b.com")
    r2 = orchestrator.enforce(policy, requested_model="gpt-4.1", text="email me at a@b.com")

    assert r1["final_decision"].decision == r2["final_decision"].decision
    assert r1["output_text"] == r2["output_text"]
