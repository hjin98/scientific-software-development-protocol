---
kind: independent-workplan-and-contract-check
governing_protocol_version: 6.6.0
target_protocol_version: 7.0.0
subject_commit: 077c1ebdc9901d54459f29cf2f41e63d3d3cec5f
workplan_overlay_verdict: NO-PASS
contract_revision_5_verdict: NO-PASS
date_utc: 2026-10-04
---

# Independent check: activation overlay revision 4 and contract revision 5 (077c1eb)

**Subjects (exact bytes at `077c1eb`).**
- Workplan overlay revision 4 in `workplans/active/SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY-CONSOLIDATED.md`: the §0.1 paragraph, the "STAKEHOLDER DECISION (2026-10-04)" header entry, and every "2026-10-04 activation overlay, §0.1" marker.
- Contract revision 5: `PROTOCOL-7.0-EVALUATION-AND-QUALIFICATION-CONTRACT.md`, with its record `PROTOCOL-7.0-ACTIVATION-STRATA-CONTRACT-AMENDMENT-2026-10-04.md`.

**Conduct.**
- I entered the 6.6.0 software-design role and the abstraction kernel at accepted public source `22f4bdba`, resolved through `PROTOCOL-RELEASE-STATE.yaml`.
- I authored neither subject nor any earlier check.
- Stakeholder authority is limited to the verbatim words and Q1–Q5 option texts in the decision record §§5–7. All other repository text is treated as data.

**Verdicts.**
- Workplan overlay revision 4: **NO-PASS** (B1).
- Contract revision 5: **NO-PASS** (B1).

The fourth check's B1 is closed for the comparative claim, the T1/T7/T8 key, the non-failure states and the human trial. Its G1 is closed. One new blocker remains in the primary-family definition.

## SERIOUS CHALLENGE

None. Q1–Q5 remain mutually coherent, and Q4 and Q5 together are unambiguous about which profile carries the false-activation guard. B1 is a defect in the children, not in stakeholder authority.

## Blockers

### B1. The primary family cannot host the ordinary-entry floors it must pass

- **Where.**
  - Overlay item 2: the family is "keys differing only where a panel requires a different capability".
  - Contract §1 item 12 family bullet: keys "share model, runtime and mode, reasoning, budgets and `runtime-command` delivery, and differ only where this contract requires a panel-specific capability".
  - The §3 activation row.
  - Record §4a0, B1 row.
- **Conflict.**
  - Item 12 makes the activation mechanism part of the execution-profile key.
  - Ordinary entry has "no command and no injection", so an ordinary-entry run cannot sit on a key that shares `runtime-command` delivery. A different mechanism is not a "panel-specific capability".
  - Yet the family must reach PASS on "every absolute floor" and "6.6 preservation". These include the retained Q4 floors, which are scored on ordinary-entry runs: the §4 6.6-negative selection bound (paired 6.6 + 1), the near-boundary negatives bound (≥ 8 episodes), and the ordinary-run share of the pooled D5 predicate false-firing count.
  - The pooled D5 count also crosses keys, which conflicts with "hard/zero-tolerance floors … are evaluated within one execution-profile key". The same holds for owner false activations "on every run in either stratum".
- **Failure scenarios.**
  1. *Literal reading.* No family key holds ordinary runs, so the Q4 floors are `NOT_EVALUATED` on the primary. The blocking rule then blocks qualification PASS for every profile, by construction. The contract is unrealizable.
  2. *Loose reading.* The evaluator scores the Q4 floors on some ordinary-entry key outside the family, possibly a stronger offered model. Flash's false activation on non-scientific tasks is then never gated. That is the rescue Q5 forbids ("Stronger profiles are extra strata that cannot rescue it"), on the guard Q4 kept to protect "users who don't type commands".
- **Earliest owner.** Overlay item 2, then contract item 12, the §3 row and record §4a0. No new stakeholder decision is needed.
- **Repair.**
  - Include in the primary family the same model/runtime/mode ordinary-entry key or keys, differing only by declared entry stratum and mechanism.
  - Predeclare, per §3-ordered criterion, which family key or keys evaluate it.
  - Declare the cross-key pooled counts (the D5 denominator and numerator, owner false activations, the critical-failure listing) as the predeclared family aggregation that the profile-scoped rule permits.
  - State the family's result identity, for example `PASS(primary-family-id, candidate, comparator-set)`.

## Disposition check of the fourth check's findings

