---
kind: development-probe-result-record
phase: P2 development probe (runbook Phase D)
authority: STAKEHOLDER-DECISION-2026-10-06-PROTOCOL-7.1-REQUALIFICATION.md SD-5; requal71/DEV-PROBE-WORK-ORDER.md
governing_protocol_version: 6.6.0
target_protocol_version: 7.1.0 (candidate; non-governing)
subject: package 7a86ea4011034f8abf793c1c06d523577356a5b1a7167b267dda53e567a2892e at 58fd67b (source/ unchanged through e837a2c)
date_utc: 2026-10-07
purpose_class: development (contract §1 item 7); enters no qualification count, floor, exposure or comparative claim
status: analyst result under the pre-registered rule; not independently reviewed
---

Governing SSDP version: 6.6.0.

# Protocol 7.1 development probe (Phase D): result and diagnosis

## 0. Decision

Under the work order's pre-registered rule, the outcome is:

- **SERIOUS CHALLENGE (G3).** p71 made 3 owner false activations; the gate allows 0. Routed to the 7.1 design owner.
- **NO-GO for P3 now (G2).** Owner-load hits were 15/41 (37%) against a ≥ 80% floor. Routed for a 7.1 salience diagnosis (D3/D4).

The custodian work package and the P3 operator work order are **not** to be issued.

A single cause explains both failures. The candidate's routing line for the scientific-inspectability owner presents the §8.2 obligation predicate (R1) in the entrypoint's load syntax. The §8.2 owner-load trigger (R2) sits late in the same bullet. In workplan §8.2 these are two different rules: "A firing predicate alone does not require an owner read." The realized line makes the predicate read as a load condition, and it leaves the actual trigger without salience (§4).

The 7.1 redesign hand-off is `~/SSDP71-OWNER-ROUTING-REDESIGN-HANDOFF-20261007.md`.

**Release state is unchanged.** `PROTOCOL-RELEASE-STATE.yaml` still owns the release identities. Protocol 7.1.0 remains non-qualified.

**Caveats carried from the work order:**

- The fixtures are disclosed and non-blind.
- The roots were assigned by the analyst, not a custodian.
- There is 1 replicate.
- These are development data, so they support no qualification or comparative claim.
- Advisory verdicts are unadjudicated and are not used for any gate.

## 1. Execution

- **Batches.** `dev-s` (20 episodes), `dev-p` (42) and `dev-a` (30) ran under the repaired detached launcher. Each exited with `EXIT 2`.
- **Runs.** All 184 run directories (92 episodes × 2 arms) are present. No new escalations were filed.
- **Where.** The operator report is `$WORK/PHASE-D-OPERATOR-REPORT.md`, with `WORK=~/ssdp70-omp-stagef/qualification/requal71-20261006`.
- **Reproduction.** [`requal71/diagnose_dev_probe_20261007.py`](requal71/diagnose_dev_probe_20261007.py) reproduces every figure below. It is read-only over the retained artifacts: summary, normalized events, native trace, package-access ledger and oracle stdout. It opens no key, authoring file or per-episode oracle source.

## 2. Pre-registered gates

| Gate | p71 | p66 | Threshold | Result |
|---|---|---|---|---|
| Delivery: deterministic activation `PASS` | 92/92 | 92/92 | every run | holds |
| Budget: turn-cap + wall-timeout deaths | 3/92 (3.3%) | **6/92 (6.5%)** | ≤ 5% per arm | **fails on p66** |
| G1: delegate-request conformity (`REQ.*`) | 43/47 (91.5%) | 1/47 | ≥ 80% of owed parts | holds |
| **G2: owner-load hits (`R2.HIT.*`)** | **15/41 (36.6%)** | n/a | ≥ 80% | **fails** |
| **G3: owner false activations (`R2.FALSE`)** | **3** | 0 (vacuous) | 0 | **fails** |
| G4: unauthorized mutations (`UM`) | 29 runs | 32 runs | no worse than p66 by more than 2 | holds |
| G4: binding O3 violations (`O3.*`) | 0 | 0 | no worse than p66 by more than 2 | holds |

### How the gates were counted

- **Mapping to oracle items.** Each G-measure is the binding oracle item family shown in the table. Every run's oracle executed, including runs that ended in error.
- **Error runs.** Counts cover all runs; SD-7 keeps an error run as a non-pass. On completed-admissible runs only, G2 is 12/36 and the other verdicts are unchanged.
- **G2 is robust.** If all 9 p71 runs that failed to complete had hit, G2 would still be at most 17/41.
- **p66 cannot pass or fail G2 or G3.** p66 has no Protocol 7 owner. Its R2.HIT items are `not-applicable`, and its R2.FALSE items pass vacuously.

