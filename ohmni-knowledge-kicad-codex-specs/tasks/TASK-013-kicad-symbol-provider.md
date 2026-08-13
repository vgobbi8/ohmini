# TASK-013 — KiCad Symbol Parser and Knowledge Provider

## Goal

Parse `.kicad_sym` data needed by Ohmni and expose it through `KnowledgeProvider`.

## Read first

- `15_KICAD_SYMBOL_PROVIDER.md`
- `07_PROVENANCE_AUTHORITY_EPISTEMICS.md`

## Required work

1. Implement/choose a robust minimal S-expression parser strategy.
2. Extract required symbol properties and pins from fixtures.
3. Handle derived/inherited symbols as far as required by real fixture cases; document limitations.
4. Normalize to entity/fact/relation knowledge consistently.
5. Set KiCad-specific source provenance and authority scope.
6. Support exact canonical ID and simple textual search.

## Tests

- Device:R-style fixture.
- LM358-like multi-unit fixture if feasible.
- Pin number/name/type extraction.
- Missing symbol unresolved case.

## Definition of done

- Agent-facing result contains normalized knowledge, not parser-native structures.

## Non-goals

- No vector search.
- No live KiCad IPC.
