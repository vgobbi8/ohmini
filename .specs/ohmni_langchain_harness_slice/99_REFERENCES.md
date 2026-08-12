# References Used for This Slice

Checked on 2026-08-10. These are engineering references for Codex, not the TCC bibliography.

## LangChain custom chat models

Official integration guidance:

https://docs.langchain.com/oss/python/contributing/implement-langchain

BaseChatModel reference:

https://reference.langchain.com/python/langchain-core/language_models/chat_models/BaseChatModel

Current source:

https://github.com/langchain-ai/langchain/blob/master/libs/core/langchain_core/language_models/chat_models.py

Current contract summary:

```text
_generate: required
_llm_type: required
_identifying_params: optional
_stream: optional
_agenerate: optional
_astream: optional
```

Always verify installed signatures.

## Google Gemini LangChain integration

https://docs.langchain.com/oss/python/integrations/chat/google_generative_ai

Package:

```text
langchain-google-genai
```

Class:

```text
ChatGoogleGenerativeAI
```

Current docs describe Gemini Developer API and Vertex AI support, `GOOGLE_API_KEY` with `GEMINI_API_KEY` fallback, and explicit `vertexai` selection.

## Coding-agent harness

Repository:

https://github.com/twaldin/harness

Specification:

https://github.com/twaldin/harness/blob/main/SPEC.md

Current `RunSpec` includes harness, prompt, workdir, model, instructions, timeoutSeconds, env, and modelNoResolve.

Current run results expose exit status, duration, stdout/stderr, timeout state, optional cost/tokens, and parsed raw payload.

Current behavior notes:

- `run()` is synchronous/blocking;
- Python also exposes async `run_async`;
- non-zero exits/timeouts are reflected in result objects;
- registry/prerequisite problems can raise `HarnessError`;
- streaming callbacks are currently not provided;
- user secrets are expected from the user's environment, not adapter-owned storage.

Pin and vendor an exact upstream commit before relying on these details.
