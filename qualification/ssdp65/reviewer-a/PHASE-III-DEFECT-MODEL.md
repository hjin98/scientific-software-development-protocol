---
kind: ssdp65-phase-iii-defect-model
investigation: SSDP-6.5-FRONTIER-MODEL-RE-EVALUATION
reviewer: A
subject: P0 = Protocol 6.4 at 55c085261eb827e3047637d045a8e6917ea6b962
authority: non-normative-diagnostic-evidence
status: frozen-for-cross-examination
blocking_findings: 2
material_findings: 9
improvement_opportunities: 2
serious_challenge_to_d1_d4_doctrine: none
created: 2026-09-24
---

# Phase III — Evidence-Backed Defect Model (reviewer A)

## 1. Disposition

**Protocol 6.4 did not survive unchanged.** Reviewer A admits two blocking and nine material findings, plus two improvement opportunities. **No defect was found in the D1–D4 authority model, the evidence model, proxy-proof doctrine or the PEM non-authority boundary**; these survived falsification (Phase II §6, §13).

The admitted defects concentrate where SSDP governs **itself** — its lifecycle-state representation, release qualification, meta-level vocabulary and representation practice — rather than in the object-level engineering doctrine it gives to agents.

This model does not decide the version outcome. Several findings are defect corrections within 6.4 semantics (the versioning owner's *patch* class); others concern the protocol's lifecycle and qualification design. The choice among "6.4 survives", "6.4.x patch" and "successor" is deferred until reviewer B's independent findings and cross-examination.

## 2. Finding tuples `F = (O, E, I, R, C, S)`

Severity scale (brief §17): **Blocking** — can produce materially incorrect or unsafe protocol behavior and requires repair before any candidate acceptance; **Material** — meaningfully reduces correctness, efficiency, generality or clarity without invalidating the protocol; **Improvement** — no demonstrated defect; **Preference** — no protocol consequence (none admitted).

### A-01 — Incoherent current lifecycle/version state across canonical and generated surfaces — **Blocking**

- **O:** Accepted-current canonical source and the generated accepted-current orchestrator profile assert that Protocol 6.3 is accepted-current and 6.4 is a candidate without recovery; every role/specialist skill description says "under Protocol 6.3"; the language router says Protocol 6.2 doctrine is authoritative; the versioning owner's own 6.4 section contradicts itself.
- **E:** Phase II CE-1 (file/line quotations), E1 (every gate green), E3 census.
- **I:** I3, I13, I14, I11.
- **R:** (R-1) the current-lifecycle fact is copied by value into ≥ 10 surfaces with no single owner that other surfaces reference by role; (R-2) closeout oracles enumerate specific stale phrases per surface instead of asserting an invariant over all surfaces; (R-3) cutover is a post-Review transaction outside Review and outside any coherence oracle.
- **C:** Orchestrated runs and skill selection receive a false baseline; rollback/version-bound reasoning and Protocol-7 inheritance can bind to the wrong version; the defect is invisible to the entire acceptance workflow.
- **S:** **Blocking** — the same cutover mechanism would reproduce the defect for any successor; it must be repaired before a candidate can be accepted. Repair owner: versioning owner (A12) and documentation owners (A11), with descendants regenerated.
- **Strongest counterargument:** the versioning owner is canonical for version identity, so a careful agent would resolve the conflict in its favor. **Rebuttal:** 6.4's own I3 forbids resolving simultaneous conflicting current statements by precedence guesses; the orchestration profile is the surface Core actually executes.

### A-02 — Release gate does not discriminate semantic change; it discriminates wording — **Blocking**

- **O:** QF64-A..N qualification predicates take only test-local dicts as input; the complete acceptance workflow passed 12 of 15 single-sentence inversions of core doctrine (owner conflict, stale pass, SC baseline, spec-over-code, tolerance ownership ×2, parameter-sensitive evidence, source/context availability, human gate, PEM non-authority, abstraction adequacy, absence-is-not-evidence) and rejected meaning-preserving paraphrases of pinned sentences (Phase II §3).
- **E:** E2 (`evidence/mutation-results.json`), E8, CE-3, CE-10; Stage-C record; final Review statement that QF64 "provides discriminating polarity".
- **I:** I7, I15; A8's own requirements on counterfactual oracles and on string presence.
- **R:** (R-4) protocol qualification is defined as internal polarity of author-written predicates plus phrase presence; nothing binds protocol-qualification evidence to its real semantic consumer (protocol text interpreted by agents); (R-5) tests pin exact wording, so representation is constrained while meaning is not.
- **C:** A candidate that inverts governing doctrine can pass every mechanical gate; acceptance then depends wholly on Review; lossless simplification is penalized.
- **S:** **Blocking** for any successor acceptance claim resting on this gate. Material for accepted 6.4 (doctrine is not shown wrong; its acceptance evidence is weaker than stated). Repair owner: testing owner (A8) for the protocol-qualification method; the repository's D4 test suite.
- **Strongest counterargument:** mechanical checks were never meant to establish semantics; Review is the semantic gate (Stage C says so). **Rebuttal:** then QF64 PASS must not be presented as qualification of semantic classes (README/AGENTS/Stage C/Review do so), and the Review itself (H5) was directed by the same obligation matrix and accepted the self-referential oracle. Mutant selection bias: reviewer A wrote mutants after reading tests; this inflates the undetected share for the development set and is why HO4 is pre-registered.

### A-03 — Authorized 6.4 public fallback diverges from accepted 6.4; recorded lesson did not prevent recurrence — **Material**

- **O:** Bootstrap `e09a9d1` (sole authorized 6.4 fallback) differs from recovery `74bc572` in kernel, evidence owner, writing owner and prompts; the difference is the repair of a Serious Challenge (SC64-R1) self-classified as "clarification"; the bootstrap's prompts permanently state that 6.3 is accepted-current and no 6.4 fallback exists. FF-001 was marked APPLICABLE in the 6.4 HAS; its occurrence count remains 1 after 6.3's four invalidated bootstraps and this episode.
- **E:** CE-2, E4, H3/H4/H6, archived 6.4 workplan §20 and §27, Stage-F closeout.
- **I:** I3/I12 (one canonical meaning per version), I13, I9, purpose of I17.
- **R:** (R-1) lifecycle state embedded in immutable content; (R-6) lifecycle orders fallback publication before Review, so any Review-driven semantic repair necessarily strands the fallback; (R-7) SC resolution does not classify an ambiguity-removing clarification as a semantic narrowing.
- **C:** Agents following the prescribed fallback route obtain non-accepted semantics and a false lifecycle statement; the H3/H4 class will recur under the same lifecycle.
- **S:** **Material.** Practical semantic harm of the stranded text is modest (the pre-repair `USES_DEFINITION` sentence is interpretable), but the false lifecycle statement is not, and the structural cause is shared with A-01. Repair owner: versioning/lifecycle owner (A12); Challenge semantics (A1).

### A-04 — No instrument ties release acceptance to engineering outcomes — **Material**

- **O:** Behavioral qualifications 92/92, 94/94, 95/95, 115/115, 260/260 PASS by the author model family judging whether text rejects stated wrong behaviors; no baseline arm, no recorded failure, no transcripts/seeds; 6.1 reopened twice after its PASS.
- **E:** CE-4; qualification records; history.
- **I:** I7 (discrimination; stochastic replicate identity), I16.
- **R:** (R-4) "qualification" for protocol releases is defined as conformance of text to author intent, not as comparative outcome evidence.
- **C:** SSDP cannot currently show that any version improves development outcomes over its predecessor (RQ10), nor detect a version that makes agents worse.
- **S:** **Material.** (It becomes blocking only for a claim `P1 ≻ P0`; the pre-registered design already requires matched trials.) Repair owner: A8 + A12.
- **Strongest counterargument:** scenario qualification was designed as a conformance check, which it performs. **Rebuttal:** release records and README present it as acceptance qualification; its measured miss rate on 6.1 is non-zero and its false-positive rate is unmeasured.

### A-05 — Project memory does not learn across releases; accepted-memory basis is undeclared — **Material**

- **O:** After 6.3 and 6.4 acceptance the self-hosted PEM still declares `maintained_under_protocol: 6.3.0`, basis = 6.2 recovery, "6.3 candidate overlay"; no recurrence, success pattern or new family recorded despite repeated bootstrap invalidation, descendant-publication successes and three NO-PASS rounds; the 6.4 closeout-learning assessment scoped itself to Stage F; the project never declares the policy that selects the accepted PEM base.
- **E:** CE-5, E7, Stage-F closeout, 6.4 HAS (`accepted_pem: 0928acc…`), PEM front matter.
- **I:** I17 (purpose), I3 (three defensible accepted bases).
- **R:** (R-8) closeout-learning scope is chosen by the assessor rather than defined as "the whole accepted intervention since the last accepted memory basis"; (R-9) no rule converts a candidate overlay into accepted memory at the project acceptance event or requires the project to declare the selection policy; self-declared front-matter fields persist after they stop being true.
- **C:** The memory's most valuable lessons (both negative and positive) are absent; HAS dispositions become ritual (CE-2 shows APPLICABLE without effect).
- **S:** **Material.** Repair owner: workflow owner (A6) for closeout scope; PEM owner (A10) and Git owner (A13) for basis promotion/declaration.

### A-06 — The executable PEM validator is a second schema owner — **Material**

- **O:** Validator requires/interprets fields absent from doctrine and template (`recurrence_basis`, `independence_basis`, `alias_of`, `maturity_basis`, `comparative_authority`, `provenance_independence_required`, `temperature_override`) and applies a `git patch-id` alias rule stated nowhere in doctrine.
- **E:** CE-9, E7 field census.
- **I:** I3; A8 "concretization of the documented schema, not a second semantic owner".
- **R:** (R-5) executable concretizations accreted semantics without reconciliation to the canonical owner.
- **C:** Following doctrine and template cannot produce a valid recurrence or `PROVEN` record; plausible contributor to A-05 (causal link unproven).
- **S:** **Material.** Repair owner: PEM owner (A10) — decide which fields are doctrine and which are removed.

### A-07 — Serious Challenge lifecycle under-specified (threshold, adjudicator, semantic status of resolution) — **Material**

- **O:** SC fires when authority "may be" defective with no evidence standard; adjudicator is unspecified when the agent occupies the owning role and no human is present; resolving an ambiguity SC by clarification is not classified as a semantic change.
- **E:** CE-6, H6.
- **I:** I9, I8.
- **R:** (R-7) SC defined by trigger and routing but not by resolution semantics and evidence standard.
- **C:** Both false-positive blockers (autonomy loss) and self-dissolving Challenges with stranded artifacts are locally compliant.
- **S:** **Material.** Repair owner: kernel (A1) Challenge section.

### A-08 — Governing meta-predicates undefined or inconsistently strong — **Material**

- **O:** "Material(ly)" (463 uses) has no generic definition; "independent" Review/falsification is undefined and its requirement strength differs across kernel, D1/D2/D3 SKILLs and prompts; "where required" has no named requirement owner.
- **E:** CE-7, E5.
- **I:** I12 applied to the protocol's own governing vocabulary; Stage-C self-hosting claim.
- **R:** (R-10) the protocol's definition discipline was applied to object-level semantics but not to its own control predicates.
- **C:** Divergent obligations for identical situations (integration evidence, independent falsification, human gates); common-mode Review (same model family for authoring, qualification and review) is locally compliant.
- **S:** **Material.** Repair owner: kernel (A1) with consistent consequences in D1–D4 owners and prompts.

### A-09 — Acceptance authority for protocol versions is unassigned — **Material (stakeholder decision required)**

- **O:** Review PASS (self-described as evidence) authorizes Stage F; lifecycle automation declares "accepted-current"; the index states no `main` merge is required; no human ratification is recorded or required by project declaration.
- **E:** CE-7; Stage-F records; authority index; commit authorship ("Protocol 6.4 lifecycle automation").
- **I:** I10, I4 (a Review conclusion functioning as authority).
- **R:** (R-10) meta-level governance parameter left undeclared.
- **C:** A successor could be declared accepted without the stakeholder's act; the investigation's own closure step ("bind the accepted candidate") has no defined acceptor.
- **S:** **Material**; must be decided by the human stakeholder before any acceptance. Repair owner: stakeholder, recorded by the versioning owner/`AGENTS.md`.

### A-10 — Representation accretion contrary to the Lossless Representation Rule — **Material**

- **O:** Always-loaded kernel +41 % in 6.4 (+70 % since 6.2) for conditionally activated doctrine; 13 release-labelled appendix sections; restated predicates diverge (PEM activation lists in D1/D2 SKILLs vs A6); templates not updated since 6.1 labels and lacking 6.4 slots.
- **E:** CE-8, E5.
- **I:** I11 (LRR consequences 1, 3, 4, 9), I5 for operational instruments.
- **R:** (R-11) releases are authored as additive deltas; no rule requires integration of a release into owners and instruments before acceptance.
- **C:** Context cost for every task; doctrine not operationalized in the templates agents fill; divergence risk grows per release.
- **S:** **Material.** Repair owner: A1/A11 and template owners.

### A-11 — Review/repair cycles optimize the author's obligation matrix; convergence doctrine not self-applied — **Material**

- **O:** Three NO-PASS rounds on sibling defects of one lifecycle/qualification-oracle family; each round added machinery; high-consequence defects (A-01, A-02, A-03) were not found; 82 % of cycle commits were lifecycle/review/publication.
- **E:** CE-12, H5, E6.
- **I:** I19, I16, I6 (Review reconstructs, it does not replay the author's decomposition).
- **R:** (R-12) Review scope is seeded by the author's obligation matrix; A9's family/simplification triggers are not applied to protocol lifecycle machinery.
- **C:** Large K for low decision value; systematic blind spots outside the matrix (N12).
- **S:** **Material.** Repair owner: workflow (A6) and convergence (A9) owners.

### A-12 — Cross-workplan value copies of owner-held facts — **Improvement** (with evidence of cost)

- **O:** Protocol 7 binds its fallback baseline by value; Revisions 3–5 exist only to update that value.
- **E:** CE-11.
- **I:** I3/I11.
- **R:** R-1.
- **C:** Per-release cost; silent staleness if forgotten.
- **S:** **Improvement opportunity** (no observed failure yet). Repair owner: Protocol 7 workplan owner jointly with versioning owner — out of this investigation's mutation scope.

### A-13 — PEM salience/maturity machinery without observed use — **Improvement**

- **O:** Temperature thresholds, maturity lattice and derived statistics exist; all self-hosted entries are `UNASSESSED`; no update in two releases.
- **E:** E7.
- **I:** I11 / minimum justified complexity (I2) — only as hypothesis.
- **R:** Unknown: non-use may reflect A-05/A-06 rather than lack of value.
- **C:** Maintenance/validator complexity (validator ≈ 1 400 lines) without demonstrated benefit.
- **S:** **Improvement opportunity**; no removal is justified without evidence from projects that use PEM (holdout HO3). Classified F4/F5 *candidate* only.

## 3. Root-cause clusters

| Cluster | Root cause | Findings |
| --- | --- | --- |
| RC-α | Mutable lifecycle/identity state is stored by value in many canonical, immutable and generated surfaces; no single owner is referenced by role; cutover is manual and outside Review/oracles | A-01, A-03, A-12 |
| RC-β | Release qualification measures text presence and author-written proxies rather than semantic discrimination or engineering outcomes; Review inherits the author's obligation matrix | A-02, A-04, A-11 |
| RC-γ | Meta-level control vocabulary and governance parameters are undefined (materiality, independence, acceptor, SC resolution, closeout scope, accepted-memory policy) | A-05, A-07, A-08, A-09 |
| RC-δ | Additive release practice and executable concretizations accrete representation/semantics outside canonical owners | A-06, A-10, A-13, part of A-02 |

**Cross-cutting hypothesis (for Phase IV, not a design):** SSDP's object-level rules — one owner per claim, evidence must discriminate its real owner, convergence triggers simplification, abstraction adequacy of children, definition before use — are sound, but SSDP does not apply them to its own lifecycle, qualification and representation. Most admitted defects are instances of that single self-application gap.

## 4. Research questions — status after Phase III

| RQ | Status | Answer so far |
| --- | --- | --- |
| RQ1 fundamental vs historical | answered (provisional) | F1: D1–D4 layering, SC, stale-evidence, proxy-proof, human gates, unexecuted-check blocking, snapshot handoff. F2: progressive disclosure, per-role restatement. F3: HAS/evidence-route syntax, obligation matrices. F4 candidates: bootstrap/recovery dual identity and staged publication ceremony. F4/F5 candidates: PEM temperature/maturity statistics, release-labelled appendices, inheritance-only revisions. |
| RQ2 missing invariants | answered | lifecycle-state coherence across surfaces (A-01); release-gate semantic discrimination (A-02); one-meaning-per-version across fallback and recovery (A-03); SC resolution semantics (A-07); closeout-learning scope (A-05) |
| RQ3 semantic compression | open | candidates identified (lifecycle identity by reference; restatement → route; self-application principle); coverage/exclusion/generalization not yet argued |
| RQ4 excessive conservatism | answered (evidence) | Stage-E cycles on machinery; bootstrap-before-Review; unconditional D3 independent falsification in autonomous settings; inheritance-only revisions |
| RQ5 insufficient constraint | answered | semantic drift passes all gates (E2); authority drift passes (A-01); evidence drift passes (A-03) |
| RQ6 layer ownership | answered | D1–D4 boundaries complete and coherent in doctrine but not mechanically enforced; meta-level ownership gaps (A-08, A-09) |
| RQ7 evidence epistemology | answered | doctrine distinguishes test/proof/qualification/validation correctly; self-application fails (A-02, A-04); "qualification" overloaded |
| RQ8 simplicity | open (likely yes) | evidence of removable duplication and ceremony; no compression proven |
| RQ9 model independence | answered for findings | the two blocking findings were produced by mechanical instruments (a grep census and a mutation script) and do not depend on frontier-model capability; they are protocol-design defects |
| RQ10 empirical improvement | not testable yet | no P1; no trial infrastructure |
| RQ11 novel generalization | not testable yet | N1–N17 specified for later trials; holdout reserved |
| RQ12 causal usefulness | not testable yet | requires P1 and ablation |

## 5. Stop-condition decision (brief §18)

`D = {A-01 … A-13}` is non-empty and contains blocking findings; Protocol 6.4 is **not** recorded as surviving the frontier review unchanged. This does **not** establish that a Protocol 6.5 is warranted:

- A-01 is a defect correction within accepted 6.4 semantics (patch class).
- A-02/A-04/A-11 concern how SSDP qualifies and reviews itself; they must be resolved before any successor acceptance claim, but could be resolved in lifecycle/qualification practice without changing D1–D4 doctrine.
- A-03, A-05–A-10 are candidate protocol-level changes subject to Phase IV coverage/exclusion/generalization tests.

Next step: freeze these findings (commit), obtain reviewer B's independent findings, then cross-examine. Phase IV–VIII remain unauthorized.

## 6. Known weaknesses of this finding set (for cross-examination)

1. Reviewer A authored the mutants after reading the tests (selection bias); HO4 is the unbiased measurement.
2. Historical replay is analytic, not executed; causal claims about what a fresh agent "would" do are predictions.
3. Two historical review records could not be read in this session; H5-era 6.2/6.3 review content is represented by file names and later records only.
4. Downstream-project evidence (HO3) was unavailable; PEM findings (A-05, A-06, A-13) rest on one self-hosted project.
5. Reviewer A shares model lineage risks with earlier reviewers in kind (a single frontier model); its blind spots are unknown until reviewer B reports.
