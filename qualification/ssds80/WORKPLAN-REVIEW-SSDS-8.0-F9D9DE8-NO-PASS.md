# SSDS 8.0 prospective architecture workplan — independent D3 Review

**Governing SSDP:** 6.6.0  
**Repository:** `hjin98/scientific-software-development-protocol`  
**Branch inspected:** `ssds-8.0-graph-native-architecture`  
**Candidate under Review:** `f9d9de8f466963cbd4e53e85e44a7ab262952ffc`  
**Candidate branch head at Review start and final recheck:** `f9d9de8f466963cbd4e53e85e44a7ab262952ffc`  
**Intervening commits:** none  
**Primary workplan:** `workplans/active/SSDS-8.0-GRAPH-NATIVE-DETERMINISTIC-ORCHESTRATION-ARCHITECTURE.md`  
**Primary workplan Git blob:** `aba4e967a2ecda9e82a544317b1ead47d8a690c5`  
**Review method:** independent D3 reconstruction and falsification under SSDP 6.6.0; the workplan's own diagnosis/comparison/inheritance claims were treated as hypotheses, not evidence.

## 1. SERIOUS CHALLENGE

**none**

I found no credible evidence that the accepted SSDP 6.6 governing goals are contradictory, inadequate, or unrealizable. The blocking findings below are defects in the proposed SSDS 8 concretization. They do not require reopening accepted 6.6 doctrine.

## 2. Verdict

# **NO-PASS**

Scope: prospective SSDS 8.0 D3 architecture workplan at exact candidate `f9d9de8f466963cbd4e53e85e44a7ab262952ffc`, bound to workplan blob `aba4e967a2ecda9e82a544317b1ead47d8a690c5`, including the routing index, consolidation regression test, archived befe678 hypothesis, predecessor inheritance, frozen Orchestrator Architecture 1.6.0 implications, and the current implemented Core surfaces material to the proposed supersession.

The design direction is materially stronger and smaller than the befe678 hypothesis in several respects: one Admission writer, basis-bound judgments, pure derivation rather than mutable lifecycle state, a clean semantic/machine boundary, explicit optimistic-admission residual risk, one intake route, and a low-bookkeeping agent interface are coherent. However, three architecture-level blockers remain. The first also survives the requested out-of-matrix abstraction-adequacy attack and is therefore decisive independently of the workplan's own qualification matrix.

A future PASS of this workplan still would **not** authorize SSDS 8 D4. Protocol 7 inheritance must first be reconsolidated after Protocol 7 closes, and the SSDS 8 Architecture Manual must resolve the workplan's D3 closure obligations and itself receive the required independent Review/acceptance.

## 3. Blockers, grouped by earliest affected owner

### B1 — Abstraction/concretization and semantic-definition boundary: byte-preserving refinement can mechanically manufacture accepted child authority

**Earliest affected owner:** accepted SSDP 6.6 abstraction/concretization and semantic-definition doctrine; then D3 migration/intake architecture.

**Failure trajectory / counterexample**

1. A legacy process has accepted one coarse authority unit `P` whose semantics are holistic across two regions `A` and `B`. The accepted claim may depend on coupling between the two regions even when the bytes contain no explicit authored relation encoding that coupling.
2. SSDS imports the exact accepted revision of `P` through `LEGACY_ACCEPTANCE`.
3. During migration, §12.2 performs a byte-preserving structural partition of `P` into child units `A` and `B` with unchanged bytes and unchanged declared relations.
4. Under §12.2, the parent's **acceptance is carried to both children by rule** because, in the workplan's words, meaning did not change. Completeness is not carried, so closures widen conservatively to the former parent scope.
5. A later native obligation may now treat child `A` as an accepted unit/revision even though no qualified semantic actor judged that the old holistic acceptance of `P` is valid as an acceptance of the newly scoped semantic object `A`.
6. Every local migration rule can be satisfied: bytes are unchanged, scope is conserved, relations are unchanged, completeness is not transferred, and conservative widening keeps sibling context visible. Yet the system has changed the **scope and identity of what is accepted** without a semantic acceptance/equivalence judgment.

