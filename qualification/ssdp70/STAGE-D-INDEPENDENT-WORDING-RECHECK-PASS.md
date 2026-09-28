---
kind: independent-wording-attribution-check
governing_protocol_version: 6.6.0
target_protocol_version: 7.0.0
stage: D
result: PASS
---

# Stage D independent wording recheck (element 5 and owner m3/m4) — PASS

## Independence, custody and subject

**Independence and custody.** This is the same non-authoring context that wrote `STAGE-D-INDEPENDENT-WORDING-CHECK-NO-PASS.md`. It worked read-only except for this record, made no commits and read nothing under `/home/samjin/ssdp70-fixture-custody/`. The governing workplan is at SHA-256 `66f29437af5bde3381a66c8a7609ef3ee87b230f32c210eb7fbf1858e22d78b1`. Accepted 6.6 semantics come from `22f4bdba53795da3a6f13f162529f3a843fc37ae`. The recheck subject is HEAD `980ec182` plus the uncommitted working tree.

**Scope.** This recheck covers only NO-PASS findings B1 and m1–m4. Findings m5 and the Stage E files (prompts, versioning owner, orchestrator, tests, README/CHANGELOG) are outside the subject.

**Rechecked files (SHA-256):**

- `source/roles/scientific-formulation/SKILL.md`: `bd3760d674223780d1b1daf7b5a3f2d905619e47557bb2d8651c2e4af942a745`
- `source/roles/numerical-algorithm-design/SKILL.md`: `88ceaec0f9e8911275b9cbebdf6490cb9b5d8a3c36d3ef2d20f441230485daf7`
- `source/shared/references/scientific-inspectability-and-initiative.md`: `370802006b9cd11f0d77f67d0891eb0c0d075878432b13546064377925027140` (45,958 B)

**Reference owners, unchanged since the NO-PASS check (hashes match):**

- `workflow-and-workplans.md`: `7a6261b72934ec7226dd2bc7f22436b07666466e0955fdd6eda05e8c1cc399a1`
- `evidence-evolution-and-dependencies.md`: `8fe20778d49d0546a3a9523aaab3ea287dbd50f48ea43af779f30e1b7fc8001d`

## Element 5 (closes B1, m1 and m2)

**Current text.** The line is byte-identical in both D1/D2 entrypoints: SHA-256 `da2a003b…3bde`, 671 B in source and 672 B generated.

> When revising, renaming, splitting, merging or replacing D1/D2 authority, also search recorded tensions bound to its accepted concretizations. In the revision's own record and its gate evidence, record the predecessor identity and, per found tension, a revision-scoped applicability assessment: applicable, inapplicable with its reason, or review-required; it neither changes nor closes the tension's own status in its home. Each assessment states in its content whether a human or an AI made it, and which agent (the account it is written or committed through does not show this); an agent's assessment is marked proposed until the revision's acceptance considers it.

**Against frozen element 5 and its label rows:**

- **Revising search over accepted concretizations.** Carried.
- **Where it is recorded.** The predecessor identity and each tension's assessment go in the revision's record and its gate evidence. Carried.
- **Applicability-assessment row.** Applicable, inapplicable with reason, or review-required. The assessment is scoped to the revision and neither changes nor closes the tension's status. Carried.
- **Written-record asserter row.** The record's content states human or AI and which agent, and the account does not show this. Carried.
- **Marked proposed.** Carried.

**Closure:**

- **B1 closed.** The text now says "is marked proposed until".
- **m1 closed.** The non-required owner example was removed.
- **m2 closed.** The text now says "written or committed through". Dropping "or identity" from the row wording loses no meaning, because the duty to state the asserter in content is unchanged.

**Nothing else changed:**

- Every other added line in the two entrypoints is byte-identical to the NO-PASS subject (R1/R2, heading, and elements 1–4, 6 and 7 all have unchanged hashes).
- The regenerated measurement shows no removed or reworded 6.6 lines.
- Gross additions are now 8,814 B on each D1/D2 entrypoint (element 5: 672 B, all required). The other entrypoints are unchanged at D3 8,141 B, D4 7,183 B, documentation 5,019 B, audit 3,615 B and hygiene 0 B.

## Owner edits (closes m3 and m4)

**m3, human gate evidence.** The section is now a route to the workflow owner. It names revision-gate assessments as included in that owner's contract.

- The unchanged workflow delta carries the whole of §6.6:
  - an intelligible projection;
  - the consequential-decision contents;
  - anchoring, including "mere reachability";
  - revision gates, including assessments marked inapplicable, with asserters;
  - semantic adequacy.
- §3.2 assigns this REFINES row to the workflow owner, and §6.6 is headed "(Channel C; workflow owner)". The owner therefore need not carry it.
- The owner keeps everything of its own that bears on gates:
  - the "decision-sufficient gate evidence" term;
  - the Channel C row in the channels table;
  - rule 11 ("A human gate SHALL NOT close unqualified …");
  - the revising duty's recording in gate evidence.

**m3, inquiry status.** The bullet is now a route to the evidence owner's `CHALLENGES` definition.

- The removed sentences were: separate from strength, applicability and disposition; a single exploratory counterexample can warrant Serious Challenge; a confirmatory label proves neither strength nor independence.
- All three are present in the unchanged evidence delta, which §3.2 names as the owner (REFINES).
- The owner's epistemic-initiative rule 7 (exploratory is not confirmatory) is unchanged.

**m4.** "A human's exploratory choice may be unaccepted" is restored. The §9 non-goals "Orchestrator transition/control semantics or profile schema" and "implement the Protocol 8 deterministic orchestrator" are restored.

**No new drop, contradiction or shadow definition.** The owner diff against HEAD touches only these four places.

## Disposition

PASS. Element 5 now carries frozen element 5 and its label-row meanings losslessly, with per-sentence attribution fully required. B1 and m1–m4 are closed.

Together with the NO-PASS record's verified items, the entrypoint wording and attribution satisfy the §8.3 independent check required before the Stage F freeze. Minor finding m5 (rendered numbering of gapped items) remains cosmetic and non-blocking. Stage G reviews the frozen candidate.
