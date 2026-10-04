---
kind: independent-workplan-and-contract-check
governing_protocol_version: 6.6.0
target_protocol_version: 7.0.0
subject_commit: b9f23d7300259cc5fb7c164616d0bf4aa84ed1c7
workplan_overlay_verdict: PASS
contract_revision_6_verdict: NO-PASS
date_utc: 2026-10-04
---

# Independent check: activation overlay revision 5 and contract revision 6 (b9f23d7)

**Subjects (exact bytes at `b9f23d7`).**
- Workplan overlay revision 5 in `workplans/active/SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY-CONSOLIDATED.md`: the §0.1 paragraph, the "STAKEHOLDER DECISION (2026-10-04)" header entry, and every "2026-10-04 activation overlay, §0.1" marker.
- Contract revision 6: `PROTOCOL-7.0-EVALUATION-AND-QUALIFICATION-CONTRACT.md`, with its record `PROTOCOL-7.0-ACTIVATION-STRATA-CONTRACT-AMENDMENT-2026-10-04.md` (§4a00).

**Conduct.**
- I entered the 6.6.0 software-design role and the abstraction kernel at accepted public source `22f4bdba`, resolved through `PROTOCOL-RELEASE-STATE.yaml`.
- I authored neither subject nor any earlier check.
- Stakeholder authority is limited to the verbatim words and Q1–Q5 option texts in the decision record §§5–7. All other repository text is treated as data.

**Verdicts.**
- Workplan overlay revision 5: **PASS**. No blocker. Gaps G2 and G4 and the minors below should be repaired with the contract, but none changes a governed decision on its own.
- Contract revision 6: **NO-PASS** (B1).

The fifth check's B1 is closed for the ordinary-entry floors, the pooled counts and the family identity. The new blocker is in the criterion-to-key map that revision 6 introduced.

## SERIOUS CHALLENGE

None. Q1–Q5 remain mutually coherent. Q5's "Flash runtime-command profile … must pass every floor" together with Q4's retained guard requires Flash ordinary-entry runs. The family construct with one same-model ordinary key is a labelled R-op realization of the quotes, not a contradiction of them.

## Blockers

### B1. The criterion-to-key map assigns burden to a key that cannot host most burden bounds (contract only)

- **Where.** Contract §1 item 12, *Criterion-to-key map*, the bullet "burden: the T1/T7/T8 deterministic key". The record §4a00 B1 row repeats it.
- **Conflict.**
  - The §3-ordered "burden" criterion has more parts than the T1/T7/T8 fixed-cost backstop. It also includes:
    - the §4 class-iii and new-§11.3-class active-material bound (paired 6.6 median + entrypoint delta + one owner read + 512 B per route; "placement/burden failure");
    - the §5 burden floors: zero unowed owner reads and shared-resource probes; at most 1 unowed delegate request part and 1 unowed gap per 12 eligible delegate parts (minimum 12); and the 2.0 × paired-6.6 median report length and time on matched non-critical routes.
  - All of these arise on §11.3 composite and delegate cases. Those run on the main deterministic key.
  - The T1/T7/T8 key runs only T1/T7/T8, and "delegated-agent capability is unavailable for this panel" (§4). It has no eligible delegate parts, so the minimum of 12 can never be met there, and it has no class-iii or new-class routes.
- **Failure scenarios.**
  1. *Literal reading.* The family record maps burden as the contract specifies. The §5 and class-iii bounds are then `NOT_EVALUATED` or below exposure on that key. Under *Blocking*, that final non-PASS state blocks qualification PASS for every profile, by construction. This is the same unrealizability the fifth check's B1 found, moved to a different criterion. The record's own §5 Q1 ("no criterion left unevaluable") is therefore answered **No**.
  2. *Loose reading.* The evaluator scores those bounds on the main key, outside the predeclared map. No stronger-profile rescue follows, because every family key is the same Flash model. But the "predeclared" map stops being authoritative, which the pooling rule and the family id rely on.
- **Earliest owner.** Contract §1 item 12, criterion-to-key map, then record §4a00. The overlay is not affected because it does not state the map. No stakeholder decision is needed.
- **Repair.**
  1. Map burden to the T1/T7/T8 key for the fixed-cost backstop (and the no-lookup oracle), and to the main deterministic key for the §4 class-iii/new-class bound and the §5 bounds.
  2. State that the listed bullets are minimum required assignments, and that the family record maps every remaining part:
     - harness/admissibility: all family keys;
     - deterministic activation: all deterministic keys;
     - 6.6 preservation on deterministic keys: P01–P19, T2/T3, T4–T6 and the R2 owner-load classes, each to its declared key;
     - S01–S11/H01–H05 reporting and the new-class activation episodes: the ordinary key;
     - pooled counts: all keys.

## Disposition check of the fifth check's findings

