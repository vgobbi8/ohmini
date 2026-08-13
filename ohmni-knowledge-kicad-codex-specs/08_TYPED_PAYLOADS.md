# 08 — Typed Knowledge Payloads

Use small dataclasses/value objects rather than one giant unvalidated dictionary.

## EntityKnowledge

Represents a domain entity or concept.

Suggested fields:

```text
entity_type
canonical_name
aliases
properties
external_ids
```

Examples: `LM358`, `Device:R`, `RC low-pass filter`.

## FactKnowledge

Suggested fields:

```text
subject
property
value
unit optional
qualifiers
```

## RelationKnowledge

Suggested fields:

```text
subject
predicate
object
qualifiers
```

## RuleKnowledge

Keep generic but structured enough to distinguish condition and consequence:

```text
statement
conditions
consequences
priority optional
```

Do not build a rule inference engine in this slice.

## ConstraintKnowledge

Suggested fields:

```text
statement
strength: HARD | SOFT | RECOMMENDATION
scope
condition optional
```

## FormulaKnowledge

Suggested fields:

```text
expression
variables
units
applicability
notes
```

## ProcedureKnowledge

Suggested fields:

```text
goal
inputs
prerequisites
steps
outputs
validation_strategy optional
```

Procedure steps should be ordered and serializable.

## ToolKnowledge

Suggested fields:

```text
name
capabilities
limitations
inputs
outputs
```

Tool knowledge tells the agent what a tool can prove or perform. It does not itself execute the tool.
