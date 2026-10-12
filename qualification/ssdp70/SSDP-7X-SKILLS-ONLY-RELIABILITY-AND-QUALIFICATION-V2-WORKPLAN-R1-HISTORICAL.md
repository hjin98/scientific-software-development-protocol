---
kind: implementation-workplan
workplan_id: SSDP-7X-SKILLS-ONLY-RELIABILITY-AND-QUALIFICATION-V2
protocol_version: 6.6.0
target_protocol_version: 7.x skills-only candidate (label per SD-R6; recommended 7.2.0)
amends: SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY-CONSOLIDATED §8.2, §8.3, §11 (on adoption)
status: proposed; stakeholder decisions SD-R1..R8 recorded 2026-10-07; executable only after the S0 independent check of the D3 design and contract v2
created_date: 2026-10-07
---

# Skills-only 7.x reliability, harness simplification and calibrated qualification: D3 → D4 workplan

Governing SSDP version: 6.6.0.

## Background and terminology

- **Scientific checks block.** The single entrypoint section that carries Protocol 7's required behaviour. It replaces the 7.1 owner routing bullet and the completion clause.
- **Fragment.** `source/shared/fragments/scientific-checks.md`, the one source of every block.
- **A/A run.** The 6.6 arm run twice on the same corpus. It calibrates the instrument.
- **Q1–Q5.** The contract v2 gates.
- **Consumed surface.** The text a run sees without loading anything: the injected `SKILL.md`.

**Design authority:** `qualification/ssdp70/D3-PROTOCOL-7X-RELIABILITY-SIMPLIFICATION-AND-CALIBRATED-QUALIFICATION-DESIGN-2026-10-07.md`. It is referred to as *design* below, and its §-numbers are cited.

## 1. Outcome and authority

- **Protected outcome.** A skills-only 7.x that delivers its Protocol 7 duties as reliably as an indeterministic executor allows, with:
  - a smaller cognitive load;
  - a qualification that a good candidate can pass and a no-effect candidate cannot;
  - an instrument no larger than the decision needs.
- **Accepted D3 being concretized:**
  - design §2 principles, §3 reopened decisions, §5 skill shape, §6 harness functions H1–H5;
  - contract v2 (`qualification/ssdp70/PROTOCOL-7X-CALIBRATED-QUALIFICATION-CONTRACT-V2-PROPOSED.md`).
- **Governed constraints.** All are unchanged:
  - 6.6 entrypoint text (`22f4bdba`) outside the block and description;
  - workplan §8.2 R1 meaning; elements 1–7 and the role map; O1–O3; OD-3 (qualifier inside each delegate question); OD-4(b) and A2 neutrality;
  - SD-2 custody; release state.
- **Non-goals:**
  - compressing 6.6 text;
  - new owners, routes or kernel placement;
  - restructuring the owner beyond relocation;
  - any deterministic control (design §7 → 8.0);
  - running a qualification campaign (that needs fresh fixtures and a separate work order).
- **Upstream exclusion.** No D1/D2 scientific or numerical meaning changes. The doctrine change (owner reads become optional depth) is a D3/workplan decision covered by SD-R3.

## 1a. Scientific inspectability (O1)

This work produces qualification evidence about agent behaviour, not scientific results about a natural system.

- **Material realized record.** Per-run traces, oracle and evaluator verdicts, gate computations, A/A rates.
- **Reader.** The stakeholder and the independent reviewers.
- **Routine questions:**
  - Did each gate pass, and with what operating characteristics?
  - Which runs drove each verdict?
  - Which errors did the candidate make that the baseline did not?
- **Product inspectability surfaces (within the deliverable).** The H4 scorer report (contract v2 §7), which retains per-run attribution.
- **Variant search.** Threshold variants were explored only in `qual-v2/operating_characteristics.py`. Exposures n ∈ {40, 48, 60, 80} were compared, and the selected sizes are fixed in contract v2 §4 before any run.

## 2. Importance and attention allocation

**Highest-value outcomes:**
1. The block's uptake: Q2 and Q3 direction on the development probe.
2. Correct, calibrated gate computation in H4.
3. The harness budget, met with H1–H5 intact.

**Mandatory acceptance floors:**
- 6.6 text byte-identical outside the block and description.
- Every removed clause has an owner home, confirmed by an independent relocation check.
- Block sizes within SD-R4.
- Repository acceptance green.
- H4 re-scores the dev-probe artifacts to the recorded G-figures.
- The line budget is met.

