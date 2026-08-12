# Spec 10 — Circuit Pipeline Orchestration

## Goal

Create the smallest orchestration object that composes:

```text
CircuitGenerator -> CircuitValidator(s) -> PipelineResult
```

Do not introduce LangGraph.

---

## Pipeline inputs

The pipeline receives:

```text
CircuitGenerationRequest
```

Dependencies are injected:

```python
class CircuitPipeline:
    def __init__(
        self,
        *,
        generator: CircuitGenerator,
        validators: Sequence[CircuitValidator],
        run_artifacts: RunArtifactStore,
    ):
        ...
```

If artifact storage is implemented in Spec 12 instead, temporarily inject a small run-directory provider and adapt later.

---

## Execution sequence

1. allocate a unique run;
2. persist/snapshot the incoming requirement;
3. invoke the generator;
4. persist raw/normalized generation artifacts;
5. execute validators in configured order;
6. persist each validation result;
7. build a final pipeline result;
8. persist final report;
9. return the result to the CLI.

---

## Fail-fast policy

For v1:

- generation failure stops validation;
- a validator `failed` result does **not** automatically prevent later validators unless execution would be meaningless;
- a validator `error` should be recorded and the pipeline may continue only if later validators are independent;
- no automatic repair occurs.

Keep policy explicit and testable.

---

## `PipelineResult`

Suggested shape:

```python
@dataclass(frozen=True)
class PipelineResult:
    run_id: str
    run_dir: Path
    generated_circuit: GeneratedCircuit | None
    validation_results: tuple[ValidationResult, ...]
    status: str
```

Pipeline-level statuses:

```text
passed
failed
error
```

Initial aggregation:

- `error` if generation fails or required infrastructure prevents meaningful completion;
- `failed` if at least one validator returns `failed`;
- `passed` if generation succeeds and all required validators pass;
- define behavior for `skipped` explicitly.

Do not call a run `passed` if all validators were skipped.

---

## No retry/repair loop

Do not implement:

```text
generate -> validate -> repair -> validate
```

Yet.

Leave the code easy to wrap/replace with LangGraph later.

Do not add `attempts` state until repair is implemented.

---

## Tests

Use:

- fake generator;
- fake validators;
- temporary run directories.

Cover:

- successful run;
- generation failure;
- validator failure;
- validator infrastructure error;
- multiple validators;
- ordering;
- final status aggregation;
- artifacts invoked at the expected boundaries.

---

## Acceptance criteria

- Pipeline has no provider-specific logic.
- Pipeline has no ngspice subprocess code.
- Pipeline does not read environment variables.
- Pipeline has no LangGraph dependency.
- Adding `SkidlGenerator` later does not change pipeline code.
