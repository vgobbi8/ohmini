# Spec 02 — `HarnessChatModel(BaseChatModel)`

## Goal

Implement a LangChain-compatible chat model that executes a coding-agent CLI through the vendored `twaldin/harness` code.

It must be a genuine chat model usable through:

```python
model.invoke(messages)
```

and later by LangChain/LangGraph components accepting a `BaseChatModel`.

## Verify installed LangChain first

Before coding:

```bash
python -c "import langchain_core; print(langchain_core.__version__)"
```

Inspect the installed `BaseChatModel` signature/source if needed. Do not paste an old tutorial implementation.

For current LangChain, custom chat models require `_generate` and `_llm_type`; match the installed version's exact signatures.

## Suggested fields

Because LangChain models are Pydantic-based, define configuration using fields compatible with the installed `langchain-core`.

Conceptually:

```python
harness_name: str
model: str
timeout_seconds: int = 300
workspace_root: Path | None = None
```

Do not store API keys, arbitrary environment dumps, or credential state.

## `_llm_type`

Return a stable identifier such as:

```text
ohmni-harness
```

Do not put the model name in `_llm_type`.

## `_identifying_params`

Implement if practical with safe fields only:

```python
{
    "harness": self.harness_name,
    "model": self.model,
    "timeout_seconds": self.timeout_seconds,
}
```

Never expose credentials, environment variables, or auth state.

## Message conversion

Input is `list[BaseMessage]`.

### System messages

Collect system instructions in order and combine them into `RunSpec.instructions`.

Use a deterministic separator when multiple system messages exist.

### Human messages

Convert textual human-message content into the task prompt. Preserve order and role boundaries when multiple messages exist.

### AI messages

Initial Ohmni generation should not normally send prior AI messages, but support textual AI messages by folding them into the rendered prompt with explicit role markers.

### Unsupported messages/content

For `ToolMessage`, tool/function-call blocks, image/audio/file content, or other non-text content:

- do not silently discard;
- raise a clear `NotImplementedError` or application-owned unsupported-message error.

This slice is text-only.

## Prompt rendering

Do not blindly concatenate message text. Use deterministic role markers for non-system history, for example:

```text
[USER]
Design ...

[ASSISTANT]
Previous response ...

[USER]
Correction ...
```

System instructions should go to `RunSpec.instructions` and not be duplicated in the task prompt.

## Isolated workspace

Each invocation must use a fresh working directory.

Never use repository root, current source directory, or user home as the agent workdir.

Use something like:

```text
<workspace_root>/<uuid>/
```

The directory may be retained under run artifacts for reproducibility.

## Build `RunSpec`

Map:

```text
harness        <- harness_name
prompt         <- rendered non-system messages
instructions   <- rendered system messages, if any
workdir        <- isolated invocation workspace
model          <- explicit configured model
timeoutSeconds <- timeout_seconds
```

Do not rely on harness default model names.

Do not pass an `env` map unless a future requirement explicitly needs it. The child CLI may inherit the normal process environment so local authentication works, but never persist that environment.

## Invoke the vendored harness

Use the vendored Python harness API.

Implement synchronous `_generate` using its synchronous `run(spec)` path.

Do not add fake streaming. Do not override `_stream` unless the underlying harness later supports meaningful streaming.

Do not implement native async merely by blocking inside `async def`.

## Failure mapping

Handle:

- harness registry/prerequisite errors;
- `timedOut=True`;
- non-zero exit;
- empty/unextractable assistant output.

Raise clean infrastructure errors and preserve useful causes. Never include credential values.

## Assistant text extraction

`RunResult.stdout` is not universally the final assistant text.

Create one internal extractor:

```python
_extract_assistant_text(result: RunResult) -> str
```

Keep adapter-specific extraction inside this infrastructure class/module.

Current upstream examples include:

- Claude Code raw payload with a `result` field;
- Gemini raw payload with a `response` field;
- adapters that require stdout extraction;
- adapters where `raw` is `None`.

Prefer an upstream normalized helper if the exact vendored revision provides one.

Never return JSON/JSONL envelopes as assistant text.

## Return LangChain types

Return a `ChatResult` containing one `ChatGeneration` with an `AIMessage`.

Attach safe response metadata.

Where compatible with installed LangChain, populate standard usage metadata from known harness values:

```text
tokensIn  -> input_tokens
tokensOut -> output_tokens
```

Do not invent usage. Keep cost/duration in safe response metadata when useful.

## Stop sequences

The harness contract does not expose a generic stop-sequence field.

If `_generate(..., stop=...)` receives non-empty stop sequences, do not silently ignore them. Raise `NotImplementedError` unless the exact vendored revision has a generic reliable mechanism.

## Tools / structured output

Do not implement `bind_tools()`.

Do not claim native tool calling or native structured output.

## Tests

Patch the vendored harness invocation. Do not execute real CLIs.

Cover:

1. `_llm_type`;
2. safe `_identifying_params`;
3. system -> instructions;
4. human -> prompt;
5. message order/role preservation;
6. unsupported multimodal/tool messages;
7. isolated workspace;
8. exact `RunSpec` mapping;
9. Claude-style result extraction;
10. Gemini-style extraction if present;
11. stdout fallback extraction;
12. token usage mapping;
13. cost/duration metadata;
14. timeout;
15. non-zero exit;
16. empty result;
17. stop sequence rejected;
18. `model.invoke([...])` returns `AIMessage`.

## Acceptance criteria

This works independently of Ohmni's generator:

```python
model = HarnessChatModel(
    harness_name="codex",
    model="<configured-model>",
)
response = model.invoke("Return exactly: hello")
assert isinstance(response, AIMessage)
```

A real invocation is manual/optional and never runs in normal tests.
