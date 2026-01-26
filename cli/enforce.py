import json
import sys
import yaml

from core.enforcement.orchestrator import EnforcementOrchestrator
from core.decision import DecisionType


def _load_text(text_arg):
    if text_arg.startswith("@"):
        with open(text_arg[1:]) as f:
            return f.read()
    return text_arg


def _load_context(path):
    if not path:
        return None
    with open(path) as f:
        return json.load(f)


def run_enforce(args) -> int:
    try:
        with open(args.policy) as f:
            policy = yaml.safe_load(f)
    except Exception as e:
        print(f"Failed to load policy: {e}", file=sys.stderr)
        return 2

    text = _load_text(args.text) if args.text else None
    context = _load_context(args.context)

    orchestrator = EnforcementOrchestrator()

    try:
        result = orchestrator.enforce(
            policy=policy,
            requested_model=args.model,
            requested_max_tokens=args.max_tokens,
            region=args.region,
            text=text,
            context=context,
        )
    except Exception as e:
        print(f"Enforcement failed: {e}", file=sys.stderr)
        return 3

    final = result["final_decision"]

    if args.verbose:
        print(
            json.dumps(
                {
                    "final_decision": final.decision.value,
                    "decisions": [
                        d.to_dict() for d in result["decisions"]
                    ],
                },
                indent=2,
            )
        )
    else:
        print(
            json.dumps(
                {
                    "final_decision": final.decision.value,
                    "reason": final.reason,
                    "policy_section": final.policy_section,
                }
            )
        )

    if final.decision == DecisionType.ALLOW:
        return 0
    if final.decision == DecisionType.MODIFY:
        return 10
    if final.decision == DecisionType.BLOCK:
        return 20

    return 3

