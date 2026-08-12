# Spec 04 — Harness Model Backend

## Goal

Implement a `ModelBackend` adapter over the vendored coding-agent CLI harness so Ohmni can use subscription-authenticated or otherwise locally configured coding-agent CLIs without coupling generators to CLI details.

Initial providers:

```text
codex
claude-code
opencode
```

The backend must be isolated behind the `ModelBackend` contract.

---

## Upstream basis

Vendor the Python implementation from:

```text
https://github.com/twaldin/harness
```

At the time this spec was prepared, upstream exposed a common `RunSpec` → `RunResult` interface for multiple coding-agent CLIs.

Do not depend on upstream `main` at runtime.

The exact vendoring procedure and attribution requirements are in Spec 14.

---

## Security boundary

This is critical.

Coding-agent CLIs can have file/tool access. Ohmni only needs them as model execution mechanisms.

**Never run a harness-backed model with the repository root as its working directory.**

For every model invocation:

1. create an isolated per-run/per-invocation workspace;
2. place it under the configured output/run area or system temporary directory;
3. do not copy source code into it by default;
4. pass only the prompt/instructions required for generation;
5. do not expose unrelated project files;
6. clean up only if doing so does not remove artifacts required for reproducibility.

The adapter may inherit the user's CLI authentication/session environment, but must not dump the environment into logs or artifacts.

---

## Backend construction

Suggested constructor:

```python
class HarnessModelBackend:
    def __init__(
        self,
        *,
        provider: str,
        model: str,
        timeout_seconds: int,
        workspace_factory: ModelWorkspaceFactory,
    ):
        ...
```

The backend is fully configured after construction.

`invoke()` should not receive provider/model repeatedly.

---

## Mapping to the harness

For each `ModelRequest`:

- `harness` = configured provider;
- `model` = configured model;
- `prompt` = user prompt;
- `instructions` = system prompt when present;
- `workdir` = isolated workspace;
- `timeoutSeconds` = configured timeout.

Do not pass arbitrary Ohmni environment values through `RunSpec.env`.

Only add extra environment variables when an adapter demonstrably requires them.

---

## Output normalization

A harness `RunResult` may contain raw stdout and adapter-specific parsed data.

The adapter must produce one `ModelResponse`.

Use the harness's parsed result when it provides a clean assistant result.

Do not blindly return JSON envelopes or JSONL event streams as `content`.

If the vendored harness already exposes a normalized result text, use it.

Otherwise isolate provider-specific extraction inside this backend, not in circuit generators.

The final `content` must be the assistant's textual answer.

---

## Usage mapping

Map available harness metrics:

```text
tokensIn  -> ModelUsage.input_tokens
tokensOut -> ModelUsage.output_tokens
costUsd   -> ModelUsage.cost_usd
durationSeconds -> ModelUsage.duration_seconds
```

If a CLI cannot report a metric, leave it `None`.

Do not estimate costs or token counts.

---

## Failure behavior

The upstream harness reports subprocess failure/timeout in `RunResult`.

Convert:

- timeout -> `ModelTimeoutError`;
- non-zero exit -> `ModelInvocationError`;
- missing executable/prerequisite -> `ModelConfigurationError` or `ModelBackendError`, depending on where detected;
- empty/non-extractable assistant output -> `ModelOutputError`.

Include stderr excerpts only after removing obviously sensitive material.

Limit stored exception excerpts to a reasonable length.

The full raw stdout/stderr may be persisted as run artifacts only if sanitized and if they do not expose credentials.

---

## CLI availability checks

At backend construction or first use, verify the selected provider is supported by the vendored harness.

Do not require all three CLIs to be installed.

For example, a Codex-only machine must still work.

---

## Do not create provider-specific Ohmni backends

Do **not** create:

```text
CodexBackend
ClaudeCodeBackend
OpenCodeBackend
```

unless the harness proves incapable of providing a reliable common boundary.

The intended design is:

```text
HarnessModelBackend
    ↓
vendored harness
    ├── codex
    ├── claude-code
    └── opencode
```

---

## Tests

Unit tests must not invoke real CLIs.

Patch/fake the vendored harness `run()` call and cover:

- Codex mapping;
- Claude Code mapping;
- OpenCode mapping;
- system prompt -> instructions mapping;
- isolated workspace use;
- successful text extraction;
- usage mapping;
- timeout;
- non-zero exit;
- missing/empty result;
- unsupported provider.

Add one manually runnable integration test or script, disabled by default, for a locally authenticated Codex CLI.

It must never run in normal CI.

---

## Acceptance criteria

- `DirectSpiceGenerator` can later use this backend without importing harness types.
- Swapping `codex` to `opencode` is configuration, not generator code.
- Repository root is never the model workdir.
- Tests use no paid model calls.
- Provider-specific subprocess behavior remains inside the vendored harness/backend.
