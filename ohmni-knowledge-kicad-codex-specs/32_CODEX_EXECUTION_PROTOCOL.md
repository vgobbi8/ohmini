# 32 — Codex Execution Protocol

For every task under `tasks/`:

1. Read `README.md`, `00_MASTER_PLAN.md`, and the task file.
2. Read any root specs referenced by the task.
3. Inspect the current repository and existing equivalents before editing.
4. State a concise implementation plan.
5. Implement only the task plus necessary supporting changes.
6. Add/update tests.
7. Run focused tests first.
8. Run broader regression tests when the task changes shared contracts.
9. Do not generate unrelated cleanup commits.
10. Do not add future-scope dependencies merely because they are mentioned in architecture docs.
11. End with:
    - files changed;
    - design decisions;
    - tests executed and result;
    - limitations;
    - deviations from the spec and rationale;
    - recommended next task.

## When the spec conflicts with repository reality

Repository reality wins only when preserving current working behavior or avoiding duplication requires adaptation. Document the deviation instead of silently changing the architecture.

## When uncertain

Prefer the smallest implementation that preserves the architectural seam. Avoid inventing production-scale abstractions.
