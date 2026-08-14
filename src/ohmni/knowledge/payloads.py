"""Typed, provider-independent payloads for each knowledge kind."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from .errors import KnowledgeValidationError
from .taxonomy import ConstraintStrength


def _text(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise KnowledgeValidationError(f"{field_name} must be a non-blank string")
    return value.strip()


def _texts(values: tuple[str, ...] | list[str], field_name: str) -> tuple[str, ...]:
    normalized = tuple(_text(value, field_name) for value in values)
    return normalized


def _mapping(values: Mapping[str, Any], field_name: str) -> dict[str, Any]:
    if not isinstance(values, Mapping):
        raise KnowledgeValidationError(f"{field_name} must be a mapping")
    return {str(key): value for key, value in sorted(values.items(), key=lambda item: str(item[0]))}


@dataclass(frozen=True, slots=True)
class EntityKnowledge:
    entity_type: str
    canonical_name: str
    aliases: tuple[str, ...] = ()
    properties: Mapping[str, Any] = field(default_factory=dict)
    external_ids: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "entity_type", _text(self.entity_type, "entity_type"))
        object.__setattr__(self, "canonical_name", _text(self.canonical_name, "canonical_name"))
        object.__setattr__(self, "aliases", _texts(self.aliases, "alias"))
        object.__setattr__(self, "properties", _mapping(self.properties, "properties"))
        object.__setattr__(self, "external_ids", _mapping(self.external_ids, "external_ids"))

    def to_dict(self) -> dict[str, Any]:
        return {"entity_type": self.entity_type, "canonical_name": self.canonical_name, "aliases": list(self.aliases), "properties": dict(self.properties), "external_ids": dict(self.external_ids)}


@dataclass(frozen=True, slots=True)
class FactKnowledge:
    subject: str
    property: str
    value: Any
    unit: str | None = None
    qualifiers: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "subject", _text(self.subject, "subject"))
        object.__setattr__(self, "property", _text(self.property, "property"))
        object.__setattr__(self, "qualifiers", _mapping(self.qualifiers, "qualifiers"))
        if self.unit is not None:
            object.__setattr__(self, "unit", _text(self.unit, "unit"))

    def to_dict(self) -> dict[str, Any]:
        return {"subject": self.subject, "property": self.property, "value": self.value, "unit": self.unit, "qualifiers": dict(self.qualifiers)}


@dataclass(frozen=True, slots=True)
class RelationKnowledge:
    subject: str
    predicate: str
    object: str
    qualifiers: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "subject", _text(self.subject, "subject"))
        object.__setattr__(self, "predicate", _text(self.predicate, "predicate"))
        object.__setattr__(self, "object", _text(self.object, "object"))
        object.__setattr__(self, "qualifiers", _mapping(self.qualifiers, "qualifiers"))

    def to_dict(self) -> dict[str, Any]:
        return {"subject": self.subject, "predicate": self.predicate, "object": self.object, "qualifiers": dict(self.qualifiers)}


@dataclass(frozen=True, slots=True)
class RuleKnowledge:
    statement: str
    conditions: tuple[str, ...] = ()
    consequences: tuple[str, ...] = ()
    priority: int | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "statement", _text(self.statement, "statement"))
        object.__setattr__(self, "conditions", _texts(self.conditions, "condition"))
        object.__setattr__(self, "consequences", _texts(self.consequences, "consequence"))

    def to_dict(self) -> dict[str, Any]:
        return {"statement": self.statement, "conditions": list(self.conditions), "consequences": list(self.consequences), "priority": self.priority}


@dataclass(frozen=True, slots=True)
class ConstraintKnowledge:
    statement: str
    strength: ConstraintStrength
    scope: str
    condition: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "statement", _text(self.statement, "statement"))
        object.__setattr__(self, "scope", _text(self.scope, "scope"))
        if not isinstance(self.strength, ConstraintStrength):
            try:
                object.__setattr__(self, "strength", ConstraintStrength(str(self.strength).lower()))
            except ValueError as exc:
                raise KnowledgeValidationError(f"Unknown constraint strength: {self.strength!r}") from exc
        if self.condition is not None:
            object.__setattr__(self, "condition", _text(self.condition, "condition"))

    def to_dict(self) -> dict[str, Any]:
        return {"statement": self.statement, "strength": self.strength.value, "scope": self.scope, "condition": self.condition}


@dataclass(frozen=True, slots=True)
class FormulaKnowledge:
    expression: str
    variables: Mapping[str, str] = field(default_factory=dict)
    units: Mapping[str, str] = field(default_factory=dict)
    applicability: str | None = None
    notes: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "expression", _text(self.expression, "expression"))
        object.__setattr__(self, "variables", _mapping(self.variables, "variables"))
        object.__setattr__(self, "units", _mapping(self.units, "units"))
        for name in ("applicability", "notes"):
            value = getattr(self, name)
            if value is not None:
                object.__setattr__(self, name, _text(value, name))

    def to_dict(self) -> dict[str, Any]:
        return {"expression": self.expression, "variables": dict(self.variables), "units": dict(self.units), "applicability": self.applicability, "notes": self.notes}


@dataclass(frozen=True, slots=True)
class ProcedureKnowledge:
    goal: str
    inputs: tuple[str, ...] = ()
    prerequisites: tuple[str, ...] = ()
    steps: tuple[str, ...] = ()
    outputs: tuple[str, ...] = ()
    validation_strategy: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "goal", _text(self.goal, "goal"))
        object.__setattr__(self, "inputs", _texts(self.inputs, "input"))
        object.__setattr__(self, "prerequisites", _texts(self.prerequisites, "prerequisite"))
        object.__setattr__(self, "steps", _texts(self.steps, "step"))
        object.__setattr__(self, "outputs", _texts(self.outputs, "output"))
        if self.validation_strategy is not None:
            object.__setattr__(self, "validation_strategy", _text(self.validation_strategy, "validation_strategy"))

    def to_dict(self) -> dict[str, Any]:
        return {"goal": self.goal, "inputs": list(self.inputs), "prerequisites": list(self.prerequisites), "steps": list(self.steps), "outputs": list(self.outputs), "validation_strategy": self.validation_strategy}


@dataclass(frozen=True, slots=True)
class ToolKnowledge:
    name: str
    capabilities: tuple[str, ...] = ()
    limitations: tuple[str, ...] = ()
    inputs: tuple[str, ...] = ()
    outputs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "name", _text(self.name, "name"))
        for field_name in ("capabilities", "limitations", "inputs", "outputs"):
            object.__setattr__(self, field_name, _texts(getattr(self, field_name), field_name[:-1] if field_name.endswith("s") else field_name))

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name, "capabilities": list(self.capabilities), "limitations": list(self.limitations), "inputs": list(self.inputs), "outputs": list(self.outputs)}


__all__ = [
    "ConstraintKnowledge",
    "EntityKnowledge",
    "FactKnowledge",
    "FormulaKnowledge",
    "ProcedureKnowledge",
    "RelationKnowledge",
    "RuleKnowledge",
    "ToolKnowledge",
]
