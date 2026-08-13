# Codex — Start Here

Repository: `vgobbi8/ohmni`

You are implementing a new architecture slice for the Ohmni TCC prototype.

## First action

Execute `TASK-000-repo-audit.md` before creating new abstractions.

## Architectural invariant

Do not collapse these concepts:

```text
ModelBackend     = how AI is executed
KnowledgeEngine  = what reusable knowledge can be consulted
EDA adapters     = deterministic engineering/tool operations
Pipeline state   = evidence from the current run
```

## KiCad invariant

```text
.kicad_sym / sym-lib-table parsing
    -> knowledge provider

kicad-cli
    -> EDA/tool adapter
```

Live KiCad Schematic Editor IPC is intentionally outside the current implementation scope.

## Implementation style

Prefer small protocols and dataclasses. Keep the core independent of provider libraries. Preserve the current direct-SPICE path. Add one useful implementation at a time and keep tests deterministic.
