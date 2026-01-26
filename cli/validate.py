import json
import sys
import yaml

from core.policy_validator import PolicyValidator


def run_validate(args) -> int:
    try:
        with open(args.policy) as f:
            policy = yaml.safe_load(f)
    except Exception as e:
        print(f"Failed to load policy: {e}", file=sys.stderr)
        return 2

    validator = PolicyValidator()
    result = validator.validate(policy)

    if args.json:
        print(
            json.dumps(
                {
                    "valid": result.valid,
                    "errors": result.errors,
                    "warnings": result.warnings,
                },
                indent=2,
            )
        )
    else:
        if result.valid:
            print("✔ Policy is valid")
        else:
            print("✖ Policy is invalid")

        if result.errors:
            print("\nErrors:")
            for e in result.errors:
                print(f"  - {e}")

        if result.warnings:
            print("\nWarnings:")
            for w in result.warnings:
                print(f"  - {w}")

    if not result.valid:
        return 1

    if args.strict and result.warnings:
        return 1

    return 0

