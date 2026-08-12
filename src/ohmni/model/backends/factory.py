from __future__ import annotations

from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

from ohmni.config.settings import Settings
from ohmni.model.backends.harness_backend import HarnessModelBackend
from ohmni.model.contracts import FakeModelBackend, ModelResponse
from ohmni.model.errors import ModelConfigurationError
from ohmni.model.infrastructure.langchain_backend import LangChainModelBackend as GenericLangChainModelBackend


def _fake_response(request):
    return ModelResponse(
        content=(
            "V1 in 0 DC 5\n"
            "R1 in out 1k\n"
            "C1 out 0 1u\n"
            ".tran 1ms 10ms\n"
            ".end\n"
        ),
        metadata={"fake": True},
    )


def _build_api_chat_model(settings: Settings):
    provider = settings.model_provider
    api_key = settings.api_key
    if provider == "google":
        return ChatGoogleGenerativeAI(
            model=settings.model_name,
            api_key=SecretStr(api_key) if api_key else None,
            vertexai=False,
            request_timeout=settings.model_timeout_seconds,
        )
    if provider == "openai":
        return ChatOpenAI(
            model=settings.model_name,
            api_key=api_key,
            timeout=settings.model_timeout_seconds,
        )
    if provider == "anthropic":
        return ChatAnthropic(
            model=settings.model_name,
            api_key=api_key,
            timeout=settings.model_timeout_seconds,
        )
    raise ModelConfigurationError(
        f"Unsupported API provider: {provider!r}",
        backend="api",
        provider=provider,
        model=settings.model_name,
    )


def build_model_backend(settings: Settings):
    if settings.model_backend == "fake":
        return FakeModelBackend(_fake_response)
    if settings.model_backend == "harness":
        return HarnessModelBackend(
            provider=settings.model_provider,
            model=settings.model_name,
            timeout_seconds=settings.model_timeout_seconds,
            workspace_dir=settings.workspace_dir,
        )
    if settings.model_backend == "api":
        chat_model = _build_api_chat_model(settings)
        return GenericLangChainModelBackend(
            chat_model=chat_model,
            backend_name="api",
            provider=settings.model_provider,
            model_name=settings.model_name,
        )
    raise ModelConfigurationError(f"Unknown backend: {settings.model_backend!r}")
