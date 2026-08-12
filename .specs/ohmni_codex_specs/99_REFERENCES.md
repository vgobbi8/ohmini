# Implementation References

These references were checked while preparing the specs on 2026-08-10.

They are implementation references, not a bibliography for the TCC itself.

## Coding-agent harness

- Repository: https://github.com/twaldin/harness
- Specification: https://github.com/twaldin/harness/blob/main/SPEC.md

At the time checked, the project described a unified Python/TypeScript interface for invoking multiple coding-agent CLIs and used a `RunSpec` / `RunResult` contract. Verify the exact current commit and license again when vendoring.

## Codex CLI

- Repository: https://github.com/openai/codex
- Documentation: https://developers.openai.com/codex/

The official Codex repository documents local CLI usage and ChatGPT-plan authentication. Verify currently supported non-interactive behavior through the official docs when debugging an adapter.

## OpenCode

- CLI: https://opencode.ai/docs/cli/
- Server: https://opencode.ai/docs/server/
- SDK: https://opencode.ai/docs/sdk/

The CLI documentation includes non-interactive `opencode run` behavior and model selection.

## LangChain

- Chat integrations: https://docs.langchain.com/oss/python/integrations/chat
- Implementing integrations: https://docs.langchain.com/oss/python/contributing/implement-langchain

LangChain chat integrations are infrastructure only in this architecture. Ohmni's public model contract remains its own `ModelBackend`.
