---
kind: ssds-major-architecture-workplan
workplan_id: SSDS-8.0-GRAPH-NATIVE-DETERMINISTIC-ORCHESTRATION-ARCHITECTURE
protocol_version: 6.6.0
target_system_version: 8.0.0
status: proposed
created_date: 2026-10-01
revised_date: 2026-10-01
design_revision: 3
source_branch_basis: f96b7ccf90dede4150d0efa17264fff07ec12d0d
source_branch: ssdp-7.0-scientific-epistemic-closure
design_basis: befe6782e7c8fe038bf7cb764646d133ca167855
prior_review: qualification/ssds80/WORKPLAN-REVIEW-SSDS-8.0-441CF5C-NO-PASS.md
prior_reviewed_candidate: 441cf5c4cce0428b44c6d3e15db697b0b4f6262c
review_history:
  - qualification/ssds80/WORKPLAN-REVIEW-SSDS-8.0-F9D9DE8-NO-PASS.md
  - qualification/ssds80/WORKPLAN-REVIEW-SSDS-8.0-441CF5C-NO-PASS.md
design_review_state: pending-fresh-independent-d3-review
d3_architecture_state: proposed
implementation_handoff: not-authorized
active_serious_challenge: none
supersedes:
  - SSDP-8.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-CONSOLIDATED
  - SSDS-8.0-GRAPH-NATIVE-DETERMINISTIC-ORCHESTRATION-ARCHITECTURE-BEFE678-HYPOTHESIS
---

# SSDS 8.0 — Deterministic Orchestration Architecture: Basis-Stamped Judgments over Content-Addressed Units — Prospective Workplan

The workplan ID keeps the historical `GRAPH-NATIVE` lexeme for routing stability. The architecture it carries is not graph-native in the sense of its predecessor hypothesis (§3): graphs are derived views over one typed relational substrate.

## 0. Disposition

```text
GOVERNING DESIGN PROTOCOL: SSDP 6.6.0 (accepted-current; identities owned by PROTOCOL-RELEASE-STATE.yaml)
TARGET: SSDS 8.0.0, the system-level successor to the document-controlled SSDP line
THIS FILE: single current prospective SSDS 8 architecture handoff, design revision 3; proposed, not accepted-current;
           not an Architecture Manual
PRIOR REVIEWS: f9d9de8 NO-PASS (qualification/ssds80/WORKPLAN-REVIEW-SSDS-8.0-F9D9DE8-NO-PASS.md), repaired by revision 2;
           441cf5c NO-PASS, three blockers A-C and findings N6-N10
           (qualification/ssds80/WORKPLAN-REVIEW-SSDS-8.0-441CF5C-NO-PASS.md), repaired here at their owners (§0.1)
SUPERSEDES: the consolidated Protocol 8 plan (archived byte-identically, with its nine-file lineage)
            and the befe678 graph-native hypothesis (archived byte-identically as ...-BEFE678-HYPOTHESIS.md)
SERIOUS CHALLENGE: NONE (§1.3 records why the governing goals are judged consistent)
PROTOCOL 7: active closure; inheritance NOT FINAL; §19 lists prospective inputs only
INDEPENDENT D3 REVIEW: ready for a fresh independent falsification Review of design revision 3; this revision is
            refinement, not acceptance, and awards itself nothing;
            a PASS cannot authorize D4 before Phase A (Protocol 7 reconsolidation) and Phase C (accepted Architecture Manual)
SSDS 8 D4: NOT AUTHORIZED
```

**What the architecture is.** Four primitives (§5): content-addressed **units** (leaf regions grouped into acceptance **subjects**), typed **relations**, immutable **records** in one append-only ledger, and the **basis** each record relied on. Everything else — validity, currency, obligations, readiness, impact, context, views — is a pure stratified derivation (§6.6). One Admission writer serializes every canonical change (§6.8). The ledger is a Git object chain on one authoritative ref, appended by single-ref compare-and-swap, admitted only once a witness quorum holds the new head, and published to the product integration ref as a reconciled effect (§15).

**Three separations carry the design.** Each removes a class of failure rather than one example:

| Separation | Rule | Failure class it makes impossible |
|---|---|---|
| observed repository state vs admitted governance state | content proposes; admitted records enact. Ruleset, structural roles, membership, scope and acceptance change only by admission (S11, §6.1) | authority, routing or acceptance arising from repository presence, foreign pushes, restores or merges |
| definitional dependency vs warrant dependency | every relation type has a closed semantic role and cycle class; cycles are legal only among definitional edges inside a declared simultaneous-definition group (§6.2) | circular warrant, authority, evidence, provenance or lineage, inside or across subjects |
| appended ledger state vs current-qualified state | an append is provisional until a witness quorum holds its exact head; only admitted state is ever asserted current (P4, §15.3-§15.4) | a historical prefix or an unwitnessed append presented as the current head |

### 0.1 Revision 3: what changed and why

