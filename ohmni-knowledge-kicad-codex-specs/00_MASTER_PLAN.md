# 00 — Master Plan

## Objective

Implement the first complete Ohmni knowledge boundary and establish deterministic KiCad integration without turning the core application into KiCad plugin code or a RAG-specific application.

The implementation must support this conceptual flow:

```text
Natural-language requirement
        ↓
Circuit Design Pipeline
        ↓
Agent / Generator
   ↙            ↘
KnowledgeEngine  ModelBackend
        ↓
KnowledgeBundle
        ↓
Circuit generation
        ↓
Circuit artifacts
   ↙             ↘
SPICE          KiCad
  ↓              ↓
ngspice       kicad-cli ERC / exports
   ↘             ↙
Validation feedback
        ↓
Future repair loop
```

## Architectural principles

1. `ModelBackend` answers **how AI is executed**.
2. `KnowledgeEngine` answers **what reusable knowledge can be queried**.
3. EDA/tool adapters answer **what deterministic external operations can be performed**.
4. Pipeline state answers **what happened in this specific run**.
5. Agent memory, if introduced later, is only one possible knowledge provider and is not the Knowledge Engine itself.
6. RAG is one retrieval implementation, not the architectural abstraction.
7. KiCad library parsing is a knowledge concern; `kicad-cli` execution is an EDA/tool concern.
8. Never silently infer authoritative engineering facts when a configured authoritative source can be queried.
9. Missing or unresolved knowledge must be representable explicitly.
10. A successful tool execution must never be described as proving more than the tool actually checks.

## Compatibility requirement

The existing direct-SPICE path must remain functional while this slice is introduced.

Do not require the new knowledge system for every old test or CLI command immediately. Introduce a clean seam first, then integrate incrementally.

## Deliverables

- `ohmni.knowledge` domain contracts and models;
- knowledge provider abstraction;
- knowledge engine/federation layer;
- ingestion boundary;
- manual Markdown knowledge provider;
- small curated electronics fixtures;
- KiCad symbol/library provider;
- `ohmni.eda` tool boundary;
- KiCad CLI wrapper;
- KiCad ERC validator;
- KiCad export operations;
- pipeline integration seam;
- artifact/reproducibility conventions;
- unit and fixture-based tests;
- opt-in KiCad CLI integration tests;
- documentation and acceptance report.
