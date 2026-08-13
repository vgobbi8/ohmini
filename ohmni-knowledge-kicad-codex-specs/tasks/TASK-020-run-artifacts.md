# TASK-020 — Knowledge and KiCad Run Artifacts

## Goal

Extend reproducibility artifacts to record knowledge/tool evidence when those features participate in a run.

## Read first

- `23_ARTIFACTS_AND_REPRODUCIBILITY.md`

## Required work

1. Add serializable knowledge query/bundle/source artifact support.
2. Add KiCad version/command/result artifact support.
3. Use relative paths in reports where appropriate.
4. Sanitize configuration and avoid credentials.
5. Do not require files for features that were not used.

## Tests

- Artifact path tests.
- No-secret snapshot test.
- Knowledge bundle serialization.

## Definition of done

- A grounded/tool-assisted run can be reconstructed from artifacts at a useful level.

## Non-goals

- Do not expand beyond this task unless supporting code is strictly necessary.
