# 13 — EDA Boundary

## Purpose

Separate external deterministic engineering tools from the Knowledge Engine.

Suggested package:

```text
src/ohmni/eda/
├── __init__.py
├── contracts.py
├── errors.py
└── kicad/
```

## Concepts

A minimal EDA command result may contain:

```text
command
exit_code
stdout
stderr
duration
artifacts
metadata
```

Do not force this exact class if the repository already has an appropriate process/tool result abstraction.

## Important distinction

```text
KiCadSymbolKnowledgeProvider
    reads/normalizes KiCad library information

KiCadToolchain / KiCadCli
    executes kicad-cli operations
```

They may share low-level configuration helpers but must not be the same service.
