# 10 — Knowledge Provider and Engine Federation

## Stable provider contract

Conceptually:

```python
class KnowledgeProvider(Protocol):
    def search(self, query: KnowledgeQuery) -> Sequence[KnowledgeItem]:
        ...
```

The actual signature may include provider result metadata if the repository design benefits from it.

## KnowledgeEngine responsibilities

- accept a `KnowledgeQuery`;
- select or call appropriate providers;
- collect normalized items;
- deduplicate conservatively;
- retain provenance;
- apply query-level filters;
- collect warnings;
- represent unresolved information;
- return `KnowledgeBundle`.

## KnowledgeEngine non-responsibilities

- LLM reasoning;
- circuit design decisions;
- tool execution;
- automatic promotion of agent output to trusted knowledge;
- provider-specific parsing leaking into consumers.

## Deduplication

Prefer stable IDs and source identities.

Do not aggressively merge two items merely because their text is similar. Conflicting sources may be important evidence and should be retained unless the domain model explicitly knows they are equivalent.

## Future providers

The design must leave room for:

```text
MarkdownKnowledgeProvider
KiCadSymbolKnowledgeProvider
DatasheetKnowledgeProvider
RagKnowledgeProvider
DatabaseKnowledgeProvider
HttpKnowledgeProvider
McpKnowledgeProvider
AgentMemoryKnowledgeProvider
```
