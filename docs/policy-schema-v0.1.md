# ai-governor Policy Schema v0.1

**Status:** Supported (v0.3, feature-frozen)  
**Scope:** Policy structure and semantics only

This document defines the **policy schema version `0.1`** as implemented and supported by **ai-governor v0.3**.

It describes:
- The valid structure of a governance policy
- Supported fields and their semantics
- Explicit non-goals and exclusions

It does **not** define:
- Legal or regulatory compliance guarantees
- Model behavior or safety outcomes
- Enforcement ordering (see `docs/STABILITY.md`)

---

## Design Principles

- **Deterministic**: the same policy always produces the same decisions
- **Explicit**: no implicit unions or hidden defaults
- **Fail-fast**: invalid or ambiguous policies are rejected
- **Composable**: policies may be layered via inheritance
- **Auditable**: every decision is traceable to a policy rule

---

## Top-Level Structure

```yaml
version: 0.1

metadata:        # optional
model:           # optional
data:            # optional
tools:           # optional
```

Fields not listed above are **intentionally unsupported** in schema v0.1.

---

## 1️⃣ `version` (Required)

```yaml
version: 0.1
```

- Must be exactly `"0.1"`
- Used to select schema validation rules
- Version mismatches are rejected

---

## 2️⃣ `metadata` (Optional)

Arbitrary metadata for human or system context.

```yaml
metadata:
  owner: platform-team
  environment: production
```

- Not interpreted by enforcement logic
- Included in audit context when provided

---

## 3️⃣ `model` (Optional)

Defines allowed and denied model identifiers.

```yaml
model:
  allow:
    - gpt-4.1
  deny:
    - "*-preview"
  max_tokens: 4096
```

### Fields

| Field | Type | Description |
|-----|----|-------------|
| `allow` | list[string] | Allowed model identifiers |
| `deny` | list[string] | Explicitly denied identifiers |
| `max_tokens` | integer | Maximum allowed token count |

### Semantics

- `deny` always takes precedence over `allow`
- If `allow` is present, models not listed are blocked
- Identifiers are matched as literal strings or simple wildcards

---

## 4️⃣ `data` (Optional)

Defines data-handling governance rules.

### 4.1 Regions

```yaml
data:
  regions:
    allowed:
      - IN
      - EU
```

| Field | Type | Description |
|-----|----|-------------|
| `allowed` | list[string] | Allowed region codes |

If a region is provided at enforcement time and is not allowed, the decision is `BLOCK`.

---

### 4.2 PII

```yaml
data:
  pii:
    action: block | redact
```

| Action | Behavior |
|------|----------|
| `block` | Request is blocked if PII is detected |
| `redact` | PII is deterministically removed and request is modified |

Notes:
- Absence of a `pii` policy implies no PII enforcement
- PII detection is deterministic and rule-based (not ML)

---

## 5️⃣ `tools` (Optional)

Defines governance rules for tool or agent invocation.

```yaml
tools:
  allow:
    - search
    - summarize
  deny:
    - execute_code
```

### Fields

| Field | Type | Description |
|-----|----|-------------|
| `allow` | list[string] | Allowed tool names |
| `deny` | list[string] | Explicitly denied tool names |

### Semantics

- `deny` always takes precedence
- If `allow` is present, tools not listed are blocked
- Absence of `tools` policy implies no tool restrictions

Tool argument-level governance is **out of scope for v0.1**.

---

## 6️⃣ Policy Inheritance (`extends`)

Policies may extend a single base policy.

```yaml
extends: base-policy.yaml
```

Rules:
- Single inheritance only
- Inheritance is resolved before validation
- Child policies override base policies explicitly
- `null` removes an inherited field
- Cycles are rejected

Example:

```yaml
extends: base.yaml

data:
  pii:
    action: block
```

---

## Defaults & Implicit Behavior

- Policies are evaluated only after successful validation
- Absence of a policy section implies no governance for that dimension
- Enforcement without a valid policy is undefined and discouraged

---

## Explicit Non-Goals (Schema v0.1)

The following are **intentionally out of scope**:

- Access control / IAM semantics
- Prompt or content moderation rules
- ML-based safety classifiers
- Logging or retention configuration
- Enforcement behavior configuration
- Compliance certifications or mappings

These may be introduced only in **future schema versions**.

---

## Stability & Compatibility

- Schema v0.1 is **feature-frozen in ai-governor v0.3**
- Backward-incompatible changes require a new schema version
- Enforcement and audit guarantees are defined in `docs/STABILITY.md`

---

## Summary

Policy schema v0.1 defines a **minimal, enforceable contract** for LLM governance.

It is designed to be:
- predictable
- composable
- reviewable
- safe to depend on

Nothing more — and nothing less.
