# 18 — KiCad CLI Exports

## Goal

Expose deterministic export operations without confusing exports with validation.

## Schematic SPICE/netlist export

When a `.kicad_sch` artifact exists, support the documented equivalent of:

```bash
kicad-cli sch export netlist --format spice --output circuit.sp generated.kicad_sch
```

This path is strategically important because downstream ngspice can validate the representation exported by KiCad rather than a separate unrelated text generation path.

Also permit KiCad-native or other netlist formats when useful for diagnostics, but do not make every format a requirement.

## BOM export

Support a wrapper for the documented schematic BOM export command when available:

```bash
kicad-cli sch export bom --output bom.csv generated.kicad_sch
```

Treat BOM as an inspection/reproducibility artifact, not validation.

## PDF export

Support schematic PDF export when available:

```bash
kicad-cli sch export pdf --output schematic.pdf generated.kicad_sch
```

Useful for human review and TCC evidence.

## SVG export

Support schematic SVG export when available. Store per-sheet output predictably.

## Symbol SVG export

Optionally expose `kicad-cli sym export svg` as a diagnostic visualization helper. It is not the primary symbol query API.

## Symbol library upgrade

Optionally wrap `kicad-cli sym upgrade` for explicit user/tooling workflows. Never mutate a user's original library in place by default.

## Requirements

- validate source artifact existence;
- explicit destination paths;
- structured result;
- preserve command and KiCad version metadata;
- no shell execution;
- do not silently overwrite important user files unless caller explicitly permits it.
