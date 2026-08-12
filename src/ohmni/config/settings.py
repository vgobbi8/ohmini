from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping
import os

from ohmni.errors import OhmniError


class SettingsError(OhmniError):
    pass


_HARNESS_PROVIDERS = {"codex", "claude_code", "opencode", "agy"}
_API_PROVIDERS = {"openai", "anthropic", "google"}
_BACKENDS = {"fake", "harness", "api"}
_VALID_GENERATORS = {"direct_spice"}
_VALIDATORS = {"ngspice"}


def _truthy(value: str | None) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


def _parse_dotenv(path: Path) -> dict[str, str]:
    parsed: dict[str, str] = {}
    if not path.exists():
        return parsed
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'").strip('"')
        if key:
            parsed[key] = value
    return parsed


def _coerce_validators(value: str | None) -> tuple[str, ...]:
    if value is None:
        return ("ngspice",)
    parts = [item.strip() for item in value.split(",") if item.strip()]
    return tuple(parts)


@dataclass(slots=True, frozen=True)
class Settings:
    model_backend: str
    model_provider: str
    model_name: str
    model_timeout_seconds: float = 60.0
    generator_name: str = "direct_spice"
    validator_names: tuple[str, ...] = field(default_factory=lambda: ("ngspice",))
    ngspice_executable: str = "ngspice"
    output_dir: Path = Path("runs")
    output_dir_raw: str = "runs"
    dotenv_enabled: bool = True
    api_key: str | None = field(default=None, repr=False, compare=False)
    workspace_dir: Path | None = None

    @classmethod
    def from_env(
        cls,
        environ: Mapping[str, str] | None = None,
        *,
        cwd: Path | None = None,
    ) -> "Settings":
        base_env = dict(os.environ if environ is None else environ)
        cwd = Path.cwd() if cwd is None else Path(cwd)
        dotenv_enabled = _truthy(base_env.get("OHMNI_ENABLE_DOTENV", "1"))
        if dotenv_enabled:
            dotenv_path = Path(base_env.get("OHMNI_DOTENV_FILE", cwd / ".env"))
            if not dotenv_path.is_absolute():
                dotenv_path = cwd / dotenv_path
            dotenv_values = _parse_dotenv(dotenv_path)
            for key, value in dotenv_values.items():
                base_env.setdefault(key, value)

        model_backend = base_env.get("OHMNI_MODEL_BACKEND", "").strip()
        model_provider = base_env.get("OHMNI_MODEL_PROVIDER", "").strip()
        model_name = base_env.get("OHMNI_MODEL", "").strip()
        generator_name = base_env.get("OHMNI_GENERATOR", "direct_spice").strip() or "direct_spice"
        validator_names = _coerce_validators(base_env.get("OHMNI_VALIDATORS"))
        timeout_raw = base_env.get("OHMNI_MODEL_TIMEOUT_SECONDS", "60").strip()
        output_dir_raw = base_env.get("OHMNI_OUTPUT_DIR", "runs")
        output_dir_value = output_dir_raw.strip()
        ngspice_executable = base_env.get("OHMNI_NGSPICE_EXECUTABLE", "ngspice").strip() or "ngspice"
        workspace_dir_raw = base_env.get("OHMNI_HARNESS_WORKSPACE_DIR", "").strip()
        api_key = None
        if model_provider == "openai":
            api_key = base_env.get("OPENAI_API_KEY") or None
        elif model_provider == "anthropic":
            api_key = base_env.get("ANTHROPIC_API_KEY") or None
        elif model_provider == "google":
            api_key = base_env.get("GOOGLE_API_KEY") or base_env.get("GEMINI_API_KEY") or None

        try:
            timeout = float(timeout_raw)
        except ValueError as exc:
            raise SettingsError("OHMNI_MODEL_TIMEOUT_SECONDS must be numeric") from exc

        workspace_dir = Path(workspace_dir_raw) if workspace_dir_raw else None
        output_dir = Path(output_dir_value or "runs")

        settings = cls(
            model_backend=model_backend,
            model_provider=model_provider,
            model_name=model_name,
            model_timeout_seconds=timeout,
            generator_name=generator_name,
            validator_names=validator_names,
            ngspice_executable=ngspice_executable,
            output_dir=output_dir,
            output_dir_raw=output_dir_value,
            dotenv_enabled=dotenv_enabled,
            api_key=api_key,
            workspace_dir=workspace_dir,
        )
        settings.validate()
        return settings

    def validate(self) -> None:
        if self.model_backend not in _BACKENDS:
            raise SettingsError(f"Unknown model backend: {self.model_backend!r}")
        if not self.model_provider:
            raise SettingsError("OHMNI_MODEL_PROVIDER is required")
        if self.model_backend == "harness" and self.model_provider not in _HARNESS_PROVIDERS:
            raise SettingsError("Selected provider is incompatible with the harness backend")
        if self.model_backend == "api" and self.model_provider not in _API_PROVIDERS:
            raise SettingsError("Selected provider is incompatible with the API backend")
        if self.model_backend == "fake" and self.model_provider != "fake":
            raise SettingsError("Selected provider is incompatible with the fake backend")
        if not self.model_name:
            raise SettingsError("OHMNI_MODEL is required")
        if self.model_timeout_seconds <= 0:
            raise SettingsError("OHMNI_MODEL_TIMEOUT_SECONDS must be greater than zero")
        if not self.validator_names:
            raise SettingsError("At least one validator is required")
        if any(not name.strip() for name in self.validator_names):
            raise SettingsError("Validator names cannot be blank")
        if not self.output_dir_raw:
            raise SettingsError("OHMNI_OUTPUT_DIR cannot be blank")
        if self.generator_name not in _VALID_GENERATORS:
            raise SettingsError(f"Unknown generator: {self.generator_name!r}")
        for validator_name in self.validator_names:
            if validator_name not in _VALIDATORS:
                raise SettingsError(f"Unknown validator: {validator_name!r}")
        if self.model_backend == "api" and not self.api_key:
            raise SettingsError(f"Missing API credential for provider {self.model_provider!r}")

    @property
    def requires_api_key(self) -> bool:
        return self.model_backend == "api"

    def config_snapshot(self) -> dict[str, Any]:
        return {
            "backend": self.model_backend,
            "provider": self.model_provider,
            "model": self.model_name,
            "generator": self.generator_name,
            "validators": list(self.validator_names),
            "model_timeout_seconds": self.model_timeout_seconds,
            "ngspice_executable": self.ngspice_executable,
            "output_dir": str(self.output_dir),
        }

    def __repr__(self) -> str:  # pragma: no cover - intentionally simple
        return (
            "Settings("
            f"backend={self.model_backend!r}, provider={self.model_provider!r}, "
            f"model={self.model_name!r}, generator={self.generator_name!r}, "
            f"validators={list(self.validator_names)!r}, timeout={self.model_timeout_seconds!r}, "
            f"ngspice={self.ngspice_executable!r}, output_dir={str(self.output_dir)!r}"
            ")"
        )
