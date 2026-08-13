# TASK-012 — KiCad Symbol ID and Library Discovery

## Goal

Implement deterministic KiCad symbol identifiers and discovery/resolution of configured symbol libraries.

## Read first

- `14_KICAD_LIBRARY_DISCOVERY.md`
- `15_KICAD_SYMBOL_PROVIDER.md`

## Required work

1. Implement canonical `LibraryNickname:SymbolName` parsing/value object.
2. Parse project symbol library tables needed by fixtures.
3. Resolve configured library paths and selected path substitutions.
4. Allow explicit library path/table configuration for headless tests.
5. Represent missing libraries/path variables as errors or warnings according to policy.

## Tests

- Symbol ID parse/render.
- Project table fixture.
- Path substitution fixture.
- Missing library.

## Definition of done

- Configured nickname can resolve to a library file in tests.

## Non-goals

- Do not expand beyond this task unless supporting code is strictly necessary.
