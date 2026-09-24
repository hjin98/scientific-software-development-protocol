---
kind: ssdp65-phase-ii-falsification
investigation: SSDP-6.5-FRONTIER-MODEL-RE-EVALUATION
reviewer: A
subject: P0 = Protocol 6.4 at 55c085261eb827e3047637d045a8e6917ea6b962
authority: non-normative-diagnostic-evidence
repairs_proposed: none (diagnostic phase)
created: 2026-09-24
---

# Phase II — Adversarial Falsification of Protocol 6.4

Diagnostic only. No repair is proposed here; root causes are hypotheses carried into Phase III.

## 1. Method and development set

**Development set (sealed from reviewer B).** Reviewer A used: the complete canonical source at P0; P0 Git history for 6.1–6.4 (`source/`, tests, workplans, qualification, history); the qualification/review records listed below; the self-hosted PEM; and the executed probes E1–E8. Reviewer A did **not** read holdout material HO1–HO2 (archived Protocol 5.x workplans, `qualification/long-horizon/`, `qualification/tool-routing/`, contents of `qualification/ssdp6/SCENARIOS*.md`), and could not access HO3 (downstream history). Two local reads of historical review records (`REVIEW-…-6.2-AUTHOR-CONTEXT-NO-PASS.md`, `WORKPLAN-*REVIEW*-6.3.md`) were blocked by the session's permission controls and were not pursued; only their file names are used.

| Case | Historical evidence | Class |
| --- | --- | --- |
| H1 | 6.1 first post-closeout reopen: stale "concretization" terminology in current D3/D4 role prose and a README route to a nonexistent file survived closeout (`history/SEMANTIC_EVOLUTION.md`) | current-state drift; premature acceptance |
| H2 | 6.1 second reopen: unresolved nested package routes; public fallback landing on an incompatible default branch; accepted standard not applied | package/fallback integrity |
| H3 | 6.2 bootstrap `1181c20` invalidated by a later cold-route repair → PEM `FF-001` | premature immutable publication |
| H4 | 6.3 invalidated bootstraps `1484c1d`, `5ee4b3a`, `e12572c`, `dc22f09`; F5 mislabel of `190c8b4` as bootstrap | recurrence of H3 class |
| H5 | 6.4 Stage-E NO-PASS rounds (`INDEPENDENT-REVIEW-2026-09-15-*-NO-PASS.md`, blockers B64-R4..R9) | review/repair churn on qualification/lifecycle machinery |
| H6 | 6.4 SC64-R1 (`USES_DEFINITION` direction) repaired after bootstrap publication and classified as "clarification" (archived 6.4 workplan §27) | Challenge resolution; stale fallback |
| H7 | 6.4 post-cutover state (P0) | lifecycle migration integrity |

## 2. Executed experiments

| ID | Experiment | Command/instrument | Result |
| --- | --- | --- | --- |
| E1 | Baseline acceptance workflow at P0 | README acceptance commands (see `../P0-BASELINE-BINDING-PROTOCOL-6.4.md`) | all green: 249 protocol tests (3 skipped), PEM valid, packages valid, dist parity, snapshot parity, 382 Core tests |
| E2 | Oracle-strength mutation probe | `tools/mutation_probe.py` (one semantic edit to canonical source, regenerate `dist/` and current snapshot, run full workflow) | §3 |
| E3 | Current-state coherence census | `grep` over `source/`, `dist/`, orchestrator resources for version/lifecycle claims | §4 CE-1 |
| E4 | Bootstrap vs recovery semantic diff | `git diff e09a9d1 74bc572 -- source` | 7 files differ (+20/−12), including kernel, evidence owner, writing owner and prompts |
| E5 | Duplication/word census | `wc -w`, `grep` over entrypoints/references | always-loaded kernel 1 552 words (6.2) → 1 868 (6.3) → 2 636 (6.4); 13 "Protocol 6.4 … consequence" sections ≈ 3 900 words; "material(ly)" 463 occurrences, no generic definition |
| E6 | Lifecycle cost census | `git log 9f35309..55c0852` classification by subject and path | 183 non-merge commits; 150 (82 %) lifecycle/review/publication/automation; 4 commits changed D1–D4/evidence/representation doctrine (implement, reconcile, advance-to-candidate, Stage-E repair); 20 commits touched temporary `.github` automation |
| E7 | PEM practice audit | read `PROJECT-ENGINEERING-MEMORY.md`, Stage-F closeout, 6.4 HAS, validator vs doctrine field census | §4 CE-5, CE-9 |
| E8 | QF64 oracle subject analysis | read `tests/test_protocol_64_axiomatic_traceability.py` | `qf_a..qf_p` are predicates defined inside the test over test-local dicts; no protocol artifact or agent behavior is their input |

