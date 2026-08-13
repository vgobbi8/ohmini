# TASK-019 — Pipeline Composition Seams

## Goal

Expose KnowledgeEngine and EDA services through composition without rewriting agent orchestration yet.

## Read first

- `21_PIPELINE_INTEGRATION.md`
- `25_CONFIGURATION.md`

## Required work

1. Add configuration/composition for implemented knowledge providers.
2. Add configuration/composition for KiCad CLI adapter.
3. Make a future design/generator consumer able to request a KnowledgeBundle.
4. Keep ModelBackend independent from knowledge.
5. Avoid forcing knowledge mocks into unrelated tests.

## Tests

- Settings tests.
- Composition with fake providers.
- Existing CLI regression.

## Definition of done

- Services can be constructed cleanly from typed settings.

## Non-goals

- Do not expand beyond this task unless supporting code is strictly necessary.
