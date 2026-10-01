---
kind: ssds-major-architecture-workplan
workplan_id: SSDS-8.0-GRAPH-NATIVE-DETERMINISTIC-ORCHESTRATION-ARCHITECTURE
protocol_version: 6.6.0
target_system_version: 8.0.0
status: proposed
created_date: 2026-10-01
revised_date: 2026-10-01
source_branch_basis: f96b7ccf90dede4150d0efa17264fff07ec12d0d
source_branch: ssdp-7.0-scientific-epistemic-closure
design_basis: befe6782e7c8fe038bf7cb764646d133ca167855
design_review_state: pending-independent-d3-review
d3_architecture_state: proposed
implementation_handoff: not-authorized
active_serious_challenge: none
supersedes:
  - SSDP-8.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-CONSOLIDATED
  - SSDS-8.0-GRAPH-NATIVE-DETERMINISTIC-ORCHESTRATION-ARCHITECTURE-BEFE678-HYPOTHESIS
---

# SSDS 8.0 — Deterministic Orchestration Architecture: Basis-Stamped Judgments over Content-Addressed Units — Prospective Workplan

The workplan ID keeps the historical `GRAPH-NATIVE` lexeme for routing stability. The architecture it now carries is not graph-native in the sense of its predecessor hypothesis (§3): graphs are derived views over one typed relational substrate.

## 0. Disposition

```text
GOVERNING DESIGN PROTOCOL: SSDP 6.6.0 (accepted-current; identities owned by PROTOCOL-RELEASE-STATE.yaml)
TARGET: SSDS 8.0.0, the system-level successor to the document-controlled SSDP line
THIS FILE: single current prospective SSDS 8 architecture handoff; proposed, not accepted-current
SUPERSEDES: the consolidated Protocol 8 plan (archived byte-identically, with its nine-file lineage)
            and the befe678 graph-native hypothesis (archived byte-identically as ...-BEFE678-HYPOTHESIS.md)
SERIOUS CHALLENGE: NONE (section 1.3 records why the goals are judged consistent)
PROTOCOL 7: active closure; inheritance NOT FINAL; section 19 lists prospective inputs only
INDEPENDENT D3 REVIEW: ready for a fresh independent falsification Review of this architecture hypothesis;
            a PASS cannot authorize D4 before Phase A (Protocol 7 reconsolidation) and Phase C (Architecture Manual)
SSDS 8 D4: NOT AUTHORIZED
```

**What this revision did.** It re-derived the problem from the governing objectives, independently of the befe678 vocabulary, and replaced the four-graph / event-sourced / epoch / frozen-plan design with a smaller architecture built on five primitives (§5). Every still-valid guarantee of the consolidated Protocol 8 plan and every demonstrated capability of the befe678 hypothesis is carried, replaced by an equal-or-stronger mechanism, or explicitly retired with reason (§18). The befe678 commit had also dropped material lineage from the authority index and broken two repository regression tests; this revision restores that routing truthfully.

**Protocol 7 Stage H routing note.** The Protocol 7 consolidated workplan (Stage H, §15) assigns its closeout the authoring of "the Protocol 8 inheritance reconciliation" of the consolidated Protocol 8 plan. That plan is superseded here. The obligation is unchanged in substance and now applies to this file: Protocol 7 closeout reconciles its inputs against §19 and §24 of this workplan, advances the pre-cutover baseline, selects no SSDS 8 architecture, authorizes no D4, and recommends (never self-adopts) a governing-version adoption. This note does not edit the Protocol 7 workplan.

**Project Engineering Memory basis.** This is replacement/migration design for mature machinery, so the PEM predicate fires. Accepted/base memory: `PROJECT-ENGINEERING-MEMORY.md` on `main` at `2585b73f00420daca185a4fbb9ac42a79473eda1` (accepted base `23e46543c174a8451bbadc402df63538105eab10`); this branch carries no overlay (byte-identical). Historical Applicability Set:

| Entry | Binding | Disposition for this design |
|---|---|---|
| PC-001 frozen historical profiles | `AUTHORITY_BOUND` (versioning owner) | Applicable and mandatory through its owner: SSDS 8 preserves every version-bound profile/resource independently (§24). |
| SP-002 self-reference-safe identity | `EVIDENCE_ONLY` | Applicable: result/admission records reference candidate commits and are never stored inside them (§6.6). |
| FF-001 premature immutable publication | `EVIDENCE_ONLY` | Applicable to genesis, cutover and SSDS release: no immutable genesis/cutover identity is published before every required route and record exists (§12.5, §23). |
| DS-001 synthetic fixtures do not discriminate real-owner defects | `EVIDENCE_ONLY` | Applicable to qualification: synthetic fixtures bound only mechanical properties; semantic adequacy needs real-owner trials and independent Review (§22). |
| SP-001 repair canonical source, regenerate derivatives | `EVIDENCE_ONLY` | Applicable by analogy: derived views are regenerated from canonical content and ledger, never patched (§6.5). |

## 1. Problem, objective and allocation

### 1.1 The engineering problem

SSDS 8 coordinates stochastic reasoning agents and humans over evolving scientific software while preserving SSDP's hierarchy of semantic authority. It must answer mechanically, wherever an answer is mechanically decidable: what is authoritative; what depends on what; what changed; what is stale; what work is legal now; what may proceed concurrently; what context a task needs; what an agent modified; whether a result still applies to the state it was produced against; and what genuinely needs semantic judgment or human authority. It must absorb manual, external and legacy change without corrupting canonical state, let an old repository become governed progressively without stopping production, and let history be reconstructed after failures, migrations and schema evolution.

### 1.2 Allocation principle (refined)

The task statement's allocation is retained with two refinements that carry most of the architecture's leverage:

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

*Machines over-approximate; judgment narrows; recorded judgment is reused until its basis moves.* The agent is a semantic reasoning resource, never a bookkeeper. SSDS 8 succeeds only if added deterministic machinery reduces, rather than transfers, complexity to agents and humans.

### 1.3 Consistency of the governing goals (Serious Challenge check)

The goals were tested for contradiction. Three apparent conflicts dissolve under the architecture rather than being engineered around:

- *Mandatory deterministic control vs. never stopping production.* Production commits remain ordinary Git; what non-closure blocks is canonical governance status, not execution (§11, §12).
- *Minimal agent context vs. "absence of an edge is not independence".* Context is minimal only within declared-complete scopes; elsewhere the basis widens conservatively and the brief says so (§6.4, §9).
- *Single canonical writer vs. multi-host teams.* One writer per ledger is enforced by compare-and-swap on the designated authoritative replica (§15.2).

One residual limitation is real but not a contradiction: semantic dependencies an agent uses without the machinery observing them cannot be captured by any read-set scheme. The design bounds this risk (mechanical minimum basis, integration-time re-verification, explicit incompleteness) rather than claiming to eliminate it (§8.4). No Serious Challenge is raised.

## 2. Reconstructed invariants

Source tags: **[6.6]** accepted-current SSDP doctrine; **[P8]** consolidated Protocol 8 proposal (reviewed under 6.1, never accepted-current); **[S8]** SSDS 8 objective from stakeholder/task authority; **[P7?]** prospective Protocol 7 input, not final. Tags show where a requirement comes from; they do not make P8 or P7? items accepted authority.

### 2.1 Semantic

- **S1** D1-D4 semantic authority; one current owner per material normative claim; current ownership acyclic; D1-D4 is a layered DAG, not a waterfall; a higher abstraction never depends on a lower concretization; legitimate mutual definition only through an explicit simultaneous group. [6.6]
- **S2** Concretization fidelity and abstraction adequacy are distinct; Serious Challenge stops counterfeit closure; a risk override leaves dependents visibly provisional. [6.6]
- **S3** Authority mutation: proposal -> independent falsification where required -> required human ratification -> acceptance -> bounded impact -> reconcretization. Presence in a repository promotes nothing. [6.6]
- **S4** Evidence: specification -> realization -> observation -> assessment; observations immutable, assessments superseding; target vs execution dependency; stale passing evidence never confirms, stale failing evidence never refutes; binding health tracked separately from historical existence. [6.6]
- **S5** Absence of a relation establishes independence only inside a scope explicitly reviewed complete for that relation. [6.6]
- **S6** Specialized substantive inference requires the exact canonical meaning; definitions establish no truth, existence or adequacy; conflicting simultaneous meanings are adjudicated by their owner, never by order or recency. [6.6]
- **S7** Version-bound interpretation; no retroactive reinterpretation; no self-adoption; capability, not wording, is the compatibility oracle. [6.6]
- **S8** PEM is non-authoritative project learning; HAS is task-local. [6.6]
- **S9** A machine-control vocabulary never converts a semantic judgment into a deterministic fact; agent PASS is a recommendation. [6.6][P8]

### 2.2 Control

- **C1** Exactly one serialization point for canonical state changes per governed ledger. [P8]
- **C2** Same canonical inputs and rule version give exactly one derived state. [P8]
- **C3** Nondeterministic facts (time, filesystem, Git remote, resources, model output, human judgment) enter only as recorded typed records. [P8]
- **C4** External effects follow intent -> idempotent/reconcilable effect -> observed outcome; ambiguity is reconciled before retry. [P8]
- **C5** Unknown required semantics fail closed; unknown optional fields follow the declared compatibility contract. [P8]
- **C6** A disagreement between semantic content and its control representation is an integrity defect that blocks dependent transitions. [P8]
- **C7** Control data is the minimum needed to select, validate, serialize, replay or audit a transition. [P8]

### 2.3 Concurrency and isolation

- **K1** A result is admitted only if everything it relied on is still current, or it is revalidated. [P8][S8]
- **K2** No two mutating executions share one working tree. [P8]
- **K3** A clean textual merge is not semantic orthogonality. [S8]
- **K4** Correctness never depends on predictions being complete; predictions may only reduce wasted work. [derived here]

### 2.4 Provenance and replay

- **P1** Every canonical change records what, who, against which basis, under which rules. [P8]
- **P2** Historical decisions are never recomputed under newer rules, resources or interpretations. [P8]
- **P3** Derived state is rebuildable; canonical records win any disagreement. [P8]

