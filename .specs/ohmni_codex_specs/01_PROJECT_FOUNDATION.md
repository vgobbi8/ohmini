# Spec 01 — Project Foundation

## Goal

Prepare the existing Ohmni repository for the incremental architecture without rewriting working code.

This is a repository-alignment step, not a feature implementation step.

---

## Required work

### 1. Inspect the existing project

Identify:

- package root;
- current Python version;
- dependency manager;
- current CLI entry point;
- existing generation logic;
- existing ngspice/KiCad integration;
- existing tests;
- current output/artifact conventions;
- current configuration approach.

Respect existing conventions where they are reasonable.

### 2. Keep the current toolchain

If the repository uses `uv`, continue using `uv`.

Do not migrate package managers.

Do not change the Python version merely to satisfy a preference. Only change it if a required dependency is incompatible, and report that before doing so.

### 3. Establish modules for the new boundaries

Create or align modules for:

- configuration;
- model contracts/backends;
- generation contracts/implementations;
- validation contracts/implementations;
- pipeline/orchestration;
- run artifacts.

Avoid empty architecture ceremony. A module may initially contain only the contracts needed by subsequent specs.

### 4. Preserve existing behavior

If there is already an Ohmni CLI or a working vertical slice:

- do not delete it;
- do not rename it without necessity;
- do not remove current fixtures;
- do not remove existing KiCad or ngspice work;
- do not force old code through new abstractions in this step unless necessary to keep tests passing.

### 5. Add a project-local example environment file

Add:

```text
.env.example
```

Do **not** add `.env`.

Ensure `.env` is ignored by git.

The final variable list is defined in Spec 02.

### 6. Dependency discipline

Do not add LangGraph.

Do not add SKiDL.

Do not add a web framework.

Do not add a persistence/database package.

Do not add model-provider SDKs yet unless they are already present.

---

## Tests

At the end:

- existing tests must still pass;
- no network calls are allowed;
- no real model calls are allowed;
- no ngspice invocation is required in this spec.

---

## Acceptance criteria

- Repository still builds/installs with the existing workflow.
- Existing tests pass.
- New module boundaries exist or are mapped cleanly onto the existing structure.
- `.env.example` exists.
- `.env` is ignored.
- No existing feature was intentionally removed.
- No LangGraph/RAG/SKiDL work was introduced.

---

## Out of scope

- model invocation;
- API providers;
- circuit generation;
- ngspice validation;
- pipeline execution;
- repair loops.
