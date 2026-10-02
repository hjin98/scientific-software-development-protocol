# SSDS 8.0 Prospective Architecture Workplan — Independent D3 Review

```text
GOVERNING SSDP: 6.6.0
REPOSITORY: hjin98/scientific-software-development-protocol
BRANCH: ssds-8.0-graph-native-architecture
CANDIDATE: 441cf5c4cce0428b44c6d3e15db697b0b4f6262c
HEAD AT REVIEW START: 441cf5c4cce0428b44c6d3e15db697b0b4f6262c
HEAD AT FINAL RECHECK: 441cf5c4cce0428b44c6d3e15db697b0b4f6262c
INTERVENING COMMITS: none
PRIMARY WORKPLAN: workplans/active/SSDS-8.0-GRAPH-NATIVE-DETERMINISTIC-ORCHESTRATION-ARCHITECTURE.md
PRIMARY WORKPLAN GIT BLOB: cb967c15aae2d8451e86b67430d9cbb8c6627073
AUTHORITY INDEX GIT BLOB: e6115ad5bfab02f91dd1867a2bf4cd8324832479
CONSOLIDATION TEST GIT BLOB: 798a7d5f6527f37e1e48c02586b9cf3c13fd3e42
PRIOR REVIEW: qualification/ssds80/WORKPLAN-REVIEW-SSDS-8.0-F9D9DE8-NO-PASS.md
REVIEW METHOD: fresh read-only D3 reconstruction and adversarial falsification; prior-review and workplan self-assessments treated only as hypotheses
```

## SERIOUS CHALLENGE

**None.**

The accepted SSDP 6.6 authority reconstructed from the immutable public-source commit named by `PROTOCOL-RELEASE-STATE.yaml` is sufficiently coherent for this decision. The defects below are defects in the prospective SSDS 8 D3 concretization, not demonstrated contradictions or unrealizability in SSDP 6.6 itself.

## Verdict

# **NO-PASS**

Revision 2 materially repairs most of the first review's architecture defects. In particular, exact subject/scope/revision acceptance, the four-stratum derivation, single-ref ledger commit plus reconciled product publication, the confidentiality breach protocol, the explicit Orchestrator 1.6.0 capability-transfer table, structured handoff routing, executable widening algorithm, removal of `Change` as a primitive, and the explicit cross-repository boundary are substantive improvements rather than wording-only repairs.

Three D3 blockers remain:

1. the relation/SCC rule conflates legitimate simultaneous definition with arbitrary same-subject circular warrant;
2. foreign absorption can activate structural declarations in S0 while the promised intake quarantine exists only as an S3 consequence, allowing a structural-only foreign change to alter subject routing before intake closure and, in a legal history, to resurrect an old acceptance through a challenged boundary;
3. the anti-rollback design explicitly permits an undetectable rewind window while simultaneously claiming that a valid historical prefix is never mistaken for the current head.

These are architecture-owner defects. They do not require abandoning the four-primitive/stratified-derivation architecture, but they must be repaired before this workplan can be judged D3-coherent.

---

## 1. Identity and authority reconstruction

### 1.1 Candidate identity

The branch head was checked before substantive review and again immediately before this record was written. Both checks returned exactly:

`441cf5c4cce0428b44c6d3e15db697b0b4f6262c`

There are no intervening commits. The review therefore applies to exactly the requested candidate and the exact workplan blob `cb967c15aae2d8451e86b67430d9cbb8c6627073`.

The candidate also contains the requested index blob `e6115ad5bfab02f91dd1867a2bf4cd8324832479` and regression-test blob `798a7d5f6527f37e1e48c02586b9cf3c13fd3e42`.

### 1.2 Governing SSDP identity

`PROTOCOL-RELEASE-STATE.yaml` at the candidate identifies:

- accepted current version: `6.6.0`;
- immutable public-source ref: `22f4bdba53795da3a6f13f162529f3a843fc37ae`;
- accepted recovery ref: `384666764da4c55b282e6b1595ab97e2f86e1dc4`.

The current branch's evolving `source/` was not treated as 6.6 semantic authority. The review reconstructed the applicable 6.6 rules from `22f4bdba...`, including abstraction/concretization, D3 architecture, workflow/acceptance, semantic definition, evidence/dependencies, testing, concurrency/orchestration, storage/recovery, Git, security/trust, versioning/compatibility, and PEM.

The governing rules material to the blockers are:

- legitimate mutually recursive **definitions** may be represented by an explicit simultaneous-definition/composite node or SCC condensation, while **circular claim warrant remains invalid**;
- a definition/graph/trace does not recursively warrant its endpoints;
- repository presence or structural representation cannot manufacture semantic authority;
- unresolved challenge/risk state must not be reset to unqualified accepted-current by descendants;
- derived dependency views may claim absence/independence only inside an explicitly reviewed-complete scope;
- durable state/recovery must distinguish complete/current state from stale, incomplete, corrupt, or historical state rather than making an older/partial state look valid;
- evidence and project memory remain data, not authorization; and
- protocol/profile interpretation remains exact-version bound.

### 1.3 PEM basis

The workplan's PEM basis was independently checked rather than trusted from §0.3. `PROJECT-ENGINEERING-MEMORY.md` at the claimed accepted/base point `2585b73f00420daca185a4fbb9ac42a79473eda1` and at the candidate is byte-identical, Git blob:

`1561797125622f355f84eb27319f87e8fa4227d9`

The relevant current memory remains non-authoritative. `PC-001` is authority-bound only because its current versioning owner requires frozen historical profile/resource preservation; `SP-002`, `FF-001`, `DS-001`, and `SP-001` are evidence-only learned capabilities. The candidate does not introduce a PEM overlay.

