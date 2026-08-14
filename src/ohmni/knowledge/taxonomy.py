"""Stable, task-oriented knowledge taxonomy."""

from __future__ import annotations

from enum import StrEnum


class KnowledgeFamily(StrEnum):
    """Broad role a knowledge item plays for a design process."""

    DECLARATIVE = "declarative"
    PROCEDURAL = "procedural"
    OPERATIONAL = "operational"

    @classmethod
    def from_value(cls, value: str) -> "KnowledgeFamily":
        """Parse the stable serialized value, rejecting blank/unknown values."""

        if not isinstance(value, str) or not value.strip():
            raise ValueError("KnowledgeFamily value must be a non-blank string")
        return cls(value.strip().lower())


class KnowledgeKind(StrEnum):
    """The eight reusable knowledge forms supported by this slice."""

    ENTITY = "entity"
    FACT = "fact"
    RELATION = "relation"
    RULE = "rule"
    CONSTRAINT = "constraint"
    FORMULA = "formula"
    PROCEDURE = "procedure"
    TOOL = "tool"

    @property
    def default_family(self) -> KnowledgeFamily:
        """Return the recommended family for this kind.

        A future item may explicitly override this recommendation when there
        is a documented domain reason; the taxonomy does not enforce that
        policy or perform inference.
        """

        if self is KnowledgeKind.PROCEDURE:
            return KnowledgeFamily.PROCEDURAL
        if self is KnowledgeKind.TOOL:
            return KnowledgeFamily.OPERATIONAL
        return KnowledgeFamily.DECLARATIVE

    @classmethod
    def from_value(cls, value: str) -> KnowledgeKind:
        """Parse the stable serialized value, rejecting blank/unknown values."""

        if not isinstance(value, str) or not value.strip():
            raise ValueError("KnowledgeKind value must be a non-blank string")
        return cls(value.strip().lower())


class ConstraintStrength(StrEnum):
    """How strongly a constraint should influence a design decision."""

    HARD = "hard"
    SOFT = "soft"
    RECOMMENDATION = "recommendation"

    @classmethod
    def from_value(cls, value: str) -> "ConstraintStrength":
        if not isinstance(value, str) or not value.strip():
            raise ValueError("ConstraintStrength value must be a non-blank string")
        return cls(value.strip().lower())


__all__ = ["ConstraintStrength", "KnowledgeFamily", "KnowledgeKind"]




