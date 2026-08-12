# Spec 05 — Gemini API Provider Through Native LangChain Model

## Goal

Add Google Gemini as the API provider while proving the same `BaseChatModel` infrastructure path works for API and harness models.

Use:

```python
from langchain_google_genai import ChatGoogleGenerativeAI
```

Do not implement a custom Gemini HTTP client.

## Dependency

Add a current compatible `langchain-google-genai` dependency through the repository's dependency manager.

Do not pin an arbitrary old tutorial version; resolve compatibility with installed `langchain-core`.

## Environment

Support:

```bash
OHMNI_MODEL_BACKEND=api
OHMNI_MODEL_PROVIDER=google
OHMNI_MODEL=<explicit-gemini-model>
GOOGLE_API_KEY=<secret>
```

The current LangChain integration checks `GOOGLE_API_KEY` first and can use `GEMINI_API_KEY` as fallback.

For Ohmni docs/defaults, prefer `GOOGLE_API_KEY`.

Never copy secrets into public settings snapshots.

## Target Developer API

The Google integration supports Gemini Developer API and Vertex AI.

For this TCC slice, explicitly target the **Gemini Developer API using API-key authentication**.

Avoid accidental Vertex selection caused by unrelated environment settings.

The current integration exposes `vertexai=False`; inspect the installed package constructor before coding and use its supported equivalent.

## Provider factory

Conceptually:

```python
if backend == "api" and provider == "google":
    chat_model = ChatGoogleGenerativeAI(
        model=settings.model,
        vertexai=False,
    )
    return LangChainModelBackend(
        chat_model=chat_model,
        backend_name="api",
        provider_name="google",
        model_name=settings.model,
    )
```

Do not put Gemini-specific logic in `LangChainModelBackend`.

## Existing providers

If OpenAI/Anthropic support already exists, keep it and route each through its native LangChain `BaseChatModel` implementation plus `LangChainModelBackend`.

Google is mandatory for this slice. Do not spend time adding unrelated providers.

## Credentials

Fail clearly when Google API execution is actually selected without usable credentials.

Do not fail harness execution because Google credentials are absent.

Never print/store the key.

## Do not enable extra Gemini capabilities

Do not enable Google Search, URL context, code execution, tool calling, multimodal input, provider-native structured output, Vertex AI, or context caching.

This is a plain text model call for SPICE generation.

## Usage metadata

Allow `ChatGoogleGenerativeAI` to produce normal LangChain usage metadata. Let `LangChainModelBackend` map it.

Do not create Google-specific token accounting in generators.

## Tests

No real Google API calls.

Cover:

- `api/google` selects `ChatGoogleGenerativeAI`;
- configured model is passed;
- Developer API path selected explicitly when supported;
- Google key absent from public config;
- absent Google key does not break harness selection;
- generic LangChain bridge handles the response.

## Acceptance criteria

Direct-SPICE works unchanged with both:

```bash
OHMNI_MODEL_BACKEND=api
OHMNI_MODEL_PROVIDER=google
OHMNI_MODEL=<gemini-model>
GOOGLE_API_KEY=...
```

and:

```bash
OHMNI_MODEL_BACKEND=harness
OHMNI_MODEL_PROVIDER=codex
OHMNI_MODEL=<codex-model>
```

Only composition/configuration changes.
