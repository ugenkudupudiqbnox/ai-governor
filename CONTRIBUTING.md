Below is a **discipline-setting, maintainer-friendly `CONTRIBUTING.md`** you can commit as-is.
Tone: firm, respectful, and aligned with governance infrastructure (not hobby OSS).

Create this file at:

```
CONTRIBUTING.md
```

---

# Contributing to ai-governor

Thank you for your interest in contributing to **ai-governor**.

This project deals with **runtime governance, security, and compliance controls** for LLM systems.
As such, contributions are expected to meet a **higher bar for clarity, intent, and discipline** than typical application code.

This document explains **how to contribute effectively** and **what expectations apply**.

---

## Project Philosophy (Read First)

Before contributing, please read:

* [`docs/WHY_THIS_EXISTS.md`](docs/WHY_THIS_EXISTS.md)
* [`docs/policy-schema-v0.1.md`](docs/policy-schema-v0.1.md)

If your contribution conflicts with the project’s **direction or non-goals**, it is unlikely to be merged.

---

## What We Value Most

We prioritize contributions that improve:

1. **Correctness**
2. **Determinism**
3. **Auditability**
4. **Clarity of governance intent**
5. **Long-term maintainability**

More code is **not** inherently better code.

---

## How to Contribute (Preferred Order)

### 1. Start With a Discussion (Strongly Recommended)

For anything beyond a trivial fix:

* Open a **GitHub Discussion** first
* Explain:

  * The problem you are solving
  * Why it belongs in ai-governor
  * Which policy or enforcement gap it addresses

This prevents wasted effort and misaligned PRs.

---

### 2. Open an Issue (If Appropriate)

Issues should be:

* Focused
* Reproducible
* Clearly scoped

Avoid:

* Feature dumps
* Vague “support X” requests
* Legal or regulatory interpretations

---

### 3. Submit a Pull Request

Pull Requests must:

* Reference an Issue or Discussion
* Be small and reviewable
* Include tests where applicable
* Preserve backward compatibility unless explicitly discussed

---

## Contribution Rules (Non-Negotiable)

### 1. Policy Before Code

If your change affects governance behavior:

* Update or reference the **policy schema**
* Explain enforcement semantics clearly

No implicit behavior.

---

### 2. Deterministic Behavior Only

Governance decisions must be:

* Predictable
* Explainable
* Repeatable

Avoid:

* Hidden heuristics
* Non-deterministic logic
* Silent failures

---

### 3. Explicit Over Implicit

Good governance code favors:

* Explicit enums
* Clear defaults
* Verbose reasoning

Over:

* Magic values
* Inferred behavior
* “Smart” shortcuts

---

### 4. No Vendor Lock-In

Core logic must remain:

* Model-agnostic
* Provider-neutral

Provider-specific code belongs in clearly isolated adapters.

---

### 5. No Legal Claims

Do **not**:

* Claim regulatory compliance
* Encode legal interpretations
* Use compliance standards as enforcement truth

ai-governor supports **technical controls**, not legal certification.

---

## Code Style & Standards

### General

* Prefer clarity over cleverness
* Small functions > large abstractions
* Comment *why*, not *what*

### Python

* Python ≥ 3.9
* Type hints encouraged
* No unused dependencies

### Naming

* Use governance language (`policy`, `decision`, `enforcement`)
* Avoid UI or product-oriented naming

---

## Testing Expectations

If you add enforcement logic:

* Include at least one test that:

  * Demonstrates ALLOW
  * Demonstrates BLOCK or MODIFY
* Tests should be readable and intention-revealing

Untested enforcement logic is unlikely to be merged.

---

## Backward Compatibility

For v0.x:

* Breaking changes require discussion
* Policy schema changes must be versioned
* Existing example policies must continue to validate

---

## What We Are Not Looking For

Please do **not** submit PRs that:

* Turn ai-governor into a chatbot framework
* Add UI dashboards
* Introduce heavy ML moderation pipelines
* Bundle hosted services
* Add unrelated utilities

These may be good ideas — just not for this repository.

---

## Security Issues

If you discover a security vulnerability:

* **Do not open a public issue**
* Use GitHub Security Advisories (preferred)
* Or contact the maintainers privately

---

## Maintainer Discretion

Maintainers may:

* Request changes
* Close issues or PRs that are out of scope
* Prioritize design discussions over implementation

This is intentional and aligned with the project’s goals.

---

## Final Note

ai-governor aims to be **boring, correct infrastructure**.

If your contribution helps make governance:

* Clearer
* More enforceable
* More auditable

…it is very welcome.

Thank you for contributing.
