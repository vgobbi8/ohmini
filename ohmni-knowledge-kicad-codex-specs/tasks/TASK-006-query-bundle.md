# TASK-006 — KnowledgeQuery and KnowledgeBundle

## Goal

Implement provider-independent query input and normalized bundle output, including explicit unresolved knowledge.

## Read first

- `09_KNOWLEDGE_QUERY_AND_BUNDLE.md`

## Required work

1. Implement query filters without assuming embeddings.
2. Implement `KnowledgeBundle` canonical item storage and typed views.
3. Implement warnings and unresolved requests.
4. Keep query/context metadata serializable.

## Tests

- Exact-query construction.
- Filtered typed views.
- Unresolved serialization.

## Definition of done

- Bundle can represent successful, partial, and unresolved query outcomes.

## Non-goals

- Do not expand beyond this task unless supporting code is strictly necessary.