**Critical uncertainties:**
- Whether the compressed block keeps G1-level uptake on the gating flash executor.
- Whether OMP can enforce the turn cap without the observer proxy.

**Rigor plan:**

| Mode | Applies to |
|---|---|
| DEEP | The relocation map; the H4 gate arithmetic (cross-checked against `operating_characteristics.py` and `diagnose_dev_probe_20261007.py`) |
| STANDARD | Fragment injection; harness consolidation |
| LIGHT | Description trims; the tombstone README |
| DEFER | Owner restructuring; 6.6 text compression; adapters other than OMP |

**Stop triggers.** Design §10 X1–X5. Stop when a further edit cannot change a gate outcome or the byte or line budget.

## 3. Cycle decisions and delegated D4 space

**Frozen (from the design):**
- Fragment plus build injection.
- Block shape and placement (design §5.1).
- Owner reads optional (§5.2).
- H1–H5 as the only harness functions.
- Retirement list and budgets (§6).
- Gate rules and exposures (contract v2 §4).

**Delegated:**
- Exact block wording, within the frozen shape and SD-R4.
- The fragment's tag syntax.
- How the retained harness modules are merged and named.
- Whether turn-cap enforcement needs a minimal provider proxy (≤ 250 lines) or uses an OMP setting.
- The scorer's internal structure.
- The evaluator prompt wording, under the frozen rubric.

**Simplification target:**
- Remove the 7.1 owner routing bullet and completion clause: about 8.2 KB per role becomes about 3.0 KB.
- Retire about 8.4k non-test lines outright (design §6 retirement table), plus their tests.
- Shrink the retained modules, about 11.9k lines, to the 5,000-line budget by removing their admission, observer and provenance paths.
- Replace `requal71.py`, `batch_assess70.py` and the per-stage gate scripts with one H4 scorer.

## 4. Material implementation obligations

| # | Obligation | Acceptance evidence | Shortcut to reject |
|---|---|---|---|
| O-1 | `source/shared/fragments/scientific-checks.md` with tagged lines; `build_skills.py` injects each entrypoint's subset at its marker; the six entrypoints carry markers per the role map; `repository-hygiene` none | Build output: each generated block equals the fragment subset for its tags; unit test for the injection (unknown tag, missing marker, duplicate marker fail) | Hand-editing six blocks; editing `dist/` |
| O-2 | Entrypoint text outside the block and description stays byte-identical to `22f4bdba` | A test diffs each source entrypoint against `git show 22f4bdba:` after removing the block and description | Re-flowing 6.6 text "while there" |
| O-3 | Lossless relocation: a map from every clause removed from the 7.1 entrypoints (`58fd67b`) to its exact owner home; missing homes appended to an owner section "Completion detail" | Map file under `qualification/ssdp70/qual-v2/`; independent relocation check record | Claiming "covered by the owner" without a locator |
| O-4 | Block sizes ≤ 3,000 B per role and ≤ 1,600 B per specialist; descriptions ≤ 60 words | Static test over the generated `dist/` | Moving required actions into the owner to meet bytes, which breaks design principle 1 |
| O-5 | Owner routing bullet removed from the routing lists; the block's depth sentence names the owner and the R2 situations as recommended reading | Text test; the P7 tests updated to the new consumed surface (negative cases: a block missing a delegate question or element fails) | Leaving both the old bullet and the new block |
| O-6 | Harness H1–H5 consolidated under `qualification/ssdp70/eval/` (or `qual-v2/`); retired modules deleted from the working tree with a tombstone README (module → last commit) | Line counts ≤ 5,000 non-test and ≤ 2,500 test; integration test launches a real bubblewrap OMP episode with the scripted stub delegate; pins test | Deleting before the new harness passes; replacing the real launch with a mock |
| O-7 | The H4 scorer implements contract v2 §4–§7 exactly, including δ(n, p̂), the McNemar rule, Q2's k-table, the ambiguity rule and the report | (a) Unit tests of each rule against `operating_characteristics.py` values; (b) re-scoring the 2026-10-06/07 dev-probe runs reproduces `diagnose_dev_probe_20261007.py` G1–G4 figures | Scoring advisory regex verdicts as binding |
| O-8 | Evaluator calibration set (20 items, ≥ 5 known failures) and the oracle known-good and known-bad fixtures, kept as precondition-C inputs | Files frozen and pinned; the instrument check runs in H4 | An evaluator that shares the executor model |
| O-9 | Release documents: CHANGELOG entry for the new label (after SD-R6), README routes intact, `history/SEMANTIC_EVOLUTION.md` entry for the qualification-philosophy change; the 7.0 workplan §8.2/§8.3/§11 amended by pointer to the design | Repository acceptance release-document checks | Putting release identities into README |
| O-10 | 8.0 inputs (design §7) appended to the 8.0 workplan through its change control, as an inputs list only | Diff limited to an inputs section | Starting 8.0 design work |

