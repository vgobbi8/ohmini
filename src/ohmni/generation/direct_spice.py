from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any

from ohmni.generation.contracts import CircuitGenerationRequest, GeneratedCircuit
from ohmni.generation.errors import GenerationError
from ohmni.model.contracts import ModelBackend, ModelRequest, ModelResponse


DEFAULT_SYSTEM_PROMPT = (
    "You are a circuit netlist generator. "
    "Return exactly one complete ngspice-compatible SPICE netlist as plain text. "
    "Do not use Markdown fences or explanations. "
    "Include .end. "
    "Use explicit component values."
)


_FENCE_RE = re.compile(r"```(?:[a-zA-Z0-9_+-]+)?\n(.*?)\n```", re.DOTALL)


def _looks_like_netlist_line(line: str) -> bool:
    stripped = line.lstrip()
    if not stripped:
        return False
    if stripped.startswith("*") or stripped.startswith("."):
        return True
    return bool(re.match(r"^[A-Za-z][^\s]*\s+", stripped))


def _normalize_model_text(text: str) -> str:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n").strip()
    if not normalized:
        raise GenerationError("Model returned empty output")

    fenced = _FENCE_RE.findall(normalized)
    candidate = fenced[0].strip() if len(fenced) == 1 else normalized
    lines = [line.rstrip() for line in candidate.splitlines()]

    if len(fenced) != 1:
        start = next((i for i, line in enumerate(lines) if _looks_like_netlist_line(line)), None)
        end = next((i for i in range(len(lines) - 1, -1, -1) if lines[i].strip().lower() == ".end"), None)
        if start is not None and end is not None and end >= start:
            lines = lines[start : end + 1]

    meaningful = [line for line in lines if line.strip() and not line.lstrip().startswith("*")]
    if not meaningful:
        raise GenerationError("Model output did not contain a usable netlist")
    if not any(line.strip().lower().startswith(".end") for line in lines):
        raise GenerationError("Model output did not contain .end")

    return "\n".join(lines).strip() + "\n"


@dataclass(slots=True)
class DirectSpiceGenerator:
    backend: ModelBackend
    system_prompt: str = DEFAULT_SYSTEM_PROMPT

    def generate(self, request: CircuitGenerationRequest) -> GeneratedCircuit:
        prompt = (
            "Create exactly one complete ngspice-compatible SPICE netlist for the requirement below.\n\n"
            f"Requirement:\n{request.requirement.strip()}\n"
        )
        response = self.backend.invoke(
            ModelRequest(prompt=prompt, system_prompt=self.system_prompt, metadata=dict(request.metadata))
        )
        if not isinstance(response, ModelResponse):  # pragma: no cover - defensive
            raise GenerationError("Model backend returned an invalid response object")
        netlist = _normalize_model_text(response.content)
        metadata: dict[str, Any] = {
            "normalized": True,
            "response_length": len(response.content),
            "netlist_length": len(netlist),
        }
        return GeneratedCircuit(
            requirement=request.requirement.strip(),
            netlist=netlist,
            raw_model_response=response.content,
            model_usage=response.usage,
            model_metadata=dict(response.metadata),
            generator_name="direct_spice",
            metadata=metadata,
        )