This is not cured by conservative widening. Widening protects dependency closure; it does not establish that an acceptance judgment whose subject was `P` semantically applies to newly created child subjects. It also conflicts internally with §6.4 and §14, which correctly state that a representation-preserving split/editorial-only determination is semantic beyond trivial byte identity and therefore requires a qualified `EQUIVALENCE` judgment.

The defect is especially consequential in deployment Case B: section-level units can be declared over accepted legacy documents, so a coarse historical acceptance can otherwise be projected into finer authority scopes during migration.

**Governing invariant violated**

- Accepted authority, not mechanical representation, defines what must be true.
- A lower-level mechanism, file split, graph relation, test, or historical acceptance does not gain authority to redefine the semantic subject of acceptance.
- Semantic equivalence/materiality beyond explicitly conservative mechanical identity is a semantic judgment owned by a qualified actor.
- Migration/reconstruction may use bottom-up evidence, but upstream/native authority is established only through its owner's acceptance.
- The control plane may operationalize accepted semantic facts; it may not manufacture them.

**Minimum repair direction**

Remove automatic child acceptance from byte-preserving refinement. A refinement may mechanically carry only bytes, region coverage, lineage/provenance, old-parent acceptance as historical context, and conservative dependency scope. Then choose one explicit semantic route:

- keep `P` as the accepted composite authority while children remain structural/reconstruction units; or
- require a qualified, scope-specific refinement/equivalence judgment establishing that the old acceptance is transferable to the proposed child semantic subjects, plus owner acceptance where the governing domain requires it.

The rule must make clear that byte identity proves content identity, not semantic-subject equivalence. Update §22 accordingly: its current expected migration case, “byte-preserving split carries acceptance but not completeness,” would otherwise qualify the defect instead of detecting it.

### B2 — D3 control semantics: §6.4 currency/validity recursion is not yet well-founded for simultaneous-definition groups and negative challenge dependencies

**Earliest affected owner:** D3 state/control semantics and semantic-definition dependency architecture.

**Failure trajectory / counterexample**

The workplan states that `current(j)` depends on every basis entry being satisfied, `satisfied_validity(u)` depends on `valid(u)`, and `valid(u)` depends on current acceptance judgments and absence of unresolved blocking challenges. It then permits an acceptance judgment to name members of its own simultaneous-definition group in its basis while claiming the recursion remains well-founded.

Take a legitimate simultaneous-definition group `{a,b}` and acceptance judgments `j_a`, `j_b` such that:

```text
current(j_a) requires valid(b)
valid(a)     requires current(j_a)
current(j_b) requires valid(a)
valid(b)     requires current(j_b)
```

This is permitted by the prose exception for “members of their own simultaneous group.” The Boolean equations admit at least two fixed points absent an additional group rule: all four false, or all four true. The derivation is therefore not uniquely defined merely by saying the group is legitimate. Conversely, if Admission is meant to reject this cycle, the simultaneous-group exception is underspecified and the stated support for simultaneous definitions is not realized.

The same issue is more dangerous when a `current` predicate contains negation through “no unresolved blocking challenge”: challenge activation/resolution must be stratified above the facts it challenges, or a challenge whose basis itself depends on the challenged currentness can create a non-stratified negative cycle. §6.5 says the rules are stratified, but §6.4 does not define the dependency strata or show that the admitted record/basis graph obeys them.

**Governing invariant violated**

- Derived state claimed deterministic must be a total, single-valued pure function of version-bound accepted inputs.
- Current normative ownership/dependency must remain acyclic except where a simultaneously defined semantic object has an explicitly coherent treatment.
- A machine state model must not permit circular self-acceptance or challenge logic whose truth depends on itself.

**Minimum repair direction**

Make simultaneous groups and challenge strata formal rather than prose exceptions. The simplest safe design is:

