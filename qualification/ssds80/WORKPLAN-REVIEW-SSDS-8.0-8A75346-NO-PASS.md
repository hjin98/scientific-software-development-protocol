# SSDS 8.0 Prospective Architecture Workplan — Independent D3 Review, Design Revision 3

    GOVERNING SSDP: 6.6.0
    REPOSITORY: hjin98/scientific-software-development-protocol
    BRANCH: ssds-8.0-graph-native-architecture
    CANDIDATE: 8a75346892852a719df41d7ba6f296bb376fe9cf
    HEAD AT REVIEW START: 8a75346892852a719df41d7ba6f296bb376fe9cf
    HEAD AT FINAL RECHECK BEFORE THIS RECORD: 8a75346892852a719df41d7ba6f296bb376fe9cf
    INTERVENING COMMITS: none
    PRIMARY WORKPLAN: workplans/active/SSDS-8.0-GRAPH-NATIVE-DETERMINISTIC-ORCHESTRATION-ARCHITECTURE.md
    PRIMARY WORKPLAN GIT BLOB: d130da4e796c409716ae0bcc63d6a27e440f862a
    AUTHORITY INDEX GIT BLOB: b00aec69898d1afe66095b9b6d94c09c0ac26a84
    CONSOLIDATION TEST GIT BLOB: 798a7d5f6527f37e1e48c02586b9cf3c13fd3e42
    GOVERNING PUBLIC-SOURCE REF: 22f4bdba53795da3a6f13f162529f3a843fc37ae
    GOVERNING RECOVERY REF: 384666764da4c55b282e6b1595ab97e2f86e1dc4
    PRIOR REVIEWS, HYPOTHESIS ONLY:
      qualification/ssds80/WORKPLAN-REVIEW-SSDS-8.0-F9D9DE8-NO-PASS.md
      qualification/ssds80/WORKPLAN-REVIEW-SSDS-8.0-441CF5C-NO-PASS.md
    REVIEW METHOD: fresh D3 reconstruction from the immutable 6.6 owners; adversarial abstraction-adequacy pass;
                   prior reviews, commit prose, workplan self-assessment and qualification matrix treated as hypotheses

## SERIOUS CHALLENGE

**None.**

The accepted SSDP 6.6 authority reconstructed from the immutable public-source ref named by PROTOCOL-RELEASE-STATE.yaml is coherent enough for this decision. The defects below are in the prospective SSDS 8 D3 concretization. They do not demonstrate that accepted 6.6 authority is false, contradictory, materially ambiguous, mutually incompatible, or unrealizable.

## Verdict

# **NO-PASS**

Design revision 3 is a substantial repair, not a wording-only revision. It closes the three blockers from the 441cf5c review at their original owners: relation-cycle legality now distinguishes simultaneous definition from circular warrant; structural declarations have an admitted effective state distinct from observed repository presence; and currentness is restricted to a quorum-witnessed ledger head with a mathematically sufficient read/write intersection condition.

Two new D3 blockers survive independent out-of-matrix attack:

1. **Publication reconciliation has a canonical-recording cycle.** Publication status is defined from a recorded live-ref observation, while the next ledger append is prohibited until the preceding publication is resolved. A successful or overtaken publication therefore has no specified legal path by which the observation that resolves it can itself enter the ledger.
2. **Explicit ledger-loss recovery can resurrect pre-loss authority when the ledger and product repository are restored together to the same stale snapshot.** The quarantine argument in revision 3 protects only the case where the repository still contains structural changes from the lost ledger suffix. If both stores are stale-consistent, Q is empty and a retained old acceptance can become current again across a known lost admitted interval.

Neither defect requires abandoning the four-primitives / seven-components architecture. Both require repairing the D3 persistence and recovery contract before D4.

---

## 1. Identity and authority reconstruction

### 1.1 Candidate identity

The branch head was checked before substantive review and again immediately before writing this record. Both checks returned exactly:

8a75346892852a719df41d7ba6f296bb376fe9cf

There are no intervening commits. This Review therefore applies exactly to the requested candidate.

The required candidate blobs are:

| Artifact | Git blob |
|---|---|
| Primary workplan | d130da4e796c409716ae0bcc63d6a27e440f862a |
| Workplan authority index | b00aec69898d1afe66095b9b6d94c09c0ac26a84 |
| tests/test_protocol_80_orchestrator_consolidation.py | 798a7d5f6527f37e1e48c02586b9cf3c13fd3e42 |

The candidate has two commits after 441cf5c: d9720e14aa934e076b5998015c6ecefb918c8d83 adds the 441cf5c Review record, and 8a75346892852a719df41d7ba6f296bb376fe9cf contains the revision-3 workplan/index repair. The branch itself did not advance beyond the requested candidate during this Review.

### 1.2 Governing SSDP identity

PROTOCOL-RELEASE-STATE.yaml at the candidate identifies:

- accepted-current version: 6.6.0;
- immutable public-source ref: 22f4bdba53795da3a6f13f162529f3a843fc37ae;
- recovery ref: 384666764da4c55b282e6b1595ab97e2f86e1dc4.

The branch's evolving source/ was not used as governing 6.6 semantic authority. The Review reconstructed the applicable rules from the exact public-source ref above, including these owners and blob identities:

| 6.6 owner | Blob |
|---|---|
| abstraction-and-concretization.md | c38aa30efb927ef106df0ea27d8b39544e233f11 |
| architecture-and-design.md | 51f021667ebf50282905235188a380aa52fbdb07 |
| workflow-and-workplans.md | 1de334e34a3a0880f2a67f93c1a2eb49fee024db |
| semantic-definition-and-traceability.md | 94b48b508de2e4a10809c27f964ed3f7a0a48d33 |
| evidence-evolution-and-dependencies.md | 2807401064d4ce91792aa0e4b5453339b760579b |
| testing-and-validation.md | b2d75e0fe5795d50891098d85e7cdfb944d7cbc1 |
| concurrency-and-orchestration.md | c6b6bf9adc431c03e59fb301128e50b2d42c400f |
| storage-and-io.md | 7a3548e8f2140bcbe2208f300b9a4830ab533a08 |
| git-and-version-control.md | cf493cd9c61a13df8cb3a0fa39b869f4f4e7843b |
| security-and-trust-boundaries.md | d8a08c6bc9116ef0d1886d5a83349d8ba4dee7c1 |
| protocol-versioning-and-compatibility.md | 74f2acab9fba6b0f967138d05d718f983915179d |
| project-engineering-memory.md | 89849ecad084bdbb4ce20ed8a1f0d3f23602d53a |