---

## 2. Recheck of the prior Review

| Prior item | Independent disposition at `441cf5c` | Reason |
|---|---|---|
| **B1 — refinement manufactured child acceptance** | **Closed at the earliest owner** | Acceptance is now exact `(subject, scope_id, rev)`. Byte-preserving refinement creates parts of the same accepted subject; promotion to a new subject requires a qualified acceptance. The holistic-document counterexample is explicitly represented. |
| **B2 — currency/validity multiple fixed points** | **Original fixed-point defect closed; replacement mechanism still has a different blocker** | S0/S1/S2/S3 separates rules/content, challenge recursion, monotone support, and consequences; S2 has a least-fixed-point semantics and Admission additionally requires an acyclic support graph. However, the separate authored-relation SCC rule still accepts circular warrant inside one subject; see Blocker A. |
| B2 additional — `acc(policy)` self-reference | **Closed** | Ruleset adoption is an S0 ledger fact admitted under the previous ruleset; derivation does not derive the rules that define itself. |
| B2 additional — negative obligation recursion | **Closed** | Discharge/readiness consequences are S3; collateral regression is checked at Admission instead of feeding support validity. |
| **B3.1 — correctness depended on remote multi-ref atomic push** | **Closed** | Canonical ledger commit is one-ref compare-and-swap; product publication is separately reconciled as `PENDING`, `PUBLISHED`, or `OVERTAKEN`. Multi-ref atomic push is explicitly only an optimization. |
| **B3.2 — fresh clone can accept a rewound valid prefix** | **Not closed** | Witness/high-water machinery catches rewinds only beyond what some evaluator or witness knows. The design explicitly allows undetectable rewind inside anchoring lag; this contradicts invariant P4 and the claimed current-head distinction. See Blocker C. |
| **B3.3 — secret lineage replacement did not remediate leaked history** | **Closed at D3** | The closed reference schema, preventive scanning, immediate credential rotation, replica inventory, explicit destructive purge/new-repository branch, protected-main rule, and yielded-guarantee disclosure form a coherent security/recovery contract. |
| **N1 — Orchestrator Architecture 1.6.0 transfer incomplete** | **Closed for a prospective workplan** | All 26 product invariants and the frozen surfaces are explicitly classified as preserved/replaced/retired/deferred. Deferred surfaces name Architecture Manual closure obligations rather than silently disappearing. |
| **N2 — routing test treated Markdown substrings as semantic truth** | **Closed** | Current handoff/routing assertions use parsed YAML frontmatter. The remaining substring test is explicitly bounded to archived-lineage representation and disclaims semantic adequacy. |
| **N3 — authority index reassigned Protocol 7 Stage H itself** | **Closed** | The index is explicitly only a routing projection, and the SSDS workplan describes Stage H reconciliation prospectively. The active Protocol 7 owner still owns the actual Stage H reassignment. |
| **N4 — widening algorithm underspecified** | **Closed** | The scope chain, relation class, boundary-completeness criterion, membership-sensitive basis, least fixed point, and whole-tree fallback are specified well enough to constrain D4. |
| **N5 — unnecessary `Change` primitive / cross-repository scope** | **Closed** | `Change` is a typed admission request, not a persistent primitive. Cross-repository units use immutable pins and imported acceptance; multi-repository admission is explicitly non-atomic. |

The archived `befe678` hypothesis is present byte-identically as blob `af9c005b15c4d0cfc56b0efb4dfe6b032fa4d958`.

---

## 3. Blocking findings by earliest owner

## Blocker A — Semantic-definition / relation owner: same-subject SCC is too weak to distinguish simultaneous definition from circular warrant

**Earliest owner:** §6.1 Subjects/composites + §6.2 Relation + §6.8 Admission structure checks.

**Violated governing invariant:** SSDP 6.6 permits mutually recursive definitions only through an explicit simultaneous-definition/composite representation and separately forbids circular claim warrant. A graph condensation is representation; it does not make a circular warrant valid.

### Failure trajectory

1. Create composite subject `G` with parts `a` and `b`.
2. Let `a` and `b` be claim-bearing units, not merely two jointly defined symbols.
3. Author prerequisite relations:
   - `a DERIVED_FROM b`
   - `b DERIVED_FROM a`
4. The authored prerequisite graph contains SCC `{a,b}`.
5. The candidate's structural rule accepts that SCC because all units have one common `subj`, namely `G`.
6. Admit one qualified acceptance judgment `j_G` on `G`. Its support basis can be ordinary content plus external governing prerequisites; the internal authored `DERIVED_FROM` cycle is not necessarily an S2 support-dependency cycle.
7. `valid(G)` can therefore evaluate `T`: the support graph is acyclic even though the semantic warrant for `a` and `b` is circular.

Every stated local structural rule can be obeyed. The higher invariant is nevertheless violated.

### Why the current repair does not close it

The candidate says that a refinement parent and a simultaneous-definition group use the same composite-subject construct and then generalizes:

> every authored relation cycle must consist of units with one common `subj`

That is a necessary locality condition but not a sufficient semantic condition. The relation vocabulary explicitly includes `DERIVED_FROM`, `DEPENDS_ON`, `ASSUMES`, `CONCRETIZES`, `EVIDENCES`, `EXECUTION_DEPENDS_ON`, `GENERATED_FROM`, and extensible future prerequisite relations. Many of those represent warrant, authority, evidence, or provenance rather than simultaneous definition.

The S2 support graph solves a different problem: recursive *currentness/validity of records*. It does not prove that an accepted subject's internal authored claim-warrant graph is semantically non-circular.

### Minimum repair direction