- treat a simultaneous-definition group as one atomic acceptance subject for validity purposes;
- give that group one acceptance judgment whose validity-basis can reference only predecessors in the condensed authority DAG, not member validity;
- derive member acceptance/validity from the accepted group plus their content revisions;
- place challenge creation/adjudication/supersession in explicit higher strata so negative dependencies cannot recurse into the challenged predicate; and
- define an admission-time dependency graph over every predicate-relevant record/basis edge, rejecting any cycle not covered by the atomic-group rule.

The Architecture Manual and qualification must include mutation/model cases for positive cycles, negative/challenge cycles, simultaneous groups, supersession, risk override, and a proof/test that one ledger/content/ruleset input has exactly one derived state.

Related but non-blocking formalization debt should be closed at the same time: define `unresolved blocking challenge` as a derived predicate, define scope-order selection for conservative widening unambiguously, and specify when a basis records transitive governing units in `content` versus `validity` mode so early-cutoff/backdating behavior is predictable rather than accidental.

### B3 — D3 storage/security/Git architecture: the in-repository canonical ledger adoption has not yet resolved the predecessor's concurrency, privacy, history, and ownership conditions

**Earliest affected owner:** D3 persistence/recovery, Git/concurrency, and security/trust-boundary architecture.

The predecessor deliberately allowed in-repository canonical control state only if a later D3 adoption resolved concurrency, privacy, history, and ownership consequences. §15.2 declares that adoption for the SSDS ledger. The design resolves some of the problem—one Admission writer, an authoritative replica, CAS, hash chaining, a separate ref, operator secrets outside the repository—but three material failure trajectories remain open.

#### B3.1 Atomicity is assumed from co-location rather than made a deployment capability

**Failure trajectory.** The authoritative ledger ref is remote and the integration ref is remote in the same Git repository. Admission validates a joint update and relies on “one reference transaction.” Remote multi-ref atomic update is not guaranteed merely because two refs share a repository: Git's atomic push is a negotiated server capability. If the server does not support it, an atomic push request fails; if the implementation does not require that capability, sequential ref updates can expose a ledger/product mismatch after a crash or rejection.

Git's published protocol explicitly treats `atomic` as a server-advertised capability. Therefore the architecture must either make that capability a checked deployment precondition or treat the integration-ref update as a reconcilable external effect even for same-repository remote operation.

**Invariant violated.** Canonical accepted-event/content publication must have one explicit atomicity boundary; partial canonical publication may not be mistaken for accepted state.

**Minimum repair.** Specify the local and remote cases separately. For a local authoritative repository, a local ref transaction may be the atomic boundary. For a remote authoritative replica, require/probe server atomic-ref capability and fail closed when absent, or use the ledger-first intent/outcome reconciliation protocol with a defined intermediate state. Qualification must inject a failure between the two ref effects on a server without atomic capability.

#### B3.2 Ledger rewind can be hash-valid and invisible to a fresh clone

**Failure trajectory.** An administrator, compromised credential, hosting restore, or mistaken force-push moves the authoritative ledger ref from head `L100` back to its valid ancestor `L80`. The hash chain from genesis to `L80` is intact. A fresh clone whose only authority anchor is that ref cannot infer that `L81..L100` ever existed. Product-ref movements are observable only if the missing ledger history still exists somewhere; the ledger's own rollback is not made detectable by its internal hash chain.

**Invariant violated.** Canonical history must not be silently lost or rewound while still passing integrity validation; recovery must distinguish a valid historical prefix from the accepted current head.

**Minimum repair.** Declare the threat/trust model and add an anti-rollback anchor appropriate to it: for example an independently retained signed/checkpointed head, append-only hosting policy with protected ref plus retained audit log, or a replica-reconciliation rule that refuses a shorter authoritative history when any trusted replica has a later compatible head. Define fork versus rollback versus loss explicitly. Test authoritative-ref rewind and fresh-clone recovery.

#### B3.3 The accidental-secret break-glass path preserves audit continuity but not confidentiality

**Failure trajectory.** A non-secret-by-contract ledger record accidentally contains a credential, private path/token, regulated datum, or other sensitive value. It is replicated to clones. §15.2 proposes a new lineage with a migration record, but the sensitive Git object remains in old object databases, clones, mirrors and possibly server retention. An append-only “old records retained” rule cannot itself remove the disclosure.