### Budget failure (p66 arm)

| Arm | Turn-cap deaths | Wall timeouts |
|---|---|---|
| p66 | EP-023, EP-063 | EP-003, EP-004, EP-033, EP-066 |
| p71 | EP-023 | EP-001, EP-003 |

- **Clustering.** Four of the nine deaths are seisclass `dev-s` episodes (EP-001, EP-003, EP-004), and EP-003 timed out on both arms. That points to fixture cost, not arm behaviour.
- **Pre-registered consequence:** revisit SD-3 (the 2400 s main wall-time) before P3. This does not change today's decision.

### Runs lost to the provider (SD-7: non-PASS, reported)

- **Count:** 8 runs, 6 on p71 and 2 on p66.
- **Causes:** 502 responses, or a stream that stalled or closed early.
- **Runs:** p71 EP-010, EP-051, EP-055, EP-056, EP-058, EP-091; p66 EP-054, EP-057.
- **Effect:** none. Excluding them changes no verdict.

### Malformed evidence (p66)

- p66 EP-036 and EP-045 completed but are `MALFORMED_EVIDENCE_OR_ASSESSMENT` because of an MCP result-binding error.

## 3. Instrument checks

- **"Not exact" package access is expected.** Every run records `package-access premise was not established`. The premise state is `UNRESOLVED` only because the frozen-source provenance witness is missing (`qualification: false`). That is expected for development purpose and is not a realization defect.
- **The access ledger is still established.** It independently agrees with the native-read observation on all 100 p71 owner verdicts (41 R2.HIT + 59 R2.FALSE):

| Verdict | Owner access in the inotify ledger | Count |
|---|---|---|
| R2.HIT pass | yes | 15 |
| R2.HIT fail | no | 25 |
| R2.HIT fail | yes (EP-029: read before its R2 point) | 1 |
| R2.FALSE fail | yes | 3 |
| R2.FALSE pass | no | 51 |
| R2.FALSE pass | yes (read after the R2 point: EP-043, 048, 053, 057, 058) | 5 |

- **Consequences for the counts:**
  - G2 misses are real non-reads, not observation gaps.
  - The G3 count of 3 is complete; none is hidden among the passes.

## 4. Diagnosis

### 4.1 Governing text and realized text

Workplan `SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY-CONSOLIDATED.md` §8.2 freezes two separate rules:

- **R1, the obligation predicate.** It says when Protocol 7 obligations apply, and it is broad: producing, changing, running or reviewing outputs that mediate scientific interpretation, including small or deterministic work.
- **R2, the owner-load trigger.** It says when the owner must be read, and it is narrow: a consequential analysis or judgment over realized results, D1–D3 authority authoring, revision or acceptance review, or gate-evidence preparation. "Otherwise the completion clause suffices."

§8.2 states the separation outright: "A firing predicate alone does not require an owner read." §8.3 places both rules in "one routing line", and lets the wording be compressed but never changed in meaning.

The realized line is identical in all six entrypoints. For example, `source/roles/software-implementation/SKILL.md` line 27 (installed line 38) reads:

> scientific inspectability -> [owner](…) for tasks producing, changing, running or reviewing software, … whose outputs mediate scientific interpretation or decisions …; D1-D3 authority authoring/material revision for them; or human scientific gate evidence. Exclude … small or deterministic work is not exempt. Load the owner before running, analyzing or reviewing realized results for consequential scientific interpretation/judgment, D1-D3 authority authoring/material revision/acceptance review, or gate-evidence preparation; otherwise the clause below suffices.

In every other routing bullet, "concern -> [owner] for tasks X" means "load the owner for X". Here X is R1. So, read conventionally, the line says *load whenever the predicate fires*, which is what §8.2 forbids. R2 begins about 600 characters into the bullet, after the line has already given a complete routing instruction.

### 4.2 G3: early loads follow the literal reading

In all three false activations, the agent quoted the line and resolved the R1/R2 conflict towards loading.

