---
kind: independent-contract-check
governing_protocol_version: 6.6.0
target_protocol_version: 7.0.0
subject_commit: d370193
verdict: NO-PASS
date_utc: 2026-10-04
---

# Independent check: activation-strata amendment (d370193)

**Subject.** Exact bytes at `d370193`:
- `PROTOCOL-7.0-EVALUATION-AND-QUALIFICATION-CONTRACT.md`: §1 items 4 and 12, §3, §4, §6, §8;
- `PROTOCOL-7.0-ACTIVATION-STRATA-CONTRACT-AMENDMENT-2026-10-04.md`;
- the workplan §0.1 cross-route paragraph.

**Conduct.** The checker entered the 6.6.0 software-design role and the abstraction kernel from the accepted public source `22f4bdba` (resolved through `PROTOCOL-RELEASE-STATE.yaml`). The checker did not author the subject.

**Verdict: NO-PASS.** There is one Serious Challenge and four blockers. Each blocker needs only a narrow repair, but the Serious Challenge needs a governed workplan change before the contract can rely on these bytes.

## SERIOUS CHALLENGE

**SC-1. The accepted workplan requires ordinary-entry qualification, and the stakeholder decision now conflicts with it. A contract amendment plus cross-route cannot settle this.** Owner: workplan, through a governed amendment and a fresh independent workplan Review; the stakeholder adjudicates scope. This answers §6 question 4: **yes**.

- **Basis.** The contract says the handoff's §11.3 cases and §§11.4–11.6 floors govern it (contract preamble). The workplan's design assumes ordinary entry throughout:
  - §8.3: "§11 must exercise ordinary entry through the installed catalog, with selection counted as part of the subject";
  - the §11.3 composite cases are "ordinary entry … with the agent's own skill selection counted", and authority authoring and tension retrieval are "each run on ordinary entry";
  - the consumed-surface sufficiency text scores "§11 decision-critical cases on ordinary routes";
  - §11.5 T1/T7/T8 calls the historical prompt prefix "a reference realization";
  - acceptance criterion 13 requires "selection and routing are reliable on ordinary entry, as shown by §11";
  - the §8.3 reopen trigger, and the §13 reopen list that repeats it, fire on "material initiative misses on ordinary tasks attributable to non-selection".
- **What the amendment changes.**
  - It evaluates every absolute floor and the comparative claim on the deterministic stratum only (§3).
  - It makes the historical prefix inadmissible for T1/T7/T8 (§4).
  - Its record §4 makes non-selection feed the §8.3 trigger "only when that row fails". That row is PROPOSED, and §5 of the record offers a report-only alternative under which the trigger could never fire.
  - Taken together, these change a frozen reopen trigger, an acceptance criterion and the run mode of the §11.3 cases.
- **Consequence.** As drafted, the contract contradicts its own governing parent. The record's claim that the §11.3 *Route* rule is "unchanged, and §1 item 12 realizes it" is incorrect: *Route* ties non-selection to the §8.3 placement-miss path, and the amendment conditions that path on a new row.
- **The stakeholder decision anticipated this.** Its §4.1 lists "workplan §8.3 / §11" among the amendments that need governed change.
- **Discriminating repair.** Make a governed workplan amendment covering §8.3 (the ordinary-entry clause and the reopen trigger), §11.3 (case run mode, *Route*), §11.5 (T1/T7/T8 realization, selection floor) and §13 (criterion 13 and the reopen list). Then give it a fresh independent workplan Review, and re-check the contract against the amended parent.
- **Baseline preserved.** Until then the workplan bytes as they stand remain authoritative.

## Blockers

**B1. Ordinary-run accountability is ambiguous, so the same run can be scored as PASS or FAIL.** Sections: contract §1 item 12 (third bullet) and §3 (order sentence). Owner: contract.

- **The conflict.**
  - §3 evaluates the absolute floors on the deterministic stratum.
  - Item 12 says "Activated ordinary runs are fully accountable, including the zero-tolerance critical rule".
  - Neither says whether §3's "no critical failure" step and the 100%/0 rows count failures from activated ordinary runs.
  - "Doctrine measures / doctrine items / doctrine floor" is undefined. Nothing says whether O3/unauthorized mutation, claim integrity and critical disposition are doctrine measures, which drop out of non-activated runs, or protected-outcome safety measures.
- **Failure scenario 1.** An activated ordinary candidate run makes a wrong critical decision. One reader fails qualification; another excludes the run because the floors are deterministic-only.
- **Failure scenario 2.** A non-activated ordinary run performs an unauthorized write. Under one reading it is "descriptive"; under the other it violates the O3 floor.
- **Failure scenario 3.** A run that loads an SSDP root which is not admissible is treated as "no admissible root". Delivered doctrine is then excluded, and a critical failure under a delivered wrong role disappears from every floor. Item 12 conditions delivery on an *admissible* root, not on any SSDP root delivered.
- **Repair.**
  - Define the stratum-scoped measure set explicitly.
  - State that any critical, O3 or claim-integrity failure in any run where an SSDP entrypoint was delivered fails the no-critical-failure step.
  - State that ordinary runs never enter deterministic rate denominators.
  - Require a per-arm table of critical and O3 events from non-activated runs. This addresses §6 question 3: exclusion is acceptable only with explicit scope and prominent reporting.

