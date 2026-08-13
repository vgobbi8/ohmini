# TASK-010 — Markdown Knowledge Provider

## Goal

Implement the first concrete file-backed/manual knowledge provider using safe Markdown frontmatter parsing.

## Read first

- `11_INGESTION_AND_MARKDOWN.md`
- `examples/knowledge/formula-rc-cutoff.md`

## Required work

1. Choose/use a safe frontmatter parser compatible with repository dependencies.
2. Load configured knowledge paths.
3. Parse required metadata and Markdown body.
4. Normalize to KnowledgeItem.
5. Support exact ID and basic metadata/text filtering.
6. Retain source file provenance.
7. Provide actionable malformed-file errors.

## Tests

- Valid fixture load.
- Exact ID.
- Tag/kind filtering.
- Malformed frontmatter.
- Unknown enum.
- Source path retention.

## Definition of done

- A new valid Markdown item is queryable without Python changes.

## Non-goals

- No embeddings/vector DB.
