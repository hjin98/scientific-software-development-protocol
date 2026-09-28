---
kind: protocol-stage-evidence
governing_protocol_version: 6.6.0
target_protocol_version: 7.0.0
stage: A
disposition: CLOSED
active_serious_challenge: none
---

# Protocol 7 Stage A closure

Stage A is closed. The `STAGE-A-CONTRACT-NO-PASS-STOP-2026-09-28.md` stop is now historical.

## Contract repair and fresh independent check

The 2026-09-28 framework check (`STAGE-A-INDEPENDENT-CONTRACT-CHECK-NO-PASS.md`) found three material gaps in contract `7fc325b5…`. They are repaired in `PROTOCOL-7.0-EVALUATION-AND-QUALIFICATION-CONTRACT.md` as follows. No other threshold changed.

1. **§4 owner-load placement.** Hits are scored per R2 trigger class: (a) realized-result judgment; (b) D1–D3 authority authoring/revision or acceptance review, with ≥2 of each; (c) gate evidence. Each class needs ≥6 distinct opportunities and ≥⌈0.8n⌉ hits. Class assignment is predeclared, a replicate counts only on a strict majority, and an under-exposed class defeats the placement claim.
2. **§3 unnamed-class detection.** A separate row requires ≥⌈0.8n⌉ of n≥6 eligible unnamed properties, critical and non-critical alike. It is independent of the non-critical 16/20 row and the critical-disposition rule. A correct limitation is not a detection.
3. **§7 human legibility.** Each of ≥4 participants reviews one fixture per arm, never the same fixture in both arms. Order is counterbalanced, and each arm sees ≥2 fixtures, ≥20 routine and ≥4 critical answer opportunities. Dropouts leave both arms, and underexposure is never a pass.

A context that authored neither the candidate, the contract nor any fixture rechecked the exact revision. Result: **PASS for the framework only** (`STAGE-A-INDEPENDENT-CONTRACT-RECHECK-PASS.md`). All three gaps are closed, with no new material gap and no Serious Challenge.

**Frozen framework:** contract SHA-256 `02dd12dbf2468c5134119146bd04b8ae9d46551a505e498aa0e2b885030ce077`, bound with workplan `66f29437…`, stakeholder decision `b1ae718c…`, basis map `8ae7a966…` and release state `be05bc06…`. Any later contract edit needs a new applicability check. Its front-matter `status` line is retained as checked; current status is this record. This contract binds before any candidate run.

The recheck's eight minor findings are carried, not repaired. Editing the contract now would unbind the PASS, and none makes a floor lax. One matters for interpretation. Jointly across three classes, a true 0.9 owner-load hit rate passes only about 0.69 of the time. A placement-miss result must therefore be read with that power in mind. It fails safe, toward a reopen, and never toward a false pass. The Stage F report restates the minors' substance where it applies, such as the escalation route for a Stage E/live backstop breach and the structural-check list, both governed by workplan §8.3/§11.5.

## Custody designation

- **Fixture custodian.** A separate subagent context, launched 2026-09-28 by the implementing session, authors no Protocol 7 doctrine or candidate source. It writes only under `/home/samjin/ssdp70-fixture-custody/`, outside the repository. `keys/`, `oracles/`, `probes/` and `human-trial/` hold solution-bearing material. `corpus/` holds executor-facing fixtures, which the author still does not read. Its only permitted hand-back to the author is `METADATA-FOR-IMPLEMENTER.md`, which carries counts, episode totals and unmet minimums. It keeps an `ACCESS-LOG.md`.
- **Candidate author/implementer.** Reads none of the custody directory before the affected candidate freeze. It sees only the metadata file and the custodian's non-solution-bearing hand-back. The harness code it writes is generic: runner, catalog isolation, trace capture, delegate and issue stand-ins, side-effect log. It loads custody paths without the author inspecting their content.
- **Pre-run contract checker.** A context that authored neither candidate nor fixtures. That is either the recheck context or a fresh context of the same independence. It performs the withheld-instance and actual-harness checks before any candidate run and reports only counts and pass/fail to the author.
- **Independent evaluator.** A fresh context that receives keys only after frozen run output.

## Pre-run checks still required (not passed)

These carry forward to the Stage F pre-run gate. They are required, and none has run:

- the withheld classification rationale, including disguised listed mechanisms;
- per-arm and per-R2-class exposure;
- unnamed eligibility;
- critical keys and dispositions;
- oracle branches and R2 events;
- route classes against the withheld context;
- the human-trial plan;
- the actual-harness checks: collection, per-branch known-broken and known-good, complete capture, side-effect detection, composite-mode and the chained cheap-first-look probe;
- Stage E remeasurement of the generated D4 entrypoint and the owners T7 reads;
- fresh paired 6.5/6.6 baselines.

## Stage A obligations

| Workplan §12 Stage A item | Evidence |
| --- | --- |
| Protocol 8 consolidation and authority index | `STAGE-A-BASIS-AND-PRESERVATION.md`; index reconciled at this closure |
| §3.2 ownership map versus immutable 6.6 owners | basis map; no new row needed |
| PEM basis, HAS, 6.6 intake and governance request | basis map (partial-coverage request routed; no PEM edit) |
| Capability-preservation map, hygiene sentinel, route classes, supported-profile list to Stage E | basis map |
| Burden thresholds, self-adoption oracle, fixed-cost backstop, 512 B margin, T7 rule | contract §4 and §5; `STAGE-A-STATIC-PREMEASUREMENT.md` (its 1.10 text is historical, superseded by the 2026-09-28 decision) |
| D4 draft, independent losslessness check and backstop comparison | `STAGE-A-D4-ENTRYPOINT-COMPRESSED-DRAFT.md`: 14,331 B against a 16,208 B static limit under 2.0 × with 512 B margin |
| §11 framework, custodian and checker designation, independent pre-run check | contract `02dd12db…`; recheck PASS; designation above |
| 6.6 release state unchanged; 6.6 semantics from mapped immutable source | `PROTOCOL-RELEASE-STATE.yaml` unchanged (`be05bc06…`) |

## Checks at closure

Python 3.11 via uv:

- `source/release_state.py`: coherent;
- `source/project_engineering_memory.py PROJECT-ENGINEERING-MEMORY.md`: schema 1, five families, zero notices;
- `python -m unittest discover -s tests`: **398 OK, 3 skipped**. The skips are the remote 6.2 fallback, the 6.3 bootstrap and the 6.4 exact-ref bootstrap, all CI-only;
- `git diff --check`: clean.

Package build, parity, frozen-resource and Orchestrator checks are not triggered by evidence-only Stage A. They apply from Stage B onward.
