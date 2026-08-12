# Spec 05 — API Model Backend Using LangChain Integrations

## Goal

Add an API-key/provider-based model execution path without changing the `ModelBackend` contract or circuit-generation code.

Use LangChain as an infrastructure integration layer, not as Ohmni's core architecture.

Initial providers:

```text
openai
anthropic
```

---

## Boundary rule

This file is the architectural rule:

```text
Ohmni core
    ↓
ModelBackend
    ↓
LangChainApiModelBackend
    ↓
LangChain provider integration
```

Do **not** expose these outside the backend module:

- `BaseChatModel`;
- `AIMessage`;
- `HumanMessage`;
- `SystemMessage`;
- provider-specific LangChain classes.

Generators must receive Ohmni `ModelResponse`, not LangChain messages.

---

## Dependencies

Use current LangChain v1-style provider integrations.

Prefer:

```text
langchain-core
langchain-openai
langchain-anthropic
```

Use lazy imports/provider extras if that keeps the base installation smaller.

Do not add LangGraph.

If optional dependencies are used, provide a clear error such as:

```text
Provider 'anthropic' requires the anthropic model extra/dependency.
```

Do not fail application startup for an unselected provider's missing package.

---

## Provider factory

Implement a small internal factory.

Conceptually:

```python
def _create_chat_model(provider: str, model: str):
    if provider == "openai":
        return ChatOpenAI(model=model)
    if provider == "anthropic":
        return ChatAnthropic(model=model)
    raise ModelConfigurationError(...)
```

Provider-native integrations should read their standard environment variables:

```text
OPENAI_API_KEY
ANTHROPIC_API_KEY
```

Do not pass secrets through Ohmni configuration snapshots.

---

## Request mapping

Map:

```python
ModelRequest(
    system_prompt="...",
    prompt="..."
)
```

to LangChain messages:

```text
SystemMessage, when present
HumanMessage
```

Invoke synchronously for v1.

---

## Response mapping

Map the provider result into:

```python
ModelResponse
```

`content` must be a plain string usable by the generator.

If a provider returns structured/multipart content, normalize text parts deterministically.

If no text can be extracted, raise `ModelOutputError`.

Capture available usage metadata without assuming every provider exposes identical fields.

Unknown metrics remain `None`.

Metadata must be sanitized and kept small.

---

## Error mapping

Translate provider/framework failures into Ohmni errors:

- missing credential -> `ModelConfigurationError`;
- timeout -> `ModelTimeoutError`;
- authentication/provider request failure -> `ModelInvocationError`;
- unusable response -> `ModelOutputError`.

Keep the original exception chained as the cause when useful.

Do not expose raw request headers or secrets.

---

## Tests

No real network calls.

Patch/fake the LangChain model object and cover:

- OpenAI factory selection;
- Anthropic factory selection;
- system/user message mapping;
- text response mapping;
- usage metadata mapping;
- missing credential behavior where practical;
- unsupported API provider;
- provider exception translation;
- multipart content normalization.

---

## Acceptance criteria

These two configurations can use the same generator:

```bash
OHMNI_MODEL_BACKEND=harness
OHMNI_MODEL_PROVIDER=codex
```

and:

```bash
OHMNI_MODEL_BACKEND=api
OHMNI_MODEL_PROVIDER=openai
```

No generator code changes are permitted between them.

LangChain types must not appear in core/generation/validation contracts.
