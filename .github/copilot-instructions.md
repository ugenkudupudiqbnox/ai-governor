# AI Governor – Copilot Agent Instructions

## Project Overview

**ai-governor** is a model-level governance runtime for LLM systems. It enforces deterministic, auditable control policies *between your application and the model*, returning `ALLOW`, `BLOCK`, or `MODIFY` decisions before model execution.

**Key insight:** This is NOT a prompt framework or safety wrapper—it's a governance control plane. Policies are code-like, composable, and deterministic.

---

## Architecture

### Core Entry Point: `EnforcementOrchestrator`
Located in [core/enforcement/orchestrator.py](core/enforcement/orchestrator.py), this class orchestrates the entire enforcement pipeline:

1. **Policy Validation** → Checks policy structure against schema v0.1
2. **Model Enforcement** → Allow/deny lists + token limits
3. **Region Enforcement** → Jurisdiction-based restrictions
4. **Tool Enforcement** → Tool/agent governance
5. **PII Enforcement** → Detect + redact/block sensitive data
6. **Audit Emission** → Emit immutable Decision events

**Critical pattern:** Enforcement stops immediately on `BLOCK` decision (early termination in orchestrator.enforce).

### Decision & Audit Model
- [core/decision.py](core/decision.py): `Decision` is immutable (frozen dataclass), with `DecisionType` enum: `ALLOW`, `BLOCK`, `MODIFY`
- [core/audit/emitter.py](core/audit/emitter.py): `AuditEventEmitter` generates audit-grade JSON logs with full decision context
- Every enforcement function returns a `Decision` object with reason, policy_section, policy_version, and metadata

### Policy Loading & Validation
- [core/policy/loader.py](core/policy/loader.py): Recursive policy inheritance via `extends` field; detects cycles
- [core/policy_validator.py](core/policy_validator.py): Validates against schema v0.1
- Policy files are YAML; see [docs/policy-schema-v0.1.md](docs/policy-schema-v0.1.md) for complete structure

### Enforcement Modules
Each enforcer returns a `Decision` and is called by orchestrator in strict order:
- [core/enforcement/model.py](core/enforcement/model.py): Model allow/deny (fnmatch patterns), max_tokens limit
- [core/enforcement/region.py](core/enforcement/region.py): Geographic/jurisdiction enforcement
- [core/enforcement/tools.py](core/enforcement/tools.py): Tool/agent allowlists
- [core/enforcement/data.py](core/enforcement/data.py): PII detection (email, phone, credit card) → block/redact/allow actions
- [core/redaction/engine.py](core/redaction/engine.py): Deterministic redaction using regex patterns

---

## Key Conventions

### Immutability & Determinism
- `Decision` objects are frozen dataclasses; never mutate them
- All decisions must be deterministic (same input → same output)
- No randomness or external API calls in enforcement functions

### PII Detection & Redaction
- Regex patterns in [core/enforcement/data.py](core/enforcement/data.py) and [core/redaction/engine.py](core/redaction/engine.py) must be kept **in sync**
- Supported types: `email`, `phone`, `credit_card`
- `RedactionResult` includes both redacted text and list of detected entity types

### Policy Versioning
- All policies require `version: 0.1` (frozen in v0.3)
- Child policies extending a parent must have matching version
- Validation enforces this strictly; mismatch raises `PolicyVersionMismatchError`

### CLI Integration
- [cli/main.py](cli/main.py): Two subcommands: `validate` (check policy), `enforce` (run governance)
- `enforce` returns JSON with `final_decision`, `decisions` array, and optional `output_text`
- Context is passed as optional JSON file; metadata flows through the entire audit trail

---

## Testing Patterns

Tests use simple `pytest` conventions without fixtures. Key patterns:

- **Decision creation**: Use factory methods: `Decision.allow()`, `Decision.block()`, `Decision.modify()`
- **Policy loading**: Test inheritance via `extends` and cycle detection
- **Orchestrator**: Test early termination on `BLOCK` decision
- **Audit emission**: Verify events contain complete decision context + metadata
- **Redaction**: Check both text output and entity detection

Example (from [tests/test_decision.py](tests/test_decision.py)):
```python
decision = Decision.block(reason="Test", policy_section="test.section")
assert decision.to_dict()["decision"] == "BLOCK"
```

See [tests/v0_3_contract](tests/v0_3_contract) for v0.3 contract tests; these establish stability boundaries.

---

## Developer Workflows

### Setup & Testing
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
pytest tests/  # Run all tests
pytest tests/v0_3_contract/  # Verify v0.3 stability contract
```

### Validate a Policy
```bash
ai-governor validate policy.yaml --json --strict
```

### Enforce a Policy (CLI)
```bash
ai-governor enforce --policy policy.yaml --model gpt-4 --region EU --text "user input" --verbose
```

### Examples
- [examples/demo_app](examples/demo_app): Minimal CLI example with policy.yaml
- [examples/fastapi_demo](examples/fastapi_demo): FastAPI integration example

---

## Common Patterns

### Adding a New Enforcement Rule
1. Create a function in [core/enforcement/](core/enforcement/) that returns `Decision`
2. Add it to orchestrator.enforce() in correct order (before or after audit/decision check)
3. Write tests in [tests/](tests/)
4. Update policy schema docs if it requires new YAML fields

### Extending Audit Capabilities
- Add new `AuditSink` implementations in [core/audit/sinks.py](core/audit/sinks.py)
- Sinks must implement `write(event: AuditEvent)` method
- Default is `StdoutSink`; file sink, hardening sink also supported

### Redaction & PII
- Update patterns in **both** [core/enforcement/data.py](core/enforcement/data.py) (detection) **and** [core/redaction/engine.py](core/redaction/engine.py) (replacement)
- Keep `REDACTION_MAP` and detection logic synchronized
- Test via [tests/test_redaction_engine.py](tests/test_redaction_engine.py)

---

## Critical Stability Commitments

From [docs/STABILITY.md](docs/STABILITY.md):
- Policy schema v0.1 is frozen; new schema versions require major version bump
- `Decision` and `DecisionType` enums are stable; no values will be removed
- Enforcement ordering in orchestrator is part of the public contract
- Audit event JSON schema is stable

When modifying core decision-making logic, ensure [tests/v0_3_contract](tests/v0_3_contract) tests still pass.

---

## File Organization

```
core/              → Governance runtime logic
  enforcement/    → Individual enforcement modules (model, region, tools, data)
  policy/         → Policy loading, merging, validation
  audit/          → Event emission and sinks
  redaction/      → PII redaction engine
  decision.py     → Core Decision + DecisionType
  policy_engine.py, policy_validator.py

cli/               → CLI subcommands (validate, enforce)
docs/              → Schema, quick start, stability guarantees
examples/          → Demo applications (CLI, FastAPI)
tests/             → Unit tests; v0_3_contract/ for stability tests
```

---

## When Contributing

- **Determinism first:** No external API calls, randomness, or side effects in enforcement
- **Audit trail:** Every decision must be traceable; include metadata
- **Version stability:** Check [docs/STABILITY.md](docs/STABILITY.md) before changing core types
- **Test contract:** All v0_3_contract tests must pass
- **Policy examples:** Update [compliance/base-policy.example.yaml](compliance/base-policy.example.yaml) if adding schema features
