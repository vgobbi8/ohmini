# Spec 15 — End-to-End Prototype Acceptance

## Goal

Prove that the complete minimal architecture works before adding any additional TCC feature.

Do not start SKiDL, RAG, LangGraph, repair, KiCad UI, or a frontend until this spec passes.

---

## Scenario A — deterministic no-LLM test

Run:

```text
FakeModelBackend
    ↓
DirectSpiceGenerator
    ↓
CircuitPipeline
    ↓
NgSpiceValidator
```

The fake backend returns a valid RC circuit netlist.

Expected:

- pipeline status `passed`;
- ngspice status `passed`;
- complete run directory exists;
- no credentials required;
- no internet required.

This is mandatory.

---

## Scenario B — Codex CLI

Prerequisites:

- Codex CLI installed;
- user already authenticated locally;
- ngspice installed.

Configuration:

```bash
OHMNI_MODEL_BACKEND=harness
OHMNI_MODEL_PROVIDER=codex
OHMNI_MODEL=<explicit-model>
OHMNI_GENERATOR=direct-spice
OHMNI_VALIDATORS=ngspice
```

Run a simple requirement:

```text
Create an RC low-pass filter with a 1 kHz cutoff and include an AC analysis suitable for checking its frequency response.
```

Expected:

- model runs in isolated workspace, not repository root;
- raw model response is preserved;
- SPICE netlist is extracted;
- ngspice is invoked;
- result is reported;
- all artifacts are persisted.

The circuit is allowed to fail validation. A failure must still be captured correctly.

---

## Scenario C — API backend

Use either OpenAI or Anthropic.

Example:

```bash
OHMNI_MODEL_BACKEND=api
OHMNI_MODEL_PROVIDER=openai
OHMNI_MODEL=<explicit-model>
OPENAI_API_KEY=<local-secret>
```

Run the same requirement used in Scenario B.

Expected:

- same generator;
- same pipeline;
- same validator;
- different model backend only.

No code change is allowed between Scenario B and C.

---

## Scenario D — backend swap

Change:

```text
harness/codex
```

to:

```text
harness/opencode
```

or another installed harness provider.

Expected:

- configuration-only change;
- no direct SPICE generator modification;
- no pipeline modification;
- no validator modification.

If the local CLI is unavailable, the application must fail with a clear infrastructure/configuration error.

---

## Required documentation

Update the project README with a concise section:

```text
Architecture
Configuration
Running with a CLI backend
Running with an API backend
Artifacts
Testing
Third-party code
```

Do not write the entire TCC into the README.

---

## Final quality gate

Before declaring the prototype complete:

- default tests pass;
- no secrets are tracked;
- `.env` is ignored;
- no paid calls occur during tests;
- real model calls use an isolated workspace;
- ngspice result semantics are accurately described;
- old working functionality remains available;
- vendored attribution exists;
- code contains no unfinished architecture branch that is required for the happy path.

---

## Stop condition

Once this passes, stop feature development and use the prototype for experiments/documentation unless a concrete TCC requirement is missing.

The prototype is intentionally small.