At D3, distinguish cycle legality by semantic relation role rather than by common subject alone.

At minimum:

- require an explicit declaration that an SCC is a **simultaneous-definition group**;
- permit SCC condensation only for relation classes whose owner semantics actually allow mutual definition;
- require the warrant/authority/evidence dependency projection to remain acyclic even inside one subject, except where the governing owner explicitly defines a sound non-warrant recursion;
- make Admission reject a same-subject SCC that contains circular warrant merely because the bytes share one acceptance subject; and
- add a qualification case where two claims in one accepted composite recursively `DERIVED_FROM`/`DEPENDS_ON` one another and the expected result is rejection/non-acceptance.

This need not add a new primitive. A semantic-role field on authored relations or on the composite declaration is sufficient if its rules are closed and versioned.

---

## Blocker B — Derivation/intake owner: foreign structural declarations take effect below the intake quarantine

**Earliest owner:** §6.1 structural identity + §6.6 S0/S2/S3 strata + §6.8 foreign absorption + §11 intake.

**Violated governing invariants:** repository presence does not manufacture acceptance; challenge cannot be escaped by structural redeclaration; §11.3's own contract says foreign-affected content cannot serve as governing context, evidence, or acceptance basis until intake obligations are discharged.

### Structural contradiction

The candidate deliberately excludes **structural declarations** (partition boundaries, member lists, part/subject role) from `rev`, while those declarations directly determine `scope` and `subj`. This is required for byte-preserving refinement of a holistic accepted subject.

For ordinary Admission, step 4 prevents role/scope redeclaration inside a challenged or revoked subject. But foreign content already on the integration ref is mechanically absorbed; violations of steps 4-5 are recorded as **integrity findings** instead of being rejected.

The strata then matter:

- S0 reads the admitted tree and therefore reads the absorbed structural declarations;
- S2 computes `valid(s)` and record currency from S0/S1 plus bases;
- intake obligations, drift, blockers, and integrity findings are S3 consequences;
- by design, nothing below S3 may read S3.

Therefore the workplan has no shown lower-stratum predicate capable of making §11.3's promised intake quarantine constrain S2 validity for a structural-only foreign edit whose semantic revision is unchanged.

### Concrete failure trajectory

A legal implementation can reach the following history while obeying the written rules:

1. Subject `A` is accepted at exact triple `(A, S, R)` by judgment `j_A`.
2. Later, while unchallenged, an admitted structural change demotes `A` into a part of composite subject `P`, and `P` is accepted. The workplan's qualification language explicitly contemplates demotion. No architecture rule requires demotion to syntactically supersede `j_A`; while `A` is a part, its old acceptance is simply not the routed subject acceptance.
3. `P` later receives an unresolved blocking challenge.
4. A human/manual/foreign push changes only the structural role declaration so `A` is again a subject. The governed bytes and semantic declarations for `A` remain exactly `S,R`; structural markers are intentionally excluded from `rev`.
5. Mechanical absorption cannot reject what is already on the integration ref. It records the step-4 violation as an S3 integrity finding.
6. S0 nevertheless computes `subj(A)=A` from the absorbed declaration.
7. S2 can again find `j_A` as a current passing acceptance of exact `(A,S,R)`. The challenge on `P` no longer controls `valid(A)` because routing changed in S0.
8. The S3 intake obligation/integrity finding cannot feed back into S2 by construction.

The result is a structural challenge escape and acceptance resurrection before the foreign intake is semantically dispositioned. It directly contradicts §11.3's sentence that affected content cannot serve as an acceptance basis until intake obligations are discharged.

Even if a particular D4 implementation chooses to supersede `j_A` during demotion, that does not repair the D3 abstraction: the workplan does not require it, and the more general S0/S2 versus S3 quarantine contradiction remains for structural declarations.

### Minimum repair direction

Do not solve this by letting S2 read S3; that would destroy the stratum contract.

A coherent minimum repair is one of:

1. **Observed vs effective governance declarations.** Absorption may make foreign bytes the admitted content tree while structural governance declarations remain at the last governance-admitted state until a qualified intake/role-transition judgment activates the new declarations; or
2. **A lower-stratum intake/currentness factor.** Represent foreign structural mutation as an S0 fact and require a current support-tier intake/role-transition judgment in S2 before an affected structural declaration may influence `subj`, acceptance selection, evidence use, or governing-context eligibility.

In either design, also specify the lifecycle of old subject acceptances across demotion/promotion so an old exact triple cannot become current merely because the same structural role is reintroduced. Restoration may reuse prior evidence if valid, but **restoring authority is itself an explicit qualified judgment**, not an effect of a content declaration.

Qualification must include at least:

- foreign structural-only promotion/demotion with unchanged bytes;
- the same trajectory while the enclosing subject is challenged/overridden;
- a historical acceptance of the promoted subject to test resurrection; and
- proof that the foreign tree remains buildable/observable while governance validity stays quarantined.

---

## Blocker C — Persistence/recovery owner: anchoring permits a silent valid-prefix rollback that P4 forbids

**Earliest owner:** §15.4 Freshness and anti-rollback, with §13 recovery and §22 qualification consequences.

**Violated invariant:** candidate P4 states that a valid historical prefix is **never** mistaken for the current head and that rollback, fork, and loss are distinguished and fail closed. The first review's B3.2 made the same distinction material.

### Failure trajectory

Use the candidate's own `synchronous` policy as written:

