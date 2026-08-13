# Ohmni Knowledge Engine + KiCad Integration — Codex Implementation Dossier

This package is the implementation specification for the next Ohmni architecture slice.

The goal is to introduce a provider-agnostic **Knowledge Engine** and a file/CLI-oriented **KiCad integration layer** while preserving the current working model, generation, validation, and pipeline behavior.

## Core idea

Ohmni should separate four concerns:

1. **ModelBackend** — how AI is executed.
2. **KnowledgeEngine** — what reusable domain knowledge the agent can consult.
3. **EDA/Tool adapters** — deterministic operations such as KiCad library inspection, KiCad CLI execution, ERC, exports, and ngspice.
4. **Design pipeline** — how generation, validation, feedback, and future repair attempts are orchestrated.

The Knowledge Engine is **not synonymous with RAG** and is **not synonymous with agent memory**. Knowledge may be manually authored, imported, retrieved from KiCad libraries, read from documents, queried from databases, provided by MCP servers, or obtained from HTTP resources. Every source must normalize into stable Ohmni knowledge contracts.

## How Codex should use this dossier

Start with `00_MASTER_PLAN.md` and `tasks/TASK_INDEX.md`.

For each task:

1. inspect the current repository before changing code;
2. preserve working behavior unless the task explicitly changes it;
3. implement only the task scope plus strictly necessary support;
4. add or update tests;
5. run the smallest relevant test set;
6. report files changed, tests executed, limitations, and deviations;
7. do not automatically continue to the next task unless instructed.

## Suggested implementation order

Follow `tasks/TASK_INDEX.md`. The task files are deliberately small enough to execute independently but share the architecture described in the root specifications.

## Important scope decision

Live KiCad Schematic Editor control through IPC is **not required** for this slice. Ohmni should use:

- configured KiCad symbol libraries as a knowledge source;
- `.kicad_sym` and library tables for deterministic symbol discovery/query;
- `.kicad_sch` as an export artifact when supported by the implementation;
- `kicad-cli` for deterministic validation and export operations;
- manual opening/import into KiCad as an acceptable current workflow.

Live editor IPC, automatic placement/routing, and full PCB automation are future work.