### 2.5 Agent interface and context

- **A1** Routine work never requires reading machine records, decoding history, maintaining edges or reconstructing Git topology. [S8]
- **A2** Context is version-bound, explains why each item is present, labels its epistemic status, and states known incompleteness. [S8]
- **A3** One logical task/result contract across harnesses and transports; a zero-context agent can locate its task from a minimal bootstrap. [P8]

### 2.6 Repository and Git

- **G1** Git is content, isolation, transport and history substrate, never workflow authority. [P8]
- **G2** Transport artifacts are not merged into product history. [P8]
- **G3** No record must contain the identity of the commit that contains it. [P8][6.6, SP-002]
- **G4** Secrets and private telemetry never enter project repositories. [P8]

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
- **T4** Human decisions are authenticated through a declared trust mechanism; no cryptographic guarantee is claimed beyond what is implemented. [P8]

### 2.9 Backward compatibility

- **B1** Older version-bound work stays governed by its declared version and immutable source; frozen orchestration profiles stay independently testable (PC-001). [6.6]
- **B2** Rollback is version rollback to an immutable baseline, never simultaneous dual authority. [P8]
- **B3** Protocol 7 inheritance is not final and is not bound here. [task authority]

### 2.10 Conveniences that had been masquerading as architecture

Four canonical graph families; a global authority epoch; whole-plan freezing with a global replanning stop; event-sourced storage of state transitions and stored lifecycle FSMs; a hand-authored work graph with many node kinds; pre-declared write claims as the concurrency-correctness mechanism; a separate write-side graph transaction engine with dirty flags; separate context-resolver and semantic-projection components; a dedicated ingestion engine; legacy aggregates as a special node type; a mandatory refactor of all authority documents into per-node files; and MCP as the interface definition. None follows from §2.1-§2.9. Each is either replaced (§17) or retained as a delegated D4 option.

## 3. Diagnosis of the befe678 hypothesis

The befe678 hypothesis correctly identified the need for machine-readable relations, derived code dependencies, context retrieval, isolation, reconciliation and progressive migration. Its weaknesses are structural:

1. **Synchronization burden by construction.** Four canonical graph families with independent lifecycles share identities and cross-family edges (EVIDENCES, CONCRETIZES from code, work claims over authority). Their consistency had to be maintained by a GraphTransaction, candidate overlay, GraphDelta and dirty-flag machinery — machinery created by the decomposition, not by the problem.
2. **Global coupling where the problem is local.** AuthorityEpoch totally orders independent authority changes, so unrelated acceptances advance the epoch every task is bound to. Whole-plan PlanRevision plus a conservative stop on new mutating tasks during replanning turns a local amendment into a project-wide barrier.
3. **Two parallel staleness systems.** Staleness of tasks (epoch/plan binding), of context (ContextBundle), of evidence (EvidenceGraph status) and of graphs (DIRTY) were separate mechanisms answering one question: *did anything this conclusion relied on change?*
4. **Stored state that is really derived.** Execution/outcome/validity/authority/evidence FSMs were stored and reduced from events, although almost all of them are functions of content plus recorded judgments.
5. **Correctness resting on predictions.** WorkClaims declared before execution were the parallelism-safety mechanism; they are necessarily incomplete for semantic conflicts across disjoint files, generated outputs and dynamic dependencies.
6. **Fragile canonical history.** Canonical history lived only in a private local SQLite store; loss of that store with intact repositories lost all accepted decisions, and clone/fork/move had no history path.
7. **Interface leakage.** Agents were asked to propose PlanPatch node/edge operations, maintain WorkClaims, call `change.reconcile`, and choose among seventeen operations.
8. **Migration as a special subsystem.** LegacyAggregate, an ingestion engine with four modes, and a separate repository-explainability rule duplicated what one coverage partition with adaptive granularity provides.
9. **Lossless-representation defect.** It declared supersession of the consolidated Protocol 8 plan while omitting material inherited guarantees (semantic/control projection rule, forward compatibility, transport-artifact and self-reference rules, bootstrap locator, human-gate/risk-override propagation, cutover quiescence, pre-cutover baseline identities, Protocol 7 inputs, versioning preservation, most failure qualifications).

## 4. Alternatives considered

| Candidate | Core idea | Verdict |
|---|---|---|
| **H0** befe678 | Four canonical graphs, event-sourced reducer, epochs, frozen plan revisions, graph transactions, legacy aggregates | Rejected as a whole for §3. Retained capabilities are mapped in §18.2. |
| **H1** verified incremental computation | Content-addressed units; an immutable ledger of judgments and observations; everything else derived by versioned rules; staleness = basis change (build-system "early cutoff") | **Selected core.** One mechanism answers staleness, readiness, impact and context; locality is natural. |
| **H2** logic knowledge base | All facts, authored and derived, in a Datalog/relational store with an event log of assertions/retractions | Hybridized. Strong queries, but retraction semantics and a rule language as architecture add risk. Kept: derivation rules must be stratified so that negation ("not current") is deterministic (§6.5); rule engine form delegated. |
| **H3** Git-only documents-as-state | Plans, judgments and statuses as repository files; CI as gate | Rejected as primary: anyone can push a PASS file, concurrent status edits conflict, and status-in-documents is exactly what SSDS 8 removes. Kept: Git as content store, isolation, replication and transport, including the ledger (§15). |
| **H4** hosted service | Central database plus durable-workflow engine | Rejected: operational cost, not local or lightweight, polling-first violated, no benefit for the single-team scale that must work first. |

Comparison of the serious candidates (H0, H1+H2+H3 hybrid):

| Criterion | H0 | Selected hybrid |
|---|---|---|
| Authority integrity | relations in separate graph store can drift from content | authored relations live inside the content they belong to; drift impossible by construction |
| Determinism | reducer over events | pure derivation over ledger + content; fewer stored states |
| Duplication | four graphs + control state + caches | one content store, one ledger, derived index |
| Implementation complexity | high (sync, overlays, dirty tracking) | moderate (derivation engine with memoization) |
| Agent burden | many operations, plan/claim maintenance | five verbs; no bookkeeping |
| Recovery | local store loss is fatal | ledger replicated with the repository |
| Concurrency | claim-based, incomplete | optimistic validation at admission; claims advisory |
| Migration | separate subsystem | ordinary refinement of coverage |
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
          (queries, read-only)                (proposals)
                 v                                   v
         Derivation Engine  <-------------------  Admission  ---- sole writer ----+
   currency · validity · obligations ·         validate · append ·                |
   readiness · impact · context                integrate                          |
          |            |                                                          v
   Content Model    Analyzers                                   Ledger (append-only, hash-chained,
   units · coverage  derived relations                                  replicated with the repository)
   authored relations                                                   Integration ref (product branch)
          \            /                                                          ^
           Git content store  <-- workspaces (isolated) -- Dispatcher ------------+
                                                       scheduling · effects · harness adapters
                                                       (operator state: private, local)
