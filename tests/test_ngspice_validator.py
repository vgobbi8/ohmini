from __future__ import annotations

import os
import subprocess
from pathlib import Path
import tempfile
import unittest
from unittest import mock

from ohmni.generation.contracts import GeneratedCircuit
from ohmni.model.contracts import ModelUsage
from ohmni.validation.contracts import ValidationContext
from ohmni.validation.ngspice import NgSpiceValidator


class NgSpiceValidatorTests(unittest.TestCase):
    def test_passed_validation_persists_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            circuit = GeneratedCircuit(requirement="r", netlist="V1 in 0 5\n.end\n", raw_model_response="raw", model_usage=ModelUsage())
            context = ValidationContext(run_dir=tmp_path / "run dir", ngspice_executable="ngspice", timeout_seconds=5)
            validator = NgSpiceValidator()
            completed = subprocess.CompletedProcess(args=["ngspice"], returncode=0, stdout="ngspice ok\nargs\n", stderr="")
            with mock.patch("ohmni.validation.ngspice.subprocess.run", return_value=completed):
                result = validator.validate(circuit, context)
            self.assertEqual(result.status, "passed")
            self.assertTrue((context.run_dir / "generated.sp").exists())
            self.assertTrue((context.run_dir / "ngspice.stdout.txt").exists())
            self.assertTrue((context.run_dir / "ngspice.command.txt").exists())

    def test_nonzero_exit_is_failed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            circuit = GeneratedCircuit(requirement="r", netlist="V1 in 0 5\n.end\n", raw_model_response="raw")
            context = ValidationContext(run_dir=tmp_path / "run", ngspice_executable="ngspice", timeout_seconds=5)
            completed = subprocess.CompletedProcess(args=["ngspice"], returncode=2, stdout="", stderr="")
            with mock.patch("ohmni.validation.ngspice.subprocess.run", return_value=completed):
                result = NgSpiceValidator().validate(circuit, context)
            self.assertEqual(result.status, "failed")
            self.assertEqual(result.exit_code, 2)

    def test_timeout_is_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            circuit = GeneratedCircuit(requirement="r", netlist="V1 in 0 5\n.end\n", raw_model_response="raw")
            context = ValidationContext(run_dir=tmp_path / "run", ngspice_executable="ngspice", timeout_seconds=0.1)
            with mock.patch(
                "ohmni.validation.ngspice.subprocess.run",
                side_effect=subprocess.TimeoutExpired(cmd=["ngspice"], timeout=0.1),
            ):
                result = NgSpiceValidator().validate(circuit, context)
            self.assertEqual(result.status, "error")
            self.assertTrue(any(issue.code == "NGSPICE_TIMEOUT" for issue in result.issues))

    def test_missing_executable_is_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            circuit = GeneratedCircuit(requirement="r", netlist="V1 in 0 5\n.end\n", raw_model_response="raw")
            context = ValidationContext(run_dir=tmp_path / "run", ngspice_executable=str(tmp_path / "missing"), timeout_seconds=5)
            result = NgSpiceValidator().validate(circuit, context)
            self.assertEqual(result.status, "error")
            self.assertTrue(any(issue.code == "NGSPICE_MISSING_EXECUTABLE" for issue in result.issues))

    def test_paths_with_spaces_work(self) -> None:
        with tempfile.TemporaryDirectory(prefix="ohmni test ") as tmp:
            tmp_path = Path(tmp)
            circuit = GeneratedCircuit(requirement="r", netlist="V1 in 0 5\n.end\n", raw_model_response="raw")
            context = ValidationContext(run_dir=tmp_path / "run dir with spaces", ngspice_executable="ngspice", timeout_seconds=5)
            completed = subprocess.CompletedProcess(args=["ngspice"], returncode=0, stdout="ok\n", stderr="")
            with mock.patch("ohmni.validation.ngspice.subprocess.run", return_value=completed):
                result = NgSpiceValidator().validate(circuit, context)
            self.assertEqual(result.status, "passed")

    def test_invalid_executable_is_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            circuit = GeneratedCircuit(requirement="r", netlist="V1 in 0 5\n.end\n", raw_model_response="raw")
            context = ValidationContext(run_dir=tmp_path / "run", ngspice_executable="ngspice", timeout_seconds=5)
            with mock.patch(
                "ohmni.validation.ngspice.subprocess.run",
                side_effect=OSError("invalid executable format"),
            ):
                result = NgSpiceValidator().validate(circuit, context)
            self.assertEqual(result.status, "error")
            self.assertTrue(any(issue.code == "NGSPICE_EXECUTION_ERROR" for issue in result.issues))


if __name__ == "__main__":
    unittest.main()