## 5. Evidence and dependencies

**Reused, still applicable:**
- The 2026-10-06/07 dev-probe artifacts, as the regression oracle for H4 only.
- The historical records, as lessons (design §1).

**Stale for the candidate:**
- Every 7.1 run.
- Every contract rev 16 floor computation.
- The executor and evaluator admissions.

**New evidence realizations required:**
- The development probe (stage S4).
- Then a campaign (separate work order), with fresh fixtures, the A/A run and the calibration set.

## 6. Affected surface and acceptance

**Affected surface:**
- the six entrypoints;
- the fragment;
- `build_skills.py` and its tests;
- `dist/skills/*`;
- the orchestrator protocol snapshot;
- the P7 tests (`tests/test_protocol_70_*`);
- the owner (append only);
- the harness tree;
- `requal71/` operator material, now superseded for P3 by a v2 work order;
- the CHANGELOG, history and README routes;
- the 7.0 and 8.0 workplans.

**Required checks:**
- repository acceptance per README/CI: inherited regression, package build plus independent validation, dist parity, whitespace, frozen-resource integrity, `generate_protocol_snapshot.py --check`;
- O-1 to O-8 tests;
- harness integration with a real bubblewrap launch;
- H4 regression on the dev-probe artifacts;
- the line and byte budget checks.

**Production qualification.** A campaign under contract v2 is required for any qualification claim. It is outside this workplan and needs fresh fixtures (P3).

## 7. Authority, documentation and history impact

- **D3 and workplan.** The 7.0 workplan §8.2/§8.3/§11 change through the design, after the independent check and SD-R1/SD-R3. Contract rev 16 is superseded by v2 on SD-R1. Rev 16 is preserved unchanged as history.
- **D4 specification.** The P7 tests encode the new consumed surface.
- **History.** `history/SEMANTIC_EVOLUTION.md` records the shift from absolute floors to calibrated comparative gates, and the reason (design §1).
- **Generated outputs.** `dist/` and the orchestrator snapshot are regenerated, never hand-edited.

## 8. Stages

| Stage | Content | Gate to next |
|---|---|---|
| S0 | Independent check of the design and contract v2; stakeholder SD-R1..R8 | PASS and decisions recorded |
| S1 | Skill: O-1 to O-5, regenerate, P7 tests, relocation check (independent) | Repository acceptance green; relocation check PASS |
| S2 | Harness: O-6 to O-8, retirement after the new harness passes | Budgets met; H4 regression reproduces the dev-probe figures |
| S3 | Release documents and workplan pointers: O-9, O-10; independent D4 Review of S1–S3 | Review PASS |
| S4 | Development probe (disclosed corpus, development purpose, pre-registered): GLM-5.3-Flash (plus the optional flash-tier comparison model); p66 vs candidate; Q2 and Q3 direction; A/A preview | X1 not triggered → commission P3 custodian and campaign work order under contract v2 |

## 9. Reopen and Challenge triggers

- **D4-local:** a test failure; a budget overrun attributable to implementation.
- **D3 reopen:** design §10 X1–X5.
- **D2/D1:** none expected. Any finding that a Protocol 7 element's meaning is wrong routes to the doctrine owner as a SERIOUS CHALLENGE.
- **Additive-repair guard:** any added clause, gate or module must show its byte, line and compound-probability cost (X5).

## 10. Final handoff

Lead with:
- any Serious Challenge or blocker;
- the gate state of S0–S4;
- measured block bytes per entrypoint;
- harness line counts (before and after);
- the relocation-check verdict;
- the H4 regression result;
- the development-probe Q2/Q3 figures with the A/A preview.

Unexecuted required checks are blocking.
