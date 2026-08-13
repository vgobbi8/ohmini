# 15 — KiCad Symbol Knowledge Provider

## Goal

Expose configured KiCad symbol definitions as normalized Ohmni knowledge.

## Input formats

Primary source: modern `.kicad_sym` libraries and the library tables that reference them.

Do not use `kicad-cli` as the primary symbol metadata query API. Parse/query library files deterministically.

## Minimum extracted symbol data

Where present, extract:

```text
library nickname
symbol name
canonical identifier
extends/derived symbol relationship
reference prefix
value/name properties
description
keywords/tags
units
pins
pin numbers
pin names
pin electrical types
fields/properties
footprint filters/references when represented
```

Do not invent fields absent from the source.

## Normalization

A symbol should produce at minimum an `ENTITY` knowledge item.

Related facts/relations may be either:

- embedded in the entity payload; or
- emitted as additional `FACT`/`RELATION` items.

Choose one consistent approach and document it.

## Authority

Suggested provenance:

```text
source_type = kicad_symbol_library
authority = AUTHORITATIVE
authority_scope = kicad_symbol_definition
```

This authority does not extend to manufacturer electrical ratings unless such data is explicitly sourced separately.

## Search modes

Support:

- exact canonical ID;
- exact symbol name within library;
- library filtering;
- simple name/keyword textual search;
- optional pin/property filters only if straightforward.

Do not add vector search.

## Anti-hallucination rule

When exact configured symbol/pin data is available, downstream agent instructions should prefer retrieved pin definitions over LLM recall.
