# TASK-000 Audit — Live Repository Reconciliation

## Audit date

2026-08-13

## Environment and baseline

- OS/shell: Windows PowerShell
- Python: 3.14.2 (`D:\scoop\apps\python\current\python.exe`)
- Packaging: `pyproject.toml` with setuptools backend
- Test runner: pytest 9.1.1 in the project `.venv`
- Baseline command: `.\.venv\Scripts\python.exe -m pytest -q`
- Baseline result: 27 passed, 6 failed
- Focused non-subprocess regression: 25 passed

The six failures occur in existing fake-ngspice/pipeline tests because the test helper creates a Unix-style executable that Windows cannot launch (`WinError 193`). This is an existing platform/test-fixture issue, not a knowledge or KiCad change. It should be addressed before claiming a fully green baseline.

## Current package map

```text
src/ohmni/
├── config/          Settings parsing, validation, dotenv support
├── model/           ModelRequest/Response, ModelBackend, fake/harness/API adapters
├── generation/      CircuitGenerationRequest, GeneratedCircuit, DirectSpiceGenerator
├── validation/      CircuitValidator, ValidationResult, NgSpiceValidator
├── pipeline/        CircuitPipeline, RunArtifacts, reports and persisted outputs
├── _vendor/         Small vendored agent-harness boundary
└── cli.py           Settings → backend → generator → validators → pipeline composition
```

Tests currently cover model contracts/backends, direct-SPICE generation, settings, ngspice validation, and pipeline/CLI behavior. No existing knowledge, EDA, KiCad parser, KiCad provider, or exporter implementation was found.

## Contract mapping

| Dossier concept | Current equivalent or proposed location | Compatibility decision |
|---|---|---|
| `ModelBackend` | `ohmni.model.contracts.ModelBackend` | Preserve unchanged. |
| model execution | `ohmni.model.backends`, `ohmni.model.infrastructure` | Keep independent of knowledge and EDA. |
| circuit generation | `ohmni.generation.contracts`, `DirectSpiceGenerator` | Preserve direct-SPICE path. |
| circuit validation | `ohmni.validation.contracts.CircuitValidator` | Extend through generic contracts only. |
| run state/artifacts | `ohmni.pipeline.artifacts`, `CircuitPipeline` | Extend incrementally for knowledge/tool evidence. |
| composition root | `ohmni.cli._build_generator`, `_build_validators` | Add factories/seams without forcing existing CLI behavior. |
| knowledge domain | new `src/ohmni/knowledge/` | Provider-independent dataclasses/protocols. |
| KiCad knowledge | new `src/ohmni/knowledge/providers/kicad/` or equivalent | Parse libraries into normalized knowledge items. |
| EDA/tool boundary | new `src/ohmni/eda/` | Keep subprocess and KiCad details outside validation core. |
| KiCad CLI | new EDA adapter | Use argument lists, `shell=False`, explicit errors/results. |
| KiCad validation | new validator using existing `ValidationResult` | ERC violations differ from invocation/tool errors. |
| circuit exporter seam | new exporter/IR contracts near generation or EDA boundary | Do not rewrite `DirectSpiceGenerator` prematurely. |

## Naming and dependency risks

- `provider` already means model provider in settings and model metadata; knowledge providers must remain namespaced and must not reuse model-provider settings.
- `validation` already owns generic validation contracts; KiCad ERC should adapt to those contracts rather than introduce KiCad objects into them.
- `RunArtifacts` currently writes a flat-ish generation/validation layout; knowledge and KiCad evidence should be added incrementally.
- Existing `NgSpiceValidator` writes subprocess artifacts directly and currently exposes a Windows fake-executable test limitation. New KiCad process execution should use a reusable, platform-aware EDA runner rather than copying this limitation.
- No YAML/frontmatter parser is currently declared. Markdown ingestion should either use a minimal supported format or add a narrowly scoped dependency during its task.

## Proposed implementation mapping

```text
TASK-001..006  src/ohmni/knowledge/core domain contracts and serialization
TASK-007..008  src/ohmni/knowledge provider protocol and engine
TASK-009..011  src/ohmni/knowledge ingestion, Markdown provider, fixtures
TASK-012..013  src/ohmni/knowledge/providers/kicad library discovery/provider
TASK-014..017  src/ohmni/eda contracts, process runner, KiCad CLI/export/ ERC adapters
TASK-018        circuit/exporter seam with minimal impact to generation
TASK-019        composition and pipeline integration
TASK-020        pipeline artifact/reproducibility extensions
TASK-021..023  regression, acceptance documentation, future repair-loop note
```

## Audit conclusion

The repository matches the expected baseline architecture. The dossier can be implemented additively. The first production code should be the provider-independent knowledge foundation; no existing concept needs to be renamed or removed. KiCad knowledge and KiCad CLI work can proceed as separate branches after the foundation audit, joining at pipeline composition.

## Recommended next task

`TASK-001 — Knowledge Package Foundation`.
