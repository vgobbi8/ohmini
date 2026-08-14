from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess
import time

from ohmni.generation.contracts import GeneratedCircuit
from ohmni.validation.contracts import CircuitValidator, ValidationContext, ValidationIssue, ValidationResult


@dataclass(slots=True)
class NgSpiceValidator:
    name: str = "ngspice"

    def validate(self, circuit: GeneratedCircuit, context: ValidationContext) -> ValidationResult:
        start = time.perf_counter()
        run_dir = Path(context.run_dir)
        run_dir.mkdir(parents=True, exist_ok=True)

        netlist_path = run_dir / "generated.sp"
        netlist_path.write_text(circuit.netlist, encoding="utf-8")

        stdout_path = run_dir / "ngspice.stdout.txt"
        stderr_path = run_dir / "ngspice.stderr.txt"
        command_log_path = run_dir / "ngspice.command.txt"

        command = [context.ngspice_executable, "-b", "-o", str(run_dir / "ngspice.log"), str(netlist_path)]
        command_log_path.write_text(" ".join(command), encoding="utf-8")

        try:
            completed = subprocess.run(
                command,
                cwd=str(run_dir),
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=context.timeout_seconds,
                shell=False,
                check=False,
            )
        except FileNotFoundError as exc:
            duration = time.perf_counter() - start
            issue = ValidationIssue(
                code="NGSPICE_MISSING_EXECUTABLE",
                message=f"ngspice executable not found: {context.ngspice_executable}",
                details={"error": str(exc)},
            )
            return ValidationResult(
                validator_name=self.name,
                status="error",
                issues=(issue,),
                duration_seconds=duration,
                stdout_path=str(stdout_path),
                stderr_path=str(stderr_path),
                artifact_names=(netlist_path.name, stdout_path.name, stderr_path.name, command_log_path.name),
            )
        except OSError as exc:
            duration = time.perf_counter() - start
            issue = ValidationIssue(
                code="NGSPICE_EXECUTION_ERROR",
                message=f"ngspice could not be executed: {context.ngspice_executable}",
                details={"error": str(exc)},
            )
            return ValidationResult(
                validator_name=self.name,
                status="error",
                issues=(issue,),
                duration_seconds=duration,
                stdout_path=str(stdout_path),
                stderr_path=str(stderr_path),
                artifact_names=(netlist_path.name, stdout_path.name, stderr_path.name, command_log_path.name),
            )
        except subprocess.TimeoutExpired as exc:
            duration = time.perf_counter() - start
            stdout_text = exc.stdout or ""
            stderr_text = exc.stderr or ""
            stdout_path.write_text(stdout_text, encoding="utf-8")
            stderr_path.write_text(stderr_text, encoding="utf-8")
            issue = ValidationIssue(code="NGSPICE_TIMEOUT", message="ngspice timed out", details={"timeout_seconds": context.timeout_seconds})
            return ValidationResult(
                validator_name=self.name,
                status="error",
                issues=(issue,),
                duration_seconds=duration,
                stdout_path=str(stdout_path),
                stderr_path=str(stderr_path),
                artifact_names=(netlist_path.name, stdout_path.name, stderr_path.name, command_log_path.name),
            )

        stdout_path.write_text(completed.stdout or "", encoding="utf-8")
        stderr_path.write_text(completed.stderr or "", encoding="utf-8")
        duration = time.perf_counter() - start

        if completed.returncode != 0:
            issue = ValidationIssue(
                code="NGSPICE_NONZERO_EXIT",
                message="ngspice exited with a non-zero status",
                details={"returncode": completed.returncode},
            )
            return ValidationResult(
                validator_name=self.name,
                status="failed",
                issues=(issue,),
                duration_seconds=duration,
                exit_code=completed.returncode,
                stdout_path=str(stdout_path),
                stderr_path=str(stderr_path),
                artifact_names=(netlist_path.name, stdout_path.name, stderr_path.name, command_log_path.name),
            )

        output_text = f"{completed.stdout or ''}\n{completed.stderr or ''}".lower()
        if "fatal" in output_text or "error" in output_text:
            issue = ValidationIssue(
                code="NGSPICE_FATAL_OUTPUT",
                message="ngspice reported a fatal parsing or simulation error",
                details={"stdout": completed.stdout, "stderr": completed.stderr},
            )
            return ValidationResult(
                validator_name=self.name,
                status="failed",
                issues=(issue,),
                duration_seconds=duration,
                exit_code=completed.returncode,
                stdout_path=str(stdout_path),
                stderr_path=str(stderr_path),
                artifact_names=(netlist_path.name, stdout_path.name, stderr_path.name, command_log_path.name),
            )

        return ValidationResult(
            validator_name=self.name,
            status="passed",
            duration_seconds=duration,
            exit_code=completed.returncode,
            stdout_path=str(stdout_path),
            stderr_path=str(stderr_path),
            artifact_names=(netlist_path.name, stdout_path.name, stderr_path.name, command_log_path.name),
        )
