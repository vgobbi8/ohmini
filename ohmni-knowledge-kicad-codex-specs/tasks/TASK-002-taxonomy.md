# TASK-002 — Knowledge Taxonomy and Enums

## Goal

Implement knowledge families, kinds, and small semantic enums required by the representation.

## Read first

- `06_KNOWLEDGE_REPRESENTATION.md`
- `07_PROVENANCE_AUTHORITY_EPISTEMICS.md`

## Required work

1. Implement `KnowledgeFamily` and `KnowledgeKind`.
2. Implement constraint strength and other small enums only where used.
3. Define/document default family for each kind.
4. Make enum serialization predictable and stable.

## Tests

- Round-trip enum serialization.
- Default family mapping.
- Invalid enum handling.

## Definition of done

- All eight knowledge kinds are represented.
- No ontology/rule engine introduced.

## Non-goals

- Do not expand beyond this task unless supporting code is strictly necessary.
