# TASK-003 — Provenance, Authority, and Epistemic State

## Goal

Implement source/provenance value objects plus scoped authority and epistemic status.

## Read first

- `07_PROVENANCE_AUTHORITY_EPISTEMICS.md`
- `24_ERROR_MODEL.md`

## Required work

1. Implement source identity/type model.
2. Implement authority level and `authority_scope`.
3. Implement epistemic status.
4. Support provider/source metadata without exposing secrets.
5. Provide serialization helpers consistent with repository style.

## Tests

- Source round trip.
- Authority scope retention.
- Agent/candidate status case.

## Definition of done

- A source can be traced independently of provider implementation.
- Authority is explicitly scoped.

## Non-goals

- Do not expand beyond this task unless supporting code is strictly necessary.
