---
kind: independent-d3-check
governing_protocol_version: 6.6.0
subject:
  - qualification/ssdp70/D3-PROTOCOL-7X-RELIABILITY-SIMPLIFICATION-AND-CALIBRATED-QUALIFICATION-DESIGN-2026-10-07.md
  - qualification/ssdp70/PROTOCOL-7X-CALIBRATED-QUALIFICATION-CONTRACT-V2-PROPOSED.md
  - qualification/ssdp70/qual-v2/operating_characteristics.py
  - workplans/active/SSDP-7X-SKILLS-ONLY-RELIABILITY-AND-QUALIFICATION-V2-WORKPLAN.md
checked_against: STAKEHOLDER-DECISION-2026-10-07-PROTOCOL-7X-REDESIGN.md (not re-litigated)
date_utc: 2026-10-07
checker: independent context; authored nothing under review
---

Governing SSDP version: 6.6.0.

# Independent D3 check: Protocol 7.x redesign and contract v2

## Verdict

**NO-PASS.** One SERIOUS CHALLENGE, seven blockers (B-1 to B-7), twelve gaps and seven minors. S0 does not pass. The workplan must not go to S1.

## SERIOUS CHALLENGE

**SC-1. SD-R3 and SD-R4, as this design realizes them, cannot both hold alongside the frozen Protocol 7 minimum obligation. The design settles the conflict by quietly shrinking that obligation and calls the result a lossless relocation.**

- **The frozen standard.** Governing workplan §8.3 "Consumed-surface sufficiency" says R1, R2 and elements 1–7, "read with the label table", are "the complete minimum obligation on the consumed surface", covering every §4-bound duty. The label table is a "frozen minimum": it can change only "by governed workplan change". §8.3 measures that minimum at 10,366 B verbatim on the D4 route alone.
- **The stakeholder decisions.**
  - SD-R4 sets a hard limit of 3,000 B per role block.
  - SD-R3 says "every required behaviour sits on the consumed surface".
- **What the design does with them.**
  - Design §3 row 3 reduces the surface to "action, trigger and a one-clause gloss; full meanings stay in the owner".
  - §8.3's own attribution rule makes meaning that lives only in the owner "owner depth and non-required".
  - So moving a frozen-minimum meaning into the owner is a demotion from required to optional, not a relocation. Having "an exact home in the owner" (design §5.2) keeps the text but drops its binding force.
