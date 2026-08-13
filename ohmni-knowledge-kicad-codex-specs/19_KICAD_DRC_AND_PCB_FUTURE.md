# 19 — KiCad DRC and PCB Integration — Future/Optional

## Scope position

PCB DRC is not a primary requirement of the current TCC circuit-generation slice because DRC requires a meaningful `.kicad_pcb` artifact.

Do not create fake board data merely to run DRC.

## Architecture extension point

The EDA layer should leave room for a future validator equivalent to:

```text
KiCadDrcValidator
```

using the documented KiCad CLI PCB DRC operation and machine-readable reports when supported.

Potential future checks include schematic/PCB parity when a real PCB exists.

## Manufacturing exports

KiCad CLI can support future board/manufacturing exports such as Gerber, drill, position, IPC, ODB++, PDF, SVG, STEP, and other formats depending on KiCad version.

These are future EDA exporters and must not be placed in the Knowledge Engine.