```

Five primitives:

1. **Unit** — a governed region of repository content with stable identity and a content-addressed revision (§6.1).
2. **Relation** — a typed, directed fact between units, classed as authored, derived or proposed (§6.2).
3. **Record** — an immutable ledger entry: a judgment, an observation or an admission (§6.3).
4. **Basis** — the exact set of unit revisions and records a record relied on; currency is computed from it (§6.4).
5. **Change** — a candidate content mutation (Git commit) plus its records, admitted or rejected as one unit (§6.6).

Everything else — lifecycle states, obligations, readiness, staleness, impact sets, context bundles, graph views, diffs, dashboards — is **derived**.

## 6. Primitives

### 6.1 Unit

A **unit** `u` has: a stable logical identity; a kind and owning domain (D1, D2, D3, D4, plan, evidence specification, generated, external, unclassified); a **region** of repository content (a set of paths, or an anchored span within a file); and a declaration source.

- **Declaration.** Units are declared inline (an anchor at a section of a semantic document) or in a repository-owned unit manifest (path patterns, heading paths or symbol sets). External declaration is mandatory for immutable or version-pinned artifacts, which are never rewritten to acquire anchors.
- **Revision.** `rev(u, T)` is a content hash of the bytes of `u`'s region in tree `T` together with its declaration (including its authored outgoing relations). It is computed from Git content, so no separate hash graph is stored. Unit granularity is adaptive: a whole file, a section, a symbol set, or an entire legacy subtree.
- **Coverage partition.** For every admitted tree, the regions of declared units partition all governed content: every tracked path outside declared ignore patterns, and every span of a sectioned file, belongs to exactly one unit. Genesis may declare a single catch-all `UNCLASSIFIED` unit. Partition validity is mechanically checked at every admission.
- **Single definer.** A unit may declare that it defines a named semantic object. Two current units defining the same object is an integrity conflict that blocks dependent use until the owner adjudicates (S6).
- **Status lives in the ledger.** Acceptance, governance mode, reconstruction status and lifecycle are derived from records (§6.5), never written as editable fields in the unit content.

Why units rather than files or Git blobs: per-file identity makes any edit to a long authority document invalidate every conclusion that relied on any part of it. Unit identity gives locality; adaptive granularity keeps the declaration cost proportional to need.

### 6.2 Relation

A **relation** is `(subject, type, object, class, provenance)`.

- **Authored** relations are declared inside the subject unit's region (or its manifest declaration) and are therefore part of the subject's revision. They are accepted when the subject revision is accepted, and change only by changing the subject. Semantic relations and their meaning cannot drift apart, and a human editing a document edits its relations in the same act.
- **Derived** relations are computed by a versioned analyzer from content (imports, calls, build edges, generated-from, test-to-code). They are never edited and never stored as canonical; they are cached under their derivation key.
- **Proposed** relations are records (from search, analyzers with semantic uncertainty, or agents) awaiting acceptance; acceptance happens by an admitted change to the subject's authored relations.
- **Record-level relations** (challenges, evidence assessments, supersession of assessments, refinement lineage) are properties of records, not edits to their targets: a challenger never owns the challenged unit.

Direction and typing follow the evidence and definition owners: stored direction is subject -> prerequisite; reverse traversal is impact analysis, not a second relation. Representative authored types: `CONCRETIZES`, `DERIVED_FROM`, `DEPENDS_ON`, `USES_DEFINITION`, `ASSUMES`, `CONSTRAINED_BY`, `SUPERSEDES`/`REPLACES`, `EVIDENCES` (evidence specification -> claim unit), `EXECUTION_DEPENDS_ON`, `GENERATED_FROM`. The vocabulary is versioned and extensible; generic "related-to" cannot support any closure (S5).

Mechanical structural rules checked at admission: referenced units exist; no authored dependency from a higher abstraction to a lower concretization; same-domain strongly connected components exist only inside a declared simultaneous-definition group, which is accepted as one unit; plan items do not depend on lower-layer work in a way that inverts the authority order.

**Completeness is itself a judgment.** "Relation class R is complete over scope X" is a `COMPLETENESS` judgment with its own basis. The common case is per-unit *outgoing* completeness attested during the unit's acceptance review ("this unit's declared prerequisites of class R are complete"). Any inference of independence records the completeness judgment it used in its basis. If a completeness claim later fails, every independence inference that relied on it becomes non-current automatically (§6.4). Completeness never transfers through refinement (§12.2).

### 6.3 Record and ledger

The **ledger** is the single canonical store of everything that cannot be derived from content. It is append-only, totally ordered per ledger, hash-chained, and serialized in a canonical versioned schema. Every record carries: identity, kind, actor and actor class, subject, basis, outcome, schema and ruleset version, provenance, and references to any substantive report artifact. Records never contain essays, equations, patches or raw logs (C7).

| Record kind | Produced by | Examples |
|---|---|---|
| **Judgment** | agent, human, or semantic-role tool | acceptance review; conformance review; equivalence/non-materiality; completeness; challenge; Serious Challenge; adjudication; risk override; ratification; evidence assessment; plan acceptance; intake classification; reconstruction proposal; finding |
| **Observation** | machinery | evidence realization result with execution basis, from a trusted runner (§10); intent and outcome of a canonical effect (integration-ref update); live-ref movement and other foreign-change detection; analyzer output recorded because the analyzer is nondeterministic or expensive; artifact availability |
| **Admission** | Admission only | accept or reject of a proposal with reason codes, validated basis, ruleset version, and resulting integration commit |
| **Lifecycle** | Admission, under human gate where required | genesis (project identity, authoritative replica, trust roots); ruleset adoption; schema migration; fork; cutover; ledger-loss declaration |

Every record enters through Admission. A judgment is *recorded* when admitted; whether it is *current* is derived (§6.4). Rejections are recorded too, so provenance includes what was refused and why.

The ledger holds only what derivation consumes or audit requires. Purely operational facts — task issue, reservations, leases, worktree creation, agent launch, retries — live in the Dispatcher's durable operator journal under the same intent -> effect -> observed-outcome discipline (C4); they influence scheduling, never derived workflow state. Execution provenance that matters for audit (route, harness, model, attempt) travels inside the submitted records.

### 6.4 Basis, currency and validity

A **basis** entry is `(target, revision-or-record, mode)`, where the target is a unit or a record and the mode is `content` (the bytes it saw) or `validity` (it relied on the target being accepted and valid).

The basis of a record is the union of:

- the **mechanical minimum** computed by the rule for its kind: the governing units of its obligation, their dependency closure over the relation classes that rule requires, the context items supplied to the task, and the change base;
- **recorded reads** made through the interface (and harness-observed reads where an adapter can observe them);
- **declared reliance** the actor adds at submission.

An actor can add to the mechanical minimum, never remove from it.

**Conservative widening.** When the rule needs a dependency closure over a relation class and a unit's outgoing relations of that class are not covered by a current completeness judgment, the closure includes every unit of the unit's nearest enclosing scope (its document or manifest group, then directory, up to the whole tree) for which such a judgment exists, and the whole tree if none does. Widening is sound and may be expensive; narrowing it requires a completeness or equivalence judgment. When mechanical knowledge is incomplete, the basis widens and never narrows.

**Definitions.** Let the **admitted tree** be the integration tree named by the latest admission record. `cur(u)` is `u`'s revision in the admitted tree — never in the live integration ref, whose movements enter only as recorded observations (C3, §11). `acc(u)` is `u`'s most recently accepted revision (admitted with discharged acceptance, or imported from a legacy process, §12.1). A basis entry naming a revision of a unit later refined is satisfied while every child still has its refinement-time revision (refinement lineage). Consumption class `k` identifies how a record uses a target (for example, structural use vs behavioral conformance).

```text
satisfied_content(e = (u, r)) <=>  cur(u) = r
                                   OR exists current EQUIVALENCE judgment q with
                                      q.from = r, q.to = cur(u), q.scope covers k(e)
satisfied_validity(e = (u, r)) <=> satisfied_content(e) AND valid(u)
satisfied(e = (record x))      <=> current(x)

valid(u)      <=> acc(u) defined AND cur(u) = acc(u)           -- no drift
                  AND each acceptance obligation for (u, acc(u)) is discharged by a current judgment
                  AND no unresolved blocking challenge targets (u, acc(u))
provisional(u) <=> as valid(u), except a blocking challenge is under an admitted risk override

current(j)    <=> j not superseded AND no unresolved blocking challenge targets j
                  AND every basis entry of j is satisfied
                  (provisional when any satisfied entry relies on a provisional target)
```

Recursion is well-founded: acceptance judgments of a unit may place in their basis only units earlier in the condensed authority order, records earlier in the ledger, and members of their own simultaneous group; Admission rejects any other cycle.

**Early cutoff with backdating.** When upstream D2 unit `a` changes, the D3 unit `b` whose acceptance relied on `a` becomes not valid; D4 judgments that relied on `b` become not current (validity mode). If a re-review of `b` against the new `a` passes *without changing `b`*, `b` is valid again and every D4 judgment whose basis named `b`'s unchanged revision becomes current again with no further work. Staleness propagates exactly as far as meaning actually moved.

**Equivalence is semantic unless trivial.** Machinery may decide equivalence only for byte identity and rule-defined conservative normalizations, and may use derived interface fingerprints only for consumers of derived structure — never for behavioral conformance, evidence or semantic acceptance. Everything else ("editorial only", "representation-preserving split", "does not affect this consumer") is an `EQUIVALENCE` judgment by a qualified actor, scoped to consumption classes. Where the rule requires independence, the author of a change cannot be the sole qualifier of an equivalence or completeness judgment about that change; a self-declared one remains a proposal and backdates nothing.

This one mechanism replaces epoch binding, plan-revision binding, context staleness, stale-result detection, evidence staleness, dirty-graph tracking and the freeze frontier.

### 6.5 Derivation

The **Derivation Engine** computes, as a pure function,

```text
derive(ruleset_v, ledger[0..n], content of trees referenced in ledger[0..n],
       recorded observations in ledger[0..n]) -> exactly one derived state D_n
