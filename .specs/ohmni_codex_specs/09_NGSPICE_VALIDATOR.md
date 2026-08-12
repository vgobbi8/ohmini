# Spec 09 — ngspice Validator

## Goal

Implement deterministic SPICE validation by running the generated netlist through the system `ngspice` executable in batch mode.

This validator initially answers:

> Can ngspice parse and execute this generated netlist/analysis successfully?

It does **not** yet answer:

> Does the circuit meet every functional requirement in the original natural-language request?

---

## Name

```text
ngspice
```

---

## Configuration

Use:

```text
OHMNI_NGSPICE_EXECUTABLE
OHMNI_NGSPICE_TIMEOUT_SECONDS
```

Do not read the environment directly in this class.

Inject the executable and timeout through its constructor.

---

## Execution

Within the run directory, write the SPICE netlist to a deterministic artifact path such as:

```text
circuit.cir
```

Run ngspice in non-interactive/batch mode.

Prefer an invocation equivalent to:

```bash
ngspice -b -o ngspice.log circuit.cir
```

Use `subprocess` without `shell=True`.

Set:

- explicit cwd;
- timeout;
- text mode/encoding behavior;
- captured stdout/stderr when useful.

Do not invoke through a shell string.

---

## Result classification

### `passed`

Use `passed` when:

- process launches;
- does not time out;
- exits successfully;
- no fatal simulation/parser failure is detected that invalidates the run.

### `failed`

Use `failed` when ngspice executes but rejects or fails to simulate the circuit.

Generate stable issue codes for common classes where they can be identified reliably, for example:

```text
NGSPICE_NONZERO_EXIT
NGSPICE_PARSE_ERROR
NGSPICE_SIMULATION_ERROR
```

Do not build a huge regex taxonomy in v1.

### `error`

Use `error` when validation infrastructure fails, for example:

```text
NGSPICE_NOT_FOUND
NGSPICE_TIMEOUT
NGSPICE_EXECUTION_ERROR
```

A missing ngspice binary is an environment/tooling error, not proof that the circuit is invalid.

---

## Logs and output

Persist:

```text
circuit.cir
ngspice.log
ngspice.stdout.txt
ngspice.stderr.txt
```

Only create files that provide actual information; empty stdout/stderr files are optional.

The structured `ValidationResult.metadata` may reference artifact file names.

Do not embed the entire log into `validation.json`.

---

## Timeout

On timeout:

- terminate/kill process safely;
- return `error`;
- create issue `NGSPICE_TIMEOUT`;
- preserve partial output when available.

---

## Cross-platform behavior

Support Windows, macOS, and Linux by invoking the configured executable name/path directly.

Do not hard-code `/usr/bin/ngspice`.

---

## Tests

### Unit

Mock subprocess execution and cover:

- successful exit;
- non-zero exit;
- timeout;
- executable missing;
- stdout/stderr/log persistence;
- paths with spaces;
- no `shell=True`.

### Integration

Add an optional integration test using a known-valid tiny RC netlist.

Mark it so default CI can skip it if ngspice is unavailable.

When ngspice is installed, the test should pass without network/model access.

---

## Acceptance criteria

- Generated SPICE is written to the run directory.
- ngspice is invoked deterministically.
- Tooling errors and circuit failures are distinguishable.
- Full logs are preserved outside the structured result.
- Validator makes no unsupported claim about meeting user intent.
