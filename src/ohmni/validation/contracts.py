from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping, Protocol, runtime_checkable

from ohmni.generation.contracts import GeneratedCircuit


@dataclass(slots=True, frozen=True)
class ValidationIssue:
    code: str
    message: str
    severity: str = "error"
    details: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "message": self.message,
            "severity": self.severity,
            "details": dict(self.details),
        }


@dataclass(slots=True, frozen=True)
class ValidationResult:
    validator_name: str
    status: str
    issues: tuple[ValidationIssue, ...] = ()
    duration_seconds: float | None = None
    exit_code: int | None = None
    stdout_path: str | None = None
    stderr_path: str | None = None
    artifact_names: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "validator_name": self.validator_name,
            "status": self.status,
            "issues": [issue.to_dict() for issue in self.issues],
            "duration_seconds": self.duration_seconds,
            "exit_code": self.exit_code,
            "stdout_path": self.stdout_path,
            "stderr_path": self.stderr_path,
            "artifact_names": list(self.artifact_names),
            "metadata": dict(self.metadata),
        }


@dataclass(slots=True, frozen=True)
class ValidationContext:
    run_dir: Path
    ngspice_executable: str
    timeout_seconds: float
    config_snapshot: Mapping[str, Any] = field(default_factory=dict)


@runtime_checkable
class CircuitValidator(Protocol):
    def validate(self, circuit: GeneratedCircuit, context: ValidationContext) -> ValidationResult: ...
