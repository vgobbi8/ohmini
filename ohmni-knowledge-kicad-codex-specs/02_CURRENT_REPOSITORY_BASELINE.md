# 02 — Current Repository Baseline

Before editing, Codex must inspect the current `main` branch and reconcile this spec with the real repository.

The current architecture is expected to contain equivalents of:

```text
src/ohmni/
├── config/
├── generation/
├── model/
├── pipeline/
├── validation/
└── cli.py
```

Important existing contracts expected at the time this dossier was written:

```python
ModelBackend.invoke(ModelRequest) -> ModelResponse
CircuitGenerator.generate(CircuitGenerationRequest) -> GeneratedCircuit
CircuitValidator.validate(GeneratedCircuit, ValidationContext) -> ValidationResult
```

Existing behavior includes:

- direct LLM-to-SPICE generation;
- backend abstraction for model execution;
- ngspice validation;
- run artifact persistence;
- CLI composition;
- fake backend support for tests.

## Required preservation

Do not delete or unnecessarily rename existing abstractions merely to fit this dossier.

If the repository has evolved, adapt the design to equivalent current structures. Document every deliberate deviation.

## Desired new top-level concepts

```text
src/ohmni/knowledge/
src/ohmni/eda/
```

Do not introduce provider/tool dependencies into `model/contracts.py`, `generation/contracts.py`, or validation core contracts unless an explicit compatibility extension is required.
