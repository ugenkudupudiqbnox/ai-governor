# CI Pipeline Example — Policy Gating with ai-governor (v0.3)

This document shows how to use **ai-governor in CI/CD** to **block unsafe or non-compliant LLM configurations before deployment**.

This example is compatible with **ai-governor v0.3 (feature-frozen)** and relies only on **stable CLI behavior**.

---

## What This Pipeline Does

The pipeline will:

- Validate the governance policy
- Enforce governance rules at build time
- Fail the build if governance returns `BLOCK`
- Allow `ALLOW` and `MODIFY` explicitly
- Produce machine-verifiable audit evidence

No model calls are made.

---

## Example: GitHub Actions

### Use Case

> Prevent deploying services that use **disallowed models, regions, tools, or unsafe data handling rules**.

---

## 1️⃣ Repository Structure (Example)

```text
.
├── policy.yaml
├── prompts/
│   └── sample.txt
└── .github/
    └── workflows/
        └── ai-governor.yml
```

---

## 2️⃣ Sample Policy (`policy.yaml`)

```yaml
version: 0.1

model:
  allow:
    - gpt-4.1
  deny:
    - "*-preview"

data:
  regions:
    allowed: ["IN", "EU"]
  pii:
    action: redact
```

This policy is intentionally simple and deterministic.

---

## 3️⃣ GitHub Actions Workflow

Create the following workflow file:

```
.github/workflows/ai-governor.yml
```

### `ai-governor.yml`

```yaml
name: AI Governance Check

on:
  pull_request:
  push:
    branches: [ main ]

jobs:
  ai-governance:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.10"

      - name: Install ai-governor
        run: |
          python -m venv .venv
          source .venv/bin/activate
          pip install -e .

      - name: Validate governance policy
        run: |
          source .venv/bin/activate
          ai-governor validate policy.yaml

      - name: Enforce governance rules
        run: |
          source .venv/bin/activate
          ai-governor enforce \
            --policy policy.yaml \
            --model gpt-4.1 \
            --region IN \
            --text @prompts/sample.txt
```

If governance returns `BLOCK`, the job fails automatically.

---

## 4️⃣ How CI Enforcement Works

ai-governor uses **exit codes** to integrate cleanly with CI systems.

| Exit Code | Meaning | CI Result |
|---------|--------|-----------|
| `0` | ALLOW | ✅ Pass |
| `10` | MODIFY (redaction required) | ✅ Pass |
| `20` | BLOCK | ❌ Fail |
| `1–3` | Validation / runtime error | ❌ Fail |

### Example: BLOCK Fails the Build

If the workflow is changed to:

```bash
--model gpt-4.1-preview
```

The enforcement step exits with code `20`, causing the pipeline to fail.

---

## 5️⃣ Optional: Persist Audit Evidence in CI

You can capture audit logs as CI artifacts.

### Example

```yaml
      - name: Capture audit logs
        if: always()
        run: |
          mkdir -p audit
          ai-governor enforce \
            --policy policy.yaml \
            --model gpt-4.1 \
            --region IN \
            --text @prompts/sample.txt \
            > audit/audit.jsonl

      - name: Upload audit logs
        uses: actions/upload-artifact@v4
        with:
          name: ai-governor-audit
          path: audit/
```

Each line in `audit.jsonl` is a complete, append-only governance decision.

> Note: if audit logging fails, enforcement fails by design.

---

## 6️⃣ What This Proves (For Reviewers & Auditors)

This pipeline demonstrates that:

- Governance rules exist ✔️
- They are enforced automatically ✔️
- Violations block deployment ✔️
- Decisions are logged ✔️
- Enforcement is deterministic ✔️

These are **technical controls**, not compliance claims.

---

## 7️⃣ GitLab CI (Minimal Example)

```yaml
ai_governance:
  image: python:3.10
  script:
    - pip install -e .
    - ai-governor validate policy.yaml
    - ai-governor enforce --policy policy.yaml --model gpt-4.1 --region IN --text "hello"
```

---

## Key Takeaway

This CI setup turns **AI governance from documentation into an enforceable deployment gate**.

> If it violates policy, it does not ship.

That is the core value of **ai-governor**.