The reconstructed invariants material to this Review are:

- D1-D4 form an acyclic authority/concretization graph; each material normative claim has one current semantic owner.
- Repository presence, a workplan, test, review, historical success, generated view, or PEM entry does not manufacture authority.
- Concretization fidelity and abstraction adequacy are distinct. A child abstraction is defective if descendants can obey it while violating a material parent invariant.
- Legitimate mutually recursive definition is representable; circular claim warrant remains invalid. Definition/dependency structure never warrants its endpoints merely by existing.
- Authority mutation follows the owning acceptance lifecycle; unresolved blocking challenge or risk override cannot silently become unqualified accepted-current downstream.
- Relation absence proves independence only inside a scope reviewed complete for the relevant relation family.
- Evidence applicability is exact enough to prevent stale passing or stale failing observations from being used against the wrong subject, regime, execution basis or claim revision.
- Persistent/recovery state must distinguish current, complete, incomplete, stale, corrupt and historical state; recovery may not silently make an older state look current.
- Orchestration publication/retry must be idempotent or transactionally reconciled; durable completion cannot be inferred from file/ref presence alone.
- External, evidence and memory text is data, not instruction or authorization.
- Version-bound behavior and historical resources remain interpreted by their own accepted version; no self-adoption or retroactive reinterpretation is allowed.
- Tests and synthetic fixtures establish only the properties their oracle can discriminate; required checks that did not execute are not PASS evidence.

The workplan's §2 is materially consistent with those owners. The two blockers arise later, where the persistence/recovery mechanisms fail to realize §2's own stronger invariants.

### 1.3 PEM basis and HAS disposition

The claimed accepted/base memory was independently checked against main. At Review time main is exactly:

2585b73f00420daca185a4fbb9ac42a79473eda1

PROJECT-ENGINEERING-MEMORY.md at main and at the candidate is byte-identical, blob:

1561797125622f355f84eb27319f87e8fa4227d9

There is therefore no candidate-only PEM overlay.

The relevant HAS disposition is consistent with the accepted memory rather than inferred from the workplan's §0.3:

- **PC-001** remains AUTHORITY_BOUND only through its current versioning owner. The candidate preserves independently testable frozen prior-version Core/profile resources and keeps older work version-bound.
- **SP-002** remains EVIDENCE_ONLY. The candidate's record/candidate self-reference design is compatible with the lesson but the memory itself authorizes nothing.
- **FF-001** remains EVIDENCE_ONLY. Genesis/cutover/public-source identities are not treated as established before their owning records exist.
- **DS-001** remains EVIDENCE_ONLY and is directly relevant: revision 3 improves the qualification matrix substantially, but two current fixtures still normalize or omit the failure trajectories identified below.
- **SP-001** remains EVIDENCE_ONLY. Source-owner repair plus regeneration is a useful historical pattern, not an architectural requirement.

No PEM entry supplies independent evidence that the candidate is adequate.

---

## 2. Recheck of prior findings

### 2.1 441cf5c findings

| Prior finding | Revision-3 disposition | Independent basis |
|---|---|---|
| **Blocker A — same-subject SCC licensed circular warrant** | **Closed at the earliest owner** | §6.2 now gives relation types semantic roles and cycle classes. SIMULTANEOUS is definition-only; WARRANT, GOVERNING, EVIDENTIAL, PROVENANCE and LINEAGE cycles are acyclic; mixed SCCs are illegal. The same predicate is used at Admission and in S0 well-formedness, so absorbed content also fails closed. |
| **Blocker B — foreign structural declarations affected governance before intake** | **Closed at the earliest owner** | Observed declarations and effective structure are distinct. Σ changes only by admitted structural changes; absorption never changes it. Q and aff(Q) are S0 facts, and S2 ok(s) makes affected subjects invalid before any S3 intake scheduling. Tenure prevents old acceptance carryover. |
| **Blocker C — bounded anchoring lag contradicted P4** | **Original defect closed at the earliest owner; persistence family now has different blockers** | Append is provisional; no publication, dispatch or current answer occurs before q_a durable witnesses. q_a + r > N + f gives read/write intersection greater than f, so every qualifying read intersects every admission quorum in at least one honest witness. There is no admitted-state lag window. New failures are publication-recording and explicit-loss recovery, not the old anchoring defect. |
| **N6 — qualification lacked same-subject circular-warrant discriminator** | **Closed** | §22 now includes same-subject DERIVED_FROM, DEPENDS_ON, mixed SCC, unknown type, undeclared simultaneity, nested/sibling SDG and code-recursion counterexamples at both Admission and absorbed-tree paths. |
| **N7 — qualification encoded anti-rollback defect as expected success** | **Closed for the old defect; new DS-001 gap remains** | The L99/L100 fixture now expects ROLLBACK for an admitted L100. However, qualification does not test canonical recording of publication outcome and does not test post-LEDGER_LOSS derivation after a coordinated stale restore. See N2 below. |
| **N8 — foreign-intake qualification omitted structural-only mutations** | **Closed** | §22 expressly requires structural-only foreign cases including part/subject changes, membership, partition boundaries, domain changes, deleted manifest, challenge-bearing reparenting and restoration. |
| **N9 — Manual deferrals acceptable only with hard D4 boundary** | **Still valid and bounded** | §21 enumerates the deferred Architecture Manual obligations and §§23/25/28 retain a hard D4 gate. This remains acceptable only while that gate remains effective. |
| **N10 — routing regression test should respect DS-001** | **Closed** | The unchanged test blob parses frontmatter for current routing/status. Its only prose substring assertion is explicitly described as an archived-lineage representation guard and says it does not establish routing truth. |

### 2.2 f9d9de8 findings

