# TASK-017 — KiCad BOM, PDF, SVG and Diagnostic Exports

## Goal

Implement selected reproducibility/human-inspection exports through the KiCad CLI wrapper.

## Read first

- `18_KICAD_EXPORTS.md`

## Required work

1. Verify target-version command shapes.
2. Implement BOM export helper.
3. Implement schematic PDF export helper.
4. Implement schematic SVG export helper.
5. Optionally implement symbol SVG export helper if cleanly supported.
6. Do not automatically overwrite user-owned files.

## Tests

- Command builder tests for each supported export.
- Artifact path behavior.

## Definition of done

- Exports are exposed as tool operations and labeled non-validation artifacts.

## Non-goals

- Do not expand beyond this task unless supporting code is strictly necessary.
