# 30 — Coding Conventions for This Slice

## General

- Python 3.11+ compatible unless repository has moved higher.
- Prefer standard library dataclasses/protocols when sufficient.
- Keep public types small and explicit.
- Prefer frozen/slotted dataclasses for value objects when consistent with existing code.
- Use `Protocol` for replaceable architectural boundaries where appropriate.
- Keep serialization deterministic.
- Use `pathlib.Path` for filesystem paths.
- Use UTF-8 explicitly.
- Avoid global mutable registries unless clearly justified.
- Avoid provider-specific imports in knowledge core.

## Parsing

- never use unsafe YAML loaders;
- never execute knowledge document content;
- treat malformed source files as explicit errors/warnings according to provider policy;
- retain enough location metadata to debug failures.

## Subprocess

- `shell=False`;
- argument arrays;
- explicit cwd when needed;
- timeout;
- captured stdout/stderr;
- no command-string interpolation of untrusted values.

## Scope discipline

Do not opportunistically refactor unrelated code while implementing this slice.