**Invariant violated.** Secrets/private telemetry must stay outside repository persistence, and a recovery contract must address the consequence of accidental inclusion rather than only logical lineage continuity.

**Minimum repair.** Define prevention plus breach recovery. Keep the ledger schema reference-oriented and apply bounded redaction/secret scanning at Admission, but also define that confidentiality incidents may require a sanctioned destructive repository-history purge/new repository or encrypted/private ledger replacement, credential rotation, replica invalidation, and explicit loss-of-old-audit-access disclosure. The architecture must state which invariant yields under emergency redaction; a new logical lineage alone is not secret removal.

These storage issues do not prove that an in-repository ledger is a bad design. They mean the declared adoption is premature. A repaired plan can retain it as a **conditional concretization** to be accepted by the Architecture Manual once the deployment capability, anti-rollback, replication/refspec, privacy, and break-glass contracts are explicit; alternatively it can return to a private transactional canonical store with governed replication/export.

## 4. Non-blocking findings, ranked by consequence

### N1 — High: Architecture 1.6.0 transfer is not yet enumerated losslessly

§16 explicitly disposes frozen Architecture 1.6.0 invariants 1-7/11/24 and preserves a subset (2,4,5,13,14,23,26), but it does not explicitly disposition every frozen invariant. In particular 8-10, 12, 15-22 and 25 are not individually mapped. Several are plausibly preserved elsewhere (scheduler subordination, version binding, shared transport semantics, structured results, uncertain semantic state), while others may be intentionally retired with the old capability ladder. The omission is not presently a blocker because §21 requires the Architecture Manual to explicitly supersede Architecture 1.6.0 before D4; however, that closure obligation should require a **per-invariant transfer/retirement table** so a future manual cannot silently lose a frozen guarantee.

Current Core inspection reinforces why this matters: the implemented Core already embodies one composition root, version/profile-separated source resolution, frozen historical profile identities, JSON-compatible versioned records, and explicit no-cross-version source substitution. These existing accepted capabilities need deliberate preservation or retirement, not inference from architectural similarity.

### N2 — High: the consolidation regression test is partly structural, but it still parses prose for routing/status truth

`tests/test_protocol_80_orchestrator_consolidation.py` correctly checks active/archive file placement structurally, but its key routing/status assertions are `assertIn`/`assertNotIn` over Markdown text. It can therefore stay green if the index contains the expected path while assigning the wrong semantics to it, or if the active handoff contains the expected unauthorized strings in a non-governing context. This is exactly the failure family recorded in accepted/base PEM DS-001: synthetic/string fixtures can discriminate representation regressions while missing real-owner semantic defects.

Minimum improvement: keep the file-placement test, but move machine routing/status facts that truly need deterministic checking into structured frontmatter or a small canonical routing manifest and parse that structure. Keep semantic routing adequacy under independent Review rather than trying to encode it as prose substring tests.

No CI/check status was attached to candidate `f9d9de8` at Review time, and I could not execute the repository test suite because this environment has no local checkout and direct container network access to GitHub was unavailable. I therefore make no claim that the test ran here.

### N3 — Medium-high: the authority-index Stage H redirection is directionally correct but overstates what an index can authorize

The candidate changes no Protocol 7 artifact, which correctly respects the hard boundary. The index points future SSDS 8 work to the new handoff and accurately states that Protocol 7 is not final and D4 remains unauthorized. However, Protocol 7 Stage H still explicitly names the archived consolidated Protocol 8 workplan. The index says that because the old plan is superseded, the Stage H obligation “now applies” to the SSDS 8 handoff.

An authority index is a routing projection, not the owner entitled to amend Protocol 7's exact closeout obligation. Phrase this as prospective routing: when Protocol 7 Stage H runs, its owning closeout must reconcile/retarget that obligation through its normal authority process to the then-current SSDS 8 handoff. The index may point to the likely successor; it must not make the semantic reassignment itself. This is non-blocking now because Protocol 7 is still active, Phase A explicitly requires final reconsolidation, and no SSDS 8 implementation is authorized.

