# ai-governor

**ai-governor is a model-level governance and compliance runtime for LLM systems.**

It provides a **deterministic control layer** between applications and Large Language Models (LLMs), enabling teams to **enforce policies, control model usage, handle sensitive data, and generate audit-grade evidence** at runtime.

Unlike prompt-only guardrails or policy documents, ai-governor focuses on **technical enforcement** — not intentions.

---

## What ai-governor Does

ai-governor allows you to:

- Enforce **model allow/deny rules** and token limits  
- Control **PII handling** (allow, block, or modify)  
- Make **explicit governance decisions** (`ALLOW`, `BLOCK`, `MODIFY`)  
- Emit **immutable audit events** for every decision  
- Apply governance consistently across models and providers  

All enforcement is:
- **Policy-driven**
- **Explainable**
- **Auditable**
- **Model-agnostic**

---

## What ai-governor Is (and Is Not)

ai-governor **is**:
- A runtime governance layer for LLM systems
- Policy-as-code for model usage and data handling
- Infrastructure for security, compliance, and platform teams

ai-governor **is not**:
- A chatbot framework
- A prompt-only safety wrapper
- A hosted SaaS service
- A legal compliance certification tool

It enforces **technical controls**, not regulatory interpretations.

---

## Project Status

⚠️ **Early-stage (v0.1 alpha)**  
The core governance runtime is implemented and functional.  
APIs may evolve, but foundational concepts and contracts are stable.

---

## Why This Exists

LLMs are now production infrastructure — but lack:
- Access control
- Deterministic enforcement
- Auditability
- Runtime governance

ai-governor fills this gap.

Read the full rationale here:  
👉 `docs/WHY_THIS_EXISTS.md`

---

## Architecture & Flow

ai-governor is designed as a **runtime governance layer** that sits between an application and a Large Language Model (LLM).

It enforces policies **before execution**, **during evaluation**, and **after decisions**, while producing **audit-grade evidence**.

### High-Level Architecture

```
Application / API
        |
        v
+----------------------+
|  ai-governor Runtime |
|----------------------|
|  Policy Validator    |
|  Enforcement Engine  |
|  Decision Model      |
|  Audit Emitter       |
+----------------------+
        |
        v
LLM Provider / Model
```

ai-governor is **model-agnostic** and does not depend on a specific LLM vendor.

---

### Core Components

**Policy Schema**  
Declarative YAML/JSON policies defining governance rules.

**Policy Validator**  
Validates policies for correctness before enforcement.

**Enforcement Orchestrator**  
Executes governance checks in a fixed, deterministic order.

**Decision Model**  
Every check returns `ALLOW`, `BLOCK`, or `MODIFY` with reasons.

**Audit Event Emitter**  
Every decision generates immutable, structured audit evidence.

---

### Execution Flow

```
Policy YAML
   ↓
Policy Validator
   ↓
Enforcement Orchestrator
   ├─ Model Enforcement
   ├─ PII Enforcement
   └─ (future controls)
   ↓
Decision(s)
   ↓
Audit Event(s)
   ↓
Final Governance Outcome
```

---

## Quick Start (10 lines)

```python
from core.enforcement.orchestrator import EnforcementOrchestrator

policy = {
    "version": "0.1",
    "model": {"allow": ["gpt-4.1"], "deny": ["*-preview"]},
    "data": {"pii": {"action": "redact"}},
}

orchestrator = EnforcementOrchestrator()

result = orchestrator.enforce(
    policy=policy,
    requested_model="gpt-4.1",
    text="Contact me at test@example.com",
)

print(result["final_decision"].to_dict())
```

👉 See `docs/QUICKSTART.md`

---

## Minimal Code Example (No Providers)

```python
from core.enforcement.orchestrator import EnforcementOrchestrator
from core.decision import DecisionType

policy = {
    "version": "0.1",
    "model": {
        "allow": ["gpt-4.1"],
        "max_tokens": 4096,
    },
    "data": {
        "pii": {"action": "block"},
    },
}

orchestrator = EnforcementOrchestrator()

result = orchestrator.enforce(
    policy=policy,
    requested_model="gpt-4.1",
    requested_max_tokens=1024,
    text="Email me at admin@example.com",
)

decision = result["final_decision"]

if decision.decision == DecisionType.BLOCK:
    print("Blocked:", decision.reason)
elif decision.decision == DecisionType.MODIFY:
    print("Modify required")
else:
    print("Allowed")
```

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

## Versioned Roadmap

### v0.1 (Current – Alpha)
- Policy schema & validator
- Canonical Decision model
- Model allow/deny enforcement
- PII enforcement
- Audit event emission
- Enforcement orchestrator

### v0.2 (Planned)
- Redaction engine
- Region enforcement
- CLI (`ai-governor validate`, `ai-governor enforce`)
- Pluggable audit sinks

### v0.3 (Future)
- Tool / agent governance
- Policy composition & inheritance
- Compliance control mappings

---

## Security

Security and correctness are first-class concerns in ai-governor.

If you discover a vulnerability, please follow our responsible disclosure process and do not open a public issue.

👉 See `SECURITY.md` for details.

---

## Contributing

Please read `CONTRIBUTING.md` before opening issues or pull requests.  
Design discussions are strongly encouraged before large changes.

---

## License

MIT — open, inspectable, and vendor-neutral by design.
