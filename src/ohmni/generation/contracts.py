from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Protocol, runtime_checkable

from ohmni.model.contracts import ModelResponse, ModelUsage


@dataclass(slots=True, frozen=True)
class CircuitGenerationRequest:
    requirement: str
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.requirement or not self.requirement.strip():
            raise ValueError("CircuitGenerationRequest.requirement must not be blank")


@dataclass(slots=True, frozen=True)
class GeneratedCircuit:
    requirement: str
    netlist: str
    raw_model_response: str
    model_usage: ModelUsage | None = None
    model_metadata: Mapping[str, Any] = field(default_factory=dict)
    generator_name: str = "direct_spice"
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        payload = {
            "requirement": self.requirement,
            "netlist": self.netlist,
            "raw_model_response": self.raw_model_response,
            "model_metadata": dict(self.model_metadata),
            "generator_name": self.generator_name,
            "metadata": dict(self.metadata),
        }
        if self.model_usage is not None:
            payload["model_usage"] = self.model_usage.to_dict()
        return payload


@runtime_checkable
class CircuitGenerator(Protocol):
    def generate(self, request: CircuitGenerationRequest) -> GeneratedCircuit: ...
