---
kind: protocol-workplan-review
protocol_version: 6.6.0
target_protocol_version: 7.0.0
reviewed_subject: hjin98/scientific-software-development-protocol@d41506ac0b1d2229f16d05d4eaf64cfc5134b360:workplans/active/SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY-CONSOLIDATED.md
disposition: NO-PASS
active_serious_challenge: none-established
---

# Protocol 7.0 Consolidated Workplan — Review of d41506a

## Basis and independence

This records the independent workplan-level Review delivered in the task before the stakeholder instructed "Repair." The reviewing context authored neither the reviewed subject nor its `27fb2bd` repairs. It subsequently authored the proposed repair at that instruction and cannot independently accept that repair. This record preserves the original NO-PASS assessment; it is not evidence that the repair is correct.

The checkout was the exact reviewed subject. Release identities were resolved from `PROTOCOL-RELEASE-STATE.yaml`: accepted Protocol 6.6.0, public source `22f4bdba53795da3a6f13f162529f3a843fc37ae`, recovery `384666764da4c55b282e6b1595ab97e2f86e1dc4`. `source/` and `dist/` had no diff against that public source, so 6.6 owners were read there. Section 4 is byte-identical at `88a82b5`, `d255a92`, `665a5cc`, `27fb2bd` and `d41506a` (sha256 of the `## 4.` to `## 5.` extraction `2bcc977cb219c3544a81181bfab997e792c98f3b03e22959bf623221d213e2f4`). The §0.1 repair map, the §0.2 intake table and all prior Review records were treated as claims. The reviewer shares a model family with earlier authors and reviewers; that common-mode limit is recorded rather than resolved.

## Serious Challenges

None. §4, SD-B and its confirmation are coherent and realizable. The corrected SD-B arithmetic was verified against `qualification/ssdp66/eval/scenarios.yaml` `redesign.burden_rule` and `qualification/ssdp66/eval/results/final/final-summary.json`: 1.10 × 8,360 = 9,196 B; 7,057 + 1,000 = 8,057 B (0.964 × 6.5, 1.142 × 6.6); panel net holds to about 4.8 KB of additions (0.85 × 41,908 = 35,622 versus 3 × 7,057 = 21,171); direct reduction fails above 49 B (7,106 − 7,057); T7 direct reduction already failed in 6.6 (maximum 24,800 not below minimum 8,360); D1/D2 entrypoints would reach 1.25/1.30 × their 6.5 size (5,851/5,833 B). The backstop is realizable only with compression (G3), but a breach is an escalation, not a dropped element, so it is not unrealizable.

## Implementation-readiness blockers

**B1 — Section-4-bound obligations are orphaned on ordinary routes; "complete minimum" is false.** Earliest owner: §8.3 required elements and §8.2 R2.

- §4.3's default ("SHALL record its materiality choices", short form "no retention/projection change", scored in §10 and §11.3) and §6.2.1's disclosure of consequential agent choices (§11.3 planted "agent-chosen exclusion rule", §11.4 decision-provenance marking, Stage G "agent-chosen exclusion presented as standard") are in no element 1-4. R2 explicitly excludes "a feature or a workplan implementation", the route where agents build pipelines and choose exclusions.
- O1 authoring content (§4.1) rests on R2 and Stage C owner deltas. I66-1, which the workplan applies to every role, says ordinary agents skip those reads; in 6.6, 17 of 18 T-route runs read only the entrypoint despite "Before substantive D4 implementation, read spec" (`qualification/ssdp66/STAGE-F-G-EVALUATION-AND-QUALIFICATION.md`). Reviewing proposed authority for acceptance is not an R2 branch.
- §8.3 scores ordinary-route critical cases only against elements 1-4, so the O1, short-form and exclusion cases are unscoreable or the §4 SHALLs are silently demoted. Direction: carry a compact consequential-choice/materiality element and an O1 element on the consumed surface, or obtain a stakeholder decision to weaken §4; account for the bytes against the D4 backstop.

**B2 — Element 3 requires an owner-depth trust judgment that a critical case scores.** Earliest owner: §8.3 element 3 and §11.3.

- "An unattributed or unauthorized disposition not closing it" needs the default dispositioning authority or a project designation, which §6.4/§8.3 assign to owner depth and §0.1 leaves to the human. On the consumed surface an attributed non-owner dismissal looks like a valid closing disposition: the laundering path §1 protects against, scored as a critical case.
- The paired revision-drift variant expects reporting of a revision-scoped applicability assessment, but element 3 names only "latest disposition"; ordinary-route treatment of an AI "inapplicable" assessment is undefined and untested.
- Direction (narrowing only, per §14): the ordinary route reports each found tension's latest recorded status or applicability assessment with its asserter and never itself treats a found tension as closed or inapplicable; authorization and applicability stay owner depth or the human's.

## Material gaps