1. Witness quorum has checkpointed ledger head `L99`.
2. Admission appends valid authenticated entry `L100`. The ledger ref now points at `L100`; derivation can advance on the appended ledger position.
3. The `synchronous` policy only requires that **the next admission** wait until a quorum holds the previous head. Thus there is a real interval in which `L100` is newer than every external checkpoint.
4. Before `L100` reaches a witness, the authoritative replica is restored/force-moved to `L99`, and every participant that had a high-water mark at `L100` is lost or unavailable.
5. A fresh clone reads the authoritative head `L99` and obtains the witness quorum. The highest witness checkpoint is also `L99`.
6. `L99` authenticates from genesis and extends every checkpoint/high-water mark known to the evaluator, so rule 4 accepts `L99` as current.
7. Yet `L99` is only a valid historical prefix; `L100` existed as canonical accepted history and has been lost.

There is no surviving fact from which the fresh clone can infer that `L100` ever existed. The loss cannot be distinguished from a world in which `L99` was genuinely the latest head.

The bounded-lag policy makes the contradiction explicit rather than hypothetical: §22 says that a rewind within the declared anchoring lag is **undetected exactly as stated**.

### Why disclosure is not sufficient

Truthfully disclosing a bounded detection limit is good security practice, but it cannot coexist with the stronger invariant P4 and the qualification expectation that “no path silently treats `L80` as current.” The architecture currently claims both:

- absolute current-head distinction in P4 and the recovery vocabulary; and
- an interval in which precisely that distinction is unknowable.

This is not merely a D4 witness implementation detail. It determines the semantics of canonical current state and recovery.

### Minimum repair direction

Choose one contract and make every dependent statement consistent with it.

For the strong P4 contract, an entry may be **committed in the ledger but not current-qualified** until a quorum witness has anchored that exact head (or a later head that cryptographically proves it). “Synchronous” must bind currentness/qualification of `L_n` to anchoring `L_n`, not merely block admission of `L_{n+1}` until `L_n` is anchored. Interfaces and Dispatch must not emit unqualified current-state claims from an unanchored latest head.

If bounded-lag anchoring is a deliberate deployment mode, then P4 and all currentness/recovery claims must be weakened to the exact bounded guarantee. During the unanchored window the state must be visibly provisional/unanchored; a fresh clone must not claim that replica head as an unqualified current accepted head merely because it equals the latest checkpoint it can see.

Qualification must stop treating “undetected exactly as stated” as success under the strong P4 contract.

---

## 4. Non-blocking findings, ranked by consequence

### N6 — High: §22 needs a same-subject circular-warrant discriminator

The qualification matrix tests legitimate simultaneous definition and the prior four-predicate acceptance recursion, but it does not discriminate the Blocker A case: an authored warrant SCC entirely inside one accepted subject. Add a relation-semantic fixture, not only a support-currentness fixture.

### N7 — High: §22 currently encodes the anti-rollback defect as an expected success

The qualification statement “rewind within the declared anchoring lag is undetected exactly as stated” is internally truthful but inconsistent with P4. After Blocker C is repaired, the expected result must be changed so the test discriminates the selected guarantee rather than normalizing the defect.

### N8 — Medium: the foreign-intake qualification must exercise structural-only mutations

Existing intake cases cover manual edits, external branches, unknown files, agent overstep, and live-ref movement. The decisive case is a foreign change that alters only normalized-out structural declarations while preserving the semantic revision. Without it, a test suite can remain green while §11.3 is false for the exact class of edits created by the refinement design.

### N9 — Low: Architecture Manual deferrals are acceptable only while the hard D4 boundary remains intact

The transfer table appropriately marks exact API/SPI mapping, configuration layout, harness lifecycle detail, and static component fitness as Architecture Manual closure obligations. Those are not blockers in a prospective workplan because the handoff explicitly requires a separately reviewed/accepted Architecture Manual before D4. If implementation were authorized directly from this workplan, they would become premature deferrals.

### N10 — Positive bounded finding: the routing regression test now respects DS-001

`tests/test_protocol_80_orchestrator_consolidation.py` parses frontmatter for semantic routing facts and explicitly says its Markdown substring test is only an archived-lineage representation guard. It does not claim that substring presence proves semantic adequacy. That is an appropriate scope for this regression test.

---

## 5. Independent out-of-matrix abstraction-adequacy pass

This pass set aside the candidate's own §22, §25, and §27 conclusions and attempted trajectories that obey local rules while violating higher invariants.

