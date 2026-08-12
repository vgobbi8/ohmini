# Ohmni Task Index

Source: `.specs/ohmni_codex_specs/`

This is a collapsed task index for the full spec set.

## Task list

1. `00_MASTER_PLAN.md` — align on the prototype scope, constraints, and implementation order.
2. `01_PROJECT_FOUNDATION.md` — inspect the repo and establish the module boundaries.
3. `02_CONFIGURATION_LAYER.md` — add typed settings, validation, and dotenv support.
4. `03_MODEL_CORE_CONTRACTS.md` — define the model request/response/backend contracts.
5. `04_HARNESS_BACKEND.md` — wrap the vendored harness provider backend.
6. `05_API_BACKEND_LANGCHAIN.md` — implement the API backend via LangChain integrations.
7. `06_GENERATION_CORE.md` — define generator contracts and generation outputs.
8. `07_DIRECT_SPICE_GENERATOR.md` — implement the direct SPICE generator.
9. `08_VALIDATION_CORE.md` — define validation contracts and result semantics.
10. `09_NGSPICE_VALIDATOR.md` — implement the ngspice validator.
11. `10_PIPELINE_ORCHESTRATION.md` — orchestrate generation, validation, and reporting.
12. `11_CLI_AND_COMPOSITION_ROOT.md` — wire settings, backend selection, and CLI behavior.
13. `12_RUN_ARTIFACTS_AND_REPRODUCIBILITY.md` — persist reproducible run artifacts.
14. `13_TESTING_STRATEGY.md` — cover unit, contract, integration, and E2E tests.
15. `14_VENDORING_AND_LICENSES.md` — vendor and attribute upstream harness code.
16. `15_END_TO_END_ACCEPTANCE.md` — validate the prototype end to end.
17. `16_FUTURE_EXTENSION_POINTS.md` — keep future features out of the prototype.
18. `99_REFERENCES.md` — reference material for implementation details.

## Execution order

Follow the order in the master plan:

1. `01_PROJECT_FOUNDATION.md`
2. `02_CONFIGURATION_LAYER.md`
3. `03_MODEL_CORE_CONTRACTS.md`
4. `04_HARNESS_BACKEND.md`
5. `05_API_BACKEND_LANGCHAIN.md`
6. `06_GENERATION_CORE.md`
7. `07_DIRECT_SPICE_GENERATOR.md`
8. `08_VALIDATION_CORE.md`
9. `09_NGSPICE_VALIDATOR.md`
10. `10_PIPELINE_ORCHESTRATION.md`
11. `11_CLI_AND_COMPOSITION_ROOT.md`
12. `12_RUN_ARTIFACTS_AND_REPRODUCIBILITY.md`
13. `13_TESTING_STRATEGY.md`
14. `14_VENDORING_AND_LICENSES.md`
15. `15_END_TO_END_ACCEPTANCE.md`

## Notes

- `00_MASTER_PLAN.md` is the top-level implementation guide.
- `16_FUTURE_EXTENSION_POINTS.md` is intentionally not for implementation.
- The individual task files were collapsed into this single index on request.
