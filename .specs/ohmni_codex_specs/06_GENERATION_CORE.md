# Spec 06 — Circuit Generation Core

## Goal

Define an incrementable generation boundary so direct SPICE generation remains working when SKiDL or another representation is added later.

---

## `CircuitGenerationRequest`

Create:

```python
@dataclass(frozen=True)
class CircuitGenerationRequest:
    requirement: str
```

Validation:

- non-blank requirement.

Do not add dozens of speculative fields.

Future constraints can be added when real use cases require them.

---

## `GeneratedCircuit`

Create a representation that separates the generator's source artifact from the common SPICE validation artifact.

Suggested shape:

```python
@dataclass(frozen=True)
class GeneratedCircuit:
    generator: str
    source_type: str
    source_text: str
    spice_netlist: str
    model_response: ModelResponse | None = None
```

Initial direct-SPICE behavior:

```text
source_type = "spice"
source_text = normalized SPICE
spice_netlist = normalized SPICE
```

Future SKiDL behavior:

```text
source_type = "skidl"
source_text = generated SKiDL source
spice_netlist = compiled SPICE netlist
```

This is the key incrementability requirement.

If retaining the complete `ModelResponse` inside the domain object feels too coupled/heavy, use a lightweight generation metadata object instead. What matters is that run artifacts can trace the model used and raw output.

---

## `CircuitGenerator`

```python
class CircuitGenerator(Protocol):
    @property
    def name(self) -> str:
        ...

    def generate(
        self,
        request: CircuitGenerationRequest,
    ) -> GeneratedCircuit:
        ...
```

Do not make generator selection an `if/elif` inside the pipeline.

Selection belongs in the composition root/factory.

---

## Errors

Add generation-owned exceptions:

```text
CircuitGenerationError
CircuitOutputParseError
```

Model errors may propagate with context or be wrapped while preserving cause.

---

## Testing helper

Implement a `FakeCircuitGenerator` only if it materially simplifies pipeline tests.

Do not add it if the existing `FakeModelBackend + DirectSpiceGenerator` is sufficient.

---

## Acceptance criteria

- The pipeline can depend on `CircuitGenerator`.
- Validators receive a generated circuit with a SPICE netlist regardless of the source representation.
- No SKiDL dependency is added.
- Direct SPICE can remain as a permanent strategy.