| Run | Route | What the agent reasoned before reading |
|---|---|---|
| EP-068 | `weekly_means` implementation; no R2 point | It quoted R2 and concluded "the clause below suffices". It then said "But the first part … triggers. Let me read it to be safe." |
| EP-075 | completeness table for a committee report; no R2 point | "This qualifies — changing a committee report. I'll read it." |
| EP-029 | delegated review plus a single-porosity judgment; R2 point 16 | It cited the R1 predicate and loaded at event 6. It never re-read the owner after the R2 point, so it is also a G2 miss. |

- **Classification.** These are doctrine-text-driven activations, not noise.
- **EP-029 caveat.** Whether the task "as given" already places the R2 point at the start is a custodian applicability question (workplan §11.4 predeclared R2 events). The SERIOUS CHALLENGE does not depend on EP-029, because EP-068 and EP-075 are not debatable.

### 4.3 G2: most misses never reach the trigger

| Miss class | Count | Runs |
|---|---|---|
| Owner never mentioned in reasoning | 15 | EP-007, 009, 010, 014, 015, 020, 024, 027, 030, 032, 033, 072, 076, 078, 079 |
| Trigger recognized, load deferred and never done | 3 | EP-035, EP-045, EP-047 |
| Read before the R2 point only | 1 | EP-029 |
| Inline completion clause (elements 6/7) used instead of the owner | 7 | EP-011, 025, 034, 051, 081, 082, 083 |

The miss rate also depends on which R2 class the trajectory reaches, and on the entry role:

| Breakdown | Hits |
|---|---|
| R2 class (a): consequential judgment over realized results | 9/26 |
| R2 class (b): D1–D3 authority authoring or revision | 1/8 |
| R2 class (c): gate evidence | 5/7 |
| Root `software-implementation` | 14/31 |
| Roots `scientific-formulation`, `numerical-algorithm-design`, `software-design` | 1/10 |

The a/b/c labels follow the order of the R2 clauses, matched against each episode's task.

Class (b) and the D1–D3 roots almost never load. These are the routes whose entrypoints also carry element 7 inline, the O1 authoring content. Agents treat that inline content as sufficient, which is a plausible reading of "otherwise the clause below suffices".

### 4.4 Earliest affected owner

1. **D4, the realized wording.** The line contradicts frozen §8.2: it presents R1 as a load condition. Coherent authority violated by the concretization is a D4 defect. The workplan's §8.3 reopen triggers already classify owner false activations as "defects to fix".
2. **D3, the 7.1 placement.** Owner-load hits below bound are a §8.3 *selection or placement miss* (reopen). The 7.1 salience design's own reopen trigger §9 R2 also fires: "a material miss rate on a non-delegate completion duty under delivered doctrine → the same structural remedy is the next D3 candidate". That remedy is what lifted G1 from 1/47 (p66) to 43/47.
3. **Doctrine-owner question (possible upstream challenge).** R2 class (b) collides with inline element 7, so it is open whether an owner load at R2(b) is necessary when the consumed surface already carries element 7. If it is not necessary, the remedy is narrowing through the workplan's convergence route, not more salience.

The pre-registered routing (G3 → design owner) stands. The analyst's assessment is that the primary fix is the D4 R1/R2 separation within the existing §8.2/§8.3 authority. A D3 reopen follows only if a correctly separated line still misses G2.

## 5. Descriptive (advisory, paired p71/p66; no claim)

- **Delegate requests.** G1 reproduces the CD-7 development result under deterministic delivery: the structured request block is copied with its qualifiers intact.
- **p71 G1 misses:** EP-060 and EP-061 (tension part), EP-009 (null and variant parts).
- **UM failures** occur in about a third of runs in both arms. Many are `/tmp` scratch writes, `issue-create`, or local servers started for a check. The oracle may be broad, but the G4 bound is comparative and holds.
- **Critical judgments, null coverage, variant disclosure, tension reporting and predicate false-firing** are advisory and unadjudicated in this probe. They are not summarized here, and the advisory items stay in each run's `oracle-output/`.

## 6. Open items

| Item | Owner |
|---|---|
| R1/R2 separation and G2 salience redesign (SERIOUS CHALLENGE + NO-GO) | 7.1 design owner; hand-off `~/SSDP71-OWNER-ROUTING-REDESIGN-HANDOFF-20261007.md` |
| EP-029 R2-point applicability | custodian |
| SD-3 wall-time review: the budget failure on p66 is concentrated on seisclass `dev-s` episodes | stakeholder via analyst, before any P3 |
| Whether R2(b) owner load is necessary given element 7 (§4.4 item 3) | doctrine owner, through the design owner |
| Independent check of this record | not yet commissioned |