| Prior finding | Revision-3 disposition | Independent basis |
|---|---|---|
| **B1 — refinement could manufacture child acceptance** | **Closed at the earliest owner** | Parts inherit subject routing, not acceptance. Promotion creates a new tenure and requires a qualified same-request acceptance. Legacy whole-document acceptance cannot be projected onto a section. |
| **B2 — currentness/validity had a self-supporting fixed point** | **Closed at the earliest owner** | S0/S1/S2/S3 is stratified; S1 is a finite later-record recursion; S2 is monotone on F < P < T with least-fixed-point semantics; Admission additionally rejects support-dependency cycles. |
| B2 policy self-reference | **Closed** | Ruleset adoption is an S0 ledger fact admitted under the previous ruleset. Derived policy validity does not define its own evaluator. |
| B2 negative obligation recursion | **Closed** | Readiness/discharge/impact are S3; lower strata do not read them. |
| **B3.1 — multi-ref atomic publication assumption** | **Closed; replaced by a new publication-reconciliation defect** | The multi-ref optimization is removed. Single-ref ledger append plus later product CAS is a portable architecture, but the outcome-recording sequence is internally circular; see Blocker A below. |
| **B3.2 — valid-prefix rollback can look current** | **Closed for ordinary rollback; replaced by a new explicit-loss defect** | Quorum-qualified currentness catches a known later admitted checkpoint. The new defect arises only after an explicit human LEDGER_LOSS abandons an unrecoverable admitted suffix and both canonical content surfaces have been restored consistently stale. |
| **B3.3 — confidentiality remediation did not remove leaked history** | **Closed at D3** | Rotation/revocation, replica inventory, new/private replacement lineage, old-lineage retirement witnessed by the old quorum, explicit destructive purge authorization, protected-main new-repository rule and yielded-guarantee disclosure form a coherent D3 incident contract. |
| **N1 — Architecture 1.6.0 transfer incomplete** | **Substantively closed; one traceability omission remains** | §16.2 now classifies all 26 frozen product invariants and the major frozen surfaces. See N3 for the separate archived Protocol-8 §36 row omission. |
| **N2 — routing test parsed prose as authority** | **Closed** | See 441cf5c N10 above. |
| **N3 — index overclaimed Stage H authority** | **Closed** | The index says it routes and authorizes nothing; Protocol 7 Stage H remains the owning closeout. |
| **N4 — widening underspecified** | **Closed** | The enclosing-scope chain, completeness selection, whole-tree fallback, uncovered region and fixed-point closure are explicit and deterministic. |
| **N5 — Change primitive / cross-repository boundary** | **Closed** | Change is an admission request, not a fifth primitive. Cross-repository authority is imported only through immutable pins and explicit external-acceptance/consultation records; atomic multi-repository admission is a declared non-goal. |
| **N6 — befe678 archival identity** | **Confirmed** | The archived hypothesis exists at blob af9c005b15c4d0cfc56b0efb4dfe6b032fa4d958. |

No prior blocker survives unchanged. The NO-PASS is caused by newly exposed defects in the repaired persistence/recovery architecture.

---

## 3. Blocking findings by earliest owner

## Blocker A — Concurrency/persistence owner: publication cannot both require a recorded observation and forbid the append that records it

### Concrete failure trajectory

Assume admission entry n is already admitted by q_a witnesses. Its admission record names candidate commit C_n and expected predecessor B_n.

1. The latest recorded observation of the integration ref says L = B_n.
2. By §15.3, publication state is therefore PENDING.
3. Admission performs the external compare-and-swap B_n -> C_n successfully.
4. The live integration ref is now C_n, but the ledger still contains only the earlier observation L = B_n.
5. §6.3 classifies publication outcome and live-ref movement as Observation records and says every record enters through Admission.
6. §15.3 also says publication state is derived from the ledger plus the latest **recorded** live-ref observation.
7. Therefore the canonical state is still PENDING until a new Observation recording L = C_n is appended.
8. But §15.3 states that entry n+1 may be appended only after entry n's publication is resolved.
9. The Observation needed to make publication resolved cannot legally be appended while publication is unresolved.

The OVERTAKEN path has the same problem. Absorbing the foreign live ref is itself a new canonical entry, yet the previous publication is defined as unresolved until the observation/absorption exists.

If an implementation instead treats the ambient live ref as sufficient to resolve publication before recording it, the other half of the contract fails: canonical progression now depends on nondeterministic external state that C3 and §6.3 say enters derivation/control only as a recorded typed fact. A replay from the ledger cannot reconstruct why the append gate opened.

This is not a mere omitted D4 API. It is a contradictory D3 transition rule at the ledger/effect boundary.

### Earliest owner

The earliest owner is the D3 persistence/concurrency publication state machine: §6.3 record ownership plus §15.3 commit/publication ordering, under C3/C4.

### Minimum repair direction

Define one explicit reconciliation transition that can legally occur while the preceding admission's publication is unresolved. For example:

- after the external CAS attempt, Admission may append exactly one publication-reconciliation Observation or absorption entry as the only permitted successor while publication is unresolved;
- that entry is itself single-ref appended and quorum-admitted;
- PUBLISHED or OVERTAKEN is then derived from that admitted observation;
- only after that reconciliation entry is admitted may normal admission requests resume.

The repair must also specify idempotent restart behavior for: CAS succeeded but observation append did not; observation appended but not quorum-admitted; foreign movement occurred between CAS and observation; and the OVERTAKEN absorption path.

An alternative architecture may keep publication outcome strictly in operator state, but then it must remove publication outcome from canonical records/derivation and re-establish replay, audit and next-admission correctness. Merely saying "observe after crash" does not close the cycle.

---

## Blocker B — Storage/recovery and authority-lifecycle owner: LEDGER_LOSS can resurrect retained pre-loss authority after a coordinated stale restore

### Concrete failure trajectory

Let A be a subject.

1. At admitted ledger position L10, A is an effective subject in tenure τ1 with passing acceptance j_A on exact triple (A, S, R).
2. At admitted L11, A is lawfully demoted into part of composite P. That admission ends τ1. The product repository is also published with the new manifest, so the current repository says A is a part.
3. Later, storage fails beyond the declared fault bound. All reconstructable copies of the admitted L11 suffix and the newer product objects are lost, but a witness checkpoint or participant high-water mark still proves that a later admitted head H11 existed.
4. The operator restores a stale backup containing both the ledger through L10 and the product tree as of L10. The two restored canonical content surfaces are internally consistent: Σ reconstructed from the retained ledger says A is a subject, and the restored manifest says the same.
5. Currentness qualification correctly detects ROLLBACK because H11 is still known. No suffix copy can be recovered, so the human invokes the architecture's explicit LEDGER_LOSS / witness-redesignation recovery and names H11 abandoned.
6. After that explicit loss is accepted, derivation runs on the retained prefix plus the loss record. The current workplan gives LEDGER_LOSS no recovery epoch that invalidates retained authority across the unknown lost interval.
7. Q is empty, because observed structure and Σ both came from the same stale point. aff(Q) therefore supplies no protection.
8. A's effective signature again appears uninterrupted in the retained history. j_A remains in that retained history and can satisfy the current-tenure ACC filter.
9. A's old acceptance is therefore capable of becoming current again even though the system positively knows that an admitted interval after j_A existed and has been abandoned.