| Attack trajectory | Result | Independent disposition |
|---|---|---|
| Semantic authority transfer during byte-preserving refinement | Survives attack | Ordinary refinement keeps child regions as parts of the same subject; promotion needs qualified acceptance. |
| Holistic legacy acceptance projected onto section | Survives attack | Import is exact accepted legacy scope; section cannot inherit whole-document acceptance. |
| Carve-out cutover while parent remains accepted | Survives attack | Frozen parent scope and explicit residual/cutover rules prevent silent acceptance transfer. |
| Circular/self-supporting acceptance through S2 validity/currentness | Survives the prior attack | Least fixed point + Admission support-graph acyclicity blocks the former multiple-fixed-point construction. |
| Circular semantic warrant inside one composite | **FAIL** | Same-subject authored SCC is admitted without proving it is simultaneous definition; Blocker A. |
| Challenge/adjudication/risk-override recursion | Survives ordinary attack | S1 order is well-founded; override remains provisional and can itself be challenged. |
| Challenge escape by ordinary re-scope | Survives ordinary Admission | Step 4 rejects the role/scope change. |
| Challenge escape by **foreign structural absorption** | **FAIL** | Structural declaration takes effect in S0 while its integrity/intake quarantine is S3; Blocker B. |
| Stale/rewound canonical ledger state | **FAIL** | A rewind inside anchoring lag can be accepted by a fresh clone as current; Blocker C. |
| Crash between ledger append and product publication | Survives attack | `PENDING`/`PUBLISHED`/`OVERTAKEN` plus exact-ref CAS covers the windows without overwriting foreign work. |
| Foreign push during publication | Survives content-preservation attack | CAS prevents overwrite; overtaken admitted work remains ledger-reachable and is routed to revalidation. |
| Manual/foreign structural declaration | **FAIL** | Same as Blocker B. |
| Missing dependency knowledge | Survives attack | No completeness judgment causes deterministic widening through the scope chain to whole-tree `UNBOUNDED`; missing knowledge is not independence. |
| Stale evidence reuse | Survives architectural attack | Evidence realization/assessment and basis binding make changed target/execution inputs stale; unavailable binding does not remain positive support. |
| Ruleset/policy self-reference | Survives attack | Ruleset is adopted under previous rules in S0; lower strata do not derive their own rules. |
| Historical profile/version isolation | Survives attack | Frozen Core profiles remain version-bound; native and `LEGACY(p)` interpretation are distinct. |
| Repository loss/restoration | **Blocked by Blocker C only** | Object retention, replica restore, `LEDGER_LOSS`, and binding-health semantics are coherent, but current-head proof is not sound inside anchoring lag. |
| Simultaneous legacy and native production | Survives attack | Per-subject modes, carve-out, and foreign intake avoid automatic dual authority in the ordinary path. |
| Cross-repository references | Survives attack | Immutable pin + explicit imported acceptance; no false claim of cross-repo atomicity. |
| Agent proposal mistaken for authority | Survives attack | Agent judgments are proposals/records; authorization, acceptance, discharge and human gates remain distinct. |

**Out-of-matrix result: FAIL.**

The failures are not test omissions alone. Each exposes a locally legal descendant behavior that violates a higher governing invariant, so repair belongs at D3 before D4.

---

## 6. Derivation-strata assessment

### S0

The adopted-ruleset mechanism successfully removes the predecessor's `acc(policy)` self-reference. Ruleset evolution is an explicit lifecycle record admitted under the prior ruleset, and historical admissions are not retroactively re-adjudicated.

However, S0 also consumes structural declarations from the latest absorbed tree. This becomes unsound when a foreign structural declaration is supposed to be quarantined until intake closure; see Blocker B.

### S1

The challenge recursion is well-founded because challenge-tier targets are constrained to earlier records and challenges cannot target challenges. Later adjudications/withdrawals/overrides can be evaluated in reverse ledger order without a negative cycle. Challenging an override or adjudication remains conservative.

### S2

The lattice `F < P < T`, monotone `min`/`max`, content/equivalence recursion, exact acceptance set, current gates, and current evidence assessments support a unique least fixed point. The former ambiguous positive recursion is no longer present. Admission's support-graph acyclicity is a stronger operational invariant and is computable from the declared edge families.

The S2 defect is not monotonicity; it is the missing lower-stratum foreign-intake gate for structural declarations. S3 cannot repair S2 after the fact.

### S3

Consequences are appropriately non-monotone and kept out of lower tiers. That separation is a design strength. It is exactly why the intake promise cannot be implemented merely as an S3 “foreign change awaiting intake” obligation when structural declarations already changed S0 routing.

### One-input/one-state claim

For a fully admitted ledger/content input satisfying the stated structural contracts, the mathematical S0-S3 pipeline is single-valued. The three blockers concern **whether the input has been assigned sound semantics/currentness**, not evaluation-order ambiguity.

---

## 7. Commit point, publication, recovery, and confidentiality

### 7.1 Ledger commit and product publication

The single-ref ledger CAS is a real closure of prior B3.1. Correctness no longer depends on a server advertising atomic multi-ref push.

The publication state machine is adequate at D3:

- `PENDING`: integration still at exact predecessor, so retry is idempotent;
- `PUBLISHED`: admitted commit is in live ancestry or an explicitly recognized equivalent external merge occurred;
- `OVERTAKEN`: live ref moved elsewhere, so foreign work is absorbed and the admitted request is revalidated.

A losing writer does not overwrite foreign work, and an admitted-but-unpublished candidate remains separately identifiable.

### 7.2 Anti-rollback

Not adequate because of Blocker C. The witness is a necessary addition for a strong anti-rollback claim, but the selected anchoring/currentness semantics do not yet establish the claim.

### 7.3 Confidentiality

The confidentiality architecture is materially adequate and closes prior B3.3 at D3:

- reference-oriented closed ledger schema, no generic free-text payload;
- preventive bounded scanning stated as assistance rather than guarantee;
- operator secrets stay outside repositories;
- dedicated private ledger is an explicit deployment option;
- incident response requires credential rotation/revocation first;
- controlled replicas are inventoried and invalidated/purged where confidentiality requires it;
- protected `main` is not rewritten in place; a new repository is required where old reachable history must remain;
- old uncontrolled copies are explicitly outside the guarantee; and
- replacement lineage states which append-only/reproducibility/anchoring guarantees yield.

This is honest about the unavoidable limits.

---

## 8. Conservative widening

The widening algorithm is now sufficiently architectural rather than aspirational.

The chain is deterministic and monotone by construction: singleton, enclosing composites, directory scopes, whole governed tree. A current `COMPLETENESS(X,R)` at the smallest qualifying scope permits bounded widening; absent completeness falls back to whole-tree `UNBOUNDED`. Membership identity in the completeness basis invalidates a previously complete scope when members change. Closure iteration is a least fixed point, so traversal order is not a semantic variable.

Most importantly, the fallback does not infer independence from missing edges. It widens and surfaces incompleteness. This closes prior N4.

