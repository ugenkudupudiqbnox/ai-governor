# CI Pipeline Example (Policy Gating with ai-governor)

This example shows how to use **ai-governor in CI** to **block unsafe or non-compliant LLM configurations before deployment**.

The pipeline will:

* Validate the policy
* Enforce governance rules
* Fail the build if governance returns `BLOCK`
* Allow `MODIFY` and `ALLOW` explicitly

---

## Example: GitHub Actions

### Use case

> Prevent deploying services that use **disallowed models, regions, or unsafe data handling**.

---

## 1️⃣ Repository Structure (Example)

```
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

---

## 3️⃣ GitHub Actions Workflow

Create:

```
.github/workflows/ai-governor.yml
```

### ✅ `ai-governor.yml`

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

---

## 4️⃣ How CI Enforcement Works

The key behavior is driven by **exit codes**:

| Exit Code | Meaning | CI Result                   |
| --------- | ------- | --------------------------- |
| `0`       | ALLOW   | ✅ Pass                      |
| `10`      | MODIFY  | ✅ Pass (redaction required) |
| `20`      | BLOCK   | ❌ Fail                      |
| `1–3`     | Error   | ❌ Fail                      |

### Example: BLOCK fails the build

If someone changes the workflow to:

```bash
--model gpt-4.1-preview
```

CI output:

```
final_decision: BLOCK
reason: Model 'gpt-4.1-preview' is explicitly denied by policy
```

➡️ **Pipeline fails automatically**

---

## 5️⃣ Optional: Capture Audit Logs in CI

You can persist audit evidence as CI artifacts.

### Add this step:

```yaml
      - name: Save audit logs
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

This creates **immutable governance evidence per build**.

---

## 6️⃣ Why This Matters (For Reviewers & Auditors)

With this pipeline you can prove:

* Governance rules exist ✔️
* They are enforced automatically ✔️
* Violations block deployment ✔️
* Decisions are logged ✔️
* Enforcement is deterministic ✔️

This directly supports:

* SOC 2 CC7.x
* ISO 27001 A.12.4
* Internal AI governance controls

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

This CI setup turns **AI governance from documentation into an enforceable gate**.

> If it violates policy, it never ships.

That’s the real value of **ai-governor**.

