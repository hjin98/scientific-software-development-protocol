---
kind: protocol-workplan-review
protocol_version: 6.6.0
target_protocol_version: 7.0.0
reviewed_subject: hjin98/scientific-software-development-protocol@665a5cc3bed3c07910075bfee3a576241cc1083e:workplans/active/SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY-CONSOLIDATED.md
disposition: NO-PASS
active_serious_challenge: none-established
---

# Protocol 7.0 Consolidated Workplan — Review of 665a5cc

## Basis and independence

This records the independent workplan-level Review delivered in the task before the stakeholder instructed "Repair." The reviewing context authored neither the reviewed subject nor its `d255a92` repairs. It subsequently authored the proposed repair at that instruction and cannot independently accept that repair. This record preserves the original NO-PASS assessment; it is not evidence that the repair is correct.

The checkout was the exact reviewed subject. Release identities were resolved from `PROTOCOL-RELEASE-STATE.yaml`: accepted Protocol 6.6.0, public source `22f4bdba53795da3a6f13f162529f3a843fc37ae`, recovery `384666764da4c55b282e6b1595ab97e2f86e1dc4`. Canonical `source/` and `dist/` bytes matched that public source, so 6.6 owners were read there. Section 4 is byte-identical at `88a82b5`, `d255a92` and `665a5cc` (sha256 `a469824f89b39a06393724aaff9e6a64dea8e460f318523a1d83b8b9fea2956f`); the stakeholder's §4 decisions were accepted inputs. The §0.1 repair map, the 6.6 intake table and all prior Review records were treated as claims. The reviewer likely shares a model family with earlier authors and reviewers; that common-mode limit is recorded rather than resolved.

## Serious Challenges

None established against accepted 6.6 or the stakeholder-accepted §4. The findings concern unaccepted parts of the plan.

## Implementation-readiness blockers

**B1 — The §6.4 tension-retrieval invariant still loses findings, and its key is absent from the consumed surface.** This is the fourth related finding (`c50f267` B5, `88a82b5` B1, `d255a92` B3); under the plan's own convergence rule it questions the mechanism rather than inviting another clause.

- *Ambiguous owner.* The home carries "every plausibly challenged D1/D2 lineage **or** states the ambiguity." An ambiguity-only home is unreachable by the mandatory lineage-identity search, and the rule fires only when the finder recognizes uncertainty, although the 6.6 evidence owner states that a D4 contradiction does not identify the faulty owner. `d255a92` B3's second counterexample (bound to D2, real target D1) therefore survives: a D1-relying or D1-revising task searches D1, and the prior-revision search covers D1 only, not its concretizations.
- *Identity change.* "Stable logical identity" defers to the evidence owner's endpoint identity, which may be a path. Rename, split, merge or replacement (`SUPERSEDES`/`REPLACES`) breaks later searches on the successor; whether replacement is a "revision" triggering the prior-revision search is unstated.
- *Consumed surface.* The §8.3 completion clause says only "search for recorded tensions against it." The lineage key, predecessor scope and never-silently-dropped rule live only in the owner, which I66-1 says ordinary routes do not read. The B3 repair is inert on ordinary routes, and the revision-drift fixture predictably tests owner reading.
- Direction: re-derive around two duties — the persisting side binds every plausibly implicated authority along the concretization chain plus the subject; the relying/revising side searches the relied-on authority, its lineage predecessors and its concretizations — with the minimum carried compactly in the consumed clause.

**B2 — The 6.6 burden-preservation floor is vacuous on 6.6's own reference routes, and the placement has no ex-ante budget.**

- The fixed-cost bound applies only to predicate-excluded routes. 6.6's burden routes T1 (grid-I/O defect dropping data), T7 (signal-rescale workplan) and T8 (stats `median`), and selection routes S04/S08, all fire §8.2. For firing routes added material only "falls under the burden bound", which is undefined, so 6.6's criterion-4 capability (D4 entrypoint 7,057 B, ratio 0.844) is protected nowhere.
- Arithmetic: the frozen predicate (~727 B), completion clause (~590 B) and exemption amendment add roughly 1.2–1.6 KB per entrypoint, about 1.17–1.23× the D4 entrypoint, against a cited 1.10. Live burden equals entrypoint size, so this is predictable before runs.
- The reopen ladder (specialist entrypoint, then kernel) does not respond to a burden failure; kernel placement adds bytes everywhere.
- The exemption amendment partially supersedes 6.6's local-work exemption for nearly every scientific local defect without §13.16 classification.
- Needed: classify 6.6 reference routes under §8.2, freeze an entrypoint-addition budget, preserve or explicitly propose superseding the criterion-4 level for stakeholder decision (not a Stage A threshold choice), and fix the reopen path for burden.