```

where `ruleset_v` is the ruleset (system ruleset plus accepted project policy) in force at position `n` according to the ledger's own adoption records.

Derived state includes: unit accepted revisions, validity and provisional status; currency of every record; authority, validity, evidence and obligation classifications (the composed-dimension state model of the predecessor, now computed rather than stored); obligations, readiness and blockers; impact sets for any hypothetical change; context answers; graph, diff and history views.

- **Rules** live in a versioned registry: for each judgment kind, the admissible subjects, actor qualifications (agent, independent agent, human role), mechanical minimum basis, allowed outcomes and consequences; for each obligation rule, its trigger and discharge predicate. Rules are stratified so that negation ("no current judgment exists") has one meaning. Scientific truth is never encoded in a rule. The system ruleset is versioned with SSDS; **project policy** (required gates, actor qualifications, serialization surfaces, scoped-amendment policy, trust roots) is a protected repository unit, and derivation always uses its *accepted* revision `acc(policy)`, so an unadmitted edit to policy content takes no effect. Both versions are bound by an admitted ruleset-adoption record.
- **Analyzers** produce derived relations keyed by `(analyzer identity, version, configuration, input revisions)`. A deterministic analyzer's output is cache. A nondeterministic or expensive analyzer's output is recorded as an observation so that replay uses what was observed. Analyzer incompleteness (reflection, plugins, dynamic registration, generated code, runtime configuration, external consumers) is declared and triggers conservative widening.
- **Caching** is memoization keyed by inputs; there is no dirty state because nothing is cached without its content key. Incremental derivation must equal from-scratch derivation for the same inputs (qualified, §22).
- **Integrity checks** run on every derivation: coverage partition, single definer, relation structure, content-vs-acceptance drift, ledger hash chain.

### 6.6 Change and Admission

A **change** is a candidate commit (or commit series) on an isolated ref, built on a recorded base, together with the records the producing task submits; a change may also be records only (a review, ratification or challenge of already-admitted content). Admission is the **sole writer** of the ledger. Other actors can still move the integration ref (humans pushing to legacy scopes, an external merge button, a force-push); such movement carries no admitted status. It is recorded as an observation and absorbed mechanically as a foreign change (§11): the new tree becomes the admitted tree, and every touched unit whose content now differs from `acc(u)` shows drift. Production is never blocked by this; governance validity is. An external merge mechanism may perform an admitted merge only when the resulting tree is identical to the merge result Admission validated.

Admission validates, in order, and either appends atomically or rejects with recorded reasons:

1. **schema** — records well-formed; unknown required semantics fail closed (C5);
2. **reference** — every identity, revision, task and obligation exists and matches;
3. **authorization** — actor class qualified for each judgment kind; protected surfaces untouched without their own authority (§15.4);
4. **structure** — coverage partition, relation direction and grouping, single definer, on the merged tree;
5. **currency** — every basis entry of every submitted record is satisfied at the current ledger head (optimistic concurrency); otherwise the change is classified stale and routed to revalidation rather than admitted;
6. **legality** — the obligation the change claims to discharge exists and is undischarged at the current head (a duplicate discharge is rejected and recorded), and its discharge predicate (§7.4) holds after the change's own records, including affected evidence rerun on the merged tree;
7. **no collateral regression** — every obligation discharged at the current head and affected by the merged tree stays discharged, with affected evidence rerun. The only legal way to reopen others' closures is an accepted change to a prerequisite authority, whose derived impact obligations are the intended consequence; a D4 change that breaks another closure is a regression and is not admitted;
8. **commit** — one atomic append of all records plus the integration-ref update; then derivation advances.

Mechanical absorption of a foreign change is the one admission that skips steps 5-7: it records what already happened rather than proposing anything, so it cannot be stale or illegal. Its consequences — drift, non-current records, broken closures — become derived obligations (§11).

Atomicity: where the ledger and integration ref live in one repository, both refs update in one reference transaction. Otherwise the integration-ref update is an external effect under the intent/outcome protocol (C4), and a ledger head that names an integration commit not yet observed on the ref is reconciled before any further admission.

**Self-reference.** Records reference the candidate commit; they are never stored inside it. Task and result envelopes on run branches are transport, ingested into the ledger, never merged (G2, G3).

**Agent PASS is a proposal.** An admitted PASS judgment is a recorded fact about what the actor concluded; closure is a derived discharge (§7.4).

## 7. Work: obligations and change plans

### 7.1 Two sources of work

The befe678 WorkGraph conflated two different things.

- **Derived obligations** follow from rules and state: a unit without a current acceptance judgment; a judgment no longer current; an evidence specification without a current admissible realization for its claim; an active challenge awaiting owner adjudication; a pending human gate; a foreign change awaiting intake; a scope deviation awaiting disposition. These are never authored; they appear and disappear as derivation changes. They carry deterministic identities derived from `(rule, subject)`.
- **Authored intents** carry creative direction: implement this, investigate that, migrate this region. They live in **change plans**, which are plan units (documents) whose sections are **items** with an objective, governing units, acceptance criteria, intended affected units, required gates and dependencies on other items or units.

### 7.2 Plan acceptance and local amendment

A `PLAN_ACCEPTANCE` judgment (independent where policy requires) names in its basis the plan's objective section and the item revisions it accepts. An item is issuable only while some current plan-acceptance judgment covers its current revision. Item-level revisions give locality:

- an amendment is an ordinary change to the plan unit; tasks whose basis names a changed item become non-current; tasks on unchanged items continue;
- whole-plan invariants are rechecked mechanically on every amendment: referenced units exist, dependencies are acyclic and respect authority order, gates required by policy are present, acceptance criteria name resolvable evidence;
- the plan's policy states whether an amendment may be accepted by a scoped review of the changed items plus their derived impact set or needs whole-plan review; changes to the plan objective, acceptance criteria, topology or gates always need whole-plan review, and a scoped reviewer always receives the whole-plan objective and may escalate;
- running tasks remain bound to their basis; no revision pretends an old task saw new requirements.

No global planning/working phase and no global stop exist; an unaccepted amendment only makes its own items non-issuable. Plan lifecycle fields in documents are non-authoritative or generated (§12.6).

### 7.3 Readiness, iteration and attempts

An obligation is **ready** when every prerequisite it names is valid (or provisional where policy permits provisional continuation, which then marks the result provisional) and its plan item (if any) is accepted. Readiness is derived from the ledger and content alone. This is the whole "freeze frontier": readiness through the authority DAG, not a waterfall, with no extra state. Whether a ready obligation is *dispatched now* — resources, routes, serialization surfaces already held (§8.3) — is the Dispatcher's operational decision and never feeds back into derived state.

An **iteration** is the sequence of judgments recorded against one obligation; a NO-PASS leaves the obligation undischarged and the next task is a new iteration. An **attempt** is one execution of one task, owned by the Dispatcher; a failed attempt is recorded in the operator journal and does not touch derived workflow state.

### 7.4 Discharge (canonical closure)

```text
discharged(o) <=> exists current judgment j of kind(o) on subject(o)
                   by an actor qualified for kind(o), with outcome in passing(o)
              AND no unresolved blocking finding against subject(o)
              AND no active governing Serious Challenge, unless under an admitted
                  risk override (then: discharged-provisional, never unqualified)
              AND every evidence obligation of o has a current admissible realization
                  assessed for the current claim revision
              AND every human gate of o is discharged by an authenticated human judgment
              AND every derived obligation triggered by the change that claims o is
                  discharged or explicitly carried as provisional
```

A missing required check is an undischarged obligation; no rule can turn it into PASS.

## 8. Concurrency

### 8.1 What is decided where

| When | What can be established | Mechanism |
|---|---|---|
| Before issue (prediction) | probable footprint: intended affected units, derived impact closure, serialization surfaces | Dispatcher avoids issuing overlapping work; advisory only (K4) |
| At admission (proof) | everything the change relied on is current; actual write set; structural validity of the merged tree | basis currency (§6.4), diff mapped to units, structural checks |
| After merge (evidence) | behavior of the combined tree | evidence currency recomputed on the merged tree; affected realizations rerun |
| Never mechanically | joint validity of independently valid changes where no relation, invariant or evidence covers the interaction | judgment: declared joint-invariant units, review of integrated results, residual risk stated |

### 8.2 Optimistic admission (serializable by validation)

Concurrent tasks work from recorded bases in isolated workspaces. Admission applies changes one at a time to the integration head (a merge queue; speculative batching is delegated D4 and must preserve this serial order). A change whose basis was overtaken is revalidated — rebased, re-derived, affected judgments re-requested — not rejected outright and never silently admitted. Two changes conflict when one modifies a unit (or record) in the other's basis; this catches write-skew among recorded reliances, including across disjoint files.

A very late result whose basis is still current is admissible regardless of age; a fresh result with a stale basis is not. Lease expiry affects scheduling, never correctness.

### 8.3 Serialization policy

Some surfaces make speculative concurrency wasteful or unsafe to merge mechanically: shared schemas and public contracts, build configuration, D1-D3 units in one dependency neighborhood, and generated outputs. A unit may carry a policy-declared serialization attribute; the Dispatcher issues at most one mutating task on it at a time. Generated units are never hand-merged: they declare `GENERATED_FROM` their generator and inputs and are reproduced by regeneration, with conflicts resolved by regenerating.

### 8.4 Residual risk

Semantic dependencies an agent uses without the machinery observing them cannot be captured. Mitigation is layered: the mechanical minimum basis already includes the governing closure; integration reruns affected evidence; units may declare cross-cutting **joint invariants**, any change touching whose scope re-derives their conformance obligation; reviews of integrated results are triggered where policy marks a surface high-consequence. The remaining risk is stated in briefs and Review records rather than hidden.

## 9. Agent and human interface

### 9.1 Logical operations

The interface is defined independently of transport.

| Operation | Purpose |
|---|---|
| `open(task)` | returns the task brief (§9.2) and workspace locator |
| `ask(query)` | typed questions: what governs X; what X depends on / what depends on X (per relation class); explain a unit, record or obligation; evidence for a claim; why is this blocked or stale; impact of this workspace diff or proposed edit; text/semantic search; history of X (PEM-gated) |
| `read(ref)` | content by unit identity or path; recorded into the basis |
| `report(item)` | finding, challenge, Serious Challenge, proposed relation, question for a human, scope deviation, blocker |
| `submit(result)` | outcome classification from the task's allowed set, plus the workspace; machinery computes the diff, touched units, changed authored relations and derived consequences |
| `decide(gate)` | human only: a gate brief (§9.4) and an authenticated decision |

Within a task, `ask` and `read` answer at the task's basis (snapshot isolation), so an agent never sees a mixture of states; `ask("what changed since my basis")` reports admitted changes that intersect the task, letting the agent stop early instead of discovering staleness at submission.

The agent never declares claims, revisions, edges (other than by writing authored relations as part of semantic content), epochs, plan patches, lifecycle states or reconciliation steps.

### 9.2 Task brief

A task brief contains, in this order: objective and obligation kind; allowed outcomes; **governing content inline** (exact text of governing units at the basis revisions); constraints, non-goals and delegated space; acceptance criteria and required evidence; open challenges, findings and provisional states touching the subject; **incompleteness notices** (where the basis was widened, where analyzers are incomplete, where relations are only proposed); workspace and submission instructions. It is rendered deterministically from derived state by version-bound templates; no model is needed to translate machine state.

### 9.3 Epistemic status of context

Every context item is labeled:

| Class | Meaning |
|---|---|
| `GOVERNING` | authority the task's subject concretizes or is constrained by; mandatory |
| `IMPLIED` | reached by accepted authored relations inside a declared-complete scope |
| `ADJACENT` | reached by derived structural relations; completeness per analyzer declaration |
| `EVIDENTIAL` | evidence for the subject's claims, with current/stale/unavailable status |
| `HISTORICAL` | PEM entries and Git history; offered only when the PEM predicate fires or on explicit request |
| `CANDIDATE` | search or embedding hits and unaccepted proposals; never authority, never closure support |

Each item also carries its acceptance status (accepted, provisional, challenged, stale, drift, unclassified) and its inclusion path. Answers are deterministic for identical basis, query and policy version; search indexes record their versions, and nondeterministic search contributes only `CANDIDATE` items outside the determinism guarantee. A search hit can lead to a proposed relation but never to an accepted one by itself.

### 9.4 Human gates

A gate brief presents the non-narrative evidence core first (identities, coverage, key data and trajectories, findings as data), then agent interpretation, alternatives, anomalies and unresolved findings separately. Gate-evidence adequacy is a semantic judgment, not a presence predicate: the human's decision records whether the evidence was adequate, and that record can itself be challenged. Agents and machinery may request a gate; they cannot synthesize a human judgment. A risk override is a distinct judgment kind that authorizes bounded continuation and leaves dependents provisional (S2).

### 9.5 Transports and harnesses

Transports expose the same logical operations: an MCP server, a CLI, and a Git-envelope transport for zero-context web agents (immutable task envelope on an isolated run branch; result envelope plus candidate commits written back; polling-first fetch of the specific run branch). Harness adapters (Claude Code, Codex, OMP, Pi or others) only map these operations and launch/observe executions. The bootstrap is `Execute SSDS task <id>` plus the minimum locator not already bound by the environment (repository, run ref, envelope path, protocol/profile source); it fails truthfully when protocol material cannot be resolved. Transport and process success never imply evidence admissibility or task success.

## 10. Evidence

| SSDP evidence concept | SSDS 8 representation |
|---|---|
| specification | evidence unit with `EVIDENCES` -> claim unit and declared or derived `EXECUTION_DEPENDS_ON` |
| realization | observation record whose basis has two parts: **target** (claim unit revision) and **execution** (code units, data identity, environment, backend, precision, configuration, parameter instance, regime, seed and replicate identity) |
| observation | the realization record's outcome plus references to native artifacts (logs, data) by content identity where possible |
| assessment | judgment record; later reassessment supersedes, never rewrites |

A realization supports a claim at revision `c` only while its execution basis is current and its target is `c` (or an equivalence judgment covers the change). An execution-dependency change triggers a rerun obligation; a target change triggers an assessment-review obligation. Stale passing evidence never discharges; stale failing evidence is not admissible against the current claim. Unavailable artifacts degrade binding health through availability observations: the historical record survives, present use becomes `UNAVAILABLE`. Process exit or harness success is never evidence admissibility; a realization with incomplete or malformed evidence is recorded as such and cannot enter a PASS/FAIL assessment. Raw data stays in native stores; the ledger stores identities and bounded classifications.

**Who may realize evidence.** A realization can discharge an evidence obligation only when it was executed by a runner that project trust policy designates for that specification (normally Dispatcher-controlled execution of the specification on the exact candidate or merged tree), or when a designated runner reproduces it. Results an agent reports from its own workspace are findings: useful for direction, never admissible for discharge. Expensive scientific realizations (long simulations, HPC campaigns) may be designated by policy to run under recorded custody outside the Dispatcher, with the custody evidence named in the realization record.

## 11. Intake: one route for every change of unknown provenance

Intake is not a separate engine. It is a set of derivation rules plus judgment kinds that treat any content not produced by an admitted change as a change with an **unknown basis**.

**Detection.** Recorded observations show: the live integration ref has moved away from the admitted tree (direct push, external merge, force-push); a submitted workspace contains changes outside its reported result; an external branch is offered for import; content differs from accepted revisions (drift); a scheduled census finds untracked or unexpected material.

Two entry paths share one rule set. Content **already on the live integration ref** is absorbed mechanically (§6.6) and its consequences become obligations. Content **offered as a candidate** — an external or foreign-agent branch, or agent work outside its reported result — is a change whose basis is computed conservatively from its merge base (mechanical minimum plus widening); it reaches the integration ref only through ordinary Admission after its intake obligations are discharged.

**Processing.**

```text
preserve exact identity (commit/ref/tree; nothing executed)
 -> diff against last admitted state, map changed paths to units via coverage
 -> uncovered paths: proposed new units, statically classified
    (path, type, Git history, known producers, build manifests, parsers, provenance)
 -> mechanical consequences: every record whose basis moved is non-current
 -> obligations: classification and disposition judgments; equivalence/materiality
    judgments; conformance or acceptance reviews for touched authority; quarantine for
    untrusted or opaque active content
