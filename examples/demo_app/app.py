"""
ai-governor demo application

This simulates an application boundary that wants to call an LLM.
Governance happens BEFORE the model call.
"""

import json
import sys
from pathlib import Path

from core.enforcement.orchestrator import EnforcementOrchestrator
from core.decision import DecisionType


BASE_DIR = Path(__file__).parent


def load_request(path: str) -> dict:
    with open(BASE_DIR / path) as f:
        return json.load(f)


def main(request_file: str):
    # Load policy
    with open(BASE_DIR / "policy.yaml") as f:
        policy = f.read()

    import yaml
    policy = yaml.safe_load(policy)

    orchestrator = EnforcementOrchestrator()

    request = load_request(request_file)

    print("\n--- Incoming Request ---")
    print(json.dumps(request, indent=2))

    result = orchestrator.enforce(
        policy=policy,
        requested_model=request["model"],
        requested_max_tokens=request.get("max_tokens"),
        region=request.get("region"),
        text=request.get("prompt"),
        context={
            "request_id": request.get("id"),
            "actor": "demo-app",
            "environment": "local",
        },
    )

    decision = result["final_decision"]

    print("\n--- Governance Decision ---")
    print(json.dumps(decision.to_dict(), indent=2))

    if decision.decision == DecisionType.BLOCK:
        print("\n❌ Request blocked by governance")
        sys.exit(1)

    if decision.decision == DecisionType.MODIFY:
        print("\n✂️ Redacted Prompt:")
        print(result["output_text"])

    print("\n✅ Ready to call LLM (simulated)")
    print("(No actual model call is made)")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python app.py <request.json>")
        sys.exit(1)

    main(sys.argv[1])

