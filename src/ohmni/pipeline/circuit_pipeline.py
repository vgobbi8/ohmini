from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Sequence

from ohmni.generation.contracts import CircuitGenerationRequest, CircuitGenerator, GeneratedCircuit
from ohmni.generation.errors import GenerationError
from ohmni.model.errors import ModelError
from ohmni.pipeline.artifacts import RunArtifacts, utc_timestamp
from ohmni.validation.contracts import CircuitValidator, ValidationContext, ValidationResult


@dataclass(slots=True, frozen=True)
class PipelineResult:
    run_id: str
    status: str
    requirement: str
    run_dir: Path
    report_path: Path
    generated_circuit: GeneratedCircuit | None = None
    validation_results: tuple[ValidationResult, ...] = ()
    error_message: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "status": self.status,
            "requirement": self.requirement,
            "run_dir": str(self.run_dir),
            "report_path": str(self.report_path),
            "generated_circuit": None if self.generated_circuit is None else self.generated_circuit.to_dict(),
            "validation_results": [result.to_dict() for result in self.validation_results],
            "error_message": self.error_message,
            "metadata": dict(self.metadata),
        }


@dataclass(slots=True)
class CircuitPipeline:
    generator: CircuitGenerator
    validators: Sequence[CircuitValidator]
    output_dir: Path
    config_snapshot: dict[str, Any]
    ngspice_executable: str
    model_identity: dict[str, Any]

    def run(self, requirement: str) -> PipelineResult:
        artifacts = RunArtifacts.create(self.output_dir)
        request = CircuitGenerationRequest(requirement=requirement)
        started_at = utc_timestamp()
        artifacts.write_json(
            "request.json",
            {"run_id": artifacts.run_id, "started_at": started_at, "requirement": requirement.strip()},
        )
        artifacts.write_json("config.json", self.config_snapshot)

        try:
            generated = self.generator.generate(request)
            artifacts.write_text("model/response.txt", generated.raw_model_response)
            artifacts.write_json(
                "model/metadata.json",
                {
                    "model_identity": self.model_identity,
                    "model_metadata": dict(generated.model_metadata),
                    "model_usage": None if generated.model_usage is None else generated.model_usage.to_dict(),
                },
            )
            artifacts.write_text("generation/netlist.sp", generated.netlist)
            artifacts.write_text("generation/raw_response.txt", generated.raw_model_response)
        except (GenerationError, ModelError, ValueError) as exc:
            report = self._write_report(
                artifacts,
                run_status="error",
                requirement=requirement,
                generated_circuit=None,
                validation_results=(),
                error_message=str(exc),
            )
            return PipelineResult(
                run_id=artifacts.run_id,
                status="error",
                requirement=requirement,
                run_dir=artifacts.root_dir,
                report_path=report,
                error_message=str(exc),
            )

        context = ValidationContext(
            run_dir=artifacts.root_dir,
            ngspice_executable=self.ngspice_executable,
            timeout_seconds=float(self.config_snapshot["model_timeout_seconds"]),
            config_snapshot=self.config_snapshot,
        )
        validation_results: list[ValidationResult] = []
        overall_status = "passed"
        for validator in self.validators:
            result = validator.validate(generated, context)
            validation_results.append(result)
            validator_dir = artifacts.ensure_dir(f"validation/{result.validator_name}")
            artifacts.write_json(f"validation/{result.validator_name}/result.json", result.to_dict())
            if result.stdout_path:
                artifacts.write_text(
                    f"validation/{result.validator_name}/stdout.txt",
                    Path(result.stdout_path).read_text(encoding="utf-8") if Path(result.stdout_path).exists() else "",
                )
            if result.stderr_path:
                artifacts.write_text(
                    f"validation/{result.validator_name}/stderr.txt",
                    Path(result.stderr_path).read_text(encoding="utf-8") if Path(result.stderr_path).exists() else "",
                )
            if result.status == "failed":
                overall_status = "failed"
            elif result.status == "error" and overall_status == "passed":
                overall_status = "error"

        report = self._write_report(
            artifacts,
            run_status=overall_status,
            requirement=requirement,
            generated_circuit=generated,
            validation_results=tuple(validation_results),
            error_message=None,
        )
        return PipelineResult(
            run_id=artifacts.run_id,
            status=overall_status,
            requirement=requirement,
            run_dir=artifacts.root_dir,
            report_path=report,
            generated_circuit=generated,
            validation_results=tuple(validation_results),
        )

    def _write_report(
        self,
        artifacts: RunArtifacts,
        *,
        run_status: str,
        requirement: str,
        generated_circuit: GeneratedCircuit | None,
        validation_results: tuple[ValidationResult, ...],
        error_message: str | None,
    ) -> Path:
        report = {
            "run_id": artifacts.run_id,
            "started_at": utc_timestamp(),
            "status": run_status,
            "requirement": requirement.strip(),
            "generator": None if generated_circuit is None else generated_circuit.generator_name,
            "model_identity": self.model_identity,
            "config_snapshot": self.config_snapshot,
            "validation_results": [result.to_dict() for result in validation_results],
            "generated_netlist_path": None if generated_circuit is None else "generation/netlist.sp",
            "artifact_paths": {
                "request": "request.json",
                "config": "config.json",
                "model_response": "model/response.txt",
                "model_metadata": "model/metadata.json",
                "generated_netlist": "generation/netlist.sp",
                "raw_response": "generation/raw_response.txt",
                "report": "report.json",
            },
            "error_message": error_message,
        }
        path = artifacts.write_json("report.json", report)
        return path
