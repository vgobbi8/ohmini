# Spec 07 — Tests

## Goal

Prove infrastructure interchangeability without consuming subscription/API quota during normal tests.

## Default-test rule

Normal tests must never call Google Gemini API, OpenAI, Anthropic, Codex CLI, Claude Code CLI, or OpenCode CLI.

Patch/fake external boundaries.

## `HarnessChatModel` tests

Mandatory:

```text
test_harness_chat_model_is_base_chat_model
test_harness_chat_model_llm_type
test_harness_chat_model_identifying_params_are_safe
test_system_message_maps_to_instructions
test_human_message_maps_to_prompt
test_message_order_is_preserved
test_unsupported_multimodal_message_fails
test_tool_message_fails
test_stop_sequences_are_not_silently_ignored
test_each_call_uses_isolated_workspace
test_timeout_is_failure
test_nonzero_exit_is_failure
test_empty_response_is_failure
test_claude_result_text_extraction
test_gemini_result_text_extraction_if_supported
test_stdout_result_text_extraction
test_usage_metadata_mapping
test_model_invoke_returns_ai_message
```

## `LangChainModelBackend` tests

Mandatory:

```text
test_model_request_maps_to_langchain_messages
test_string_ai_message_maps_to_model_response
test_text_blocks_map_to_model_response
test_usage_metadata_maps_to_model_usage
test_invalid_nontext_response_fails
test_provider_exception_maps_to_ohmni_error
test_backend_does_not_branch_for_harness_or_google
```

## `HarnessModelBackend` tests

Mandatory:

```text
test_harness_backend_wraps_harness_chat_model
test_harness_backend_uses_generic_langchain_bridge
test_harness_backend_exposes_public_identity
```

## Gemini factory tests

Mandatory:

```text
test_google_provider_creates_chat_google_generative_ai
test_google_provider_uses_configured_model
test_google_provider_targets_developer_api
test_google_secret_not_in_public_settings
test_missing_google_key_does_not_affect_harness_configuration
```

## Generator compatibility

Use the existing `DirectSpiceGenerator` with two fake model backends representing harness/codex and api/google. Return the same SPICE output and assert generator behavior is identical.

The generator must contain no backend/provider branch.

## Deterministic end-to-end

Where ngspice is locally available, test:

```text
Fake BaseChatModel
 -> LangChainModelBackend
 -> DirectSpiceGenerator
 -> NgSpiceValidator
```

and:

```text
Fake harness run
 -> HarnessChatModel
 -> HarnessModelBackend
 -> DirectSpiceGenerator
 -> NgSpiceValidator
```

No paid calls.

## Optional manual tests

Use explicit markers/opt-in env variables for real CLI/API integration. Never enable by default.

## Acceptance criteria

- default tests require no credentials;
- default tests consume no quota;
- harness model behaves as a LangChain chat model;
- Gemini and harness paths converge before generation.
