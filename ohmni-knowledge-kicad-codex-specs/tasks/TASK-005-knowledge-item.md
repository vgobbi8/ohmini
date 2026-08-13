# TASK-005 — KnowledgeItem and Serialization

## Goal

Implement the normalized universal knowledge item and deterministic serialization/deserialization.

## Read first

- `06_KNOWLEDGE_REPRESENTATION.md`
- `07_PROVENANCE_AUTHORITY_EPISTEMICS.md`
- `08_TYPED_PAYLOADS.md`

## Required work

1. Implement `KnowledgeItem` identity/classification/payload/tags/applicability/relationships/provenance.
2. Validate family/kind/payload consistency.
3. Implement stable dictionary/JSON-friendly serialization.
4. Preserve extension metadata without weakening required validation.
5. Add relationship/reference model only as needed.

## Tests

- Round-trip each kind.
- Mismatched payload/kind failure.
- Provenance retention.

## Definition of done

- KnowledgeItem is provider-agnostic.
- Serialized form is deterministic enough for run artifacts/tests.

## Non-goals

- Do not expand beyond this task unless supporting code is strictly necessary.
