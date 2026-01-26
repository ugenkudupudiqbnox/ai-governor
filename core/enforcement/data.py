from __future__ import annotations

import re
from typing import Any, Dict, List

from core.decision import Decision


# --- Simple deterministic PII detectors (v0.1) ---

EMAIL_REGEX = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
PHONE_REGEX = re.compile(r"\b\d{10}\b")
CREDIT_CARD_REGEX = re.compile(r"\b\d{13,19}\b")


def detect_pii(text: str) -> List[str]:
    """
    Detect basic PII types in text.

    Returns a list of detected PII entity types.
    """
    detected = []

    if EMAIL_REGEX.search(text):
        detected.append("email")

    if PHONE_REGEX.search(text):
        detected.append("phone")

    if CREDIT_CARD_REGEX.search(text):
        detected.append("credit_card")

    return detected


def enforce_pii_policy(
    policy: Dict[str, Any],
    text: str,
) -> Decision:
    """
    Enforce PII handling rules defined in the policy.

    Returns a Decision indicating ALLOW, BLOCK, or MODIFY.
    """

    data_policy = policy.get("data", {})
    pii_policy = data_policy.get("pii")

    # No PII policy → allow
    if not pii_policy:
        return Decision.allow(
            reason="No PII policy defined",
            policy_section="data.pii",
        )

    action = pii_policy.get("action")
    detected_entities = detect_pii(text)

    # No PII detected → allow
    if not detected_entities:
        return Decision.allow(
            reason="No PII detected in content",
            policy_section="data.pii",
        )

    # PII detected → enforce action
    if action == "block":
        return Decision.block(
            reason="PII detected and policy requires blocking",
            policy_section="data.pii",
            metadata={"detected_entities": detected_entities},
        )

    if action == "redact":
        return Decision.modify(
            reason="PII detected and policy requires redaction",
            policy_section="data.pii",
            metadata={"detected_entities": detected_entities},
        )

    if action == "allow":
        return Decision.allow(
            reason="PII detected but policy allows it",
            policy_section="data.pii",
            metadata={"detected_entities": detected_entities},
        )

    # Defensive fallback (should not happen if validated)
    return Decision.block(
        reason=f"Unknown PII action '{action}'",
        policy_section="data.pii",
    )