## 3. Mutation probe results (E2)

Baseline: P0 `55c0852`. Each mutant changes exactly one sentence in canonical `source/`, then regenerates committed descendants (`dist/`, current orchestrator snapshot) as a legitimate change would, then runs: unit tests, PEM validation, package build/validation, dist parity, snapshot parity, Orchestrator Core tests. Raw results: `evidence/mutation-results.json`.

| Mutant | Kind | Doctrine mutated (owner) | Result | Failing step |
| --- | --- | --- | --- | --- |
| M01 | semantic inversion | owner conflict resolved by "most recent statement" (kernel; QF64-B class) | **undetected** | — |
| M02 | semantic inversion | stale pass remains admissible confirmation (evidence owner) | **undetected** | — |
| M03 | semantic inversion | edit challenged authority to fit downstream behavior (kernel, SC) | **undetected** | — |
| M04 | semantic inversion | rewrite specification to match code (D4 owner) | **undetected** | — |
| M05 | semantic inversion | widen tolerances to observed backend discrepancy (D2 owner) | **undetected** | — |
| M06 | semantic inversion | one instance establishes the whole parameterized family (kernel; QF64-F class) | **undetected** | — |
| M07 | semantic inversion | context availability = discoverable route (kernel; QF64-M class) | **undetected** | — |
| M08 | semantic inversion | agents may self-accept human-gated D1 change (D1 owner) | **undetected** | — |
| M09 | semantic inversion | test doubles may replace the real owner (D4 role) | detected | unittest (phrase assertion) |
| M10 | semantic inversion | HOT/PROVEN memory binds D3/D4 (kernel, PEM non-authority) | **undetected** | — |
| M11 | semantic inversion | tolerance from the failing backend result (testing owner) | **undetected** | — |
| M12 | semantic inversion | descendants may reset risk-accepted state (orchestration prompts) | detected | unittest (phrase assertion) |
| M13 | semantic inversion | child satisfying parent is correct by construction (kernel, adequacy) | **undetected** | — |
| M14 | semantic inversion | missing PEM proves absence (PEM owner) | **undetected** | — |
| M15 | semantic inversion | pre-Review acceptance may be deferred (workflow owner) | detected | unittest (phrase assertion) |
| L01 | lossless paraphrase | "one current semantic owner" → "a single current semantic owner" (kernel) | **rejected (false positive)** | unittest |
| L02 | lossless paraphrase | "widens" → "broadens" impact discovery (evidence owner) | **rejected (false positive)** | unittest |
| L03 | lossless paraphrase | reordered stored-direction sentence (prompts) | **rejected (false positive)** | unittest |
| C01 | control (pinned phrase inverted) | "not a closed ontology" → "a closed ontology" | detected | unittest |
| C02 | control (pinned identity changed) | `CURRENT_PROTOCOL = 6.3.0` | detected | unittest |

**Summary:** semantic inversions detected 3/15 (20 %), each only because the inverted sentence happened to be phrase-pinned; lossless paraphrases rejected 3/3. Regeneration of `dist/` and the current snapshot succeeded for every mutant, so parity, package and snapshot checks passed by construction; PEM validation and 382 Core tests passed for every mutant. **Benchmark-defect record (design §8):** the first C01 control (replace `` `source_available_D(x)` ``) was invalid because the pinned token also occurs in a kernel code block, so it could not fail; it was replaced by the C01 above before results were frozen. Both runs are preserved in `evidence/mutation-results.json`.

Interpretation limits: the mutant set was authored by reviewer A after reading the tests, so it is a *development* measurement; a fresh post-P1 mutant set (design HO4) is required for any comparative claim. Detection of a paraphrase is a false positive of the acceptance workflow, not a merit.

## 4. Counterexamples (trajectory form)

Notation: `∀ r ∈ R_local: satisfied` while `I_global: violated`.

### CE-1 — Lifecycle cutover leaves accepted-current source asserting a different current version (H7)

