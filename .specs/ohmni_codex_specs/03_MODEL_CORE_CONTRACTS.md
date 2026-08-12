# Spec 03 — Model Core Contracts

## Goal

Define the stable provider-neutral boundary used by circuit generators.

The core layer must not import LangChain, the vendored harness, OpenAI, Anthropic, Codex, OpenCode, Claude Code, or subprocess modules.

---

## Contracts

### `ModelRequest`

Keep v1 deliberately small:

```python
@dataclass(frozen=True)
class ModelRequest:
    prompt: str
    system_prompt: str | None = None
```

Validation:

- `prompt` must not be blank;
- `system_prompt` may be `None`.

Do not add chat history yet.

Do not add tool calling yet.

### `ModelUsage`

Represent usage data only when known:

```python
@dataclass(frozen=True)
class ModelUsage:
    input_tokens: int | None = None
    output_tokens: int | None = None
    cost_usd: float | None = None
    duration_seconds: float | None = None
```

Unknown values remain `None`.

Do not fabricate zeros.

### `ModelResponse`

```python
@dataclass(frozen=True)
class ModelResponse:
    content: str
    backend: str
    provider: str
    model: str
    usage: ModelUsage
    metadata: Mapping[str, object]
```

Rules:

- `content` is the normalized textual response consumed by generators;
- metadata is optional provider/backend diagnostic information;
- metadata must already be sanitized;
- metadata must never contain credentials.

### `ModelBackend`

Use a protocol/ABC appropriate to the existing project:

```python
class ModelBackend(Protocol):
    def invoke(self, request: ModelRequest) -> ModelResponse:
        ...
```

Keep v1 synchronous.

Do not add streaming.

Do not add async unless the current repository is already async and a sync API would create unnecessary friction.

---

## Errors

Define application-owned errors:

```text
ModelBackendError
ModelConfigurationError
ModelInvocationError
ModelTimeoutError
ModelOutputError
```

Provider-specific exceptions must not leak through the stable boundary unless preserved as `__cause__`.

Error messages should include useful public context:

- backend;
- provider;
- model;
- exit code when relevant.

Never include:

- API keys;
- entire environment;
- authentication tokens.

---

## Fake backend

Implement a tiny `FakeModelBackend` for tests.

It should:

- accept a predefined response or response callback;
- record requests it receives;
- return a normal `ModelResponse`;
- require no network;
- consume no paid model usage.

This is a first-class testing tool, not a throwaway mock.

---

## Tests

Cover:

- request validation;
- response construction;
- fake backend invocation;
- fake backend request recording;
- error inheritance.

---

## Acceptance criteria

- No third-party LLM framework imports in core contracts.
- Generators can use `ModelBackend` without knowing how it is implemented.
- Tests can execute the future pipeline with `FakeModelBackend`.
