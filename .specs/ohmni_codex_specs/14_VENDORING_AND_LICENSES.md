# Spec 14 — Vendoring and Open-Source Attribution

## Goal

Vendor the small open-source coding-agent harness used by Ohmni so the TCC prototype does not depend on an unstable remote repository at runtime, while preserving proper attribution and license obligations.

This is not legal advice; follow the actual upstream license text included with the selected source.

---

## Upstream project

Initial source:

```text
twaldin/harness
https://github.com/twaldin/harness
```

At the time of planning, the repository is MIT-licensed and provides Python adapters for coding-agent CLIs including Codex, Claude Code, and OpenCode.

Before copying code, verify the license in the exact upstream commit being vendored.

---

## Vendoring procedure

1. Choose an exact upstream commit.
2. Record:
   - repository URL;
   - commit SHA;
   - date vendored;
   - upstream license.
3. Copy only the Python components required by Ohmni, unless copying the complete small Python package is simpler and safer.
4. Place them under a clearly private namespace such as:

```text
src/ohmni/_vendor/agent_harness/
```

5. Preserve copyright/license notices.
6. Add a copy of the applicable license under something like:

```text
THIRD_PARTY_LICENSES/harness-MIT.txt
```

7. Add:

```text
THIRD_PARTY.md
```

with origin and commit details.
8. Keep Ohmni-specific behavior outside vendored code whenever possible.
9. Wrap vendored code through `HarnessModelBackend`.

---

## Modification policy

Prefer:

```text
Ohmni adapter -> vendored upstream code
```

rather than editing vendored code.

If an upstream bug must be patched:

- make the smallest change;
- document it in `THIRD_PARTY.md`;
- add a comment only where useful;
- add a regression test outside or alongside the vendored package.

Do not reformat the entire vendored package.

Do not remove upstream attribution.

---

## Why vendor

The implementation should remain reproducible if:

- upstream changes flags;
- PyPI package changes behavior;
- the repository disappears;
- an incompatible release is published.

Vendoring does **not** eliminate the need for the actual external CLI executables.

Codex/Claude Code/OpenCode are still runtime prerequisites for their respective harness providers.

---

## Academic documentation

Add a concise note to project documentation stating that:

- Ohmni uses/adapts open-source infrastructure for invoking coding-agent CLIs;
- that infrastructure is not claimed as original TCC work;
- Ohmni's contribution is the application architecture, generation/validation pipeline, experimental use, and subsequent analysis.

Do not exaggerate originality.

Do not bury third-party reuse.

---

## Update procedure

Do not automatically track upstream `main`.

A future update should be intentional:

1. inspect upstream changes;
2. update recorded commit;
3. replace/update vendored code;
4. run adapter contract tests;
5. document local patches.

---

## Tests

After vendoring:

- run the vendored library's relevant unit/fixture tests if practical;
- run Ohmni harness backend adapter tests;
- ensure no network is required for unit tests.

---

## Acceptance criteria

- Exact upstream revision is recorded.
- License text is preserved.
- Vendored code lives in a clearly identified namespace.
- Ohmni code does not import the external PyPI harness package at runtime.
- Ohmni-specific behavior is implemented in the wrapper, not scattered through vendored code.
