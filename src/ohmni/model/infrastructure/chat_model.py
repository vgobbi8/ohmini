from __future__ import annotations

from pathlib import Path
from typing import Any, Sequence

from pydantic import ConfigDict, Field
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.outputs import ChatGeneration, ChatResult

from ohmni._vendor.agent_harness import RunSpec, RunResult, run_spec
from ohmni.model.errors import ModelConfigurationError, ModelInvocationError, ModelOutputError, ModelTimeoutError
from ohmni.model.infrastructure.translation import (
    content_to_text,
    extract_assistant_text,
    render_messages_for_harness,
    sanitize_metadata,
    usage_from_mapping,
)


SUPPORTED_HARNESS_PROVIDERS = {"agy", "codex", "claude_code", "opencode"}


class HarnessChatModel(BaseChatModel):
    provider: str
    model: str
    timeout_seconds: float = Field(default=60.0)
    workspace_dir: Path | None = Field(default=None, exclude=True)
    command: tuple[str, ...] | None = Field(default=None, exclude=True)

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @property
    def _llm_type(self) -> str:
        return "ohmni-harness"

    @property
    def _identifying_params(self) -> dict[str, Any]:
        return {
            "provider": self.provider,
            "model": self.model,
            "timeout_seconds": self.timeout_seconds,
        }

    def _build_command(self, prompt: str) -> list[str]:
        if self.command is not None:
            return list(self.command)
        if self.provider == "agy":
            return ["agy", "--model", self.model, "--print", prompt]
        return [self.provider, "run", self.model, prompt]

    def _generate(
        self,
        messages: list[BaseMessage],
        stop: list[str] | None = None,
        run_manager: CallbackManagerForLLMRun | None = None,
        **kwargs: Any,
    ) -> ChatResult:
        if stop:
            raise NotImplementedError("Stop sequences are not supported by HarnessChatModel")
        if kwargs:
            unsupported = sorted(kwargs)
            raise NotImplementedError(f"Unsupported chat-model kwargs for harness execution: {unsupported}")
        if self.provider not in SUPPORTED_HARNESS_PROVIDERS:
            raise ModelConfigurationError(
                f"Unsupported harness provider: {self.provider!r}",
                backend="harness",
                provider=self.provider,
                model=self.model,
            )

        instructions, prompt = render_messages_for_harness(messages)
        try:
            result = run_spec(
                RunSpec(
                    provider=self.provider,
                    model=self.model,
                    prompt=prompt,
                    instructions=instructions,
                    timeout_seconds=self.timeout_seconds,
                    workspace_dir=self.workspace_dir,
                    command=tuple(self._build_command(prompt)),
                )
            )
        except NotImplementedError:
            raise
        except FileNotFoundError as exc:
            raise ModelConfigurationError(
                f"Harness executable not found for provider {self.provider!r}",
                backend="harness",
                provider=self.provider,
                model=self.model,
            ) from exc
        except Exception as exc:
            raise ModelInvocationError(
                "Harness backend failed to launch",
                backend="harness",
                provider=self.provider,
                model=self.model,
            ) from exc

        if result.timed_out:
            raise ModelTimeoutError(
                "Harness backend timed out",
                backend="harness",
                provider=self.provider,
                model=self.model,
            )
        if result.returncode != 0:
            raise ModelInvocationError(
                "Harness backend exited with a non-zero status",
                backend="harness",
                provider=self.provider,
                model=self.model,
                exit_code=result.returncode,
            )

        assistant_text = extract_assistant_text(result.raw) or (result.stdout or "").strip()
        if not assistant_text.strip():
            raise ModelOutputError(
                "Harness backend returned no extractable assistant output",
                backend="harness",
                provider=self.provider,
                model=self.model,
            )

        usage = usage_from_mapping(getattr(result, "usage", None))
        response_metadata = sanitize_metadata(
            {
                "provider": self.provider,
                "model": self.model,
                "workspace": str(result.workspace),
                "returncode": result.returncode,
                "stderr": result.stderr,
                "duration_seconds": result.duration_seconds,
                "raw": result.raw,
            }
        )
        ai_message = AIMessage(
            content=assistant_text,
            usage_metadata=usage,
            response_metadata=response_metadata,
        )
        return ChatResult(
            generations=[ChatGeneration(message=ai_message)],
            llm_output=response_metadata,
        )