The residual limitation—an undeclared semantic dependency no actor/tool observes—remains honestly disclosed and is not eliminable by graph mechanics alone.

---

## 9. Minimum-architecture assessment

The review does **not** find that the overall architecture is overbuilt or missing a new top-level component.

### Four primitives

- **Unit** is needed for adaptive semantic/content locality.
- **Relation** is needed for direct semantic/dependency provenance and widening.
- **Record** is needed for non-derivable judgments/observations/lifecycle facts.
- **Basis** is needed for currentness, stale-result rejection, impact locality and replay.

`Change` is correctly demoted to a request/ledger identity rather than retained as a fifth persistent primitive.

### Seven components

Content Model, Analyzers, Ledger Store, Derivation Engine, Admission, Dispatcher, and Interface have distinct ownership. No identified blocker requires restoring Tracker/Adapter/Scheduler as separate authority-bearing components. Dispatcher remains subordinate to derived readiness and does not become a second Admission writer.

### Persistent surfaces

The content store, canonical ledger, derived index, operator state, transport refs, and external checkpoint witness each have a distinct recovery/trust role. The witness is justified **if** the architecture keeps its strong anti-rollback claim; Blocker C concerns witness semantics, not the need for the surface.

### Synchronization mechanisms

Single-ledger CAS, product-ref CAS/reconciliation, worktree serialization, and optimistic basis revalidation are all materially motivated. No additional distributed transaction coordinator is justified by the stated one-ledger-per-project boundary.

---

## 10. Capability transfer from frozen Orchestrator Architecture 1.6.0

The frozen text and the implemented Core surfaces were independently inspected where transfer mattered. The current Core has one extension registry/composition root, versioned API/SPI records, route-independent preparation/profile/workplan services, and packaged frozen protocol profiles including 5.16 and 6.0-6.6. Current tests explicitly protect byte-stable prior profiles and the pre-7 lifecycle/control schema.

The candidate's transfer table is materially more accurate than the predecessor's. Independent disposition:

| # | Frozen 1.6.0 invariant | Independent SSDS 8 disposition |
|---:|---|---|
| 1 | Progressive usefulness; Core alone complete | **Replaced for native SSDS, preserved for version-bound Core.** Read-only derivation/interface can be useful before mutation capability. |
| 2 | Strict `core <- tracker <- adapters <- scheduler` ladder | **Legitimately retired/replaced.** New SSDS component DAG is the successor architecture; old Core remains independently usable. |
| 3 | Graceful degradation/no silent policy bypass | **Preserved in substance.** SSDS degrades to truthful non-closure/read-only state rather than pretending policy absence. |
| 4 | One CLI/composition root | **Preserved principle; Manual closure required.** Deferral is explicit and bounded by no-D4 gate. |
| 5 | Versioned public boundaries | **Preserved; exact mapping deferred.** |
| 6 | No duplicated workflow authority | **Replaced coherently.** Native workflow authority is ledger+Admission/derivation; legacy profiles retain older ownership. |
| 7 | Manual operation first-class | **Preserved in route/handoff substance; document-only control retired for native scopes.** |
| 8 | Capability recommendation before resource scheduling | **Module boundary retired; semantic separation retained in Dispatcher.** |
| 9 | Benchmark observations preserve context | **Preserved; exact fields deferred.** |
| 10 | Scheduler subordinate to workflow intent | **Preserved/strengthened.** Dispatcher acts only on derived-ready work. |
| 11 | Private state outside project repo | **Deliberately replaced in part.** Operator/private telemetry remains private; canonical closed-schema ledger may be Git-hosted after explicit D3 adoption. |
| 12 | Subset acceptance permanent | **Core preservation retained; old module-ladder rule retired for SSDS components.** No later SSDS requirement is allowed to invalidate old version-bound Core acceptance. |
| 13 | Stable IDs cross components, not private objects | **Preserved.** |
| 14 | Read-only query vs durable mutation visible | **Preserved.** Derivation/Interface read; Admission mutates canonical state. |
| 15 | Explicit long-running execution lifecycle | **Preserved in Dispatcher contract; lifecycle detail deferred.** |
| 16 | Manual/direct routes share route vocabulary | **Preserved.** |
| 17 | Capability identity independent of API version | **Preserved; keys deferred.** |
| 18 | Explicit route choice not a resource-admission bypass | **Preserved in Dispatcher.** |
| 19 | Route admission precedes route-sensitive final rendering | **Preserved in substance.** |
| 20 | Run identity precedes scheduling/rendering | **Preserved.** |
| 21 | Structured seam for manual result tracking | **Replaced/strengthened by typed Admission request.** |
| 22 | Protocol version binding explicit | **Preserved.** |
| 23 | One mutating run owns one local worktree | **Preserved.** |
| 24 | Workflow routing authority profile-owned | **Deliberately replaced for native scopes; preserved for legacy/version-bound rendering.** |
| 25 | Uncertain routing remains uncertain | **Preserved.** Unknowns remain explicit/fail closed. |
| 26 | Orchestrator implementation containment | **Preserved default; explicit Manual supersession required for any successor root.** |

The frozen surface dispositions (§5 API standard, §6 Core SPI, §7 Core records, §8 Core, §9-11 unimplemented higher modules, configuration, persistence, security, benchmark integrity, fitness checks, acceptance ladder, versioning and simplicity triggers) are all at least named with preserve/replace/retire/defer treatment. No silent capability loss was found in this pass.

The current Core implementation corroborates the most important backward-compatibility claim: existing frozen profiles are physically separate version-bound resources, and tests compare their exact blob identities/derived profile coherence. The SSDS plan does not require mutating those bytes.

---

