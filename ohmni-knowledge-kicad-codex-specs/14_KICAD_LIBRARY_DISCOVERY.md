# 14 — KiCad Library Discovery

## Goal

Discover the symbol libraries actually configured for the relevant KiCad environment/project without hardcoding the complete library catalog into Ohmni.

## Sources

Support at least the concepts of:

- project `sym-lib-table`;
- configured global symbol library table when available/configured;
- environment/path substitutions such as project-relative variables;
- direct configured library paths for tests and headless execution.

## Requirements

- deterministic parsing;
- preserve library nickname;
- resolve a library nickname to a source file/path when possible;
- do not silently ignore missing configured libraries;
- produce warnings for unresolved path substitutions;
- allow explicit configuration overrides for tests and CI;
- avoid hardcoding OS-specific KiCad installation paths in knowledge core.

## Symbol identifier

Introduce or reuse a tiny value object representing:

```text
LibraryNickname:SymbolName
```

Examples:

```text
Device:R
Device:C
Amplifier_Operational:LM358
```

It should parse, validate, and render the canonical form.

## Tests

Use temporary fixture directories and tiny library tables. Tests must not depend on the user's real KiCad installation.
