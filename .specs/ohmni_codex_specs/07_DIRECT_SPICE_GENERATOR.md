# Spec 07 — Direct SPICE Generator

## Goal

Implement the first real generation strategy:

```text
Natural-language requirement
        ↓
ModelBackend
        ↓
SPICE netlist
```

The generator must not know whether the backend is Codex CLI, OpenCode, Claude Code, OpenAI API, Anthropic API, or a fake.

---

## Constructor

Conceptually:

```python
class DirectSpiceGenerator:
    def __init__(self, model_backend: ModelBackend):
        self._model_backend = model_backend
```

Name:

```text
direct-spice
```

---

## Prompt design

Keep the prompt deterministic and narrow.

The system prompt should tell the model:

- act as a circuit-netlist generator;
- output one complete ngspice-compatible netlist;
- return plain text only;
- do not use Markdown fences;
- include required analysis directives where necessary for the requested circuit;
- include `.end`;
- avoid explanations outside the netlist;
- use explicit component values;
- use node `0` as ground when appropriate;
- prefer simple components/models supported by standard ngspice for the initial prototype;
- do not invent unavailable vendor models unless the requirement explicitly needs them.

Do not embed API/provider/model-specific instructions.

Do not give the model filesystem tasks.

The user prompt contains the circuit requirement.

---

## Raw vs normalized output

Preserve the original model response for reproducibility.

The generator should normalize the response into a SPICE netlist.

Normalization may:

- trim surrounding whitespace;
- strip a single Markdown code fence if the model disobeys;
- strip obvious prose before/after a uniquely fenced netlist;
- normalize line endings.

Normalization must **not** silently redesign the circuit.

Do not automatically "fix" components, values, node names, or directives.

If a reliable netlist cannot be extracted, raise `CircuitOutputParseError`.

---

## Minimal SPICE sanity rules

Generation is not validation, but reject obviously unusable output:

- empty output;
- no non-comment content;
- no `.end` after normalization.

Do not implement a complete SPICE parser here.

Let ngspice be the source of truth for actual parsing/simulation errors.

---

## Returned object

Return:

```text
GeneratedCircuit(
    generator="direct-spice",
    source_type="spice",
    source_text=<normalized netlist>,
    spice_netlist=<normalized netlist>,
    ...
)
```

Ensure the raw model response remains available to the run-artifact layer separately or via generation metadata.

---

## Tests

Use `FakeModelBackend`.

Cover:

- exact backend request/system prompt shape;
- clean netlist response;
- fenced netlist response;
- whitespace normalization;
- blank output;
- prose-only output;
- missing `.end`;
- generator metadata;
- no provider-specific branching.

Fixture example should be a very simple RC circuit.

---

## Acceptance criteria

- Generator has zero imports from LangChain and vendored harness.
- Same generator instance works with any `ModelBackend`.
- No ngspice call occurs inside the generator.
- No correction loop occurs.
- Original response can be preserved by the pipeline.
