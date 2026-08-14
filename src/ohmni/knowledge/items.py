"""Normalized universal knowledge items."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from typing import Any, Mapping, TypeAlias

from .errors import KnowledgeValidationError
from .payloads import (
    ConstraintKnowledge,
    EntityKnowledge,
    FactKnowledge,
    FormulaKnowledge,
    ProcedureKnowledge,
    RelationKnowledge,
    RuleKnowledge,
    ToolKnowledge,
)
from .provenance import EpistemicStatus, Provenance, _safe_metadata
from .taxonomy import KnowledgeFamily, KnowledgeKind


KnowledgePayload: TypeAlias = (
    EntityKnowledge
    | FactKnowledge
    | RelationKnowledge
    | RuleKnowledge
    | ConstraintKnowledge
    | FormulaKnowledge
    | ProcedureKnowledge
    | ToolKnowledge
)

_PAYLOAD_TYPES: dict[KnowledgeKind, type] = {
    KnowledgeKind.ENTITY: EntityKnowledge,
    KnowledgeKind.FACT: FactKnowledge,
    KnowledgeKind.RELATION: RelationKnowledge,
    KnowledgeKind.RULE: RuleKnowledge,
    KnowledgeKind.CONSTRAINT: ConstraintKnowledge,
    KnowledgeKind.FORMULA: FormulaKnowledge,
    KnowledgeKind.PROCEDURE: ProcedureKnowledge,
    KnowledgeKind.TOOL: ToolKnowledge,
}


def _text(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise KnowledgeValidationError(f"{field_name} must be a non-blank string")
    return value.strip()


@dataclass(frozen=True, slots=True)
class KnowledgeRelationship:
    """A lightweight reference to another normalized knowledge item."""

    relationship_type: str
    target_id: str
    metadata: Mapping[str, Any] = field(default_factory=dict, repr=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "relationship_type", _text(self.relationship_type, "relationship_type"))
        object.__setattr__(self, "target_id", _text(self.target_id, "target_id"))
        object.__setattr__(self, "metadata", _safe_metadata(self.metadata))

    def to_dict(self) -> dict[str, Any]:
        return {
            "relationship_type": self.relationship_type,
            "target_id": self.target_id,
            "metadata": _safe_metadata(self.metadata),
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "KnowledgeRelationship":
        return cls(
            relationship_type=payload["relationship_type"],
            target_id=payload["target_id"],
            metadata=payload.get("metadata", {}),
        )


@dataclass(frozen=True, slots=True)
class KnowledgeItem:
    """A typed, traceable, provider-neutral unit of reusable knowledge."""

    id: str
    title: str
    family: KnowledgeFamily
    kind: KnowledgeKind
    payload: KnowledgePayload
    provenance: Provenance
    tags: tuple[str, ...] = ()
    applicability: str | None = None
    epistemic_status: EpistemicStatus = EpistemicStatus.RETRIEVED
    relationships: tuple[KnowledgeRelationship, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict, repr=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "id", _text(self.id, "id"))
        object.__setattr__(self, "title", _text(self.title, "title"))
        if not isinstance(self.family, KnowledgeFamily):
            try:
                object.__setattr__(self, "family", KnowledgeFamily.from_value(str(self.family)))
            except ValueError as exc:
                raise KnowledgeValidationError(f"Unknown knowledge family: {self.family!r}") from exc
        if not isinstance(self.kind, KnowledgeKind):
            try:
                object.__setattr__(self, "kind", KnowledgeKind.from_value(str(self.kind)))
            except ValueError as exc:
                raise KnowledgeValidationError(f"Unknown knowledge kind: {self.kind!r}") from exc
        expected_type = _PAYLOAD_TYPES[self.kind]
        if not isinstance(self.payload, expected_type):
            raise KnowledgeValidationError(
                f"Payload for kind {self.kind.value!r} must be {expected_type.__name__}, "
                f"got {type(self.payload).__name__}"
            )
        if not isinstance(self.provenance, Provenance):
            raise KnowledgeValidationError("provenance must be a Provenance instance")
        if not isinstance(self.epistemic_status, EpistemicStatus):
            try:
                object.__setattr__(self, "epistemic_status", EpistemicStatus(str(self.epistemic_status).lower()))
            except ValueError as exc:
                raise KnowledgeValidationError(f"Unknown epistemic status: {self.epistemic_status!r}") from exc
        normalized_tags = tuple(sorted({_text(tag, "tag") for tag in self.tags}))
        object.__setattr__(self, "tags", normalized_tags)
        if self.applicability is not None:
            object.__setattr__(self, "applicability", _text(self.applicability, "applicability"))
        relationships = tuple(
            relationship if isinstance(relationship, KnowledgeRelationship) else KnowledgeRelationship.from_dict(relationship)
            for relationship in self.relationships
        )
        object.__setattr__(self, "relationships", relationships)
        object.__setattr__(self, "metadata", _safe_metadata(self.metadata))

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "family": self.family.value,
            "kind": self.kind.value,
            "payload": self.payload.to_dict(),
            "tags": list(self.tags),
            "applicability": self.applicability,
            "epistemic_status": self.epistemic_status.value,
            "relationships": [relationship.to_dict() for relationship in self.relationships],
            "provenance": self.provenance.to_dict(),
            "metadata": _safe_metadata(self.metadata),
        }

    def to_json(self) -> str:
        """Return deterministic JSON suitable for artifacts and snapshots."""

        return json.dumps(self.to_dict(), indent=2, sort_keys=True) + "\n"

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "KnowledgeItem":
        kind = KnowledgeKind.from_value(str(payload["kind"]))
        payload_type = _PAYLOAD_TYPES[kind]
        return cls(
            id=payload["id"],
            title=payload["title"],
            family=KnowledgeFamily.from_value(str(payload["family"])),
            kind=kind,
            payload=payload_type(**payload["payload"]),
            tags=tuple(payload.get("tags", ())),
            applicability=payload.get("applicability"),
            epistemic_status=EpistemicStatus(str(payload.get("epistemic_status", EpistemicStatus.RETRIEVED.value)).lower()),
            relationships=tuple(KnowledgeRelationship.from_dict(item) for item in payload.get("relationships", ())),
            provenance=Provenance.from_dict(payload["provenance"]),
            metadata=payload.get("metadata", {}),
        )


__all__ = ["KnowledgeItem", "KnowledgePayload", "KnowledgeRelationship"]
