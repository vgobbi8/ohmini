from __future__ import annotations

from dataclasses import dataclass

from ohmni.errors import OhmniError


@dataclass(slots=True)
class _ModelErrorDetails:
    backend: str | None = None
    provider: str | None = None
    model: str | None = None
    exit_code: int | None = None


class ModelError(OhmniError):
    def __init__(
        self,
        message: str,
        *,
        backend: str | None = None,
        provider: str | None = None,
        model: str | None = None,
        exit_code: int | None = None,
    ) -> None:
        super().__init__(message)
        self.backend = backend
        self.provider = provider
        self.model = model
        self.exit_code = exit_code


class ModelConfigurationError(ModelError):
    pass


class ModelInvocationError(ModelError):
    pass


class ModelTimeoutError(ModelError):
    pass


class ModelOutputError(ModelError):
    pass


class ModelBackendError(ModelError):
    pass
