# MEMORY.md

## Purpose

This file documents efficient context memory strategies for ai-governor development. It enables rapid resumption and continuity of coding sessions, ensuring contributors and Copilot agents maintain deterministic, schema-driven workflows.

---

## Context Memory Guidelines

1. **Session State Tracking**
   - Record current branch, active files, and last test results.
   - Note any failing tests, uncommitted changes, or pending pushes.
   - Summarize recent commits and their intent.

2. **Active Development Context**
   - List current feature, bugfix, or refactor in progress.
   - Reference relevant schema sections (e.g., v0.2, v0.3 contract).
   - Document open questions, blockers, or decisions awaiting review.

3. **Test-First Workflow**
   - Always note which tests define the next implementation step.
   - Record which tests are expected to fail or pass after changes.

4. **Strict Schema Adherence**
   - Track which schema version is being targeted (e.g., v0.2, v0.3).
   - List any schema fields or enforcement rules under active development.

5. **Error and Decision Logging**
   - Summarize recent validation errors, enforcement decisions, and audit events.
   - Note any error messages that require improved clarity or coverage.

6. **Resumption Checklist**
   - What was the last command run? (e.g., pytest, git push)
   - Which files were edited most recently?
   - What is the next planned action (test, code, commit, push)?

---

## Example Session Memory

- **Branch:** v0.4-dev
- **Active File:** tests/v0_4_schema/test_model_family_rules.py
- **Last Command:** pytest tests/v0_3_contract (all passed)
- **Recent Commit:** "Add failing v0.2 tool argument and model family rule tests"
- **Current Focus:** Implement minimal model family evaluation (deny > allow, explicit > family)
- **Schema Target:** v0.2 (see docs/policy-schema-v0.2.md)
- **Next Step:** Write/verify enforcement logic for tool argument governance

---

## Session Summary (2026-02-28)

- **Active Branch:** v0.4-dev
- **Files Being Edited:**
  - MEMORY.md
  - tests/v0_4_schema/test_model_family_rules.py
  - tests/v0_4_schema/test_tool_argument_governance.py
  - core/policy_validator.py
- **Last Command Run:**
  - .venv/bin/python -m pytest tests/v0_3_contract (all passed)
- **Recent Commits:**
  - Add failing v0.2 tool argument and model family rule tests
  - Add failing schema dispatch tests for v0.4
  - Freeze v0.2 schema draft
- **Current Development Focus:**
  - Implement minimal model family evaluation (deny > allow, explicit > family)
  - Ensure strict schema-driven enforcement for v0.2 features
- **Targeted Schema Version:** v0.2 (see docs/policy-schema-v0.2.md)
- **Failing Tests/Errors:**
  - All contract and schema tests currently pass
- **Next Planned Action:**
  - Implement minimal enforcement logic for tool argument governance
- **Open Questions/Blockers:**
  - None at this time

---

## Usage

Update MEMORY.md at the start and end of each session, or when switching tasks. Use it to quickly restore context, communicate session state to collaborators, and ensure strict adherence to ai-governor development conventions.
