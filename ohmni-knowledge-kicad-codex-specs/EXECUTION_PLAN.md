# Execution Plan — Ohmni Knowledge + KiCad Slice

## Purpose

Turn the dossier's task list into demonstrable vertical slices. The task IDs remain the source of implementation detail; this document defines sequencing, integration gates, and the definition of done for each slice.

## Execution rules

1. Start with `TASK-000` and reconcile the dossier with repository reality.
2. Keep the existing direct-SPICE path green throughout the work.
3. Every slice ends with focused tests and a small demonstration or fixture.
4. Do not merge future-scope infrastructure: RAG, vector databases, MCP/HTTP providers, live KiCad IPC, PCB automation, or repair-loop orchestration.
5. Keep knowledge parsing and KiCad CLI execution as separate boundaries.
6. Record deviations from the dossier in the task result and update the traceability matrix when contracts settle.

## Slice map

### Slice 0 — Baseline and workspace contract

Tasks: `TASK-000`

Outcome: a repository audit, file mapping, dependency notes, and a runnable baseline test command.

Gate:

- current package layout and existing contracts are documented;
- test runner/environment status is known;
- no implementation changes beyond audit notes.

Current observation: `pytest` is not installed in the current environment, so the baseline command must be established before relying on test results.

### Slice 1 — Knowledge domain foundation

Tasks: `TASK-001` → `TASK-006`

Outcome: provider-independent knowledge objects that can represent all eight knowledge kinds, provenance, epistemic state, typed payloads, queries, bundles, and unresolved results.

Suggested internal checkpoints:

- package imports and taxonomy;
- provenance/authority/epistemics;
- payloads and `KnowledgeItem` round trips;
- query filtering and typed bundle views.

Gate: pure domain tests pass without filesystem, network, KiCad, or model dependencies.

### Slice 2 — Provider contracts and manual knowledge

Tasks: `TASK-007` → `TASK-011`

Outcome: a federatable provider contract, ingestion boundary, Markdown provider, and curated electronics fixtures.

Demo: add a valid Markdown knowledge file and retrieve it through `KnowledgeEngine` without changing Python code.

Gate: fixture tests prove exact ID lookup, kind/tag filtering, malformed input handling, provenance retention, and unresolved queries.

### Slice 3 — KiCad as a knowledge source

Tasks: `TASK-012` → `TASK-013`

Outcome: deterministic library discovery and normalized symbol knowledge, including symbol identifiers, properties, units, and pins.

Demo: resolve `Device:R` (and an optional multi-unit operational-amplifier fixture) from a test `sym-lib-table` and `.kicad_sym` file.

Gate: no KiCad installation is required; provider results contain normalized `KnowledgeItem` objects and KiCad provenance, never parser-native structures.

### Slice 4 — Deterministic KiCad tool boundary

Tasks: `TASK-014` → `TASK-017`

Outcome: EDA contracts and a safe KiCad CLI adapter for version, ERC, SPICE/netlist, BOM, PDF, and SVG operations.

Suggested internal checkpoints:

- process execution/error model and version;
- ERC normalized to `ValidationResult`;
- SPICE/netlist export;
- inspection/document exports.

Gate: mocked subprocess tests cover missing executable, timeout, non-zero exit, command construction, and artifact paths. Exports must not be reported as validation.

### Slice 5 — Circuit and pipeline seams

Tasks: `TASK-018` → `TASK-019`

Outcome: a future-compatible circuit exporter/IR seam and composition factories that can construct knowledge and EDA services without coupling model contracts to either implementation.

Demo: construct the pipeline with fake knowledge providers and optional KiCad services while the existing direct-SPICE generator still runs unchanged.

Gate: existing CLI/pipeline tests remain compatible; knowledge usage can expose query, returned item IDs, source IDs, warnings, and unresolved items.

### Slice 6 — Reproducible grounded execution

Tasks: `TASK-020`

Outcome: run artifacts record knowledge inputs, provider/source identities, tool versions/commands, outputs, validation, and sanitized configuration.

Demo: one grounded/tool-assisted run can be reconstructed from its run directory without secrets.

Gate: artifact layout and no-secret tests pass; first implementation may extend the existing `RunArtifacts` layout rather than rewrite it.

### Slice 7 — Verification, acceptance, and boundary documentation

Tasks: `TASK-021` → `TASK-023`

Outcome: full regression pass, acceptance demonstrations, traceability updates, and a documentation-only note for the future repair loop.

Gate: all available tests pass; optional real KiCad tests skip cleanly when KiCad is absent; acceptance evidence does not overclaim ERC/SPICE correctness.

## Dependency and parallelization plan

After Slice 0, Slice 1 is the critical path for knowledge work. Slice 4 can proceed in parallel with Slices 1–3 after its own audit dependency is satisfied. Slice 5 waits for both branches. Slice 6 waits for Slice 5, and Slice 7 is final.

```text
Slice 0
  ├── Slice 1 → Slice 2 → Slice 3 ─┐
  └── Slice 4 ─────────────────────┤→ Slice 5 → Slice 6 → Slice 7
```

Within a slice, keep commits/tasks small and ordered. Do not parallelize edits to shared contracts unless the contract is agreed first.

## Recommended implementation order

1. Establish the test environment and complete `TASK-000`.
2. Execute Slices 1 and 2 as the first end-to-end knowledge milestone.
3. Execute Slice 3 and verify KiCad knowledge independently of KiCad CLI.
4. Execute Slice 4 independently with mocked subprocesses.
5. Join both branches in Slice 5, then add artifact evidence in Slice 6.
6. Finish with the complete test/acceptance/documentation pass.

## Global definition of done

- direct-SPICE generation and existing behavior remain functional;
- all implemented contracts have deterministic serialization and focused tests;
- missing knowledge, unavailable tools, timeouts, and validation violations remain distinguishable;
- no provider or KiCad dependency leaks into model, generation, or validation core contracts;
- traceability matrix and acceptance documentation identify evidence for each requirement;
- limitations and deviations are explicitly recorded.