## 11. Archived Protocol 8 lineage and befe678 capability transfer

The consolidated predecessor and its nine-file historical composition were independently inspected at the candidate, rather than trusting §18's table alone.

The relevant inherited requirements are present in the predecessor family:

- deterministic reducer/derivation must not consult live mutable ambient state during replay;
- external effects require intent/idempotent or reconcilable effect/observed outcome;
- canonical control history requires explicit durability, corruption, restore, schema/version and retention semantics;
- semantic authority remains in D1-D4 owners rather than control projection;
- scheduling/resource choice remains subordinate to workflow readiness;
- default private control persistence could be changed to in-repository state only by a later D3 design that resolves concurrency, privacy, history and ownership;
- transport envelopes are not semantic repository content;
- version-bound replay and pre-cutover fallback/recovery are preserved; and
- Protocol 6.2-6.6 inheritance revisions changed inherited baselines/capabilities without silently accepting D3.

Revision 2's Git ledger decision is therefore permitted in principle because this candidate **does** attempt the required later D3 storage/trust adoption. The adoption is not rejected merely because the predecessor default was private storage. The remaining issue is narrower: its anti-rollback currentness guarantee is not yet sound.

The archived `befe678` hypothesis independently contains the distinction the current same-subject SCC rule accidentally blurs: D1-D4 ordering is a DAG after explicit condensation of **legitimate simultaneous definitions**, while accidental circular warrant is invalid. Blocker A is therefore also a regression from a useful befe678 semantic distinction, despite the candidate's simplification of the graph machinery.

---

## 12. Routing and Protocol 7 inheritance discipline

The current authority index is a routing projection, not a semantic owner. Its `current_handoffs` frontmatter routes:

- `protocol-7.0` to the active Protocol 7 consolidated workplan; and
- `ssds-8.0` to this SSDS 8 architecture workplan.

The index explicitly says that it authorizes nothing and that substantive requirements live in the routed owners.

The active Protocol 7 Stage H still owns its own eventual Protocol 8 inheritance reconciliation. It currently names the archived consolidated Protocol 8 workplan, advances the pre-cutover baseline, binds Protocol 7 gate-evidence/RSR semantics as inputs, selects no Protocol 8 architecture, and authorizes no Protocol 8 D4. The SSDS workplan correctly phrases its relationship to that future action prospectively. No final Protocol 7 recovery, gate-evidence identity, or adoption identity was invented here.

No dual current semantic authority was found in the routing layer.

---

## 13. Qualification and regression-test adequacy

The workplan's §22 is appropriately broad for a future implementation qualification plan, including the required holistic-acceptance counterexample. It does not itself constitute execution evidence.

Three changes are required by the blockers:

1. add a **same-subject circular-warrant** case distinct from the existing legitimate simultaneous-definition and S2 positive-recursion cases;
2. add a **foreign structural-only absorption** case whose structural markers are excluded from revision identity and that attempts challenge escape/old-acceptance resurrection; and
3. replace the anti-rollback expectation that treats an undetected within-lag rewind as successful behavior if P4 remains the governing invariant.

The repository-level consolidation regression test is correctly narrow. It verifies proposed/unauthorized frontmatter, archived lineage closure, frontmatter-based current-handoff routing, and archived-path representation. Its docstring explicitly leaves semantic adequacy to independent Review. No test expectation there was found to counterfeit D3 semantic truth.

---

## 14. Evidence used

### 14.1 Executed during this Review

No repository qualification/test command was successfully executed because this environment has no local checkout of the repository and its container cannot resolve `github.com` for Git transport.

Environment checks actually executed:

```text
git version 2.47.3
Python 3.13.5
```

A live Git transport probe was attempted:

```text
git ls-remote https://github.com/hjin98/scientific-software-development-protocol.git refs/heads/ssds-8.0-graph-native-architecture
```

It failed before repository access with:

```text
Could not resolve host: github.com
```

Therefore none of the following are represented as executed evidence in this Review:

- `python -m unittest discover -s tests`
- `python source/release_state.py`
- `python source/project_engineering_memory.py PROJECT-ENGINEERING-MEMORY.md`
- `python source/build_skills.py --output /tmp/protocol-dist`
- `python source/validate_packages.py --dist /tmp/protocol-dist`
- `python source/check_dist.py --expected /tmp/protocol-dist --committed dist`
- `git diff --check`
- `python orchestrator/scripts/generate_protocol_snapshot.py --check`
- `python orchestrator/scripts/run_core_tests.py`

The commands above were independently recovered from `.github/workflows/protocol-check.yml`; they are not author-reported execution evidence.

### 14.2 Read-only evidence independently inspected

Using repository/API reads bound to the exact candidate or immutable accepted ref, this Review inspected at least:

- branch head at start and final recheck;
- `PROTOCOL-RELEASE-STATE.yaml`;
- `AGENTS.md`;
- accepted SSDP 6.6 owners at `22f4bdba...`, including semantic definition, architecture, workflow, evidence/dependencies, storage, security, Git/versioning and PEM rules material to the decision;
- the exact SSDS 8 workplan blob `cb967c15...`;
- prior `f9d9de8` NO-PASS record as a hypothesis source;
- the authority index blob `e6115ad5...`;
- the regression test blob `798a7d5f...`;
- frozen `orchestrator/docs/architecture.md` Architecture 1.6.0;
- current Core composition/profile/protocol-source/API and frozen-profile tests/snapshot generator where needed to judge transfer;
- active Protocol 7 Stage H wording;
- archived consolidated Protocol 8 workplan;
- archived parent/Revisions 1-7 and version-rebind lineage, with targeted deep inspection of the storage/control/recovery amendments;
- archived befe678 hypothesis blob `af9c005b...`; and
- accepted/base and candidate `PROJECT-ENGINEERING-MEMORY.md`, both blob `156179712...`.

