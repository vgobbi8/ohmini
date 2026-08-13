# Task Index

Execute tasks in order unless a later task is explicitly selected after its dependencies are satisfied.

| Task | Goal | Main dependencies |
|---|---|---|
| TASK-000 | Audit current repository | none |
| TASK-001 | Create knowledge package/core skeleton | 000 |
| TASK-002 | Implement taxonomy/enums | 001 |
| TASK-003 | Implement provenance/authority/epistemics | 002 |
| TASK-004 | Implement typed payloads | 002–003 |
| TASK-005 | Implement KnowledgeItem + serialization | 003–004 |
| TASK-006 | Implement KnowledgeQuery + KnowledgeBundle | 005 |
| TASK-007 | Implement KnowledgeProvider contract | 006 |
| TASK-008 | Implement KnowledgeEngine federation | 007 |
| TASK-009 | Implement ingestion boundary | 005–007 |
| TASK-010 | Implement Markdown provider | 009 |
| TASK-011 | Add initial electronics fixtures | 010 |
| TASK-012 | Implement KiCad symbol ID + library discovery | 005–007 |
| TASK-013 | Implement KiCad symbol parser/provider | 012 |
| TASK-014 | Create EDA core + KiCad CLI wrapper | 000 |
| TASK-015 | Implement KiCad ERC validator | 014 |
| TASK-016 | Implement KiCad netlist/SPICE export | 014 |
| TASK-017 | Implement BOM/PDF/SVG export helpers | 014 |
| TASK-018 | Establish circuit-exporter/IR seam | 000,016 |
| TASK-019 | Integrate knowledge/tool seams with pipeline composition | 008,013–018 |
| TASK-020 | Extend run artifacts/reproducibility metadata | 019 |
| TASK-021 | Full testing/regression pass | all implementation tasks |
| TASK-022 | Documentation + acceptance demo | 021 |
| TASK-023 | Future repair-loop architecture note only | 022 |

Do not automatically implement future RAG, MCP, HTTP, database, datasheet extraction, live KiCad IPC, or LangGraph work.
