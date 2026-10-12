---
kind: implementation-workplan
workplan_id: SSDP-7X-SKILLS-ONLY-RELIABILITY-AND-QUALIFICATION-V2
protocol_version: 6.6.0
target_protocol_version: 7.2.0 (SD-R6)
amends: SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY-CONSOLIDATED §8.2, §8.3, §11 (on acceptance of the design)
revision: 2
status: proposed; executable only after (1) the second independent check of design revision 2 and contract v2 revision 2 passes and (2) SD-R9 is decided (adopted by the stakeholder 2026-10-07)
revision_history: revision 1 preserved as qualification/ssdp70/SSDP-7X-SKILLS-ONLY-RELIABILITY-AND-QUALIFICATION-V2-WORKPLAN-R1-HISTORICAL.md (sha256 52ff83df…)
created_date: 2026-10-07
---

# Skills-only 7.2: reliability, harness simplification and calibrated qualification — D3 → D4 workplan (revision 2)

Governing SSDP version: 6.6.0.

## Background and terminology

- **Scientific checks block.** The single entrypoint section that carries the full frozen §8.3 minimum obligation. It replaces the 7.1 owner routing bullet and the completion clause.
- **Fragment.** `source/shared/fragments/scientific-checks.md`, the one source of every block.
- **B1 / B2.** The two 6.6 replicates. B1 is the baseline; B2 calibrates.
- **Q1–Q5, Precondition C.** The contract v2 gates and their calibration precondition.
- **Consumed surface.** The text a run sees without loading anything.

**Proposed design:** `qualification/ssdp70/D3-PROTOCOL-7X-RELIABILITY-SIMPLIFICATION-AND-CALIBRATED-QUALIFICATION-DESIGN-2026-10-07.md` (revision 2). Referred to as *design*, with its §-numbers. It becomes the accepted cycle design only when the second independent check passes.

## 1. Outcome and authority

- **Protected outcome.** A skills-only 7.2 that delivers Protocol 7 duties as reliably as an indeterministic executor allows, with:
  - no required owner load;
  - a qualification that a good flash candidate passes with probability ≥ 0.80 and a no-effect candidate with ≤ 0.05;
  - an instrument of at most 9,000 non-test and 4,000 test lines.
- **D3 being concretized:**
  - design §2 principles; §3 reopened decisions; §5 skill shape and placement; §6 harness functions H1–H5;
  - contract v2 revision 2.
- **Governed constraints** (all unchanged):
  - the 6.6 entrypoint text and its order (`22f4bdba`);
  - the frozen §8.3 minimum (elements 1–7, role map, label table, OD-3) and its attribution rule;
  - the R1 predicate; O1–O3; OD-4(b) and A2 neutrality;
  - the 2.0× backstop; SD-2 custody; the release state.
- **Non-goals:**
  - compressing 6.6 text;
  - trimming entrypoint descriptions;
  - new owners, routes or kernel placement;
  - restructuring the owner beyond the targeted lines;
  - deterministic control (design §7 → 8.0);
  - any qualification campaign (that needs fresh fixtures and its own work order).
- **Upstream.** No D1/D2 scientific or numerical meaning changes. The doctrine change (owner reads become recommended depth) is a D3/workplan decision covered by SD-R3.

## 1a. Scientific inspectability (O1)

- **What is produced.** Qualification evidence about agent behaviour.
- **Realized record:** per-run traces, oracle and evaluator verdicts, gate computations, the B1/B2 rates.
- **Reader:** the stakeholder and the independent reviewers.
- **Routine questions:**
  - Did each gate pass, and at what operating characteristics?
  - Which runs drove each verdict?
  - Which candidate errors are absent from B1 and B2?
- **Inspectability surface.** The H4 report (contract §7), within the deliverable.
- **Variant search.** Exposures and margins were explored in `qual-v2/operating_characteristics.py` across ICC values. The selected values are fixed in contract §5 before any run.

## 2. Importance and attention allocation

**Highest-value outcomes:**
1. Block uptake: Q2 and the Q3 effect on the S4 probe.
2. A correct, calibrated H4.
3. The harness budget, met with H1–H5 intact.

**Mandatory floors:**
- the frozen-minimum mapping is complete and independently checked;
- 6.6 text byte-identical in source and `dist/`;
- block ≤ 95% of its 7.1 block;
- owner, workplan and entrypoints consistent (no mandatory owner read anywhere);
- repository acceptance green;
- H4 reproduces the dev-probe G-figures;
- the line budget is met;
- the relay keeps all four functions.

