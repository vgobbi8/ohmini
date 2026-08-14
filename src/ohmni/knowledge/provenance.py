"""Traceability, authority, and epistemic state for knowledge items."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any, Mapping

from .errors import KnowledgeValidationError


class SourceType(StrEnum):
    """Supported source categories without coupling to provider classes."""

    MANUAL_MARKDOWN = "manual_markdown"
    KICAD_SYMBOL_LIBRARY = "kicad_symbol_library"
    DATABASE = "database"
    HTTP = "http"
    MCP = "mcp"
    AGENT_MEMORY = "agent_memory"
    UNKNOWN = "unknown"


class AuthorityLevel(StrEnum):
    """Trust level of a source for a specifically scoped subject area."""

    AUTHORITATIVE = "authoritative"
    CURATED = "curated"
    DERIVED = "derived"
    HEURISTIC = "heuristic"
    EXAMPLE = "example"
    UNVERIFIED = "unverified"


class EpistemicStatus(StrEnum):
    """How a knowledge item is known, rather than how relevant it is."""

    ASSERTED = "asserted"
    RETRIEVED = "retrieved"
    DERIVED = "derived"
    ASSUMED = "assumed"
    RECOMMENDED = "recommended"
    CANDIDATE = "candidate"
    UNKNOWN = "unknown"


_SECRET_MARKERS = (
    "api_key",
    "apikey",
    "authorization",
    "credential",
    "cookie",
    "password",
    "secret",
    "token",
)


def _is_secret_key(key: str) -> bool:
    normalized = key.strip().lower().replace("-", "_")
    return any(marker in normalized for marker in _SECRET_MARKERS)


def _safe_metadata(value: Any) -> Any:
    """Copy metadata while removing credential-like fields recursively."""

    if isinstance(value, Mapping):
        return {
            str(key): _safe_metadata(item)
            for key, item in value.items()
            if not _is_secret_key(str(key))
        }
    if isinstance(value, (list, tuple)):
        return [_safe_metadata(item) for item in value]
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    return str(value)


def _required_text(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise KnowledgeValidationError(f"{field_name} must be a non-blank string")
    return value.strip()


@dataclass(frozen=True, slots=True)
class KnowledgeSource:
    """Stable identity and descriptive metadata for a source."""

    source_id: str
    source_type: SourceType
    name: str
    location: str | None = None
    version: str | None = None
    provider: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict, repr=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "source_id", _required_text(self.source_id, "source_id"))
        object.__setattr__(self, "name", _required_text(self.name, "name"))
        if not isinstance(self.source_type, SourceType):
            try:
                object.__setattr__(self, "source_type", SourceType(str(self.source_type).lower()))
            except ValueError as exc:
                raise KnowledgeValidationError(f"Unknown source_type: {self.source_type!r}") from exc
        object.__setattr__(self, "metadata", _safe_metadata(self.metadata))

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_id": self.source_id,
            "source_type": self.source_type.value,
            "name": self.name,
            "location": self.location,
            "version": self.version,
            "provider": self.provider,
            "metadata": _safe_metadata(self.metadata),
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "KnowledgeSource":
        return cls(
            source_id=payload["source_id"],
            source_type=SourceType(str(payload["source_type"]).lower()),
            name=payload["name"],
            location=payload.get("location"),
            version=payload.get("version"),
            provider=payload.get("provider"),
            metadata=payload.get("metadata", {}),
        )


@dataclass(frozen=True, slots=True)
class Authority:
    """Authority level explicitly limited to a subject scope."""

    level: AuthorityLevel
    scope: str

    def __post_init__(self) -> None:
        if not isinstance(self.level, AuthorityLevel):
            try:
                object.__setattr__(self, "level", AuthorityLevel(str(self.level).lower()))
            except ValueError as exc:
                raise KnowledgeValidationError(f"Unknown authority level: {self.level!r}") from exc
        object.__setattr__(self, "scope", _required_text(self.scope, "authority scope"))

    @property
    def authority_scope(self) -> str:
        return self.scope

    def to_dict(self) -> dict[str, str]:
        return {"level": self.level.value, "scope": self.scope}


@dataclass(frozen=True, slots=True)
class Provenance:
    """Traceability record attached to normalized knowledge."""

    source: KnowledgeSource
    authority: Authority
    epistemic_status: EpistemicStatus = EpistemicStatus.RETRIEVED
    retrieved_at: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict, repr=False)

    def __post_init__(self) -> None:
        if not isinstance(self.epistemic_status, EpistemicStatus):
            try:
                object.__setattr__(self, "epistemic_status", EpistemicStatus(str(self.epistemic_status).lower()))
            except ValueError as exc:
                raise KnowledgeValidationError(f"Unknown epistemic status: {self.epistemic_status!r}") from exc
        object.__setattr__(self, "metadata", _safe_metadata(self.metadata))

    def to_dict(self) -> dict[str, Any]:
        return {
            "source": self.source.to_dict(),
            "authority": self.authority.to_dict(),
            "epistemic_status": self.epistemic_status.value,
            "retrieved_at": self.retrieved_at,
            "metadata": _safe_metadata(self.metadata),
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "Provenance":
        authority_payload = payload["authority"]
        return cls(
            source=KnowledgeSource.from_dict(payload["source"]),
            authority=Authority(
                level=AuthorityLevel(str(authority_payload["level"]).lower()),
                scope=authority_payload["scope"],
            ),
            epistemic_status=EpistemicStatus(str(payload["epistemic_status"]).lower()),
            retrieved_at=payload.get("retrieved_at"),
            metadata=payload.get("metadata", {}),
        )


__all__ = [
    "Authority",
    "AuthorityLevel",
    "EpistemicStatus",
    "KnowledgeSource",
    "Provenance",
    "SourceType",
]
