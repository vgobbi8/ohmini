# TASK-009 — Knowledge Ingestion Boundary

## Goal

Separate writing/importing knowledge from querying it and define a small ingestion abstraction.

## Read first

- `11_INGESTION_AND_MARKDOWN.md`
- `10_PROVIDER_AND_ENGINE.md`

## Required work

1. Define ingestion request/result contracts only as needed.
2. Keep ingestion separate from KnowledgeEngine query responsibilities.
3. Support manual/file-based provider implementation next.
4. Do not add agent auto-learning.

## Tests

- Fake ingestion implementation.
- Invalid item handling.

## Definition of done

- Consumers can ingest without depending on agent/model code.

## Non-goals

- Do not expand beyond this task unless supporting code is strictly necessary.