The lost interval may have contained not only demotion but a challenge, revocation, supersession, ruleset adoption, domain/mode change, confidentiality action, or other event that made the retained authority non-current. The witness hash proves that history existed but does not reveal enough semantics to reconstruct which retained claims remain safe.

Revision 3's stated repair for ledger truncation assumes the product repository still declares the lost demotion, producing Q. That is a useful defense for a one-sided ledger loss, but it is not a general recovery invariant. Restoration from a stale backup of both stores is explicitly within the requested failure surface.

This trajectory does not dispute the information-theoretic limit. The architecture cannot reconstruct lost facts. Precisely because it cannot, it may not silently preserve retained positive authority whose continuity crosses the known lost interval.

### Earliest owner

The earliest owner is the D3 storage/recovery and authority-lifecycle contract for LEDGER_LOSS / witness-set redesignation, including tenure/currentness after an admitted suffix is explicitly abandoned.

### Minimum repair direction

A human-gated abandonment of an admitted suffix must create an explicit conservative recovery boundary independent of whether the restored product tree happens to agree with the retained ledger. At minimum:

- record the last retained head and the highest known lost checkpoint;
- start a new recovery continuity/tenure epoch for authority whose validity could have changed in the lost interval;
- make retained support/acceptance non-current until re-established, unless an independently durable summary proves a narrower unaffected set;
- if the contents of the lost interval are unknowable, conservatively requalify all authority/evidence whose currentness could have been changed there rather than inferring safety from a stale-consistent tree;
- keep old records historical and citeable, but do not allow them to become current merely because the recovery tree matches their old structure.

Qualification must restore **both** ledger and product to the same stale pre-change snapshot, acknowledge a known later admitted checkpoint by LEDGER_LOSS, and then prove that j_A, stale challenges/revocations, and old ruleset-dependent acceptance do not revive without new owner action.

---

## 4. Non-blocking findings, ranked by consequence

### N1 — Medium-high: warrant-validity mode needs an explicit intra-subject rule and positive discriminator

Revision 3 widens validity-mode basis entries from governing prerequisites to governing **or warrant** prerequisites, while Admission step 5 rejects any validity entry naming the record's own subject or one of its parts. This is safe against self-support but leaves the intended positive case under-specified.

A legitimate subject G may contain parts a and b with an acyclic authored relation b DERIVED_FROM a. That is expressly legal in §6.2. If an acceptance/evidence rule mechanically assigns validity mode to every direct warrant prerequisite, the basis entry for a routes through subj(a) = G and Admission rejects the judgment as self-validity. If it instead records intra-subject warrant as content reliance, the case is representable.

The Architecture Manual is already assigned exact per-judgment mode composition, so no current invariant is necessarily violated. The D3 abstraction should nevertheless state the routing rule explicitly: intra-subject warrant must not become self-validity; inter-subject warrant may use validity where the rule requires it; subject-projected support cycles remain rejected. Add a positive qualification case for a legal same-subject acyclic warrant graph. This prevents the new warrant mode from causing accidental over-invalidation or making a legitimate claim structure unadmittable.

### N2 — High: §22 does not discriminate either new persistence blocker

The qualification program is much stronger than revision 2, but two cases currently normalize the candidate's own assumptions:

- "crash after the compare-and-swap, before the outcome is recorded (observed as PUBLISHED)" assumes the publication outcome can become a legal canonical observation; it does not exercise the no-next-entry-until-resolved gate that prevents recording it;
- the LEDGER_LOSS truncation fixture assumes the repository still declares the lost demotion, and the stale-backup fixture stops at ROLLBACK / LEDGER_LOSS. Neither derives current authority after restoring both ledger and product to one stale-consistent snapshot and explicitly abandoning the missing admitted suffix.

Under DS-001 these are insufficient discriminators for the claimed properties. They should be repaired after the architecture owner is repaired; they cannot themselves define the repair.

### N3 — Medium: archived Protocol 8 capability-transfer table omits an explicit §36 disposition

§18.1 says every section of the archived consolidated Protocol 8 workplan is disposed. The table covers §§1-35 and §37, but has no explicit row for archived §36 "Final target."

No material capability loss was found: §36's substance — semantic artifacts carry meaning; agents reason; evidence supports/challenges; bounded schemas communicate control facts; rules validate transitions; one orchestrator commits workflow state; replay determinism is control determinism, not deterministic scientific reasoning — is preserved by the candidate's semantic/control separation, C2/C3, single Admission writer, and §14 machinery-stop boundary.

The defect is traceability, not architecture semantics. Add a §36 row so the "every section" claim is literally true and future transfer reviews do not need to reconstruct this mapping indirectly.

### N4 — Low, bounded: Architecture Manual deferrals remain acceptable only while the D4 gate remains hard

Several frozen Architecture 1.6.0 details are deliberately Deferred: composition-root realization, benchmark fields, execution lifecycle detail, capability keys, public API/SPIs, configuration layout, component fitness checks and mappings of existing Core records.

That is acceptable for this prospective D3 workplan because §21 enumerates them and §25 makes an independently reviewed and accepted Architecture Manual a prerequisite for D4. If that gate weakens, these immediately become handoff blockers rather than harmless deferrals.

### N5 — Positive bounded finding: the strong P4 quorum inequality is sound for its stated fault model

For a witness universe of size N, any admission quorum Q_a and read quorum R satisfy:

|Q_a ∩ R| >= q_a + r - N

The requirement q_a + r > N + f therefore guarantees intersection size greater than f. With at most f faulty witnesses, at least one intersection member is honest and retains the admitted checkpoint. Thus a qualifying read cannot hide a known admitted head merely by choosing a different read quorum.