```

**Dispositions** are judgment outcomes: `ABSORB`, `RECONCILE` (needs rework), `SPLIT`, `ARCHIVE`, `RETAIN_AS_EVIDENCE`, `MARK_GENERATED`, `QUARANTINE`, `REJECT` (reverted by an ordinary change), `DISPOSABLE` (classification only; deletion is a separate authorized change).

Until intake obligations are discharged, affected content cannot serve as governing context, evidence or acceptance basis; affected units show `drift` or `unclassified`. Production is not blocked: foreign commits remain in Git and can be built and released; what remains open is governance closure. Agent overstep, manual edits, collaborator branches, foreign-agent work, legacy import and corruption repair all use this one route.

## 12. Migration and live coexistence

### 12.1 Governance modes

Every unit is in exactly one governance mode at any ledger position (M3):

| Mode | Meaning |
|---|---|
| `NATIVE` | SSDS-governed: acceptance, conformance and evidence obligations derived and enforced by Admission |
| `LEGACY(p)` | governed by a declared legacy process bound to protocol version `p` (for example document-controlled SSDP 6.6); SSDS records and derives but does not adjudicate or reinterpret |
| `UNGOVERNED` | production content with no authority system yet (Case C); changes are recorded, mechanical consequences derived, no conformance claims made |
| `UNCLASSIFIED` | unknown content; excluded from governing context, evidence and acceptance basis until classified |

Mode transitions are admitted lifecycle records. A change touching units in several modes receives the union of their obligations. Changes confined to `LEGACY(p)` or `UNGOVERNED` units may arrive as ordinary commits; they are absorbed mechanically (§6.6, §11) and derive only intake classification for uncovered paths plus whatever the mode's policy requires.

**Relying on legacy authority.** SSDS never adjudicates a `LEGACY(p)` unit, but native work often depends on legacy authority that its own process did accept (for example SSDP source accepted through `PROTOCOL-RELEASE-STATE.yaml`). A `LEGACY_ACCEPTANCE` judgment imports that fact: it cites the legacy process's acceptance evidence for an exact revision and sets `acc(u)`, without claiming SSDS reviewed it. Native work relying on a legacy unit without an imported acceptance is provisional.

### 12.2 Reconstruction status and refinement

Authority-bearing units also carry a reconstruction status: `OPAQUE` (internal semantic structure unknown), `PARTIAL`, `RECONSTRUCTED`. **Refinement** is an admitted change that partitions a unit's region into child units; scope conservation is checked mechanically (children's regions are disjoint and their union is the parent's region). Coarse relations to and from the parent stay on its lineage until redirected to children by authored relations. A byte-preserving partition with unchanged relations carries the parent's *acceptance* to the children by rule, because meaning did not change; it never carries the parent's *completeness*. Implicit dependencies between sibling sections that the coarse unit covered are therefore kept conservatively: each child's closure widens to its enclosing scope (the former parent region) until a completeness judgment narrows it (§6.4). Any content or relation change carries nothing. Structural refinement (splitting a large opaque region into smaller opaque regions) needs no semantic claim and enables parallel reconstruction.

This replaces LegacyAggregate: a legacy aggregate is simply a coarse `OPAQUE` unit, and "digestion" is refinement.

### 12.3 Discovery bottom-up, acceptance top-down

Agents may propose candidate D3, D2 and D1 units reconstructed from D4 behavior, papers, comments, tests and history (reconstruction judgments). A proposed upstream unit is accepted only through its owner's acceptance (human-gated where policy requires). Until then, descendants that rely on it are provisional, and no D4 behavior creates accepted authority. Reconstruction that cannot recover intent records `PROVISIONAL` or `UNKNOWN` explicitly (M5).

### 12.4 Cutover

`LEGACY(p)` or `UNGOVERNED` -> `NATIVE` for a unit requires: adequate reconstruction status under policy; a migration-equivalence judgment that representation changed and behavior and meaning did not (or a separately governed change if they did); owner acceptance of the native revision; disposition of every in-flight legacy run on that unit (drained, pinned to its version in an isolated workspace, or explicitly migrated, M6); and an admitted cutover record. After cutover only Admission governs the unit; the legacy representation is historical. Interrupted migration leaves no half state: each refinement and cutover is one admission.

### 12.5 Deployment cases

| Case | How it enters | What is special |
|---|---|---|
| A native project | genesis with fine units; all `NATIVE` | nothing |
| B SSDP 7 or earlier documents | manifest declares section-level units over existing documents without rewriting them; mode `LEGACY(p)`; proposed relations extracted heuristically as `CANDIDATE`/proposed | version-pinned workplans stay governed by their protocol; reconstruction accepts relations; scope-local cutover |
| C mature repository without authority | a few coarse `UNGOVERNED`/`OPAQUE` units by top-level region; analyzers give derived structure early | bottom-up reconstruction proposals, top-down acceptance; production continues |
| D live partial migration | mixed modes | a production edit to a unit makes non-current exactly the reconstruction judgments whose basis named it; unrelated migration work is unaffected — no special rule |
| E external or foreign-agent branch | intake of a change with unknown basis | provenance recorded; obligations derived from touched units |
| F drift or corruption | intake; derived state rebuilt; ledger integrity checked | §13 |

Genesis for an existing repository records project identity, the authoritative ledger replica, trust roots, ruleset version, the initial coverage, and the baseline commit. Per FF-001, no genesis or cutover identity is published as immutable before every required declaration and record exists and validates.

### 12.6 Documents, workplans and skills after cutover

Change plans and authority documents remain semantic artifacts. Lifecycle fields (`status:`) and directory placement (`active/`, `archive/`) in documents governed natively are either removed or generated from derived state and marked non-authoritative; a manual edit to them enacts nothing. Skills remain epistemic procedures and stop owning workflow transitions represented by rules. Historical pre-cutover workplans and records stay immutable under their original semantics.

## 13. Failure, recovery and long-horizon evolution

| Failure | Detection | Repair |
|---|---|---|
| Corrupted derived state | integrity checks, mismatch with re-derivation | discard and re-derive |
| Corrupted ledger | hash chain, schema validation | restore from replica; else truncate to the last verified prefix and admit an explicit ledger-loss record; lost judgments become undischarged obligations; prose or reports may inform new judgments by qualified actors but never restore old records |
| Lost local store, intact repository | absent operator state | ledger is in the repository; operator journal rebuilt; running executions reconciled by observing harnesses and workspaces; stale leases released |
| Repository move, clone | — | project identity is in genesis, not in paths |
| Fork | divergent ledger | a fork record starts a new project identity; cross-fork work enters by intake; ledgers never merge automatically |
| Analyzer version change | derivation key change | re-derive; judgments whose basis named analyzer output become non-current only if the output changed (early cutoff) |
| Relation or record schema change | schema version | explicit READ/MIGRATE/REJECT; migration is an admitted lifecycle record; old records retained |
| Ruleset change | ruleset adoption record | admissions are never re-adjudicated; current derivation uses the adopted ruleset; any previously discharged obligation that the new ruleset no longer considers discharged becomes an open obligation, never a rewritten history; historical views are reproducible with the ruleset in force at their position |
| Interrupted migration | — | refinement and cutover are atomic admissions |
| Very old task returns | basis check | current basis: admissible; stale basis: recorded as observation and routed to revalidation |
| Concurrent results from stale bases | currency at admission | first admitted; others revalidated only where their basis intersects |
| External evidence artifact disappears | availability observation | binding health degraded; present use `UNAVAILABLE`; rerun or remap obligation |
| Manual edit of authority | drift | intake; every reliant record non-current; accepting the edited revision (a light representation-only acceptance when it is editorial) plus an independent equivalence judgment restores reliant records without re-reviewing them; otherwise normal impact closure |
| Migration under a wrong interpretation | later challenge against the reconstruction judgment | challenged reconstruction makes dependents non-current or provisional; blast radius computed from bases |
| Completeness claim proves false | challenge to the completeness judgment | every independence inference that relied on it becomes non-current automatically |
| Admission crash mid-commit | ref/ledger mismatch | reconcile through the effect protocol before any further admission |
| SSDS 9 migrates SSDS 8 | — | ledger is self-describing and versioned; SSDS 9 either reads it compatibly or starts a new lineage with a migration record naming the SSDS 8 head; no reinterpretation of admissions |

Recovery-time objective: derivation of current state must not require replaying an unbounded history; derived checkpoints keyed by `(ledger position, ruleset, schema, analyzer versions)` bound restart cost and are verified against the ledger before use.

## 14. Where machinery must stop

Deterministic machinery prepares, but never decides:

- whether two scientific or numerical formulations mean the same thing, and whether a change is editorial or semantic beyond byte/normalization identity;
- whether an observed discrepancy is a D4 defect or exposes inadequate D3, D2 or D1;
- whether evidence actually supports a governed claim, and whether gate evidence is adequate;
- whether an inferred or searched-for relationship is materially real; whether a relation scope is complete;
- how an ambiguous legacy region decomposes and what its upstream intent was;
- whether an architectural change preserves its parent abstraction;
- whether a Serious Challenge is warranted, how it is adjudicated, and whether a risk override is acceptable;
- whether a marked product surface is accepted (product-scope owner, P7?).

For each, the machinery produces a **focused question**: the exact subject and revisions, the distinctions already resolved, the evidence and its status, what the answer will change, and the allowed outcomes. The answer is a recorded judgment that then propagates mechanically.

## 15. Persistence, trust and security

### 15.1 Stores

| Store | Content | Canonical? | Location |
|---|---|---|---|
| Content store | all repository content including authored relations and unit manifests | yes, for meaning | the project's Git repository |
| Ledger | records (§6.3) | yes, for everything not derivable | reserved ref namespace in the project repository (cycle decision) |
| Derived index | derived state and checkpoints | no | local, rebuildable (SQLite or equivalent, delegated) |
| Operator state | leases, reservations, account and quota telemetry, harness sessions, raw prompts and transcripts, secret references | no project authority | private user-local root outside repositories |
| Transport | task and result envelopes on run branches | no | isolated run refs; retired by policy, never merged |

### 15.2 Ledger in the repository

The consolidated Protocol 8 plan defaulted canonical history to a private local store and allowed in-repository non-secret control state only by explicit D3 adoption resolving concurrency, privacy, history and ownership. This architecture proposes that adoption for the **ledger only**:

- **Ownership and concurrency.** Admission is the only writer. Each ledger names its authoritative replica in genesis; appends are compare-and-swap on that replica's ref (local repository for a single operator; the designated remote for multi-host teams). A losing writer re-validates against the new head, exactly as in §8.2.
- **History.** Records are immutable and hash-chained; the ledger ref is not a product branch, is never merged, and is replicated with ordinary fetch/push. The ledger keeps every content commit it references reachable, so a force-push or branch deletion on product refs cannot make history underivable; such rewrites appear as foreign live-ref movement (§11).
- **Privacy.** The ledger holds bounded non-secret facts and references only. A project may host its ledger in a separate private repository; the requirement is replicability independent of one machine, not public visibility. Because records are immutable, accidental inclusion of sensitive data needs an explicit break-glass procedure (new lineage with a migration record), defined in the Architecture Manual.
- **Why.** It removes the single point of failure of a local-only store, makes clone/move/fork/backup ordinary Git operations, and lets ledger and integration ref update in one reference transaction.

The Architecture Manual may replace the storage concretization if review finds a counterconstraint; the requirements (append-only, hash-chained, replicated with the project independently of any one machine, single writer per ledger) remain.

### 15.3 Actors and authentication

Agents are not principals with authority; their records are proposals attributed to an execution identity (harness, route, model, task, attempt) observed by the Dispatcher. Humans are authenticated through a trust mechanism declared in genesis and changeable only by a human-gated lifecycle record (for example signed records with registered keys, or an explicitly declared single-user local trust). No guarantee beyond the implemented mechanism is claimed.

### 15.4 Protected surfaces and untrusted input

Agents cannot modify the ledger, rules registry, project policy, schemas, trust roots, unit governance state or issued task envelopes; changes to rules, policy and schemas are their own governed changes requiring a human gate. Admission detects any touch of a protected surface. Agent branches and result envelopes are untrusted until validated; malformed or adversarial records cannot inject actions; agent-reported test results are never admissible evidence (§10). Unknown executable or binary content is classified statically and never executed or deserialized to classify it. Paths are repository-contained. Evidence, memory and external text are data.

## 16. Components and ownership

| Component | Owns | Never does |
|---|---|---|
| Content Model | unit declarations, coverage partition, authored relation extraction, unit revisions | store status |
| Analyzers | derived relations and their incompleteness declarations | claim completeness they do not have |
| Ledger Store | append-only persistence, hash chain, replication | interpret records |
| Derivation Engine | all derived state and queries (§6.5) | write canonical state |
| Admission | validation and the only writes to ledger and integration ref | judge semantics; perform agent work |
| Dispatcher | scheduling among ready obligations (resource/account/model feasibility, route selection, reservations), workspaces, harness adapters, external effects, operator state | decide readiness or completion; act as a second admission |
| Interface | logical operations, transports, version-bound brief and gate rendering | hold state of its own |

Dependency direction: Content Model and Analyzers <- Derivation <- {Admission, Interface, Dispatcher}; Ledger Store is read by Derivation and written only by Admission; Dispatcher submits trusted-runner evidence realizations and canonical-effect outcomes through Admission. Scheduling decisions never influence derived workflow state; the route, harness, model and attempt provenance they produce travels in submitted records and is replayed as recorded fact, never recomputed against current resources.

**Supersession of Orchestrator Architecture 1.6.0** (frozen, `orchestrator/docs/architecture.md`), for SSDS-governed scopes only, to be carried out by the Architecture Manual rather than layered beneath it:

| 1.6.0 invariant | Disposition |
|---|---|
| 6 no duplicated workflow authority; Tracker is evidence only | replaced: ledger + Admission is the single workflow authority; workplans and profiles stop owning transitions |
| 7 manual operation first-class and complete | narrowed: manual invocation of agents remains; manual document control is not complete for native scopes |
| 24 workflow routing is profile-owned | replaced: rules registry; profiles remain for version-bound rendering |
| 1-3 capability ladder, graceful degradation | replaced by staged usefulness: read-only derivation and interface are useful without Admission (§23); Core prompt mode remains for version-bound older work |
| 11 private state outside repositories | narrowed: operator state stays private; the non-secret ledger is adopted into the repository (§15.2) |
| 2, 4, 5, 13, 14, 23, 26 dependency direction, one composition root, versioned boundaries, stable IDs, query/mutation separation, one mutating run per worktree, repository containment | preserved |

The Tracker (Level 1) was never implemented; only Level 0 Core exists. No Tracker data needs migration.

## 17. Mechanisms deliberately removed

| Removed | Replaced by |
|---|---|
| AuthorityGraph, WorkGraph, CodeGraph, EvidenceGraph as canonical families | units + authored/derived/proposed relations; graphs are views |
| AuthorityEpoch | per-record basis |
| Whole-plan PlanRevision freeze, planning/working phases, global replanning stop | item-level plan revisions, plan acceptance judgments, scoped amendment |
| Freeze frontier as a concept | readiness rule over validity |
| Event-sourced control state and stored lifecycle FSMs | immutable ledger of judgments/observations/admissions; pure derivation |
| WorkGraph node kinds (barrier, router, integration gate, review/qualification gate) | obligations typed by required judgment kind and actor qualification |
| WorkClaims as safety mechanism | optimistic admission; advisory footprints; declared serialization surfaces |
| GraphTransaction, candidate overlay, GraphDelta, DIRTY marking | Git candidate + derivation keyed by content; diffs derived on demand |
| Context Resolver and Semantic Projection Layer as components | derivation queries + interface templates |
| Project Ingestion and Reconciliation Engine (four modes) | intake rules over changes with unknown basis |
| LegacyAggregate | coarse `OPAQUE` units; refinement |
| "UNKNOWN_BUT_ACTIVE is invalid" | total coverage with explicit `UNCLASSIFIED` status and restricted use |
| Graph history/diff subsystem | derived diff between two ledger positions |
| Mandatory refactor of D1-D3 into per-node documents | adaptive unit granularity, inline or manifest declaration |
| Seventeen MCP operations | six logical operations, transport-neutral |

## 18. Inheritance and capability transfer

### 18.1 Consolidated Protocol 8 plan

Every section of `workplans/archive/SSDP-8.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-CONSOLIDATED.md` is disposed below. That plan itself carried, as one composition, these archived records (`workplans/archive/<id>.md`): `SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION`, `SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-1-SECOND-REVIEW-CLOSURE`, `SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-2-DETERMINISM-AND-RECOVERY-CLOSURE`, `SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-3-PROTOCOL-6.2-INHERITANCE-RECONCILIATION`, `SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-4-PROTOCOL-6.3-INHERITANCE-RECONCILIATION`, `SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-5-PROTOCOL-6.4-INHERITANCE-RECONCILIATION`, `SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-6-PROTOCOL-6.5-INHERITANCE-RECONCILIATION`, `SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-7-PROTOCOL-6.6-INHERITANCE-AND-D3-REASSESSMENT`, `SSDP-8.0-DETERMINISTIC-ORCHESTRATOR-VERSION-REBIND`. Their historical inheritance dispositions (6.2-6.6 reconciled; D3 reopen required; D4 not authorized) remain true and are carried here. "Carried" means binding here with unchanged meaning; "Replaced" means an equal-or-stronger mechanism; "Changed" means a deliberate D3 decision with reason.

| Predecessor | Disposition |
|---|---|
| §1 control plane coordinates and indexes, never reproduces semantics | Carried (§6.3, C7) |
| §2 lossless inheritance of all accepted doctrine incl. 6.2 representation and 6.3 PEM; no mirror registries; inadequacy reopens D3 | Carried (§2, §20) |
| §3.1 deliberate supersession of Architecture 1.6.0; no hidden layer | Carried (§16) |
| §3.2 Protocol 6.6 reassessment input | Carried; this revision is a proposed reassessment, adjudicated only by independent D3 Review (§21) |
| §4 reducer vs Scheduler; scheduling decisions recorded and replayed as facts | Carried and strengthened as Admission/Derivation vs Dispatcher: scheduling can no longer affect derived workflow state at all; its provenance is recorded fact (§7.3, §16) |
| §5 planes; §5.4 semantic owner vs control projection, mismatch blocks, classification provenance | Carried and strengthened: authored relations inside content remove one mismatch class; drift detection covers the rest (§6.2, §11) |
| §6 minimal control data; four anti-duplication rules | Carried (§6.3, §12.6) |
| §7 versioned formal schemas, canonical interchange, forward compatibility, fail-closed unknown required semantics | Carried (§6.3, §6.6 step 1) |
| §8 logical identity vs revision; prefer Git identity; no universal per-claim hash graph without need | Carried; unit revisions are computed from Git content, justified by locality (§6.1) |
| §9 typed relations; completeness scoped; absence not independence | Carried and strengthened: completeness is a judgment in the basis (§6.2) |
| §10 evidence formalization without bulk migration | Carried (§10) |
| §11 composed state dimensions | Replaced: derived classifications (§6.5) |
| §12.1 version-bound replay; no silent reinterpretation; explicit migration | Replaced by the derivation property plus never-re-adjudicated admissions (§6.5, §13) |
| §12.2 reducer purity and observation boundary | Carried (§6.5, C3) |
| §12.3 snapshots derived and verified | Carried (§13) |
| §13 seven validation layers; single canonical writer; humans decide meaning, writer serializes | Carried (§6.6, §9.4) |
| §14 external effects | Carried (C4, §6.6) |
| §15.1 private canonical store by default; in-repository only by explicit D3 adoption | **Changed**: ledger adopted into the repository with the four consequences resolved; operator state stays private (§15.2) |
| §15.2 durability and recovery contract | Carried and strengthened (§13, §15) |
| §16 formal action registry | Replaced by the rules registry (§6.5) |
| §17 schema-valid agent outputs; no prose parsing | Carried (§9.1) |
| §18.1-18.2 TaskEnvelope / ResultEnvelope | Carried: envelope = obligation + basis + brief; result = records + candidate (§9) |
| §18.3 candidate identity without self-reference | Carried (§6.6) |
| §18.4 transport artifacts not merged; protected surfaces | Carried (§15.4) |
| §19 agent PASS is not canonical PASS | Carried (§7.4) |
| §20 human gates, risk override, Serious Challenge preservation | Carried (§9.4, §7.4) |
| §21 deterministic impact; materiality by judgment | Carried and made central (§6.4) |
| §22 workplans/skills after cutover; lifecycle metadata non-authoritative | Carried (§12.6) |
| §23 minimal activation and bootstrap locator | Carried (§9.5) |
| §24 one logical protocol, multiple transports; polling first | Carried (§9.5) |
| §25 isolation, atomic publication, stale/duplicate/partial results | Carried and strengthened by basis currency (§8.2) |
| §26 security | Carried (§15) |
| §27 failure semantics; no implicit document fallback; manual work is non-canonical until admitted | Carried (§12, §24) |
| §28.1 pre-cutover baseline identities from release state; public fallback and recovery distinct | Carried (§24) |
| §28.2 rollback is version rollback; no dual-current control | Carried (§24) |
| §28.3 cutover quiescence: drain, pin or migrate | Carried, per unit (§12.4) |
| §29 migration phases incl. shadow comparison and difference classification | Replaced by §23, classification carried |
| §30 D3 obligations 1-15 | Carried into §21 |
| §31-§32 failure and semantic/adversarial qualification | Carried into §22 |
| §33 versioning and historical preservation | Carried (§24) |
| §34 acceptance criteria | Carried into §25 |
| §35 non-goals | Carried (§20) |
| §37 version rebind, Protocol 7 inputs and reconciliation contract | Carried (§0, §19) |

### 18.2 befe678 hypothesis capabilities

| Capability | Where preserved |
|---|---|
| Machine-readable D1-D3 relations with layer direction and SCC handling | §6.2 |
| Derived code dependencies with explicit blind spots | §6.5 analyzers |
| Evidence applicability metadata | §10 |
| Typed, non-flattened relation classes | §6.2 |
| Reviewed plans; immutable accepted plan content; no retroactive requirements | §7.2 |
| Modular plans with structure separate from runtime state | §7.1, §12.6 |
| Iteration vs attempt vs plan vs authority revision | §7.3, §6.1 |
| Deterministic, explainable, version-bound context with explicit gaps | §9.2-§9.3 |
| Minimum-semantic-burden interface | §1.2, §9 |
| Safe parallelism and integration checks beyond textual merge | §8 |
| Direct writes allowed in isolated workspaces | §6.6, §11 |
| Incremental maintenance equal to full rebuild | §6.5, §22 |
| Structural history and diffs | §6.5 derived views |
| Repository explainability, artifact trust, classification, dispositions | §6.1 coverage, §11 |
| Progressive migration, scope conservation, coarse boundary edges, uncertainty | §12 |
| Discovery bottom-up, authority top-down | §12.3 |
| Mandatory orchestrator after scope-local cutover, legacy envelopes | §12.1, §12.4 |

## 19. Protocol 7 prospective inputs (not final)

Protocol 7 closure is active; nothing here binds Protocol 7 semantics or selects an inheritance. Known prospective inputs and where they would land:

| Input | Landing point | Open question for Phase A |
|---|---|---|
| Gate-evidence adequacy is semantic, not a presence predicate; non-narrative evidence core separable and read first | §9.4 | final gate-brief obligations |
| Realized scientific record and feedback persistence live in existing project artifacts; no universal discovery database | §10 (native artifacts referenced) | whether the ledger may be a project-designated canonical home for findings/tensions, or must only index external homes |
| One canonical home per finding; tension binding to authority identity and earlier revisions; native attribution as asserter | §6.3, §11 | mapping of tension search to unit identity and refinement lineage |
| Marked product inspectability surfaces accepted by product-scope owner, never by technical D3 Review | §14 | judgment kind and actor qualification |
| Claim-integrity floor on agent assertions | §9 report/submit | none expected at architecture level |
| Stage F fail-closed evidence-state model separating transport success from evidence admissibility (evidence-only lesson) | §9.5, §10 | final portable execution-profile semantics for the Dispatcher |
| Pre-cutover baseline advances to Protocol 7 recovery/public fallback (distinct) | §24 | exact identities from release state |

## 20. Non-goals

SSDS 8.0 does not: convert scientific reasoning or evidence into machine JSON; encode scientific truth in rules; require a graph database, network database or distributed consensus; infer independence outside declared-complete scope; let agents write canonical state; let derived relations override source; let D4 behavior create accepted D1-D3 authority; treat Git branches, commits or PRs as workflow semantics; require every write to pass through an interface; expose machine records as routine agent UX; use search as an authority resolver; execute unknown artifacts to classify them; force all-at-once migration or stop valid production for incomplete migration; allow two current authorities or processes over one unit; use migration as a hidden redesign channel; keep document-controlled workflow as a dual-current fallback for native scopes; add webhooks, brokers or hosted services before polling and local operation prove insufficient; add registries, wrappers or fields solely to mirror inherited doctrine; provide atomic admission across multiple repositories (cross-repository work references external units by immutable identity).

## 21. D3 closure obligations before D4

The SSDS 8 Architecture Manual, independently reviewed, SHALL decide and document:

1. unit model: declaration syntax classes, manifest ownership, revision normalization, coverage partition rules, single-definer rule;
2. relation vocabulary, classes, direction, layer and grouping rules, completeness-judgment semantics;
3. record schemas, judgment kinds, actor qualifications, outcome vocabularies, compatibility contract;
4. basis composition per judgment kind, consumption classes, conservative widening, equivalence scope;
5. derivation property, rules registry, stratification, analyzer contract (deterministic vs recorded), checkpoint and recovery-time bounds;
6. Admission validation order, optimistic concurrency, merge-queue serial order, atomicity and effect reconciliation;
7. obligation rules, readiness, discharge predicate, provisional propagation, iteration/attempt identity;
8. change-plan structure, plan acceptance, scoped amendment policy, plan invariants;
9. serialization policy surfaces, generated-unit handling, joint invariants, residual-risk disclosure;
10. interface operations, query classes, brief and gate templates, epistemic labels, read recording, transports, bootstrap locator;
11. evidence realization basis fields for scientific regimes, stochastic replicates, environments and precision; trusted-runner designation and custody for expensive external realizations;
12. intake detection, static classification, dispositions, trust/quarantine;
13. governance modes, legacy-acceptance import, reconstruction status, refinement (including completeness non-transfer), cutover, quiescence, genesis;
14. ledger storage, replication, authoritative replica, break-glass procedure; operator-state boundary; derived index;
15. actor identity and human authentication trust roots;
16. protected surfaces and SSDS self-governance of rules/schemas;
17. component boundaries and dependency direction; Dispatcher/Admission separation; explicit supersession of Architecture 1.6.0;
18. ruleset/schema evolution and SSDS-to-successor migration;
19. versioning: system, schema, ruleset, interface and profile versions kept distinct;
20. final Protocol 7 inheritance (§19) and the pre-cutover baseline;
21. a minimum-justified-architecture reassessment against the then-current accepted baseline, including whether every primitive in §5 is still needed.

## 22. Qualification program

Qualification binds every claim to the property its method can discriminate (DS-001): synthetic fixtures establish mechanical properties only; semantic adequacy needs real-owner cases and independent Review. Required, at minimum:

- **Determinism and replay.** Identical derived state from identical ledger, content and ruleset; independence from wall clock and live external state; incremental equals from-scratch derivation; checkpoint corruption detected and rebuilt; ruleset and schema evolution fixtures; historical admissions never re-adjudicated; historical views reproducible.
- **Currency.** Upstream change makes exactly the reliant records non-current; re-review without content change backdates descendants; equivalence judgments scope correctly; conservative widening when completeness is absent; a falsified completeness judgment invalidates every inference that used it; drift blocks dependent use.
- **Admission and concurrency.** Disjoint bases admit concurrently; intersecting bases revalidate; write-skew across disjoint files caught through recorded reliance; clean Git merge with semantic conflict blocked; stale, duplicate, partial and very late results; unauthorized protected-surface edits rejected; agent-modified envelopes rejected; duplicate discharge rejected; a D4 change that breaks another closure on the merged tree rejected while an accepted upstream authority change legitimately reopens dependents; live-ref movement absorbed as drift without blocking production; self-declared equivalence backdates nothing; crash at every admission boundary; ref/ledger mismatch reconciled; multi-host compare-and-swap loser revalidates.
- **Effects and dispatch.** Crash after intent before start; after start before outcome; scheduler decisions replayed as facts; Dispatcher cannot discharge or ready anything; unavailable network, Git remote or harness; interrupted harness; cancellation.
- **Interface.** Same brief for same basis; inclusion reasons and epistemic labels correct; incompleteness surfaced; candidate items cannot support closure; zero-context web agent locates its task from the bootstrap; local and Git-envelope transports give identical admissions for identical submissions; verbose or alternative prose cannot change outcomes when structured content is identical.
- **Evidence.** Execution change forces rerun; target change forces reassessment; specification survives concretization replacement; stale passing and stale failing evidence inadmissible; unavailable artifact degrades binding health; transport success without complete evidence cannot enter assessment; agent-reported results never discharge evidence obligations; proxy evidence cannot close the real owner.
- **Intake.** Manual edit, untracked generated file, opaque binary (quarantined, never executed), external branch, authority-like document, agent overstep — each through the one route; unclassified content excluded from governing context and evidence.
- **Migration.** Whole-repository single opaque unit; scope-conserving refinement; byte-preserving split carries acceptance but not completeness, so sibling reliance widens; any other split carries nothing; native reliance on legacy authority is provisional without an imported legacy acceptance; coarse relations redirected; production edits invalidate only intersecting reconstruction; no dual-current mode; bottom-up proposals never self-accept; per-unit cutover with drained/pinned/migrated in-flight work; final disappearance of `OPAQUE`/`UNGOVERNED` material closes migration coverage.
- **Semantic and adversarial.** A coherent-D3 D4 defect stays D4; a downstream observation can challenge D3, D2 or D1 and blocks dependent closure; machinery never auto-resolves scientific ambiguity; risk override stays visibly provisional; a missing required check never becomes PASS; documents' lifecycle fields enact nothing; historical reasoning remains reachable; no second authority emerges.
- **Security and privacy.** No secrets or private telemetry in the ledger or repository by default; adversarial records cannot inject actions; human decisions require the declared trust mechanism.
- **Usability.** Live trajectories on real tasks, in shadow mode, showing that agents complete bounded work without reading machine records and with less context than the document-controlled baseline. Claims stay bounded to the trajectories, harnesses and models actually exercised, consistent with the Protocol 6.6 stochastic robustness boundary.
- **Repository acceptance.** The inherited repository workflow (regression, PEM checks, package build/validation, distribution parity, whitespace, frozen-resource integrity, Orchestrator Core snapshot/tests) for every affected surface.

## 23. Development sequence

- **Phase A — Protocol 7 reconsolidation.** After Protocol 7 closes, bind its exact identities and inputs (§19), advance the pre-cutover baseline, and recommend (not self-adopt) a governing-version adoption for this family.
- **Phase B — independent D3 falsification of this architecture.** May begin before Phase A as hypothesis testing; its PASS cannot authorize D4 until Phase A and Phase C close.
- **Phase C — SSDS 8 Architecture Manual** resolving §21, independently reviewed, with explicit stakeholder acceptance of this major change.
- **Phase D — read-only kernel (shadow, no authority).** Content Model, Analyzers, ledger schema and Derivation over this repository, with a shadow genesis from existing history. Value: currency, impact and "what governs" answers with no control change.
- **Phase E — read-only interface.** `open/ask/read` offered to agents working under the document-controlled baseline; measure burden reduction by live trajectories.
- **Phase F — Admission and Dispatcher in shadow.** Compute admission decisions beside document control; classify every material difference as SSDS defect, baseline ambiguity/defect, deliberate stronger rule, or unresolved semantic judgment; independently review each.
- **Phase G — intake and migration pilot.** This repository's legacy documents (Case B) and one external scientific repository (Case C/D) without disturbing production.
- **Phase H — adversarial and fault qualification** (§22).
- **Phase I — scope-local native cutover** after accepted architecture, implementation acceptance, shadow qualification, independent Review, required human/project approval and demonstrated rollback.

## 24. Cutover, rollback and versioning

- The pre-cutover baseline is the accepted document-controlled protocol resolved from `PROTOCOL-RELEASE-STATE.yaml` (currently Protocol 6.6: recovery `384666764da4c55b282e6b1595ab97e2f86e1dc4`, public fallback `22f4bdba53795da3a6f13f162529f3a843fc37ae`, distinct). It advances only by an explicit inheritance reconciliation (Phase A).
- Older version-bound work stays under its declared version and immutable source; every supported orchestration profile stays frozen and independently testable (PC-001); migration never reinterprets old records as authored under SSDS 8.
- Native cutover is per unit; after cutover no document-controlled process governs that unit. Shadow comparison is permitted only while one side is explicitly non-authoritative.
- Orchestrator unavailability yields truthful non-closure for native scopes, never implicit document-control fallback. Exploratory or report-only work may proceed but claims no canonical closure until admitted.
- Rollback is version rollback to the immutable pre-cutover baseline: stop Admission for the affected scope, resume the pinned baseline process there, repair SSDS separately.
- System, schema, ruleset, interface and profile versions are distinct and never conflated with protocol semantic version.

## 25. Acceptance criteria for the architecture cycle

D4 handoff is possible only when:

1. Protocol 7 inheritance is reconciled (Phase A);
2. one accepted Architecture Manual resolves every §21 obligation;
3. exactly one canonical writer exists per ledger and no document, profile, tracker, scheduler or derived view can enact a transition;
4. the five primitives and their derived semantics are fully specified, including currency, validity, discharge and provisional propagation;
5. every §18 inherited guarantee and capability is carried, replaced with equal-or-stronger evidence, or retired with accepted reason;
6. concurrency correctness rests on admission-time validation, with residual risk stated;
7. intake is the single route for unknown-provenance change, and migration is coverage refinement with per-unit cutover;
8. persistence, replication, recovery and evolution are specified and survive loss of any one machine;
9. the agent interface meets the minimum-semantic-burden invariant, demonstrated by live trajectories in shadow mode;
10. independent D3 Review/Challenge finds no blocker or active governing Serious Challenge;
11. stakeholder acceptance of this major architectural change is explicit.

## 26. Reopen triggers and open uncertainties

Reopen this architecture if: conservative widening makes too much work non-current to be useful on real repositories; read recording proves infeasible across target harnesses so that bases are systematically too weak; unit declaration cost outweighs locality benefit at practical granularity; ledger-in-repository storage fails privacy, scale or hosting constraints; Protocol 7 finalizes semantics that require the ledger to be, or forbid it from being, a canonical home for findings; live trajectories show agents still doing bookkeeping; or any inherited guarantee proves unpreservable under §6.

Uncertainties that cannot close by design work alone:

- **Protocol 7 dependent:** gate-brief obligations; finding/tension canonical home; product-surface acceptance actor; final pre-cutover baseline; execution-profile semantics from Stage F portability.
- **Empirical:** rate of false staleness under conservative widening; analyzer completeness for real Python and C++ scientific code; feasibility of read recording per harness; practical unit granularity; derivation cost and checkpoint sizing on large repositories; ledger growth over years; agent context and success compared with the document-controlled baseline.

## 27. Handoff state

```text
GOVERNING DESIGN PROTOCOL: SSDP 6.6.0
TARGET: SSDS 8.0.0
ARCHITECTURE: basis-stamped judgments over content-addressed units; ledger + pure derivation;
              single Admission writer; optimistic concurrency; one intake route; refinement-based migration
SOURCE SNAPSHOT: f96b7ccf90dede4150d0efa17264fff07ec12d0d (ssdp-7.0-scientific-epistemic-closure)
DESIGN BASIS: befe6782e7c8fe038bf7cb764646d133ca167855 (befe678 hypothesis archived byte-identically)
THIS WORKPLAN: proposed; not accepted-current
SSDP 7: active closure; inheritance NOT FINAL; Stage H reconciliation targets this file
D3: ready for fresh independent falsification Review; D4 handoff requires Phases A and C
D4: NOT AUTHORIZED
SERIOUS CHALLENGE: none
NEXT ACTION: fresh independent D3 Review of this architecture by a context that authored neither it nor
             its predecessors; preserve the branch while Protocol 7 closes; then Phase A.
```
