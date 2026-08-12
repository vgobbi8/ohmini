from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ohmni.model.contracts import ModelRequest, ModelResponse
from ohmni.model.infrastructure.langchain_backend import LangChainModelBackend as _LangChainModelBackend


@dataclass(slots=True)
class LangChainApiModelBackend:
    """Backward-compatible alias for the generalized LangChain backend."""

    chat_model: Any
    backend_name: str = "api"
    provider: str | None = None
    model_name: str | None = None

    def __post_init__(self) -> None:
        self._backend = _LangChainModelBackend(
            chat_model=self.chat_model,
            backend_name=self.backend_name,
            provider=self.provider,
            model_name=self.model_name,
        )

    def invoke(self, request: ModelRequest) -> ModelResponse:
        return self._backend.invoke(request)


LangChainModelBackend = _LangChainModelBackend
