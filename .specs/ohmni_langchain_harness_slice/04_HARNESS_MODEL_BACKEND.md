# Spec 04 — Thin `HarnessModelBackend`

## Goal

Preserve the semantic Ohmni `harness` backend while removing duplicate model-call logic.

Target:

```text
HarnessModelBackend
      ↓
LangChainModelBackend
      ↓
HarnessChatModel
      ↓
vendored harness
```

## Why retain it

The configured backend value remains:

```text
OHMNI_MODEL_BACKEND=harness
```

`HarnessModelBackend` is useful as a composition convenience and place for harness-specific configuration validation.

It must not duplicate message conversion, `AIMessage` conversion, usage mapping, or generic exception mapping already implemented by `LangChainModelBackend`.

## Preferred implementation

Composition is preferred if clearer:

```python
class HarnessModelBackend(ModelBackend):
    def __init__(...):
        self._inner = LangChainModelBackend(
            chat_model=HarnessChatModel(...),
            backend_name="harness",
            provider_name=harness_name,
            model_name=model,
        )

    def invoke(self, request):
        return self._inner.invoke(request)
```

A thin subclass is acceptable if it does not create Pydantic/type friction.

## Validation

Validate:

- harness/provider non-blank;
- explicit model non-blank;
- timeout > 0;
- selected adapter exists in vendored harness registry.

Do not require every supported CLI to be installed.

## Workspace root

Inject the model workspace root. Prefer:

```text
out/runs/<run-id>/model/workspaces/<uuid>/
```

If run-id wiring is not available in this slice, use a controlled temporary root and keep the architecture ready for later wiring.

Never use repo root.

## Tests

Cover:

- creates/wraps `HarnessChatModel`;
- delegates through generic LangChain bridge;
- public provider/model identity;
- invalid provider;
- generator calls through `ModelBackend` without harness types.

## Acceptance criteria

A harness-backed generation travels through:

```text
DirectSpiceGenerator
 -> ModelBackend
 -> HarnessModelBackend
 -> LangChainModelBackend behavior
 -> HarnessChatModel
 -> harness
```

No `RunSpec` or LangChain type appears in `DirectSpiceGenerator`.