This is a safety result, not an availability guarantee. Configurations may still fail closed if insufficient witnesses respond, which the workplan states honestly. The information-theoretic limit for a never-admitted entry whose every copy/checkpoint disappears is also stated honestly.

---

## 5. Independent out-of-matrix abstraction-adequacy pass

The following trajectories were attempted independently of the workplan's §27 matrix.

| Attack | Result | Independent disposition |
|---|---|---|
| Circular warrant hidden inside one composite subject | **Blocked** | WARRANT cycle classes are ACYCLIC regardless of common subject. |
| Circular warrant hidden inside an SDG | **Blocked** | Only DEFINITIONAL / SIMULTANEOUS edges may participate in an SDG cycle; mixed cycles fail. |
| Circular warrant spanning subjects through governing, evidence, provenance, supersession or equivalence support | **Blocked** | Relation-cycle classes plus Admission's subject-projected support-dependency acyclicity reject the cycle. |
| Self-declared simultaneous-definition group treated as warrant | **Blocked** | SDG is semantic content requiring subject acceptance and grants no warrant. |
| Legitimate mutually recursive scientific/numerical definition | **Survives** | Explicit SDG + definitional edges is legal; no warrant is inferred. |
| Recursive code/import/call structure | **Survives** | Derived STRUCTURAL / NEUTRAL edges carry context only and are excluded from warrant/validity. |
| Foreign structural-only change while source subject is challenged | **Blocked** | Σ does not change; Q/aff(Q) invalidates affected governance; adoption is frozen. |
| Foreign structural-only change that changes a challenged destination subject | **Blocked** | Admission freeze covers source and destination membership/scope changes. |
| Demotion then restoration with same bytes/scope | **Blocked in ordinary history** | New subject tenure requires new acceptance; prior ACC is excluded. |
| Scope/domain/mode oscillation | **Blocked in ordinary history** | Signature change ends tenure; domain change needs current-owner qualification; mode change is lifecycle-governed. |
| Ledger truncation with current product repository still present | **Blocked** | Lost structural admission disagrees with observed manifest and becomes quarantine. |
| Ledger loss plus coordinated restoration of both ledger and product to the same stale snapshot | **FAILS** | Q is empty and no recovery epoch invalidates retained pre-loss acceptance. Blocker B. |
| Version rollback to LEGACY(p) | **Blocked from resurrection** | Mode transition ends tenure and requires a fresh LEGACY_ACCEPTANCE import. |
| Ruleset change that reclassifies an existing relation | **Fails closed** | Affected current subjects become ill-formed; historical views retain historical vocabulary. |
| Challenge escape by rescoping the challenged source | **Blocked** | Challenge freeze applies before the structural change. |
| Challenge escape by changing the destination subject | **Blocked** | Destination membership/scope changes are frozen too. |
| Realignment used to bypass quarantine | **Blocked** | Realignment returns observed declarations to Σ; it does not adopt foreign structure. |
| Adoption used to ratify foreign structure merely because it exists | **Blocked** | Adoption is re-authoring under current rules, including challenge, mode and promotion checks. |
| Mechanical adoption of governance-neutral delta changes subject authority | **No violating path found** | "Neutral" is restricted to an intra-subject leaf repartition with unchanged subject regions/kind/domain; subject acceptance does not move. Content/completeness effects still derive normally. |
| Deleted unit manifest | **Blocked from authority mutation** | Effective structure stays in Σ; missing observed declarations produce quarantine and governance invalidity. |
| Inline anchor declares new role/kind/domain/scope | **Blocked by abstraction** | Inline anchors may delimit leaf spans only and inherit governance fields from the manifest. |
| Overtaken publication silently overwrites foreign work | **Intended behavior safe, transition incomplete** | CAS never overwrites foreign work; OVERTAKEN absorbs it, but canonical recording is blocked by Blocker A. |
| Incomplete dependency knowledge treated as independence | **Blocked** | Missing completeness widens to whole governed tree plus uncovered region and is labeled UNBOUNDED. |
| Quarantined structure narrows widening | **Blocked** | Scope chain is built from effective Σ, not quarantined declarations. |
| Stale evidence reused after role/tenure change | **No violating path found** | Evidence may remain historically applicable to bytes, but it cannot substitute for the required current-tenure subject acceptance; target/execution bases still govern use. |
| Vocabulary evolution during quarantined intake | **Fails closed** | Σ/Q unchanged; later adoption is under then-current rules; unknown/reclassified relation types invalidate affected subjects. |
| Historical profile reinterpreted after schema/ruleset evolution | **Blocked** | Historical views use the ruleset/schema at their position; legacy work is version-bound. |
| Crash after ledger append before quorum | **Safe** | Entry is provisional and no external effect/current answer depends on it. |
| Crash after quorum before publication | **State is conceptually recoverable** | Admission knows an admitted head and retries publication, but durable publication-outcome recording is Blocker A. |
| Crash after publication CAS before publication observation is recorded | **FAILS** | No legal canonical append is available to record the observation that would resolve the publication. Blocker A. |
| Conflicting witness checkpoints | **Fails closed** | FORK requires human-gated resolution; no automatic merge. |
| Witness loss within fault bound | **Safe for currentness** | Quorum inequality preserves at least one honest admission/read intersection. |
| Witness loss beyond bound | **Explicit loss path only** | UNQUALIFIED until redesignation/loss handling; post-loss authority continuity is defective under Blocker B. |
| Read repair fabricates a checkpoint | **Blocked** | It may relay only an authenticated checkpoint; it cannot forge one. |
| Witness-set redesignation silently ignores an accessible old quorum | **Blocked by stated contract** | Where reachable, redesignation must be admitted under both old and new quorums; unavailable-old-quorum case is explicit human loss acknowledgment. |
| Restore product repository from stale backup while ledger remains intact | **Blocked** | Live-ref movement is absorbed; revisions drift and structural deltas quarantine. |
| Restore ledger from stale backup while product remains current | **Blocked** | ROLLBACK plus Q after loss keeps old structure from silently becoming valid. |
| Restore both to same stale backup after known admitted suffix is unrecoverable | **FAILS** | See Blocker B. |
| Foreign force-push/manual merge | **Blocked from governance promotion** | Absorption changes observed content only; foreign structure is quarantine. |
| Legacy and native authority simultaneously current for one subject | **Blocked** | One governance mode per subject; cutover/mode transitions end tenure; legacy edits after cutover are foreign. |
| Cross-repository imported authority later becomes rejected/forked/retired | **Bounded and explicit** | Adverse later consultation supersedes prior consultation; external status is honestly only as fresh as the latest consultation. |
| Confidentiality remediation leaves old lineage presentable as current | **Blocked under stated witness assumptions** | Old witness quorum receives a retirement statement; old mirrors become historical-only. |
| Agent PASS treated as closure | **Blocked** | PASS is a judgment/proposal; discharge is derived. |
| Agent PROVISIONAL submission treated as admitted | **Blocked** | submit reports ADMITTED only after q_a witness admission. |
| Agent self-declared equivalence/completeness treated as independent authority | **Blocked where independence required** | Such a declaration cannot be sole qualifier of its own change. |