### N4 — Medium: conservative widening is conceptually sound but its scope-selection algorithm needs one exact interpretation

The design correctly refuses to infer independence from missing edges. However, §6.4's phrase “nearest enclosing scope ... for which such a judgment exists” should be normalized into an executable rule: define the enclosing-scope lattice, the relation class and completeness judgment being sought, whether the chosen completeness judgment covers the full scope or each member, and the exact fallback to whole-tree closure. The current intent is conservative; the remaining issue is formal computability and consistent implementations.

### N5 — Medium: minimum-architecture claim should explicitly re-test `Change` as a first-class primitive and cross-repository scope

`Unit`, `Relation`, `Record` and `Basis` each carry irreducible semantics. `Change` may prove to be a useful first-class transaction identity, but it is closer to an admission request/candidate aggregate than to persisted semantic authority. The Architecture Manual's minimum-justified-architecture pass should explicitly test whether it needs primitive status or can remain a typed Admission input without losing identity/audit semantics.

The workplan explicitly declines atomic multi-repository admission and treats cross-repository work through immutable external identities. That is an honest scope boundary rather than a hidden defect. The Manual should nevertheless state the project class this supports and the reconciliation semantics when one scientific project spans multiple repositories, because scientific evidence/data/code commonly cross repository boundaries.

### N6 — Low: befe678 archival identity is correct

Verified: the archived file `workplans/archive/SSDS-8.0-GRAPH-NATIVE-DETERMINISTIC-ORCHESTRATION-ARCHITECTURE-BEFE678-HYPOTHESIS.md` at `f9d9de8` and the active hypothesis file at commit `befe6782e7c8fe038bf7cb764646d133ca167855` have the same Git blob identity, `af9c005b15c4d0cfc56b0efb4dfe6b032fa4d958`. This is byte identity, not a prose comparison.

## 5. Out-of-matrix abstraction-adequacy pass

**Result: FAIL — one material global-invariant violation survives while following the workplan locally.**

I set aside §18, §21, §22 and the workplan's own acceptance list and attempted to construct a descendant trajectory that follows the local architecture rules but violates accepted 6.6 meaning.

The surviving trajectory is B1:

```text
accepted coarse legacy semantic unit P
 -> byte-identical structural refinement into A + B
 -> scope conservation passes
 -> declared relations unchanged
 -> completeness intentionally does not transfer
 -> conservative widening preserves A/B context
 -> workplan rule mechanically carries P acceptance to A and B
 -> native obligation consumes A as an accepted semantic subject
```

Nothing in that local trajectory requires a qualified semantic judgment that the old acceptance of `P` is valid as an acceptance of new subject `A`. The workplan's own migration qualification currently expects this behavior, so the matrix can remain green while the global abstraction/authority invariant is violated. This is an abstraction-adequacy defect, not merely a missing test.

No second independent out-of-matrix trajectory survived after accounting for basis widening, trusted evidence realization, independent equivalence/completeness qualifications, provisional propagation, one Admission writer, foreign-change drift, and the explicit residual-risk disclosure for unobserved semantic dependencies.

## 6. Evidence used

### Executed / directly inspected

