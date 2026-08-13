# 22 — Agent Repair Loop — Future Architecture

Do not implement the full repair loop in this slice unless explicitly requested later.

## Target flow

```text
requirement
   ↓
query knowledge
   ↓
generate
   ↓
validate
   ↓
failed?
 ┌─┴─┐
no  yes
│    ↓
│  structured feedback
│    ↓
│  query additional knowledge if needed
│    ↓
│  repair/regenerate
│    └──> validate again
▼
finish
```

## Attempt state

Each attempt should eventually record:

```text
attempt number
knowledge query/bundle IDs
assumptions
model identity
model output
generated artifacts
validation results
termination reason
```

## Research relevance

This is the architectural point at which deterministic validation feedback can be experimentally measured as a mechanism for reducing invalid LLM-generated circuit artifacts.
