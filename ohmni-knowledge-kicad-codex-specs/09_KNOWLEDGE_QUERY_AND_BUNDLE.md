# 09 — Knowledge Query and Knowledge Bundle

## KnowledgeQuery

The query contract must support multiple retrieval modes without prescribing implementation.

Suggested fields:

```text
text
objective
kinds
families
domains
topics
entities
tags
source_types
authority requirements
context
limit
```

All fields except the minimal query intent may be optional.

## Retrieval styles to preserve

### Free-text/semantic

```text
How do I design a first-order RC low-pass filter?
```

### Exact

```text
Amplifier_Operational:LM358
```

### Structured

```text
kind = ENTITY
tag = op-amp
source_type = kicad_symbol_library
```

### Property-oriented

```text
pins for Amplifier_Operational:LM358
```

The contract must not force vector embeddings.

## KnowledgeBundle

Recommended canonical storage:

```text
items: tuple[KnowledgeItem, ...]
warnings: tuple[KnowledgeWarning, ...]
unresolved: tuple[UnresolvedKnowledge, ...]
sources: tuple[KnowledgeSource, ...]
metadata
```

Expose convenient typed views such as `facts`, `procedures`, `constraints`, and `formulas` rather than duplicating storage.

## Unresolved knowledge

An unresolved item should capture:

```text
what was requested
why it is unresolved
providers consulted when known
suggested next source/action optional
```

An empty result is not always equivalent to a resolved negative answer.
