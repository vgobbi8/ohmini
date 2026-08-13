# 21 — Pipeline Integration Seam

## Goal

Make knowledge available to future agent/design orchestration without immediately rewriting the whole pipeline.

## Desired future context

```text
DesignContext
├── requirement
├── pipeline state
├── KnowledgeBundle
├── assumptions
├── previous validation results
└── attempt metadata
```

Do not add LangGraph merely to carry this state.

## Current-slice integration

At minimum:

- provide a composition/factory seam that can construct a `KnowledgeEngine`;
- make it possible for a future generator/agent to request a `KnowledgeBundle`;
- avoid forcing existing `DirectSpiceGenerator` tests to mock knowledge unless knowledge is truly required;
- do not couple `ModelBackend` to `KnowledgeEngine`.

## Traceability

When knowledge is used in a design attempt, the architecture should make it possible to record:

```text
query
returned item IDs
source IDs
warnings
unresolved items
```

This is especially important for TCC experiments comparing grounded and ungrounded behavior.
