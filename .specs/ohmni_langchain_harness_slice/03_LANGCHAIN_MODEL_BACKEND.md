# Spec 03 — Generalized `LangChainModelBackend`

## Goal

Create one thin Ohmni adapter that can wrap **any** LangChain `BaseChatModel`, including:

```text
HarnessChatModel
ChatGoogleGenerativeAI
ChatOpenAI
ChatAnthropic
future BaseChatModel integrations
```

This is the bridge between infrastructure and Ohmni core.

## Rename/generalize if necessary

If the current code contains `LangChainApiModelBackend` and it only converts Ohmni requests to/from a `BaseChatModel`, rename/generalize it to `LangChainModelBackend`.

Preserve imports/aliases temporarily if needed.

## Constructor

Conceptually:

```python
class LangChainModelBackend(ModelBackend):
    def __init__(
        self,
        *,
        chat_model: BaseChatModel,
        backend_name: str,
        provider_name: str,
        model_name: str,
    ):
        ...
```

Explicit metadata is preferred over introspecting provider-private fields.

## Request conversion

Convert:

```python
ModelRequest(system_prompt=..., prompt=...)
```

into:

```text
SystemMessage(system_prompt)  # if present
HumanMessage(prompt)
```

No provider branching. No harness branching.

## Invocation

Call:

```python
chat_model.invoke(messages)
```

Validate that a usable `AIMessage`/chat result is returned.

## Response text normalization

`AIMessage.content` may be string or content blocks.

Implement one conservative text extractor:

1. string -> use directly;
2. list -> join textual blocks in order;
3. non-text-only -> fail clearly;
4. do not stringify arbitrary dicts into model text.

This path is shared by API and harness-backed models.

## Usage mapping

Extract LangChain-standard usage metadata when available and map into Ohmni `ModelUsage`.

Unknown metrics remain `None`. Never estimate.

Map cost/duration from safe response metadata if present.

## Metadata

Persist only safe metadata such as response id, finish reason, harness identity, duration, or provider diagnostics.

Never include API keys, auth headers, environment dumps, or credential paths.

## Error conversion

Convert infrastructure/provider/LangChain failures into Ohmni-owned errors:

```text
ModelConfigurationError
ModelInvocationError
ModelTimeoutError
ModelOutputError
```

Preserve exception chaining.

## Tests

Use fake `BaseChatModel` implementations or LangChain test fakes.

Cover:

- request -> messages;
- string response;
- text-block response;
- unusable response;
- usage mapping;
- metadata sanitation;
- exception mapping;
- absence of provider-specific branches.

## Acceptance criteria

All of these use the same adapter:

```python
LangChainModelBackend(chat_model=HarnessChatModel(...), ...)
LangChainModelBackend(chat_model=ChatGoogleGenerativeAI(...), ...)
LangChainModelBackend(chat_model=ChatOpenAI(...), ...)
```

The direct-SPICE generator sees only `ModelBackend`.
