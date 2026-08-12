# Ohmni — LangChain-Compatible Harness Slice

## Objective

Refactor the model infrastructure so that coding-agent CLI execution is represented as a real LangChain `BaseChatModel` **inside the infrastructure layer**, while Ohmni itself continues to depend on its own stable `ModelBackend` abstraction.

Target architecture:

```text
APPLICATION / CORE

CircuitGenerator
      ↓
ModelBackend
──────────────────────────────────────────── stable Ohmni boundary

INFRASTRUCTURE

              BaseChatModel
             /             \
HarnessChatModel          ChatGoogleGenerativeAI
      ↓                   ChatOpenAI
vendored harness          ChatAnthropic
      ↓
Codex / Claude Code / OpenCode / ...
```

Then:

```text
HarnessModelBackend
        ↓
HarnessChatModel : BaseChatModel
        ↓
vendored harness
```

and:

```text
LangChainModelBackend
        ↓
BaseChatModel
        ↓
ChatGoogleGenerativeAI / ChatOpenAI / ChatAnthropic / ...
```

The key rule is:

> `BaseChatModel` is the common infrastructure model abstraction, but `ModelBackend` remains the application-facing Ohmni abstraction.

This keeps Ohmni independent from LangChain while making every infrastructure model directly usable later by LangChain/LangGraph.

## Scope

Implement only:

1. `HarnessChatModel(BaseChatModel)`;
2. robust LangChain-message -> harness prompt/instructions translation;
3. harness `RunResult` -> `AIMessage`/`ChatResult` translation;
4. a thin `HarnessModelBackend` that uses the chat model;
5. a generalized `LangChainModelBackend` that can wrap any `BaseChatModel`;
6. Gemini API provider support through `ChatGoogleGenerativeAI`;
7. composition-root changes;
8. tests;
9. compatibility with the existing direct-SPICE generator.

Do **not** implement LangGraph, agents, tools, streaming, SKiDL, RAG, repair loops, frontend, database, or model-memory behavior.

## External contracts

Current LangChain documentation states that custom chat models subclass `BaseChatModel`; required implementation points are `_generate` and `_llm_type`, with `_identifying_params` optional. Inspect the installed version and adapt exact signatures rather than copying old tutorials.

The current `twaldin/harness` spec exposes a common `RunSpec`/`RunResult` contract. Its synchronous `run()` is blocking, and streaming callbacks are currently not part of the contract. Do not invent fake streaming.

## Execution order

Apply these specs in order:

1. `01_ARCHITECTURE_REFACTOR.md`
2. `02_HARNESS_CHAT_MODEL.md`
3. `03_LANGCHAIN_MODEL_BACKEND.md`
4. `04_HARNESS_MODEL_BACKEND.md`
5. `05_GEMINI_API_PROVIDER.md`
6. `06_COMPOSITION_AND_CONFIGURATION.md`
7. `07_TESTS.md`
8. `08_ACCEPTANCE_AND_MIGRATION.md`

`99_REFERENCES.md` is informational.

## Codex protocol

For each spec:

1. inspect the repository before editing;
2. locate the abstractions created by the previous Ohmni specs;
3. state a short plan;
4. implement only this slice;
5. preserve working direct-SPICE behavior;
6. add/modify tests;
7. run the smallest relevant test group;
8. run project lint/type checks already configured;
9. report changed files, tests, limitations, and any spec deviation.

Do not automatically continue to the next spec.
