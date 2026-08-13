# TASK-007 — KnowledgeProvider Contract

## Goal

Define the stable provider abstraction and provider result semantics.

## Read first

- `10_PROVIDER_AND_ENGINE.md`
- `03_TARGET_ARCHITECTURE.md`

## Required work

1. Define provider protocol/interface.
2. Decide whether provider returns items directly or a small provider result wrapper with warnings; document choice.
3. Ensure providers expose stable identity/name when useful for traceability.
4. Do not add storage-specific methods to the query contract.

## Tests

- Fake provider contract test.
- Provider substitution test.

## Definition of done

- A fake provider can satisfy consumers with no concrete provider dependency.

## Non-goals

- Do not expand beyond this task unless supporting code is strictly necessary.
