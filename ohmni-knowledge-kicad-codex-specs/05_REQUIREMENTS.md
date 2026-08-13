# 05 — System Requirements for This Slice

These requirements are implementation-oriented counterparts to the TCC requirements. They should remain technology-independent where practical.

## Functional requirements

- **RF-K01** — The system shall make reusable technical knowledge available to the design process.
- **RF-K02** — The system shall allow knowledge to originate from multiple independent sources.
- **RF-K03** — The system shall allow manually authored knowledge to be added without modifying agent reasoning code.
- **RF-K04** — The system shall preserve source/provenance references when knowledge is retrieved.
- **RF-K05** — The system shall distinguish different forms of knowledge such as facts, relations, rules, constraints, formulas, procedures, entities, and tool capabilities.
- **RF-K06** — The system shall support knowledge queries that do not assume vector similarity retrieval.
- **RF-K07** — The system shall represent unresolved or unavailable information explicitly.
- **RF-K08** — The system shall query configured KiCad symbol libraries and expose normalized symbol knowledge.
- **RF-K09** — The system shall identify configured KiCad symbols using stable library/symbol identifiers.
- **RF-K10** — The system shall expose symbol pin information when available from the configured KiCad symbol definition.
- **RF-E01** — The system shall execute supported KiCad CLI operations through a deterministic adapter.
- **RF-E02** — The system shall run KiCad schematic ERC and normalize the outcome to Ohmni validation results.
- **RF-E03** — The system shall support exporting KiCad schematic artifacts to SPICE/netlist representations when a schematic artifact exists.
- **RF-E04** — The system shall support selected non-validation exports such as BOM, PDF, and SVG when useful for reproducibility or inspection.

## Non-functional requirements

- **RNF-K01 — Modularity:** knowledge core must be independent from retrieval/storage technology.
- **RNF-K02 — Extensibility:** new providers must be addable without changing consumers.
- **RNF-K03 — Traceability:** retrieved knowledge should retain source identity whenever available.
- **RNF-K04 — Epistemic transparency:** assumptions, derived information, recommendations, retrieved facts, and unknowns must not be silently conflated.
- **RNF-K05 — Determinism where possible:** exact identifier and library lookups should use deterministic lookup rather than semantic retrieval.
- **RNF-E01 — Tool isolation:** KiCad-specific execution details must remain outside validation and pipeline core contracts.
- **RNF-E02 — Reproducibility:** tool version, command, exit code, and relevant artifacts should be recordable per run.
- **RNF-E03 — Backward compatibility:** existing direct-SPICE generation must remain functional.
