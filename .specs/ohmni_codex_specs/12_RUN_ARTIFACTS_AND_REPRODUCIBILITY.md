# Spec 12 — Run Artifacts and Reproducibility

## Goal

Make every experiment inspectable and reproducible enough for TCC evaluation.

Every real or fake pipeline run gets an immutable run directory.

---

## Run directory

Use:

```text
<OHMNI_OUTPUT_DIR>/runs/<run_id>/
```

Generate a sortable, collision-resistant run id.

A suitable format is:

```text
YYYYMMDDTHHMMSSZ-<short-random-id>
```

Do not use timestamps alone.

---

## Required artifacts

Target layout:

```text
run/
├── request.json
├── config.json
├── model/
│   ├── response.txt
│   └── metadata.json
├── generation/
│   ├── source.txt
│   └── circuit.cir
├── validation/
│   ├── results.json
│   └── ngspice/
│       ├── ngspice.log
│       ├── stdout.txt
│       └── stderr.txt
└── report.json
```

Adapt names to existing conventions, but keep the information.

---

## `request.json`

Include:

- original natural-language requirement;
- run id;
- start timestamp.

Do not rewrite the user's requirement before storing it.

---

## `config.json`

Store the sanitized effective runtime configuration.

Include:

- backend;
- provider;
- model;
- generator;
- validators;
- relevant timeouts;
- tool executable names/paths;
- application version/commit when cheaply available.

Never store:

- API keys;
- auth tokens;
- entire environment variables;
- CLI credential files.

---

## `model/response.txt`

Store the raw textual assistant result as returned by the Ohmni `ModelBackend`.

If a backend exposes raw subprocess JSON/JSONL, do not confuse that with the normalized model response.

Provider raw diagnostic output may be stored separately only if useful and sanitized.

---

## `model/metadata.json`

Store public metadata:

- backend;
- provider;
- model;
- token counts when available;
- cost when available;
- duration when available.

Unknown metrics stay `null`.

---

## Generation artifacts

Store:

```text
source.txt
circuit.cir
```

For direct SPICE they may contain the same normalized text.

Keep both concepts because future SKiDL will make them different.

---

## Validation artifacts

Store structured validation results separately from large logs.

`results.json` should be easy to analyze later using Python/pandas.

---

## `report.json`

Summarize:

- run id;
- overall status;
- generator;
- model identity;
- validator statuses;
- artifact relative paths;
- timing if available.

Do not duplicate giant logs.

---

## Atomicity

Prefer writing important JSON files atomically:

1. write temp file;
2. flush/close;
3. rename into final path.

This is useful because model/simulator runs may fail mid-process.

Do not overengineer a transactional storage layer.

---

## Failure artifacts

Even failed runs should preserve as much context as safely possible.

For example, model failure should still leave:

```text
request.json
config.json
report.json
```

and diagnostic metadata.

---

## Tests

Cover:

- unique run ids;
- directory creation;
- expected file layout;
- JSON serialization;
- failure runs still produce a report;
- secrets absent;
- paths in reports are relative when practical.

---

## Acceptance criteria

A researcher can inspect a run directory later and determine:

- what was requested;
- which model/backend generated it;
- which generator was used;
- what netlist was produced;
- what ngspice reported;
- why the run passed/failed.

No credential is required to understand an old run.
