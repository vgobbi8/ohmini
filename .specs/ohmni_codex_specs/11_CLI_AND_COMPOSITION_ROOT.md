# Spec 11 — CLI and Composition Root

## Goal

Wire typed environment configuration into concrete runtime implementations without contaminating core layers.

The composition root is the only place that should contain implementation-selection logic.

---

## Preserve the existing CLI

Inspect the current CLI.

If a working command already exists:

- extend it;
- preserve backward compatibility when practical;
- do not rename the package/entry point just to match this document.

Add a `run` command or equivalent only if needed.

---

## Composition

Implement factories in the startup/composition layer.

### Model backend

Conceptually:

```python
def create_model_backend(settings: ModelSettings) -> ModelBackend:
    match settings.backend:
        case "harness":
            return HarnessModelBackend(...)
        case "api":
            return LangChainApiModelBackend(...)
        case _:
            raise ModelConfigurationError(...)
```

Provider selection for each backend remains inside that backend/factory.

### Generator

```python
def create_generator(settings, backend):
    if settings.generation.generator == "direct-spice":
        return DirectSpiceGenerator(backend)
```

Do not add SKiDL yet.

### Validators

Build validators from the ordered configured list.

Unknown names should fail with a clear configuration error.

### Pipeline

Construct the pipeline with explicit dependencies.

---

## CLI behavior

Support a command equivalent to:

```bash
<ohmni> run "Design an RC low-pass filter..."
```

Also support reading a requirement from a text/fixture file if the existing CLI already does so.

Do not force users to put multiline engineering requirements in an environment variable.

---

## Terminal output

Keep output compact.

Example:

```text
Run: 20260810T203100Z-8f21c4
Backend: harness/codex/<model>
Generator: direct-spice
Validation:
  ngspice: PASSED
Artifacts: out/runs/20260810T203100Z-8f21c4
Overall: PASSED
```

On failure, show the first useful issue and artifact directory.

Do not dump full model output or ngspice logs by default.

---

## Exit codes

Use stable exit behavior:

```text
0 = pipeline passed
1 = circuit/generation/validation failed
2 = configuration or infrastructure error
```

If the existing CLI already has an exit-code convention, integrate cleanly instead of creating conflicts.

---

## Configuration display

Optional but useful:

```bash
<ohmni> config
```

May display the sanitized configuration snapshot.

Never display secrets.

Do not add this command if it meaningfully delays the core prototype.

---

## Tests

Use CLI test tooling already present in the project.

Cover:

- successful fake-backed run;
- invalid config;
- generation failure;
- validator failure;
- exit codes;
- no secret output;
- implementation selection based on settings.

No real CLI-agent or API invocation in normal tests.

---

## Acceptance criteria

The following changes require no generator changes:

```text
harness/codex -> harness/opencode
harness/codex -> api/openai
api/openai -> api/anthropic
```

They are configuration/composition changes only.
