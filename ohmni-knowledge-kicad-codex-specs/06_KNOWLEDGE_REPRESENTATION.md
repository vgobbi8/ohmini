# 06 — Knowledge Representation

## Research-informed stance

The representation is deliberately task-oriented. It does not attempt to exhaustively model electronics or become a universal ontology. It defines the concepts that Ohmni needs to make explicit for design and verification. The same generic representation may later be extended to other knowledge domains by defining domain-relevant entities, relations, rules, procedures, and sources.

## Knowledge families

```text
DECLARATIVE
PROCEDURAL
OPERATIONAL
```

## Knowledge kinds

```text
ENTITY
FACT
RELATION
RULE
CONSTRAINT
FORMULA
PROCEDURE
TOOL
```

## Family defaults

Suggested mapping:

```text
ENTITY       -> DECLARATIVE
FACT         -> DECLARATIVE
RELATION     -> DECLARATIVE
RULE         -> DECLARATIVE
CONSTRAINT   -> DECLARATIVE
FORMULA      -> DECLARATIVE
PROCEDURE    -> PROCEDURAL
TOOL         -> OPERATIONAL
```

Keep the model flexible enough that domain needs can override a default only when there is a clear reason.

## Generic shape

```text
KnowledgeItem
├── id
├── title
├── family
├── kind
├── payload
├── tags
├── applicability
├── epistemic_status
├── relationships
└── provenance
```

## Important distinction

A stored formula is knowledge. Evaluating that formula for a specific design produces **derived pipeline state**, not automatically reusable knowledge.

Likewise, a validator result is evidence about one run, not a permanent fact about electronics.