The 441cf5c Review returned NO-PASS with three blockers. Each was treated as a falsification hypothesis, not as authority, and was reconstructed independently from the accepted 6.6 owners at the public-source commit named by `PROTOCOL-RELEASE-STATE.yaml` (`22f4bdba…`; the branch's evolving `source/` was not used as 6.6 authority). All three were confirmed. In each case the repair adopted here is stronger than the Review's minimum, and the out-of-matrix pass (§27) found and closed three further defects of the same families.

| Finding | Verified against | Repair (earliest owner) |
|---|---|---|
| **A** same-subject SCC admitted circular warrant | 6.6 semantic-definition owner: mutual *definitions* use an explicit simultaneous node; circular claim warrant is invalid; a dependency graph never warrants its endpoints. Evidence owner: lineage is acyclic | Closed, versioned relation vocabulary: each type has a semantic role and a cycle class. A **simultaneous-definition group** (SDG) is a *semantic* declaration, accepted with its subject's revision. Every relation cycle must lie inside one SDG and use only definitional edges. Unknown types fail closed. Condensation is representation only. Legality is checked at Admission and is also an S0 well-formedness fact that S2 consumes (§6.2, §6.6) |
| **B** foreign structural declarations took effect in S0 while quarantine lived in S3 | 6.6 workflow owner: repository presence promotes nothing. Evidence owner: restoring old content restores no validity. Risk-override rule: descendants never reset to accepted-current | **Observed vs effective structure.** Effective structure `Σ` is a fold of admitted structural changes. Absorption sets only the observed tree. Quarantine `Q` and the affected subjects `aff(Q)` are S0 facts, which S2 consumes (`ok(s)`). Acceptance belongs to a **subject tenure** and never revives. The challenge freeze applies to source and destination subjects. Adopting a foreign declaration means re-authoring it through Admission (§6.1, §6.6, §6.8, §11, §12.2) |
| **C** anchoring lag contradicted P4 | 6.6 storage and concurrency owners: partial or older state must not look valid; do not claim a commit before publication completes. The Review's L99/L100 world | **Strong P4.** An append is *provisional*; a witness-quorum checkpoint of the exact head *admits* it, and that is the commit point for every external effect. Read/write quorum intersection lets every qualifying evaluator see every admitted head. Publication, dispatch and current assertions follow admission. The bounded-lag mode and the multi-ref publication optimization are withdrawn (§2.4, §15.3-§15.4) |
| N6 same-subject circular-warrant discriminator | — | §22 relation-cycle trajectories |
| N7 anti-rollback expectation normalized the defect | — | §22 anchoring expectations rewritten to discriminate the strong contract |
| N8 structural-only foreign trajectories | — | §22 structural intake and tenure trajectories |
| N9 Manual deferrals acceptable only while D4 stays gated | — | unchanged; D4 remains gated by Phases A and C |
| N10 routing test respects DS-001 | — | unchanged; the test still reads frontmatter only |

**Where the repair exceeds the Review's minimum.**

- *A.* The Review asked for a semantic-role field. This revision also makes simultaneity itself semantic content, so declaring an SDG needs acceptance. It puts legality in S0, so a ruleset reclassification or an absorbed violation fails closed in validity, not only at Admission. It rejects self-relations, so single-object recursion stays the unit's own content.
- *B.* Of the Review's two options, this revision takes the observed/effective separation. It is the same rule already used for the ruleset (content proposes, an adoption record enacts), it adds no store (`Σ` is derived from the ledger), and it makes quarantine a lower-stratum fact by construction. It adds the tenure lifecycle the Review asked for. It also closes two paths the Review did not name: re-scoping a challenged *destination* subject, and an acceptance revived by `LEDGER_LOSS` truncation (§27.1).
- *C.* "Synchronous" anchoring alone is not enough: a fresh clone that reaches only witnesses lacking the newest checkpoint would still accept the older head. This revision therefore makes read/write quorum intersection part of the contract (`q_a + r > N + f`). It withdraws the multi-ref publication optimization, which published before anchoring. It adds lineage-retirement checkpoints, so a purged lineage cannot be presented as current from a stale mirror (§15.5).

#### Revision 2 (prior) record

Design revision 1 (`f9d9de8`) re-derived the problem from the governing objectives, independently of the befe678 vocabulary. It replaced the four-graph, event-sourced, epoch and frozen-plan design with a smaller one (§3, §17), and restored lineage routes that befe678 had dropped from the authority index. Design revision 2 (`441cf5c`) kept that core and repaired the f9d9de8 Review's findings, reconstructed against the same 6.6 owners; two further recursion defects were found while repairing B2. Rows below record what revision 2 did; where revision 3 changed the mechanism, the row says so.

| Finding | Verified against | Repair (earliest owner) |
|---|---|---|
| **B1** byte-preserving split manufactured child acceptance | 6.6 kernel: a lower mechanism gains no authority; workflow owner: a clarification that narrows admissible interpretation is a semantic mutation unless established representation-only. The f9d9de8 rule also regressed befe678's "structural split requires no false semantic claims" | Acceptance is of an exact `(subject, scope, revision)`. Refinement creates **parts** of the unchanged subject; acceptance never moves by rule. A part becomes its own subject only through a qualified acceptance judgment (§6.1, §12.2) |
| **B2** currency/validity recursion admitted two fixed points | 6.6 semantic-definition owner: mutual definitions use an explicit composite node; circular warrant is invalid | Derivation is four strata with a monotone least fixed point in the support tier and well-founded challenge recursion. Admission keeps the support dependency graph acyclic (§6.6). *Revision 2 also made simultaneous groups composite subjects and licensed any same-subject relation cycle; revision 3 replaced that with SDGs and role-based cycle legality (Blocker A)* |
| B2 (additional) derived `acc(policy)` fed derivation of the rules that compute `acc` | same | The ruleset in force is a ledger fact named by a human-gated adoption record (§6.6 S0) |
| B2 (additional) discharge required "every triggered obligation discharged" — a negation over currency inside validity | same | Removed from discharge; collateral impact is an Admission legality check (§6.8 step 8, §7.4) |
| **B3.1** remote multi-ref atomicity assumed | Git `atomic` push is a server-advertised capability | Single-ref append everywhere; integration publication is a reconciled effect (§15.3). *Revision 2 kept atomic multi-ref push as an optional optimization; revision 3 withdrew it because it would publish before admission* |
| **B3.2** hash-valid rewind invisible to fresh clone | 6.6 storage owner: recovery must not make partial/older state appear valid | Declared threat model; signed checkpoints held by witnesses outside the replica's control plus participant high-water marks; fresh clone without a witness is never current. *Revision 2 still allowed an undetectable rewind inside the anchoring lag; revision 3 re-specified currentness as quorum admission (Blocker C, §15.4)* |
| **B3.3** new lineage does not remove a leaked secret | 6.6 security owner: exposure needs rotation/history remediation; deleting the latest copy is insufficient. Git owner: `main` history is never discarded | Closed no-free-text schema, bounded Admission checks, breach protocol with rotation, replica invalidation, sanctioned purge or new repository, explicit yielded guarantees (§15.5) |
| **N1** Architecture 1.6.0 transfer incomplete | the 26 frozen invariants and frozen surfaces, plus implemented Core | Per-invariant table (§16.2). Two f9d9de8 "preserved" claims (inv. 2, 26) were inaccurate and are corrected |
| **N2** routing test parsed prose | test inspected | Test now parses frontmatter: lineage closure via `supersedes`, routing via the index's `current_handoffs`. Semantic adequacy stays with Review |
| **N3** index reassigned Stage H itself | index and Protocol 7 Stage H text | Index and §0.2 phrase the relationship prospectively; only Protocol 7's owning closeout can retarget its obligation |
| **N4** widening not executable | §6.4 of f9d9de8 | Exact scope chain, boundary-completeness judgment, relation class, whole-tree fallback (§6.5) |
| **N5** `Change` primitive and cross-repository scope | primitive audit | `Change` demoted to a typed Admission request (§6.8); external units and the cross-repository boundary specified (§11.4) |
| N6 befe678 archival identity | blob re-checked locally | `af9c005b15c4d0cfc56b0efb4dfe6b032fa4d958` at `befe678` and in the archive; unchanged |

Revision 2's out-of-matrix and minimum-architecture passes (§27) repaired four further abstraction defects: carve-out cutover vs holistic legacy acceptance; completeness surviving scope-membership change; direct push to the ledger ref; challenge escape by re-scoping unchanged content (the ordinary-Admission path; revision 3 closed the foreign path).

### 0.2 Protocol 7 Stage H routing (prospective)

The active Protocol 7 consolidated workplan (Stage H) assigns its closeout "the Protocol 8 inheritance reconciliation" of `SSDP-8.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-CONSOLIDATED`, which this file supersedes. Neither this file nor the authority index amends that obligation. When Protocol 7's owning closeout executes Stage H, it is expected to reconcile or retarget the obligation, through its own authority process, to the then-current SSDS 8 handoff (presently this file: §19 inputs, §24 baseline). That reconciliation advances the pre-cutover baseline, selects no SSDS 8 architecture, authorizes no D4, and recommends (never self-adopts) a governing-version adoption.

### 0.3 Project Engineering Memory basis

This is replacement/migration design for mature machinery, so the PEM predicate fires. Accepted/base memory: `PROJECT-ENGINEERING-MEMORY.md` on `main` at `2585b73f00420daca185a4fbb9ac42a79473eda1` (`reconciled_through` `23e46543c174a8451bbadc402df63538105eab10`), blob `1561797125622f355f84eb27319f87e8fa4227d9`; `main` has not advanced, and this branch carries no overlay (identical blob, re-verified for revision 3). Historical Applicability Set:

| Entry | Binding | Disposition for this design |
|---|---|---|
| PC-001 frozen historical profiles | `AUTHORITY_BOUND` (versioning owner) | Applicable and mandatory through its owner: every version-bound profile/resource stays independently preserved (§24, §16.2). |
| SP-002 self-reference-safe identity | `EVIDENCE_ONLY` | Applicable: admission records reference commits and ledger heads, never the object that contains them; the checkpoint that admits entry `n` lives at witnesses, outside entry `n` (§6.8, §15.4). |
| FF-001 premature immutable publication | `EVIDENCE_ONLY` | Applicable to genesis, cutover, replacement lineages after a confidentiality incident, and SSDS release: no immutable identity is published before every required route and record validates (§12.5, §15.5, §23). Applicable by analogy to currentness: no ledger head is published or asserted current before the durability condition that makes the claim true holds (§15.3). |
| DS-001 synthetic fixtures do not discriminate real-owner defects | `EVIDENCE_ONLY` | Applicable to qualification (§22) and to the routing regression test (N2): synthetic/string checks bound only mechanical properties. |
| SP-001 repair canonical source, regenerate derivatives | `EVIDENCE_ONLY` | Applicable by analogy: derived views are regenerated from ledger and content, never patched (§6.6). |

## 1. Problem, objective and allocation

### 1.1 The engineering problem

SSDS 8 coordinates stochastic reasoning agents and humans over evolving scientific software while preserving SSDP's hierarchy of semantic authority. Wherever an answer is mechanically decidable, it must answer mechanically: what is authoritative; what depends on what; what changed; what is stale; what work is legal now; what may proceed concurrently; what context a task needs; what an agent modified; whether a result still applies to the state it was produced against; and what genuinely needs semantic judgment or human authority. It must absorb manual, external and legacy change without corrupting canonical state. It must let an old repository become governed progressively without stopping production. It must let history be reconstructed after failures, migrations, rollback attempts and schema evolution.

### 1.2 Allocation principle

```text
mechanically decidable question                  -> deterministic machinery, answered exactly
mechanically decidable only conservatively       -> deterministic machinery, answered by sound
                                                    over-approximation (never under-approximation)
precision beyond the conservative answer         -> a focused semantic judgment that narrows it
judgment already made, basis still current       -> reused mechanically; never re-asked
unresolved semantic question                     -> agent
designated authority decision                    -> human gate
canonical state change                           -> single serialized admission
```

*Machines over-approximate; judgment narrows; recorded judgment is reused until its basis moves.* Byte identity is a mechanical fact; what a set of bytes is accepted *as* is a semantic fact (§6.1). The agent is a semantic reasoning resource, never a bookkeeper. SSDS 8 succeeds only if added deterministic machinery reduces, rather than transfers, complexity to agents and humans.

### 1.3 Consistency of the governing goals (Serious Challenge check)

Four apparent conflicts dissolve under the architecture rather than being engineered around:

- *Mandatory deterministic control vs never stopping production.* Production commits remain ordinary Git; non-closure blocks canonical governance status, not execution (§11, §12).
- *Minimal agent context vs "absence of an edge is not independence".* Context is minimal only within judged-complete scopes; elsewhere the basis widens conservatively and the brief says so (§6.5, §9).
- *Single canonical writer vs multi-host teams.* One writer per ledger is enforced by compare-and-swap on one authoritative ref (§15.3).
- *Append-only audit vs confidentiality.* Prevention makes sensitive ledger content structurally unlikely. When confidentiality and append-only continuity truly conflict, a human-gated breach protocol lets confidentiality win and states which audit guarantees yield (§15.5).

Three residual limitations are real but not contradictions:

- Semantic dependencies an agent uses without the machinery observing them cannot be captured by any read-set scheme (§8.4).
- Circular reasoning stated only in prose, without declared relations, can be found only by semantic review (§6.2).
- No architecture can infer the existence of a state whose every copy and checkpoint has been destroyed. SSDS therefore asserts currentness only for durably witnessed state, under a declared witness model (§15.4).

The design bounds and discloses each; none weakens a stated invariant. No Serious Challenge is raised.

## 2. Reconstructed invariants

Source tags: **[6.6]** accepted-current SSDP doctrine; **[P8]** consolidated Protocol 8 proposal (reviewed under 6.1, never accepted-current); **[S8]** SSDS 8 objective from stakeholder/task authority; **[P7?]** prospective Protocol 7 input, not final. Tags show where a requirement comes from; they do not make P8 or P7? items accepted authority.

### 2.1 Semantic

- **S1** D1-D4 semantic authority; one current owner per material normative claim; current ownership acyclic; D1-D4 is a layered DAG, not a waterfall; a higher abstraction never depends on a lower concretization. Mutual *definition* is legitimate only through an explicit simultaneous-definition declaration. A definition, a definitional dependency or a graph condensation never warrants a claim. Circular warrant, authority, evidence, provenance or lineage is invalid. [6.6]
- **S2** Concretization fidelity and abstraction adequacy are distinct; Serious Challenge stops counterfeit closure; a risk override leaves dependents visibly provisional. [6.6]
- **S3** Authority mutation: proposal -> independent falsification where required -> required human ratification -> acceptance -> bounded impact -> reconcretization. Repository presence promotes nothing. A clarification that narrows admissible interpretation is a semantic mutation unless established representation-only. [6.6]
- **S4** Evidence: specification -> realization -> observation -> assessment; observations immutable, assessments superseding; target vs execution dependency; stale passing evidence never confirms, stale failing evidence never refutes; binding health tracked separately from historical existence. [6.6]
- **S5** Absence of a relation establishes independence only inside a scope explicitly reviewed complete for that relation family. [6.6]
- **S6** Specialized substantive inference requires the exact canonical meaning; definitions establish no truth, existence or adequacy; conflicting simultaneous meanings are adjudicated by their owner, never by order or recency. [6.6]
- **S7** Version-bound interpretation; no retroactive reinterpretation; no self-adoption; capability, not wording, is the compatibility oracle. [6.6]
- **S8** PEM is non-authoritative project learning; HAS is task-local. [6.6]
- **S9** A machine-control vocabulary never converts a semantic judgment into a deterministic fact; agent PASS is a recommendation. [6.6][P8]
- **S10** Acceptance attaches to an exact semantic subject, in one tenure, at an exact scope and revision. Content identity, scope identity, subject role and tenure, lineage, dependency coverage, semantic equivalence and acceptance are distinct facts; no mechanism infers a later one from an earlier one. [6.6, derived from S1, S3, S6]
- **S11** Effective governance is admitted, never observed. Repository presence changes no ruleset, structural role, membership, scope, kind or coverage boundary, and promotes no acceptance; declarations found in content are proposals until admitted. An acceptance belongs to one subject tenure and never revives once that tenure ends; restoring old bytes or old declarations restores no validity. [6.6 workflow: repository presence promotes nothing; 6.6 evidence: restoration does not restore validity; derived from S3, S10]

### 2.2 Control

- **C1** Exactly one serialization point for canonical state changes per governed ledger. [P8]
- **C2** Same canonical inputs and rule version give exactly one derived state. [P8]
- **C3** Nondeterministic facts (time, filesystem, Git remote, resources, model output, human judgment) enter only as recorded typed records. [P8]
- **C4** External effects follow intent -> idempotent/reconcilable effect -> observed outcome; ambiguity is reconciled before retry. [P8]
- **C5** Unknown required semantics fail closed; unknown optional fields follow the declared compatibility contract. [P8]
- **C6** A disagreement between semantic content and its control representation is an integrity defect that blocks dependent transitions. [P8]
- **C7** Control data is the minimum needed to select, validate, serialize, replay or audit a transition. [P8]
- **C8** C2's derivation is well-founded: every predicate has one value for every admitted input, with no self-supporting acceptance and no negation through recursion. [6.6 S1 + P8 C2]

### 2.3 Concurrency and isolation

- **K1** A result is admitted only if everything it relied on is still current, or it is revalidated. [P8][S8]
- **K2** No two mutating executions share one working tree. [P8]
- **K3** A clean textual merge is not semantic orthogonality. [S8]
- **K4** Correctness never depends on predictions being complete; predictions may only reduce wasted work. [derived here]

### 2.4 Provenance and replay

- **P1** Every canonical change records what, who, against which basis, under which rules. [P8]
- **P2** Historical decisions are never recomputed under newer rules, resources or interpretations. [P8]
- **P3** Derived state is rebuildable; canonical records win any disagreement. [P8]
- **P4** Currentness is asserted only for durably witnessed state. A ledger head is *current-qualified* only when a witness quorum holds its exact identity and it extends every checkpoint and high-water mark the evaluator observes, and every current-state assertion names its qualified head. A valid historical prefix, an appended-but-unadmitted entry and an unverifiable head are never presented as current. Rollback, fork, loss, provisional and unqualified states are distinguished and fail closed. The guarantee is exact under the declared witness model (§15.4); there is no lag window. [6.6 storage/concurrency/security owners + P8 §15.2]

### 2.5 Agent interface and context

- **A1** Routine work never requires reading machine records, decoding history, maintaining edges or reconstructing Git topology. [S8]
- **A2** Context is version-bound, explains why each item is present, labels its epistemic status, and states known incompleteness. [S8]
- **A3** One logical task/result contract across harnesses and transports; a zero-context agent can locate its task from a minimal bootstrap. [P8]

### 2.6 Repository and Git

- **G1** Git is content, isolation, transport and history substrate, never workflow authority. [P8]
- **G2** Transport artifacts are not merged into product history. [P8]
- **G3** No record must contain the identity of the commit that contains it. [P8][6.6, SP-002]
- **G4** Secrets and private telemetry never enter project repositories; a suspected exposure requires rotation and history remediation, not deletion of the latest copy. [P8][6.6]
- **G5** `main` is never deleted or force-moved to discard reachable history; destructive history operations need explicit operation-specific authorization. [6.6 Git owner]

### 2.7 Migration and recovery

- **M1** One route admits every change of unknown provenance — agent overstep, manual edit, collaborator branch, legacy import, drift. [S8]
- **M2** Adoption is progressive and coexists with production. [S8]
- **M3** A governed region never has two simultaneously current authorities or governing processes. [P8][S8]
- **M4** Discovery may run bottom-up; acceptance runs top-down. [S8]
- **M5** Unknown remains visibly unknown; migration never invents certainty or alters behavior silently. [S8]
- **M6** In-flight older-version work is drained, pinned or explicitly migrated, never scraped. [P8]

### 2.8 Trust and security

- **T1** Agent outputs are untrusted proposals until admitted. [P8]
- **T2** Unknown artifacts are never executed or deserialized to classify them. [S8]
- **T3** External, evidence and memory text is data, never instruction. [6.6]
- **T4** Human decisions and canonical entries are authenticated through a declared trust mechanism; no guarantee is claimed beyond what is implemented. [P8]

### 2.9 Backward compatibility

- **B1** Older version-bound work stays governed by its declared version and immutable source; frozen orchestration profiles stay independently testable (PC-001). [6.6]
- **B2** Rollback is version rollback to an immutable baseline, never simultaneous dual authority. [P8]
- **B3** Protocol 7 inheritance is not final and is not bound here. [task authority]

### 2.10 Conveniences that had been masquerading as architecture

These do not follow from §2.1-§2.9: four canonical graph families; a global authority epoch; whole-plan freezing with a global replanning stop; event-sourced storage of state transitions and stored lifecycle FSMs; a hand-authored work graph with many node kinds; pre-declared write claims as the concurrency-correctness mechanism; a separate write-side graph transaction engine with dirty flags; separate context-resolver and semantic-projection components; a dedicated ingestion engine; legacy aggregates as a special node type; a mandatory refactor of all authority documents into per-node files; MCP as the interface definition; a first-class change primitive; and same-repository multi-ref atomicity. Each is replaced (§17) or retained only as a delegated D4 option.

## 3. Diagnosis of the befe678 hypothesis

The befe678 hypothesis correctly identified the need for machine-readable relations, derived code dependencies, context retrieval, isolation, reconciliation and progressive migration. Its weaknesses are structural:

1. **Synchronization burden by construction.** Four canonical graph families with independent lifecycles share identities and cross-family edges (EVIDENCES, CONCRETIZES from code, work claims over authority). Keeping them consistent required a GraphTransaction, a candidate overlay, GraphDelta and dirty-flag machinery. The decomposition created that machinery; the problem did not need it.
2. **Global coupling where the problem is local.** AuthorityEpoch totally orders independent authority changes, so unrelated acceptances advance the epoch every task is bound to. Whole-plan PlanRevision plus a conservative stop on new mutating tasks during replanning turns a local amendment into a project-wide barrier.
3. **Parallel staleness systems.** Staleness of tasks (epoch/plan binding), context (ContextBundle), evidence (EvidenceGraph status) and graphs (DIRTY) were separate mechanisms. All four answered one question: *did anything this conclusion relied on change?*
4. **Stored state that is really derived.** Execution/outcome/validity/authority/evidence FSMs were stored and reduced from events, although almost all of them are functions of content plus recorded judgments.
5. **Correctness resting on predictions.** WorkClaims declared before execution were the parallelism-safety mechanism; they are necessarily incomplete for semantic conflicts across disjoint files, generated outputs and dynamic dependencies.
6. **Fragile canonical history.** Canonical history lived only in a private local SQLite store; loss of that store with intact repositories lost all accepted decisions, and clone/fork/move had no history path.
7. **Interface leakage.** Agents were asked to propose PlanPatch node/edge operations, maintain WorkClaims, call `change.reconcile`, and choose among seventeen operations.
8. **Migration as a special subsystem.** LegacyAggregate, an ingestion engine with four modes, and a separate repository-explainability rule duplicated what one coverage partition with adaptive granularity provides.
9. **Lossless-representation defect.** It declared supersession of the consolidated Protocol 8 plan while omitting material inherited guarantees (semantic/control projection rule, forward compatibility, transport-artifact and self-reference rules, bootstrap locator, human-gate/risk-override propagation, cutover quiescence, pre-cutover baseline identities, Protocol 7 inputs, versioning preservation, most failure qualifications).

Two befe678 capabilities were sound and are reinstated after later revisions lost them: *structural split into sub-aggregates requires no false semantic claims* (lost at f9d9de8; §12.2), and *the authority order is a DAG after explicit condensation of legitimate simultaneous definitions, while circular warrant stays invalid* (blurred at 441cf5c; §6.2).

## 4. Alternatives considered

| Candidate | Core idea | Verdict |
|---|---|---|
| **H0** befe678 | Four canonical graphs, event-sourced reducer, epochs, frozen plan revisions, graph transactions, legacy aggregates | Rejected as a whole for §3. Retained capabilities are mapped in §18.2. |
| **H1** verified incremental computation | Content-addressed units; an immutable ledger of judgments and observations; everything else derived by versioned rules; staleness = basis change (build-system "early cutoff") | **Selected core.** One mechanism answers staleness, readiness, impact and context; locality is natural. |
| **H2** logic knowledge base | All facts, authored and derived, in a Datalog/relational store with an event log of assertions/retractions | Hybridized. Kept: derivation is stratified, with a monotone least-fixed-point support tier (§6.6). Rejected: a general rule language as architecture. Rules are parameters of fixed predicate templates. |
| **H3** Git-only documents-as-state | Plans, judgments and statuses as repository files; CI as gate | Rejected as primary: anyone can push a PASS file, concurrent status edits conflict, and status-in-documents is exactly what SSDS 8 removes. Kept: Git as content store, isolation, replication and transport, including the ledger's object chain (§15). |
| **H4** hosted service | Central database plus durable-workflow engine | Rejected: operational cost, not local or lightweight, polling-first violated, no benefit for the single-team scale that must work first. |

Comparison of the serious candidates (H0, H1+H2+H3 hybrid):

| Criterion | H0 | Selected hybrid |
|---|---|---|
| Authority integrity | relations in separate graph store can drift from content | authored relations live inside the content they belong to; drift impossible by construction |
| Determinism | reducer over events | stratified pure derivation over ledger + content; fewer stored states |
| Duplication | four graphs + control state + caches | one content store, one ledger, derived index |
| Implementation complexity | high (sync, overlays, dirty tracking) | moderate (derivation engine with memoization) |
| Agent burden | many operations, plan/claim maintenance | six logical operations; no bookkeeping |
| Recovery | local store loss is fatal | ledger replicated as Git objects; currentness only for quorum-witnessed heads |
| Concurrency | claim-based, incomplete | optimistic validation at admission; claims advisory |
| Migration | separate subsystem | refinement of coverage; acceptance moves only by judgment |
| Evolution | reducer versioning | ruleset versioning; admissions never re-derived |
| Lightweight/local | yes | yes |
| Harness independence | MCP-shaped | transport-neutral logical interface |
| Scientific fit | generic | basis carries regime, parameter instance, seed, backend, precision (§10) |

## 5. Architecture overview

```text
                         agents / humans
                               |
              Interface  (open · ask · read · report · submit · decide)
                 |                                   |
          (queries, read-only)              (typed admission requests)
                 v                                   v
         Derivation Engine  <-------------------  Admission  ---- sole ledger writer -----+
   S0 observed content · effective structure ·  validate · append (single-ref CAS) ·     |
   S1 challenges · S2 support ·                 anchor (witness quorum) · publish        |
   S3 obligations, readiness, impact, context   (reconciled effects)                     v
          |            |                               Ledger Store: Git object chain on one authoritative
   Content Model    Analyzers                          ref; verification; current-head qualification
   observed declarations  derived relations             (quorum checkpoints, high-water marks)
   authored relations                                   Integration ref (product branch): published projection
          \            /                                                                 ^
           Git content store  <-- workspaces (isolated) -- Dispatcher                    |
                                                       scheduling · execution effects · harness adapters
                                                       (operator state: private, local; never canonical)
```

Four primitives:

1. **Unit** — a governed region of repository content with stable identity and a content-addressed revision; leaf units partition content; composite units group leaves into one acceptance **subject**; structure is effective only as admitted (§6.1).
2. **Relation** — a typed, directed fact between units, classed as authored, derived or proposed, whose type carries a closed semantic role and cycle class (§6.2).
3. **Record** — an immutable ledger entry: a judgment, an observation, an admission or a lifecycle record (§6.3).
4. **Basis** — the exact typed set of unit revisions and records a record relied on; currency is computed from it (§6.4).

A **change** is not a primitive. It is a typed Admission request (§6.8) whose identity and audit trail live in the admission record. Everything else — lifecycle states, validity, obligations, readiness, staleness, impact sets, context bundles, graph views, diffs, dashboards — is **derived**.

## 6. Primitives and derivation

### 6.1 Unit, scope and subject

A **unit** `u` has: a stable logical identity; a kind and owning domain (D1, D2, D3, D4, plan, evidence specification, generated, external, unclassified); a **scope** (the repository regions it covers: paths, or anchored spans within files); a declaration source; and a role: **leaf** or **composite**.

- **Leaves partition content.** For every admitted tree, leaf scopes partition all governed content. That is every tracked path outside declared ignore patterns, and every span of a sectioned file; each belongs to exactly one leaf. Genesis may declare a single catch-all `UNCLASSIFIED` leaf. Partition validity is checked at every admission.
- **Subjects.** A **composite** declares its members (leaves or nested composites); its scope is the union of its members' scopes. Composites form a laminar family: any two are nested or disjoint. Every unit, leaf or composite, is either a **subject** (the default) or a declared **part** of an enclosing composite. `subj(u)` is `u` if `u` is a subject, else the nearest enclosing composite that is a subject; laminarity makes it unique. It is a function of *effective* structural declarations only (below). A subject may contain nested subjects (a carve-out, §12.2); its scope, and so its revision, still covers their content. A subject has one acceptance; its parts have none of their own.
- **Composite subjects are not simultaneous definitions.** A composite subject groups content for one acceptance: a refinement parent whose holistic acceptance has not been divided (§12.2), a legacy document, a carve-out container. It licenses nothing about relations. Mutual definition is licensed only by a **simultaneous-definition group** declaration (§6.2), which is semantic content of one enclosing subject. Revision 2 used one construct for both, and that conflation admitted circular warrant inside a subject (441cf5c Blocker A).
- **Declaration.** Structural declarations live only in the repository-owned **unit manifest** (path patterns, heading paths, symbol sets, kinds and domains, roles, memberships, identity and rename lineage, the governed-content boundary). Inline **anchors** may only delimit leaf spans inside a manifest-declared unit, and they inherit its kind, domain and enclosing composite. An anchor never declares role, membership, kind, domain or scope. Semantic declarations live inline in content or in the semantic part of a manifest entry. External declaration is mandatory for immutable or version-pinned artifacts, which are never rewritten to acquire anchors. Confining governance-affecting declarations to the manifest keeps the observed/effective distinction on one small, identifiable surface.
- **Revision.** `rev(u, T)` = hash(content identity of `scope(u)` in tree `T`, semantic declarations within `scope(u)`). **Content identity** hashes the scope's bytes in declared order after rule-defined conservative normalizations; pure structural boundary markers carry no relation payload and are normalized out. **Semantic declarations** are the authored relations, defined-object declarations, simultaneous-definition declarations and joint-invariant declarations of the unit and of every unit inside its scope. **Structural declarations** are excluded from `rev`, but they determine scope, `subj` and tenure. They are therefore exactly the declarations that could reroute governance without changing any revision, so they take effect only as admitted (below). Revisions are computed from Git content; no separate hash graph is stored. Granularity is adaptive: a file, a section, a symbol set, or an entire legacy subtree.
- **Scope identity.** `scope_id(u)` identifies the set of regions independently of their bytes. Changing what a subject covers is a scope change, not a revision change.
- **Observed and effective structure.** `decl(T)` is the set of structural declarations parsed from tree `T`, keyed by declaration (unit identity plus field). The **effective structure** `Σ_n` is the set of structural declarations in force at ledger position `n`. It is a fold over admitted entries: genesis admits `Σ_0`, and an ordinary or intake admission changes `Σ` exactly by the structural changes it authored or explicitly adopted (§6.8 step 4). **Absorption never changes `Σ`.** `Σ_n` is derived from the ledger and the trees its records name; it is not a second stored copy.
  - *Resolution.* Effective scopes are resolved against the bytes of the observed tree `T_n` (§6.6 S0). A region that no longer resolves has content identity `ABSENT`. Governed observed content outside every effective leaf belongs to the reserved **uncovered region**, which has status `UNCLASSIFIED`.
  - *Quarantine.* `Q_n = { k : decl(T_n)[k] ≠ Σ_n[k] }` holds the **quarantined structural deltas**: what the repository declares but governance has not admitted.
  - *Governance-affecting deltas.* A quarantined delta is **governance-affecting** iff adopting it would change, for some unit, its identity, kind, domain, role or enclosing composite; for some subject, its `scope_id` or the byte regions it covers; or the governed-content boundary. Otherwise it is **governance-neutral**: a re-partition of leaves inside one subject's unchanged regions into parts of that subject with its kind and domain.
  - *Affected subjects.* `aff(Q_n)` is computed by comparing `Σ_n` with `Σ_n` overridden by `decl(T_n)`. It contains every effective subject that is, or contains, a unit named by a governance-affecting quarantined delta, plus every effective subject whose signature or regions such a delta would change. A foreign declaration that would carve a part out of `P` as a nested subject therefore affects `P`, even though `P`'s own regions would not change.
- **Subject tenure.** A subject's **governance signature** is `(role = subject, scope_id, kind/domain, governance mode)`. Its **tenure** `τ(s)` is the first ledger position of the current uninterrupted run over which `s` has been an effective subject with an unchanged signature.
  - A tenure ends when `s` is demoted to a part, its `scope_id` changes, its kind or domain changes, or its governance mode changes. A later restoration starts a new tenure.
  - Acceptance belongs to a tenure (§6.6 `ACC`). Challenges, revocations and supersessions target exact triples and records, and they survive tenure changes.
  - Byte-preserving refinement of `s`, and carve-out promotion of one of its parts, leave `s`'s tenure unchanged.
- **Single definer.** A unit may declare that it defines a named semantic object. Two current units defining the same object is an integrity conflict that blocks dependent use until the owner adjudicates (S6).
- **Status lives in the ledger.** Acceptance, governance mode, reconstruction status, lifecycle and effective structure are derived from records (§6.6), never enacted by editable fields in unit content.

The facts that S10 keeps distinct, and what establishes each:

| Fact | Established by | Never implies |
|---|---|---|
| content identity | hashing (mechanical) | any of the facts below |
| scope identity | effective unit declarations | that bytes or meaning are unchanged |
| subject role and tenure | effective structure, changed only by admission (S11) | acceptance; a past tenure's acceptance; anything from a repository declaration alone |
| lineage / provenance | refinement and rename declarations, ledger history | acceptance or equivalence |
| simultaneous definition | an SDG declaration, accepted with its subject's revision (§6.2) | warrant of any member claim |
| dependency and completeness coverage | relations; `COMPLETENESS` judgments; analyzer completeness declarations | equivalence or acceptance; widening only adds context |
| semantic-subject equivalence | `EQUIVALENCE` judgment by a qualified actor (byte identity and rule normalizations only mechanically) | acceptance of any new subject |
| acceptance | acceptance judgment on exact `(subject, scope_id, rev)` in the subject's current tenure under the owning domain's contract | anything about another subject, scope or tenure |

Units rather than files or Git blobs give locality: per-file identity would make any edit to a long authority document invalidate every conclusion that relied on any part of it. Adaptive granularity keeps the declaration cost proportional to need. Locality of *acceptance* is never cheaper than one semantic judgment (§12.2).

### 6.2 Relation

A **relation** is `(subject, type, object, class, provenance)`.

- **Authored** relations are declared inside the subject unit's scope (or its manifest declaration) and are therefore part of every enclosing subject's revision. They take effect when that subject's revision is accepted, and change only by changing content. Semantic relations and their meaning cannot drift apart, and a human editing a document edits its relations in the same act.
- **Derived** relations are computed by a versioned analyzer from content (imports, calls, build edges, generated-from, test-to-code). They are never edited and never stored as canonical; they are cached under their derivation key.
- **Proposed** relations are records (from search, analyzers with semantic uncertainty, or agents) awaiting acceptance. A proposal is accepted only by an admitted content change to the subject's authored relations.
- **Record-level relations** (challenge targets, adjudication, supersession of assessments) are properties of records, not edits to their targets: a challenger never owns the challenged unit.

Stored direction is subject -> prerequisite, following the evidence and definition owners; reverse traversal is impact analysis, not a second relation. A generic "related-to" supports no closure (S5).

**Semantic roles and cycle classes.** The relation vocabulary is part of the ruleset in force (`ρ_n`, §6.6 S0). It is closed and versioned. Every type carries mandatory attributes: direction, **semantic role**, **cycle class**, permitted classes (authored or derived), layer constraint, and completeness eligibility. Cycle legality is decided by the cycle class, never by common subject identity.

| Role | Representative types | Cycle class | What the relation can do |
|---|---|---|---|
| `DEFINITIONAL` | `USES_DEFINITION` | `SIMULTANEOUS` | fixes meaning; never warrants (6.6: a dependency graph does not warrant its endpoints) |
| `WARRANT` | `DERIVED_FROM`, `ASSUMES`, `DEPENDS_ON` | `ACYCLIC` | carries claim support or prerequisite order |
| `GOVERNING` | `CONCRETIZES`, `CONSTRAINED_BY` | `ACYCLIC`, plus layer direction | carries authority |
| `EVIDENTIAL` | `EVIDENCES` (evidence specification -> claim), `EXECUTION_DEPENDS_ON` | `ACYCLIC` | binds evidence to target and execution |
| `PROVENANCE` | `GENERATED_FROM` | `ACYCLIC` | regeneration order |
| `LINEAGE` | `SUPERSEDES`, `REPLACES` | `ACYCLIC` (6.6: lineage is acyclic) | replacement history |
| `STRUCTURAL` | analyzer-derived imports, calls, build edges, test-to-code | `NEUTRAL` | context, impact and widening only |

These constraints on the vocabulary are checked when a ruleset is adopted:

- `SIMULTANEOUS` is permitted only for `DEFINITIONAL` types.
- `NEUTRAL` is permitted only for derived `STRUCTURAL` types; no authored type is `NEUTRAL`.
- No rule may name a `NEUTRAL` type as a validity-mode or warrant prerequisite. Code-level recursion (mutually importing modules, recursive calls) is therefore legal and inert: it cannot carry warrant.
- A type with an attribute missing cannot be adopted.

A ruleset adoption that removes, renames or reclassifies a type declares, for existing uses in content, `READ` (alias to a defined type), `MIGRATE` (ordinary content changes through Admission) or `REJECT`. The adoption gate is shown the derived impact: the subjects that would become ill-formed. Historical views keep the vocabulary in force at their position. Relations in `LEGACY(p)` content that SSDS extracted heuristically are proposed, not authored, so vocabulary evolution never invalidates a legacy subject. A type absent from `ρ_n` has unknown required semantics (C5). Admission rejects any authored relation of that type, inside or outside a cycle. In absorbed content, such a relation makes its subject ill-formed (below). A future type therefore fails closed until a ruleset adoption defines its role and cycle class.

**Simultaneous-definition group (SDG).** An SDG is a *semantic* declaration, made inline or in the semantic part of a manifest entry, naming a set of units whose meanings are defined together. Being semantic, it is part of the enclosing subject's revision: adding, removing or changing an SDG is a semantic change that needs acceptance, so simultaneity is never asserted by structure or presence. Rules:

- all members of an SDG have one common `subj`, the declaration itself lies inside that subject's scope, and an SDG never contains a subject;
- SDGs are laminar;
- no relation is a self-relation: recursion inside one object's definition (a recurrence, a fixed-point equation) is that unit's own content.

An SDG is a declaration, not a unit and not a primitive.

**Cycle legality.** Let `E` be every authored relation and every derived relation whose cycle class is not `NEUTRAL`, over effective units in the observed tree. `E` is legal iff **every cycle of `E` lies inside the member set of one SDG and uses only `SIMULTANEOUS` edges**. Equivalently, every strongly connected component with more than one unit is contained in one SDG and contains no edge of another class. Consequences:

- a `DERIVED_FROM` or `DEPENDS_ON` cycle is illegal, even inside one subject or one SDG;
- a mixed cycle (definitional plus warrant) is illegal;
- a cycle spanning two sibling SDGs is illegal unless an enclosing SDG is declared;
- nested SDGs are permitted.

Contracting each SDG yields the acyclic order used for layer checks, ordering and impact. **The contraction is a representation, not a warrant.** The contracted node has no warrant of its own. Definitional edges fix meaning only. Every claim inside an SDG still needs `ACYCLIC`-class warrant, none of which can lie on a cycle, and its subject's acceptance.

Structural rules checked at admission (§6.8 step 4) on the merged tree:

- referenced units exist;
- every relation type is known in `ρ_n`;
- no authored dependency runs from a higher abstraction to a lower concretization;
- cycle legality and the SDG rules hold;
- plan items do not depend on lower-layer work in a way that inverts the authority order.

The same rules define the S0 predicate `well_formed(s)` (§6.6). `well_formed(s)` is false when any unit of `s` lies on an illegal cycle, carries a relation of unknown type or inverted layer direction, belongs to a malformed SDG, or conflicts with the single-definer rule. A violation that reaches the tree without Admission — absorbed content, or a ruleset that reclassifies a type — therefore invalidates every involved subject in S2, not only an S3 report.

Machinery checks *declared* relations. Circular reasoning stated only in prose, with no declared relation, is a semantic defect that acceptance review and Challenge must find (residual risk, §8.4).

**Completeness is a judgment.** `COMPLETENESS(X, R)` asserts, for a scope `X` (a set of units) and a relation class `R`: *every `R`-prerequisite of a unit in `X` that lies outside `X` is declared* (boundary completeness). For a singleton scope `{u}` this is the outgoing completeness of `u`, typically attested during `u`'s acceptance review. Its mechanical minimum basis is content-mode entries on every unit in `X` plus the identity of `X`'s membership, so adding, removing or editing a member makes it non-current. An analyzer may supply boundary completeness only for derived classes, only within the scope and constructs its version declares complete, and never where it detected an incompleteness marker (reflection, plugins, dynamic registration, generated code, runtime configuration, external consumers). Completeness never transfers through refinement or scope change.

### 6.3 Record and ledger

The **ledger** is the single canonical store of everything that cannot be derived from content. It is append-only, totally ordered, authenticated (§15.4), and serialized in a canonical versioned **closed schema** (§15.5). Every record carries: identity, kind, actor and actor class, subject, basis, outcome, schema and ruleset version, provenance, and content-identity references to any substantive report artifact. Records contain no free text, essays, equations, patches or raw logs (C7).

| Record kind | Produced by | Examples |
|---|---|---|
| **Judgment** (support tier) | agent, human, or semantic-role tool | acceptance; conformance; equivalence; completeness; evidence assessment; plan acceptance; intake classification and disposition, including adoption of a quarantined structural delta; legacy or external acceptance import; reconstruction proposal |
| **Judgment** (challenge tier) | qualified actors per policy | finding or challenge (blocking or not); Serious Challenge; adjudication; withdrawal; risk override |
| **Observation** | machinery | evidence realization from a trusted runner (§10); publication outcome; live-ref movement and other foreign-change detection; consultation of an external ledger's qualified head (§11.4); analyzer output recorded because the analyzer is nondeterministic or expensive; artifact availability |
| **Admission** | Admission only | accept or reject of an admission request with reason codes, validated basis, ruleset version, request identity, base commit, resulting admitted (merged) commit and adopted structural deltas; absorption of an observed tree |
| **Lifecycle** | Admission, human-gated where required | genesis (project identity, ledger location, authoritative replica, trust roots, witness set and quorums, initial effective structure); ruleset adoption; schema migration; governance-mode transition; project fork; replica redesignation; witness-set redesignation; ledger loss; ledger fork resolution; confidentiality-incident lineage migration and old-lineage retirement; redaction notice |

Every record enters through Admission. A ledger entry is *provisional* when appended and *admitted* once a witness quorum holds its head (§15.3); a judgment is *recorded* when its entry is admitted; whether it is *current* is derived (§6.6). Rejections are recorded too, so provenance includes what was refused and why.

The ledger holds only what derivation consumes or audit requires. Purely operational facts — task issue, reservations, leases, worktree creation, agent launch, retries — live in the Dispatcher's durable operator journal under the same intent -> effect -> observed-outcome discipline (C4). They influence scheduling, never derived workflow state. Execution provenance that matters for audit (route, harness, model, attempt) travels inside submitted records.

### 6.4 Basis

A **basis entry** is `(mode, target, consumption class)`. The mode is fixed by the rule for the record's kind when the record is admitted, and it is never inferred at evaluation.

| Mode | Target | Satisfied when (§6.6) | Used for |
|---|---|---|---|
| `content` | unit revision `(u, r)` | `cur(u) = r`, or an equivalence path from `r` to `cur(u)` for the entry's consumption class | everything the actor saw: the judged revision, context supplied or read, change base, content behind evidence |
| `validity` | unit revision `(u, r)` | the content condition holds and `subj(u)` is valid | **direct** governing or warrant prerequisites only, as the rule names them by relation role; never a `NEUTRAL` relation (§6.2) |
| `record` | an earlier record `x` | `x` is current | premises that are themselves judgments: completeness, evidence realization/assessment, plan acceptance |
| `identity` | a record, or `(subject, scope_id, rev)` | always (immutable fact) | targets of challenge-tier records and supersession; equivalence endpoints |

Transitive governing authority is reached through the validity of direct prerequisites, not listed separately; this is what makes early cutoff predictable (§6.7). A unit the actor actually saw also gets a `content` entry, so backdating reaches a record only through units it did not see. A rule may declare consumption classes that let an `EQUIVALENCE` judgment cover a `content` entry; the default class is exact.

The basis of a record is the union of:

- the **mechanical minimum** computed by the rule for its kind: direct governing subjects (validity), the judged revision and supplied context (content), the dependency closure over the relation classes the rule requires (§6.5), the completeness judgments that closure used (record), and the change base;
- **recorded reads** made through the interface, plus harness-observed reads where an adapter can observe them;
- **declared reliance** the actor adds at submission.

An actor can add to the mechanical minimum, never remove from it.

### 6.5 Conservative widening

Widening solves dependency uncertainty only. It never establishes equivalence, completeness or acceptance, and a widened basis never makes a part valid (§12.2).

**Enclosing-scope chain.** For a unit `u`, `chain(u) = X_0 ⊂ X_1 ⊂ ... ⊂ X_m`, built deterministically:

```text
X_0 = {u}
then each effective composite containing u, smallest first   (laminar, so nested)
then the directory containing u's declaration source, then each ancestor directory
X_m = every effective unit in the governed tree, plus the uncovered region
each step: X_{i+1} = X_i ∪ units(next scope); skip steps that add nothing
```

The chain is built from effective structure `Σ_n`, never from quarantined declarations. Uncovered observed content has no judged completeness, so it is reachable only through the whole-tree fallback, where the brief lists it as `UNCLASSIFIED`.

**Closure algorithm.** For seed set `S` and relation class `R` (the rule's class; a union class needs completeness covering each member class):

```text
closure(S, R):
  reached := S; queue := S
  while queue not empty:
    u := pop(queue)                                     -- order irrelevant to the result
    for v in declared R-prerequisites(u) (authored + derived): enqueue v if new
    if not exists X_i in chain(u) with current COMPLETENESS(X_i, R) for every member class:
        W := X_m                                        -- whole governed tree
    else:
        W := the smallest such X_i                      -- undeclared prerequisites lie inside it
    for v in W: enqueue v if new
  return reached                                        -- a least fixed point; finite
```

The result is the smallest set containing `S` that is closed under declared prerequisites and the widening rule, so it is independent of traversal order. Exact closure (no widening beyond `{u}`) needs a current singleton completeness judgment on every reached unit. **Fallback** when no judgment exists anywhere in `u`'s chain: the whole governed tree. The brief marks it `UNBOUNDED` and lists declared external units; undeclared external dependencies cannot be enumerated and are stated as such. *Missing dependency knowledge never proves independence.*

### 6.6 Derivation

The **Derivation Engine** computes, as a pure function,

```text
derive(L_n, content of trees referenced in L_n) -> exactly one derived state D_n
```

where `L_n` is the ledger prefix through position `n` (its observations included). The ruleset and the effective structure are read from `L_n` (S0 below), not supplied from outside. Derivation is defined for every authenticated prefix. *Which* prefix may be presented as current is decided outside derivation by currentness qualification (§15.4), so witness reads never enter `D_n`.

Derivation has four strata. A stratum reads only lower strata. Within S1 and S2 recursion is permitted only in the forms proved unique below. The SSDS system version fixes the derivation semantics. Project policy only parameterizes fixed predicate templates: judgment kinds, actor qualifications, mechanical-minimum composition, consumption classes, passing outcomes, required gates, and obligation triggers. A ruleset whose parameters would make a lower stratum read a higher one is rejected at adoption. There is no general rule language.

**S0 — observed content, effective structure and ledger syntax.**

- *Ruleset in force* `ρ_n`, including the relation vocabulary of §6.2: the latest admitted `RULESET_ADOPTION` record at or before `n`, naming an exact system ruleset version and an exact policy content hash.
- *Observed tree* `T_n`: named by the latest admission or absorption record.
- *Effective structure* `Σ_n`: the fold of admitted structural changes (§6.1, §6.8 step 4). From it come the units, leaves, composites, `scope_id`, `subj`, kind/domain, coverage and tenure `τ(s)`.
- *Quarantine* `Q_n` and *affected subjects* `aff(Q_n)` (§6.1).
- *Revisions:* `rev(u, T)` and `cur(u) = rev(u, T_n)`, over effective scopes resolved in the observed bytes.
- *Relations and well-formedness:* authored and derived relations read from `T_n`; `well_formed(s)` (§6.2).
- *Record syntax:* record targets, and `superseded(x)` ⇔ some admitted record names `x` in its `supersedes` field (authorization was checked at admission).

Policy and structure follow one rule: **content proposes; admitted records enact.** The project policy unit is ordinary content, and an edit to it takes effect only through a human-gated adoption record that Admission validated under the previous ruleset. A structural declaration takes effect only through an admission that authored or adopted it. Derivation never reads a derived acceptance of policy or a derived validity of structure, so S0 depends on nothing above it.

**S1 — challenge tier.** Records of kinds CHALLENGE (with `blocking` flag; Serious Challenge is always blocking), ADJUDICATION (target a challenge; outcome `UPHELD` or `DISMISSED`), WITHDRAWAL (target the raiser's own challenge) and RISK_OVERRIDE (target a challenge; declared continuation scope). A challenge may target a support-tier record, a subject revision `(s, scope_id, r)`, an adjudication or a risk override, never another challenge. Targets carry no tenure, so a challenge or revocation on a triple binds every tenure in which that triple recurs. A challenge raised against a part targets its subject's current revision and records the part as its locus. To contest a challenge, a qualified actor requests adjudication. Every target is strictly earlier in the ledger (Admission step 5).

```text
in_force(y), y ∈ ADJUDICATION ∪ WITHDRAWAL ∪ RISK_OVERRIDE
                 ⇔ ¬∃ c ∈ CHALLENGE : c.target = y ∧ c.blocking ∧ open(c)
open(c)          ⇔ ¬∃ y ∈ ADJUDICATION ∪ WITHDRAWAL : y.target = c ∧ in_force(y)
upheld(c)        ⇔ ∃ a ∈ ADJUDICATION : a.target = c ∧ a.outcome = UPHELD ∧ in_force(a)
overridden(c)    ⇔ open(c) ∧ ∃ o ∈ RISK_OVERRIDE : o.target = c ∧ in_force(o)

unresolved blocking challenge on z  ⇔  ∃ c : c.target = z ∧ c.blocking ∧ open(c)

status1(z) = REVOKED      if ∃ c : c.target = z ∧ upheld(c)
             BLOCKED      else if ∃ unresolved blocking c on z with ¬overridden(c)
             PROVISIONAL  else if ∃ unresolved blocking c on z
             CLEAR        otherwise
```

*Uniqueness.* Every right-hand side refers only to records whose position is strictly greater than the record on the left (a resolver is later than what it resolves; a challenge is later than its target). The definitions are therefore a recursion on a finite, strictly increasing chain of positions, evaluated once in decreasing ledger order. Each value is unique even though negation appears; no negative cycle can exist. Non-blocking challenges have no S1 effect; they create S3 obligations. Effects are conservative in both directions. A challenge against a dismissal restores the original block. A challenge against an override or an upholding adjudication suspends it.

**S2 — support tier.** Values in the three-point lattice `F < P < T` (non-current/invalid < provisional < current/valid), with `∧ = min`, `∨ = max`, empty `∨ = F`, empty `∧ = T`. S0 and S1 are constants here.

```text
base(z)  = F if superseded(z) or status1(z) ∈ {REVOKED, BLOCKED};  P if status1(z) = PROVISIONAL;  else T

current(x)  = base(x) ∧ ⋀_{e ∈ basis(x)} sat(e)                         -- x a support-tier record

sat(content (u, r, k))   = T                         if cur(u) = r
                         = ⋁_{paths r = r_0 -> ... -> r_m = cur(u)} ⋀_i current(q_i)
                                                     over EQUIVALENCE judgments q_i on u, class k
sat(validity (u, r, k))  = sat(content (u, r, k)) ∧ valid(subj(u))
sat(record x)            = current(x)
sat(identity z)          = T

ok(s)    = T if well_formed(s) and s ∉ aff(Q_n), else F                 -- S0 constant (§6.1, §6.2)

valid(s) = base((s, scope_id(s), cur(s))) ∧ ok(s)
           ∧ ⋁_{j ∈ ACC(s)} ( current(j)
                              ∧ ⋀_{required kind/actor q of ρ_n for s} ⋁_{j' passing, by q, on the same triple} current(j')
                              ∧ ⋀_{required human gate g} ⋁_{authenticated human judgment h for g} current(h)
                              ∧ ⋀_{required evidence obligation e} ⋁_{admissible assessment a for e at cur(s)} current(a) )
  where ACC(s) = admitted passing acceptance judgments on exactly (s, scope_id(s), cur(s)),
                 admitted at or after τ(s), by actors qualified for them (checked at admission)

valid(part u) is not a variable: every use routes to valid(subj(u))
```

The right-hand sides are built from `min` and `max` over S2 variables and constants, so the system is monotone on a finite lattice and has exactly one **least fixed point**. That fixed point is the S2 state. An ungrounded cycle evaluates to `F`: no acceptance can support itself. For the f9d9de8 review's counterexample (`current(j_a)` ← `valid(b)` ← `current(j_b)` ← `valid(a)` ← `current(j_a)`), the least fixed point is all-`F`, never all-`T`. The configuration is also inadmissible on two independent grounds. Mutual validity reliance between subjects is a support cycle (below). Mutual authored warrant between `a` and `b` is an illegal relation cycle (§6.2) whether or not `a` and `b` share a subject. The two checks are distinct because they guard different graphs: the support graph guards record currentness, and cycle legality guards declared semantic warrant (441cf5c Blocker A).

`ok(s)` and `τ(s)` are how lower-stratum governance constrains S2 without reading S3. A subject touched by an unadmitted governance-affecting declaration, or carrying an illegal relation structure, cannot be valid. An acceptance from an earlier tenure cannot count. Both facts are syntactic functions of the ledger and the observed tree.

Admission maintains the stronger invariant that the **support dependency graph** is acyclic. Its nodes are `valid(s)` and `current(x)`. Its edges come from three sources: each basis entry; each subject to every acceptance, gate and assessment judgment naming it; and the static over-approximation of equivalence coverage, in which `x` depends on every equivalence judgment on `u` reachable from `r` for each `content` entry `(u, r)`. Edges change only when admitted records are added. Absorption adds none. A one-pass topological evaluation therefore computes the least fixed point. A cycle found at derivation can arise only from corrupted input; it still evaluates to `F` and raises an integrity obligation.

**S3 — consequence tier.** Non-monotone functions of S0-S2 that nothing below reads: open obligations (including intake of each quarantined delta), discharge (§7.4), readiness (§7.3), blockers, drift (`cur(s)` differs from `acc(s)`, the latest revision with a passing acceptance judgment, which is a display view only), impact sets for hypothetical changes, context answers, briefs, graph, diff and history views, and integrity findings. Provisional values and risk-override scopes are interpreted here. S3 explains and schedules quarantine and ill-formedness; it never enforces them, because S2 already did.

**Determinism claim.** For every authenticated `(L_n, content)`, S0 is a function, S1 is a well-founded recursion, S2 is the unique least fixed point, and S3 is a function. `D_n` is therefore single-valued and independent of evaluation order, wall clock, live refs, witness reachability, operator state and search indexes (C2, C3, C8). Qualification is in §22.

**Supersession and risk override.** Supersession is purely syntactic (S0). A superseded record never becomes current again, even if its superseder later goes stale. Supersession withdraws a record; it does not reverse its admitted history. A risk override never resolves a challenge. It turns `BLOCKED` into `PROVISIONAL` for the challenged target; `P` then propagates by `min`, and S3 permits provisional discharge only inside the override's declared scope. An upheld challenge on a subject revision revokes that revision permanently. Repair requires a new revision and acceptance, or a successful challenge to the upholding adjudication.

**Analyzers** produce derived relations keyed by `(analyzer identity, version, configuration, input revisions)`. A deterministic analyzer's output is cache. A nondeterministic or expensive analyzer's output is recorded as an observation, so replay uses what was observed. **Caching** is memoization keyed by inputs. There is no dirty state, because nothing is cached without its content key. Incremental derivation must equal from-scratch derivation. **Integrity checks** run on every derivation: effective coverage partition, laminarity, single definer, relation cycle legality and vocabulary, support-graph acyclicity, the observed/effective structure comparison, and ledger authentication. Currentness qualification (§15.4) runs before any derivation is presented as current.

### 6.7 Early cutoff and equivalence

When upstream D2 subject `a` changes, the D3 subject `b` whose acceptance relied on `a` (validity mode) becomes invalid, and D4 judgments relying on `b` become non-current. If a re-review of `b` against the new `a` passes *without changing `b`*, `b` is valid again. Every D4 judgment whose basis named `b`'s unchanged revision, and did not itself see `a`'s text (§6.4), becomes current again with no further work. Staleness propagates exactly as far as meaning moved.

**Equivalence is semantic unless trivial.** Machinery decides equivalence only for byte identity and rule-defined conservative normalizations. It may use derived interface fingerprints only for consumers of derived structure — never for behavioral conformance, evidence or semantic acceptance. Everything else is an `EQUIVALENCE` judgment by a qualified actor, scoped to consumption classes: "editorial only", "representation-preserving split", "does not affect this consumer". An equivalence judgment relates two revisions of one unit. Its `validity` entries must not depend back on a consumer of that unit; Admission's acyclicity check (§6.8 step 5) rejects any that would. It never creates acceptance of a different subject or scope. Where the rule requires independence, the author of a change cannot be the sole qualifier of an equivalence or completeness judgment about that change. A self-declared one is recorded as a proposal and backdates nothing.

This one mechanism replaces epoch binding, plan-revision binding, context staleness, stale-result detection, evidence staleness, dirty-graph tracking and the freeze frontier.

### 6.8 Admission requests and Admission

An **admission request** is the typed result of `submit`. It contains: a request identity (idempotency key), the producing task and obligation(s) it claims, the base admitted position and base commit, candidate commit(s) on isolated refs (or none, for records-only requests such as a review, ratification or challenge of admitted content), any quarantined structural deltas it adopts, and the records it submits. The admission record that accepts or rejects it carries the request identity, the decision, reason codes, the admitted records and the resulting admitted commit. This is the complete identity and audit trail a change needs, so no separate change primitive exists. A repeated request identity returns the recorded decision.

Admission is the **sole writer** of the ledger. Other actors can still move the integration ref: humans pushing to legacy scopes, an external merge button, a force-push, a restore from backup. Such movement carries no admitted status. It is observed and absorbed as a foreign change (§11). An absorption record sets the observed tree `T_n` and changes nothing else. Every touched unit whose content now differs from its accepted revision shows drift. Every structural declaration that differs from effective structure is quarantined. Production is never blocked by this; governance validity is.

Admission validates, in order, and either appends or rejects with recorded reasons:

1. **schema** — records well-formed under the closed schema; bounded secret/sensitive-value checks (§15.5); unknown required semantics fail closed (C5);
2. **reference** — every identity, revision, task, obligation and target exists and matches;
3. **authorization** — actor class qualified for each judgment kind; acceptance judgments only on effective subjects in their current tenure (after the request's own structural changes), never on parts, never on a `REVOKED` triple and never on an ill-formed revision; independence requirements for equivalence/completeness about the request's own change; protected surfaces untouched without their own authority (§15.7);
4. **structure** — on the merged tree `M`, in three parts:
   - *(a) effective-structure delta.* For every declaration key `k`:
     - if `k ∉ Q_n`, then `Σ_{n+1}[k] := decl(M)[k]`: an authored change, or no change;
     - if `k ∈ Q_n` and `decl(M)[k] = Σ_n[k]`, the request *realigns* the repository with governance and `Σ` is unchanged;
     - if `k ∈ Q_n` and the request carries an intake disposition adopting `k`, then `Σ_{n+1}[k] := decl(M)[k]`, validated exactly as if authored;
     - if `k ∈ Q_n` and `decl(M)[k] = decl(T_n)[k]`, the quarantine is carried unchanged;
     - any other value routes the request to revalidation.

     Authored and adopted changes are validated together: leaf coverage partition, laminar composites, scope conservation for refinement, promotion only with an acceptance in the same request (§12.2), no membership change that mixes governance modes without the mode-transition record (§12.1), SDG members never separated, and no change of a unit's kind or owning domain without a judgment by an actor qualified for its *current* domain (a unit never leaves its owner's authority by redeclaration). Admission never creates new quarantine, and repository presence never enters `Σ` except through an adopting disposition.
   - *(b) challenge freeze.* No change to the signature, scope, regions or membership of any subject is admitted, whether that subject would lose or gain units, while its current revision carries an unresolved blocking challenge (overridden or not) or is `REVOKED`. A challenge therefore cannot be escaped by re-scoping unchanged content at the source subject or at the destination subject.
   - *(c) semantic structure.* Known relation types of `ρ_n`, relation direction and layer order, cycle legality and the SDG rules (§6.2), and single definer;
5. **dependency well-formedness** — challenge-tier targets strictly earlier and of permitted kinds; no `validity` entry naming the record's own subject or a part of it; after the request's edges are added (basis entries and equivalence coverage), the support dependency graph remains acyclic (§6.6);
6. **currency** — every basis entry of every submitted record is satisfied at the current admitted ledger head (optimistic concurrency; Admission holds that head by compare-and-swap, and it is admitted because at most one provisional entry exists, §15.3), except that entries naming content the request itself changes are checked against its merged tree; otherwise the request is classified stale and routed to revalidation rather than admitted;
7. **legality** — each obligation the request claims exists and is undischarged at the current head (a duplicate discharge is rejected and recorded), and its discharge predicate (§7.4) holds after the request's own records, including affected evidence rerun on the merged tree;
8. **no collateral regression** — every obligation discharged at the current head and affected by the merged tree stays discharged, with affected evidence rerun. The only legal way to reopen others' closures is an accepted change to a prerequisite authority, whose derived impact obligations are the intended consequence. A D4 change that breaks another closure is a regression and is not admitted;
9. **commit and admit** — one ledger entry containing all records is appended by single-ref compare-and-swap (§15.3). The appended entry is *provisional*. It is *admitted* when a witness quorum holds its exact checkpoint (§15.4), and that is the commit point for every external effect. Only then is the request reported admitted, the integration ref published as a reconciled effect, work dispatched from the new state, and the next entry appended.

**Absorption** of a foreign change already on the integration ref records what happened, so it cannot be stale or illegal. It skips the validation steps and is itself appended and admitted like any entry. It sets the observed tree and changes nothing else: effective structure, ruleset and acceptance stay as admitted. Three things follow:

- foreign structural declarations become quarantined deltas (§6.1);
- foreign semantic content changes revisions, so acceptances and content reliance on it stop being current;
- foreign relation violations make the involved subjects ill-formed (§6.2).

All three take effect in S0 and S2. The S3 obligations that follow — intake, drift, broken closures, integrity findings — only schedule and explain the disposition work (§11).

**Self-reference.** Records reference the candidate commit; they are never stored inside it. Task and result envelopes on run branches are transport, ingested into the ledger, never merged (G2, G3).

**Agent PASS is a proposal.** An admitted PASS judgment is a recorded fact about what the actor concluded; closure is a derived discharge (§7.4).

## 7. Work: obligations and change plans

### 7.1 Two sources of work

The befe678 WorkGraph conflated two different things.

- **Derived obligations** follow from rules and state: a subject without a valid acceptance; a judgment no longer current; an evidence specification without a current admissible realization for its claim; an open challenge awaiting adjudication; a pending human gate; a foreign change awaiting intake, including each quarantined structural delta; a scope deviation awaiting disposition; an admitted change overtaken before publication (§15.3); an integrity finding. They are never authored; they appear and disappear as derivation changes (S3). Their deterministic identities are derived from `(rule, subject)`.
- **Authored intents** carry creative direction: implement this, investigate that, migrate this region. They live in **change plans**: plan units (documents) whose sections are **items**. Each item has an objective, governing units, acceptance criteria, intended affected units, required gates and dependencies on other items or units.

### 7.2 Plan acceptance and local amendment

A `PLAN_ACCEPTANCE` judgment (independent where policy requires) names in its basis the plan's objective section and the item revisions it accepts. An item is issuable only while some current plan-acceptance judgment covers its current revision. Item-level revisions give locality:

- an amendment is an ordinary change to the plan unit; tasks whose basis names a changed item become non-current; tasks on unchanged items continue;
- whole-plan invariants are rechecked mechanically on every amendment: referenced units exist, dependencies are acyclic and respect authority order, gates required by policy are present, acceptance criteria name resolvable evidence;
- the plan's policy states whether an amendment may be accepted by a scoped review of the changed items plus their derived impact set, or needs whole-plan review. Changes to the plan objective, acceptance criteria, topology or gates always need whole-plan review. A scoped reviewer always receives the whole-plan objective and may escalate;
- running tasks remain bound to their basis; no revision pretends an old task saw new requirements.

No global planning/working phase and no global stop exist; an unaccepted amendment only makes its own items non-issuable. Plan lifecycle fields in documents are non-authoritative or generated (§12.6).

### 7.3 Readiness, iteration and attempts

An obligation is **ready** when every prerequisite it names is valid (or provisional, where policy permits provisional continuation; the result is then provisional) and its plan item (if any) is accepted. Readiness is derived from the ledger and content alone (S3). This is the whole "freeze frontier": readiness through the authority DAG, not a waterfall, with no extra state. Whether a ready obligation is *dispatched now* is the Dispatcher's operational decision: resources, routes, serialization surfaces already held (§8.3). That decision never feeds back into derived state.

An **iteration** is the sequence of judgments recorded against one obligation; a NO-PASS leaves the obligation undischarged and the next task is a new iteration. An **attempt** is one execution of one task, owned by the Dispatcher; a failed attempt is recorded in the operator journal and does not touch derived workflow state.

### 7.4 Discharge (canonical closure)

Discharge is an S3 classification with three values: `DISCHARGED`, `DISCHARGED_PROVISIONAL`, `OPEN`.

```text
discharged(o) <=> exists current judgment j of kind(o) on subject(o)
                   by an actor qualified for kind(o), with outcome in passing(o)
              AND status1 of subject(o)'s current revision is not BLOCKED or REVOKED
              AND every evidence obligation of o has a current admissible realization
                  assessed for the current claim revision
              AND every human gate of o is discharged by a current authenticated human judgment
result is DISCHARGED_PROVISIONAL when any input above is P; that value is permitted only
  inside the declared scope of an in-force risk override or where policy permits provisional
  continuation; otherwise the obligation stays OPEN
```

The impact a change triggers on *other* subjects is not a discharge condition: those are separate obligations on the dependents, and Admission step 8 forbids collateral regression. A missing required check is an undischarged obligation; no rule can turn it into PASS.

## 8. Concurrency

### 8.1 What is decided where

| When | What can be established | Mechanism |
|---|---|---|
| Before issue (prediction) | probable footprint: intended affected units, derived impact closure, serialization surfaces | Dispatcher avoids issuing overlapping work; advisory only (K4) |
| At admission (proof) | everything the change relied on is current; actual write set; structural validity of the merged tree; dependency well-formedness | basis currency (§6.6), diff mapped to units, structural checks |
| After merge (evidence) | behavior of the combined tree | evidence currency recomputed on the merged tree; affected realizations rerun |
| Never mechanically | joint validity of independently valid changes where no relation, invariant or evidence covers the interaction | judgment: declared joint-invariant units, review of integrated results, residual risk stated |

### 8.2 Optimistic admission (serializable by validation)

Concurrent tasks work from recorded bases in isolated workspaces. Admission applies requests one at a time to the admitted head, as a merge queue. Speculative batching is delegated to D4 and must preserve this serial order. A request whose basis was overtaken is revalidated — rebased, re-derived, affected judgments re-requested. It is not rejected outright and never silently admitted. Two requests conflict when one modifies a unit or record in the other's basis. This catches write-skew among recorded reliances, including across disjoint files. A losing compare-and-swap between two Admission hosts is the same case.

A very late result whose basis is still current is admissible regardless of age; a fresh result with a stale basis is not. Lease expiry affects scheduling, never correctness.

### 8.3 Serialization policy

Some surfaces make speculative concurrency wasteful or unsafe to merge mechanically: shared schemas and public contracts, build configuration, D1-D3 subjects in one dependency neighborhood, and generated outputs. A unit may carry a policy-declared serialization attribute; the Dispatcher then issues at most one mutating task on it at a time. Generated units are never hand-merged: they declare `GENERATED_FROM` their generator and inputs and are reproduced by regeneration, with conflicts resolved by regenerating.

### 8.4 Residual risk

Semantic dependencies an agent uses without the machinery observing them cannot be captured. Mitigation is layered. The mechanical minimum basis already includes the governing closure. Integration reruns affected evidence. Units may declare cross-cutting **joint invariants**: any change touching their scope re-derives their conformance obligation. Reviews of integrated results are triggered where policy marks a surface high-consequence. The remaining risk is stated in briefs and Review records rather than hidden.

## 9. Agent and human interface

### 9.1 Logical operations

The interface is defined independently of transport.

| Operation | Purpose |
|---|---|
| `open(task)` | returns the task brief (§9.2) and workspace locator |
| `ask(query)` | typed questions: what governs X; what X depends on / what depends on X (per relation class); explain a unit, record or obligation; evidence for a claim; why is this blocked or stale; impact of this workspace diff or proposed edit; text/semantic search; history of X (PEM-gated) |
| `read(ref)` | content by unit identity or path; recorded into the basis |
| `report(item)` | finding, challenge, Serious Challenge, proposed relation, question for a human, scope deviation, blocker |
| `submit(result)` | outcome classification from the task's allowed set, plus the workspace. Machinery builds the typed admission request (§6.8): diff, touched units, changed authored relations, basis and derived consequences. The response is `ADMITTED` only after the entry is admitted (§15.3); before that it is `PROVISIONAL`, and an entry that is lost is resubmitted by request identity |
| `decide(gate)` | human only: a gate brief (§9.4) and an authenticated decision |

Within a task, `ask` and `read` answer at the task's basis (snapshot isolation), so an agent never sees a mixture of states. `ask("what changed since my basis")` reports admitted changes that intersect the task, letting the agent stop early instead of discovering staleness at submission.

The agent never declares claims, revisions, edges (other than by writing authored relations as part of semantic content), subject roles, epochs, plan patches, lifecycle states or reconciliation steps.

### 9.2 Task brief

A task brief contains, in this order:

1. objective and obligation kind;
2. allowed outcomes;
3. **governing content inline**: the exact text of governing units at the basis revisions;
4. constraints, non-goals and delegated space;
5. acceptance criteria and required evidence;
6. open challenges, findings and provisional states touching the subject;
7. **incompleteness notices**: where the basis was widened or `UNBOUNDED`, where analyzers are incomplete, where relations are only proposed, where a relied-on unit is a part whose validity comes from a coarser subject, where the repository declares structure that governance has not admitted (quarantine), and the qualified ledger head the brief was derived at;
8. workspace and submission instructions.

It is rendered deterministically from derived state by version-bound templates; no model is needed to translate machine state.

### 9.3 Epistemic status of context

Every context item is labeled:

| Class | Meaning |
|---|---|
| `GOVERNING` | authority the task's subject concretizes or is constrained by; mandatory |
| `IMPLIED` | reached by accepted authored relations inside a judged-complete scope |
| `ADJACENT` | reached by derived structural relations; completeness per analyzer declaration |
| `EVIDENTIAL` | evidence for the subject's claims, with current/stale/unavailable status |
| `HISTORICAL` | PEM entries and Git history; offered only when the PEM predicate fires or on explicit request |
| `CANDIDATE` | search or embedding hits and unaccepted proposals; never authority, never closure support |

Each item also carries its acceptance status (valid, provisional, challenged, stale, drift, quarantined, ill-formed, unclassified) and its inclusion path. Every answer names the qualified ledger head it was derived at (§15.4); with no qualified head, answers are labeled historical (`UNQUALIFIED`) and claim no currentness. Answers are deterministic for identical basis, query and policy version. Search indexes record their versions, and nondeterministic search contributes only `CANDIDATE` items outside the determinism guarantee. A search hit can lead to a proposed relation, but never by itself to an accepted one.

### 9.4 Human gates

A gate brief presents the non-narrative evidence core first: identities, coverage, key data and trajectories, findings as data. Agent interpretation, alternatives, anomalies and unresolved findings follow separately. Gate-evidence adequacy is a semantic judgment, not a presence predicate: the human's decision records whether the evidence was adequate, and that record can itself be challenged. Agents and machinery may request a gate; they cannot synthesize a human judgment. A risk override is a distinct judgment kind that authorizes bounded continuation and leaves dependents provisional (S2, §6.6).

### 9.5 Transports and harnesses

Transports expose the same logical operations. There are three: an MCP server; a CLI; and a Git-envelope transport for zero-context web agents (an immutable task envelope on an isolated run branch, a result envelope plus candidate commits written back, and polling-first fetch of the specific run branch). Harness adapters (Claude Code, Codex, OMP, Pi or others) only map these operations and launch/observe executions. The bootstrap is `Execute SSDS task <id>` plus the minimum locator the environment does not already bind (repository, run ref, envelope path, protocol/profile source). It fails truthfully when protocol material cannot be resolved. Transport and process success never imply evidence admissibility or task success.

## 10. Evidence

| SSDP evidence concept | SSDS 8 representation |
|---|---|
| specification | evidence unit with `EVIDENCES` -> claim unit and declared or derived `EXECUTION_DEPENDS_ON` |
| realization | observation record whose basis has two parts: **target** (claim unit revision) and **execution** (code units, data identity, environment, backend, precision, configuration, parameter instance, regime, seed and replicate identity) |
| observation | the realization record's outcome plus references to native artifacts (logs, data) by content identity where possible |
| assessment | judgment record; later reassessment supersedes, never rewrites |

A realization supports a claim at revision `c` only while its execution basis is current and its target is `c`, or an equivalence judgment covers the change. An execution-dependency change triggers a rerun obligation; a target change triggers an assessment-review obligation. Stale passing evidence never discharges; stale failing evidence is not admissible against the current claim. Unavailable artifacts degrade binding health through availability observations: the historical record survives, and present use becomes `UNAVAILABLE`. Process exit or harness success is never evidence admissibility. A realization with incomplete or malformed evidence is recorded as such and cannot enter a PASS/FAIL assessment. Raw data stays in native stores; the ledger stores identities and bounded classifications.

**Who may realize evidence.** A realization can discharge an evidence obligation only in two cases: a runner that project trust policy designates for that specification executed it (normally Dispatcher-controlled execution on the exact candidate or merged tree), or a designated runner reproduced it. Results an agent reports from its own workspace are findings: useful for direction, never admissible for discharge. Policy may let expensive scientific realizations (long simulations, HPC campaigns) run under recorded custody outside the Dispatcher; the realization record then names the custody evidence.

## 11. Intake: one route for every change of unknown provenance

### 11.1 Detection and entry

Intake is not a separate engine. It is a set of derivation rules plus judgment kinds that treat any content not produced by an admitted request as a change with an **unknown basis**.

Recorded observations detect it:

- the live integration ref has moved away from the admitted commit (direct push, external merge, force-push, restore from backup, manual conflict resolution, or overtaking an unpublished admission, §15.3);
- a submitted workspace contains changes outside its reported result;
- an external branch is offered for import;
- content differs from accepted revisions (drift);
- the observed structural declarations differ from effective structure (quarantine);
- a scheduled census finds untracked or unexpected material.

Two entry paths share one rule set. Content **already on the live integration ref** is absorbed mechanically (§6.8): the observed tree advances, nothing governing changes, and its consequences become obligations. Content **offered as a candidate** is a change whose basis is computed conservatively from its merge base: mechanical minimum plus widening. That covers an external or foreign-agent branch and agent work outside its reported result. It reaches the integration ref only through ordinary Admission, after its intake obligations are discharged.

### 11.2 Processing and dispositions

```text
preserve exact identity (commit/ref/tree; nothing executed)
 -> diff against the last admitted observed tree; map changed paths to effective leaves
 -> structural declarations: compare decl(T_n) with Σ_n; each differing key is a quarantined
    delta, classified governance-affecting or governance-neutral (§6.1)
 -> uncovered paths: proposed new units, statically classified
    (path, type, Git history, known producers, build manifests, parsers, provenance)
 -> mechanical consequences (S0/S2): changed revisions make dependent records non-current;
    aff(Q) and ill-formed subjects are invalid
 -> obligations (S3): classification and disposition judgments; equivalence/materiality
    judgments; conformance or acceptance reviews for touched authority; adoption or
    realignment of each quarantined delta; quarantine for untrusted or opaque active content
```

**Dispositions** are judgment outcomes:

| Disposition | Meaning |
|---|---|
| `ABSORB` | accept the content as it stands; for a quarantined structural delta, **adopt** it (below) |
| `RECONCILE` | needs rework |
| `SPLIT` | divide into separately classified parts |
| `ARCHIVE` | keep as historical material |
| `RETAIN_AS_EVIDENCE` | keep as evidence, not authority |
| `MARK_GENERATED` | regenerate rather than edit |
| `QUARANTINE` | isolate untrusted or opaque content |
| `REJECT` | revert by an ordinary change; for a structural delta, a change that **realigns** the declaration with effective structure |
| `DISPOSABLE` | classification only; deletion is a separate authorized change |

**Structural intake.** A quarantined delta becomes effective in exactly one way: an admission request carries an `ABSORB` disposition adopting it, and Admission validates the adopted change exactly as if the requester had authored it now (§6.8 step 4). This includes the challenge freeze at source and destination, a same-request acceptance for any promotion, mode consistency and SDG integrity. Adoption is therefore re-authoring under current rules and authority, never ratification of presence. It is validated under the ruleset in force when it is admitted, not the one in force when the foreign change appeared. A ruleset adoption never changes `Σ` or `Q`, and the governance-affecting/neutral classification is fixed by system semantics, not by policy. A governance-neutral delta (re-partition of leaves inside one subject) cannot change any subject or acceptance, so where policy permits, Admission may adopt it by a mechanical intake request; it still passes step 4.

### 11.3 Effect on governance

Foreign content affects governance only through lower-stratum facts, never through S3:

1. **Changed bytes or semantic declarations** change revisions, so acceptances and content reliance on them stop being current (S2).
2. **Changed structural declarations** are quarantined. They do not enter `Σ`, and every subject in `aff(Q)` has `ok = F`. Until the delta is adopted or realigned, such a subject cannot serve as validity prerequisite, governing context or acceptance basis. Routing (`subj`, scope, tenure) continues to follow admitted structure.
3. **Uncovered content** is `UNCLASSIFIED` and excluded from governing use.
4. **Illegal relation structure** makes its subjects ill-formed (`ok = F`).

The S3 intake obligations only schedule and explain disposition work. Unqualified authority therefore cannot arise from repository presence, because no S0 input that S2 consumes is changed by presence alone.

**Inspectable and recoverable while non-authoritative.** Foreign content is never hidden or discarded. The observed tree *is* the product: foreign commits remain in Git and can be built and released. The absorption record and the ledger keep the observed tree reachable. Views show each quarantined delta beside its effective value, with the absorption entry that introduced it and its provenance. Every disposition is an ordinary admitted change that a later admitted change can reverse. Production is not blocked; what remains open is governance closure. Agent overstep, manual edits, collaborator branches, foreign-agent work, repository restores, manual merges, legacy import and corruption repair all use this one route.

### 11.4 External units and cross-repository projects

Scientific code, data and evidence often span repositories. SSDS 8 governs one ledger per project; it does not provide atomic admission across repositories (§20). It supports cross-repository projects through immutable pins:

- An **external unit** is identified by an immutable source identity: a repository identity plus an immutable commit/tree and region, a package version with digest, a dataset hash or a DOI with variant/locator. Its content never changes, so `content` entries on it never go stale. A change of pin is an ordinary local content change, and its impact is derived locally.
- **External acceptance.** An `EXTERNAL_ACCEPTANCE` judgment imports the fact that the external project's own process accepted that exact revision and scope, citing its evidence, in the same way as legacy acceptance (§12.1). Without one, native reliance on the external unit is provisional. The judgment's basis names, in `record` mode, the consultation observation it relied on. An external correction or retraction is a binding/applicability event under the 6.6 semantic-definition owner. When a later consultation observes that the pinned triple is no longer accepted by its owner, or finds the external ledger `FORK`, `ROLLBACK` or retired, Admission records it with mandatory supersession of the earlier consultation, so every import relying on that consultation becomes non-current mechanically. A merely unreachable (`UNQUALIFIED`) external ledger supersedes nothing, which keeps network loss from flapping imports. A qualified actor may additionally raise a challenge on the importing subject. External status is only as fresh as the latest consultation. Re-consultation is an advisory Dispatcher obligation, and briefs show the consulted position.
- **Another SSDS project's ledger** may be consulted read-only. The consultation qualifies that ledger's head under its own witness model (§15.4); an unqualified external head is never imported. An observation records the qualified head consulted, the checkpoints used and the derived status read. The external ledger is never written, never merged and never treated as local authority.
- **Multi-repository change** is a sequence of admissions: the producer first, then the consumer pinning the producer's admitted commit. Intermediate states are visible and legitimate: the consumer stays on its older pin until its own admission.
- **Reconciliation.** The Dispatcher may observe that a newer external revision exists; that creates an advisory obligation, never a block.
- **Supported project class:** coupling through immutable pins (submodules, lock files, package versions, dataset hashes, DOIs). Scopes that must co-evolve atomically belong in one repository and one ledger; otherwise their transient cross-repository inconsistency is visible as provisional or advisory state, never hidden.

## 12. Migration and live coexistence

### 12.1 Governance modes

Every subject is in exactly one governance mode at any ledger position, and its parts share it (M3):

| Mode | Meaning |
|---|---|
| `NATIVE` | SSDS-governed: acceptance, conformance and evidence obligations derived and enforced by Admission |
| `LEGACY(p)` | governed by a declared legacy process bound to protocol version `p` (for example document-controlled SSDP 6.6); SSDS records and derives but does not adjudicate or reinterpret |
| `UNGOVERNED` | production content with no authority system yet (Case C); changes are recorded, mechanical consequences derived, no conformance claims made |
| `UNCLASSIFIED` | unknown content; excluded from governing context, evidence and acceptance basis until classified |

Mode transitions are admitted lifecycle records, and each ends the subject's tenure (§6.1). A version rollback that returns a subject to `LEGACY(p)` therefore needs a fresh `LEGACY_ACCEPTANCE` import; an import from before cutover never revives. A membership change that would move a unit between subjects of different modes is a mode transition for that unit and needs its lifecycle record (§6.8 step 4). Neither an ordinary request nor an adopted foreign declaration can do it silently. A change touching subjects in several modes receives the union of their obligations. Changes confined to `LEGACY(p)` or `UNGOVERNED` subjects may arrive as ordinary commits. They are absorbed mechanically (§6.8, §11), and derive only intake classification for uncovered paths plus whatever the mode's policy requires.

**Relying on legacy authority.** SSDS never adjudicates a `LEGACY(p)` subject, but native work often depends on legacy authority that its own process did accept (for example SSDP source accepted through `PROTOCOL-RELEASE-STATE.yaml`). A `LEGACY_ACCEPTANCE` judgment imports that fact. It cites the legacy process's acceptance evidence for an exact revision of an exact scope, and supplies the acceptance judgment for that `(subject, scope_id, rev)` without claiming SSDS reviewed it. The imported scope is the scope the legacy process actually accepted. A legacy acceptance of a whole document or release cannot be imported onto a section: that would be B1's projection. Native work relying on a legacy subject without an imported acceptance is provisional.

### 12.2 Reconstruction status, refinement and subject promotion

Authority-bearing subjects carry a reconstruction status: `OPAQUE` (internal semantic structure unknown), `PARTIAL`, `RECONSTRUCTED`.

**Structural refinement** is an admitted change that partitions a leaf's scope into new leaves declared as **parts** of the original unit, which becomes (or remains) a composite subject. Scope conservation is checked mechanically: the children's scopes are disjoint and their union is the parent's scope. Structural refinement makes no semantic claim. A byte-preserving refinement leaves the subject's scope identity, content identity, signature and tenure unchanged, and its semantic declarations unchanged unless relations are redirected. The subject's revision is therefore unchanged and its acceptance remains valid; nothing is copied or carried. The parts hold no acceptance of their own: every `validity` reliance on a part routes to the subject (§6.6). `content` reliance on a part is local to its bytes. Refinement enables locality of reading, context and parallel reconstruction without touching authority. Coarse relations stay on the subject until redirected to parts by authored relations. Redirection is a change to semantic declarations and therefore a new subject revision that needs acceptance.

**Subject promotion** makes a part `A` of subject `P` into its own subject. It is a semantic act and needs both:

1. an admitted declaration change marking `A` as a subject, so `subj(A) = A` and a new tenure of `A` begins — authored by the request, or adopted from a quarantined foreign declaration (§11.2); and
2. an acceptance judgment on `(A, scope_id(A), rev(A))` in that new tenure, by an actor qualified for `A`'s domain under its owner's acceptance contract. If the request also changes `A`'s domain, the old domain's owner must release it as well (§6.8 step 4(a)), so promotion cannot route `A` to a weaker reviewer. The judgment records the actor's conclusion that `A`, read with its own declared relations, is a self-standing subject whose meaning the holistic acceptance of `P` supports. Its basis names `P`'s acceptance (`record` mode) and widens to `P`'s former scope until a completeness judgment narrows it (§6.5). For a `LEGACY(p)` subject, only the legacy process can accept `A` separately; SSDS does not.

Promotion and its acceptance are admitted in one request; a promotion without a current acceptance leaves `A` invalid rather than silently valid. Promotion is rejected while `P` or `A` carries an unresolved blocking challenge or a revoked revision (§6.8 step 4). The judgment may conclude that `A` is not self-standing — for example, because `A` relies on a convention stated only in a sibling part. In that case `A` stays a part, or the owner first makes the coupling explicit as an authored relation (`A USES_DEFINITION B`). Members of a simultaneous-definition group are promoted together, as one composite subject whose scope also contains the SDG declaration, or not at all. Every legal cycle lies inside one SDG (§6.2), so no promotion can split a cycle. Neither conservative widening, byte identity nor an unchanged relation set can substitute for this judgment.

**Demotion and restoration.** Demoting a subject `A` into a part of composite `P` ends `A`'s tenure. `A`'s acceptance judgments leave `ACC(A)` permanently: they stay in the ledger as history, unsuperseded, but no future tenure counts them. Validity reliance on `A` now routes to `P`, which needs its own acceptance if it is new or its scope grew.

Restoring `A` to subject status later, by an ordinary request or by adopting a foreign declaration, is a promotion and starts a new tenure. It needs a new acceptance judgment in the same request. No separate reinstatement kind exists: a reinstatement is an ordinary acceptance whose basis may cite the earlier tenure's judgments, reviews and evidence by `identity`. Prior evidence counts only where it is currently admissible: its target and execution bases are current, and stale passing evidence never confirms.

An old acceptance therefore cannot become current again because structure changed, and the protection has two independent locks:

1. repository presence never changes `Σ` (S11);
2. even an admitted restoration starts a tenure that excludes every earlier judgment.

Challenges, revocations and supersessions target exact triples and records without tenure, so they bind the restored subject exactly as before. Demotion, restoration and every other signature change are frozen while any affected subject's current revision is under unresolved blocking challenge or revoked (§6.8 step 4(b)). A challenge thus constrains a role transition rather than following the unit out of it.

**After promotion.** `P` keeps its frozen scope, which still includes `A`'s bytes, and so keeps its tenure. `P`, and validity reliance on its remaining parts, therefore stays valid only while that whole scope is byte-identical to `P`'s accepted revision. Once `A` evolves, reliance on the remaining parts needs one of three things: a scoped `EQUIVALENCE` judgment for their consumers; acceptance of a residual subject (a new scope); or, for `LEGACY(p)`, a new legacy acceptance. A **carve-out** is a promotion after which `A` leaves `P`'s governance mode (for example, cutover of one section, §12.4); the same rule applies.

**Equivalence across scopes.** An equivalence judgment relates revisions of one unit; it never relates different scopes. Acceptance moves to a new scope only through an acceptance judgment on that scope (promotion). Everything else stays historical lineage.

This replaces LegacyAggregate: a legacy aggregate is a coarse `OPAQUE` subject, and "digestion" is structural refinement followed, where wanted, by qualified promotion.

### 12.3 Discovery bottom-up, acceptance top-down

Agents may propose candidate D3, D2 and D1 units reconstructed from D4 behavior, papers, comments, tests and history (reconstruction judgments). A proposed upstream unit is accepted only through its owner's acceptance (human-gated where policy requires). Until then, descendants that rely on it are provisional, and no D4 behavior creates accepted authority. Reconstruction that cannot recover intent records `PROVISIONAL` or `UNKNOWN` explicitly (M5).

### 12.4 Cutover

A transition of a subject from `LEGACY(p)` or `UNGOVERNED` to `NATIVE` requires:

1. adequate reconstruction status under policy;
2. a migration-equivalence judgment that representation changed but behavior and meaning did not (or a separately governed change if they did);
3. owner acceptance of the native revision of that exact subject;
4. for a carve-out from a legacy subject: the subject promoted first, and a human-gated record by the legacy process owner releasing that scope from the legacy process (§12.2);
5. disposition of every in-flight legacy run on that subject: drained, pinned to its version in an isolated workspace, or explicitly migrated (M6);
6. an admitted cutover record.

After cutover only Admission governs the subject. Legacy-side edits to it are foreign changes (§11), and the legacy representation is historical. A part cannot cut over apart from its subject. Interrupted migration leaves no half state: each refinement, promotion and cutover is one admission.

### 12.5 Deployment cases

| Case | How it enters | What is special |
|---|---|---|
| A native project | genesis with fine subjects; all `NATIVE` | nothing |
| B SSDP 7 or earlier documents | manifest declares section-level **parts** of each legacy subject (the scope its process accepted: a document, or a release tree) without rewriting files; mode `LEGACY(p)`; relations extracted heuristically are `CANDIDATE`/proposed | version-pinned workplans stay governed by their protocol; section locality serves reading and context, while validity of a section routes to its legacy subject; promotion and scope-local cutover per §12.2-§12.4 |
| C mature repository without authority | a few coarse `UNGOVERNED`/`OPAQUE` subjects by top-level region; analyzers give derived structure early | bottom-up reconstruction proposals, top-down acceptance; production continues |
| D live partial migration | mixed modes | a production edit to a unit makes non-current exactly the reconstruction judgments whose basis named it; unrelated migration work is unaffected — no special rule |
| E external or foreign-agent branch | intake of a change with unknown basis | provenance recorded; obligations derived from touched units |
| F drift or corruption | intake; derived state rebuilt; ledger integrity and currentness qualification checked | §13 |

Genesis for an existing repository records project identity, ledger location, the authoritative ledger replica, trust roots, witness set and quorums, ruleset version, the initial effective structure and coverage, and the baseline commit. Per FF-001, no genesis or cutover identity is published as immutable before every required declaration and record exists and validates.

### 12.6 Documents, workplans and skills after cutover

Change plans and authority documents remain semantic artifacts. In natively governed documents, lifecycle fields (`status:`) and directory placement (`active/`, `archive/`) are either removed or generated from derived state and marked non-authoritative; a manual edit to them enacts nothing. Skills remain epistemic procedures and stop owning workflow transitions represented by rules. Historical pre-cutover workplans and records stay immutable under their original semantics.

## 13. Failure, recovery and long-horizon evolution

| Failure | Detection | Repair |
|---|---|---|
| Corrupted derived state | integrity checks, mismatch with re-derivation | discard and re-derive |
| Corrupted ledger entry | authentication, hash chain, schema validation | restore from a replica whose chain qualifies (§15.4); else human-gated `LEDGER_LOSS` naming the abandoned checkpoint. Lost judgments become undischarged obligations; prose or reports may inform new judgments by qualified actors but never restore old records. Lost structural admissions leave the repository declaring structure that `Σ` no longer contains; that difference is quarantined (§11.3), so a truncated history cannot revive an acceptance that a lost demotion had ended |
| Ledger ref rewound (force-push, hosting restore, backup older than the admitted head, mistaken or malicious reset) | head is a strict ancestor of a checkpoint observed in a read quorum (every admitted head is visible there, §15.4) or of a high-water mark | fail closed (`ROLLBACK`); restore the later chain from any replica or clone that holds it; if none does, human-gated `LEDGER_LOSS`; Admission halted until resolved |
| Ledger fork, or witnesses holding checkpoints on conflicting chains | qualification | fail closed (`FORK`); human-gated fork resolution choosing one lineage and naming the abandoned head; key rotation if compromise is suspected; never auto-merged |
| Crash after append, before admission | provisional entry on the ledger ref | on restart Admission completes anchoring of the surviving entry (idempotent; nothing else could append in between). If the entry survives nowhere, it was never admitted: no effect, publication, dispatch or answer depended on it, and its request is resubmitted by identity. A sub-quorum checkpoint of a vanished entry surfaces as `FORK`/loss and is resolved by human-gated abandonment; abandoning it loses no admitted judgment |
| Crash after admission, before publication | admitted entry, publication `PENDING` | §15.3: publication retried, or the overtaken change revalidated |
| Witnesses below read quorum (unreachable or lost) | qualification cannot complete | `UNQUALIFIED`: historical views only, no current assertion, Admission halted, production continues; permanent loss beyond the fault bound needs human-gated witness-set redesignation (§15.4) |
| Authoritative replica lost | unreachable or empty | restore from any replica extending the highest observed checkpoint; human-gated replica redesignation record |
| Fresh clone (with or without a historical prefix) | no high-water mark | qualify against a read quorum; fetch the missing suffix (`BEHIND`) or detect `ROLLBACK`; with no read quorum, views are `UNQUALIFIED` and Admission refuses to append |
| Lost local store, intact repository | absent operator state | ledger is in Git; operator journal rebuilt; running executions reconciled by observing harnesses and workspaces; stale leases released; high-water mark re-established by qualification |
| Foreign structural change (manual manifest edit, force-push, restore from stale backup, manual conflict resolution) | observed declarations differ from `Σ` | absorbed; bytes remain buildable; deltas quarantined; `aff(Q)` invalid until adopted or realigned (§11.2-§11.3); no tenure restarts and no acceptance revives |
| Content objects referenced by the ledger unavailable | object lookup | binding health `UNAVAILABLE` for affected derivations; fail closed for dependent closure; restore objects from any replica (the ledger keeps referenced commits reachable) |
| Repository move, clone | — | project identity is in genesis, not in paths |
| Project fork (intentional) | fork lifecycle record | new project identity; cross-fork work enters by intake; ledgers never merge automatically |
| Analyzer version change | derivation key change | re-derive; judgments whose basis named analyzer output become non-current only if the output changed (early cutoff) |
| Relation or record schema change | schema version | explicit READ/MIGRATE/REJECT; migration is an admitted lifecycle record; old records retained |
| Ruleset change | ruleset adoption record | admissions are never re-adjudicated; current derivation uses the adopted ruleset; a previously discharged obligation that the new ruleset no longer considers discharged becomes an open obligation, never rewritten history; a relation reclassification that makes an accepted structure illegal makes its subjects ill-formed until repaired; effective structure and quarantine are unchanged; historical views are reproducible with the ruleset in force at their position |
| Interrupted migration | — | refinement, promotion and cutover are atomic admissions |
| Very old task returns | basis check | current basis: admissible; stale basis: recorded as observation and routed to revalidation |
| Concurrent results from stale bases | currency at admission | first admitted; others revalidated only where their basis intersects |
| External evidence artifact disappears | availability observation | binding health degraded; present use `UNAVAILABLE`; rerun or remap obligation |
| Manual edit of authority | drift | intake; every reliant record non-current; acceptance of the edited revision (a light representation-only acceptance when editorial) plus an independent equivalence judgment restores reliant records without re-reviewing them; otherwise normal impact closure |
| Migration under a wrong interpretation | later challenge against the reconstruction or promotion judgment | upheld challenge revokes it; dependents non-current or provisional; blast radius computed from bases |
| Completeness claim proves false | challenge to the completeness judgment | every inference that used it becomes non-current |
| Crash before the append | no entry with the request identity | nothing happened; request retried idempotently |
| Sensitive value found in a ledger entry or pinned content | Admission checks, audit, report | §15.5 breach protocol |
| SSDS 9 migrates SSDS 8 | — | ledger is self-describing and versioned; SSDS 9 either reads it compatibly or starts a new lineage with a migration record naming the SSDS 8 last admitted head; no reinterpretation of admissions |

Recovery-time objective: derivation of current state must not require replaying an unbounded history. Derived checkpoints keyed by `(ledger position, ruleset, schema, analyzer versions)` bound restart cost and are verified against the ledger before use. They cache the derivation of a position, including `Σ`; they carry no currentness, which belongs only to the qualified head (§15.4). They are unrelated to the witness checkpoints of §15.4.

## 14. Where machinery must stop

Deterministic machinery prepares, but never decides:

- whether two scientific or numerical formulations mean the same thing, and whether a change is editorial or semantic beyond byte/normalization identity;
- whether an acceptance of one subject supports a newly scoped subject (promotion, carve-out, restoration);
- whether a foreign structural declaration expresses intended governance (adoption of a quarantined delta), and whether a set of objects is genuinely simultaneously defined;
- whether an observed discrepancy is a D4 defect or exposes inadequate D3, D2 or D1;
- whether evidence actually supports a governed claim, and whether gate evidence is adequate;
- whether an inferred or searched-for relationship is materially real; whether a relation scope is complete;
- how an ambiguous legacy region decomposes and what its upstream intent was;
- whether an architectural change preserves its parent abstraction;
- whether a Serious Challenge is warranted, how it is adjudicated, and whether a risk override is acceptable;
- whether a marked product surface is accepted (product-scope owner, P7?);
- whether a confidentiality incident requires destructive remediation.

For each, the machinery produces a **focused question**: the exact subject, scope and revisions; the distinctions already resolved; the evidence and its status; what the answer will change; and the allowed outcomes. The answer is a recorded judgment that then propagates mechanically.

## 15. Persistence, publication, trust and security

### 15.1 Stores

| Store | Content | Canonical? | Location | Sole writer | Recovery |
|---|---|---|---|---|---|
| Content store | all repository content including authored relations, unit manifests and anchors (the *observed* state) | yes, for meaning; structural declarations are proposals until admitted | the project's Git repository | humans and tools through Git; Admission only by publication CAS | Git replication; foreign movement absorbed (§11); referenced commits kept reachable by the ledger |
| Ledger | records (§6.3) under the closed schema, from which effective structure, ruleset and acceptance derive | yes, for everything not derivable | one authoritative ref in a Git repository designated at genesis: the project repository's reserved namespace, or a dedicated (for example private) ledger repository | Admission | any replica extending the highest observed checkpoint; else human-gated `LEDGER_LOSS` (§15.4) |
| Witness checkpoints | authenticated `(ledger id, position, head)` statements and lineage-retirement statements; hashes only | no; evidence that admits entries and detects rollback | declared witnesses outside the authoritative replica's administrative control | Admission (checkpoints); any participant may relay an existing authenticated checkpoint (read repair) | redundancy by quorum; loss beyond the fault bound by human-gated witness-set redesignation |
| Derived index | derived state, effective structure and derivation checkpoints | no | local, rebuildable (SQLite or equivalent, delegated) | Derivation | discard and re-derive |
| Operator state | leases, reservations, account and quota telemetry, harness sessions, raw prompts and transcripts, signing keys and secret references, high-water marks | no project authority | private user-local root outside repositories | Dispatcher (journal); each participant's Ledger Store (its high-water mark); Admission (its keys) | journal rebuilt by observing harnesses and workspaces; high-water mark re-established by qualification; keys by trust-root lifecycle |
| Transport | task and result envelopes on run branches | no | isolated run refs; retired by policy, never merged | Dispatcher and Interface (envelopes); agents (results) | regenerated from the ledger and obligations; results ingested only through Admission |

### 15.2 Storage decision

The consolidated Protocol 8 plan defaulted canonical history to a private local store. It permitted in-repository non-secret control state only when a later D3 adoption resolved concurrency, privacy, history and ownership. The f9d9de8 revision declared that adoption prematurely (B3). The candidates were re-evaluated on total fitness:

| Option | Commit atomicity | Machine loss | Multi-host | Rollback detection | Privacy | Authoritative representations |
|---|---|---|---|---|---|---|
| (a) private transactional store (SQLite) + governed repository export | local transaction | export lag is a loss window; restore needs the export | needs a hosted service, or the export becomes the authority | still needs anchoring of the export | private by default | two; after loss the export is the de facto authority |
| (b) f9d9de8: Git ledger with same-repository multi-ref atomic update | depends on a negotiated server capability | replicated | compare-and-swap | absent | in-repository; break-glass undefined | one |
| **(c) selected**: Git ledger, single-ref append, quorum admission, reconciled publication | single-ref compare-and-swap on every Git host, admitted by witness quorum | replicated with ordinary fetch/push | compare-and-swap | currentness only for quorum-witnessed heads; read/write quorum intersection; high-water marks | closed schema; optional private ledger repository; breach protocol | one, plus a small checkpoint witness set |

**Decision.** Retain a Git-replicated canonical ledger, re-specified as (c). Option (a) needs a second authoritative representation to survive machine loss, or a hosted service, and still needs the same anchoring. Option (b) rests correctness on a capability many deployments lack. Option (c) resolves the predecessor's four conditions explicitly: ownership and concurrency (§15.3), history (§15.3-§15.4), and privacy (§15.5). It adds only a checkpoint witness set, which P4 requires anyway: currentness cannot be proven by the replica it is meant to check. The D3 contract is complete at this level; deployment realizations listed in §21 item 14 remain Architecture Manual closure obligations, not open D3 choices. Reopen triggers are in §26. If the Manual finds a counterconstraint to Git-hosted storage, replacing it reopens D3, and any replacement must keep these requirements: append-only authenticated history; a single-writer append; currentness only for quorum-witnessed state; reconciled publication after admission; replication independent of any one machine; and the closed schema.

### 15.3 Commit point and publication

**Ledger representation.** Each admission or lifecycle entry is one Git commit on the authoritative ledger ref, whose parent is the previous entry. Git's commit chain is the ledger's hash chain. Each entry is authenticated under the declared trust mechanism (§15.4). The ledger keeps every content commit it references reachable from its own history, so product-ref force-pushes or deletions cannot make history underivable. When the ledger lives in a dedicated repository, that repository holds those objects.

**Append (one semantics, local and remote).** The append is a compare-and-swap of the single ledger ref from the expected previous head to the new entry:

- *local authoritative repository:* a local reference transaction with expected old value, under a declared durability configuration (object and ref fsync) sufficient for the claimed crash model;
- *remote authoritative replica:* a push of the single ledger ref with expected old value, which the server rejects if the ref moved. This needs no multi-ref capability.

A losing writer re-validates against the new head (§8.2).

**Commit point: admission by witness quorum.** An appended entry is **provisional**. It becomes **admitted** — current-qualified, and the commit point for every external effect — at the moment `q_a` witnesses have durably acknowledged its exact checkpoint (§15.4). The ordering is fixed:

```text
append (CAS, durable)  ->  PROVISIONAL
checkpoint acknowledged by q_a witnesses  ->  ADMITTED
then: submit response ADMITTED; integration-ref publication; dispatch from the new state;
      current-state answers at the new head; next append
```

Admission keeps **at most one provisional entry**. It appends entry `n+1` only after entry `n` is admitted and `n`'s publication is resolved. The single exception is a human-gated witness-set redesignation, which may be appended over a provisional entry and whose admission settles that prefix (§15.4). Because of this rule, the head Admission validates against (§6.8 step 6) is always admitted. A provisional entry never influences derivation that anyone relies on.

After a crash, the request identity tells Admission what happened. If no entry carries it, nothing happened and the request is retried. If a provisional entry carries it, Admission completes the idempotent checkpoint distribution; nothing else could have appended in between, so the validation still holds. If an admitted entry carries it, Admission proceeds to publication. A provisional entry whose every copy is lost was never admitted, and its request is resubmitted by identity (§15.4).

**Publication.** An admission record names its admitted commit `C_n` and expected predecessor `B_n`, the commit at which the previous admission was published or absorbed. Publication begins only after the entry is admitted, and appending the next entry requires it to be resolved. Publication is an effect under C4: Admission compare-and-swaps the integration ref from `B_n` to `C_n`. The publication state is derived from the ledger plus the latest recorded observation of the live integration ref `L`:

| State | Condition | Action |
|---|---|---|
| `PENDING` | `L = B_n` | retry the idempotent compare-and-swap |
| `PUBLISHED` | `C_n` is an ancestor of or equal to `L`; or an observed external merge produced a commit with `C_n`'s tree and parent `B_n` | record outcome; any movement of `L` beyond it is ordinary foreign change; next admission may proceed. A records-only request has `C_n = B_n` |
| `OVERTAKEN` | otherwise (the ref moved in the window: foreign push, external merge of other work, force-push) | absorb `L` as a foreign change (§11); `C_n` stays recorded and reachable, its records are re-evaluated against the absorbed tree, and an obligation to revalidate the overtaken request is derived (§8.2) |

The three states are sufficient under the repaired currentness semantics, and no fourth publication state is added. Being provisional is a property of the ledger entry, not of publication, and publication is never attempted for a provisional entry. An `OVERTAKEN` admission's structural changes are already in `Σ` but absent from the absorbed tree. The difference appears as quarantine until the revalidated request publishes and realigns the repository (§6.8 step 4), which is conservative and needs no special case.

Admission never moves the integration ref except by compare-and-swap from the exact expected predecessor, so it never overwrites foreign work. Revision 2 allowed updating the ledger and integration refs in one multi-ref transaction as an optimization; that is withdrawn, because it would publish an entry before admission. No product ref ever shows provisional state. If the authoritative replica, the integration host or a witness read quorum is unreachable, admissions stop (fail closed) while production continues.

### 15.4 Currentness qualification and anti-rollback

**Contract (P4).** Currentness is asserted only for durably witnessed state. A head is *current-qualified* only when a witness quorum holds its exact identity and it extends every checkpoint and high-water mark the evaluator observes. Every current-state assertion names its qualified head. Revision 2 claimed this while also permitting an undetectable rewind inside a bounded anchoring lag. That mode is withdrawn, and the claim now holds without exception under the declared witness model.

**Witness model.** Genesis declares `N` witnesses outside the authoritative replica's administrative control, an admission quorum `q_a`, a read quorum `r`, and a fault bound `f`, with

```text
q_a + r > N + f        (any admission quorum and any read quorum share more than f witnesses)
```

A faulty witness may be lost, rolled back or adversarial. Genesis and every witness-set redesignation reject parameters that violate the inequality. The declared single-user local-trust mode is the instance `N = 1, q_a = r = 1, f = 0`, with the witness on another medium under the same user. It is the same contract under a stated premise (that witness is not rolled back together with the replica), and status views show the mode.

**Threat and trust model.**

- *Defended against:* mistaken force-push or deletion of the ledger ref; hosting restore from an older backup; a compromised push credential for the authoritative replica; replica divergence after failover; direct pushes of crafted entries; crashes at any point; loss, rollback or misbehaviour of at most `f` witnesses.
- *Trusted:* Admission signing keys declared in genesis trust roots and held only in private operator state; at most `f` faulty witnesses; each participant's own high-water mark.
- *Not defended:* more than `f` faulty witnesses acting with control of the replica; forgery by a holder of an Admission key (such forgery shows up as a fork if any honest copy exists); the information-theoretic case below.

**Mechanism.**

1. **Authentication.** Every ledger entry is authenticated: signed by an Admission key in the trust roots, or protected by local access control in declared local-trust mode. Derivation rejects any chain containing an unauthenticated entry; this is how a direct push to the ledger ref is detected.
2. **Admission by quorum.** After each append, Admission sends an authenticated checkpoint `(ledger id, position, head)` to every witness. The entry is admitted when `q_a` witnesses have acknowledged durable retention (§15.3). Witnesses retain every checkpoint they receive, append-only per ledger id. Any participant may relay an authenticated checkpoint it has seen to further witnesses (read repair); relaying can complete a quorum but cannot forge one.
3. **High-water marks.** Every participant that presents current state (Admission, Dispatcher, Interface hosts, clones) keeps the last head it qualified, in private operator state.
4. **Qualification.** An evaluator with authoritative-replica head `A` and high-water mark `W` collects checkpoint sets from at least `r` witnesses, then classifies:
   - `FORK` — two observed checkpoints, or `A` and an observed checkpoint, lie on conflicting chains, with no authenticated human-gated resolution record in `A`'s chain naming the abandoned side;
   - `ROLLBACK` — `A` is a strict ancestor of an observed checkpoint or of `W`, with no authenticated abandonment record (`LEDGER_LOSS`, fork resolution) naming it. For a non-authoritative copy that can fetch the missing suffix from a replica, the state is `BEHIND`: fetch, then re-qualify;
   - otherwise, the **qualified head** `H*` is the highest entry of `A`'s chain that the evaluator observes held by `q_a` witnesses (after read repair if needed) and that extends every observed checkpoint and `W`. `A` is either `H*` or `H*`'s single provisional successor, which is labeled `PROVISIONAL` and never presented as current;
   - `UNQUALIFIED` — fewer than `r` witnesses respond, or no head can be confirmed at `q_a`. Only historical views are available, no current assertion is made, and Admission does not append.
5. **Use.** Every current-state answer, task brief, readiness decision for dispatch, snapshot export, external consultation and publication is bound to a named `H*`. Admission's own validation uses the head it holds by compare-and-swap, which is admitted by construction (§15.3). Every other participant's assertion is "current as of `H*`". Nothing irreversible depends on a non-Admission participant's notion of currency: results are revalidated at Admission (K4).

**Why the contract is sound, and where information runs out.**

- *Every admitted head is seen.* An admitted head is held by `q_a` witnesses. Any `r` responses include more than `f` of them, so at least one honest holder. Every qualifying evaluator therefore observes every admitted head, and an older prefix cannot qualify. This is what defeats the Review's L99/L100 world: if L100 was admitted, a fresh clone that sees replica head L99 also sees the L100 checkpoint and reports `ROLLBACK`; if L100 was not admitted, L99 *is* the current head and saying so is true.
- *An unadmitted entry was never relied on.* No effect, publication, dispatch or answer depended on an entry that never reached `q_a`.
- *The limit.* If every copy and every checkpoint of such an entry disappears, nothing distinguishes it from never having been appended, and no architecture can infer it. SSDS needs no such inference, because it never granted that entry currentness; its request is resubmitted by identity.
- *A partial trace.* If a sub-quorum checkpoint of a vanished entry survives, evaluators that see it report `FORK` or `ROLLBACK` and fail closed until a human-gated record names it abandoned. Since the entry was never admitted, abandoning it loses no admitted judgment.

The architecture thus aligns the definition of provable currentness with the durable evidence that proves it.

**Distinctions.**

| Term | Definition | Consequence |
|---|---|---|
| valid historical prefix | an authenticated chain from genesis to some entry | historical views only |
| provisional entry | appended, not yet held by `q_a` witnesses; at most one exists | never current; completed or resubmitted |
| admitted (qualified) head `H*` | §15.4 rule 4 | the only input to current assertions |
| `BEHIND` | a non-authoritative copy lacking a fetchable admitted suffix | fetch, then re-qualify |
| `ROLLBACK` | the authoritative head is a strict ancestor of an observed checkpoint or high-water mark, with no abandonment record | fail closed; restore |
| `FORK` | conflicting authenticated chains or checkpoints from one genesis | fail closed; human-gated fork resolution naming the abandoned head; never auto-merged |
| loss | admitted entries unavailable from every replica | human-gated `LEDGER_LOSS`; lost judgments become obligations; lost structural admissions surface as quarantine |
| abandoned provisional | a sub-quorum checkpoint whose entry survives nowhere | human-gated abandonment; nothing admitted is lost |
| `UNQUALIFIED` | no read quorum, or no head confirmable at `q_a` | historical views only; Admission halted |
| retired lineage | the old lineage's witnesses hold a retirement statement naming a successor (§15.5) | historical views only, from any mirror |
| recovery | restoring a replica whose chain qualifies; redesignating the authoritative replica by a human-gated lifecycle record | resume |

**Witness lifecycle.** The witness set and quorums are declared in genesis and change only through a human-gated `WITNESS_SET_REDESIGNATION` lifecycle record. Where the old quorum is reachable, the record is admitted under both the old and the new quorum. Where it is not, the human gate gathers every reachable checkpoint and high-water mark and names the head the new set continues from. That record is the explicit acknowledgment that an admitted entry known only to permanently lost witnesses and lost replicas is declared lost, in the same way as `LEDGER_LOSS`. Witness admission latency sits on the Admission critical path; it is a reopen trigger (§26), not a reason to restore a lag window.

A project fork is different: an intentional lifecycle record creates a new project identity (§13).

### 15.5 Privacy and confidentiality

**Prevention.**

1. **Closed, reference-oriented schema.** Ledger fields are identifiers with declared grammars, enumerations, content hashes, integers, recorded observation times, validated repository-relative paths, and content-identity references. There are no free-text fields. Reasons are enumerated codes. Rationale and reports are referenced by content identity: they live in repository content under ordinary hygiene, or in a private store.
2. **Bounded Admission checks.** Grammar validation, known-credential patterns and high-entropy detection over every string-valued field. Where policy enables it, the same scan runs over the candidate diff. A hit rejects the request with a reason code. These checks are preventive help, not a confidentiality guarantee.
3. **Operator secrets** (signing keys, tokens, prompts, transcripts, account telemetry) live only in private operator state.
4. **Visibility separation.** When governance records must be more private than the product, genesis places the ledger in a dedicated private repository; semantics are unchanged (§15.3).

**Breach protocol.** This applies when a sensitive value is found in a replicated ledger entry, or in product content that the ledger pins.

1. Treat it as a human-gated security incident under the security owner; halt Admission for the affected ledger.
2. **Rotate or revoke** every exposed credential immediately. For credentials, rotation is the remedy that restores security, and it does not wait for any purge.
3. **Inventory replicas**: authoritative replica, other remotes, clones, mirrors, forks, CI and harness caches, hosting retention and backups. Checkpoints contain hashes only.
4. **Choose remediation by confidentiality need** (human decision):
   - *Rotation suffices* (the value is useless after rotation): keep history; append a `REDACTION_NOTICE`; no guarantee yields.
   - *Confidentiality required:* create a replacement ledger lineage in a new or private repository.
     - **Settle the old head.** Settle any provisional entry of the old lineage first: admit it or record its abandonment. The old lineage then has one last admitted head.
     - **Re-encode.** Re-encode records with the sensitive fields replaced, and map commit identities if product history moves to a new repository; any pseudonym mapping is held privately.
     - **Bind the new genesis.** The replacement's genesis carries a migration record naming the old lineage's last admitted head *hash* (a commitment, not content). Qualify that the replacement derives the same state, effective structure included, up to the renaming.
     - **Retire the old lineage.** Publish an authenticated **retirement statement** for the old ledger id to the old witnesses, naming the successor lineage by hash. It is held by `q_a` of them like a checkpoint, so every read quorum observes it. Evaluators that observe it treat the old lineage as historical only. A stale mirror, an old clone or a restored backup paired with the old witnesses therefore cannot present the purged lineage as current, even though its chain still qualifies cryptographically. Retire participants' high-water marks for the old lineage.
     - **Purge.** Purge the old ledger ref and objects on every controlled replica; this is a destructive history operation and needs explicit operation-specific authorization (G5). Declare old clones and mirrors invalid for SSDS use. Request host garbage collection and backup purge.
     - **Protected `main`.** If the value sits in product history on a protected `main`, SSDP 6.6 forbids discarding `main`'s reachable history. Confidentiality then requires a new repository, with the old one archived or access-restricted, never an in-place rewrite. Effective structure is ledger-derived, so moving product history does not move governance structure. The new repository's declarations are compared with the re-encoded `Σ` like any observed tree.
     - **Publish last.** Per FF-001, the replacement lineage is not published until it validates.
5. **Disclose what yields**, in the incident record:
   - append-only continuity: the old lineage is abandoned or purged;
   - reproducibility of the affected records: only their hashes, and the private mapping, survive;
   - checkpoint continuity: the replacement lineage starts new checkpoints; old checkpoints and the retirement statement remain only as commitments (witnesses never held content);
   - confidentiality of copies outside controlled replicas: it cannot be guaranteed.

A new logical lineage alone never removes leaked data, and SSDS never claims it does.

### 15.6 Actors and authentication

Agents are not principals with authority. Their records are proposals attributed to an execution identity (harness, route, model, task, attempt) observed by the Dispatcher. Humans are authenticated through a trust mechanism declared in genesis and changeable only by a human-gated lifecycle record — for example signed records with registered keys, or an explicitly declared single-user local trust. Admission keys are trust roots of the same kind. No guarantee beyond the implemented mechanism is claimed.

### 15.7 Protected surfaces and untrusted input

Agents cannot modify the ledger, rules registry, project policy, schemas, trust roots, witness configuration, unit governance state or issued task envelopes. Agents may propose structural declarations in the unit manifest as ordinary content; those take effect only through Admission (§6.8 step 4). Changes to rules, policy, schemas, trust roots and witnesses are their own governed changes requiring a human gate. Admission detects any touch of a protected surface. Agent branches and result envelopes are untrusted until validated. Malformed or adversarial records cannot inject actions, and agent-reported test results are never admissible evidence (§10). Unknown executable or binary content is classified statically and never executed or deserialized to classify it. Paths are repository-contained. Evidence, memory and external text are data.

## 16. Components and ownership

### 16.1 Components

| Component | Owns | Never does |
|---|---|---|
| Content Model | parsing observed declarations (manifest, anchors, semantic declarations), resolving effective scopes against observed bytes, authored relation extraction, revisions and scope identities | store status; decide which structure is effective |
| Analyzers | derived relations and their incompleteness/completeness declarations | claim completeness they do not have |
| Ledger Store | ledger persistence, authentication and hash-chain verification, currentness qualification (read quorum, read repair, high-water marks, `FORK`/`ROLLBACK`/`BEHIND`/`UNQUALIFIED`), replica restore | interpret records; present a provisional or unqualified head as current |
| Derivation Engine | the four strata and every query over them, including the effective-structure fold, quarantine, tenure and well-formedness in S0 (§6.6) | write canonical state; choose which prefix is current |
| Admission | validation (including structural deltas and adoption), the only ledger appends, admission by witness quorum (checkpoint distribution), and canonical publication effects (integration ref) | judge semantics; perform agent work; publish or report before admission |
| Dispatcher | scheduling among obligations ready at the qualified head (resource/account/model feasibility, route selection, reservations), workspaces, harness adapters, execution effects including trusted-runner evidence, operator journal | decide readiness or completion; act as a second admission; move canonical refs; dispatch from a provisional head |
| Interface | logical operations, transports, version-bound brief and gate rendering | hold state of its own |

Dependency direction: Content Model and Analyzers <- Derivation <- {Admission, Interface, Dispatcher}; Ledger Store is read by Derivation and written only by Admission. Ledger Store qualification is consulted by Admission, Interface and Dispatcher before anything is presented as current; Derivation itself never consults witnesses. No component was added for the three revision-3 separations: effective structure and well-formedness are S0 derivation, quarantine is S0/S3 derivation plus an intake judgment, and quorum admission is Admission's existing checkpoint effect plus Ledger Store's existing verification. The Dispatcher submits trusted-runner realizations and execution outcomes through Admission. Scheduling decisions never influence derived workflow state. The route, harness, model and attempt provenance they produce travels in submitted records and is replayed as recorded fact, never recomputed against current resources.

### 16.2 Transfer of frozen Orchestrator Architecture 1.6.0

Architecture 1.6.0 (`orchestrator/docs/architecture.md`, frozen) is superseded **for SSDS-governed scopes only**, and only when the accepted Architecture Manual performs the supersession explicitly. It is not layered beneath SSDS. For version-bound older work, the implemented Level 0 Core keeps its accepted behavior (PC-001): one composition root, version/profile-separated source resolution, frozen historical profiles, versioned JSON records, no cross-version source substitution. SSDS does not make Core's standalone acceptance depend on SSDS. The Tracker, Adapter and Scheduler levels were never implemented, so no Level 1-3 data needs migration.

Classification: **Preserved** (binding on SSDS with unchanged meaning); **Replaced** (by the named mechanism, equal or stronger); **Retired** (with rationale); **Deferred** (to the Architecture Manual with the stated closure requirement).

| # | 1.6.0 product invariant | Disposition |
|---|---|---|
| 1 | Progressive usefulness; Core alone complete | **Replaced** for native scopes by staged usefulness: read-only derivation and interface are useful without Admission (§23); document-only operation is not complete for native scopes (§24). **Preserved** for version-bound older work through Core prompt mode |
| 2 | `core <- tracker <- adapters <- scheduler`, no reverse/lateral dependencies | **Retired** (the four-level ladder) with the ladder itself; **Replaced** by the acyclic SSDS component dependency order (§16.1). f9d9de8 wrongly listed this as preserved |
| 3 | Graceful degradation without silent policy bypass | **Replaced**: degradation is truthful non-closure plus read-only derivation, labeled `UNQUALIFIED` or historical when currentness cannot be established (§15.4, §24); the no-silent-bypass clause is **Preserved** |
| 4 | One CLI and one composition root; extensions via versioned SPIs | **Preserved** as a principle (one composition root per installation); **Deferred**: the Manual decides whether SSDS reuses the `sdp` CLI/Core root or defines a successor, and must not produce two roots for one installation |
| 5 | Versioned public boundaries (`api.vN`/`spi.vN`) | **Preserved** |
| 6 | No duplicated workflow authority; Tracker is evidence | **Replaced**: ledger + Admission is the single workflow authority for native scopes; workplans and profiles stop owning transitions there and keep them for `LEGACY(p)` |
| 7 | Manual operation is first-class | **Replaced** in part: manual agent invocation and the Git-envelope route stay first-class (§9.5), and manual results enter by admission; manual document control is not complete for native scopes |
| 8 | Capability recommendation precedes resource scheduling (Adapter/Scheduler split) | **Retired** as a module boundary; both functions consolidate in the Dispatcher. **Preserved** substance: recommendation evidence never acts as quota/resource authority |
| 9 | Benchmark observations preserve context | **Preserved** for Dispatcher route recommendation; **Deferred**: exact fields to the Manual. Never derived workflow state |
| 10 | Scheduler subordinate to workflow intent | **Preserved and strengthened**: the Dispatcher acts only on derived-ready obligations and cannot affect derived state |
| 11 | Private state outside project repositories | **Replaced** in part: operator state stays private; the closed-schema ledger lives in a Git repository designated at genesis, which may be private (§15) |
| 12 | Subset acceptance is permanent | **Preserved** for Core (SSDS never makes Core acceptance depend on it); **Retired** as a ladder rule for SSDS components, which are accepted as one system (§25) |
| 13 | Stable IDs cross modules, implementation objects do not | **Preserved** across SSDS components |
| 14 | Read-only query and durable mutation are visibly distinct | **Preserved**: `ask`/`read` and Derivation are pure; Admission alone mutates canonical state |
| 15 | Long-running execution is explicit (admit, start, events, control, cancel, result) | **Preserved** as the Dispatcher harness-adapter contract; **Deferred**: lifecycle detail to the Manual |
| 16 | Manual and direct routes share one route vocabulary | **Preserved** (§9.5) |
| 17 | Capability identity independent of API version | **Preserved**; **Deferred**: capability keys for transports/adapters to the Manual |
| 18 | Explicit route choice is not a resource-admission bypass | **Preserved** in the Dispatcher ("resource admission" there is distinct from SSDS Admission) |
| 19 | Route admission precedes final prompt rendering | **Preserved**: the Dispatcher selects the route before route-specific brief rendering (privacy exposure differs by route) |
| 20 | Run identity precedes scheduling and rendering | **Preserved**: task and attempt identity precede dispatch and travel in submitted records |
| 21 | Manual result tracking has a structured seam | **Replaced and strengthened** by the typed admission request (§6.8) |
| 22 | Protocol version binding is explicit | **Preserved** (S7, B1, §24) |
| 23 | One mutating run owns one local worktree | **Preserved** (K2) |
| 24 | Workflow routing authority is profile-owned | **Replaced** by the rules registry for native scopes; profiles remain for version-bound rendering |
| 25 | Uncertain routing remains uncertain | **Preserved**: ambiguity and unknown outcomes surface as explicit S3 states or fail closed (C5); no guessed transition |
| 26 | Orchestrator code contained under `orchestrator/` | **Preserved** as the default; **Deferred**: the Manual may change containment only by explicit supersession declaring one SSDS containment root. f9d9de8 listed this as unconditionally preserved |

| 1.6.0 frozen surface | Disposition |
|---|---|
| §3 capability ladder and distributions | **Retired** for SSDS scopes; Level 0 Core **Preserved** for version-bound work |
| §5 public API standard (compatibility, records, pagination, problems/errors, idempotency, sync/async, two-stage freeze) | **Deferred**: the Manual adopts or explicitly supersedes each sub-rule for the Interface and component boundaries |
| §6 Core composition SPI | **Preserved** for Core; **Deferred** with invariant 4 |
| §7 Core shared records (IDs, DigestRef, ProtocolProfileRef, WorkplanRef, CandidateRef, ProjectDescriptor, EventEnvelope, StageResultEnvelope) | **Preserved** for Core; **Deferred**: the Manual maps CandidateRef/StageResultEnvelope onto the admission request, or explicitly declines reuse |
| §8 Core/Prompt module | **Preserved** for version-bound work |
| §9 Tracker; §10 Adapters; §11 Scheduler | **Retired** as modules (never implemented); their functions are replaced by Ledger/Derivation (Tracker history/projection) and the Dispatcher (routes, execution, benchmarks, metering, reservations, prediction, failover), with detail **Deferred** to the Manual |
| §12 configuration ownership; secrets as references | **Preserved** principle (one config owner; secrets never in snapshots/history); **Deferred**: SSDS configuration layout |
| §13 persistence/event ownership | **Replaced** by §15 stores; "persisted state is not repository authority" is **Retired** for native scopes, where the ledger is authority |
| §15 failure/degradation | **Replaced** by §13 and §24 |
| §16 security/privacy (untrusted pasted output, no tokens in prompts/caches/repositories, no local paths or telemetry in web context, no transcript auto-injection, restrictive permissions) | **Preserved** (§15.5-§15.7) |
| §17 benchmark integrity | **Preserved** for Dispatcher recommendation |
| §18 executable architecture fitness | **Deferred**: the Manual defines static dependency-direction checks for SSDS components |
| §19-§20 module acceptance ladder and module-workplan derivation | **Retired**; **Replaced** by §23 phases and Manual-derived D4 workplans |
| §21 versioning/evolution | **Preserved** principle; SSDS versions are distinct per §24 |
| §22 active simplicity/reopen triggers | **Preserved** where applicable (separate mutable workflow authority, duplicated resolution, hidden preview writes, private objects in public API, process execution outside its owner) |

## 17. Mechanisms deliberately removed

| Removed | Replaced by |
|---|---|
| AuthorityGraph, WorkGraph, CodeGraph, EvidenceGraph as canonical families | units + authored/derived/proposed relations; graphs are views |
| AuthorityEpoch | per-record basis |
| Whole-plan PlanRevision freeze, planning/working phases, global replanning stop | item-level plan revisions, plan acceptance judgments, scoped amendment |
| Freeze frontier as a concept | readiness rule over validity |
| Event-sourced control state and stored lifecycle FSMs | immutable ledger of judgments/observations/admissions; stratified pure derivation |
| WorkGraph node kinds (barrier, router, integration gate, review/qualification gate) | obligations typed by required judgment kind and actor qualification |
| WorkClaims as safety mechanism | optimistic admission; advisory footprints; declared serialization surfaces |
| GraphTransaction, candidate overlay, GraphDelta, DIRTY marking | Git candidate + derivation keyed by content; diffs derived on demand |
| Context Resolver and Semantic Projection Layer as components | derivation queries + interface templates |
| Project Ingestion and Reconciliation Engine (four modes) | intake rules over changes with unknown basis |
| LegacyAggregate | coarse `OPAQUE` subjects; structural refinement; qualified promotion |
| "UNKNOWN_BUT_ACTIVE is invalid" | total coverage with explicit `UNCLASSIFIED` status and restricted use |
| Graph history/diff subsystem | derived diff between two ledger positions |
| Mandatory refactor of D1-D3 into per-node documents | adaptive unit granularity, inline or manifest declaration |
| Seventeen MCP operations | six logical operations, transport-neutral |
| f9d9de8: `Change` as a primitive | typed admission request; identity in the admission record |
| f9d9de8: acceptance carried to refined children by rule | parts route to the unchanged subject; promotion by qualified acceptance |
| f9d9de8: same-repository multi-ref atomicity | single-ref append; reconciled publication |
| f9d9de8: derived `acc(policy)` feeding derivation | ruleset named by adoption record |
| 441cf5c: any relation cycle licensed by a common subject; one composite construct for refinement parents and simultaneous definitions | relation roles and cycle classes; SDG as semantic declaration; cycle legality in Admission and S0 (§6.2) |
| 441cf5c: structural declarations effective on repository presence (including absorbed foreign ones) | effective structure as a fold of admitted changes; quarantine in S0; tenure-scoped acceptance (§6.1, §11) |
| 441cf5c: append as commit point; bounded-lag anchoring mode; optional multi-ref publication in one transaction | provisional append, admission by witness quorum with read/write intersection; publication after admission (§15.3-§15.4) |

## 18. Inheritance and capability transfer

### 18.1 Consolidated Protocol 8 plan

Every section of `workplans/archive/SSDP-8.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-CONSOLIDATED.md` is disposed below. That plan itself carried these archived records (`workplans/archive/<id>.md`) as one composition:

1. `SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION`
2. `SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-1-SECOND-REVIEW-CLOSURE`
3. `SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-2-DETERMINISM-AND-RECOVERY-CLOSURE`
4. `SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-3-PROTOCOL-6.2-INHERITANCE-RECONCILIATION`
5. `SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-4-PROTOCOL-6.3-INHERITANCE-RECONCILIATION`
6. `SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-5-PROTOCOL-6.4-INHERITANCE-RECONCILIATION`
7. `SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-6-PROTOCOL-6.5-INHERITANCE-RECONCILIATION`
8. `SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-7-PROTOCOL-6.6-INHERITANCE-AND-D3-REASSESSMENT`
9. `SSDP-8.0-DETERMINISTIC-ORCHESTRATOR-VERSION-REBIND`

Their historical inheritance dispositions (6.2-6.6 reconciled; D3 reopen required; D4 not authorized) remain true and are carried here. "Carried" means binding here with unchanged meaning; "Replaced" means an equal-or-stronger mechanism; "Changed" means a deliberate D3 decision with reason.

| Predecessor | Disposition |
|---|---|
| §1 control plane coordinates and indexes, never reproduces semantics | Carried (§6.3, C7) |
| §2 lossless inheritance of all accepted doctrine incl. 6.2 representation and 6.3 PEM; no mirror registries; inadequacy reopens D3 | Carried (§2, §20) |
| §3.1 deliberate supersession of Architecture 1.6.0; no hidden layer | Carried and made per-invariant (§16.2) |
| §3.2 Protocol 6.6 reassessment input | Carried; this revision is a proposed reassessment, adjudicated only by independent D3 Review (§21) |
| §4 reducer vs Scheduler; scheduling decisions recorded and replayed as facts | Carried and strengthened as Admission/Derivation vs Dispatcher: scheduling cannot affect derived workflow state at all; its provenance is recorded fact (§7.3, §16) |
| §5 planes; §5.4 semantic owner vs control projection, mismatch blocks, classification provenance | Carried and strengthened: authored relations inside content remove one mismatch class; drift detection covers the rest (§6.2, §11) |
| §6 minimal control data; four anti-duplication rules | Carried (§6.3, §12.6) |
| §7 versioned formal schemas, canonical interchange, forward compatibility, fail-closed unknown required semantics | Carried (§6.3, §6.8 step 1), with the schema now closed (§15.5) |
| §8 logical identity vs revision; prefer Git identity; no universal per-claim hash graph without need | Carried; revisions computed from Git content, with scope identity separated (§6.1) |
| §9 typed relations; completeness scoped; absence not independence | Carried and strengthened: relation types carry closed semantic roles and cycle classes; completeness is a boundary judgment in the basis; widening is exact (§6.2, §6.5) |
| §10 evidence formalization without bulk migration | Carried (§10) |
| §11 composed state dimensions | Replaced: S3 derived classifications (§6.6) |
| §12.1 version-bound replay; no silent reinterpretation; explicit migration | Replaced by the derivation property plus never-re-adjudicated admissions (§6.6, §13) |
| §12.2 reducer purity and observation boundary | Carried (§6.6, C3) |
| §12.3 snapshots derived and verified | Carried (§13) |
| §13 seven validation layers; single canonical writer; humans decide meaning, writer serializes | Carried as nine steps (§6.8, §9.4) |
| §14 external effects | Carried (C4, §15.3) |
| §15.1 private canonical store by default; in-repository only by explicit D3 adoption resolving concurrency, privacy, history and ownership | **Changed**: Git-replicated ledger adopted with the four conditions resolved (§15.2-§15.5); operator state stays private |
| §15.2 durability and recovery contract (atomic publication boundary, corruption detection, durable flush, backup/restore, identity mapping, compatibility on restore, retention) | Carried and strengthened (§13, §15.3-§15.5): the atomic publication boundary is quorum admission of a durable append; anti-rollback added as quorum-qualified currentness |
| §16 formal action registry | Replaced by the rules registry of fixed predicate templates (§6.6) |
| §17 schema-valid agent outputs; no prose parsing | Carried (§9.1) |
| §18.1-18.2 TaskEnvelope / ResultEnvelope | Carried: envelope = obligation + basis + brief; result = typed admission request (§6.8, §9) |
| §18.3 candidate identity without self-reference | Carried (§6.8) |
| §18.4 transport artifacts not merged; protected surfaces | Carried (§15.7) |
| §19 agent PASS is not canonical PASS | Carried (§7.4) |
| §20 human gates, risk override, Serious Challenge preservation | Carried and formalized (§6.6 S1, §9.4, §7.4) |
| §21 deterministic impact; materiality by judgment | Carried and made central (§6.4-§6.7) |
| §22 workplans/skills after cutover; lifecycle metadata non-authoritative | Carried (§12.6) |
| §23 minimal activation and bootstrap locator | Carried (§9.5) |
| §24 one logical protocol, multiple transports; polling first | Carried (§9.5) |
| §25 isolation, atomic publication, stale/duplicate/partial results | Carried and strengthened by basis currency and request identity (§6.8, §8.2, §15.3) |
| §26 security | Carried (§15) |
| §27 failure semantics; no implicit document fallback; manual work is non-canonical until admitted | Carried (§12, §24) |
| §28.1 pre-cutover baseline identities from release state; public fallback and recovery distinct | Carried (§24) |
| §28.2 rollback is version rollback; no dual-current control | Carried (§24) |
| §28.3 cutover quiescence: drain, pin or migrate | Carried, per subject (§12.4) |
| §29 migration phases incl. shadow comparison and difference classification | Replaced by §23, classification carried |
| §30 D3 obligations 1-15 | Carried into §21 |
| §31-§32 failure and semantic/adversarial qualification | Carried into §22 |
| §33 versioning and historical preservation | Carried (§24) |
| §34 acceptance criteria | Carried into §25 |
| §35 non-goals | Carried (§20) |
| §37 version rebind, Protocol 7 inputs and reconciliation contract | Carried (§0.2, §19) |

### 18.2 befe678 hypothesis capabilities

| Capability | Where preserved |
|---|---|
| Machine-readable D1-D3 relations with layer direction and SCC handling (condensation of legitimate simultaneous definitions only; circular warrant invalid) | §6.2 roles, cycle classes and SDGs |
| Derived code dependencies with explicit blind spots | §6.6 analyzers, §6.2 |
| Evidence applicability metadata | §10 |
| Typed, non-flattened relation classes | §6.2 |
| Reviewed plans; immutable accepted plan content; no retroactive requirements | §7.2 |
| Modular plans with structure separate from runtime state | §7.1, §12.6 |
| Iteration vs attempt vs plan vs authority revision | §7.3, §6.1 |
| Deterministic, explainable, version-bound context with explicit gaps | §9.2-§9.3 |
| Minimum-semantic-burden interface | §1.2, §9 |
| Safe parallelism and integration checks beyond textual merge | §8 |
| Direct writes allowed in isolated workspaces | §6.8, §11 |
| Incremental maintenance equal to full rebuild | §6.6, §22 |
| Structural history and diffs | §6.6 S3 views |
| Repository explainability, artifact trust, classification, dispositions | §6.1 coverage, §11 |
| Progressive migration, scope conservation, coarse boundary edges, uncertainty | §12 |
| Structural split requires no false semantic claims (lost at f9d9de8, reinstated) | §12.2 |
| Discovery bottom-up, authority top-down | §12.3 |
| Mandatory orchestrator after scope-local cutover, legacy envelopes | §12.1, §12.4 |
| Atomic accepted-event publication, integrity, backup/restore, crash recovery | §15.3-§15.4 (quorum admission), §13 |
| Private control state and secrets kept out of repository transport | §15.1, §15.5 |

## 19. Protocol 7 prospective inputs (not final)

Protocol 7 closure is active, and nothing here binds Protocol 7 semantics or selects an inheritance. The source snapshot is `f96b7cc`. At this revision the Protocol 7 branch had advanced by a Stage 7 probe record (`7d7810f`) without closing. Phase A binds the final identities. Known prospective inputs, and where they would land:

| Input | Landing point | Open question for Phase A |
|---|---|---|
| Gate-evidence adequacy is semantic, not a presence predicate; non-narrative evidence core separable and read first | §9.4 | final gate-brief obligations |
| Realized scientific record and feedback persistence live in existing project artifacts; no universal discovery database | §10 (native artifacts referenced) | whether the ledger may be a project-designated canonical home for findings/tensions, or must only index external homes (the closed schema of §15.5 already forbids narrative content in the ledger) |
| One canonical home per finding; tension binding to authority identity and earlier revisions; native attribution as asserter | §6.3, §11 | mapping of tension search to unit identity, scope identity and refinement lineage |
| Marked product inspectability surfaces accepted by product-scope owner, never by technical D3 Review | §14 | judgment kind and actor qualification |
| Claim-integrity floor on agent assertions | §9 report/submit | none expected at architecture level |
| Stage F fail-closed evidence-state model separating transport success from evidence admissibility (evidence-only lesson) | §9.5, §10 | final portable execution-profile semantics for the Dispatcher |
| Pre-cutover baseline advances to Protocol 7 recovery/public fallback (distinct) | §24 | exact identities from release state |

## 20. Non-goals

SSDS 8.0 does not:

- convert scientific reasoning or evidence into machine JSON, or encode scientific truth in rules;
- provide a general rule or theorem language;
- require a graph database, network database, hosted service or distributed consensus;
- infer independence outside judged-complete scope;
- transfer acceptance by byte identity, scope arithmetic or widening;
- let agents write canonical state, let derived relations override source, or let D4 behavior create accepted D1-D3 authority;
- treat Git branches, commits or PRs as workflow semantics;
- depend on server-negotiated multi-ref atomicity;
- assert currentness for state that a witness quorum does not hold, claim rollback detection beyond the declared witness model, or claim that lineage migration erases leaked data;
- let repository presence, a foreign push, a restore or a merge change effective structure, ruleset or acceptance;
- license a relation cycle by common subject identity, or let a definition or a condensation warrant a claim;
- require every write to pass through an interface;
- expose machine records as routine agent UX;
- use search as an authority resolver;
- execute unknown artifacts to classify them;
- force all-at-once migration, or stop valid production for incomplete migration;
- allow two current authorities or processes over one subject;
- use migration as a hidden redesign channel;
- keep document-controlled workflow as a dual-current fallback for native scopes;
- add webhooks, brokers or hosted services before polling and local operation prove insufficient;
- add registries, wrappers or fields solely to mirror inherited doctrine;
- provide atomic admission across multiple repositories (§11.4 states the supported cross-repository semantics).

## 21. Architecture Manual closure obligations (before D4)

The SSDS 8 Architecture Manual, independently reviewed and accepted, SHALL decide and document:

1. unit model: manifest and anchor declaration syntax (governance-affecting declarations confined to the manifest), content normalization and boundary-marker rules, scope identity, coverage partition and laminarity rules, single-definer rule; effective-structure fold, declaration keys, resolution of effective scopes against observed bytes (`ABSENT`, uncovered region), governance-affecting vs neutral classification algorithm, `aff(Q)`, governance signature and tenure;
2. relation vocabulary with every type's direction, semantic role, cycle class, permitted classes, layer constraint and completeness eligibility; vocabulary adoption checks; SDG declaration syntax and rules; cycle legality and `well_formed`; boundary-completeness judgment semantics and analyzer completeness declarations;
3. closed record schemas, judgment kinds and tiers, actor qualifications, outcome vocabularies, compatibility contract;
4. basis composition and mode assignment per judgment kind, consumption classes, equivalence-path composition, the widening chain and closure algorithm;
5. derivation: strata S0-S3 (including `Σ`, `Q`, `aff`, `τ`, `well_formed` and `ok` in S0), the fixed predicate templates and the adoption-time stratification check, least-fixed-point evaluation, analyzer contract (deterministic vs recorded), derivation checkpoints and recovery-time bounds;
6. Admission validation order including the structural-delta rule (author, realign, carry, adopt), source/destination challenge freeze, dependency well-formedness, request identity and idempotency, merge-queue serial order, single-ref append, quorum admission and the single provisional entry, publication states and effect reconciliation;
7. obligation rules, readiness, three-valued discharge, provisional propagation and risk-override scope, iteration/attempt identity;
8. change-plan structure, plan acceptance, scoped amendment policy, plan invariants;
9. serialization policy surfaces, generated-unit handling, joint invariants, residual-risk disclosure;
10. interface operations, query classes, brief and gate templates, epistemic labels, read recording, transports, bootstrap locator;
11. evidence realization basis fields for scientific regimes, stochastic replicates, environments and precision; trusted-runner designation and custody for expensive external realizations;
12. intake detection, static classification, dispositions, trust/quarantine, structural quarantine views, adoption and realignment requests, policy for mechanical adoption of governance-neutral deltas;
13. governance modes, legacy and external acceptance import scope, external consultation supersession, reconstruction status, structural refinement, subject promotion, demotion and restoration, carve-out, cutover, quiescence, genesis;
14. ledger storage realization: Git entry format, referenced-object retention, durability (fsync) configuration, ledger location options, authentication scheme and key lifecycle, witness kinds, the witness model `(N, q_a, r, f)` and its deployment classes, checkpoint and retirement-statement formats, read repair, the qualification procedure and its states, fresh-clone procedure, replica and witness-set redesignation, confidentiality breach procedure and the closed-schema secret checks; operator-state boundary; derived index;
15. actor identity and human authentication trust roots;
16. protected surfaces and SSDS self-governance of rules, schemas, trust roots and witnesses;
17. component boundaries and dependency direction; Dispatcher/Admission separation; executed supersession of Architecture 1.6.0 resolving every **Deferred** row of §16.2;
18. ruleset/schema evolution and SSDS-to-successor migration;
19. versioning: system, schema, ruleset, interface and profile versions kept distinct;
20. external units, external acceptance import and the cross-repository boundary (§11.4);
21. final Protocol 7 inheritance (§19) and the pre-cutover baseline;
22. a minimum-justified-architecture reassessment against the then-current accepted baseline, including whether every primitive in §5, component in §16.1 and persistent surface in §15.1 is still needed.

## 22. Qualification program

Qualification binds every claim to the property its method can discriminate (DS-001). Synthetic fixtures and model cases establish mechanical properties only; semantic adequacy (promotion, equivalence, completeness, gate adequacy) needs real-owner cases and independent Review. Material persistence and recovery claims use deterministic failpoints with the production owner executing, per the 6.6 storage and concurrency owners. Required, at minimum:

- **Derivation model cases (well-foundedness).**
  - *One input, one state:* property-based generation of admissible ledgers and trees. Derived state is identical across evaluation orders, incremental vs from-scratch evaluation, repeated runs and hosts.
  - *Illegal per-member acceptance:* acceptance judgments on parts are rejected.
  - *Illegal positive recursion:* the f9d9de8 review's four-predicate configuration is rejected at Admission; a fixture-injected ledger evaluates to all-`F` with an integrity obligation, never all-`T`. Mutual validity reliance between subjects in different domains is rejected. An equivalence judgment relying on a consumer of the compared unit is rejected.
  - *Negative/challenge recursion:* a challenge targeting a later record or another challenge is rejected. The chain challenge -> adjudication -> challenge -> adjudication evaluates uniquely. A challenge against a dismissal restores the block. A challenged risk override stops being in force. Demoting, promoting or re-scoping units of a subject with an unresolved blocking challenge (including an overridden one) or a revoked revision is rejected, at the source and at the destination subject.
  - *Supersession:* a superseded acceptance stays non-current after its superseder goes stale.
  - *Risk override:* `BLOCKED` becomes `PROVISIONAL`; `P` propagates; discharge outside the override scope stays `OPEN`; no unqualified closure.
  - *Ruleset:* a ruleset whose parameters make a lower stratum read a higher one is rejected at adoption. An unadopted policy edit has no effect. Historical views reproduce under the ruleset in force at their position.
- **Relation-cycle legality (441cf5c Blocker A).** Each case runs at Admission (authored) and as an injected absorbed tree (S0 `well_formed`, S2 `ok`):
  - *Valid simultaneous recursive definition:* parts `a`, `b` of subject `G` with `a USES_DEFINITION b`, `b USES_DEFINITION a`, inside a declared SDG `{a, b}`. Admitted; `G` is accepted once; both are valid through `G`; an edit to either, or removal of the SDG declaration, changes `G`'s revision and invalidates both.
  - *Same-subject circular `DERIVED_FROM`:* `a DERIVED_FROM b`, `b DERIVED_FROM a` inside one subject, with or without an SDG. Rejected; when absorbed, `G` is ill-formed and invalid, even though the S2 support graph is acyclic.
  - *Same-subject circular `DEPENDS_ON`:* the same, for `DEPENDS_ON`. Rejected or ill-formed.
  - *Mixed SCC:* `a USES_DEFINITION b`, `b DERIVED_FROM a` inside an SDG. Rejected: the cycle contains an `ACYCLIC`-class edge.
  - *Unknown future type:* a cycle through a type absent from `ρ_n` (and the same type outside any cycle). Rejected at Admission; ill-formed when absorbed; becomes legal only after a ruleset adoption defines its role and cycle class, and then only per that class.
  - *Undeclared simultaneity:* the valid case without the SDG declaration is rejected; the SDG declaration alone, without acceptance of the new revision, validates nothing.
  - *Nested and sibling groups:* nested SDGs with a cycle spanning inner and outer members are legal; a cycle spanning two sibling SDGs is illegal until an enclosing SDG is declared; overlapping (non-laminar) SDGs are rejected.
  - *Group boundaries:* an SDG whose members have different subjects, or that contains a subject, is rejected; promotion of one SDG member alone is rejected; promotion of all members as one composite whose scope contains the declaration is admissible with acceptance.
  - *Code recursion stays legal:* mutually importing modules and recursive calls (derived `STRUCTURAL`, `NEUTRAL`) are admitted, carry no warrant, and are traversed by widening.
  - *Self-relation:* any self-relation is rejected.
  - *Condensation carries no warrant:* a claim inside an SDG with no `ACYCLIC`-class warrant leaving the SDG is reported unwarranted by the brief, and the SDG's acceptance remains the only acceptance.
  - *Ruleset reclassification:* a new ruleset that reclassifies an admitted `SIMULTANEOUS` type to `ACYCLIC` makes the affected subjects ill-formed (S2 `F`) without re-adjudicating history; historical views at earlier positions are unchanged.
  - *Vocabulary adoption:* a ruleset declaring a `SIMULTANEOUS` warrant type, an authored `NEUTRAL` type, a type missing an attribute, or a rule naming a `NEUTRAL` type in validity mode, is rejected at adoption.
- **Structural intake and tenure (441cf5c Blocker B).** Each foreign case is a structural-only change (bytes and semantic declarations unchanged, so no revision changes) absorbed from the integration ref, then dispositioned. In every case the foreign tree stays buildable, the quarantined delta is visible beside its effective value, and no S0 input to S2 changes by presence.
  - **Required counterexample.** (1) `A` accepted as subject at `R` (`j_A`, tenure `τ1`). (2) `A` lawfully demoted into part of composite `P` (tenure `τ1` ends). (3) `P` accepted. (4) `P` receives an unresolved blocking challenge. (5) A foreign structural-only change declares `A` a subject again. Expected: `Σ` unchanged, so `subj(A) = P` and validity reliance on `A` is `F` through blocked `P`; `P` is in `aff(Q)` (it contains `A`), so it stays `F` even after its challenge is dismissed, until the delta is dispositioned; `j_A` is not in any `ACC`; adoption of the delta is rejected while `P`'s challenge is unresolved. (6) After the challenge is dismissed, adoption without a new acceptance is rejected; adoption with a qualified acceptance in the same request starts tenure `τ2`, and only that judgment counts. (7) Variant: `P` under risk override instead of open challenge; result stays at most `P`, never `T`. (8) Variant: a later challenge upholding against `A`'s triple `(A, S, R)` revokes it in `τ2` as well.
  - *Part to subject:* quarantined; `aff` invalid; adoption is a promotion with acceptance.
  - *Subject to part:* quarantined; the subject keeps effective status but is invalid while affected (`aff`); adoption ends its tenure.
  - *Composite membership mutation:* moving a unit between composites, into a subject of another governance mode, or into a challenged subject, is quarantined; adoption follows mode-transition and destination-freeze rules.
  - *Partition boundary mutation:* a cross-subject boundary move changes subject bytes and also quarantines the declaration; an intra-subject re-partition is governance-neutral, leaves validity unchanged and may be adopted mechanically where policy permits.
  - *Kind or domain reclassification* of a unit, and *governed-content boundary* (ignore) changes: quarantined and governance-affecting.
  - *Challenge-bearing subject reparenting:* a challenged subject declared a part of an unchallenged composite: quarantined; adoption rejected while the challenge is unresolved; the challenge remains on its triple.
  - *Destination freeze (ordinary Admission):* re-scoping a challenged composite by adding or removing members is rejected.
  - *Restoration after repository rewind or manual conflict resolution:* the integration ref is force-moved to an older commit, or a manual merge resolves manifest conflicts arbitrarily. Old declarations are quarantined; no tenure restarts; no old acceptance revives; realignment by an ordinary change clears the quarantine.
  - *Ledger truncation:* after `LEDGER_LOSS` drops the admission that demoted `A`, the repository still declares `A` a part, so the difference is quarantined and `A` is invalid until dispositioned; `j_A` never silently revives.
  - *Lawful demotion then restoration without foreign change:* the restoring request must carry a new acceptance; `j_A` from `τ1` never counts; prior evidence counts only where its bases are current.
  - *Ruleset evolution during quarantine:* adopting a new ruleset leaves `Σ` and `Q` unchanged; the later adoption of the delta is validated under the ruleset then in force.
  - *Overtaken admission:* an `OVERTAKEN` structural admission shows as quarantine against the absorbed tree until the revalidated request publishes.
  - *Deleted manifest:* a foreign deletion of the unit manifest quarantines every declaration; effective scopes still resolve from `Σ`; governance is invalid until realignment; production is unaffected.
- **Determinism and replay.** Independence from wall clock and live external state; checkpoint corruption detected and rebuilt; schema evolution fixtures; historical admissions never re-adjudicated.
- **Currency.** Upstream change makes exactly the reliant records non-current. Re-review without content change backdates descendants that did not see the upstream text. Equivalence judgments scope correctly by consumption class. A falsified completeness judgment invalidates every inference that used it. Drift blocks dependent use.
- **Conservative widening.** The scope chain is deterministic. Boundary completeness at the smallest qualifying scope is used. With no judgment anywhere, the result is the whole tree, flagged `UNBOUNDED`. Adding or editing a member of a judged scope makes the judgment non-current. The closure is independent of traversal order. A widened basis never makes a part valid.
- **Admission and concurrency.**
  - Disjoint bases admit concurrently; intersecting bases revalidate.
  - Write-skew across disjoint files is caught through recorded reliance.
  - A clean Git merge with a semantic conflict is blocked.
  - Stale, duplicate (same request identity), partial and very late results are handled.
  - Unauthorized protected-surface edits and agent-modified envelopes are rejected.
  - A duplicate discharge is rejected.
  - A D4 change that breaks another closure on the merged tree is rejected, while an accepted upstream authority change legitimately reopens dependents.
  - Live-ref movement is absorbed as drift without blocking production.
  - A self-declared equivalence backdates nothing.
  - Concurrent Admission hosts: the compare-and-swap loser revalidates.
- **Admission, publication and crash windows** (deterministic failpoints; production owner executing):
  - *clean synchronous admission:* append, `q_a` acknowledgments, `ADMITTED` response, publication `PUBLISHED`; no answer, dispatch or publication observed between append and admission;
  - crash before the ledger append (nothing happened; request retried idempotently);
  - *crash before admission:* the provisional entry survives locally; restart completes checkpoint distribution; no publication, dispatch or `ADMITTED` response occurred before;
  - *crash after admission:* restart finds `q_a` checkpoints, proceeds to publication;
  - *append survives locally but witness admission fails:* the entry stays `PROVISIONAL`; Admission halts further appends; current answers stay at the previous qualified head; when witnesses return, admission completes; on permanent loss, witness-set redesignation settles the prefix;
  - *admitted but publication lost:* `PENDING`, then `PUBLISHED`;
  - crash after the compare-and-swap, before the outcome is recorded (observed as `PUBLISHED`);
  - foreign push between admission and the compare-and-swap (`OVERTAKEN`: absorbed, request revalidated, foreign work never overwritten);
  - force-push of the integration ref in the window (`OVERTAKEN`);
  - integration host unreachable (fail closed; production continues);
  - an external merge producing a different commit with the admitted tree (`PUBLISHED`);
  - no configuration publishes a provisional entry (the multi-ref optimization is absent).
- **Currentness qualification and recovery** (witness model `(N, q_a, r, f)` with `q_a + r > N + f`, exercised at least with `N = 3, q_a = 2, r = 2, f = 0` and the local-trust instance):
  - *Review's L99/L100 world:* L100 admitted, then every replica rewound to L99 and every high-water mark lost. A fresh clone reaching any read quorum observes the L100 checkpoint and reports `ROLLBACK`; L99 is never presented as current.
  - *Total loss of an unadmitted newest entry:* L100 appended, no checkpoint reached any witness, every copy lost. Qualified head is L99, which is true; L100's request is resubmitted by identity; nothing had depended on L100.
  - *Sub-quorum trace:* L100 reached one witness only, then every copy was lost. Evaluators that see the checkpoint report `FORK`/loss and fail closed until a human-gated abandonment names it; no admitted judgment is lost.
  - *Fresh clone from a valid historical prefix:* `BEHIND`, fetch, re-qualify; if the authoritative replica is also behind, `ROLLBACK`.
  - *Forked repository plus witness disagreement:* conflicting authenticated chains, or witnesses holding checkpoints on conflicting chains: `FORK`, fail closed, human-gated resolution, never auto-merged.
  - *Malicious or accidental rewind* of the authoritative ref, including with a compromised push credential: `ROLLBACK` from any read quorum.
  - *Witness loss below read quorum:* `UNQUALIFIED`; no current assertion; Admission halted; production continues; read repair completes a quorum when enough witnesses return.
  - *Faulty witnesses within the bound:* `f` witnesses rolled back or withholding checkpoints cannot hide an admitted head; with `f + 1`, the declared limit is reached and documented, never silently exceeded.
  - *Restoration from a backup older than the admitted head:* `ROLLBACK`; restore from any replica holding the suffix; otherwise human-gated `LEDGER_LOSS`, lost judgments become obligations, lost structural admissions surface as quarantine.
  - Two authenticated chains: `FORK`, fail closed.
  - An unauthenticated entry pushed directly is rejected.
  - Authoritative replica lost: restored from a clone extending the highest observed checkpoint.
  - Content objects missing: `UNAVAILABLE`.
  - Snapshots and derived checkpoints at a provisional position are never served as current; answers always name their qualified head.
  - External consultation of another SSDS ledger qualifies its head; an unqualified or retired external head is never imported.
- **Confidentiality.**
  - A credential-like or high-entropy value in a record field is rejected at Admission.
  - A fixture-forced sensitive value runs the incident drill: a provisional entry settled first; rotation recorded; replacement lineage derives the same state, effective structure included, up to renaming; old-lineage retirement statement published, so a stale mirror plus the old witnesses yields only historical views; old-lineage high-water marks retired; yielded guarantees recorded.
  - Restoration of a backup containing the purged lineage presents it as retired, never current.
  - A sensitive value in `main` history is routed to a new repository, never an in-place rewrite.
- **Effects and dispatch.** Crash after intent before start; after start before outcome; scheduler decisions replayed as facts; Dispatcher cannot discharge or ready anything; unavailable network, Git remote or harness; interrupted harness; cancellation.
- **Interface.** Same brief for same basis. Inclusion reasons and epistemic labels are correct. Incompleteness is surfaced, including part-to-subject routing. Candidate items cannot support closure. A zero-context web agent locates its task from the bootstrap. Local and Git-envelope transports give identical admissions for identical submissions. Verbose or alternative prose cannot change outcomes when structured content is identical.
- **Evidence.** Execution change forces rerun; target change forces reassessment; specification survives concretization replacement; stale passing and stale failing evidence inadmissible; unavailable artifact degrades binding health; transport success without complete evidence cannot enter assessment; agent-reported results never discharge evidence obligations; proxy evidence cannot close the real owner.
- **Intake.** Manual edit, untracked generated file, opaque binary (quarantined, never executed), external branch, authority-like document, agent overstep, foreign manifest edit — each through the one route; unclassified and quarantined content excluded from governing context and evidence by S0/S2 facts, not by S3 obligations.
- **Migration and refinement.**
  - A whole repository can start as a single opaque subject.
  - Byte-preserving structural refinement of accepted `P` into parts `A`, `B`: `P`'s revision and validity are unchanged; no acceptance record is created for `A` or `B`; validity reliance on `A` routes to `P`; content reliance on `A` survives an edit to `B`; validity reliance on `A` does not survive it unless a scoped equivalence judgment covers it.
  - **Holistic counterexample (required).** A D2 document `P` states in section `A` "all quantities in Gaussian units unless stated" and gives in section `B` equations without unit annotations. `P` is accepted holistically, and the bytes partition cleanly into `A` and `B`. Expected:
    - after refinement, `B` is a part, not an accepted subject;
    - promotion of `B` by rule, by self-declaration or by widening is rejected;
    - a qualified promotion review either rejects promotion or requires `B USES_DEFINITION A` first;
    - `B`'s promotion basis widens to `A` until completeness is judged.
  - Legacy Case B: a whole-document `LEGACY_ACCEPTANCE` cannot be imported onto a section, and native reliance on a section routes to the document subject.
  - Carve-out cutover: requires promotion plus legacy-owner release; the residual stays valid only while carved-out bytes are unchanged.
  - Coarse relations are redirected only by a new subject revision with acceptance.
  - A version rollback of a cut-over subject to `LEGACY(p)` needs a fresh legacy acceptance import; the pre-cutover import does not revive.
  - Production edits invalidate only intersecting reconstruction.
  - No dual-current mode.
  - Bottom-up proposals never self-accept.
  - Per-subject cutover with drained, pinned or migrated in-flight work.
  - Final disappearance of `OPAQUE`/`UNGOVERNED` material closes migration coverage.
- **Cross-repository.** A pinned external unit never goes stale by external movement; a pin change derives local impact; reliance without external acceptance is provisional; a producer-then-consumer admission sequence leaves visible intermediate states; a consulted external ledger is never written; a later consultation finding the pinned triple no longer accepted supersedes the earlier consultation and makes reliant imports non-current.
- **Semantic and adversarial.** A coherent-D3 D4 defect stays D4. A downstream observation can challenge D3, D2 or D1 and blocks dependent closure. Machinery never auto-resolves scientific ambiguity. A missing required check never becomes PASS. Documents' lifecycle fields enact nothing. Historical reasoning remains reachable. No second authority emerges.
- **Security and privacy.** No secrets or private telemetry in the ledger or repository by default; adversarial records cannot inject actions; human decisions require the declared trust mechanism.
- **Usability.** Live trajectories on real tasks, in shadow mode, showing that agents complete bounded work without reading machine records and with less context than the document-controlled baseline. Claims stay bounded to the trajectories, harnesses and models actually exercised, consistent with the Protocol 6.6 stochastic robustness boundary.
- **Repository acceptance.** The inherited repository workflow (regression, PEM checks, package build/validation, distribution parity, whitespace, frozen-resource integrity, Orchestrator Core snapshot/tests) for every affected surface.

## 23. Development sequence

- **Phase A — Protocol 7 reconsolidation.** After Protocol 7 closes, bind its exact identities and inputs (§19), advance the pre-cutover baseline, and recommend (not self-adopt) a governing-version adoption for this family.
- **Phase B — independent D3 falsification of this architecture.** May begin before Phase A as hypothesis testing; its PASS cannot authorize D4 until Phase A and Phase C close.
- **Phase C — SSDS 8 Architecture Manual** resolving §21, independently reviewed, with explicit stakeholder acceptance of this major change.
- **Phase D — read-only kernel (shadow, no authority).** Content Model, Analyzers, ledger schema and Derivation over this repository, with a shadow genesis from existing history. Value: currency, impact and "what governs" answers with no control change.
- **Phase E — read-only interface.** `open/ask/read` offered to agents working under the document-controlled baseline; measure burden reduction by live trajectories.
- **Phase F — Admission and Dispatcher in shadow.** Compute admission decisions beside document control. Classify every material difference as an SSDS defect, a baseline ambiguity or defect, a deliberate stronger rule, or an unresolved semantic judgment, and independently review each.
- **Phase G — intake and migration pilot.** This repository's legacy documents (Case B) and one external scientific repository (Case C/D) without disturbing production.
- **Phase H — adversarial and fault qualification** (§22).
- **Phase I — scope-local native cutover** after accepted architecture, implementation acceptance, shadow qualification, independent Review, required human/project approval and demonstrated rollback.

## 24. Cutover, rollback and versioning

- The pre-cutover baseline is the accepted document-controlled protocol resolved from `PROTOCOL-RELEASE-STATE.yaml`: currently Protocol 6.6, with recovery `384666764da4c55b282e6b1595ab97e2f86e1dc4` and public fallback `22f4bdba53795da3a6f13f162529f3a843fc37ae`, kept distinct. It advances only by an explicit inheritance reconciliation (Phase A).
- Older version-bound work stays under its declared version and immutable source; every supported orchestration profile stays frozen and independently testable (PC-001); migration never reinterprets old records as authored under SSDS 8.
- Native cutover is per subject; after cutover no document-controlled process governs that subject. Shadow comparison is permitted only while one side is explicitly non-authoritative.
- Orchestrator unavailability yields truthful non-closure for native scopes, never implicit document-control fallback. Exploratory or report-only work may proceed but claims no canonical closure until admitted.
- Rollback is version rollback to the immutable pre-cutover baseline: stop Admission for the affected scope, resume the pinned baseline process there, repair SSDS separately. The mode change ends each affected subject's tenure, so pre-cutover legacy acceptance imports never revive; a fresh import is needed (§12.1). Ledger rollback (§15.4) is an integrity incident, not a version rollback.
- System, schema, ruleset, interface and profile versions are distinct and never conflated with protocol semantic version.

## 25. Acceptance criteria for the architecture cycle

D4 handoff is possible only when:

1. Protocol 7 inheritance is reconciled (Phase A);
2. one accepted Architecture Manual resolves every §21 obligation;
3. exactly one canonical writer exists per ledger, and no document, profile, tracker, scheduler, index or derived view can enact a transition;
4. the four primitives and their derived semantics are fully specified, including subjects, scope identity, effective structure, quarantine and tenure, relation roles and cycle legality, the four strata, currency, validity, three-valued discharge and provisional propagation, with the uniqueness argument of §6.6 independently checked;
5. every §16.2 and §18 inherited guarantee and capability is carried, replaced with equal-or-stronger evidence, retired with accepted reason, or closed by the Manual;
6. concurrency correctness rests on admission-time validation, with residual risk stated;
7. intake is the single route for unknown-provenance change, and migration is coverage refinement plus qualified promotion with per-subject cutover;
8. persistence, quorum admission and currentness qualification, publication, confidentiality recovery and evolution are specified, survive loss of any one machine, and assert currentness only for quorum-witnessed state;
9. the agent interface meets the minimum-semantic-burden invariant, demonstrated by live trajectories in shadow mode;
10. independent D3 Review/Challenge finds no blocker or active governing Serious Challenge;
11. stakeholder acceptance of this major architectural change is explicit.

## 26. Reopen triggers and open uncertainties

Reopen this architecture if:

- conservative widening makes too much work non-current to be useful on real repositories;
- part-to-subject routing makes validity locality too coarse and promotion judgments too frequent to sustain;
- read recording proves infeasible across target harnesses, so bases are systematically too weak;
- unit declaration cost outweighs locality benefit at practical granularity;
- Git-hosted ledgers cannot meet single-ref compare-and-swap, durability, privacy, scale or hosting constraints;
- no practical independent witness set satisfying `q_a + r > N + f` exists for the target deployment class, or witness admission latency on the Admission critical path proves unacceptable;
- structural quarantine produces so much governance invalidity on real repositories (frequent manifest edits, restores, merges) that intake cost outweighs its protection;
- simultaneous-definition groups prove so frequent or large that subjects become too coarse, or real owners need a sound recursive-warrant exception that the closed vocabulary cannot express;
- the confidentiality breach protocol proves operationally unrealizable;
- the fixed predicate templates cannot express a required project policy without breaking stratification;
- Protocol 7 finalizes semantics that require the ledger to be, or forbid it from being, a canonical home for findings;
- live trajectories show agents still doing bookkeeping;
- any inherited guarantee proves unpreservable under §6.

Uncertainties that cannot close by design work alone:

- **Protocol 7 dependent:** gate-brief obligations; finding/tension canonical home; product-surface acceptance actor; final pre-cutover baseline; execution-profile semantics from Stage F portability.
- **Empirical:** rate of false staleness under conservative widening and part-to-subject routing; frequency and cost of promotion judgments in Case B; analyzer completeness for real Python and C++ scientific code; feasibility of read recording per harness; practical unit granularity; derivation cost and checkpoint sizing on large repositories; ledger growth over years; witness availability and admission latency in practice; frequency of structural quarantine and of SDG declarations; agent context and success compared with the document-controlled baseline.

## 27. Adequacy and minimum-architecture passes (rounds 2 and 3)

These passes are design rationale, not evidence of adequacy. The next Review must falsify independently, and nothing here awards a PASS.

### 27.1 Out-of-matrix trajectories

Each attack tried to obey every local rule while violating a governing invariant. The expected response is a repaired abstraction at the earliest owner, not a new test. The table gives the current disposition against design revision 3. The round that exposed each defect is noted.

| Attack | Trajectory attempted | Result (revision 3) |
|---|---|---|
| Authority transfer in migration | byte-preserving split, then reliance on a child as accepted | Blocked by subject routing (§6.1, §12.2); qualification counterexample in §22 |
| Same, via legacy import | import a whole-document legacy acceptance onto a section | Blocked: import scope equals accepted scope (§12.1) |
| Same, via carve-out cutover (round 2) | cut a section over to `NATIVE` while its legacy document's holistic acceptance keeps validating the rest | Repaired in round 2 by frozen subject scope and carve-out rules (§12.2, §12.4) |
| Self-supporting acceptance | mutual validity reliance; equivalence relying on a consumer; member-level judgments in a group | Rejected at Admission; least fixed point is `F` if forced (§6.6) |
| **Circular warrant hidden inside one composite** (round 3, Blocker A) | `DERIVED_FROM`/`DEPENDS_ON`/`SUPERSEDES` cycle among parts of one accepted subject; mixed definitional-plus-warrant cycle inside an SDG; cycle through an unknown type; cycle produced by absorbed content or a ruleset reclassification | **Repaired**: role-based cycle legality at Admission and in S0 `well_formed`, which S2 consumes (§6.2, §6.6). Circular reasoning stated only in prose remains a semantic-review residual |
| Cross-subject warrant cycle with an acyclic unit graph | `x1 CONCRETIZES y1` and `y2 CONSTRAINED_BY x2`, with validity entries both ways | Support cycle; second admission rejected (§6.6) |
| Nested simultaneous-definition groups (round 3) | cycle spanning nested groups; spanning sibling groups; SDG straddling subjects; promoting one member | Nested legal; sibling illegal without an enclosing SDG; straddling rejected; members promoted together only (§6.2, §12.2) |
| Legitimate recursion banned by accident (round 3) | mutually recursive equations; recursive functions; mutually importing modules | Legal: SDG with `USES_DEFINITION`; single-object recursion is unit content; code recursion is `NEUTRAL` derived structure (§6.2) |
| Ruleset self-reference (round 2) | edit policy so derived acceptance of policy changes the rules that derive it | Repaired in round 2 by adoption record (§6.6 S0) |
| Negation inside validity (round 2) | an obligation-existence condition (negative in currency) feeding discharge and back into validity | Repaired in round 2 by S3 placement and Admission step 8 (§7.4) |
| Challenge recursion | challenge chains, counter-challenge to unblock, override under challenge | Well-founded; conservative in both directions (§6.6 S1) |
| Challenge escape by ordinary re-scoping (round 2) | demote a challenged subject into an unchallenged composite, or promote a part out of a challenged one | Repaired in round 2 at the source subject (§6.8 step 4) |
| **Challenge escape at the destination** (round 3) | re-scope a challenged composite by adding or removing members so its challenged triple is no longer current | **Repaired**: the freeze covers every subject whose scope, regions or membership change, before or after (§6.8 step 4(b)) |
| **Structural foreign change under unresolved challenge** (round 3, Blocker B) | foreign structural-only change restores a demoted part as subject while its composite is challenged | **Repaired**: `Σ` unchanged, `aff(Q)` invalid, adoption frozen, tenure excludes the old judgment (§6.1, §11, §12.2); required counterexample in §22 |
| **Old acceptance resurrection after demotion and restoration** (round 3) | lawful demotion, then lawful promotion with the same bytes and scope; or `scope_id`, domain or mode oscillation | **Repaired** by tenure-scoped `ACC` (§6.1, §6.6) |
| **Resurrection through ledger truncation** (round 3, not in the Review) | `LEDGER_LOSS` drops the admission that demoted `A`; `Σ` again says subject | **Repaired** by the observed/effective comparison: the repository still declares the demotion, so `A` is quarantined (§13) |
| **Domain laundering** (round 3, not in the Review) | reclassify a part's owning domain, then promote it so a weaker reviewer accepts it | **Repaired**: a kind or domain change needs a judgment by an actor qualified for the current domain (§6.8 step 4(a), §12.2) |
| Ruleset evolution during quarantined intake | adopt a ruleset while a structural delta is quarantined; reclassify relation types | `Σ` and `Q` unchanged; adoption validated under the ruleset then in force; reclassification makes affected subjects ill-formed with visible impact; history unchanged (§11.2, §6.2, §13) |
| **Vocabulary evolution invalidating accepted content** (round 3, not in the Review) | rename or remove a relation type in a new ruleset | **Repaired**: adoption declares `READ`/`MIGRATE`/`REJECT` for existing uses and shows the derived impact before the gate; legacy relations are proposed and unaffected (§6.2) |
| Incomplete dependency knowledge (round 2) | add a unit to a judged-complete scope with an outside dependency; foreign file added beside a judged scope | Repaired in round 2 (completeness basis includes membership). Quarantined structure never enters the scope chain; uncovered content is reachable only in the `UNBOUNDED` fallback (§6.2, §6.5) |
| Stale evidence reuse after role change (round 3) | after demotion and restoration, reuse assessments from the earlier tenure | Evidence binds to content and execution, not role. It counts only when its bases are current and only under a current-tenure acceptance (§12.2) |
| Stale evidence reuse | merged-tree change in an undeclared execution dependency | Widening via analyzer incompleteness; residual stated (§8.4, §10) |
| Historical profile isolation after schema evolution | new record schema or relation vocabulary while version-bound work continues | Frozen Core profiles untouched (PC-001); `LEGACY(p)` interpreted by `p`; historical views use the ruleset and schema of their position; current derivation fails closed only through declared vocabulary impact (§6.2, §13, §24) |
| **Crash between ledger append and currentness qualification** (round 3, Blocker C) | append L100, crash before any witness holds it | **Repaired**: L100 is provisional; nothing depended on it; anchoring completes on restart, or the request is resubmitted (§15.3) |
| Crash between qualification and publication | admitted, integration CAS not done | `PENDING`, then `PUBLISHED`/`OVERTAKEN` (§15.3) |
| **Stale or rewound canonical state** (round 3, Blocker C) | the Review's L99/L100 world; fresh clone reaching only witnesses lacking the newest checkpoint | **Repaired**: quorum admission plus `q_a + r > N + f`; every admitted head is visible to every qualifying evaluator (§15.4) |
| Witness disagreement | conflicting checkpoints; sub-quorum checkpoint of a vanished entry; relayed old checkpoints | `FORK` until human-gated resolution; relaying an old checkpoint is harmless; relaying can complete a quorum but never forge one (§15.4) |
| Repository restoration from stale backup | product ref and ledger restored to an older state | Product: absorbed, bytes drift, declarations quarantined, `Σ` unaffected. Ledger: `ROLLBACK` from any read quorum (§13) |
| Foreign force-push or manual merge | force-push of the integration ref; manual manifest conflict resolution | Absorbed; foreign work never overwritten; structural deltas quarantined (§11, §15.3) |
| Forged canonical entry (round 2) | direct push of a well-formed entry to the ledger ref | Repaired in round 2 by entry authentication (§15.4) |
| Legacy and native authority simultaneously present | legacy edit to a cut-over section; foreign move of a native unit into a legacy subject; legacy `status:` field | Foreign change and drift; mode-mixing membership needs a mode-transition record; lifecycle fields enact nothing (§12.1, §12.6) |
| Cross-repository imported authority becoming stale | external retraction, fork or rollback after import; external head consulted while provisional | Consultation qualifies the external head; an adverse later consultation supersedes the earlier one and makes reliant imports non-current; unreachability does not flap (§11.4) |
| Purged lineage presented from a stale mirror (round 3, not in the Review) | after a confidentiality lineage migration, a restored backup plus the old witnesses still qualify cryptographically | **Repaired**: retirement statement admitted at the old witnesses (§15.5) |
| Agent proposal or PASS mistaken for authority | agent submits PASS, equivalence about its own change, promotion of a part, a self-declared SDG, a manifest demotion of a challenged subject, or reports a provisional submission as admitted | Proposal only; authorization, freeze and acceptance rules reject; SDGs need acceptance; responses say `PROVISIONAL` until admission; discharge is derived (§6.8, §7.4, §9.1) |

Residuals carried rather than repaired, because no architecture removes them: undeclared semantic dependencies (§8.4); circular reasoning stated only in prose (§6.2); foreign edits that reduce governance validity, but never production, until dispositioned (§11.3); and the information-theoretic limit of §15.4.

### 27.2 Minimum-justified-architecture pass

- **Primitives:** four, unchanged since round 2, when `Change` became an admission request. Round 3 adds none. The SDG is a semantic declaration. Effective structure and tenure are S0 derivations. Provisional versus admitted is a property of a ledger entry decided by witness quorum.
- **Constructs:** round 2 used one composite subject for both refinement parents and simultaneous groups. Round 3 separates them, because the conflation was Blocker A; the separation adds a declaration, not a primitive. One boundary-completeness judgment serves per-unit and per-scope completeness. `acc(·)` is a display view.
- **Paths:** one append, admission and publication semantics for local and remote deployments. The multi-ref publication optimization is removed, so there is one path fewer. Policy acceptance is merged into ruleset adoption, and structural adoption reuses ordinary Admission validation: one rule, "content proposes, admitted records enact", now covers both. Reinstatement reuses the acceptance kind.
- **Persistent surfaces:** none added in round 3. The witness set gains quorum parameters and stores retirement statements. `Σ` lives in the derived index and is rebuilt from the ledger. Each surface has one writer and an explicit recovery path (§15.1).
- **Components:** seven, unchanged. The new responsibilities fall to existing owners: Derivation (S0 facts), Admission (structural validation, quorum admission), Ledger Store (qualification) and Content Model (observed declarations).
- **Rejected additions:**
  - a general rule language;
  - a separate refinement or reinstatement judgment kind;
  - a fourth publication state (provisional is an entry property, and publication never sees it);
  - a merge-and-publish reconciliation path;
  - a cross-repository coordinator;
  - a stored copy of effective structure;
  - automatic, non-human-gated abandonment of sub-quorum checkpoints (rare, and its safety would depend on witness counts that read repair can change);
  - a fifth primitive for simultaneous definition.

## 28. Handoff state

```text
GOVERNING DESIGN PROTOCOL: SSDP 6.6.0
TARGET: SSDS 8.0.0
ARCHITECTURE: basis-stamped judgments over content-addressed units grouped into acceptance subjects;
              stratified pure derivation (S0 observed content and admitted effective structure, S1 challenges,
              S2 least-fixed-point support, S3 consequences); relation roles and cycle classes with
              simultaneous-definition groups; tenure-scoped acceptance; single Admission writer; single-ref append
              admitted by witness quorum; currentness only for quorum-witnessed heads; reconciled publication;
              Git-replicated ledger; optimistic concurrency; one intake route with structural quarantine;
              refinement plus qualified promotion for migration
SOURCE SNAPSHOT: f96b7ccf90dede4150d0efa17264fff07ec12d0d (ssdp-7.0-scientific-epistemic-closure)
DESIGN BASIS: befe6782e7c8fe038bf7cb764646d133ca167855 (befe678 hypothesis archived byte-identically)
PRIOR REVIEWS: f9d9de8 NO-PASS (repaired by revision 2); 441cf5c NO-PASS
               (qualification/ssds80/WORKPLAN-REVIEW-SSDS-8.0-441CF5C-NO-PASS.md); repaired here (§0.1)
THIS WORKPLAN: design revision 3; proposed; not accepted-current; not an Architecture Manual; no self-awarded PASS
SSDP 7: active closure; inheritance NOT FINAL; Stage H retargeting belongs to Protocol 7's own closeout (§0.2)
D3: ready for fresh independent falsification Review; D4 handoff requires Phases A and C
D4: NOT AUTHORIZED
SERIOUS CHALLENGE: none
NEXT ACTION: fresh independent D3 Review of design revision 3 by a context that authored neither it nor its
             predecessors; preserve the branch while Protocol 7 closes; then Phase A.
```
