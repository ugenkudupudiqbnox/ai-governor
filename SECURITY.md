# Security Policy

## Supported Versions

ai-governor is under active development.

| Version        | Supported |
| -------------- | --------- |
| v0.2.x (alpha) | ✅ Yes     |
| v0.1.x         | ❌ No      |
| < v0.1         | ❌ No      |

Security fixes are applied only to the **latest active alpha version**.

---

## Reporting a Vulnerability

If you discover a **security vulnerability**, please report it responsibly.

### ✅ Preferred Method (Recommended)

Use **GitHub Security Advisories**:

1. Go to the repository on GitHub
2. Click **Security → Advisories**
3. Click **“Report a vulnerability”**
4. Provide as much detail as possible

This allows coordinated disclosure and private discussion.

---

### 📧 Alternative (If GitHub Advisories Are Not Available)

You may report security issues by email to:

```
connect@qbnox.com
```

Please include:

* A clear description of the issue
* Steps to reproduce
* Potential impact
* Any proof-of-concept (if available)

---

## What Qualifies as a Security Issue

We consider the following **security-relevant**:

* Policy bypass or enforcement gaps
* Incorrect governance decisions (`ALLOW` instead of `BLOCK`)
* Audit log tampering or loss
* Sensitive data leakage via logs or metadata
* CLI behaviors that leak secrets or bypass controls
* Dependency vulnerabilities affecting enforcement or audit integrity

---

## What Does NOT Qualify

The following are **out of scope** for security reports:

* Feature requests
* Performance optimizations
* Missing governance rules
* Policy misconfiguration by users
* Legal or regulatory interpretations
* Theoretical ML safety concerns

ai-governor enforces **technical controls**, not model behavior guarantees.

---

## Disclosure Process

1. We acknowledge receipt within **72 hours**
2. We investigate and assess impact
3. We coordinate a fix and release
4. We credit reporters when appropriate (unless anonymity is requested)

We aim for **responsible disclosure**, not silent patching.

---

## Security Design Philosophy

ai-governor is designed with the following security principles:

* **Deterministic enforcement** over heuristic behavior
* **Explicit decisions** over implicit assumptions
* **Auditability by default**
* **No secret storage**
* **No network calls in core logic**
* **No provider lock-in**

Security issues are treated as **governance failures**, not edge cases.

---

## Final Note

ai-governor is early-stage software, but security and correctness are first-class concerns.

If something feels ambiguous, unsafe, or bypassable —
**we want to hear about it.**

Thank you for helping make governance infrastructure more reliable.