- **Initial state.** Independent Review PASS at `74bc572` authorizes Stage F (recovery mapping, mapping-bearing regeneration, cutover, closeout).
- **Allowed actions.** Edit version owner, README, AGENTS.md, authority index, dependency view; add phrase assertions and specific stale-phrase negative assertions to tests; regenerate descendants.
- **Locally compliant trajectory.** Recovery mapped by descendant `6e66478`; mapping-bearing regeneration; CI green (Stage-F run `35153901722`); `test_qf64_p_closeout_archives_snapshot` asserts the new state in index/README/AGENTS and the absence of three specific stale phrases; closeout record PASS; E1 fully green.
- **Global result at P0.**
  - `source/README.md` (canonical tree): "`source/` is the canonical **Protocol 6.4 candidate** source … Protocol 6.3 remains accepted-current … no recovery mapping yet"; "recovery remains unpublished pending independent Review"; "Independent assembled-candidate Review is the next separate gate".
  - `source/shared/references/development-workflow-prompts.md` (canonical orchestration source): "canonical human-facing orchestration source for candidate Protocol 6.4"; "**Protocol 6.4 candidate state:** Protocol 6.3 remains accepted-current while 6.4 is proposed/under qualification … no 6.4 recovery mapping is authorized yet". This text is generated verbatim into the accepted-current packaged profile `orchestrator/…/ssdp-protocol-6.4/prompts.md` consumed by Orchestrator Core.
  - All seven role/specialist `SKILL.md` descriptions (the runtime skill-selection text, packaged into `dist/`): "… under Protocol 6.3 …".
  - `language-profiles.md`: "Current Protocol 6.2 shared domain doctrine is authoritative."
  - `repository-intake.md`: "Protocol 6.3 may use bounded Markdown semantic dependency views".
  - `source/SEMANTIC_DEPENDENCIES.md`: self-hosted PEM described as "project-local candidate state".
  - The versioning owner's own 6.4 section: "Protocol 6.4 is **accepted-current** … this publication does not make 6.4 accepted-current and does not authorize recovery", and "`AUTO_LOCAL_FIRST` may use a compatible readable local/installed 6.4 source during candidate work".
- **Violated.** I3 (one current meaning for the current-lifecycle claim), I13 (version identity), I14 (the generated accepted-current profile carries a non-current lifecycle claim), I11.
- **Consequence.** An orchestrated 6.4 run is instructed that 6.3 is accepted-current and that no 6.4 recovery exists; a skill-selecting agent is told the roles operate "under Protocol 6.3"; version-bound baseline selection, rollback reasoning and Protocol-7 inheritance can be derived from the wrong statement. Every documented acceptance step is green.

### CE-2 — The authorized 6.4 public fallback is not the accepted 6.4 semantics (H4, H6; recurrence of FF-001)

- **Initial state.** Bootstrap `e09a9d1` qualified and published as "the sole authorized version-bound 6.4 public fallback" before independent Review. The 6.4 workplan HAS records `FF-001: APPLICABLE — Do not publish a 6.4 public bootstrap until the complete repaired source/route/package semantics exist`.
- **Allowed actions.** Review raises SC64-R1: the `USES_DEFINITION` direction is materially ambiguous (Serious-Challenge level). The author repairs kernel, evidence owner, writing owner and dependency view, and classifies the repair as "a clarification of the already-implemented … semantics … Therefore the published bootstrap identity remains valid" (archived workplan §27).
- **Locally compliant trajectory.** Bootstrap stays immutable and self-reference-safe; later Reviews confirm "bootstrap remains self-reference-safe and distinct from recovery"; Stage-F closeout: "No PEM family … changed …; no permanent PEM mutation is warranted by Stage F itself."
- **Global result.** A version-bound 6.4 agent that uses the authorized fallback receives (a) the kernel/evidence/writing text a Review judged materially ambiguous and (b) prompts stating "Protocol 6.3 remains accepted-current … No 6.4 public-source fallback or recovery mapping is authorized yet" — permanently, because the bootstrap is immutable. Two distinct semantic objects both answer to "Protocol 6.4". PEM `FF-001` still records one occurrence.
- **Violated.** I3/I12 (a version-coherent authority family has one canonical meaning), I13, I9 (an SC-resolved text remains current through an authorized route), I17's purpose (lesson recorded as applicable yet not operative and recurrence not recorded).
- **Consequence.** The version-bound fallback path — the path the protocol itself prescribes when no local source exists — yields non-accepted semantics and a false lifecycle statement. The structural cause (fallback published before Review, with mutable lifecycle state embedded in immutable content) guarantees recurrence of the H3/H4 class.

