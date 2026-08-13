# TASK-018 — Circuit Exporter / IR Seam

## Goal

Prepare the architecture for deterministic SPICE and KiCad artifact generation without forcing a premature full rewrite.

## Read first

- `20_CIRCUIT_REPRESENTATION_AND_EXPORTERS.md`
- `02_CURRENT_REPOSITORY_BASELINE.md`

## Required work

1. Inspect current GeneratedCircuit shape.
2. Introduce the smallest exporter/representation seam that can coexist with direct-SPICE generation.
3. Document future structured CircuitDefinition concepts.
4. Avoid asking the LLM to become coupled to KiCad syntax through this abstraction.
5. Do not remove current netlist fields unless backward-compatible migration is complete.

## Tests

- Existing DirectSpiceGenerator regression.
- New boundary unit tests if implementation adds types.

## Definition of done

- Old direct-SPICE path remains intact.
- Future KiCad exporter has a clear insertion point.

## Non-goals

- Do not expand beyond this task unless supporting code is strictly necessary.
