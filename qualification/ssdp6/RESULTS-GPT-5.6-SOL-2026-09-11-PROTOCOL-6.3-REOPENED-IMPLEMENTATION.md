# Protocol 6.3 reopened implementation evidence — 2026-09-11

## Status

**Implementation semantic candidate produced; qualification acceptance not claimed.**

This implementation addresses the blocking owner-layer defects recorded by the reopened Protocol 6.3 workplan and sixth review. It deliberately does **not** advance Stage G, close the workplan, publish a replacement bootstrap, or claim independent-review acceptance. Repair E/F remain lifecycle gates after this semantic implementation candidate is published and requalified.

## Basis

- Branch before this implementation: `ssdp-6.3-engineering-memory` at `562a8bb41535f1898296327dbf21459d50225d56`.
- Accepted Protocol 6.2 implementation reference consulted: `b59adc77efe6951912cfd705cc43830c58ca27d0`, especially `source/roles/software-implementation/SKILL.md`.
- Reopened owner: `workplans/active/PROTOCOL-6.3-EVIDENCE-BACKED-PROJECT-ENGINEERING-MEMORY-WORKPLAN.md`.
- Blocking review: `qualification/ssdp6/WORKPLAN-SIXTH-REVIEW-GPT-5.6-SOL-2026-09-11-PROTOCOL-6.3.md`.

The repair follows the 6.2 implementation discipline: fix the canonical D4/PEM owner, avoid a parallel authority or package-side wrapper, keep unavailable checks unavailable rather than treating them as PASS, and preserve the independent-review boundary.

## Implemented reopened repairs

### D1 — durable evidence realization

`source/project_engineering_memory.py` now parses material evidence routes as explicit source/revision/path bindings and resolves current-repository bindings through Git. A binding can remain `HEALTHY` only when the stored revision resolves as a commit and that exact repository path exists at that immutable commit. A blob object used as a path-bearing publication revision is rejected as `UNAVAILABLE`; a missing path is also `UNAVAILABLE`.

The initial PEM bootstrap contained exactly this false-positive shape: `PC-001` labeled the preservation-census route healthy while using preservation-census **blob** identity `a9bfa4c8ade4ead8ab1820dc18d2f64e86ecd098` as if it were a containing commit. The route is corrected to immutable commit `82e6e1badf2c88c00967155bb9d30c773b80d1ef`, which actually contains `qualification/ssdp6/SSDP-6.3-PRESERVATION-CENSUS.md`.

### D2 — root/detail publication coherence

Partitioned schema-1 memory now requires root-declared SHA-256 content identity for each detail file. Loading checks the digest and requires root/detail agreement for project identity, repository, scope, accepted base, and candidate overlay. Detail partitions may not own a second active summary. Duplicate canonical IDs remain rejected before the new digest diagnostic so the historical duplicate-ID falsification continues to exercise its intended invariant.

### D3 — immutable observation lineage

An admissible occurrence/application must retain a non-empty factual `observation`. `validate_reconciliation(previous, current)` rejects silent observation rewriting. A clerical correction is accepted only when it records the previous observation SHA-256 plus reason and evidence; substantive reinterpretation remains an assessment/supersession operation instead of mutation of observed history.

### D4 — recurrence after accepted repair

A truthy `recurrence_after_accepted_repair` label no longer creates recurrence credit. It requires a structured recurrence basis tying the later event to a prior occurrence, actual repair identity, repair-acceptance evidence, the later independent event identity, and an independence basis. Alias/copy lineage cannot count as recurrence.

### D5 — provenance-aware independence and PROVEN obligations

Supporting applications carry explicit provenance clusters. A `PROVEN` family requires claim-relative structured maturity basis and closed evidence obligations. Independence-sensitive obligations require at least two independent supporting provenance clusters rather than counting multiple records from one common lineage as independent replication. Comparative/default/best guidance may likewise declare an independence requirement.

### D6 — evaluable notices

Current notices now require a trigger whose current state can be evaluated. Supported trigger classes include deadlines, accepted-base changes, binding changes, owner changes, and explicitly assessed manual/external triggers. A fired or indeterminate trigger cannot remain silently `CURRENT`; it must route to review/reconciliation. The one historically documented deterministic phrase, `review on next accepted-base change`, is retained as a compatibility path pending material edit.

### D7 — exact accepted-base / HAS / candidate-overlay seam

`validate_has(...)` pins the Historical Applicability Set to exact accepted-project, accepted-PEM, and candidate-overlay identities, rejects self-ratification, rejects omission of accepted entries, and marks an advanced accepted basis as review-required until reconciliation. `validate_overlay(...)` similarly rejects self-ratification, wrong base identity, and deletion of accepted entries by omission.

## Focused counterfactual qualification executed during implementation

Command executed against the repaired module and focused reopened suite:

```text
python -m unittest -v tests/test_protocol_63_reopened_repairs.py
```

Observed result: **7 tests, all PASS**.

The focused suite explicitly falsifies:

1. blob-as-revision and missing-path `HEALTHY` false positives;
2. mixed/tampered root-partition publication state;
3. missing admissible observations and silent observation rewrite;
4. label-only accepted-repair recurrence;
5. one common provenance cluster masquerading as independent `PROVEN` support;
6. fired or opaque review triggers left `CURRENT`;
7. stale/omissive/self-ratifying HAS basis behavior.

The focused suite was rerun after compatibility adjustments and remained 7/7 PASS.

## Compatibility checks performed

The existing `tests/test_protocol_63_engineering_memory.py` contract was inspected before publication. Existing success fixtures already carry provenance clusters; the existing `PROVEN` falsification expects missing claim-relative basis to fail; the historical recurrence diagnostic remains reachable; and duplicate partition IDs retain diagnostic precedence over the newly required digest identity.

A local network clone of the remote repository could not be completed because the execution environment returned `Could not resolve host: github.com`. Remote repository truth was therefore inspected and published through the connected GitHub repository interface. **No repository-wide test run, generated-distribution regeneration, fresh-install exercise, replacement-bootstrap qualification, or independent review is represented as executed by this artifact.** Those remain required Repair E/F gates.

## Gate disposition after this implementation commit

- Reopened D1-D7 owner-layer implementation: **implemented in the semantic candidate**.
- Focused reopened counterfactuals: **PASS (7/7)**.
- Repair E replacement-bootstrap lifecycle: **NOT YET EXECUTED / NOT PASS**.
- Repair F qualifier plus separate independent reviewer: **NOT YET EXECUTED / NOT PASS**.
- Stage G release/closure: **BLOCKED by E/F by construction**.

This report is implementation evidence, not the independent qualifier or reviewer artifact.