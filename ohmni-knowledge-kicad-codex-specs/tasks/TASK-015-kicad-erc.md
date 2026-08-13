# TASK-015 — KiCad ERC Validator

## Goal

Integrate KiCad schematic ERC as an Ohmni validator with structured issue mapping.

## Read first

- `17_KICAD_ERC_VALIDATOR.md`
- `16_KICAD_CLI_TOOLCHAIN.md`

## Required work

1. Verify target KiCad CLI ERC flags against supported version.
2. Build machine-readable ERC command when supported.
3. Parse ERC report fixture.
4. Map to existing ValidationResult/ValidationIssue.
5. Preserve raw report/command artifacts.
6. Distinguish violations from invocation failures.

## Tests

- No violations.
- Violation result.
- Malformed report.
- Missing executable.
- Opt-in real CLI fixture test if environment supports it.

## Definition of done

- ERC result can participate in existing validator sequence without KiCad-specific pipeline branches.

## Non-goals

- Do not expand beyond this task unless supporting code is strictly necessary.
