# Policy Schema v0.2 (Draft)

Status: Draft  
Target Release: v0.4.x  
Backward Compatibility: v0.1 fully supported  

---

## 1. Design Principles

v0.2 extends policy precision without changing:

- Decision types (ALLOW | BLOCK | MODIFY)
- Enforcement order
- CLI semantics
- Audit guarantees

v0.2 adds depth, not breadth.

---

## 2. Version Declaration

```yaml
version: 0.2
```

v0.1 and v0.2 must coexist.
No automatic schema upgrade is allowed.

---

## 3. Model Governance (Extended)

### 3.1 Model Families

v0.2 introduces model grouping.

```yaml
model:
  allow:
    - gpt-4.1
  families:
    openai:
      allow:
        - gpt-4.*
      deny:
        - gpt-4.1-mini
```

Rules:
- Explicit model rules override family rules.
- deny always overrides allow.

---

## 4. Tool Governance (Argument-Level)

v0.1:
```yaml
tools:
  allow:
    - search
```

v0.2:
```yaml
tools:
  allow:
    search:
      domains:
        - wikipedia.org
    http_request:
      methods:
        - GET
  deny:
    execute_code: {}
```

Rules:
- Tool name must be allowed.
- Arguments are evaluated deterministically.
- Violations → BLOCK or MODIFY.
- No scripting or dynamic evaluation.

---

## 5. PII Field-Level Rules

v0.1:
```yaml
data:
  pii:
    action: redact
```

v0.2:
```yaml
data:
  pii:
    action: redact
    fields:
      email: redact
      phone: block
```

Rules:
- Field rules override global action.
- Deterministic regex-based detection only.
- No ML classifiers.

---

## 6. Metadata (Optional)

```yaml
metadata:
  labels:
    environment: production
    team: risk
```

Metadata has no enforcement effect.
Used only for audit tagging.

---

## 7. Inheritance

v0.2 continues supporting:

```yaml
extends: base-policy.yaml
```

Merge rules:
- Child overrides parent
- `null` removes inherited values
- No deep dynamic merging beyond defined schema

---

## 8. Explicit Non-Goals

v0.2 does NOT introduce:

- User identity logic
- RBAC
- ABAC
- Provider-specific logic
- Rego/OPA
- Policy scripting
- Risk scoring
- ML-based moderation

---

## 9. Validation Requirements

Validator must:
- Dispatch based on version
- Reject unknown top-level keys
- Reject unknown nested fields
- Fail-fast on ambiguity
- Preserve deterministic behavior

---

End of Draft