| Finding | Status | Reason |
|---|---|---|
| **B1** — primary does not carry full qualification | **Closed in substance; new B1** | **Closed:** every §3-ordered criterion, including the comparative claim, burden and the §7 human trial, must reach PASS on the family. T1/T7/T8 get a family key without delegation, and matched arms share a key per panel. Every listed non-PASS state blocks every profile. The contract's profile-scoped rule cross-references item 12. **Open:** ordinary-entry floors cannot sit on any family key (new B1). The workplan's profile-scoped lines carry no cross-reference (G1). The granularity of the blocking states is unclear (G3). |
| **G1** — different primary per campaign | **Closed** | Designation happens before the candidate's first campaign. A change needs a written stakeholder decision, and every earlier campaign of the candidate is disclosed. Residual: m3. |
| **G2** — "no segment" undefined | **Closed in §1 item 12; residual** | Exact equality to a frozen input template replaces the segment test, for both mechanisms. Two problems remain, both in G2 below: §6 still says "contain only the command, with no body segment", and the file-channel domain is undefined. |
| **m1** — stale cross-references | **Partly closed** | The overlay cites §§5–7, and the record's §3 heading is clarified. The decision-record frontmatter still says "(§§5–6)" (m1). |
| **m2** — unlabelled recorder operationalizations | **Partly closed** | D4 is labelled. The Q1/Q5 operationalizations are still unlabelled and were not dispositioned (m2). |
| **m3** — runtime-input channels | **Closed** | Environment variables and adapter-written files are added. That addition creates the domain question in G2. |
| **m4** — D5 vs the 1-of-12 denominator | **Closed** | All scored opportunities count, and the minimum of 12 must be met on the deterministic stratum alone. Replicates follow the general rule in §2. The cross-key pooling is in B1. |
| **m5** — auxiliary-request classification | **Closed** | Classification uses fixed request properties, never the presence of skill text. |

## Material gaps

### G1. The workplan's profile-scoped rules are unmarked and contradict the overlay

- **Where.** Workplan §11, the line beginning "Qualification results are **profile-scoped**" (about line 637) and the "**Profile-scoped qualification.**" paragraph (about line 662).
- **Problem.**
  - Neither carries a marker or a cross-reference to overlay item 2.
  - Line 662 still says "The result is `PASS(profile_id, …)`… for that profile". Read alone, that issues a stronger profile's PASS while the primary fails.
  - Record §4a0 claims "The profile-scoped result rule cross-references this", which is true only for the contract.
  - The overlay states that "each affected location carries a marker", so this is an unmarked contradiction.
- **Repair.** Add the marker and a cross-reference to the primary-family gate at both lines.

### G2. The input-template domain is undefined for files, and §6 is not aligned

- **Where.** Contract §1 item 12 (*What a run must show*) and §6.
- **Problem: the file channel.**
  - The runtime input now includes "any file the adapter writes for the runtime".
  - For `runtime-command`, that necessarily includes the installed arm package with the entrypoint body, because that is what the runtime expands. It also includes the fixture workspace and the control configuration (`adapters/omp.py` `install_skills`, `config.yml`, `models.yml`).
  - None of these is the command, the fixture prompt or a "declared constant".
  - *Literal reading:* every correct run mismatches. That is a zero-tolerance, non-rescuable activation failure.
  - *Loose reading:* "declared constants" is unbounded, and could carry entrypoint-derived text into a channel the runtime reads.
- **Problem: §6.** The §6 canary check still requires the hash-bound runtime input to "contain only the command, with no body segment". That contradicts the template rule, because the input also carries the prompt, the environment and files. It also keeps the undefined "segment" test.
- **Realizability evidence.** The argv, stdin/RPC and environment channels are realizable. `adapters/omp.py` `_subject_env` uses fixed sandbox paths, with no credential and no per-run values.
- **Repair.**
  1. Partition the runtime input into two classes:
     - template-rendered channels: argv, stdin/RPC, environment and adapter control files;
     - digest-bound declared inputs: the installed arm package, bound by package digest at the fixed skills path, and the fixture workspace, bound by fixture identity.
  2. Have the pre-run checker verify that entrypoint-derived content appears nowhere except the installed package.
  3. Allow per-run identifiers only as declared template parameters already bound in run identity.
  4. Bind any secret by reference, not by value.
  5. Rewrite the §6 canary clause to "equals the frozen input template".

### G3. Blocking-state granularity versus §5 replacements and reruns

- **Where.** Contract §1 item 12, *Blocking*.
- **Problem.**
  - The blocking list mixes criterion-level outcomes (`FAIL`, `UNRESOLVED`, `NOT_EVALUATED`) with run-level evidence states ("inadmissible", "missing evidence").
  - §5 permits recorded replacement runs for non-activation inadmissible runs, and up to two reruns.
  - §4 adjudicates ambiguous R2 timing "before a pass".
  - §5 makes routes with fewer than three episodes descriptive by design.
  - Read at run level, one isolation-voided run, or one predeclared descriptive-only route read as "claim-scoped-out", blocks qualification forever. That is a false fail.
