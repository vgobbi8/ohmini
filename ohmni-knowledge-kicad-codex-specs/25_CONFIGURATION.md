# 25 — Configuration and Composition

Follow the existing Ohmni configuration rule: environment variables are read in configuration/composition, not scattered throughout domain modules.

## Potential settings

Only add settings actually needed by implemented tasks.

Candidates:

```text
OHMNI_KNOWLEDGE_ENABLED
OHMNI_KNOWLEDGE_PATHS
OHMNI_KICAD_CLI_EXECUTABLE
OHMNI_KICAD_PROJECT_DIR
OHMNI_KICAD_SYMBOL_LIBRARY_PATHS
OHMNI_KICAD_GLOBAL_SYM_LIB_TABLE
```

Naming may be adapted to current repository conventions.

## Rules

- typed configuration;
- explicit defaults;
- sanitized config snapshot;
- no credentials in snapshots;
- testable environment parsing;
- direct constructor injection remains possible in unit tests.
