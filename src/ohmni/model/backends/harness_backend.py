from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from ohmni._vendor.agent_harness import AVAILABLE_PROVIDERS
from ohmni.model.contracts import ModelRequest, ModelResponse
from ohmni.model.errors import ModelConfigurationError
from ohmni.model.infrastructure.chat_model import HarnessChatModel
from ohmni.model.infrastructure.langchain_backend import LangChainModelBackend


@dataclass(slots=True)
class HarnessModelBackend:
    provider: str
    model: str
    timeout_seconds: float
    workspace_dir: Path | None = None
    command: tuple[str, ...] | None = None
    _backend: LangChainModelBackend = field(init=False, repr=False)

    def __post_init__(self) -> None:
        if not self.provider.strip():
            raise ModelConfigurationError("Harness provider must not be blank", backend="harness", provider=self.provider, model=self.model)
        if not self.model.strip():
            raise ModelConfigurationError("Harness model must not be blank", backend="harness", provider=self.provider, model=self.model)
        if self.timeout_seconds <= 0:
            raise ModelConfigurationError("Harness timeout must be greater than zero", backend="harness", provider=self.provider, model=self.model)
        if self.provider not in AVAILABLE_PROVIDERS:
            raise ModelConfigurationError(
                f"Unsupported harness provider: {self.provider!r}",
                backend="harness",
                provider=self.provider,
                model=self.model,
            )
        chat_model = HarnessChatModel(
            provider=self.provider,
            model=self.model,
            timeout_seconds=self.timeout_seconds,
            workspace_dir=self.workspace_dir,
            command=self.command,
        )
        self._backend = LangChainModelBackend(
            chat_model=chat_model,
            backend_name="harness",
            provider=self.provider,
            model_name=self.model,
        )

    @property
    def chat_model(self) -> HarnessChatModel:
        return self._backend.chat_model  # type: ignore[return-value]

    def invoke(self, request: ModelRequest) -> ModelResponse:
        return self._backend.invoke(request)
