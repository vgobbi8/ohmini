# Spec 02 — Configuration Layer

## Goal

Make environment variables the single primary runtime configuration surface while exposing typed settings to the rest of the application.

Environment variables must be read once at startup and converted into typed configuration.

---

## Required environment variables

Use the `OHMNI_` prefix for Ohmni-owned runtime behavior.

### Model

```bash
OHMNI_MODEL_BACKEND=harness
OHMNI_MODEL_PROVIDER=codex
OHMNI_MODEL=<explicit-model-name>
OHMNI_MODEL_TIMEOUT_SECONDS=300
```

Allowed initial backend values:

```text
harness
api
```

Initial harness providers:

```text
codex
claude-code
opencode
```

Initial API providers:

```text
openai
anthropic
```

### Generation

```bash
OHMNI_GENERATOR=direct-spice
```

### Validation

```bash
OHMNI_VALIDATORS=ngspice
OHMNI_NGSPICE_EXECUTABLE=ngspice
OHMNI_NGSPICE_TIMEOUT_SECONDS=30
```

`OHMNI_VALIDATORS` must be comma-separated and normalized into an ordered tuple/list.

### Output

```bash
OHMNI_OUTPUT_DIR=out
```

### Optional dotenv behavior

Local development may load `.env` if the project already supports that pattern or if a minimal dependency is justified.

Real environment variables must override `.env`.

Never require `.env` in production or tests.

---

## Provider credentials

Do not invent a generic `OHMNI_API_KEY`.

Provider secrets must use provider-native variables, for example:

```bash
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
```

The typed Ohmni settings object must **not** store the raw secret unless a provider library absolutely requires receiving it explicitly.

Prefer letting official integrations read their standard environment variables.

No secret may be included in:

- `repr(settings)`;
- logs;
- `config.json`;
- run manifests;
- validation reports;
- exception messages;
- test snapshots.

---

## Required implementation

Create an immutable typed settings model.

Suggested shape:

```python
@dataclass(frozen=True)
class ModelSettings:
    backend: str
    provider: str
    model: str
    timeout_seconds: int

@dataclass(frozen=True)
class GenerationSettings:
    generator: str

@dataclass(frozen=True)
class ValidationSettings:
    validators: tuple[str, ...]
    ngspice_executable: str
    ngspice_timeout_seconds: int

@dataclass(frozen=True)
class OutputSettings:
    output_dir: Path

@dataclass(frozen=True)
class Settings:
    model: ModelSettings
    generation: GenerationSettings
    validation: ValidationSettings
    output: OutputSettings
```

Equivalent Pydantic settings are acceptable if they reduce code and fit the existing repository.

Do not expose Pydantic-specific types outside the configuration module.

---

## Validation rules

Fail fast with a clear configuration error when:

- backend is unknown;
- provider is incompatible with backend;
- model is blank;
- timeout is <= 0;
- validator list is empty;
- output directory value is blank.

Do **not** check API credentials until the selected API provider is actually instantiated.

This allows harness-based execution without API keys.

---

## Configuration snapshots

Expose a method/function that returns a sanitized JSON-serializable snapshot:

```python
settings.to_public_dict()
```

It should include behavior-affecting values such as:

- backend;
- provider;
- model;
- timeouts;
- generator;
- validators;
- ngspice executable name/path;
- output directory.

It must exclude secrets.

---

## `.env.example`

Populate it with:

```bash
# Model execution
OHMNI_MODEL_BACKEND=harness
OHMNI_MODEL_PROVIDER=codex
OHMNI_MODEL=
OHMNI_MODEL_TIMEOUT_SECONDS=300

# Circuit generation
OHMNI_GENERATOR=direct-spice

# Validation
OHMNI_VALIDATORS=ngspice
OHMNI_NGSPICE_EXECUTABLE=ngspice
OHMNI_NGSPICE_TIMEOUT_SECONDS=30

# Output
OHMNI_OUTPUT_DIR=out

# API credentials: only required for the selected API provider
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
```

---

## Tests

Cover:

- valid harness settings;
- valid API settings;
- invalid backend;
- provider/backend mismatch;
- blank model;
- timeout validation;
- comma-separated validators;
- environment precedence over `.env` if dotenv is supported;
- sanitized snapshot contains no secrets.

Use monkeypatching/environment isolation.

---

## Acceptance criteria

- All environment access is centralized.
- Application code can depend on typed settings only.
- Invalid combinations fail before model execution.
- API keys are never persisted or printed.
- Harness configuration works without API keys.
