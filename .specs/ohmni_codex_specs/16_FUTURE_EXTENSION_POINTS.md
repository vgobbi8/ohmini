# Future Extension Points — Do Not Implement Yet

This document exists so the initial architecture stays incrementable without prematurely implementing future scope.

---

## 1. SKiDL generator

Future:

```text
ModelBackend
    ↓
SkidlGenerator
    ↓
SKiDL source
    ↓
compile/export
    ↓
SPICE netlist
    ↓
same validators
```

It must implement the existing `CircuitGenerator` contract.

`GeneratedCircuit` becomes:

```text
source_type = skidl
source_text = generated Python/SKiDL
spice_netlist = compiled output
```

`DirectSpiceGenerator` remains intact and selectable.

---

## 2. Functional validators

ngspice success is not functional correctness.

Future validators may:

- extract AC cutoff frequency;
- evaluate gain;
- evaluate DC operating point;
- inspect transient response;
- compare measurements to user constraints.

Prefer separate validators/checks over bloating `NgSpiceValidator`.

---

## 3. Repair loop

Future flow:

```text
generate
    ↓
validate
    ↓
failed? ── no ──> finish
    │
   yes
    ↓
repair using structured validation feedback
    ↓
validate again
```

This is the first point where LangGraph may provide real value.

Do not retrofit LangGraph before this loop exists.

Store each attempt as an artifact.

---

## 4. LangGraph

When repair/branching is real, model graph state around:

```text
requirement
generation attempt
validation results
attempt count
termination reason
```

Model backends and generators remain unchanged.

LangGraph orchestrates existing components; it must not replace their contracts.

---

## 5. RAG / datasheets

Future retrieval should enrich `ModelRequest` or generation context.

Do not make the model backend responsible for retrieval.

Possible flow:

```text
requirement
    ↓
retrieval
    ↓
generation context
    ↓
CircuitGenerator
```

The old no-RAG path must remain selectable for experiments.

---

## 6. Additional API providers

Add provider mappings inside the API backend/factory.

Candidates:

```text
Google
OpenRouter
local OpenAI-compatible endpoint
```

Do not change generator code.

---

## 7. Local models

A future backend may use:

```text
Ollama
vLLM
OpenAI-compatible local server
```

Either add an API-provider mapping or a separate `LocalModelBackend` only when the behavior actually differs.

---

## 8. Experimental matrix

The architecture should eventually support combinations such as:

```text
model backend:
  harness / api / local

provider/model:
  codex / openai / anthropic / ...

generator:
  direct-spice / skidl

validation:
  ngspice / functional-checks / ...

repair:
  off / on
```

Do not implement a generic experiment framework until repeated manual runs become painful.

---

## Principle

Every future feature must answer:

> Can this be added as a new implementation/composition without breaking the old experimental path?

If not, revisit the boundary before adding the feature.
