# ai-governor – Quick Start Guide

This guide helps you run **model-level governance** locally using **ai-governor** — no LLM providers, no API keys, no cloud services.

You’ll validate a policy, enforce it, redact PII, and generate audit logs.

---

## 1️⃣ Install (Editable / Local)

From the repo root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Verify:

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

enforcement:
  on_violation: block
```

---

## 3️⃣ Validate the Policy

```bash
ai-governor validate policy.yaml
```

Expected output:

```text
✔ Policy is valid
```

This step ensures the policy is **structurally correct and enforceable**.

---

## 4️⃣ Enforce Governance (ALLOW)

```bash
ai-governor enforce \
  --policy policy.yaml \
  --model gpt-4.1 \
  --region IN \
  --text "Hello world"
```

Output:

```json
{
  "final_decision": "ALLOW",
  "reason": "Region 'IN' is allowed by policy",
  "policy_section": "data.regions"
}
```

Exit code: `0`

---

## 5️⃣ Enforce Governance (MODIFY – PII Redaction)

```bash
ai-governor enforce \
  --policy policy.yaml \
  --model gpt-4.1 \
  --region IN \
  --text "Contact me at test@example.com"
```

Output:

```json
{
  "final_decision": "MODIFY",
  "reason": "PII detected and policy requires redaction",
  "policy_section": "data.pii"
}
```

Exit code: `10`

Internally:

* Email is detected
* Redaction engine replaces it
* Audit event is emitted

---

## 6️⃣ Enforce Governance (BLOCK – Region Violation)

```bash
ai-governor enforce \
  --policy policy.yaml \
  --model gpt-4.1 \
  --region US \
  --text "Hello"
```

Output:

```json
{
  "final_decision": "BLOCK",
  "reason": "Region 'US' is not allowed by policy",
  "policy_section": "data.regions"
}
```

Exit code: `20`

---

## 7️⃣ Audit Logs (Automatic)

Every enforcement emits **JSON audit events**.

Default: stdout
Optional: file sink (example):

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

Each line in `audit.jsonl` is a complete, immutable audit record.

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

Perfect for CI pipelines and policy gates.

---

## 9️⃣ What You Just Achieved

You enforced:

* ✅ Model allow/deny
* ✅ Token limits
* ✅ Region restrictions
* ✅ PII detection + redaction
* ✅ Deterministic decisions
* ✅ Audit-grade evidence

**Without calling an LLM.**

---

## Demo Application

This repository includes a **minimal demo application** that shows how **ai-governor** is intended to be used in a real system.

The demo simulates an application boundary that wants to call an LLM, with governance enforced **before** any model invocation.

No external APIs, frameworks, or providers are used.

---

### What the Demo Shows

The demo demonstrates:

* Where ai-governor sits in an application
* How policies are evaluated at runtime
* How decisions (`ALLOW`, `BLOCK`, `MODIFY`) gate execution
* How PII redaction works for `MODIFY`
* How audit events are emitted automatically

This is the **canonical integration pattern**.

---

### Location

```
examples/demo_app/
```

Contents:

* `app.py` — demo application
* `policy.yaml` — governance policy
* `request_allow.json` — allowed request
* `request_modify.json` — PII redaction example
* `request_block.json` — blocked request

---

### Run the Demo

From the repository root:

```bash
python examples/demo_app/app.py examples/demo_app/request_allow.json
```

Try the other requests to see different governance outcomes:

```bash
python examples/demo_app/app.py examples/demo_app/request_modify.json
python examples/demo_app/app.py examples/demo_app/request_block.json
```

---

### Design Note

The demo intentionally:

* Uses **declared model identifiers** (strings only)
* Does **not** call a real LLM
* Focuses purely on **governance correctness**

This keeps the behavior deterministic and easy to reason about.

---

### Why This Matters

Most governance failures happen at **integration boundaries**.

This demo makes that boundary explicit and reproducible.

---

## Philosophy Reminder

ai-governor does not try to make AI *safe*.

It makes AI **governable**.

