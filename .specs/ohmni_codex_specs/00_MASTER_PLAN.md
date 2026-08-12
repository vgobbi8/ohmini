# Ohmni TCC Prototype — Codex Master Implementation Plan

## Purpose

Implement the smallest useful and incrementable Ohmni prototype for the TCC.

The prototype must prove this pipeline:

```text
Natural-language circuit requirement
        ↓
CircuitGenerator
        ↓
ModelBackend
        ↓
LLM / coding-agent execution
        ↓
SPICE netlist
        ↓
CircuitValidator(s)
        ↓
ngspice
        ↓
Reproducible run artifacts + PASS/FAIL report
```

The implementation must preserve the ability to add, without rewriting old implementations:

- new model execution mechanisms;
- API-key-based providers;
- subscription-authenticated CLI agents;
- new circuit-generation strategies such as SKiDL;
- new validators;
- a future repair loop;
- future RAG;
- future LangGraph orchestration.

The first version must stay deliberately small. Do **not** build the final Ohmni product.

---

## Global constraints

These rules apply to every spec in this directory.

1. Inspect the existing repository before changing anything.
2. Preserve existing working behavior unless a spec explicitly replaces it.
3. Do not rename the existing package, CLI entry point, or working commands unnecessarily.
4. Prefer extending existing structures over creating duplicate parallel structures.
5. Keep domain/core contracts independent of LangChain, Codex, OpenCode, Claude Code, ngspice, or any other provider/tool.
6. Environment variables are the primary runtime configuration surface.
7. Read environment variables only in the configuration/composition layer.
8. Do not scatter `os.getenv()` calls throughout the application.
9. Do not place API keys or credentials in domain models, reports, logs, fixtures, or committed files.
10. Do not add a frontend.
11. Do not add a database.
12. Do not add LangGraph yet.
13. Do not add RAG yet.
14. Do not add SKiDL yet.
15. Do not add an automatic correction loop yet.
16. Do not introduce production-scale abstractions where a small explicit contract is enough.
17. Do not use real paid LLM calls in automated tests.
18. Every real execution must leave reproducible artifacts on disk.
19. A validator may only claim what it actually checks. In particular, a successful ngspice run proves that the netlist is simulatable under that analysis; it does **not** automatically prove that the circuit satisfies the user's functional intent.
20. Keep all old generation strategies working when new ones are added later.

---

## Architectural boundaries

### Core model boundary

The stable application contract is:

```python
class ModelBackend(Protocol):
    def invoke(self, request: ModelRequest) -> ModelResponse:
        ...
```

A configured backend owns its provider/model details after startup.

Examples:

```text
HarnessModelBackend
    ├── Codex CLI
    ├── Claude Code
    └── OpenCode

LangChainApiModelBackend
    ├── OpenAI API
    └── Anthropic API
```

The rest of Ohmni must not know how the backend authenticates.

### Generation boundary

```python
class CircuitGenerator(Protocol):
    def generate(self, request: CircuitGenerationRequest) -> GeneratedCircuit:
        ...
```

Initial implementation:

```text
DirectSpiceGenerator
```

Future implementation:

```text
SkidlGenerator
```

Both must eventually expose a SPICE netlist for downstream validation.

### Validation boundary

```python
class CircuitValidator(Protocol):
    def validate(self, circuit: GeneratedCircuit, context: ValidationContext) -> ValidationResult:
        ...
```

Initial implementation:

```text
NgSpiceValidator
```

The pipeline must accept a list of validators even if only one exists initially.

---

## Required implementation order

Execute the specs in this order:

1. `01_PROJECT_FOUNDATION.md`
2. `02_CONFIGURATION_LAYER.md`
3. `03_MODEL_CORE_CONTRACTS.md`
4. `04_HARNESS_BACKEND.md`
5. `05_API_BACKEND_LANGCHAIN.md`
6. `06_GENERATION_CORE.md`
7. `07_DIRECT_SPICE_GENERATOR.md`
8. `08_VALIDATION_CORE.md`
9. `09_NGSPICE_VALIDATOR.md`
10. `10_PIPELINE_ORCHESTRATION.md`
11. `11_CLI_AND_COMPOSITION_ROOT.md`
12. `12_RUN_ARTIFACTS_AND_REPRODUCIBILITY.md`
13. `13_TESTING_STRATEGY.md`
14. `14_VENDORING_AND_LICENSES.md`
15. `15_END_TO_END_ACCEPTANCE.md`

`16_FUTURE_EXTENSION_POINTS.md` is architecture guidance only and must not be implemented unless explicitly requested later.

---

## Expected high-level package shape

Adapt this to the existing repository instead of blindly recreating it.

```text
src/ohmni/
├── config/
│   └── settings.py
├── model/
│   ├── contracts.py
│   ├── errors.py
│   └── backends/
│       ├── harness_backend.py
│       └── langchain_api_backend.py
├── generation/
│   ├── contracts.py
│   └── direct_spice.py
├── validation/
│   ├── contracts.py
│   └── ngspice.py
├── pipeline/
│   ├── circuit_pipeline.py
│   └── artifacts.py
├── cli.py
└── _vendor/
    └── agent_harness/
```

Do not force this exact tree if the repository already has an equivalent structure.

---

## Definition of done for the prototype

A user can configure a model through environment variables and run a command equivalent to:

```bash
OHMNI_MODEL_BACKEND=harness \
OHMNI_MODEL_PROVIDER=codex \
OHMNI_MODEL=<model> \
<existing-ohmni-cli> run "Create an RC low-pass filter..."
```

The application:

1. loads typed settings;
2. builds the requested `ModelBackend`;
3. injects it into `DirectSpiceGenerator`;
4. asks the model for a SPICE netlist;
5. persists the raw response;
6. normalizes/extracts the netlist;
7. executes ngspice;
8. captures stdout/stderr/logs;
9. emits structured validation results;
10. writes a sanitized run manifest;
11. prints a compact terminal summary;
12. exits predictably.

The same pipeline must also be runnable with an API backend without changing generator or validator code.

---

## Codex execution protocol

For each spec:

1. Read this master file and the target spec.
2. Inspect the current implementation before editing.
3. State a short implementation plan.
4. Implement only the requested scope plus strictly necessary supporting changes.
5. Add/update tests for the layer.
6. Run the smallest relevant test set.
7. Run lint/type checks already configured by the repository.
8. Do not "clean up" unrelated code.
9. At the end, report:
   - files changed;
   - tests executed;
   - command output summary;
   - remaining limitations;
   - any deviation from the spec and why.

Do not proceed to the next spec automatically unless explicitly instructed.
