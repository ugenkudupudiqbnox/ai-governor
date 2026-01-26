from core.redaction.engine import RedactionEngine


def test_email_redaction():
    engine = RedactionEngine()

    result = engine.redact("Contact me at test@example.com")

    assert "[REDACTED_EMAIL]" in result.text
    assert "email" in result.redacted_entities


def test_multiple_redactions():
    engine = RedactionEngine()

    text = "Email test@example.com or call 9876543210"
    result = engine.redact(text)

    assert "[REDACTED_EMAIL]" in result.text
    assert "[REDACTED_PHONE]" in result.text
    assert set(result.redacted_entities) == {"email", "phone"}


def test_no_pii():
    engine = RedactionEngine()

    result = engine.redact("Hello world")

    assert result.text == "Hello world"
    assert result.redacted_entities == []