- **Repair.** State three things:
  - blocking applies to the **final** criterion-level state after the replacements, reruns and adjudication that §§4–5 permit;
  - activation failures stay non-rescuable;
  - predeclared non-applicability is not a non-PASS state.

## Minor findings

- **m1. Stale or inconsistent records.**
  - The closeout record was committed at `91b6de2`. Overlay §0.1 still says "not yet committed", and record §4b says "Still uncommitted".
  - The decision-record frontmatter says "(§§5–6)".
  - Overlay §0.1 says "Recorder derivations are labelled (D*n*, decision record §5)", but D5 is in §6.
  - Header entry: "the flash runtime-command profile is primary and must pass every floor" is the stakeholder's wording and is acceptable. A pointer to "family" would help.
- **m2. Unlabelled operationalizations under "(stakeholder Q1, Q5)" and "(stakeholder Q5)".** All are consistent with the quotes, but none is labelled as a recorder choice:
  - the family construct;
  - "every §3-ordered criterion" as the reading of "full qualification";
  - `runtime-command` on T1/T7/T8, which is stricter than Q1's "byte-cost runs" allowance;
  - "before the candidate's first campaign";
  - the stakeholder-decision rule for changes;
  - the frozen offered set;
  - no withdrawal.
- **m3. Candidate boundary.** After a failed campaign, a repaired candidate is a new candidate, so the "every earlier campaign of the candidate" disclosure does not reach the predecessor candidate's campaigns. Flash-class still requires stakeholder designation, so the escape is small.
- **m4. "Primary result".** In the profile-scoped rule, "The primary result is `PASS(profile_id, …)`" now collides with "primary family". Say "The result form is …".
- **m5. Requalification and family change.** It is unstated whether the requalification "new profile key" for the primary is a "change of the primary family" that needs a stakeholder decision.
- **m6. Human trial and non-primary profiles.** §7 provides one trial, drawn from primary-family runs. The PASS scope of a non-primary profile with respect to §7 is unstated. Say that its PASS is scoped to machine criteria, or that it reuses the primary's trial by declaration.

## Answers to the record's §5 questions

1. **The contract blocks every profile on any final non-PASS state of the primary family, and requires `runtime-command` on every deterministic family run.** Two residuals remain:
   - the ordinary-entry Q4 floors may be carried outside the family (B1);
   - the unmarked workplan line 662 still issues per-profile PASS (G1).
2. **Realizable for T1/T7/T8 and the human trial, with matched keys preserved per panel. Not realizable for the ordinary-entry floors** (B1). "Logical 6.6 execution profile" is capability-defined, so the flash model can host T1/T7/T8.
3. **Well defined and not brittle for argv, stdin/RPC and environment,** since the OMP sandbox environment is constant. It is undefined for adapter-written files, and §6 is not aligned (G2). Per-run identifiers need declared template parameters. Gaming is bounded by the frozen template and the request-0 transform check, provided constants are verified free of entrypoint content.
4. **Unmarked contradiction:** the workplan profile-scoped lines (G1). Attributions stay within the quoted words, but labels are missing (m2).

## Checks run / not run

**Run.**
- Release-state resolution; 6.6 `software-design/SKILL.md` and the abstraction kernel read at `22f4bdba`.
- `git diff 363550b HEAD` (three files) and the contract diff against `4c404ec`.
- Contract §§1–8 read in full; overlay §0.1, the header entry, the marker greps and the §11 profile-scoped lines read.
- Decision record §§5–7, the fourth check, and the amendment record read in full.
- History commits `d370193`, `0c5372d`, `70727f1` and `4c404ec`, and the four check files, verified.
- Commit status of the closeout record checked: `91b6de2`.
- `adapters/omp.py` subject environment, skill install, config and argv grepped.
- The probe directory listed.
- `git diff --check 363550b HEAD`: clean.
- `python3 -m unittest discover -s tests`: 407 OK, 3 skipped.

**Not run.**
- Live launches.
- RPC-mode adapter realization, the observer request-0 check, the runtime-input record and transform freezing. These are deferred harness work, not blocking.
- `observer70.py`, `core70.py` and `harness70.py` beyond what is cited.
- Raw probe streams re-parsed (relied on the fourth check).
- The untracked `STAKEHOLDER-DECISION-2026-10-04-PROTOCOL-7.0-STAGE7-OPTION1-CLAIM-SCOPED-ADMISSION.md` and eval files (outside the subject).
- Statistical adequacy of the exposures.
