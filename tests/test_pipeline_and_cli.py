from __future__ import annotations

import contextlib
import io
import json
import os
from pathlib import Path
import stat
import tempfile
import textwrap
import unittest
from unittest import mock

from ohmni.cli import main
from ohmni.generation.direct_spice import DirectSpiceGenerator
from ohmni.model.contracts import FakeModelBackend, ModelResponse
from ohmni.pipeline.circuit_pipeline import CircuitPipeline
from ohmni.validation.ngspice import NgSpiceValidator


def _fake_ngspice_script(directory: Path, exit_code: int = 0) -> Path:
    script = directory / "fake-ngspice"
    script.write_text(
        textwrap.dedent(
            f"""\
            #!/usr/bin/env python3
            import sys
            print("sim ok")
            sys.exit({exit_code})
            """
        ),
        encoding="utf-8",
    )
    script.chmod(script.stat().st_mode | stat.S_IEXEC)
    return script


class PipelineAndCliTests(unittest.TestCase):
    def test_pipeline_writes_artifacts_and_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            backend = FakeModelBackend(
                lambda request: ModelResponse(
                    content="V1 in 0 5\nR1 in out 1k\nC1 out 0 1u\n.end\n",
                    metadata={"request": request.prompt},
                )
            )
            generator = DirectSpiceGenerator(backend=backend)
            script = _fake_ngspice_script(tmp_path)
            pipeline = CircuitPipeline(
                generator=generator,
                validators=[NgSpiceValidator()],
                output_dir=tmp_path / "runs",
                config_snapshot={
                    "backend": "fake",
                    "provider": "fake",
                    "model": "fake-model",
                    "generator": "direct_spice",
                    "validators": ["ngspice"],
                    "model_timeout_seconds": 5,
                    "ngspice_executable": str(script),
                    "output_dir": str(tmp_path / "runs"),
                },
                ngspice_executable=str(script),
                model_identity={"backend": "fake", "provider": "fake", "model": "fake-model"},
            )
            result = pipeline.run("RC low-pass filter")
            self.assertEqual(result.status, "passed")
            self.assertTrue(result.report_path.exists())
            report = json.loads(result.report_path.read_text(encoding="utf-8"))
            self.assertEqual(report["status"], "passed")
            self.assertEqual(report["artifact_paths"]["report"], "report.json")
            self.assertTrue((result.run_dir / "model" / "response.txt").exists())
            self.assertTrue((result.run_dir / "generation" / "netlist.sp").exists())
            self.assertTrue((result.run_dir / "validation" / "ngspice" / "result.json").exists())

    def test_cli_successful_fake_run(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            script = _fake_ngspice_script(tmp_path)
            env = {
                "OHMNI_MODEL_BACKEND": "fake",
                "OHMNI_MODEL_PROVIDER": "fake",
                "OHMNI_MODEL": "fake-model",
                "OHMNI_MODEL_TIMEOUT_SECONDS": "5",
                "OHMNI_GENERATOR": "direct_spice",
                "OHMNI_VALIDATORS": "ngspice",
                "OHMNI_NGSPICE_EXECUTABLE": str(script),
                "OHMNI_OUTPUT_DIR": str(tmp_path / "runs"),
                "OHMNI_ENABLE_DOTENV": "0",
            }
            with mock.patch.dict(os.environ, env, clear=True):
                out = io.StringIO()
                err = io.StringIO()
                with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                    code = main(["run", "Build an RC low-pass filter"])
            self.assertEqual(code, 0)
            self.assertIn("status: passed", out.getvalue())
            self.assertEqual(err.getvalue(), "")

    def test_cli_invalid_config_exits_two(self) -> None:
        with mock.patch.dict(
            os.environ,
            {
                "OHMNI_MODEL_BACKEND": "fake",
                "OHMNI_MODEL_PROVIDER": "fake",
                "OHMNI_MODEL": "",
                "OHMNI_ENABLE_DOTENV": "0",
            },
            clear=True,
        ):
            out = io.StringIO()
            err = io.StringIO()
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                code = main(["run", "Build an RC low-pass filter"])
        self.assertEqual(code, 2)
        self.assertIn("Configuration error", err.getvalue())


if __name__ == "__main__":
    unittest.main()
