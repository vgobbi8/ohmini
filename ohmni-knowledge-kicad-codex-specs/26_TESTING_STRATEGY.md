# 26 — Testing Strategy

## Layer 1 — Pure domain tests

Must run with no network and no KiCad installation:

- enum/taxonomy behavior;
- typed payload validation;
- knowledge item validation;
- provenance serialization;
- query filtering;
- bundle typed views;
- unresolved knowledge;
- engine federation;
- conservative deduplication;
- ingestion validation.

## Layer 2 — File-provider fixture tests

Use temporary/committed tiny fixtures:

- Markdown frontmatter parsing;
- exact ID lookup;
- tag/kind filtering;
- malformed document handling;
- source path provenance.

## Layer 3 — KiCad library fixture tests

Use committed tiny `.kicad_sym` and `sym-lib-table` fixtures:

- symbol ID parsing;
- library discovery;
- path substitution;
- exact symbol lookup;
- pin extraction;
- symbol property extraction;
- authority/provenance mapping.

These tests must not require a system KiCad install.

## Layer 4 — KiCad CLI command tests

Mock process execution for:

- version;
- ERC;
- netlist/SPICE export;
- BOM;
- PDF;
- SVG;
- timeout;
- executable missing.

## Layer 5 — Opt-in real tool tests

If `kicad-cli` exists and integration tests are explicitly enabled:

- run version;
- run ERC on a known fixture;
- export a known artifact.

Skip rather than fail ordinary unit test runs when KiCad is intentionally unavailable.

## Regression requirement

Run the existing repository test suite after the slice. Existing direct-SPICE tests must remain green unless a documented intentional behavior change was made.
