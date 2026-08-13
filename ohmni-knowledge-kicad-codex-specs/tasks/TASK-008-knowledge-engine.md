# TASK-008 — KnowledgeEngine Federation

## Goal

Implement orchestration across multiple knowledge providers with conservative deduplication and provenance preservation.

## Read first

- `10_PROVIDER_AND_ENGINE.md`
- `09_KNOWLEDGE_QUERY_AND_BUNDLE.md`

## Required work

1. Implement engine construction from multiple providers.
2. Call providers deterministically according to documented policy.
3. Aggregate items/warnings/unresolved state.
4. Deduplicate primarily by stable IDs/source identity.
5. Do not merge conflicting source claims silently.

## Tests

- Multiple fake providers.
- Duplicate stable-ID case.
- Conflicting-source preservation.
- Provider failure policy.

## Definition of done

- One query can return a normalized bundle spanning multiple providers.

## Non-goals

- Do not expand beyond this task unless supporting code is strictly necessary.