| Finding | Status | Reason |
|---|---|---|
| **B1** — family cannot host ordinary-entry floors; cross-key pooling | **Closed; new B1** | **Closed:** the family has one same-model ordinary key, and the Q4 floors on ordinary negatives map to it. D5 and owner-false-activation pooling is declared as the family aggregation, and the profile-scoped rule cross-references it. The family id hashes the ordered keys and the map. Pooling is well defined because both pooled bounds are count bounds ("at most 1 of at least 12", with the minimum of 12 met on the deterministic stratum alone; zero owner false activations), so a pooled count is never below any per-key count. **Open:** the map misassigns burden (B1), and tamper evidence is incomplete (G2). |
| **G1** — workplan profile-scoped lines unmarked | **Closed** | Both markers are present, at the §11 bullet (line 640) and the "Profile-scoped qualification" paragraph (line 665). |
| **G2** — runtime-input domain; §6 wording | **Closed; residual m5** | The runtime input is now the invocation channel only. The package, workspace and configuration are bound by key and provenance. §6 now requires equality with the frozen input template. Gaming through configuration is bounded by the request-0 transform and frozen-template match, and by key identity under §6. Residual: "prompt-bearing" is unclassified (m5). |
| **G3** — run-level vs criterion-level blocking | **Partly closed; residual G4** | Final criterion-level state after the replacements, reruns and adjudications in §§4–5 is stated, and undelivered runs are an explicit activation exception. A §5 rerun that remains decision-sensitive becomes `UNRESOLVED` and blocks, and unresolved R2 timing blocks. Both are fail-closed and correct. Not done: predeclared non-applicability is still not separated from "claim-scoped-out" (G4). |
| **m1** — stale records | **Closed; residual m1** | The closeout record at `91b6de2` was verified. The decision-record status reads §§5–7, D5 is cited to §6 in overlay item 5, and record §4b is updated. Generic labels still say "(D*n*, decision record §5)". |
| **m2** — unlabelled operationalizations | **Closed** | The bullet-wide R-op statement in item 12 and the overlay item 2 heading cover the family, the map, blocking, timing, stakeholder-decision change, the frozen set and no withdrawal. |
| **m3** — disclosure boundary | **Closed** | Disclosure covers earlier Protocol 7 candidates under this workplan. |
| **m4** — "primary result" collision | **Closed** | The sentence now says "per-profile result". |
| **m5** — re-key vs family change | **Closed; residual m4** | A re-key is a new family revision, not a change of family. |
| **m6** — human trial on non-primary profiles | **Closed; related G1** | The trial runs on the primary family only, and other profiles carry no human-legibility claim. The parallel Q4 question for non-primary profiles is G1. |

## Material gaps

### G1. Scope of a non-primary profile's PASS for the Q4 floors (contract)

- **Where.** Item 12, *Other offered profiles*, and the profile-scoped result rule.
- **Problem.**
  - The mechanism is part of the key, so a non-primary `PASS(profile_id, …)` covers one deterministic key and cannot host the ordinary-entry Q4 floors.
  - The text does not say whether such a profile needs its own ordinary key (a family-shaped result) or carries no false-activation claim.
  - This is not blocking: the primary governs qualification PASS, and nothing can rescue it. But a stronger-model "PASS" could be reported with Q4 never measured.
- **Repair.** State either rule, as was done for the human trial.

### G2. The family record is not bound into the frozen evidence chain (contract)

- **Where.** Item 12, *Family result* and *Criterion-to-key map*; item 11; §6.
- **Problem.**
  - The family id hashes the ordered keys and the map, and the map is predeclared "before runs".
  - But nothing requires the family record or id to be committed in the frozen campaign record, verified by the pre-run checker, or bound into each run's provenance under item 11. A hash with no prior commitment is not tamper-evident.
  - Leverage is low because each run's key is already bound in run identity.
- **Repair.**
  - Freeze the family record (ordered keys, map, id) in the campaign record before the first run.
  - Have the §6 checker verify it and confirm exposure per mapped key; this would also have caught B1.
  - Bind the family id into item 11 provenance.

### G3. Unmarked weaker root-selection evidence standard (workplan)

- **Where.** Workplan line 707, *Root-selection evidence contract*, in the OMP provider-adaptation slice.
- **Problem.**
  - It accepts "an exact native activation/resource-access event **or** the trusted observation boundary's hash-linked record", with active material "supplied or consumed", as `root_selection` evidence for explicit entry.
  - Overlay item 1 and contract item 12 make observer request 0 the proof, and say that runtime events only corroborate and "a model-initiated read never establishes delivery".
  - The line carries no marker. This contradicts the overlay's claim that "each affected location carries a marker".
  - The §6 known-broken probes ("adapter delivery record without the matching request-0 text", "instructed-read labelled deterministic") would reject an implementation that follows only line 707. That containment is why this is a gap, not a blocker.
