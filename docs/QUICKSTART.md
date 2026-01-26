# ai-governor – Quick Start Guide (v0.3)

This guide helps you run **model-level governance** locally using **ai-governor**.

No LLM providers.  
No API keys.  
No cloud services.

You will validate a policy, enforce it, redact PII, and generate audit-grade evidence.

---

## 1️⃣ Install (Editable / Local)

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Verify installation:

```bash
ai-governor version
```

---

## 2️⃣ Create a Policy

Create `policy.yaml`:

```yaml
version: 0.1

model:
  allow:
    - gpt-4.1
  deny:
    - "*-preview"
  max_tokens: 4096

data:
  regions:
    allowed:
      - IN
      - EU
  pii:
    action: redact
```

This policy:
- Allows only approved models
- Restricts regions
- Redacts detected PII
- Produces deterministic decisions

---

## 3️⃣ Validate the Policy

```bash
ai-governor validate policy.yaml
```

Expected output:

```text
✔ Policy is valid
```

Policy validation:
- Resolves inheritance (if present)
- Rejects invalid schemas
- Prevents ambiguous enforcement

---

## 4️⃣ Enforce Governance (ALLOW)

```bash
ai-governor enforce   --policy policy.yaml   --model gpt-4.1   --region IN   --text "Hello world"
```

Exit code: `0`

Meaning: execution may proceed.

---

## 5️⃣ Enforce Governance (MODIFY – PII Redaction)

```bash
ai-governor enforce   --policy policy.yaml   --model gpt-4.1   --region IN   --text "Contact me at test@example.com"
```

Exit code: `10`

Meaning:
- PII detected
- Input was redacted
- Execution may proceed **only with modified input**

---

## 6️⃣ Enforce Governance (BLOCK – Region Violation)

```bash
ai-governor enforce   --policy policy.yaml   --model gpt-4.1   --region US   --text "Hello"
```

Exit code: `20`

Meaning: execution must not proceed.

---

## 7️⃣ Audit Logs (Automatic)

Every enforcement emits a **structured audit event**.

Default: stdout

Example file sink:

```python
from core.audit.emitter import AuditEventEmitter
from core.audit.sinks import JsonFileSink
from core.enforcement.orchestrator import EnforcementOrchestrator

emitter = AuditEventEmitter(
    sinks=[JsonFileSink("audit.jsonl")]
)

orchestrator = EnforcementOrchestrator(
    audit_emitter=emitter
)
```

Each line in `audit.jsonl` is a complete, append-only audit record.

If an audit sink fails, enforcement fails by design.

---

## 8️⃣ Exit Codes (CI / Automation Friendly)

| Exit Code | Meaning                     |
| --------- | --------------------------- |
| `0`       | ALLOW                       |
| `10`      | MODIFY (redaction required) |
| `20`      | BLOCK                       |
| `1`       | Policy invalid              |
| `2`       | File / parse error          |
| `3`       | Runtime error               |

This makes ai-governor suitable for CI/CD policy gates.

---

## 9️⃣ Demo Application

A minimal demo application is included under:

```
examples/demo_app/
```

The demo shows:
- Governance enforced before any model call
- Explicit BLOCK / MODIFY behavior
- Deterministic redaction
- Automatic audit emission

Run:

```bash
python examples/demo_app/app.py examples/demo_app/request_modify.json
```

A FastAPI-based HTTP demo is also available under `examples/fastapi_demo/`
(illustrative only, not part of the stable API).

---

## 10️⃣ What You Just Achieved

You enforced:

- Model allow / deny rules
- Region restrictions
- Tool governance (if configured)
- PII detection and redaction
- Deterministic decisions
- Audit-grade evidence

**Without calling an LLM.**

---

## Stability Note

ai-governor v0.3 is feature-frozen.

See `docs/STABILITY.md` for compatibility and upgrade guarantees.

---

ai-governor does not try to make AI *safe*.  
It makes AI **governable**.
