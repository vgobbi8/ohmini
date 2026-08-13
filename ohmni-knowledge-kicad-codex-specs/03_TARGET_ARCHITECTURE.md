# 03 — Target Architecture

## Logical components

```text
                         OHMNI
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
   Model Backend     Knowledge Engine     EDA / Tools
          │                │                │
 how AI executes     what AI knows      what AI can do
          │                │                │
          └────────────────┼────────────────┘
                           ▼
                    Design Agent
                           │
                           ▼
                    Design Pipeline
                           │
                    generate → verify
                         ↑       │
                         └───────┘
```

## Dependency direction

Allowed:

```text
agent/application -> ModelBackend
agent/application -> KnowledgeEngine
application -> EDA contracts
knowledge providers -> knowledge core
KiCad knowledge provider -> KiCad parser + knowledge core
KiCad CLI adapter -> EDA core + subprocess
validators -> EDA adapter + validation core
```

Forbidden:

```text
knowledge core -> LangChain
knowledge core -> KiCad CLI
knowledge core -> vector DB
knowledge core -> HTTP
model core -> KnowledgeEngine implementation
validation core -> KiCad-specific objects
KiCad provider -> agent/model invocation
```

## Architectural rule

A provider must normalize external information into Ohmni knowledge. A tool adapter must normalize execution results into Ohmni tool/validation results. Consumers should not depend on provider-native structures.
