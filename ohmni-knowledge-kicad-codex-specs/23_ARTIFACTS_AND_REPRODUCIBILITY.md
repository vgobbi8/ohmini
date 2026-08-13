# 23 — Artifacts and Reproducibility

## Goal

Every real execution should leave enough evidence to understand what knowledge, model, tools, and artifacts participated in the run.

## Target run layout

```text
runs/<run-id>/
├── request.json
├── config.json
├── knowledge/
│   ├── query.json
│   ├── bundle.json
│   └── sources.json
├── attempts/
│   └── 001/
│       ├── model/
│       ├── circuit/
│       ├── kicad/
│       │   ├── generated.kicad_sch
│       │   ├── schematic.pdf
│       │   ├── schematic-svg/
│       │   └── bom.csv
│       └── validation/
│           ├── kicad-erc/
│           └── ngspice/
└── report.json
```

The first implementation may adapt the existing layout incrementally rather than rewrite it wholesale.

## Record where applicable

- run ID;
- timestamp;
- model backend/provider/model;
- generator strategy;
- knowledge provider identities;
- knowledge item/source IDs actually returned;
- KiCad executable/version;
- ngspice executable/version when available;
- commands executed;
- validator results;
- artifact relative paths;
- errors/timeouts;
- sanitized configuration.

## Secrets

Never write API keys, tokens, passwords, cookies, or provider credentials to run artifacts.
