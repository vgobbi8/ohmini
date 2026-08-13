# 11 — Knowledge Ingestion and Markdown Provider

## Separation

Querying and ingesting are different responsibilities.

Introduce a small ingestion boundary rather than making `KnowledgeEngine` responsible for writing all providers.

## MVP storage

Use manually authored Markdown with structured frontmatter or an equivalent transparent file format.

Suggested repository layout:

```text
knowledge/
├── concepts/
├── facts/
├── constraints/
├── formulas/
├── procedures/
├── components/
└── tools/
```

## Requirement

Adding a new knowledge document must not require modifying Python agent code.

## Frontmatter example

```yaml
---
id: electronics.filter.rc.low_pass.cutoff
family: declarative
kind: formula
title: RC low-pass cutoff frequency
tags: [electronics, rc, filter, low-pass]
authority: curated
authority_scope: engineering_formula
---
```

## Parser behavior

- fail explicitly on invalid required metadata;
- normalize enum casing according to one documented convention;
- preserve unknown non-core metadata where useful;
- never execute arbitrary code from knowledge documents;
- use UTF-8;
- retain source file reference as provenance;
- produce actionable parsing errors with file/line context when practical.

## Search behavior for MVP

A simple provider may support:

- exact ID lookup;
- tag filtering;
- kind/family filtering;
- domain/topic filtering;
- simple case-insensitive textual matching.

Do not add embeddings just to satisfy this slice.