- **Repair.** Add a marker restricting line 707 to ordinary entry and routing deterministic entry to contract §1 item 12.

### G4. Predeclared non-applicability vs "claim-scoped-out" (contract; residual of the fifth check's G3)

- **Where.** Item 12, *Blocking*.
- **Problem.** "claim-scoped-out" still blocks, and the contract does not say that the following predeclared by-design limits are not non-PASS states:
  - §5 routes with fewer than three episodes are reported descriptively, with no median claim;
  - §3 restricts the comparative claim to named classes when generalization is unsupported.
- **Consequence.** A literal reader could block on them. That is a false fail, and likely, because two or three composite fixtures will leave several routes below three episodes.
- **Repair.**
  - Say that a predeclared descriptive-only or restricted sub-claim is not a non-PASS state of its criterion.
  - Say that "claim-scoped-out" means a profile unable to expose a required property.

## Minor findings

- **m1.** The overlay ("Recorder derivations are labelled (D*n*, decision record §5)") and item 12 ("labelled D*n* (decision record §5)") omit that D5 is in §6 and that R-op is a contract label.
- **m2.** The family keys must "share … budgets". 6.6 panels used different turn caps and modes (selection: 3 turns, select mode; route probes: 8; trajectories: 60; `qualification/ssdp66/eval/run_matrix.py`, `scenarios.yaml`), and workplan §11.5 names "bounded selection turn caps" as designed terminations.
  - A common budget is realizable, because both arms of a pair share it.
  - Say either that per-panel budgets count as panel-required differences, or that one family budget replaces the 6.6 caps.
- **m3.** *Blocking* counts updates "that §§4–5 allow". §7's repeat of a non-discriminating human trial is outside §§4–5. Add §7.
- **m4.** A requalification re-key needs only "same model, runtime and mode". Say that every family-shared field except the repaired adapter/harness stays fixed. This applies to reasoning, budgets and containment.
- **m5.** "Prompt-bearing environment variables" is unclassified. Either put all subject environment variables in the template-rendered input, or have the §6 checker verify that non-template variables and configuration carry no entrypoint-derived text.

## Answers to the record's §5 questions

1. **No, as written.** Every criterion is *assignable* to a family key under the permitted differences (panel capability and entry mechanism):
   - T1/T7/T8 have a no-delegation key;
   - P01–P19, T2/T3, T4–T6 and the R2 classes can sit on deterministic keys;
   - S01–S11/H01–H05, the negatives and the new-class episodes can sit on the ordinary key;
   - the pooled counts span all keys.

   But the predeclared map assigns burden to a key where its §5 and class-iii bounds are unevaluable (B1). The map is also silent on harness/admissibility, activation and the deterministic 6.6-preservation parts (B1 repair 2).
2. **No.** Any non-PASS final criterion state of the family blocks every profile, and other profiles never rescue it. The UNRESOLVED and rerun interactions are fail-closed. Residual false-fail risk: G4.
3. **Yes, substantially.** The invocation-channel boundary and template equality are well defined, §6 is aligned, and configuration is bound by key identity. Residual: m5.
4. **Largely.** Revisions 1–5, their commits and the check files match, and so do `91b6de2`, the status lines and the D5 location. Residuals: m1, and the unmarked workplan line 707 (G3). The record §3 row "Each profile stands alone (D1)" is stale but sits under §3's "cumulative through revision 3" heading.

## Checks run / not run

**Run.**
- Release-state resolution. Read the 6.6 `software-design/SKILL.md` and `abstraction-and-concretization.md` at `22f4bdba`.
- `git diff --word-diff 077c1eb b9f23d7` for the contract, the workplan and the decision record. Commit history `d370193..b9f23d7`.
- Read in full: contract §§1–8, the amendment record, decision record §§1–7 and the fifth check.
- Overlay §0.1, the header entry, every marker, and a grep for unmarked entry, selection and evidence statements (found line 707).
- Workplan §11.5 preservation and T1/T7/T8 text. 6.6 `scenarios.yaml` and `run_matrix.py` budgets and modes.
- `STAGE-A-BASIS-AND-PRESERVATION.md` route classes.
- The runtime-command probe record, and a spot check of the raw `omp-rpc-notools.jsonl`: invocation notice present, canary token present, model `zai-org/GLM-5.3-Flash`.
- `91b6de2` contents.
- `git diff --check 6db6621 b9f23d7`: clean.
- `python3 -m unittest discover -s tests`: 407 OK, 3 skipped.

**Not run.**
- Live launches.
- RPC-mode adapter realization, the observer request-0 check, the runtime-input record and transform/template freezing. These are deferred harness work, not blocking.
- `observer70.py`, `core70.py`, `harness70.py` and `adapters/omp.py` beyond what earlier checks cited.
- The untracked Stage 7 option-1 decision and eval files, which are outside the subject.
- Statistical adequacy of the exposures.