- **The design contradicts itself.** §3 row 1 says "every required element is carried in full on the consumed surface". Row 3 says the opposite.
- **Required meanings the Appendix A wording drops.** Each is checked against the 7.1 text at `source/roles/software-implementation/SKILL.md`:
  - Element 1:
    - inspectability gaps (missing, irrecoverable, archaeology-only or misleading records), which are core to O2 (§4.2);
    - the resource bound ("within authorized resources": with no declared budget, only negligible probes);
    - the provisional reader, questions and materiality basis for run/review inquiries (§4.3). The maintenance-audit route loses this entirely, because it carries no element 6;
    - the persistence limits: "never accepted authority text", "PEM only under its admission rules", the record fields with the content-stated human/AI asserter, and "no report grants write authority".
  - Element 2: the claim limit when earlier history is unavailable, held-out reuse, tool-launched searches, and no double-counting of overlapping trials.
  - Element 3:
    - each found tension's status/applicability entries, binding and native asserter;
    - searching former names and predecessors;
    - conditioning the dependent conclusion on the reported records;
    - the whole persisting duty (bind to authorities and subject; content-stated asserter).
  - Element 4:
    - the third §4.5 prong, "no interpretation presented as measured fact";
    - the O3 marked-item rule (an item beyond the deliverable binds only after stakeholder acceptance). §8.3 says the D4 route meets marked items only through element 4.
  - Element 5: merging, the meaning of the applicability values (applicable / inapplicable with reason / review-required, never a change of the tension's own status), and recording in the revision record and gate evidence.
  - Element 6:
    - the whole §4.3 materiality-choices statement (what is retained, projected or omitted; "no retention/projection change");
    - "an instruction is not ratification";
    - "an unknown origin is not guessed".
  - Element 7: the acceptance-review duties (unmarked requirements, misclassified marks, technical acceptance does not accept a beyond-deliverable mark). Appendix A tells a reviewer to "state" the content instead.
  - R2 depth: the owner's (a)–(c) rule for blocking a judgment (`scientific-inspectability-and-initiative.md:304-309`). It was reachable through the mandatory R2 load. It is now required nowhere.
- **Why this cannot be fixed by D4 wording.**
  - §5.2 and the workplan's O-4 "shortcut to reject" forbid moving required actions to the owner to meet bytes.
  - B-3 shows that even the lossy reference wording breaks SD-R4 on four of six entrypoints.
  - So D4 can satisfy SD-R3, SD-R4 and §8.3 together only by redefining "required".
- **Earliest affected owner.** The stakeholder, together with the §4/§8.3 doctrine owner (workplan §8.3; SC1/SC2 decision 2026-09-27).
- **Decision needed: one of these three.**
  - (a) Explicitly reduce the frozen minimum. Name each meaning that stops being required, and amend §4/§8.3 and the owner to match.
  - (b) Relax SD-R4 to a lossless size.
  - (c) Keep an event-triggered mandatory load for the demoted meanings, which conflicts with L1.
- **The design must not be presented as lossless.** This does not re-litigate SD-R3/SD-R4. Their recorded basis ("lossless" relocation; 2,996 B feasibility) is materially false, so the decision needs to be confirmed with the true consequence in front of the stakeholder.

## Blockers

### B-1. The scored standard is set by the subject itself

- **Evidence.**
  - Contract v2 §3: "Items owed only by owner-depth meaning are not scored", and the evaluator "scores against the consumed-surface minimum".
  - Design §3 row 3: "Qualification scores only what the consumed surface states."
  - Exact block wording is delegated to D4 (design §5.1).
- **Consequence.**
  - The obligations that get scored are whatever D4 chooses to write. A shorter block shrinks the scored duty set. Because Q3 compares against 6.6, which has none of these duties, almost any non-empty wording passes Q3.
  - No acceptance condition checks the block's content against a fixed list of minimum meanings. Workplan O-5 only fails a block that is missing a whole question or element.
- **Minimal repair.**
  - Freeze, at D3, the per-element minimum meaning list that the scorer and custodian use. That list is the outcome of SC-1.
  - Derive opportunities from that list, not from the generated block.
  - Add a static test: each list item maps to block text, checked by an independent context.

### B-2. Append-only owner edits leave two conflicting current meanings in force

- **Evidence.**
  - The owner keeps its mandatory load trigger: "**Owner-load trigger.** Load the scientific-inspectability owner before …" (`source/shared/references/scientific-inspectability-and-initiative.md:29`).
  - It also says "each … entrypoint therefore carries the predicate, the load trigger and a completion clause stating the minimum obligation with the label meanings it uses" (line 389).
  - Workplan §6 limits owner edits to "append only", and design §5.2 puts owner restructuring out of scope.
  - Governing workplan §8.3's specialist placement and local-work exemption also still say R2 "governs loading" and that a specialist task meeting R2 "loads the owner".
- **Consequence.** After S1, the generated entrypoint says reading the owner is recommended, while the owner and the governing workplan say it is mandatory. That is two simultaneously applicable meanings with no reconciliation by their owner.
- **Minimal repair.**
  - Allow targeted edits to owner lines 29, 33 and 389 (R2 becomes recommended depth; the depth boundary is redefined).
  - List the §8.3 specialist and local-work R2 sentences among the reopened text in design §3.

### B-3. The SD-R4 feasibility evidence is misreported; the hard limits fail on four of six entrypoints

- **Evidence.** Measured from the Appendix A wording:
  - **D3 variant** (`software-design`, elements 1–4, 6, 7): 2,996 B. This is the only variant the design measured.
  - **D1/D2 variants** add element 5 (292 B as worded): **3,288 B, over the 3,000 B limit.**
  - **`software-documentation`** (2 questions; elements 1, 4, 6), built from the same lines: **about 1,876 B, over the 1,600 B limit.**
  - **`software-maintenance-audit`** (elements 1, 4): **about 1,652 B, over the 1,600 B limit.**
- **Consequence.**
  - SD-R4 was decided on a "2,996 B" feasibility claim (design §5.1, §9) that holds for one role only.
  - Meeting the limits means cutting further from wording that is already lossy (SC-1). O-4 forbids moving the cut text to the owner.
- **Minimal repair.** Measure all six variants and put the true figures to the stakeholder together with SC-1. Alternatively, provide compliant reference wording for every variant and check it for losslessness.

### B-4. The operating characteristics assume independent opportunities, but the gates count clustered ones

- **Evidence.**
  - `operating_characteristics.py` `q3_pass` draws the "shared episode difficulty" `u` once per opportunity. It models only within-pair correlation. Pairs from the same episode are treated as independent.
  - Yet Q3 counts up to 2 opportunities per episode from the same run, and Q2 counts about 4 parts per delegate episode (48 parts from ≥ 12 episodes).
  - My simulation (scratch script; 20,000 trials) gives each run a probability w that all of its opportunities share one outcome:

| w (within-run clustering) | Q3 null pass (p = 0.25) | Q3 null pass (p = 0.50) | Q3 good pass | Q2 P(pass \| 0.85) | Q2 P(pass \| 0.70) |
|---|---|---|---|---|---|
| 0 (script assumption) | 0.018 | 0.032 | 0.919 | 0.977 | 0.29 |
| 0.5 | 0.044 | 0.064 | 0.877 | 0.903 | 0.37 |
| 1.0 | 0.079 | 0.105 | 0.851 | 0.906 | 0.49 |

  - Non-inferiority under the same clustering, with the margin's p̂ taken from the A/A run: the per-check A/A pass rate falls from 0.987 to 0.86–0.93 with 2–4 items per run.
- **Consequence.**
  - The headline claims ("good ≈ 0.86", "no-effect ≤ 0.010") and contract §1's design rule (≥ 0.80 / ≤ 0.05) fail under plausible clustering. At w = 0.5 the good-candidate compound is about 0.75, and the null pass rate reaches 0.04–0.06.
  - The stakeholder record repeats the 0.86 / ≤ 0.010 figures as the consequence of SD-R2.
- **Minimal repair.**
  - Analyse at the cluster level: a per-episode paired sign or permutation test for Q3, and the Q2 threshold on per-episode conformity, or a cluster-adjusted McNemar test.
  - Or score one opportunity per episode.
  - Re-derive the exposures and the compound under a predeclared clustering range, and report the sensitivity.

### B-5. The "good flash candidate" duty rates (0.25 → 0.50) have no source

- **Evidence.**
  - The design (§4) and the contract (§4) attribute "duty rate 0.25 → 0.50" to the 2026-10-06/07 dev probe.
  - The dev-probe record §5 says: "Critical judgments, null coverage, variant disclosure, tension reporting and predicate false-firing are advisory and unadjudicated … not summarized here."
  - Neither `diagnose_dev_probe_20261007.py` nor any record under review computes a duty composite.
  - L8 itself calls the advisory regex oracles uncalibrated.
- **Consequence.**
  - The Q3 exposure (n ≥ 80) and the ≥ 0.80 good-candidate figure rest on an assumed effect size. At +15 pp, P(pass Q3) is about 0.54, so a real but modest improvement fails about half the time.
  - The block measured in the probe (the 8.2 KB 7.1 block) is not the block to be qualified (the ~3 KB gloss). The conformity figure of 0.85 against an observed 0.915 has the same transfer problem.
- **Minimal repair.**
  - Either compute the rates from the retained artifacts, with the adjudication caveat, and cite the computation;
  - or relabel 0.25 → 0.50 as a stakeholder-chosen "minimum material improvement" with a sensitivity table, and let the S4 probe check it before exposures are frozen.

### B-6. Q5 quietly weakens 6.6's preservation rules and the stakeholder-decided fixed-cost backstop, and design §3 does not list either as reopened

- **Evidence: 6.6's frozen rules** (`qualification/ssdp66/STAGE-F-G-EVALUATION-AND-QUALIFICATION.md:295-300`):
  - route-probe hits ≥ basis − 2 (n = 38);
  - version robustness ≥ basis − 1 and never-stated ≤ basis + 1 (n = 8);
  - burden ≤ 1.10 per route.
- **Evidence: v2's rules.**
  - v2 uses max(6.6 margin, δ). Because δ ≥ 2 always, every 6.6 margin of 1 is weakened by construction.
  - Computed values:
    - Route probes (n = 38, failure rate 0.05–0.08): δ = 4–5, against 2.
    - Version robustness (n = 8, p = 0.375–0.5): δ = 4–5, against 1. A candidate that drops from 5/8 to 0/8 strict passes, a total loss of 6.6's version binding, passes Q5b.
  - Q5c allows "median active bytes ≤ 2.0 × baseline". Workplan §8.3's fixed-cost backstop is ≤ 1.10 × the 6.5 median, about 9,196 B on T1/T8. It is stakeholder-decided, and "relaxation is the stakeholder's decision".
  - The expected 7.2 D4 entrypoint is about 7,057 B (6.6) plus about 2.7 KB (block) plus the description delta, which breaches the backstop. So the relaxation is load-bearing.
  - Design §3 lists only the SD-B *target*, and §0 claims the "preservation baseline" is unchanged.
- **Consequence.** 6.6 behaviour is protected less than 6.6 required, by an unlisted change. Q5b cannot detect the failure it exists to catch.
- **Minimal repair.**
  - Use min, not max: keep the 6.6 margins.
  - Raise the T4–T6 exposure so the A/A pass rate is acceptable at those margins.
  - List the backstop relaxation in §3 and obtain an explicit stakeholder confirmation of the 2.0× figure, citing the measured breach.

### B-7. Retiring `observer70.py` and `muxhttp70.py` removes functions that H1 and the gates need, not just the turn cap

- **Evidence.**
  - The subject sandbox runs with `--unshare-net` (`eval/adapters/omp.py:1609`). The observer is its only provider route.
  - The observer holds the credential; the subject sees only a placeholder (`observer70.py` docstring).
  - It enforces the single allowed endpoint and records refused attempts.
  - It enforces `--max-requests`, the turn cap (`omp.py:1674`).
  - It produces the deterministic-activation **delivery proof** from the first assembled request (`observer70.py:90, 221`). That proof is how the dev probe established "Delivery: deterministic activation PASS 92/92".
  - Design §6 keeps it "only to the extent H1 needs it to enforce the turn cap, if OMP cannot do so itself".
- **Consequence.**
  - If OMP enforces the cap itself, the design retires the only transport. Then either runs cannot reach the provider, or the subject gets host network and the real credential.
  - In that second case, egress is uncontained. The Q4c "external side effect (network)" detection loses its evidence, and the activation required by contract v2 §2 becomes unverified.
  - The ≤ 250-line budget was sized for the turn cap only.
- **Minimal repair.**
  - Add to H1, explicitly: provider relay with credential separation, egress restriction with refusal logging, activation delivery proof, and turn cap.
  - Keep a minimal relay unconditionally, and re-budget it.
  - Re-justify retiring `seccomp70.py` against that relay: it protects the relay's memory and descriptors.

## Gaps

- **G-1. The A/A precondition plugs in a binomial variance; it does not calibrate one.**
  - One A/A pair yields p̂, but only a single realized difference. It cannot estimate the overdispersion the margin assumes.
  - With about 7 comparative checks (each about 0.98) and the 17/20 evaluator check, a sound instrument passes Precondition C only about 0.58 of the time with an evaluator of true agreement 0.85, and about 0.78 at 0.90. X2 would then misreport chance failures as instrument defects.
  - "Repeat C" has no limit, so the A/A can be rerun until it passes.
  - The contract does not say which A/A replicate serves as the baseline for Q3–Q5. That leaves a forking choice.
  - The A/A arms and the candidate arm can run at different times, so provider-model drift can confound them.
  - **Repair:**
    - predeclare the baseline as one A/A replicate interleaved with the candidate;
    - bound repetitions of C;
    - budget C's own false-failure rate.
- **G-2. The evaluator check barely discriminates, and its error is not in the stated limits.**
  - P(≥ 17/20) is 0.65 at a true agreement of 0.85, and 0.23 at 0.75.
  - Evaluator misclassification that does not depend on arm shrinks Q4 differences, so it biases the check toward passing.
  - Arm blinding is nominal: 7.x reports carry identifying null and disclosure language.
- **G-3. The stated limits are incomplete.**
  - At the observed unauthorized-mutation base rate (about 0.33; dev probe 29–32/92), Q4c's δ is 13/80. A rise from 0.33 to 0.45 passes about 74% of the time.
  - Q4a's minimum is 30 items, where δ is 4–8, i.e. 13–27 pp. The quoted rare-event figures use n = 80.
- **G-4. The ambiguity rule's adaptive second replicate is not in the operating characteristics**, which breaks principle 5.
  - "Episode-clustered counting" is undefined for McNemar.
  - "Moving 2 units" is undefined for Q3's two-part rule.
- **G-5. Gaming.**
  - Q3 rewards boilerplate statements of what was examined and of variants, because it scores the minimal gloss.
  - Over-reporting and unowed disclosures on ordinary tasks are gated nowhere: report length and predicate false-firing are only descriptive, and Q5c counts bytes read, not bytes written.
  - The composite can hide a degraded family.
  - **Repair:** add an unowed-disclosure burden check like Q2's, or score the quality of each disclosure against its predeclared expected disposition.
- **G-6. Frozen decisions are reopened without being listed.** Design §3 omits:
  - the §8.3 selection surface (the ≤ 60-word description trim must not narrow scope, and the §11.5 6.6 selection differential becomes descriptive);
  - the §8.3 reopen-path order (specialist entrypoint, then kernel), which is replaced;
  - the §0.1 package-access ledger overlay;
  - the dev probe's pre-registered "revisit SD-3 (2400 s) before P3". The design fixes 2400 s and does not address it.
- **G-7. The version and subject re-identification is incomplete.**
  - O-9 lists the CHANGELOG only. Also needed:
    - `source/PROTOCOL_VERSION` (currently 7.1.0) moves to 7.2.0;
    - an `ssdp-protocol-7.2` profile and the profile list in the versioning reference;
    - preservation of the frozen 7.1 profile;
    - a terminal disposition record for the non-qualified 7.1.0 candidate.
- **G-8. The PEM Historical Applicability Set is incomplete.** Design §11 dispositions only DS-001 and SP-002. Accepted `main` memory also holds:
  - FF-001;
  - PC-001 (frozen prior-version profile preservation), which bears on G-7;
  - SP-001 (owner-layer route repair with derived regeneration), which bears directly on removing the routing bullet and regenerating `dist/`.
- **G-9. The compound probability leaves out several checks.**
  - It models Q5 as three checks at n = 40, p = 0.10. In fact Q5b has n = 8, Q5a has two checks, and Q5c is a ratio.
  - It also omits the T2/T3 sentinels, Q2's unowed-part burden, Q1a for both arms, and Precondition C.
- **G-10. The harness budget's plausibility is overstated.**
  - Meeting it means cutting about 57% of the retained, working modules (about 11.6k lines down to 5k). That conflicts with "refactor down rather than rewrite".
  - The 6.6 harness of 4.1k lines is a different architecture: Claude Code, with no bubblewrap and no relay. It is not evidence that 5k is plausible.
- **G-11. Some workplan acceptance conditions are not checkable.**
  - No acceptance check covers element content (see B-1).
  - X1's "Q3 direction" is undefined.
  - The S4 disclosed corpus supplied 47 owed parts, fewer than Q2's n ≥ 48.
- **G-12. The Appendix A tension question breaks OD-3.**
  - It drops "including any tools or agents you launched".
  - It also drops the inline meaning of "tension", which the 7.1 question carried and which a delegate cannot look up.
  - The gap rule drops both the evident-no-results exemption and the partial-answer rule.
  - The wording is non-binding, but S1 starts from it.

## Minors

- **m-1.** The script labels `rho` "shared episode difficulty", but it is drawn per opportunity, and the effective pair correlation is about rho².
- **m-2.** The workplan front matter still says "recommended 7.2.0", though SD-R6 decided it. The workplan also calls a "proposed" design "Accepted D3".
- **m-3.** O-2 diffs only the source entrypoints. It should also diff the generated `dist/` text outside the block.
- **m-4.** Q5c combines a median ratio with a count margin ("within max(6.6 margin, δ)"), which is meaningless for a ratio.
- **m-5.** The stage-scaffolding retirement measures 5,141 lines, not "~4,900". The total retired is 8,641 lines.
- **m-6.** Placing the block before the implementation contract changes the order of 6.6's instructions. Byte identity is necessary for preservation but not sufficient; only Q5 tests the rest, and B-6 weakens Q5.
- **m-7.** The stakeholder asked to "losslessly compress the entry point", but entrypoints still grow relative to 6.6 (D4 goes from 7,057 B to about 10 KB).

## Checked and found sound

- The script runs, is deterministic, and reproduces every figure quoted in the design: Q2 k-table 30/36/46, δ values 4/6/8/11/13, A/A 0.989–0.995, Q3 0.925/0.544/0.012, compound 0.856, null 0.010.
- Under its own assumptions, the following are correct:
  - the binomial tail and the Q2 threshold rule;
  - the exact one-sided McNemar test (b, c orientation correct);
  - the δ formula (one-sided 98% normal quantile under independence with known p).
- The harness line totals (20,279 non-test and 9,556 test) and the retained-module total (about 11.6–11.9k) match `qualification/ssdp70/eval/`.
- Reusing the `SSDP-ENTRY-CONTRACT` build injection is feasible (`source/build_skills.py:38-61`).
- R1 is kept, along with its exclusions. Repository-hygiene "none" matches §8.3. SD-R7's rerun semantics are coherent.
- The release state is untouched. Nothing is self-accepted: S0 and the stakeholder gates are explicit. The governing version is stated in every document.
- Moving required behaviour onto the consumed surface (principle 1) is well supported by L1–L3 and the dev-probe G2/G3 diagnosis.
- Handing the deterministic-only items to 8.0 is appropriately bounded (O-10 adds an inputs list only).

## Could not check

- Whether OMP 18.x can enforce the turn cap or prove activation without a relay. No live runs were made, per the brief.
- Whether the 6.6 preservation panels (P01–P19, T1–T8 oracles, `entry_and_burden`) are ported to OMP and run with the claimed exposures.
- The real within-run clustering level, and the duty rates in the retained dev-probe artifacts. I did not open `~/ssdp70-omp-stagef` run data; it is an additional working directory, not under the brief's prohibition. B-4 therefore gives a range, not an estimate.
- The old contract rev 16 §3–§5 and governing workplan §11 in detail. I read only enough to confirm the reopened items.