- **G1 §8.2/§11.5 static route classes versus a trajectory-dependent trigger.** §11.4 defines owner false activation by whether R2 holds; §11.5 classes (i)/(ii) are fixed per route and count "any new-owner read". They diverge when the element 1 inquiry finds affected reported results; the §11.3 "first clean local defect … whose fix changes results" case sits on that boundary. Adjudicate per trajectory; predeclare fixture state; state that the 6.6 "loads none" exemption governs only while the task stays a first clean local defect.
- **G2 §8.3 specialist placement.** "Reroutes if it meets … the missing elements' conditions" cannot be evaluated on a surface lacking those elements. Documentation stating validity/accuracy claims plausibly meets element 3's condition; "documenting accepted authority" does not cover it. The hygiene rationale overstates 6.6 protection for costly or non-deterministic realized results classed "derived/rebuildable", though hygiene is outside the predicate. Narrow: reroute on R2 only; record documentation/audit/hygiene as outside the tension-search claim; add a hygiene sentinel or narrow the rationale.
- **G3 §8.3/§11.5 backstop accounting.** Measured verbatim frozen R1+R2+E1-4 = 2,159 B (R1 723, R2 375, E1 344, E2 114, E3 531, E4 72) against 2,139 B of D4 backstop headroom. The 6.6 metric counts the whole installed `SKILL.md` including frontmatter (`harness.py` `entry_and_burden`), which the SD-B target excludes, so the description amendment and framing consume backstop headroom and B1 adds more. The only feasibility argument is "a 1,000 B addition meets it". The independent check covers attribution, not losslessness under compression pressure. T7 is bimodal (6.5 runs 25,188/25,188/8,360; 6.6 runs 7,057/24,800/7,057): one run flips the cap between 9,196 and about 27,707 B; run count and mode handling are unstated.
- **G4 §6.4 disposition authority.** Broad binding is the default but a single accepting authority dispositions status; for a D1+D2-bound tension this is undefined, and uncertain statuses accumulate into standing caveats (noise against §1). "Attributable" is not "authorized": an identifiable non-owner can block a judgment under (c). A delegated relying search can drop its envelope (§6.3.11 lists findings, variant search and null envelope only).
- **G5 §11.5 oracles and floors.** Zero selection false activations on near-boundary negatives is stricter than 6.6's own ≤ baseline + 1, without stochastic rationale (I66-2: 28/32 versus 25/32 on byte-identical catalogs); one hit forces a selection reopen and pressure towards the forbidden scope narrowing. Version margins anchor to recorded 6.6 results (5/8, 1/8), whereas 6.6 compared fresh paired arms. The 6.6 no-lookup oracle counts any WebFetch or remote shell call, conflating protocol-source lookup with element 3 project issue search. R2 hit rate has no measure; owner-depth absence is only a "placement observation" not linked to the reopen trigger.
- **G6 Stage C / §3.2 template scope.** The D1/D2 roles route material authority mutation to `abstraction_concretization_change_plan_template.md`, the vehicle for O1 and element 5's revision record; only the implementation workplan template is amended.
- **Minor.** The predicate's "or decisions" became "or scientific decisions" at `27fb2bd`, after §4 acceptance; §4 binds by pointer to this predicate and the change is not in the §0.1 map. A clarification, but unrecorded.

## Falsification results that did not establish another defect

- The §8.2 split changes nothing §4 binds; the obligation predicate equals the former load predicate. R2 does not conflict with the 6.6 kernel (which loads D1/D2 owners) or the local-work exemptions on T1/T7/T8. T1 (grid-edge parsing), T7 (rescale) and T8 (median) sit coherently in class (ii); selection-only S/H runs terminate after selection, so their class matters only for selection floors, and ambiguous routes (S05, S08, H03) are correctly left to the pre-run checker.
- Element 1's pre-irreversible-step inquiry is on the consumed surface. Mechanical renames are recoverable through Git; move-plus-rewrite is not, consistent with the "mechanical" wording, but it should be named as a limitation. The inaccessible-home default is passable on the ordinary route by conservative behavior, with over-qualification scored as burden.
- The limitation rule (a skipped first-look view counts as a miss), the harness-integrity items and the T-route run mode (root pinned with "Use the software-implementation skill.", 6.6 tool list, Agent disallowed, matching `harness.py`) hold.
- PEM: `main` = `2585b73f`; blob `1561797125622f355f84eb27319f87e8fa4227d9` identical at `2585b73f`, `22f4bdba` and HEAD; schema valid (5 families, 0 notices); stale front matter (`maintained_under_protocol: 6.5.0`, `23e46543`, PC-001 bound to the 6.5 owner at `7f7b5e24`) as stated; `2818ccf` has no learning assessment while Stage F/G §9 deferred candidates; the versioning owner's list stops at 6.5 ("include" wording) while `orchestrator/src/sdp_orchestrator/core/resources/protocol/ssdp-protocol-6.6/profile.json` exists. PC-001 re-anchoring, HAS and intake rows hold.

## Executed evidence and disposition

- HEAD `d41506a`; `PYTHONDONTWRITEBYTECODE=1 python3 source/release_state.py`: coherent; `PYTHONDONTWRITEBYTECODE=1 python3 source/project_engineering_memory.py PROJECT-ENGINEERING-MEMORY.md`: schema 1 valid, five families, zero notices.
- Diffs of `source/` and `dist/` against `22f4bdba`; §4 and §8.2 hashes across commits; 6.5 (`2b8ce17`) and 6.6 generated entrypoint bytes; byte measurement of the frozen §8.2/§8.3 text.
- Read: the workplan, SD-B and confirmation records, the `27fb2bd` Review, the 6.6 role and specialist entrypoints, the versioning owner, `scenarios.yaml`, `final-summary.json`, `routing-preservation-map.yaml`, `harness.py`, the T1/T7/T8 fixtures and the 6.6 intake sources.
- Live qualification, human trial and package acceptance: not executed; future implementation obligations.
- No files were edited during the Review. This durable record was added during the subsequently authorized repair.

**NO-PASS for implementation readiness.** D4 remains unauthorized. Proposed repairs require fresh independent workplan-level Review by a context that authored neither the workplan nor those repairs.