The two failed trajectories are exactly the two blockers above. No additional defect was invented merely to fill the matrix.

---

## 6. Strata and derivation assessment

### S0

S0 contains only ledger/content facts: ruleset in force, observed tree, admitted effective structure, quarantine, affected subjects, tenure, revisions, relations, well-formedness and syntactic supersession. Effective structure is derived from admitted structural changes; repository presence alone cannot mutate it. Quarantine and well-formedness are therefore lower-stratum facts in substance, not labels attached after validity.

**Disposition: coherent.**

### S1

Challenge resolution is a recursion over strictly later resolver records. Because every dependency moves forward in ledger position and the ledger prefix is finite, reverse-position evaluation is well-founded even though negation appears. A challenged dismissal/override/upholding can conservatively restore the earlier block.

**Disposition: coherent.**

### S2

Support uses the finite lattice F < P < T with monotone min/max equations and a least fixed point. Ungrounded positive support cycles therefore evaluate F. Admission also maintains an acyclic support dependency graph for valid admitted input, which makes normal evaluation topological rather than requiring iteration.

well_formed, aff(Q), τ and ok are S0 constants. S2 does not read S3. The original f9d9de8 multiple-fixed-point defect is not reproduced.

**Disposition: coherent, with N1 basis-mode clarification needed.**

### S3

Obligations, discharge, readiness, drift, impact, context and integrity explanations consume S0-S2 but nothing below reads them. This keeps non-monotone consequence logic out of acceptance/currentness.

**Disposition: coherent.**

### Currentness outside derivation

Witness qualification chooses which authenticated prefix may be presented as current. It does not change derive(L_n, content), so C2/C3 are not broken merely because currentness is external to D_n. The same prefix still derives one state.

**Disposition: coherent.**

The derivation is therefore single-valued and well-founded. The Review's NO-PASS does not come from S0-S3 recursion.

---

## 7. Persistence, currentness and recovery assessment

### 7.1 Strong P4

The revision-3 P4 contract is materially stronger than revision 2 and internally consistent for ordinary operation:

- append is not admission;
- admission requires q_a durable witness acknowledgments;
- no current answer, dispatch or product publication depends on a provisional entry;
- every current assertion names a qualified head;
- any read quorum intersects any admission quorum in more than f witnesses;
- ROLLBACK, FORK, BEHIND, PROVISIONAL and UNQUALIFIED are distinct;
- an admitted head cannot be hidden by a valid read quorum within the declared fault bound.

The workplan also states the real information-theoretic limit: if an entry never became admitted and all its copies/checkpoints disappear, the system cannot distinguish that world from one in which it was never appended. No stronger claim is made.

### 7.2 Single provisional entry and witness redesignation

At most one provisional entry is a sound simplification for normal operation: it prevents later state from depending on an unsettled predecessor. Human witness-set redesignation is an explicit exceptional recovery operation rather than a hidden second path.

The exception needs exact D4 protocol detail, but no independent safety counterexample was found solely from the quorum mathematics. Its major unresolved interaction is Blocker B: once an admitted suffix is explicitly declared lost, semantic continuity cannot be inferred from a retained stale prefix.

### 7.3 Publication

The separation between canonical admission and external product publication is the correct architectural direction and removes the prior remote multi-ref assumption. However, the recorded-observation/append-gate cycle in Blocker A prevents the state machine from being executable as written.

### 7.4 Recovery

Ordinary replica rewind and one-sided stale restoration fail closed. Recovery after **known admitted history loss** is not conservative enough. The current design treats Q as if it were a universal detector of lost structural effects; it is only a detector of disagreement between the restored observed tree and retained effective structure. That is insufficient when both were restored to the same stale point.

**Overall persistence/currentness disposition: NO-PASS due Blockers A and B.**

---

## 8. Intake and quarantine assessment

The observed/effective split is a material repair:

- observed declarations are parsed from the current product tree;
- Σ is admitted structure only;
- Q is their delta;
- aff(Q) enters S0;
- S2 validity uses ok(s), so governance-affecting foreign structure invalidates before S3 intake scheduling;
- adoption is validated as current re-authoring, not historical ratification;
- realignment restores observed declarations to effective structure;
- source and destination challenge freezes apply during adoption;
- inline anchors cannot smuggle governance fields;
- uncovered content is UNCLASSIFIED.

The definition of affected subjects is neither obviously too weak nor globally invalidating: it includes subjects whose signature/regions change and containing subjects implicated by governance-affecting deltas, while governance-neutral intra-subject repartition does not invalidate an unchanged subject.

The architecture does not let raw repository presence change routing, acceptance or validity positively. Foreign content may reduce validity through drift, ill-formedness and quarantine, which is the intended fail-closed direction.

**Disposition: PASS at D3, except that OVERTAKEN intake cannot complete canonically until Blocker A is repaired.**

---

## 9. Minimum-justified architecture assessment

### 9.1 Four primitives

1. **Unit** is necessary to express adaptive content granularity, subjects, scope, tenure and migration without making files the semantic atom.
2. **Relation** is necessary to distinguish definition, warrant, governing, evidence, lineage, provenance and structural dependencies with different cycle/completeness rules.
3. **Record** is necessary for nondeterministic observations, judgments, admissions and lifecycle events that cannot be recomputed from content.
4. **Basis** is necessary as a first-class semantic relation between a record and the exact content/records it relied on; treating it as an incidental record field would not remove the concept or its currency semantics.

No separate Change, graph-family, epoch, dirty marker, reinstatement, SDG-node, or stored effective-structure primitive is justified.