### 14.3 Reused evidence

No author-reported test PASS, prior-review verdict, workplan self-diagnosis, §27 self-pass, or commit-message claim was reused as execution or acceptance evidence.

Historical accepted records were used only to reconstruct capability lineage where their owner made that history relevant; they were not used to substitute for current D3 falsification.

### 14.4 Unavailable evidence

Local test/build/validation execution remains unavailable in this Review environment for the reason above. This does not create the NO-PASS: the verdict is driven by three architecture-level counterexamples visible in the reviewed contracts. A later environment should still run the complete requested suite after the D3 repairs because execution may expose additional defects.

---

## 15. Independently reconstructed invariant disposition

| Invariant | Source/owner | Candidate disposition |
|---|---|---|
| One current semantic owner; no lower mechanism manufactures authority | 6.6 abstraction/workflow | **Blocked by foreign structural activation path; ordinary promotion path is sound.** |
| D1-D4 direction is acyclic | 6.6 abstraction/architecture | Preserved. |
| Legitimate mutual definition is explicit; circular warrant invalid | 6.6 semantic-definition/evidence | **Blocked by same-subject SCC rule.** |
| Acceptance mutation requires owning acceptance process | 6.6 workflow | Preserved ordinarily; **blocked for foreign structural role activation.** |
| Risk override cannot yield unqualified closure | 6.6 workflow | Preserved in S1/S3 ordinary path. |
| Definitions/relations do not establish truth/warrant by themselves | 6.6 semantic definition | **Blocked by Blocker A.** |
| Missing relation knowledge never proves independence | 6.6 evidence/dependencies | Preserved by completeness/widening fallback. |
| Stale passing/failing evidence is inadmissible | 6.6 evidence | Preserved. |
| Evidence target and execution dependency remain distinct | 6.6 evidence | Preserved. |
| One canonical serialization point | inherited P8/D3 | Preserved by Admission + one ledger ref. |
| Same admitted input/ruleset gives one derived state | inherited P8/D3 | Preserved mathematically. |
| Historical replay does not consult live ambient state | inherited P8/D3 | Preserved. |
| External effects are idempotent/reconciled | inherited P8/D3 | Preserved at architecture level. |
| Product publication never overwrites foreign work | Git/concurrency | Preserved by exact predecessor CAS. |
| Admitted-but-unpublished state is distinguishable | persistence/publication | Preserved (`PENDING`). |
| Overtaken admitted work remains recoverable/revalidated | persistence/publication | Preserved. |
| Valid historical prefix is never mistaken for current head | storage/security + candidate P4 | **Blocked by anchoring lag.** |
| Fork, rollback, loss, recovery are distinct | storage/security | Mostly specified; **rollback/loss distinction fails inside unanchored lag.** |
| Fresh clone cannot claim currentness without adequate anchor | storage/security | **Blocked for a rewind equal to highest available checkpoint inside lag.** |
| Secrets/private telemetry do not enter project history by default | security | Preserved. |
| Secret exposure triggers rotation plus history remediation | security/Git | Preserved. |
| Protected `main` history is not rewritten to hide leakage | Git/security | Preserved. |
| Canonical/derived/cache/operator state have distinct ownership | D3/storage | Preserved. |
| Version-bound historical profiles stay immutable/testable | versioning + PC-001 | Preserved and corroborated by current Core resources/tests. |
| Protocol 7 inheritance remains non-final until its owner closes it | task/versioning | Preserved. |
| Workplans/tests/reviews/PEM do not self-authorize semantics | 6.6 kernel/PEM | Preserved in routing/test design. |
| Agent PASS/proposal is not authority | 6.6 + P8 | Preserved. |
| Unknown required semantics fail closed | 6.6/security/control | Preserved. |
| Architecture Manual must close deferred implementation-facing D3 surfaces before D4 | candidate handoff | Preserved; hard boundary remains explicit. |

---

## 16. Required repair set for a next Review

A minimal next revision does **not** need another wholesale architecture rewrite. It should repair only the earliest owners of the three counterexamples:

1. **Relation-cycle semantics:** make SCC admission semantic-role aware and distinguish explicit simultaneous definition from circular warrant.
2. **Foreign structural intake:** prevent absorbed structural declarations from altering governing subject routing/current acceptance until a lower-stratum intake/role-transition condition is satisfied; define old-acceptance lifecycle across demotion/restoration.
3. **Anti-rollback currentness:** align witness anchoring with the exact semantics of “current accepted head,” or weaken the invariant and all dependent claims to a truthful bounded guarantee.
4. Update §22 with discriminating counterexamples for all three repairs.

The repaired candidate should then receive a fresh independent D3 Review bound to its exact commit/blob. Passing repository tests alone would not close these semantic defects.

---

## 17. D4 authorization statement

**SSDS 8 D4 remains NOT AUTHORIZED.**

This NO-PASS does not authorize implementation, schema freezing, migration, ledger deployment, or replacement of the frozen Orchestrator Architecture 1.6.0.

Even after the three blockers above are repaired and this prospective workplan later receives an independent D3 PASS, D4 remains separately gated by the workplan's hard boundaries:

- Protocol 7 must first close and its owning Stage H process must perform the required SSDS/Protocol 8 inheritance reconciliation without inventing non-final identities; and
- an SSDS 8 Architecture Manual must be produced, independently reviewed, and accepted before SSDS 8 implementation authority exists.

No final Protocol 7 release, recovery, gate-evidence, inheritance, or adoption identity is inferred by this Review.