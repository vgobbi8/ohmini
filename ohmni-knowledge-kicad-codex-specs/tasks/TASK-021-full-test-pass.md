# TASK-021 — Full Test and Regression Pass

## Goal

Validate the entire implemented slice and existing Ohmni behavior.

## Read first

- `26_TESTING_STRATEGY.md`
- `27_ACCEPTANCE_CRITERIA.md`

## Required work

1. Run pure unit tests.
2. Run Markdown/provider tests.
3. Run KiCad fixture tests.
4. Run mocked CLI tests.
5. Run existing repository suite.
6. Run optional real KiCad smoke tests only when explicitly enabled/available.
7. Fix slice-introduced regressions without unrelated cleanup.

## Tests

- All repository-standard tests.

## Definition of done

- Existing direct-SPICE behavior is green.
- New tests cover all implemented boundaries.

## Non-goals

- Do not expand beyond this task unless supporting code is strictly necessary.