**Disposition: the four-primitive set remains minimum-justified.**

### 9.2 Seven components

The logical ownership split remains justified:

- Content Model: content/declaration/revision interpretation;
- Analyzers: derived relations with explicit completeness limits;
- Ledger Store: persistence/authentication/current-head qualification;
- Derivation Engine: pure S0-S3 state;
- Admission: sole canonical writer and validation boundary;
- Dispatcher: operational scheduling/execution without workflow authority;
- Interface: transport/rendering without state ownership.

Some could share a process in D4, but collapsing their **ownership** would blur purity, persistence, execution or authority boundaries. No eighth component is needed for quarantine, SDGs or witness admission.

**Disposition: minimum-justified as logical components.**

### 9.3 Persistent surfaces

The six surfaces in §15.1 each have an explicit owner and recovery story:

- content store;
- ledger;
- witness checkpoints;
- derived index;
- operator state;
- transport.

The witness surface is justified by P4; the operator journal is justified by external-effect reconciliation; derived state remains rebuildable rather than becoming a second authority.

The surface inventory is therefore not overbuilt. Its **transition protocol** is nevertheless insufficient because of Blockers A and B.

---

## 10. Capability transfer

### 10.1 Frozen Orchestrator Architecture 1.6.0 and implemented Core

orchestrator/docs/architecture.md is independently verified as:

- architecture_id SDP-ORCHESTRATOR;
- architecture_version 1.6.0;
- status frozen;
- blob 39e6de727f6c35402962509d30d947962992eaad.

The repository tree at the candidate contains only orchestrator/src/sdp_orchestrator/core as an implemented module package; Tracker, Adapter and Scheduler module packages are not present. The Core package exposes one sdp CLI/composition root and version/profile-separated protocol-source resolution, with frozen packaged profile resources including 6.x and 7.0 lines.

§16.2 now disposes all 26 product invariants individually and separately covers the major frozen surfaces. The important transfers are lossless at the D3 level:

- Core remains independently usable for older version-bound work;
- profile/source selection remains exact-version bound;
- no duplicated workflow authority is introduced for native SSDS scopes;
- query and mutation remain separated;
- one mutating run / one worktree survives;
- manual/direct routes keep one logical vocabulary;
- resource/routing choices remain subordinate to workflow intent;
- secrets/private operational state remain outside product repositories;
- the old four-level ladder is explicitly superseded rather than silently layered beneath SSDS.

Deferred exact APIs/configuration/lifecycle details are acceptable only because §21 and §25 gate D4.

**Disposition: no material capability loss found.**

### 10.2 Archived consolidated Protocol 8 lineage

The archived consolidated workplan is blob:

c229202fd282840571dec34d352a5255e23042e3

The revision-3 §18.1 mapping carries or explicitly replaces the major semantic/control/replay/evidence/concurrency/security/migration/versioning guarantees. The selected Git ledger is a deliberate change from the predecessor's private-store default and is justified at D3 by explicit concurrency, privacy, history and ownership machinery rather than by repository convenience.

One traceability omission remains: archived §36 Final target has no dedicated row even though its substance is preserved elsewhere. See N3.

**Disposition: materially lossless, minor traceability repair needed.**

### 10.3 Archived befe678 hypothesis

The archived hypothesis is blob:

af9c005b15c4d0cfc56b0efb4dfe6b032fa4d958

The candidate preserves its useful capabilities without retaining the unnecessarily large graph-native mechanism set: typed relations, derived code dependencies, evidence applicability, reviewed modular plans, deterministic explainable context, safe parallelism, repository intake/explainability, progressive migration, bottom-up discovery/top-down acceptance, crash recovery and private operator state.

The revision-3 relation-role/SDG split also repairs a capability that the f9d9de8 concretization had weakened: structural refinement no longer falsely transfers semantic acceptance.

**Disposition: no material capability loss found.**

---

## 11. Protocol 7 Stage H, routing and authorization boundary

The active Protocol 7 consolidated workplan at the candidate is blob:

36e2da1cc11d919ca4b1974996f77341dc71d3c1

Its Stage H explicitly owns the Protocol 8 inheritance reconciliation after Protocol 7's own Review/ratification closeout. That reconciliation:

- advances the pre-cutover baseline to Protocol 7 recovery/public fallback while keeping them distinct;
- binds Protocol 7 gate-evidence and RSR semantics as inputs;
- selects no SSDS 8 architecture;
- authorizes no SSDS 8 D4;
- recommends rather than self-adopts a governing-version change.

The authority index says explicitly that current_handoffs is a routing projection and "routes and authorizes nothing." It names both the active Protocol 7 handoff and the prospective SSDS 8 workplan without creating dual semantic authority. It also states Protocol 7 inheritance is NOT FINAL and SSDS 8 D4 is NOT AUTHORIZED.

The candidate workplan keeps native/legacy governance mutually exclusive per subject and permits shadow comparison only with one side explicitly non-authoritative.

**Disposition: Stage H ownership is preserved; the index is routing-only; no dual current authority is created; D4 remains unauthorized.**

---

## 12. Qualification-program assessment

§22 is substantially improved and, for the repaired relation/quarantine/currentness mechanisms, usually discriminates the claimed property rather than checking labels.

Strong additions include:

- positive legitimate recursive-definition cases and negative warrant-cycle cases;
- Admission plus absorbed-tree variants;
- structural-only foreign mutation cases;
- source/destination challenge escape;
- demotion/restoration tenure cases;
- unknown relation vocabulary and ruleset reclassification;
- whole-tree dependency widening;
- quorum L99/L100 rollback;
- stale profile/history isolation;
- confidentiality lineage retirement;
- agent PASS/proposal boundaries.

However, DS-001 still applies to the two new blockers:

1. the publication failpoint says a post-CAS state is "observed as PUBLISHED" without proving the canonical observation can legally be appended;
2. LEDGER_LOSS fixtures do not restore ledger and product together to a stale-consistent prefix and then inspect derived authority after the loss record.

Therefore §22 cannot rescue the architecture. Green future implementations of the current matrix could still satisfy every listed expectation while retaining both blockers.

---

## 13. Evidence

### 13.1 Executed during this Review

Read-only repository identity/content inspection was performed through the GitHub repository interface at exact immutable refs, including:

- branch head at start and immediately before this record;
- candidate commit lineage;
- required blob identities;
- PROTOCOL-RELEASE-STATE.yaml;
- immutable 6.6 public-source owner files at 22f4bdba53795da3a6f13f162529f3a843fc37ae;
- current/main PEM and candidate PEM;
- the candidate workplan and authority index;
- both prior Review records as hypotheses;
- the consolidation regression test;
- frozen Orchestrator Architecture 1.6.0 and implemented Core layout/source;
- archived consolidated Protocol 8 lineage and befe678 hypothesis;
- active Protocol 7 Stage H.

The local execution environment was also probed:

- Python: 3.13.5;
- Git: 2.47.3;
- no local checkout of scientific-software-development-protocol was present under the available workspace roots;
- git ls-remote against the repository failed with: "Could not resolve host: github.com".

That network/environment failure is evidence only of execution unavailability. It is not a repository failure.

### 13.2 Requested repository acceptance workflow — unavailable evidence

The following requested commands were **not run**, because there was no local checkout and the execution environment could not resolve github.com to obtain one:

| Command | Result |
|---|---|
| python source/release_state.py | **UNAVAILABLE / NOT RUN** |
| python source/project_engineering_memory.py PROJECT-ENGINEERING-MEMORY.md | **UNAVAILABLE / NOT RUN** |
| python -m unittest discover -s tests | **UNAVAILABLE / NOT RUN** |
| python source/build_skills.py --output <tmp> | **UNAVAILABLE / NOT RUN** |
| python source/validate_packages.py --dist <tmp> | **UNAVAILABLE / NOT RUN** |
| python source/check_dist.py --expected <tmp> --committed dist | **UNAVAILABLE / NOT RUN** |
| git diff --check | **UNAVAILABLE / NOT RUN** |
| python orchestrator/scripts/generate_protocol_snapshot.py --check | **UNAVAILABLE / NOT RUN** |
| python orchestrator/scripts/run_core_tests.py | **UNAVAILABLE / NOT RUN** |

No prior CI result or prior Review's command result is substituted for these commands. Green tests could not close the semantic blockers in any event, but unavailable required evidence remains unavailable evidence.

### 13.3 Reused evidence

No prior Review verdict, workplan self-assessment, commit message, or prior command result was reused as proof that this candidate passes.

The prior Review records were used only as hypothesis lists to ensure every earlier finding was re-attacked. Their conclusions were independently re-derived or rejected.

### 13.4 Evidence limitations

The Review is therefore decisive on the two semantic D3 blockers because they are contradictions/counterexamples in the candidate architecture text itself, but it does **not** establish repository acceptance-workflow health for 8a75346. A later repaired candidate still needs the requested executable acceptance workflow in an environment with a checkout and required dependencies/network.

---

## 14. Independently reconstructed invariant disposition

| Governing concern | Disposition at 8a75346 |
|---|---|
| Abstraction / concretization | **NO-PASS overall**: architecture is strong enough in most areas, but the recovery abstraction admits a stale-consistent descendant state that violates no-resurrection intent. |
| D3 architecture ownership | **NO-PASS**: component ownership is clear, but publication/recovery transitions are not fully coherent. |
| Workflow / authority lifecycle | **NO-PASS due Blocker B**: ordinary tenure/challenge lifecycle is coherent; explicit loss can bypass continuity. |
| Semantic definition / traceability | **PASS at D3**: SDGs distinguish legitimate recursive definition from circular warrant; unknown semantics fail closed. |
| Evidence / dependencies | **PASS with N1 clarification**: target/execution dependency and completeness/widening are sound; warrant-basis mode needs an explicit positive rule. |
| Testing / qualification | **NO-PASS as closure evidence**: §22 is strong but misses the two new blocker trajectories. |
| Concurrency / orchestration | **NO-PASS due Blocker A**: serial admission is coherent; external publication reconciliation cannot be canonically recorded as written. |
| Storage / recovery | **NO-PASS due Blockers A and B**. |
| Git / repository semantics | **PASS at D3**: Git is substrate, not workflow authority; product ref is not silently authoritative; destructive operations remain separately authorized. |
| Security / trust | **PASS at D3**: authenticated entries, protected surfaces, closed schema, untrusted-agent boundary and confidentiality lineage procedure are explicit. |
| Versioning / compatibility | **PASS at D3**: historical profiles remain version-bound; rollback and adoption do not silently reinterpret history. |
| PEM / HAS | **PASS**: accepted/base memory verified; PC-001 binding preserved; evidence-only families not promoted. |
| Capability transfer | **PASS with N3 traceability repair**: no material capability loss found against frozen Architecture 1.6.0, archived Protocol 8, or befe678. |
| Protocol 7 inheritance boundary | **PASS**: Stage H still owns reconciliation; current index does not authorize it. |
| Minimum architecture | **PASS structurally**: four primitives, seven logical components and six persistent surfaces remain justified; persistence protocol still needs the two blocker repairs. |

---

## 15. Required repair set for the next Review

The minimum D3 repair is narrow:

1. repair §15.3 so publication success/overtaking has one legal canonical reconciliation path that does not depend on an unrecorded external fact and does not deadlock behind the no-next-entry rule;
2. repair LEDGER_LOSS / witness-redesignation semantics so abandoning a known admitted suffix creates a conservative authority-continuity boundary even when both ledger and product are restored to the same stale snapshot;
3. add §22 counterexamples that execute those exact repaired paths rather than presupposing their outcome;
4. clarify the intra-subject versus inter-subject warrant-validity basis rule and add a positive same-subject acyclic-warrant qualification case;
5. add the missing archived Protocol 8 §36 capability-transfer row.

Items 1-2 are blockers. Items 3-5 are required follow-through / non-blocking closure repairs and should not be allowed to redefine the architecture merely to make tests pass.

---

## 16. D4 authorization statement

**SSDS 8 D4 remains NOT AUTHORIZED.**

This NO-PASS independently blocks D4 on the candidate.

Even a future D3 PASS would **not** itself authorize D4. Before D4, the owning process must still complete:

1. Protocol 7 Stage H inheritance reconciliation against the final accepted Protocol 7 state; and
2. a separately reviewed and accepted SSDS 8 Architecture Manual that closes every §21 obligation and the resulting final D3 handoff.

This Review invents no final Protocol 7 release, recovery, gate-evidence, inheritance, adoption or cutover identity.
