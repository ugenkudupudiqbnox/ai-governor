# ai-governor Policy Schema v0.1

## Status

* **Version:** 0.1
* **Stability:** Experimental
* **Audience:** Platform, security, and AI engineers
* **Scope:** Runtime governance for LLM inference

This document defines the **minimum viable policy schema** for ai-governor.

---

## Design Principles

1. **Declarative, not procedural**
   Policies describe *what must be enforced*, not *how*.

2. **Deterministic enforcement**
   Every policy evaluation must result in a clear decision:

   * `ALLOW`
   * `BLOCK`
   * `MODIFY`

3. **Auditable by default**
   Policies must produce evidence suitable for security and compliance review.

4. **Model-agnostic**
   No policy may assume a specific LLM vendor or API.

5. **Small surface area (v0.1)**
   This schema intentionally excludes advanced features to avoid early complexity.

---

## Top-Level Structure

```yaml
version: 0.1

metadata:
  ...

model:
  ...

access:
  ...

data:
  ...

safety:
  ...

logging:
  ...

enforcement:
  ...
```

All top-level keys are **optional unless explicitly marked REQUIRED**, but omission may result in default-deny behavior depending on enforcement configuration.

---

## 1. version (REQUIRED)

```yaml
version: 0.1
```

* Must be exactly `0.1`
* Used for schema validation and forward compatibility

---

## 2. metadata (OPTIONAL, RECOMMENDED)

Descriptive and ownership information.

```yaml
metadata:
  name: production-llm-policy
  owner: platform-team
  environment: production
  description: Governance policy for production LLM usage
```

### Fields

| Field       | Type   | Description                |
| ----------- | ------ | -------------------------- |
| name        | string | Human-readable policy name |
| owner       | string | Owning team or role        |
| environment | string | e.g. dev / staging / prod  |
| description | string | Free-form description      |

---

## 3. model (OPTIONAL, STRONGLY RECOMMENDED)

Controls **which models may be used** and with what constraints.

```yaml
model:
  allow:
    - gpt-4.1
    - llama-3.1-70b
  deny:
    - "*-preview"
  max_tokens: 4096
```

### Fields

| Field      | Type         | Description                                       |
| ---------- | ------------ | ------------------------------------------------- |
| allow      | list[string] | Explicitly allowed model identifiers              |
| deny       | list[string] | Explicitly denied models (supports glob patterns) |
| max_tokens | integer      | Maximum tokens allowed per request                |

### Notes

* If `allow` is defined, models not listed MUST be denied.
* `deny` always overrides `allow`.

---

## 4. access (OPTIONAL)

Defines **who** is allowed to invoke governed LLMs.

```yaml
access:
  roles:
    - admin
    - prod
```

### Fields

| Field | Type         | Description          |
| ----- | ------------ | -------------------- |
| roles | list[string] | Allowed caller roles |

### Notes

* Role resolution happens outside ai-governor.
* ai-governor only evaluates role strings passed at runtime.

---

## 5. data (OPTIONAL)

Controls how sensitive data is handled.

```yaml
data:
  pii:
    action: redact
  regions:
    allowed:
      - IN
      - EU
```

### 5.1 pii

```yaml
pii:
  action: block | redact | allow
```

| Action | Meaning            |
| ------ | ------------------ |
| block  | Reject the request |
| redact | Mask detected PII  |
| allow  | No enforcement     |

### 5.2 regions

```yaml
regions:
  allowed:
    - IN
    - EU
```

* Restricts inference execution based on detected or declared region.

---

## 6. safety (OPTIONAL)

High-level content restrictions.

```yaml
safety:
  disallowed_topics:
    - self-harm
    - illegal-activity
```

### Fields

| Field             | Type         | Description                       |
| ----------------- | ------------ | --------------------------------- |
| disallowed_topics | list[string] | Topics that must not be generated |

### Notes

* Topic detection is implementation-specific.
* v0.1 favors deterministic or lightweight classifiers.

---

## 7. logging (OPTIONAL, RECOMMENDED)

Defines **what evidence is stored**.

```yaml
logging:
  store_prompts: false
  store_outputs: true
  retention_days: 90
```

### Fields

| Field          | Type    | Description         |
| -------------- | ------- | ------------------- |
| store_prompts  | boolean | Store raw prompts   |
| store_outputs  | boolean | Store model outputs |
| retention_days | integer | Retention duration  |

### Notes

* Hashing MAY be used instead of raw storage.
* Storage backend is out of scope for v0.1.

---

## 8. enforcement (OPTIONAL)

Defines default behavior on policy violation.

```yaml
enforcement:
  on_violation: block
```

### Fields

| Field        | Type | Description                  |
| ------------ | ---- | ---------------------------- |
| on_violation | enum | `block`, `modify`, or `warn` |

### Meanings

* `block`: Reject request or response
* `modify`: Apply redaction or transformation
* `warn`: Allow but emit audit event

---

## Policy Evaluation Outcome (Normative)

Every policy evaluation MUST return:

```json
{
  "decision": "ALLOW | BLOCK | MODIFY",
  "reason": "human-readable explanation",
  "policy_section": "data.pii",
  "policy_version": "0.1"
}
```

---

## Defaults & Implicit Behavior

* If no policy is present → **ALLOW** (implementation choice)
* If a policy exists but a required constraint is violated → **BLOCK**
* Deny rules override allow rules
* Explicit policies override defaults

---

## Out of Scope for v0.1

The following are **explicitly excluded**:

* Conditional logic (`if / then`)
* Scoring or risk weighting
* Learning or adaptive policies
* Tool / agent permissions
* UI or visual policy editors
* Legal interpretations of regulations

These may appear in **v0.2+** only after real-world usage.

---

## Forward Compatibility

* New fields MUST NOT break v0.1 policies
* Unknown fields SHOULD be ignored with warnings
* Schema versioning is mandatory

