# ai-governor v0.3 — Stability & Compatibility Guarantees

## Status

**v0.3 is feature-frozen.**

From this point forward:

* No new governance concepts will be added to v0.3
* Only bug fixes, documentation updates, and internal hardening are allowed
* Breaking changes require a **minor version bump** (v0.4)

---

## What v0.3 Guarantees

v0.3 establishes **contractual stability** for the following components.

These guarantees are intentional and binding.

---

## 1️⃣ Governance Semantics (Frozen)

The following concepts are **stable and will not change** in v0.3.x:

### Decision Types

```text
ALLOW
BLOCK
MODIFY
```

Their meanings are fixed:

* `ALLOW` → execution may proceed
* `BLOCK` → execution must not proceed
* `MODIFY` → execution may proceed only with transformed input/output

No new decision types will be introduced in v0.3.x.

---

### Enforcement Order (Frozen)

Governance checks execute in the following deterministic order:

1. Model enforcement
2. Region enforcement
3. Tool governance
4. Data / PII enforcement
5. Redaction (if applicable)

This order is **guaranteed** for all v0.3.x releases.

---

## 2️⃣ Policy Schema Stability

### Supported Policy Version

```yaml
version: 0.1
```

* Policy schema `0.1` is **fully supported** in v0.3.x
* Any future schema changes will require:

  * a new version identifier
  * explicit migration documentation

---

### Policy Inheritance (`extends:`)

The following inheritance rules are **frozen**:

* Single inheritance only
* Deterministic merge semantics
* Explicit override behavior
* Explicit null-based removal
* Cycle detection with fail-fast behavior

No additional inheritance mechanisms will be added in v0.3.x.

---

## 3️⃣ Public API Stability

### EnforcementOrchestrator

The following method is **stable**:

```python
EnforcementOrchestrator.enforce(
    policy,
    requested_model,
    requested_max_tokens=None,
    region=None,
    tool_name=None,
    text=None,
    context=None,
)
```

* Parameter names and meanings are frozen
* New optional parameters may be added **only** in minor versions
* No parameter will change semantics in v0.3.x

---

### Decision Object

The `Decision` object fields are stable:

* `decision`
* `reason`
* `policy_section`
* `policy_version`
* `metadata`

No fields will be removed or repurposed in v0.3.x.

---

## 4️⃣ CLI Stability

The CLI interface is **frozen** for v0.3.x.

### Guaranteed Commands

```bash
ai-governor validate
ai-governor enforce
```

### Guaranteed Exit Codes

| Exit Code | Meaning            |
| --------- | ------------------ |
| 0         | ALLOW              |
| 10        | MODIFY             |
| 20        | BLOCK              |
| 1         | Validation error   |
| 2         | Input / file error |
| 3         | Runtime error      |

These exit codes **will not change** in v0.3.x.

---

## 5️⃣ Audit & Evidence Guarantees

Audit behavior is **stable and explicit**:

* One governance decision → one audit event
* JSON Lines format
* Append-only semantics
* Fail-fast on audit sink failure (default)

ai-governor does **not** guarantee:

* delivery
* durability
* replay
* ordering across sinks

Those concerns are delegated to external systems.

---

## 6️⃣ Backward Compatibility Policy

Within v0.3.x:

* Bug fixes are allowed
* Performance improvements are allowed
* Documentation updates are allowed
* Behavior changes are **not** allowed

Any breaking change requires:

* version bump (v0.4)
* migration notes
* explicit announcement

---

## 7️⃣ What v0.3 Explicitly Does NOT Promise

v0.3 makes **no guarantees** about:

* Legal or regulatory compliance
* Model behavior or safety
* LLM output correctness
* Provider availability
* Network reliability
* Enforcement completeness outside defined policy

ai-governor enforces **technical controls only**.

---

## 8️⃣ How to Depend on ai-governor v0.3

If you are a user or integrator, you can safely:

* Embed ai-governor in production systems
* Gate deployments using the CLI
* Treat enforcement decisions as authoritative
* Build layered policies using inheritance
* Rely on audit events for evidence

You should **not**:

* Rely on undocumented behavior
* Assume future compatibility without version pinning
* Treat ai-governor as a compliance certification

---

## 9️⃣ Versioning Commitment

* v0.3.x → bug fixes only
* v0.4 → new governance capabilities
* v1.0 → only after long-term field usage

ai-governor will not rush a 1.0.

---

## Final Statement

v0.3 is the first version of ai-governor that is:

> **Composable, enforceable, auditable, and stable enough to trust.**

All future work builds on this foundation.

