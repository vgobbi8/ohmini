# 20 — Circuit Representation and Exporters

## Strategic direction

SPICE text should not remain the long-term canonical representation if Ohmni is expected to produce both simulation and KiCad artifacts.

Target architecture:

```text
CircuitDefinition / Circuit IR
        │
        ├── SpiceCircuitExporter -> .sp
        └── KiCadSchematicExporter -> .kicad_sch
```

## Important scope constraint

Do not force a full IR rewrite in this knowledge slice if it would destabilize the current direct-SPICE prototype.

Instead:

1. introduce the exporter/representation boundary cleanly;
2. preserve `GeneratedCircuit` compatibility;
3. document how the current direct-SPICE path maps into the future representation;
4. only implement a minimal structured circuit model if required by the first KiCad export path.

## Minimal future CircuitDefinition concepts

```text
components
  reference
  value
  selected symbol id
  properties
nets
connections
assumptions
metadata
```

## Determinism principle

Once a structured circuit definition exists, generating SPICE and KiCad artifacts should be deterministic as far as practical. The LLM should reason about design intent and choices, not hand-author opaque output syntax when a deterministic compiler/exporter can perform the transformation.
