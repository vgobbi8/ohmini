from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Mapping, Protocol, runtime_checkable


@dataclass(slots=True, frozen=True)
class ModelRequest:
    prompt: str
    system_prompt: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.prompt or not self.prompt.strip():
            raise ValueError("ModelRequest.prompt must not be blank")


@dataclass(slots=True, frozen=True)
class ModelUsage:
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_tokens: int | None = None
    cost: float | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "total_tokens": self.total_tokens,
            "cost": self.cost,
        }


@dataclass(slots=True, frozen=True)
class ModelResponse:
    content: str
    usage: ModelUsage | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {"content": self.content, "metadata": dict(self.metadata)}
        if self.usage is not None:
            payload["usage"] = self.usage.to_dict()
        return payload


@runtime_checkable
class ModelBackend(Protocol):
    def invoke(self, request: ModelRequest) -> ModelResponse: ...


class FakeModelBackend:
    def __init__(
        self,
        response: str | ModelResponse | Callable[[ModelRequest], str | ModelResponse],
    ) -> None:
        self._response = response
        self.requests: list[ModelRequest] = []

    def invoke(self, request: ModelRequest) -> ModelResponse:
        self.requests.append(request)
        response = self._response(request) if callable(self._response) else self._response
        if isinstance(response, ModelResponse):
            return response
        return ModelResponse(content=response, metadata={"fake_backend": True})