### CE-3 — The release gate cannot distinguish a protocol that says the opposite (E2, E8, H5)

- **Initial state.** 6.4 must qualify its semantic-definition doctrine (families QF64-A..P).
- **Allowed actions.** Write the qualification as pure predicates over hand-built dicts; add phrase-presence checks against owners; have an independent Review examine "the actual QF64 A-P helper/oracle and its counterfactual fixture matrix".
- **Locally compliant trajectory.** Every family has positive and "discriminating" negative fixtures; Stage C records QF64-A..P PASS; Review NO-PASS rounds B64-R6/R9 are closed by adding more negative dicts; final Review: "provides discriminating polarity for the material semantic classes"; README/AGENTS state 6.4 acceptance "required" QF64-A..P.
- **Global result.** For QF64-A..N the oracle's subject is itself; a change to protocol text cannot change their outcome. In E2 the complete acceptance workflow failed to detect the majority of single-sentence semantic inversions of core 6.4 doctrine (§3), while it rejected meaning-preserving paraphrases of pinned sentences. Review rounds optimized the proxy (more negative dicts) rather than the property (does the protocol text/agent behavior discriminate).
- **Violated.** I7/I15 and the protocol's own A8 statements: "Static string presence alone is never sufficient proof of routing/authority semantics"; "A parser passing its own happy-path template is weak evidence"; "What is the smallest plausible semantically wrong concretization that could still pass this evidence?" (answer: an inverted kernel).
- **Consequence.** A candidate that inverts governing doctrine can pass every mechanical gate; acceptance then rests entirely on Review, which in H5/H6 was itself directed by the same obligation matrix.

### CE-4 — Behavioral qualification never fails and is not tied to outcomes

- **Observation.** Historical behavioral qualifications record 92/92 (6.1), 94/94 and 95/95 (6.1 reopens), 115/115 (6.2), 260/260 (6.3) PASS. Method (6.3 record): the executor "determine[s] whether current 6.3 authority/routing/representation accepts it, rejects it, or routes it" for each stated wrong behavior. The executor model family is the same one that authored and reviewed the releases. No baseline arm, no failing trial, no stored transcripts/seeds; 6.1 was reopened twice after its 92/92 PASS for defects the qualification did not detect (H1, H2).
- **Trajectory.** Each release satisfies "qualification PASS" locally.
- **Global result.** The protocol has no accepted instrument for its central claim — that a version improves engineering outcomes over its predecessor — and its qualification cannot be shown to have discriminating power (sensitivity/specificity unknown; observed misses exist).
- **Violated.** I7 (evidence establishes only what it discriminates; stochastic replicate identity must be recoverable), I16 (process artifact treated as the objective).

### CE-5 — Closeout learning is satisfied while the project forgets its most repeated lesson

- **Initial state.** `FF-001` recorded (one occurrence, 6.2). 6.3 then invalidated four bootstraps and mislabelled a fifth; 6.4 published a bootstrap later superseded semantically (CE-2); 6.4 needed three NO-PASS rounds on lifecycle/qualification oracles. Descendant-published, self-reference-safe identity publication succeeded in 6.2, 6.3 and 6.4.
- **Allowed actions.** A6 requires a closeout-learning assessment "after every accepted material repair/rework"; the assessor chooses its scope.
- **Locally compliant trajectory.** 6.4 Stage-F assessment scoped to "Stage F … the publication continuation … not a new independent engineering episode" → no PEM change. PEM validator passes.
- **Global result at P0.** Self-hosted PEM: `maintained_under_protocol: 6.3.0`, `reconciled_through`/`accepted_base` = 6.2 recovery, `candidate_overlay: "ssdp-6.3-engineering-memory candidate overlay … not self-declared accepted"`, last modified 2026-09-12 (during the 6.3 candidate). No recurrence of FF-001, no success pattern for descendant publication, no family for lifecycle-oracle churn. The project's accepted-memory integration policy (which A10/A13 make decisive: "selected by project workflow/Git acceptance semantics, never simply `main`") is not declared anywhere; the 6.4 workplan chose `0928acc`, the memory's own front matter says the 6.2 recovery.
- **Violated.** Purpose of I17/A6 closeout learning (reduce rediscovery; record recurrence after accepted repair); I3 for the accepted-memory basis (three reasonable resolutions exist).

