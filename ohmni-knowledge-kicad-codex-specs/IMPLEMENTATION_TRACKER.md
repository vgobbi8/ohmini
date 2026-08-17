# Ohmni Knowledge + KiCad Implementation Tracker

Last verified: 2026-08-16

## Status

Completed through `TASK-005`. The provider-independent knowledge foundation is implemented and the full test suite is green.

## Task checklist

- [x] `TASK-000` — Repository audit
- [x] `TASK-001` — Knowledge package foundation
- [x] `TASK-002` — Knowledge taxonomy and enums
- [x] `TASK-003` — Provenance, authority, and epistemic state
- [x] `TASK-004` — Typed knowledge payloads
- [x] `TASK-005` — KnowledgeItem and serialization
- [ ] `TASK-006` — KnowledgeQuery and KnowledgeBundle
- [ ] `TASK-007` — KnowledgeProvider contract
- [ ] `TASK-008` — KnowledgeEngine federation
- [ ] `TASK-009` — Knowledge ingestion boundary
- [ ] `TASK-010` — Markdown provider
- [ ] `TASK-011` — Initial electronics fixtures
- [ ] `TASK-012` — KiCad library discovery
- [ ] `TASK-013` — KiCad symbol provider
- [ ] `TASK-014` — EDA core and KiCad CLI wrapper
- [ ] `TASK-015` — KiCad ERC validator
- [ ] `TASK-016` — KiCad netlist/SPICE export
- [ ] `TASK-017` — KiCad human-facing exports
- [ ] `TASK-018` — Circuit exporter/IR seam
- [ ] `TASK-019` — Pipeline composition seams
- [ ] `TASK-020` — Run artifacts and reproducibility metadata
- [ ] `TASK-021` — Full test and regression pass
- [ ] `TASK-022` — Documentation and acceptance demonstration
- [ ] `TASK-023` — Future repair-loop architecture note

## Current implementation

The new `src/ohmni/knowledge/` package contains:

- taxonomy enums and constraint strength;
- knowledge-domain errors;
- source, provenance, authority, and epistemic value objects;
- eight typed payloads;
- normalized `KnowledgeItem` and relationship references;
- deterministic dictionary/JSON serialization and validation.

The existing direct-SPICE model/generation/validation/pipeline path remains intact. Fake-ngspice tests use mocked subprocess results, so ordinary tests are OS-agnostic and do not require ngspice or WSL.

## Verification

Run from the repository root:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pytest -q
```

Latest result: `53 passed, 27 subtests passed, 1 deprecation warning`.

## Next action

Implement `TASK-006 — KnowledgeQuery and KnowledgeBundle`. It should add exact/filter query construction, successful/partial/unresolved bundle states, typed bundle views, and deterministic serialization without adding provider or retrieval dependencies.

## Important boundaries

- `ModelBackend` remains model execution only.
- Knowledge core remains independent of LangChain, KiCad CLI, databases, HTTP, vector stores, and agent-memory implementations.
- KiCad library parsing will be a knowledge provider; `kicad-cli` execution will be an EDA adapter.
- Do not implement RAG, live KiCad IPC, PCB automation, or repair-loop orchestration in this slice.