**B3 — Harness-level oracle integrity checks only false acceptance.** §11.5 requires rejecting one known-broken deliverable. Missing: known-good acceptance (6.6's run-error check misclassified designed max-turn terminations, forcing a post-outcome correction); probes per acceptance branch (the 6.6 self-adoption leak passed through one rubric branch); capture of out-of-tree side effects (issue-tracker writes, network) required by the persist-then-retrieve and unauthorized-destination cases and by zero-tolerance unauthorized mutation; and verification of the new composite ordinary-entry mode (selection counted plus trajectory; 6.6 trajectories named the skill). The claim that I66-4 is fully routed is incomplete.

## Material gaps

- **G1 Selection surface.** Zero-false-activation negatives are only poem/email/books; widened run/review/gate descriptions need near-boundary negatives (non-scientific test runs, business analytics, ETL). §11.3 lacks an ordinary-entry ad hoc analysis case ("analyze this dataset"), the §2 motivating and prime variant-search case. "Scientific interpretation or decisions" parses loosely. Byte-identical 6.6 catalogs varied 28/32 vs 25/32, so non-inferiority needs an opportunity rationale.
- **G2 Hedging passes critical cases.** "Withhold with correct limitation" does not require naming the specific material area; with default qualification, generic hedges could satisfy critical cases, especially unnamed ones. Burden measures over-blocking, not over-qualification. The unnamed-class "own absolute floor" does not say detection versus disposition; non-inferiority to a near-zero 6.6 baseline is likely vacuous.
- **G3 Trust boundary (out-of-matrix).** Native-issue homes are writable by non-owners; "resolve latest disposition" imports unauthenticated state. Dispositions need asserter and authority status; a non-owner disposition must not close a tension. §3.2 routes only sensitive data to security.
- **G4 Delegation (out-of-matrix).** §6.3.11 binds the delegate directly, which may not run under SSDP; nothing requires the delegator to transmit the inquiry/disclosure request, so the delegated-finding-loss measure partly tests luck.
- **G5 PEM stale-metadata inventory (minor).** PC-001 `authority_owner` still cites 6.5 source `7f7b5e24`, and the derived summary shows `AUTHORITY_BOUND/HEALTHY`. The 6.6 re-anchoring is substantively right, but the stale binding is neither listed nor routed.
- **G6 Preservation-map scope.** Stage A omits D1/D2/architecture owner deltas, `development-workflow-prompts.md` and specialists; the 6.6 `routing-preservation-map.yaml` and route probes (hits, violations, eager loads) are not floors; "false activation" is ambiguous (SSDP selection versus new-owner loading).

## Falsification results that did not establish another defect

- §4 preserved; PEM blob `1561797125622f355f84eb27319f87e8fa4227d9` identical at `2585b73`, `22f4bdba` and HEAD; validator PASS (schema 1, five families, zero notices); release state coherent.
- Bounded intake instead of `REVIEW_REQUIRED` is admissible under the PEM owner. Intake rows I66-1..6 match `qualification/ssdp66/STAGE-F-G-EVALUATION-AND-QUALIFICATION.md` §9 and §10.5–10.9 and the evidence correction. FF-001, SP-002, PC-001, SP-001 and DS-001 dispositions are sound.
- Same-identity revision drift closes through stable-part search, applicability assessment and authoring-time prior-revision search. Inaccessible-home rule (a)–(c) is coherent with §4.5 and §6.1.11.
- All four entrypoints carry the clause, so delegating task-class allocation is safe. Out-of-list classification/custody and the acceptance-level comparative-masking counterexample survived.
- Out-of-matrix: O3 creep through Channel C and version-bound run tasks are closed.

## Executed evidence and disposition

- HEAD/ancestry, `source/`+`dist/` diff against `22f4bdba`, §4 hashes, PEM blob identity.
- `PYTHONDONTWRITEBYTECODE=1 python3 source/project_engineering_memory.py PROJECT-ENGINEERING-MEMORY.md`: PASS.
- `PYTHONDONTWRITEBYTECODE=1 python3 source/release_state.py`: PASS, coherent.
- Byte counts of generated entrypoints and the frozen predicate/clause; reads of 6.6 selection and trajectory scenarios and T1/T7/T8 fixtures.
- Live qualification, human trial and package acceptance: not executed; future implementation obligations.
- No files were edited during the Review. This durable record was added during the subsequently authorized repair.

**NO-PASS for implementation readiness.** D4 remains unauthorized. Proposed repairs require fresh independent workplan-level Review by a context that authored neither the workplan nor those repairs.
