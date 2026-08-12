from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from ohmni.model.contracts import ModelRequest, ModelResponse, ModelUsage
from ohmni.model.errors import ModelConfigurationError, ModelInvocationError, ModelOutputError, ModelTimeoutError
from ohmni.model.infrastructure.translation import content_to_text, sanitize_metadata, usage_from_mapping


def _request_to_messages(request: ModelRequest) -> list[Any]:
    messages: list[Any] = []
    if request.system_prompt:
        messages.append(SystemMessage(content=request.system_prompt))
    messages.append(HumanMessage(content=request.prompt))
    return messages


def _response_text(response: AIMessage) -> str:
    content = response.content
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        pieces: list[str] = []
        for block in content:
            if isinstance(block, str):
                pieces.append(block)
            elif isinstance(block, dict):
                if str(block.get("type", "")).lower() in {"text", "plain_text", "text_block"} or "text" in block:
                    pieces.append(str(block.get("text", block.get("content", ""))))
                else:
                    raise ModelOutputError("Chat model returned non-text content blocks that cannot be normalized")
            elif hasattr(block, "text"):
                pieces.append(str(getattr(block, "text")))
            else:
                raise ModelOutputError("Chat model returned non-text content blocks that cannot be normalized")
        text = "".join(pieces)
        if not text.strip():
            raise ModelOutputError("Chat model returned an empty textual response")
        return text
    return content_to_text(content)


def _model_usage_from_ai_message(response: AIMessage) -> ModelUsage | None:
    usage = response.usage_metadata or usage_from_mapping(getattr(response, "response_metadata", None))
    if usage is None:
        return None
    return ModelUsage(
        prompt_tokens=usage.get("input_tokens"),
        completion_tokens=usage.get("output_tokens"),
        total_tokens=usage.get("total_tokens"),
        cost=None,
    )


@dataclass(slots=True)
class LangChainModelBackend:
    chat_model: BaseChatModel
    backend_name: str = "langchain"
    provider: str | None = None
    model_name: str | None = None

    def invoke(self, request: ModelRequest) -> ModelResponse:
        messages = _request_to_messages(request)
        try:
            response = self.chat_model.invoke(messages)
        except TimeoutError as exc:
            raise ModelTimeoutError(
                "LangChain chat model timed out",
                backend=self.backend_name,
                provider=self.provider,
                model=self.model_name,
            ) from exc
        except ModelOutputError:
            raise
        except NotImplementedError as exc:
            raise ModelConfigurationError(
                str(exc),
                backend=self.backend_name,
                provider=self.provider,
                model=self.model_name,
            ) from exc
        except Exception as exc:
            raise ModelInvocationError(
                "LangChain chat model invocation failed",
                backend=self.backend_name,
                provider=self.provider,
                model=self.model_name,
            ) from exc

        if not isinstance(response, AIMessage):
            raise ModelOutputError(
                f"Expected AIMessage from chat model, got {type(response).__name__}",
                backend=self.backend_name,
                provider=self.provider,
                model=self.model_name,
            )

        content = _response_text(response)
        usage = _model_usage_from_ai_message(response)
        metadata = sanitize_metadata(getattr(response, "response_metadata", {}))
        if isinstance(metadata, dict):
            metadata.setdefault("backend", self.backend_name)
            if self.provider is not None:
                metadata.setdefault("provider", self.provider)
            if self.model_name is not None:
                metadata.setdefault("model", self.model_name)
        return ModelResponse(content=content, usage=usage, metadata=metadata)
