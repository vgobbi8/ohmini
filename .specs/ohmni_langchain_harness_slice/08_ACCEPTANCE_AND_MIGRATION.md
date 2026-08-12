# Spec 08 — Acceptance, Migration, and Stop Condition

## Goal

Complete this refactor cleanly and stop before expanding scope.

## Migration

Old conceptual shape:

```text
HarnessModelBackend -> vendored harness
LangChainApiModelBackend -> BaseChatModel
```

New shape:

```text
HarnessChatModel : BaseChatModel -> vendored harness

LangChainModelBackend -> BaseChatModel
     ↑
     ├── HarnessChatModel
     ├── ChatGoogleGenerativeAI
     ├── ChatOpenAI
     └── ChatAnthropic
```

Optional semantic convenience:

```text
HarnessModelBackend -> LangChainModelBackend(HarnessChatModel)
```

## Remove obsolete duplication

After tests pass, remove redundant direct harness -> Ohmni response conversion, duplicate LangChain message mapping, API-only naming that is no longer accurate, and provider branches inside generic adapters.

Preserve compatibility aliases temporarily if existing imports need them.

## README note

Add a short architecture section explaining:

```text
Ohmni application -> ModelBackend
Infrastructure -> BaseChatModel
Harness CLI agents -> HarnessChatModel
API providers -> native LangChain chat models
```

Explain briefly that the two boundaries keep Ohmni framework-independent while retaining LangChain/LangGraph interoperability.

## Manual acceptance A — Gemini

Configure:

```bash
OHMNI_MODEL_BACKEND=api
OHMNI_MODEL_PROVIDER=google
OHMNI_MODEL=<current-working-gemini-model>
GOOGLE_API_KEY=<local-secret>
```

Run the existing simple RC-filter generation command.

Expected:

```text
ChatGoogleGenerativeAI
 -> LangChainModelBackend
 -> DirectSpiceGenerator
 -> ngspice
```

No secret stored.

## Manual acceptance B — Codex

Configure:

```bash
OHMNI_MODEL_BACKEND=harness
OHMNI_MODEL_PROVIDER=codex
OHMNI_MODEL=<current-working-codex-model>
```

Use local Codex auth and run the exact same RC-filter requirement.

Expected:

```text
HarnessChatModel
 -> vendored harness
 -> Codex CLI
 -> AIMessage
 -> LangChainModelBackend/HarnessModelBackend
 -> DirectSpiceGenerator
 -> ngspice
```

Agent workspace must be isolated.

## Direct LangChain acceptance

Also prove:

```python
HarnessChatModel(...).invoke([
    SystemMessage(content="Return concise text."),
    HumanMessage(content="Return exactly hello."),
])
```

returns `AIMessage`.

## Future LangGraph readiness

Do **not** add LangGraph.

This slice is ready if a future graph could accept either `HarnessChatModel` or `ChatGoogleGenerativeAI` as `BaseChatModel` implementations without redesigning them.

## Final checklist

- [ ] `ModelBackend` remains application/core boundary.
- [ ] `BaseChatModel` is infrastructure boundary.
- [ ] `HarnessChatModel` subclasses `BaseChatModel`.
- [ ] Harness workspaces are isolated.
- [ ] Harness metadata maps into LangChain messages safely.
- [ ] `LangChainModelBackend` wraps any chat model.
- [ ] Gemini uses `ChatGoogleGenerativeAI`.
- [ ] Google credentials remain environment-only.
- [ ] Direct-SPICE has no provider logic.
- [ ] Tests consume no real quota by default.
- [ ] No LangGraph/RAG/SKiDL/repair code was added.

## Stop condition

Once this passes, return to the TCC pipeline:

```text
requirement -> model -> direct SPICE -> ngspice -> report
```

Do not expand the model layer again unless a real experiment requires it.