**B2. A mislabelled mechanism is neither detectable per run nor given a disposition.** Sections: §1 items 4 and 12, §6. Owners: contract, then harness. This answers §6 question 5: **no**.

- **Item 4 records only a label.** `root_selection` records a mechanism label. No required event or payload proves that the entrypoint bytes entered context before the first model request. Item 12 makes that the defining condition, but the required evidence (digest, position, role) is never named.
- **The observed OMP case slips past item 12.** Item 12 marks INADMISSIBLE only a deterministic run "whose entrypoint did not reach the subject". In the observed OMP pattern the command passes through as text and the model reads `SKILL.md` by tool, so the entrypoint *does* reach the subject. §6's withheld-entrypoint probe therefore does not exercise that case.
- **§6 adds no per-run check and no negative probe.** "Recorded mechanism matches what reached the subject" is a one-time pre-run demonstration. There is no known-broken mislabel probe and no per-run validation.
- **Failure scenario.** Some runs under a `runtime-command` profile silently fall back to the subject reading the file itself. Those runs are scored as deterministic, and the mixture reintroduces model-choice activation into the doctrine floors.
- **Repair.**
  - Add a required per-run activation-delivery record. For `harness-injection`: the delivered-byte digest, which must equal the installed entrypoint digest, plus placement, role and ordering before the first model request. For `runtime-command`: the runtime's native load record.
  - A deterministic-declared run that lacks this record, or whose first SSDP entrypoint arrival is a model-issued `resource_access`, is INADMISSIBLE and is never reclassified as ordinary.
  - Add §6 known-broken probes that must be rejected: passthrough-plus-read labelled `runtime-command`, and `instructed-read` labelled `harness-injection`.

**B3. The PROPOSED floor is not fail-closed.** Sections: §3 activation row, §8 paragraph, amendment record §7. Owners: contract, then stakeholder.

- **What the contract leaves open.** It marks the floor as a proposal but does not say what happens while it is unfixed. It does not:
  - block profile freeze or runs;
  - make the activation step `NOT_EVALUATED` with no overall PASS;
  - require the value to be fixed before any exposure.
- **The record does not close it either.** Record §7 blocks runs only "until the check passes".
- **Failure scenario.** Runs start under the proposed value, and the stakeholder then picks the floor or report-only after seeing activation rates. That is a post-exposure threshold choice, which §8 otherwise treats as a governed change with requalification.
- **Report-only is not a free choice.** It would also contradict criterion 13 and the §8.3 trigger (SC-1).
- **Repair.** Add one sentence:
  - no profile freeze, fixture freeze or run may rely on the contract until the stakeholder records the floor (or report-only, together with the matching workplan amendment);
  - until then the activation step is `NOT_EVALUATED` and no overall PASS can be issued.

**B4. `instructed-read` counts as ordinary entry and can satisfy the activation row.** Sections: §1 item 12 (second bullet) and the §3 activation row. Owner: contract.

- **The gap.** The row counts "ordinary-entry episodes whose … expected route is SSDP-applicable" and does not exclude prose-instructed episodes. Item 12 classifies those as ordinary.
- **Failure scenario.** Episodes prefixed "Use the X skill." inflate activation toward 100%. The row then measures wording compliance, which the stakeholder called unreliable, rather than unprompted selection.
- **Repair.** Restrict the activation row and the S/H populations to uninstructed `ordinary-read` episodes. Either prohibit `instructed-read` in qualification runs or report it as a separate, non-scoring stratum.

## Material gaps

**M1. Whether `harness-injection` is equivalent enough, and what claim it supports (§6 question 2).** Owners: contract and stakeholder.
- **Delivery form is not fixed.** Item 12 does not fix where the injected bytes go (system or user turn), their position, or wrapper framing.
- **Identity is inconsistent.** Item 12 puts the stratum in run identity. The stakeholder record says the mechanism changes the execution-profile key. Only the key controls pair matching and profile-scoped results.
- **Claim scope.** A PASS under injection establishes how delivered doctrine performs, not that a given runtime's user command delivers it. The README's OMP `/skill:` command is passed through as text in headless mode. Require results to be reported per mechanism, and scope any "supported usage works on runtime R" claim to runtimes where `runtime-command` was demonstrated.
- **T1/T7/T8 byte metric.**
  - The contract does not say whether injection wrapper bytes count.
  - It does not say whether a redundant model re-read of an injected `SKILL.md` counts once or twice.
  - It does not say whether the fresh 6.5 denominator is a "matched arm" bound to the same mechanism.
  - Fix all three identically across 6.5, 6.6 and 7.0 to keep the 2.0× rule comparable.

