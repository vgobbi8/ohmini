# Spec 01 — Architecture Refactor

## Goal

Prepare the existing model infrastructure so both CLI-agent models and API models converge on LangChain `BaseChatModel` **without leaking LangChain into Ohmni application/core code**.

## Inspect first

Find the existing equivalents of:

```text
ModelBackend
ModelRequest
ModelResponse
ModelUsage
HarnessModelBackend
LangChainApiModelBackend
model backend factory/composition root
```

Do not duplicate these concepts under new names. Refactor in place.

## Stable boundary

The Ohmni contract remains authoritative:

```python
class ModelBackend(Protocol):
    def invoke(self, request: ModelRequest) -> ModelResponse:
        ...
```

`CircuitGenerator` and the rest of the application continue to use this interface.

Do not change the direct-SPICE generator to accept `BaseChatModel`.

Do not make LangChain message types part of `ModelRequest`, `ModelResponse`, `GeneratedCircuit`, pipeline contracts, or validator contracts.

## Infrastructure boundary

Inside model infrastructure, standardize around:

```python
from langchain_core.language_models.chat_models import BaseChatModel
```

The infrastructure should conceptually contain:

```text
BaseChatModel
├── HarnessChatModel
├── ChatGoogleGenerativeAI
├── ChatOpenAI
└── ChatAnthropic
```

plus:

```text
LangChainModelBackend
    wraps BaseChatModel
```

## Generalize API-only naming

If the current code has `LangChainApiModelBackend` and its responsibility is just converting Ohmni requests to/from a `BaseChatModel`, rename/generalize it to `LangChainModelBackend`.

Preserve temporary aliases if needed to avoid unnecessary breakage.

## Avoid redundant layers

Preferred:

```text
HarnessModelBackend
    ↓
LangChainModelBackend behavior
    ↓
HarnessChatModel
```

Do not duplicate message conversion and usage conversion logic between `HarnessModelBackend` and `LangChainModelBackend`.

Composition is preferred over inheritance if subclassing creates awkward Pydantic/type interactions.

## Dependency direction

Allowed:

```text
generation -> ModelBackend
infrastructure backends -> model core contracts
HarnessChatModel -> langchain-core + vendored harness
provider factory -> provider integration packages
```

Forbidden:

```text
generation -> HarnessChatModel
generation -> BaseChatModel
core model contracts -> langchain-core
validation -> langchain-core
```

## Acceptance criteria

- `ModelBackend` remains stable.
- `BaseChatModel` is visible only in model infrastructure/integration modules.
- One reusable Ohmni <-> LangChain translation path exists.
- Direct-SPICE generator has no provider/backend branches.
- No LangGraph dependency is added.
