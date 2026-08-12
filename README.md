# Ohmni

Ohmni is a compact circuit-generation prototype built for a capstone project. It takes a natural-language requirement, asks a model to produce a SPICE netlist, and then validates that netlist with ngspice.

The codebase is intentionally small. Model execution, circuit generation, validation, and pipeline orchestration are kept separate so the project can grow without turning into a single hard-to-change block.

## What it does

- generates a SPICE netlist from a plain-English circuit requirement
- supports a local harness backend for coding-agent CLIs such as Antigravity, Codex, Claude Code, and OpenCode
- supports API backends through LangChain chat models
- writes reproducible run artifacts to disk
- validates generated circuits with ngspice

## Requirements

- Python 3.11 or newer
- `ngspice` for real validation runs
- a supported harness CLI such as Antigravity, Codex, Claude Code, or OpenCode if you want to use the harness backend
- API credentials if you want to use a hosted model backend

## Install

From a fresh clone:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

If you are developing locally, you can also run straight from `src/`:

```bash
PYTHONPATH=src .venv/bin/python -m ohmni.cli --help
```

## Configuration

Copy the example environment file and edit it:

```bash
cp .env.example .env
```

The most important settings are:

- `OHMNI_MODEL_BACKEND`
- `OHMNI_MODEL_PROVIDER`
- `OHMNI_MODEL`
- `OHMNI_VALIDATORS`
- `OHMNI_NGSPICE_EXECUTABLE`
- `OHMNI_OUTPUT_DIR`

For the first smoke test, use these settings:

```bash
OHMNI_MODEL_BACKEND=fake
OHMNI_MODEL_PROVIDER=fake
OHMNI_MODEL=fake-model
OHMNI_VALIDATORS=ngspice
OHMNI_NGSPICE_EXECUTABLE=ngspice
OHMNI_OUTPUT_DIR=runs
OHMNI_ENABLE_DOTENV=0
```

### Harness backend

Use this when you want Ohmni to drive a local coding-agent CLI such as `agy`:

```bash
OHMNI_MODEL_BACKEND=harness
OHMNI_MODEL_PROVIDER=agy
OHMNI_MODEL="Gemini 3.6 Flash (Low)"
```

### API backend

Use this when you want Ohmni to call a hosted model provider through LangChain:

```bash
OHMNI_MODEL_BACKEND=api
OHMNI_MODEL_PROVIDER=google
OHMNI_MODEL="gemini-2.5-flash"
GOOGLE_API_KEY=your_api_key
```

## Run

Run Ohmni with a natural-language requirement:

```bash
ohmni run "Create an RC low-pass filter with a 1 kHz cutoff"
```

If you do not want to install the console script yet, you can run the module directly:

```bash
PYTHONPATH=src .venv/bin/python -m ohmni.cli run "Create an RC low-pass filter with a 1 kHz cutoff"
```

The command prints a short summary and writes a run directory under `runs/` by default.

## Smoke test with fake backend

If you want to test the full CLI locally without calling a real model, use the fake backend:

```bash
export OHMNI_MODEL_BACKEND=fake
export OHMNI_MODEL_PROVIDER=fake
export OHMNI_MODEL=fake-model
export OHMNI_MODEL_TIMEOUT_SECONDS=5
export OHMNI_GENERATOR=direct_spice
export OHMNI_VALIDATORS=ngspice
export OHMNI_NGSPICE_EXECUTABLE=ngspice
export OHMNI_OUTPUT_DIR=runs
export OHMNI_ENABLE_DOTENV=0

ohmni run "Create an RC low-pass filter"
```

If `ngspice` is not installed, point `OHMNI_NGSPICE_EXECUTABLE` at a small local stub for the smoke test.

## Testing

Run the test suite with:

```bash
PYTHONPATH=src .venv/bin/python -m unittest discover -s tests
```

The default tests are designed to run without credentials or external network access.

## Repository layout

```text
src/ohmni/        application code
tests/            unit and integration-style tests
.specs/           implementation specs
.tasks/           collapsed task index
```

## Notes

- Direct-SPICE generation remains backend-agnostic.
- The harness backend is implemented through a LangChain `BaseChatModel` infrastructure layer.
- Secrets stay in the environment and are not written into config snapshots or reports.
