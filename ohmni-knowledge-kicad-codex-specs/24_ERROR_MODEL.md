# 24 — Error Model

Create explicit errors where they improve caller behavior; do not create dozens of exception classes without need.

## Knowledge errors

Consider categories such as:

```text
KnowledgeError
KnowledgeValidationError
KnowledgeSourceError
KnowledgeProviderError
KnowledgeIngestionError
```

## KiCad errors

Consider:

```text
EdaError
KiCadError
KiCadExecutableNotFound
KiCadTimeout
KiCadCommandError
KiCadLibraryError
KiCadParseError
```

Use existing repository error hierarchy if one already fits.

## Error semantics

Distinguish:

- invalid configuration;
- malformed knowledge;
- missing knowledge source;
- unresolved knowledge query;
- malformed KiCad library;
- tool unavailable;
- tool timeout;
- validation violations;
- process execution failure.

A validation violation is not the same thing as a tool invocation exception.
