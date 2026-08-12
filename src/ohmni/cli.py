from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from ohmni.config.settings import Settings, SettingsError
from ohmni.generation.direct_spice import DirectSpiceGenerator
from ohmni.model.contracts import FakeModelBackend, ModelResponse
from ohmni.model.errors import ModelError
from ohmni.pipeline.circuit_pipeline import CircuitPipeline
from ohmni.validation.ngspice import NgSpiceValidator


def _fake_response(request) -> ModelResponse:
    requirement = request.prompt.split("Requirement:", 1)[-1].strip()
    return ModelResponse(
        content=(
            "* fake generated netlist\n"
            "V1 in 0 DC 5\n"
            "R1 in out 1k\n"
            "C1 out 0 1u\n"
            ".tran 1ms 10ms\n"
            ".end\n"
        ),
        metadata={"requirement": requirement, "fake": True},
    )


def _build_generator(settings: Settings):
    if settings.model_backend == "fake":
        backend = FakeModelBackend(_fake_response)
    else:
        # The harness and API backends are implemented as optional adapters.
        from ohmni.model.backends.factory import build_model_backend

        backend = build_model_backend(settings)
    return DirectSpiceGenerator(backend=backend)


def _build_validators(settings: Settings):
    validators = []
    for name in settings.validator_names:
        if name == "ngspice":
            validators.append(NgSpiceValidator())
    return validators


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="ohmni")
    subparsers = parser.add_subparsers(dest="command", required=True)
    run_parser = subparsers.add_parser("run", help="Run the Ohmni pipeline")
    run_parser.add_argument("requirement", help="Natural-language circuit requirement")
    run_parser.add_argument("--show-config", action="store_true", help="Print sanitized configuration before running")

    args = parser.parse_args(argv)

    if args.command != "run":
        parser.error("Only the run command is implemented")

    try:
        settings = Settings.from_env()
    except SettingsError as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        return 2

    if args.show_config:
        print(json.dumps(settings.config_snapshot(), indent=2, sort_keys=True))

    try:
        generator = _build_generator(settings)
        validators = _build_validators(settings)
        pipeline = CircuitPipeline(
            generator=generator,
            validators=validators,
            output_dir=settings.output_dir,
            config_snapshot=settings.config_snapshot(),
            ngspice_executable=settings.ngspice_executable,
            model_identity={
                "backend": settings.model_backend,
                "provider": settings.model_provider,
                "model": settings.model_name,
            },
        )
        result = pipeline.run(args.requirement)
    except ModelError as exc:
        print(f"Model error: {exc}", file=sys.stderr)
        return 1

    print(f"run_id: {result.run_id}")
    print(f"status: {result.status}")
    print(f"report: {result.report_path}")
    if result.error_message:
        print(f"error: {result.error_message}")
    return 0 if result.status == "passed" else 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