**Critical uncertainties:**
- The true Flash duty effect and conformity under the new block (S4).
- How much of `adapters/omp.py` and `core70.py` is removable.

**Rigor plan:**

| Mode | Applies to |
|---|---|
| DEEP | The frozen-minimum mapping; the owner and workplan consistency edits; H4 gate arithmetic (cross-checked against the script and `diagnose_dev_probe_20261007.py`); relay and containment refactoring |
| STANDARD | Fragment injection; scaffolding retirement |
| LIGHT | Tombstone README; release documents |
| DEFER | Owner restructuring; 6.6 text compression; non-OMP adapters |

**Stop triggers.** Design §10 X1–X5. Stop polishing once a further edit cannot change a gate outcome or a budget.

## 3. Cycle decisions and delegated D4 space

**Frozen (from the design):**
- fragment plus build injection;
- block shape, at the 7.1 completion position (design §5.1);
- targeted owner edits (lines 29, 33, 389);
- H1–H5 with the relay;
- retirement list and budgets (§6);
- contract v2 gates and exposures.

**Delegated:**
- exact block wording (starting from design Appendix A, within the frozen minimum and the 95% limit);
- the fragment's tag syntax;
- how retained harness modules are merged and named;
- the scorer's internals;
- the evaluator prompt wording, under the frozen rubric.

**Simplification target:**
- Remove the 7.1 owner routing bullet, and replace the 7.1 completion clause with the generated block.
- Retire about 7.6k non-test lines and their tests.
- Shrink about 12.7k retained lines to the 9,000-line budget by removing admission and provenance paths.
- Replace `requal71.py`, `batch_assess70.py` and the per-stage gate scripts with one H4.

## 4. Material implementation obligations

| # | Obligation | Acceptance evidence | Shortcut to reject |
|---|---|---|---|
| O-1 | Tagged fragment; `build_skills.py` injects each entrypoint's subset at its marker per the role map; `repository-hygiene` none | Generated block equals its fragment subset; injection unit tests (unknown tag, missing or duplicate marker fail) | Hand-editing six blocks; editing `dist/` |
| O-2 | 6.6 text byte-identical outside the block | Test diffs source **and generated `dist/`** entrypoints against `22f4bdba` with the block removed; descriptions equal 7.1 | Re-flowing 6.6 text |
| O-3 | Lossless frozen-minimum mapping: each §8.3 item (elements 1–7 per role map, label table, delegate questions with qualifiers, gap rule) plus the (a)–(c) conditions, mapped to block text per entrypoint | Mapping file in `qual-v2/`; static test that each mapped phrase exists; **independent** mapping check record | Scoring or mapping against D4's own wording only |
| O-4 | Each block ≤ 95% of its own 7.1 block (routing bullet plus completion section at `58fd67b`) | Static test over generated `dist/` | Moving required meaning to the owner to meet bytes |
| O-5 | Targeted owner edits (lines 29, 33, 389) and governing-workplan §8.2/§8.3 R2 sentence amendments, per design §3; routing bullet removed | Consistency test: no current text in the owner, the governing workplan or the entrypoints makes an owner read mandatory or says the surface carries less than the minimum; P7 tests updated with negative cases (missing question, element or qualifier fails) | Leaving the old mandatory-load text in force anywhere |
| O-6 | Harness H1–H5 consolidated; relay keeps credential separation, single-endpoint egress with refusal logging, activation-delivery proof and turn cap; retired modules deleted only after the new harness passes, with a tombstone README (module → last commit) | Line counts ≤ 9,000 non-test and ≤ 4,000 test; integration test launches a real bubblewrap OMP episode through the relay with the scripted delegate, exercising activation proof, turn cap and an egress refusal; pins test | Deleting before acceptance; mocking the relay or the launch |
| O-7 | H4 implements contract v2 §3–§7 exactly: Precondition C, δ, Q2's cluster-aware k, the Q3 episode sign test, Q5 rules, report | (a) Unit tests against `operating_characteristics.py` values; (b) re-scoring the 2026-10-06/07 dev-probe runs reproduces `diagnose_dev_probe_20261007.py` G1–G4 | Treating advisory regex verdicts as binding |
| O-8 | Precondition inputs: the 40-item evaluator calibration set with ≥ 10 known failures; oracle known-good and known-bad fixtures; evaluator input with version identifiers redacted | Frozen, pinned, exercised by H4 | An evaluator sharing the executor model |
| O-9 | Version boundary (FF-001, PC-001): `source/PROTOCOL_VERSION` 7.2.0; `ssdp-protocol-7.2` profile in the versioning reference; frozen 7.1.0 package and profile preserved; terminal disposition record for 7.1.0 (superseded, non-qualified); CHANGELOG 7.2.0 entry; README routes intact; `history/SEMANTIC_EVOLUTION.md` entry (absolute floors → calibrated gates; mandatory owner load → depth) | Repository release-document checks; profile test; 7.1 artefacts byte-identical | Freezing or publishing the 7.2.0 identity before S1–S3 pass review |
| O-10 | 8.0 inputs (design §7) appended to the 8.0 workplan as an inputs list only | Diff confined to an inputs section | Starting 8.0 design |

