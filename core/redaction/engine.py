from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, List, Tuple

# Keep regexes aligned with PII detection
EMAIL_REGEX = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
PHONE_REGEX = re.compile(r"\b\d{10}\b")
CREDIT_CARD_REGEX = re.compile(r"\b\d{13,19}\b")

REDACTION_MAP: Dict[str, Tuple[re.Pattern, str]] = {
    "email": (EMAIL_REGEX, "[REDACTED_EMAIL]"),
    "phone": (PHONE_REGEX, "[REDACTED_PHONE]"),
    "credit_card": (CREDIT_CARD_REGEX, "[REDACTED_CREDIT_CARD]"),
}


@dataclass(frozen=True)
class RedactionResult:
    text: str
    redacted_entities: List[str]


class RedactionEngine:
    """
    Deterministic redaction engine for sensitive data.

    Applies simple, explainable transformations.
    """

    def redact(self, text: str) -> RedactionResult:
        redacted_entities: List[str] = []
        redacted_text = text

        for entity, (pattern, replacement) in REDACTION_MAP.items():
            if pattern.search(redacted_text):
                redacted_text = pattern.sub(replacement, redacted_text)
                redacted_entities.append(entity)

        return RedactionResult(
            text=redacted_text,
            redacted_entities=sorted(set(redacted_entities)),
        )

