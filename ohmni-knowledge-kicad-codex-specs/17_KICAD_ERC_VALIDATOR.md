# 17 — KiCad ERC Validator

## Goal

Implement a KiCad-backed schematic Electrical Rules Check validator without leaking KiCad-specific objects into validation core contracts.

## Expected command shape

Use the installed KiCad CLI's documented schematic ERC command. Prefer machine-readable JSON output when supported by the target KiCad version.

Conceptual command:

```bash
kicad-cli sch erc \
  --format json \
  --severity-all \
  --exit-code-violations \
  --output erc.json \
  generated.kicad_sch
```

Before hardcoding flags, Codex must verify the installed/documented command surface used by the repository's supported KiCad version.

## Integration

Implement a validator equivalent to:

```text
KiCadErcValidator
```

that returns the existing Ohmni `ValidationResult`/`ValidationIssue` types or their current repository equivalents.

## Mapping

Preserve:

```text
rule/violation code when available
message
affected items when available
severity
raw report artifact
command metadata
```

## Truthfulness

ERC success proves only that no configured ERC violation at the selected severity/rules was reported. It does not prove functional correctness, safety, simulation correctness, or PCB DRC correctness.

## Tests

- command builder unit test;
- JSON report parsing fixture;
- violation mapping;
- no-violation mapping;
- executable missing;
- timeout;
- opt-in real KiCad CLI smoke test.
