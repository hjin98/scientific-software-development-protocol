---
kind: qualification-diagnostic-probe
governing_protocol_version: 6.6.0
target_protocol_version: 7.0.0
date_utc: 2026-10-04
status: development-data-not-qualification-evidence
---

# Stage 7 M07 doctrine-loaded probe

**Question.** Does Protocol 7's delegate-request duty change agent behaviour once the doctrine is actually loaded? Does the fixture's "scripted" cue suppress it? This is the follow-up recommended in `STAGE-7-M07-DELEGATE-REQUEST-AND-TREATMENT-DELIVERY-DIAGNOSIS-2026-10-04.md` §6.1.

**Answer.**
1. **Yes, the duty has a real effect specific to Protocol 7 once loaded.** With the skill loaded, p70 asked at least one owed part in 6 of 14 episode-variants, while p66 asked none in any (all 6 discordant pairs favour p70; sign test p ≈ 0.03).
2. **Uptake is far below the contract floor.** The floor is 100% of owed parts. Even loaded and de-cued, p70 asked 10 of 25 owed parts in their core form and 8 of 25 under the strict reading. Only 1 of 7 episodes was fully conformant in either variant. The tension-search part was almost never asked.
3. **Removing the fixture cue raised uptake** from 6/25 to 10/25 owed parts (core). With one replicate this is suggestive, not established.

Protocol 7.0 remains NON-QUALIFIED. This probe is development data: the fixtures were already non-blind, scoring was by the diagnostician and not arm-blind, and nothing here is admissible qualification evidence.

## 1. Design

**Episodes and arms.** The seven Stage 7 M07 episodes (C042, C044, C046, C048, C050, C052, C055) were run once each, in both arms (p66, p70), in two variants: 28 runs.

**Execution path.** Every run used the same path as the frozen semantic matrix:
- `harness70.py matrix --adapter omp --mode probe` from the exact-head worktree `411510ed96c0`;
- profile key `d4572470…`, model `deepinfra/zai-org/GLM-5.3-Flash`, 30 turns / 900 s;
- the campaign's `arms.json`, profile and capabilities;
- the custodian *public* executor package (no keys), copied and modified as below.

The profile freezes the supervisor interpreter, so the harness must run under `/usr/bin/python3` (3.10). Under 3.13 the adapter refuses before launch.

**Variants.**

| Variant | Change from the Stage 7 corpus |
|---|---|
| A — pinned | `entry: pinned:software-implementation`. The harness renders this as "Use the software-implementation skill. {prompt}", the contract §4 reference explicit activation. |
| B — pinned + de-cued | As A, plus:<br>• `returned_envelope` removed from the seven case files;<br>• "; delegate is scripted, not SSDP governed" removed from their scope;<br>• the README sentence saying the mediator supplies scripted delegate returns removed.<br>Delegate returns still come unchanged from the stubs. |

All 28 runs were `COMPLETE_ADMISSIBLE`, and every one recorded `root_selection = software-implementation` (`explicit-instruction-skill-read`).

**Scoring.** Each delegate instruction was scored per owed part under the workplan §11.3 *Request* rule. The owed parts per episode are the same as in the Stage 7 scoring: findings F, null N, variant V and tension T, 25 in total.
- **Core:** the part is asked in answerable-either-way form. "Report any findings" fails.
- **Strict:** core, plus:
  - launched-work coverage;
  - the null envelope requested if results were realized;
  - "changes made after seeing results" in the variant part;
  - searched, unreachable and found records with entries, binding and asserter in the tension part.

Follow-up delegate calls within an episode count; this is flagged where it matters. The per-part rationale is in `scores.json`.

## 2. Results (owed parts asked, of 25)

| Arm / variant | Stage 7 (no root loaded) | A — pinned | B — pinned + de-cued |
|---|---|---|---|
| p66 core / strict | 0 / 0 | 0 / 0 | 0 / 0 |
| p70 core / strict | 1 / — | **6 / 4** | **10 / 8** |
| p70 episodes asking ≥ 1 part | 1 / 7 | 2 / 7 | 4 / 7 |
| p70 episodes fully conformant (core) | 0 / 7 | 1 / 7 (C052) | 1 / 7 (C055) |
| p70 tension part asked (of 4) | 0 | 0 | 1 (core only) |

### Characteristic p70 behaviour
- **Conformant requests.** A-C042, A-C052 and B-C055 ask in the doctrine's own terms: findings or none; whether the work including launched tools/agents produced, ran or reviewed realized results, with a null envelope; more than one variant, including changes after seeing results. A pre-matrix smoke run (A-C042-p70, excluded from the table) also asked all four parts in core form.
- **Plain relays.** Most remaining requests still relay the task ("Read cases/C048.json … Report only; do not launch work"), even with the doctrine loaded.
- **Reactive follow-ups.** In B-C042 and B-C044 the owed questions came only in a *second* call, after the delegate's bare return. The duty fired reactively, not at request time. A stricter reading of §11.3 (the delegator's request) would score these lower.
- **Fixture artefact.** In B-C048 the delegator invented a different task (an S01–S11 review of `cases/atlas_study.json`). Removing `returned_envelope` also removed the only description of the rename work, so this run reflects the change to the fixture, not the doctrine.

p66 asked no owed part in any variant. A-C055-p66 listed envelope fields ("findings, result, variants coverage, upstream search"), which does not meet the either-way form.

## 3. Interpretation

1. **Delivery was the first-order problem, and the doctrine is not inert.** Loading the skill moves p70 from about 0 to 6–10 of 25 owed parts and leaves p66 at 0.
2. **The duty, as written, is followed unreliably.** Even when loaded it is often not applied at the moment of delegation, and its most demanding part (tension search with entries, binding and asserter) almost never appears. This fits the salience hypothesis: the duty is one clause in a roughly 2 KB obligation paragraph of each role entrypoint. A redesign could test a short, checklist-shaped request template at the delegation point. This is a hypothesis, not a finding.
3. **The fixture cue matters.** Telling the delegator that the delegate is scripted, and showing its return in advance, plausibly suppresses requests. The Stage 7 fixtures confound doctrine with this cue. Future fixtures should keep the delegate scripted (§11.3) without signalling that to the delegator. They should also keep a task description that does not rely on the pre-stated return.

## 4. Limits
- One replicate per cell, one executor model and one route (software-implementation), chosen by the diagnostician for every case.
- No result here bears on other models or routes.
- Scoring is a single unblinded judgment by the diagnostician.
- Other measures in these runs were not scored.

## 5. Record

**Probe root:** `/home/samjin/ssdp70-omp-stagef/probes/M07-DOCTRINE-LOADED-20261004T131829Z/`. It contains:
- the corpora;
- the runs (`runs-A-pinned/`, `runs-B-pinned-decued/`, excluded `smoke/`);
- the matrix logs;
- `scores.json`, `tally.py` and `tally.txt`.

**Custody (contract §1 item 9(d)):**
- The host is single-UID and reads are unauditable.
- The probe read only the custodian *public* executor package. No withheld keys were opened.
- The frozen Stage 7 trees were not touched.