## 5. Evidence and dependencies

- **Reused:**
  - the 2026-10-06/07 dev-probe artifacts, as the H4 regression oracle only;
  - historical records, as lessons;
  - 6.6 Stage F rates, as calibration inputs to the script.
- **Stale:** every 7.1 run; the contract revision 16 computations; the executor and evaluator admissions.
- **New realizations required:** the S4 development probe; then a campaign under its own work order with fresh fixtures, B1/B2 and Precondition C.

## 6. Affected surface and acceptance

**Affected surface:**
- the six entrypoints and the fragment;
- `build_skills.py` and its tests;
- the owner (targeted lines) and the governing 7.0 workplan;
- `dist/skills/*` and the orchestrator snapshot;
- the P7 tests;
- `source/PROTOCOL_VERSION` and the versioning reference;
- the harness tree;
- `requal71/` operator material (superseded for P3 by a v2 work order);
- CHANGELOG, history, README routes;
- the 8.0 workplan.

**Required checks:**
- repository acceptance per README/CI: inherited regression; package build plus independent validation; `dist/` parity; whitespace; frozen-resource integrity; `generate_protocol_snapshot.py --check`;
- the O-1 to O-9 tests;
- harness integration through the real relay;
- the H4 regression;
- the budget checks.

**Production qualification.** A contract v2 campaign is required for any qualification claim. It is outside this workplan.

## 7. Authority, documentation and history impact

- **D3 and workplan.** The governing 7.0 workplan §8.2/§8.3/§11 are amended through the design, after the second independent check and SD-R9. Contract revision 16 is superseded by v2 and preserved unchanged.
- **D4 specification.** The P7 tests encode the new consumed surface and the consistency rule.
- **History.** One `SEMANTIC_EVOLUTION.md` entry.
- **Generated outputs.** `dist/` and the snapshot are regenerated, never hand-edited (SP-001).

## 8. Stages

| Stage | Content | Gate to next |
|---|---|---|
| S0 | **Second** independent check of design revision 2, contract v2 revision 2 and this workplan; stakeholder decision on SD-R9 | PASS (or PASS with gaps, repaired by a minimal delta) and SD-R9 recorded |
| S1 | Skill: O-1 to O-5; regenerate; P7 tests; independent mapping check | Repository acceptance green; mapping check PASS |
| S2 | Harness: O-6 to O-8; retirement after the new harness passes | Budgets met; integration through the relay green; H4 regression reproduces the dev-probe figures |
| S3 | O-9 and O-10; independent D4 Review of S1–S3 | Review PASS; then freeze the 7.2.0 identity |
| S4 | Pre-registered development probe on the disclosed corpus (development purpose): GLM-5.3-Flash, plus optionally one flash-tier comparison model; candidate vs B1 vs B2; estimates the duty effect, conformity, ICC and p̂ | X1 not triggered → re-size the exposures with the script → commission the P3 custodian and the campaign work order under contract v2 |

## 9. Reopen and Challenge triggers

- **D4-local:** a test failure; a budget overrun attributable to implementation.
- **D3 reopen:** design §10 X1–X5.
- **D2/D1:** none expected. A finding that a Protocol 7 element's meaning is wrong goes to the doctrine owner as a SERIOUS CHALLENGE.
- **Additive-repair guard:** any added clause, gate or module shows its byte, line and compound-probability cost (X5).

## 10. Final handoff

Lead with:
- any Serious Challenge or blocker;
- the S0–S4 gate states;
- measured block bytes per entrypoint, against their limits;
- harness line counts (before and after);
- the mapping-check and consistency results;
- the H4 regression result;
- the S4 estimates with the re-sized exposures.

Unexecuted required checks are blocking.