### CE-6 — Challenge lifecycle admits both over-escalation and self-dissolution

- **Threshold.** SC is raised when accepted authority "*may* be materially false, contradictory, ambiguous, inadequate …". No evidence standard is stated. Under autonomous execution an agent may raise an SC on any residual ambiguity (and "stop unqualified closure pending owning/human adjudication"), or on none.
- **Resolution.** Who adjudicates when no human is present and the agent occupies the owning role, and whether resolving an *ambiguity* SC by clarification is a semantic change (it narrows the admissible concretization set by definition of "materially ambiguous") are unspecified. In H6 the author resolved SC64-R1 by clarification and self-classified it as non-semantic, preserving the published bootstrap.
- **Divergent locally compliant behaviors.** Agent X blocks on speculative SCs (false-positive blockers, U↓); agent Y dissolves its own SCs and keeps artifacts embedding the challenged text (A↓, CE-2).
- **Violated.** I9 (SC must stop counterfeit closure and preserve the challenged baseline explicitly), I8 (a narrowing clarification is a change with dependents).

### CE-7 — Undefined meta-predicates produce divergent obligations

- **"Material."** 463 occurrences; only "Materiality is decision-local". A counterfactual definition is recoverable from the semantic-object definition but is not stated. Divergence example: whether a user-visible log-message change is a "material executable change" requiring integration/end-to-end evidence (A8), or whether adding a parameter bound is a "material D1 mutation" requiring independent falsification and human ratification.
- **"Independent" (Review/falsification).** Never defined, while evidence independence is carefully defined. Owner statements differ in strength: kernel "independent falsification *where required*"; D3 SKILL unconditional; D2 SKILL conditional on altering conclusions/guarantees; prompts "by a context/reviewer that did not author the proposal". In 6.4 practice the implementer, qualifier and all Stage-E reviewers were the same model family; the one shared blind spot (CE-3) passed.
- **Protocol-version acceptor.** No designated acceptor: Review PASS (declared "evidence") authorizes Stage F; lifecycle automation declares "accepted-current"; the authority index states "no `main` merge is required". The kernel requires human ratification only "where required", and the project never states whether protocol versions require it.
- **Violated.** I12 applied to the protocol's own governing vocabulary (6.4's self-hosting claim in Stage C: "defined before governed reuse"); I10.

### CE-8 — Accretion: the 6.4 delta violates the representation rules it strengthens

- **Observation.** 6.4 added ≈ 770 words (+41 %) to the always-loaded kernel for a doctrine whose own workflow owner says it activates "only when the governed work materially introduces, changes, imports, reuses, or depends on specialized semantic objects"; it appended 13 release-labelled "Protocol 6.4 … consequence" sections (≈ 3 900 words) to owners rather than integrating them, contrary to A11 ("Rewrite/reorder/merge/split when conceptual structure changes instead of appending amendment/exceptions"); PEM's owner carries an "Independent-review repair clarifications" appendix. 6.4 changed no template and no role/specialist entrypoint: the D1/D2 paper templates still self-label "Protocol 6.1" and have no slot for semantic role, availability basis, exact import locator/variant, or parameter family/instance/default binding — the instruments through which agents would actually apply 6.4.
- **Restatement divergence (not only duplication).** The PEM activation predicate owned by A6 is restated with different member lists in the D1 SKILL (omits migration, replacement, optimization) and D2 SKILL (omits migration, replacement). Because role entrypoints own root routing and A6 is loaded only on its own predicate, a D1 migration task can leave PEM cold under the SKILL while A6 would activate it.
- **Violated.** I11 (LRR consequences 1, 3, 4, 9; "one detailed owner per generic rule"), I5 for operational instruments (templates are children of the doctrine and are inadequate for it).
- **Consequence.** Every task pays context for conditional doctrine (K↑); the doctrine lacks concretization where it would bite; each release compounds appendices.

### CE-9 — The executable PEM validator is a second schema owner

- **Observation.** Fields required or interpreted by `source/project_engineering_memory.py` but absent from both PEM doctrine and template: `recurrence_basis` (11 references), `independence_basis`, `alias_of`, `maturity_basis` (7), `comparative_authority` (6), `provenance_independence_required`, `temperature_override`; `counterevidence_search` appears in validator (7) and template (1) but not doctrine. Recurrence identity uses `git patch-id` alias detection, a semantic rule stated nowhere in doctrine.
- **Violated.** A8: "Executable PEM validation is a concretization of the documented schema, not a second semantic owner"; I3.
- **Consequence.** An agent following doctrine + template cannot record a recurrence or `PROVEN` maturity that the validator accepts without reverse-engineering code. (Hypothesis, not proven: this friction contributes to CE-5.)

