# Spec 06 — Composition Root and Configuration

## Goal

Wire the converged infrastructure while preserving environment variables as the runtime configuration surface.

## Minimum configurations

Harness:

```bash
OHMNI_MODEL_BACKEND=harness
OHMNI_MODEL_PROVIDER=codex
OHMNI_MODEL=<explicit-model>
OHMNI_MODEL_TIMEOUT_SECONDS=300
```

Gemini API:

```bash
OHMNI_MODEL_BACKEND=api
OHMNI_MODEL_PROVIDER=google
OHMNI_MODEL=<explicit-model>
OHMNI_MODEL_TIMEOUT_SECONDS=300
GOOGLE_API_KEY=<secret>
```

## Allowed combinations

At minimum:

```text
harness / codex
harness / claude-code
harness / opencode
api / google
```

Keep already implemented `api/openai` and `api/anthropic` combinations.

Reject incompatible pairs clearly.

## Composition algorithm

Conceptually:

```text
backend=harness
    -> HarnessChatModel
    -> HarnessModelBackend / generic LangChain bridge

backend=api
    -> provider factory -> native BaseChatModel
    -> LangChainModelBackend
```

Then:

```text
ModelBackend -> DirectSpiceGenerator
```

## No environment access below composition

No `os.getenv()` inside:

- `HarnessChatModel`;
- `HarnessModelBackend`;
- `LangChainModelBackend`;
- `DirectSpiceGenerator`.

Provider SDKs may internally read standard credential env vars.

## `.env.example`

Update with:

```bash
# Model execution
OHMNI_MODEL_BACKEND=api
OHMNI_MODEL_PROVIDER=google
OHMNI_MODEL=
OHMNI_MODEL_TIMEOUT_SECONDS=300

# API credentials
GOOGLE_API_KEY=
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
```

Keep only credentials relevant to actually supported providers. Never include real values.

## Public config snapshot

For `api/google`, persist only safe values such as backend, provider, model, timeout.

Never persist `GOOGLE_API_KEY` or `GEMINI_API_KEY`.

## Tests

Cover:

- harness/codex composition;
- harness/opencode composition;
- api/google composition;
- existing providers;
- invalid pair;
- direct-SPICE receives a `ModelBackend` only;
- public config contains no secrets.

## Acceptance criteria

Changing Gemini API to Codex CLI is environment configuration only.
