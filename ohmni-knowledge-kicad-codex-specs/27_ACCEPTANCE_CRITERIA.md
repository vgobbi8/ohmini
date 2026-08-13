# 27 — End-to-End Acceptance Criteria

The slice is accepted when the following demonstrations are possible.

## A — Manual knowledge

```text
manually authored Markdown
        ↓
MarkdownKnowledgeProvider
        ↓
KnowledgeEngine
        ↓
KnowledgeBundle
        ↓
typed knowledge with provenance
```

Adding a new valid Markdown knowledge file must not require Python agent changes.

## B — KiCad knowledge

```text
sym-lib-table + .kicad_sym
        ↓
KiCadSymbolKnowledgeProvider
        ↓
exact Device:R / LM358-style lookup
        ↓
normalized entity/pin metadata
        ↓
provenance identifies KiCad source
```

## C — KiCad toolchain

```text
.kicad_sch
    ↓
KiCad CLI wrapper
    ↓
ERC
    ↓
Ohmni ValidationResult
```

When the target KiCad CLI supports it:

```text
.kicad_sch
    ↓
kicad-cli schematic netlist/SPICE export
    ↓
.sp
    ↓
existing ngspice validator
```

## D — Reproducibility

A run/tool result can record:

- knowledge sources/items used;
- KiCad version;
- executed command metadata;
- output artifact paths;
- normalized validation result.

## E — Backward compatibility

The existing direct-SPICE CLI/test path still works.