- Resolved the governing release only from `PROTOCOL-RELEASE-STATE.yaml`: accepted current SSDP 6.6.0; public fallback `22f4bdba53795da3a6f13f162529f3a843fc37ae`; recovery `384666764da4c55b282e6b1595ab97e2f86e1dc4`.
- Verified branch `ssds-8.0-graph-native-architecture` head twice, including immediately before writing this record: exact candidate `f9d9de8f466963cbd4e53e85e44a7ab262952ffc`; no intervening commits.
- Bound the primary workplan to Git blob `aba4e967a2ecda9e82a544317b1ead47d8a690c5`.
- Compared `befe6782...` to `f9d9de8...`: the candidate is exactly one descendant commit and changes only the active SSDS 8 workplan, authority index, consolidation test, and archived befe678 hypothesis.
- Verified the befe678 archived hypothesis by blob identity `af9c005b15c4d0cfc56b0efb4dfe6b032fa4d958` against the befe678 active file.
- Reconstructed accepted 6.6 doctrine from its exact immutable public-source commit, including abstraction/concretization, architecture, workflow, evidence, semantic definition, concurrency/orchestration, storage/I/O, Git, security, versioning/compatibility, and PEM owners.
- Read accepted/base PEM from the project-designated integrated `main` state and verified that the candidate's PEM bytes are identical to it (`1561797125622f355f84eb27319f87e8fa4227d9`). Applied PC-001 and DS-001 as hypotheses/evidence, not authority.
- Read the archived consolidated Protocol 8 plan and its predecessor/revision lineage, including the in-repository-storage condition and deterministic replay/recovery requirements.
- Read the befe678 hypothesis independently of the candidate inheritance table.
- Read frozen `orchestrator/docs/architecture.md` Architecture 1.6.0 and current Core implementation surfaces material to composition, profile/source version binding, and public-record boundaries.
- Read the active Protocol 7 workplan only for prospective inheritance and Stage H routing; treated it as non-final.
- Inspected `workplans/active/SSDP-6.1-7.0-WORKPLAN-AUTHORITY-INDEX.md` for routing truthfulness only.
- Inspected `tests/test_protocol_80_orchestrator_consolidation.py` directly.
- Queried candidate commit combined status: no status checks were reported.
- Checked current Git documentation for remote atomic-ref update semantics: `git push --atomic` is conditional on the server advertising/supporting the `atomic` capability; unsupported servers fail the atomic request. This was used only to test the feasibility of §15.2's same-repository atomicity assumption.

### Reused as historical evidence, not as proof of this candidate

- 6.6 Review/ratification/recovery identities named by the release-state owner.
- Archived Protocol 8 design reviews/amendments only to reconstruct obligations they carried, not to inherit their conclusions about this candidate.
- PEM PC-001, DS-001, FF-001 and SP-002 at their bounded claim strength.

### Unavailable / not claimed

- No local repository checkout was available in this execution environment.
- Direct container network cloning from GitHub was unavailable, so I did **not** run `pytest` or repository scripts locally. Static/file-identity checks above were performed against immutable GitHub objects through the connected repository interface.
- Candidate `f9d9de8` reported no CI status checks through the repository interface. I therefore do not reuse CI as execution evidence.
- Protocol 7 final release identities and final semantic inheritance do not exist yet and were not invented.

## 7. Independently reconstructed invariants and disposition

