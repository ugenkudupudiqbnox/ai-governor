import argparse
import sys

from cli.validate import run_validate
from cli.enforce import run_enforce


def main():
    parser = argparse.ArgumentParser(
        prog="ai-governor",
        description="Model-level governance and compliance runtime for LLM systems",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # validate
    validate_parser = subparsers.add_parser(
        "validate", help="Validate a governance policy"
    )
    validate_parser.add_argument("policy", help="Path to policy YAML file")
    validate_parser.add_argument("--json", action="store_true", help="JSON output")
    validate_parser.add_argument(
        "--strict", action="store_true", help="Treat warnings as errors"
    )

    # enforce
    enforce_parser = subparsers.add_parser(
        "enforce", help="Run governance enforcement"
    )
    enforce_parser.add_argument("--policy", required=True, help="Policy YAML file")
    enforce_parser.add_argument("--model", required=True, help="Requested model")
    enforce_parser.add_argument("--max-tokens", type=int, help="Requested max tokens")
    enforce_parser.add_argument(
        "--region",
        help="Request region / jurisdiction (e.g. IN, EU, US)",
    )

    enforce_parser.add_argument(
        "--text",
        help="Text input or @file.txt",
    )
    enforce_parser.add_argument(
        "--context",
        help="Optional JSON context file",
    )
    enforce_parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show all intermediate decisions",
    )

    args = parser.parse_args()

    if args.command == "validate":
        sys.exit(run_validate(args))

    if args.command == "enforce":
        sys.exit(run_enforce(args))


if __name__ == "__main__":
    main()

