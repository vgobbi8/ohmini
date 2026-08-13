# TASK-004 — Typed Knowledge Payloads

## Goal

Implement lightweight typed payloads for entity, fact, relation, rule, constraint, formula, procedure, and tool knowledge.

## Read first

- `08_TYPED_PAYLOADS.md`
- `06_KNOWLEDGE_REPRESENTATION.md`

## Required work

1. Implement one payload type per knowledge kind or a comparably typed design.
2. Validate minimal required fields.
3. Keep structures serializable.
4. Model procedure steps explicitly and in order.
5. Model formula variables/applicability without evaluating formulas here.
6. Do not add an inference engine.

## Tests

- Construct each payload.
- Invalid minimal-field cases.
- Serialization.

## Definition of done

- Payloads remain simple domain objects.
- No arbitrary provider-specific objects are required.

## Non-goals

- Do not expand beyond this task unless supporting code is strictly necessary.
