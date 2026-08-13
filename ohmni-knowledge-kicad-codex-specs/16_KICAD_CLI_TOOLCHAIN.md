# 16 — KiCad CLI Toolchain Adapter

## Goal

Provide one deterministic wrapper around `kicad-cli` execution.

## Core responsibilities

- configurable executable name/path;
- version detection;
- subprocess execution with `shell=False`;
- explicit argument arrays;
- timeout;
- stdout/stderr capture;
- exit-code capture;
- duration measurement;
- useful error translation;
- command metadata suitable for run artifacts.

## Version command

Support a command equivalent to:

```bash
kicad-cli version
```

Optionally support documented version output formats when useful.

## Security

Never concatenate untrusted strings into shell commands. Never use `shell=True` for convenience.

## Error model

Distinguish at least:

```text
executable not found
timeout
process execution error
unsupported command/version
non-zero tool result
```

A non-zero exit code is not always a wrapper failure; some KiCad validation commands use exit codes to communicate violations. The higher-level adapter/validator must interpret command semantics.
