# TASK-016 — KiCad Netlist/SPICE Export

## Goal

Wrap KiCad schematic netlist export, prioritizing SPICE for downstream ngspice validation.

## Read first

- `18_KICAD_EXPORTS.md`
- `20_CIRCUIT_REPRESENTATION_AND_EXPORTERS.md`

## Required work

1. Verify supported `sch export netlist` formats for repository target KiCad version.
2. Implement explicit source/destination path command builder.
3. Support SPICE format first.
4. Return structured artifact/result.
5. Add a seam allowing exported SPICE to be passed to existing ngspice validation later.

## Tests

- Command construction.
- Missing source.
- Successful mocked export.
- Non-zero command.

## Definition of done

- No direct shell concatenation.
- Export is not reported as validation.

## Non-goals

- Do not expand beyond this task unless supporting code is strictly necessary.
