# 01 — Scope and Boundaries

## In scope

### Knowledge representation

A lightweight, task-oriented representation for:

- entities/concepts;
- facts;
- relations;
- rules;
- constraints;
- formulas;
- procedures;
- operational/tool knowledge.

### Knowledge lifecycle

- manual authoring;
- ingestion;
- deterministic parsing;
- querying;
- provider federation;
- provenance retention;
- explicit unresolved knowledge.

### KiCad integration

- configured symbol library discovery;
- symbol identifier parsing and exact lookup;
- `.kicad_sym` inspection;
- selected symbol metadata/pin extraction;
- `kicad-cli` version detection;
- schematic ERC execution;
- schematic SPICE/netlist export;
- BOM/PDF/SVG export helpers;
- optional symbol SVG export;
- future-compatible schematic export boundary.

## Out of scope for this slice

- live Schematic Editor IPC manipulation;
- automatic graphical placement;
- wire routing in the KiCad UI;
- PCB autorouting;
- manufacturing pipeline as a TCC requirement;
- full ontology/OWL/RDF engine;
- graph database requirement;
- vector database requirement;
- automatic web crawling;
- automatic PDF/datasheet extraction;
- automatic agent-memory promotion to authoritative knowledge;
- LangGraph repair graph;
- a general experiment framework;
- replacement of the existing model abstraction.

## Design stance

Build **small stable contracts** first. Concrete providers are adapters. The core knowledge model must not know whether its items came from Markdown, KiCad, SQL, RAG, MCP, or HTTP.
