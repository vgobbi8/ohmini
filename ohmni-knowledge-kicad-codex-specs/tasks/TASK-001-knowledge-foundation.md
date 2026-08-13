# TASK-001 — Knowledge Package Foundation

## Goal

Create the `ohmni.knowledge` package and the minimum error/core module skeleton without provider dependencies.

## Read first

- `01_SCOPE_AND_BOUNDARIES.md`
- `03_TARGET_ARCHITECTURE.md`
- `30_CODING_CONVENTIONS.md`

## Required work

1. Create/adapt package structure for knowledge core.
2. Introduce only minimal shared errors/base protocols needed by subsequent tasks.
3. Keep package imports stable and avoid circular dependencies.
4. Do not import LangChain, KiCad, vector stores, databases, or HTTP libraries.

## Tests

- Import smoke tests.
- Existing regression tests.

## Definition of done

- Package imports cleanly.
- No provider dependency leaks into core.

## Non-goals

- Do not expand beyond this task unless supporting code is strictly necessary.
