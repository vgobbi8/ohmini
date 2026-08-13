# TASK-014 — EDA Core and KiCad CLI Wrapper

## Goal

Introduce the EDA/tool boundary and a safe reusable `kicad-cli` process adapter.

## Read first

- `13_EDA_BOUNDARY.md`
- `16_KICAD_CLI_TOOLCHAIN.md`
- `30_CODING_CONVENTIONS.md`

## Required work

1. Create/adapt EDA core result/error types.
2. Implement configurable KiCad CLI executable.
3. Implement version detection.
4. Implement generic safe command execution with timeout/capture.
5. Return structured command results suitable for artifacts.
6. Do not interpret validation semantics in the generic runner.

## Tests

- Version command mock.
- Executable missing.
- Timeout.
- Non-zero command result.

## Definition of done

- All execution uses `shell=False`.
- No KnowledgeEngine dependency.

## Non-goals

- Do not expand beyond this task unless supporting code is strictly necessary.
