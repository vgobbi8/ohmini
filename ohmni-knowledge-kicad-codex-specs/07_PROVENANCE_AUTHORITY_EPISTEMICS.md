# 07 — Provenance, Authority, and Epistemic State

## Goal

Avoid treating every retrieved item as equally trustworthy or equally certain.

## Suggested epistemic statuses

```text
ASSERTED
RETRIEVED
DERIVED
ASSUMED
RECOMMENDED
CANDIDATE
UNKNOWN
```

Do not force every item to use every status. Prefer a small enum plus optional explanatory metadata.

## Suggested authority levels

A simple vocabulary is enough:

```text
AUTHORITATIVE
CURATED
DERIVED
HEURISTIC
EXAMPLE
UNVERIFIED
```

## Authority scope

Authority must be scoped.

Example:

```yaml
authority: authoritative
authority_scope: kicad_symbol_definition
```

This supports statements about the configured symbol definition but must not be interpreted as authoritative manufacturer electrical data.

## Provenance structure

At minimum preserve:

```text
source id
source type
source title/name
location or URI when available
version/revision when available
retrieval/import timestamp when useful
provider identity
source metadata
```

## Safety rule

Agent-generated knowledge should default to `CANDIDATE` or `UNVERIFIED` unless a separate verification/promotion workflow explicitly changes its status.

Never let an LLM silently write authoritative electronics knowledge into the permanent knowledge base.
