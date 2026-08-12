# Spec 13 — Testing Strategy

## Goal

Make the prototype safe to refactor and extend without spending paid model quota during normal development.

---

## Test pyramid for this project

### 1. Pure unit tests

Fast and default.

Cover:

- settings;
- core contracts;
- parsing/normalization;
- status aggregation;
- factories;
- artifact serialization.

### 2. Adapter contract tests

Mock the external boundary.

Cover:

- harness `RunSpec` mapping;
- harness result mapping;
- LangChain request/response mapping;
- subprocess call construction for ngspice.

### 3. Local integration tests

Optional/marked.

Examples:

```text
ngspice integration
codex CLI integration
OpenCode integration
API integration
```

These must not run by default.

### 4. End-to-end deterministic test

Use:

```text
FakeModelBackend -> DirectSpiceGenerator -> real ngspice
```

when ngspice is installed.

The fake backend returns a known-valid RC netlist.

This validates the entire Ohmni architecture without paid LLM usage.

---

## No-paid-calls rule

Normal commands such as:

```bash
pytest
uv run pytest
```

must never:

- call OpenAI;
- call Anthropic;
- call Codex;
- call Claude Code;
- call OpenCode;
- access the internet.

Real-model integration tests require an explicit marker and opt-in environment variable.

Example:

```text
OHMNI_RUN_PAID_INTEGRATION_TESTS=1
```

Do not include this variable in normal `.env.example` unless clearly marked advanced.

---

## Fixtures

Create small deterministic fixture circuits.

Minimum:

```text
valid_rc_lowpass.cir
invalid_spice.cir
```

Keep them understandable enough to include in the TCC.

---

## Test markers

Suggested:

```text
integration
ngspice
model_cli
model_api
paid
```

Use the repository's existing test-marker conventions if present.

---

## Required tests by layer

Ensure coverage exists for:

- environment settings;
- fake backend;
- harness backend mapping;
- API backend mapping;
- direct SPICE generator;
- ngspice validator;
- pipeline;
- run artifacts;
- CLI exit behavior.

Do not chase an arbitrary coverage percentage if it wastes time.

Focus on architectural boundaries and failure modes.

---

## Reproducibility test

Add a test that verifies a completed fake run writes:

- request;
- sanitized config;
- model response;
- generated netlist;
- validation result;
- final report.

---

## Acceptance criteria

- Default test suite requires no credentials.
- Default test suite consumes no subscription/API quota.
- External tools/services are opt-in.
- Fake backend can drive the complete pipeline.