**M2. Activation-row composition and profile semantics.** Owners: contract, then stakeholder.
- **Composition.** Nothing requires the n ≥ 20 episodes to include the §8.3 selection-surface classes. Those are run/ad hoc analysis/results-review/gate-evidence, plus the copy/relay/delegate classes the D4 description now covers. Stage 7 showed that these framings never triggered catalog consultation. The row could therefore pass on legacy S/H routes, where 6.6 already reached 28/32.
- **Profile semantics.** "Must pass on at least one flash-class profile" is a cross-profile condition inside a profile-scoped regime. The contract does not say:
  - whether a second flash profile may fail;
  - on which profile the deterministic doctrine floors must pass for an overall claim;
  - how this composes with `PASS(profile_id, …)` and the separately reviewed aggregation rule.

**M3. Some content attributed to the stakeholder goes beyond the quoted decision.** Owner: stakeholder, who can confirm cheaply when fixing the floor.
- **What the quote supports.** The quoted words support three things: description coverage, activation as a target "especially on the lighter models", and the requirement for deterministic commands.
- **Recorder derivations.** These come from the recorder's §3–§4 reading, not the stakeholder's words:
  - `harness-injection` counts as deterministic;
  - deterministic activation is 100%;
  - a stronger profile cannot rescue a light-profile failure;
  - the T1/T7/T8 prefix is inadmissible.
- **Not in the decision record at all.** Evaluating the doctrine floors on the deterministic stratum only, with that stratum alone meeting the exposure minimums. Decision §4.1 instead scores doctrine wherever it was delivered, which includes activated ordinary runs.

**M4. Many run families have no stratum assigned.** Owner: contract.
- **What is assigned.** Item 12 requires every run to declare a stratum, but the contract assigns only three: S01–S11/H01–H05 (ordinary), T1/T7/T8 (deterministic) and the activation row (ordinary).
- **What is not.** No stratum is assigned to:
  - P01–P19 route probes;
  - T2/T3 sentinels;
  - T4–T6 version-bound pairs;
  - near-boundary negatives and predicate-excluded opportunities;
  - R2 owner-load opportunities;
  - §5 burden routes;
  - §7 human-trial material.
- **Why it matters.** Comparability with 6.6 depends on these choices. Require the custodian to predeclare the stratum, and the deterministic root, per case before freeze.

**M5. Exposure feasibility (§6 question 6).** Feasible only if every §11.3 case is re-authored as fresh fixtures and run deterministically. Whether ordinary composite runs are still owed, which would double the cost, depends on SC-1. This gap does not block independently.

## Minor findings

- **m1. Activation-step placement.** §3's order lists "activation" as a step after the absolute floors, while its row sits inside the absolute-floor table. State the evaluation position once.
- **m2. Dangling routes in the cross-route.** The workplan cross-route cites `STAKEHOLDER-DECISION-2026-10-04-PROTOCOL-7.0-NON-QUALIFICATION-CLOSEOUT.md`, which is untracked and not in the `d370193` tree. It also cites a wildcard home-directory corrigendum path. Commit the record and name the exact corrigendum.
- **m3. Reruns of INADMISSIBLE runs.** §5 does not say how a deterministic run that came out INADMISSIBLE is rerun. Record every replacement so that admissibility reruns cannot select outcomes.
- **m4. Question 1 depends on B3 and SC-1.** With a fixed floor, ordinary users get the activation floor plus accountability for activated runs. Under report-only they get no qualification protection. That is a stakeholder choice, but it needs the workplan change in SC-1.

## Checked / not checked

**Checked.**
- The full `d370193~1..d370193` diff.
- Contract §§1–8 in full.
- The stakeholder decision record and the three evidence records. Their figures match the amendment: 13/122; 50/50 M07 opportunities with no root loaded; 42/43 critical failures; 6–10 of 25 owed parts; 4/10 vs 2/10.
- Workplan §8.3 (placement, selection surface, reopen triggers), the §11.3 ordinary-entry cases and *Route*, §11.5 T1/T7/T8, and §13 criteria 13 and 14 plus the reopen list.
- The 6.6 S/H scenario prompts, which are uninstructed.
- Precedent `aacf79e` and the custody decision record. That amendment stayed within the contract and left workplan obligations binding.
- Offline suite `python3 -m unittest discover -s tests`: 407 tests OK, 3 skipped.
- `git diff --check` on the subject commit: clean.

**Not checked.**
- No live runtime. Whether interactive OMP or other runtimes execute skill commands was not tested.
- Adapter or harness code for injection; none exists yet.
- The statistical power of the proposed ⌈0.8 n⌉ floor beyond the record's claim.
- Workplan sections other than those listed above.
- The full content of the corrigendum.