| Invariant | Disposition at `f9d9de8` |
|---|---|
| Governing version and historical profiles are explicitly bound; no latest-version reinterpretation | **SATISFIED prospectively.** §24 preserves version-bound work/frozen profiles; current Core corroborates the existing capability. |
| Public fallback and recovery are distinct; successor publication cannot self-name | **SATISFIED prospectively.** §24 and candidate/result separation preserve this. |
| Accepted D1-D4 semantics remain owned by semantic authority, not control machinery | **FAILS in one migration path.** B1 mechanically transfers acceptance to refined child subjects. |
| Lower domains/mechanisms cannot create or redefine upstream authority | **SATISFIED generally; B1 exception blocks PASS.** Reconstruction proposals are top-down accepted; agent PASS cannot close work. |
| Semantic judgments are not converted into machine facts | **SATISFIED generally; B1 contradicts the rule.** §14 and §6.4 are otherwise strong. |
| Serious Challenge, human gate and risk override remain distinct and visible; override stays provisional | **SATISFIED prospectively.** §7.4/§9.4 preserve these semantics. |
| Gate evidence adequacy is semantic, not “artifact present” | **SATISFIED prospectively.** §9.4 states this directly; final Protocol 7 inheritance remains pending. |
| Evidence spec/realization/observation/assessment remain separate; stale pass/fail cannot close current claims | **SATISFIED prospectively.** §10 is materially lossless and preserves trusted-runner/custody boundaries. |
| One canonical workflow writer; agent/human/system inputs are proposals/observations/decisions serialized through it | **SATISFIED prospectively.** Admission is the sole ledger writer; semantic authority remains with qualified actors. |
| Canonical derived state is a pure function of version-bound accepted inputs, not wall clock/live refs/operator/search state | **SATISFIED in ownership design, but formal totality blocked by B2.** Observation/operator/search boundaries are good. |
| Ruleset evolution does not rewrite historical admissions | **SATISFIED prospectively.** Historical views bind the ruleset in force; new rules may create current obligations without rewriting admissions. |
| Currency/validity definitions are single-valued and well-founded | **FAILS / underspecified.** B2 gives a simultaneous-group fixed-point counterexample. |
| Missing dependency knowledge cannot be interpreted as independence | **SATISFIED in intent.** Completeness judgments and conservative widening are soundly conservative; N4 needs algorithmic precision. |
| Concurrency safety is not inferred from textual non-overlap | **SATISFIED with declared residual risk.** Serial Admission, basis currency, generated regeneration, joint invariants and evidence reruns cover known classes; unobserved semantic reliance is truthfully residual. |
| External effects are intent/outcome/reconcile operations and crash ambiguity cannot counterfeit completion | **SATISFIED in principle.** Same-repository remote ref atomicity needs B3 repair. |
| Canonical persistence survives machine loss and has explicit anti-corruption/recovery semantics | **PARTIAL / BLOCKED.** Repository replication improves machine-loss recovery; B3 leaves authoritative-ref rollback and privacy break-glass incomplete. |
| Secrets/private telemetry stay outside governed repository persistence | **SATISFIED by normal path; emergency path incomplete.** Operator state is private; B3.3 blocks the accidental-secret recovery claim. |
| Intake of manual/foreign/drifted content cannot silently become governing authority | **SATISFIED prospectively.** One intake route, drift and classification restrictions are coherent. |
| Legacy/native coexistence has no dual-current authority over one unit; cutover is quiescent and atomic | **SATISFIED structurally; B1 blocks semantic correctness of refinement.** Drain/pin/migrate is preserved per unit. |
| Production need not stop merely because migration is incomplete | **SATISFIED.** Ungoverned/legacy production may continue while governance closure remains open. |
| Routine agent work does not expose machine bookkeeping and interface is transport-neutral | **SATISFIED prospectively.** Six logical operations, snapshot reads and deterministic briefs are materially simpler. |
| Retrieval/search cannot self-authorize semantic relations | **SATISFIED.** Nondeterministic search is `CANDIDATE`; accepted authored relations require admission/semantic ownership. |
| Frozen Architecture 1.6.0 capabilities are explicitly preserved, replaced or retired before supersession | **PARTIAL.** N1: several invariants are not individually dispositioned; Architecture Manual can close this before D4. |
| Inheritance from consolidated Protocol 8 and befe678 is lossless or explicitly justified | **MOSTLY SATISFIED, with blockers above.** I found no additional silent loss after independent reconstruction; B3 means the storage replacement has not yet met its predecessor's conditional adoption bar. |
| Routing/index projections do not become semantic authority | **PARTIAL.** N3: routing target is sensible but Stage H reassignment wording should remain explicitly prospective/non-authoritative. |
| Qualification discriminates the property claimed and does not let synthetic/string fixtures stand in for real-owner semantic adequacy | **PARTIAL.** §22 is strong about real-owner/semantic Review, but B1 is currently encoded as expected behavior and the consolidation regression test parses prose substrings (N2). |
| Minimum architecture is justified against 6.6 operational simplicity | **PLAUSIBLE, not yet final.** Five primitives and seven components are coherent; N5 remains a Manual-level simplification check. |

## 8. D4 authorization

**SSDS 8 D4 remains unauthorized.**

This NO-PASS authorizes no implementation work. Repair the blocking architecture defects at the D3 workplan level, obtain a fresh independent Review of the repaired candidate, then still complete Protocol 7 inheritance reconsolidation and the independently reviewed/accepted SSDS 8 Architecture Manual before any SSDS 8 D4 handoff.