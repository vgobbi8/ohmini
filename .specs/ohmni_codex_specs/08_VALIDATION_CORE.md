# Spec 08 — Validation Core

## Goal

Define a validator boundary that lets Ohmni add new deterministic checks without changing generation code.

---

## Validation semantics

Use explicit statuses:

```text
passed
failed
error
skipped
```

Distinguish:

- **failed**: validator executed and found the artifact invalid for the condition it checks;
- **error**: validator itself could not execute reliably;
- **skipped**: prerequisite or policy intentionally prevented execution.

Do not reduce everything to a boolean internally.

---

## `ValidationIssue`

Suggested shape:

```python
@dataclass(frozen=True)
class ValidationIssue:
    code: str
    message: str
    severity: str
```

Initial severity values may be:

```text
info
warning
error
```

Keep issue codes stable enough for experiments.

---

## `ValidationResult`

Suggested shape:

```python
@dataclass(frozen=True)
class ValidationResult:
    validator: str
    status: ValidationStatus
    issues: tuple[ValidationIssue, ...]
    summary: str
    metadata: Mapping[str, object]
```

Metadata may contain:

- exit code;
- execution duration;
- output artifact names.

It must not contain giant logs. Logs belong in artifact files.

---

## `ValidationContext`

Provide per-run paths without hard-coding output behavior into validators:

```python
@dataclass(frozen=True)
class ValidationContext:
    run_dir: Path
```

Add fields only if actually needed.

---

## `CircuitValidator`

```python
class CircuitValidator(Protocol):
    @property
    def name(self) -> str:
        ...

    def validate(
        self,
        circuit: GeneratedCircuit,
        context: ValidationContext,
    ) -> ValidationResult:
        ...
```

---

## Semantics warning

Document this clearly in code/docstrings:

```text
A successful ngspice execution does not, by itself, prove that the generated
circuit satisfies the user's requested electrical behavior.
```

The prototype initially validates simulator acceptance/execution.

Functional requirement checking may be added later as a separate validator.

---

## Tests

Cover:

- status serialization;
- issue serialization;
- result construction;
- validator protocol/fake validator if needed;
- metadata remains JSON-serializable.

---

## Acceptance criteria

- Pipeline can execute multiple validators in order.
- Validation results are structured and persistable.
- No validator implementation is imported by core generation code.