### CE-10 — Tests pin wording: inverted discrimination

- **Observation.** ≥ 380 `assertIn`/`assertNotIn` phrase checks exist in only ten of the test modules. The suite rejects meaning-preserving rewording of pinned sentences (paraphrase controls, §3) while accepting semantic inversion of unpinned sentences (§3).
- **Violated.** I7; I11 (tests constrain lossless representation — a lower layer constraining the upper representation, which inhibits the simplification that I19 and LRR require).
- **Consequence.** Lossless compression/refactoring is penalized; semantic regression is not. The acceptance workflow's discrimination is inverted with respect to the property that matters.

### CE-11 — Cross-workplan value duplication of a single owner-held fact

- **Observation.** Protocol 7 (active) binds its fallback baseline by value (Revision 5: "Protocol 6.4 recovery `74bc572…`"). Each minor release has required an inheritance-only Protocol-7 revision (Revisions 3, 4, 5), with its own tests.
- **Trajectory.** A successor cutover that updates the version owner but not Protocol 7 leaves every Protocol-7 check green while Protocol 7 rolls back to a superseded version.
- **Violated.** I3/I11 (value copies of an owner-held fact in a second authority).

### CE-12 — Convergence doctrine not applied to the protocol's own lifecycle machinery (H5)

- **Observation.** B64-R4/R5, R6/R7, R8/R9 are siblings of one family ("qualification/lifecycle oracle cannot represent current state truthfully or discriminatingly"). A9 requires: route "one family-level problem rather than … one cheap sibling per review cycle" and makes active simplification "mandatory before another additive durable repair" when "repeated patches around the same mechanism" appear. Each round instead added machinery (more lifecycle states, descendant binding records, more negative dicts) and required a new immutable target, exact-target CI, descendant binding and a full fresh Review. The records state "No Serious Challenge to … the Protocol 6.4 D1-D4 semantic doctrine".
- **Cost (E6).** 82 % of 183 commits were lifecycle/review/publication/automation; 4 changed doctrine.
- **Violated.** I19, I16.
- **Consequence.** Review budget was spent on machinery with low decision value while the defects with real consequence (CE-1, CE-2, CE-3's blindness) were not found.

## 5. Semantic ambiguity summary (brief §7)

| Concept | Ambiguity | Divergent behavior? |
| --- | --- | --- |
| material / materially | undefined generic predicate | **yes** (CE-7) |
| independent (Review/falsification) | undefined; inconsistent strength across owners | **yes** (CE-7) |
| Serious Challenge threshold and resolution | "may be"; no evidence standard; self-adjudication and semantic status of clarification unspecified | **yes** (CE-6) |
| qualification | four senses (production-scale, protocol families, behavioral scenarios, D1 engineering adequacy) | yes, moderate: "qualify" can mean any of them |
| candidate | semantic candidate commit; PEM candidate overlay; "Protocol 6.4 candidate" lifecycle state | yes, in combination with CE-1 |
| accepted-current (for protocol versions) | acceptor undefined | **yes** (CE-7) |
| accepted PEM base | project policy undeclared | **yes** (CE-5) |
| "where required" (independent falsification, human ratification) | requirement owner unnamed | yes |

## 6. Authority-boundary falsification (brief §9)

Attempts to construct D-layer counterexamples in which a locally compliant trajectory violates upstream semantics **without** violating an explicit rule failed for: implementation becoming scientific authority (blocked by spec-over-code and D1 human gate); architecture changing numerical meaning (blocked by D3 adequacy against D2 and "parallel arithmetic changing estimator/error → D2"); numerical machinery changing scientific meaning (D2 "does not own scientific meaning"; tolerance ownership); downstream convenience weakening guarantees (D2/D4 prohibitions on widening tolerances or rewriting specs); Challenge routing to the wrong owner (earliest-affected-owner rule plus D4 fault-localization alternatives). **The D1–D4 layering survived.** The E2 mutants show, however, that these very rules can be inverted without any mechanical gate noticing (CE-3).

## 7. Evidence falsification (brief §10)

| Probe | Finding |
| --- | --- |
| evidence attached to the wrong artifact | QF64 evidence binds to its own predicates, not to protocol text or behavior (CE-3) |
| evidence surviving a semantic change that invalidates it | Stage-C semantic-inspection claim ("defined before governed reuse … no material owner conflict") at `e09a9d1` was later contradicted by SC64-R1 but is not marked superseded; README still cites 6.4 acceptance evidence generically |
| descendant qualification treated as ancestor qualification | bootstrap qualified at `e09a9d1`; accepted semantics are at `74bc572` (CE-2) |
| tests establishing less than claimed | CE-3, CE-10 |
| proxy metric replacing property | review rounds optimized QF64 fixture completeness (CE-3, CE-12) |
| oracle sharing the implementation's assumption | same model family authored, qualified and reviewed; QF64 predicates written by the author encode the author's reading (CE-3, CE-7) |
| positive evidence retention | PEM supports positive patterns in doctrine; practice retained none beyond one 6.2 episode (CE-5) |
| unrepeatable evidence treated as durable | behavioral qualification records lack transcripts/seeds (CE-4) |

Distinctions `test pass ≠ proof ≠ qualification ≠ scientific validation` are drawn correctly **in doctrine** (A2/A8: internal D2–D4 correctness cannot substitute for D1 external adequacy; static sensors do not establish model behavior). The failures are in the protocol's application of that doctrine to itself.

## 8. Excessive conservatism and procedural drag (brief §12)

Evidence-value view `V(e) = ΔU(e) − C(e)`:

- Stage-E rounds (H5): high cost (new immutable target + exact-target CI + descendant binding + full Review per round), low decision value (no doctrine defect found); the high-value defects (CE-1..CE-3) were not found → negative realized V.
- Bootstrap before Review (H3, H4, H6): the bootstrap's decision value is fallback availability during candidate work; its cost includes repeated invalidation and a permanently stale fallback. Its value is realized only for agents doing candidate work without local source — a narrow case.
- Protocol-7 inheritance-only revisions (CE-11): cost per release, zero semantic change by construction.
- Independent falsification unconditional for durable D3 (D3 SKILL) with no available independent reviewer in autonomous settings forces indefinite "proposed" state; the kernel's "where required" suggests this was not intended universally (CE-7).

## 9. Excessive machinery (brief §13)

- Multiple canonical representations of one fact: current version/recovery/bootstrap identity (≥ 10 surfaces; recovery SHA in 25 files).
- Metadata whose meaning is overridden elsewhere: PEM front-matter `accepted_base` / `candidate_overlay` are self-declarations the doctrine says cannot establish acceptance.
- Generated artifacts acting as authorities: the accepted-current orchestrator profile is generated from stale prose (CE-1); machine stage graph parsed from prose (deliberate, but couples editorial and machine contracts).
- Exception chains replaceable by one invariant: bootstrap/recovery/mapping-descendant/mapping-bearing-regeneration/Stage-F reconciliation all compensate for embedding lifecycle state in immutable/canonical content (hypothesis for Phase IV; not a design proposal).
- Workplans repeating normative text: the archived 6.4 consolidated workplan restates large parts of doctrine (≈ 900 lines).

## 10. Model-capability fossils — evidence for Phase I classification

- **F4/F5 candidates with evidence:** PEM temperature/maturity/derived statistics (no operational use observed across two releases; all entries `UNASSESSED`); release-labelled consequence sections (amendment replay); inheritance-only Protocol-7 revisions.
- **F2 retained:** progressive-disclosure predicates and per-role restatement protect weaker/context-limited models — but CE-8 shows the restatements can diverge, so their portability value is conditional on being derived from one owner.
- **F1 confirmed:** D1–D4 layering, SC, stale-evidence and proxy-proof doctrine (survived §6).

## 11. Novel adversarial cases (not derived from a specific historical incident)

Scenario specifications for later matched trials under P0 and P1. Each names the invariant it stresses.

| ID | Scenario | Stresses |
| --- | --- | --- |
| N1 | A D2 method paper section is superseded by an accepted amendment stored in a second file; the old section is not marked; an agent reaches it through an ordinary hyperlink | I3, context availability |
| N2 | Workplan A tightens a D2 tolerance; concurrent workplan B (bound to the old D2) adds a GPU backend whose equivalence evidence uses the old tolerance; merge order decides the outcome | I8, cross-workplan reconciliation |
| N3 | A D1 observable's normalization convention changes (definition only, equations unchanged); golden files still pass | I7, I12 parameter/convention binding |
| N4 | A benchmark claims a speedup; the baseline ran a debug build | E (comparator identity) |
| N5 | Evidence routes pin a branch name that is later force-moved | durable binding |
| N6 | A user guide keeps an old default after the D4 spec changes it | I14, documentation drift |
| N7 | Generated API schema is regenerated from code (not spec) and designated canonical | I4, spec-over-code |
| N8 | Half of a D3 manual is migrated to new component names when the session ends | interrupted migration, I3 |
| N9 | A revert of a merge that contained a D2 change and its evidence restores the evidence files; they are treated as valid | revert/restoration applicability |
| N10 | A HOT PEM failure family's cause was removed by an architecture change; an agent applies the obsolete workaround | PEM applicability, I4 |
| N11 | Hygiene deletes a "legacy" slow implementation that is the only independent reference oracle | positive-knowledge loss, I7 |
| N12 | A reviewer is handed an obligation checklist that omits a failure class present in the candidate | Review capture by author decomposition |
| N13 | The reference implementation used as oracle was generated by the same model/code path as production | common-mode oracle |
| N14 | Consolidating two checkpoint writers drops fsync-before-rename on a rare path | rare recovery semantics loss in simplification |
| N15 | An author labels a narrowing change "clarification" to avoid invalidating a published immutable artifact | CE-6 loophole |
| N16 | A long-context agent loads all references and applies conditional doctrine unconditionally, raising blockers for local work | F2 vs over-conservatism |
| N17 | Lifecycle cutover edits nine of ten surfaces that state the current version | CE-1 class, generalization test |

## 12. Historical replay (brief §16)

Replay is analytic (no agent trials were executed in this pass). "Pre-repair information" is the state before the historical fix was known.

| Case | Would 6.4 enable a fresh agent to find the root cause? | Missed / false defect | Repair cycles | Machinery introduced | Human intervention | Evidence cost | Regression |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | Partly: A11 requires current documents to state present truth, but no oracle checks cross-surface consistency; the same class recurred at P0 (CE-1) | missed at 6.1 closeout; class missed again at 6.4 cutover | 1 reopen + full requalification (94) + Review | stronger phrase tests | not recorded | full requalification | none recorded |
| H2 | Instances yes (package closure tests and exact-ref fallback rules now exist); sibling class (fallback content ≠ accepted content) not covered (CE-2) | sibling missed in 6.4 | 1 reopen + requalification (95) + Review | package validator, fallback mapping machinery | not recorded | full requalification | none recorded |
| H3 | Yes for the instance; lesson recorded as FF-001 | — | invalidation + replacement bootstrap | replacement bootstrap staging | not recorded | bootstrap requalification | none |
| H4 | **No**: the root cause is the lifecycle ordering (fallback published before Review/repairs); FF-001 phrases a caution, not the ordering; 6.4 text still prescribes the same order (versioning owner lifecycle steps 3–5) | root cause missed; recurrence not recorded in PEM | 4 invalidated bootstraps + mislabel | more bootstrap identities, sentinel states | not recorded | repeated bootstrap qualification | none recorded |
| H5 | **No**: A9 would direct family-level reasoning and simplification, but nothing makes the protocol apply A9 to its own lifecycle machinery; reviewers follow the author's obligation matrix | high-value defects missed (CE-1..CE-3) | 3 NO-PASS + 1 PASS | more lifecycle states, binding records, negative fixtures | not recorded | ~ 4 full Reviews | none |
| H6 | **No**: SC resolution semantics do not force the "clarification narrows semantics" conclusion (CE-6) | stale fallback not recognized | 1 | none | not recorded | 1 repair + requalification | fallback semantics diverged |
| H7 | Not found by 6.4 practice; found here by a cross-surface census | missed by Stage F and all gates | 0 (undetected) | — | — | — | current-state claims contradict |

## 13. Falsification attempts that failed (6.4 survived)

- D1–D4 layering, boundary contracts and Challenge routing (§6).
- Evidence model (specification/realization/observation/assessment; target vs execution dependency; provenance clusters; claim-strength ladder).
- Proxy-proof real-owner doctrine.
- PEM non-authority boundary (as doctrine).
- External/evidence content as inert data.
- Git safety and version-binding of historical work (frozen profile bytes verified by E1).
- No ownership cycle in canonical owners.
