---
kind: ssds-major-architecture-workplan
workplan_id: SSDS-8.0-GRAPH-NATIVE-DETERMINISTIC-ORCHESTRATION-ARCHITECTURE
protocol_version: 6.6.0
target_system_version: 8.0.0
status: proposed
created_date: 2026-10-01
source_branch_basis: f96b7ccf90dede4150d0efa17264fff07ec12d0d
source_branch: ssdp-7.0-scientific-epistemic-closure
design_review_state: pending-independent-d3-review
d3_architecture_state: proposed
implementation_handoff: not-authorized
active_serious_challenge: none
supersedes:
  - SSDP-8.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-CONSOLIDATED
---

# SSDS 8.0 — Graph-Native Deterministic Orchestration Architecture — Prospective Workplan

## 0. Disposition and scope

This is the single current prospective architectural workplan for **SSDS 8.0**, the graph-native deterministic successor to the document-driven SSDP workflow. It is governed for design purposes by SSDP 6.6.0 and is **not** accepted-current architecture, an implementation authorization, or an SSDS 8.0 cutover decision.

This workplan deliberately replaces the narrower "deterministic control plane / mandatory orchestrator" framing with an integrated architecture in which:

- semantic authority is represented as versioned graph-native D1-D3 authority units plus canonical typed relations;
- D4 code remains executable authority while machine-generated code/file/symbol dependency graphs are derived from exact source revisions;
- work is represented by an accepted versioned WorkGraph rather than a monolithic mutable workplan;
- runtime lifecycle state is reduced deterministically from accepted events;
- graph traversal provides context retrieval, impact analysis, work readiness, and dependency resolution;
- graph-aware transactions keep repository mutation and graph state synchronized;
- Git supplies isolated candidate execution and integration substrate without becoming semantic workflow authority;
- MCP/harness APIs expose compact semantic operations to agents while hiding raw graph/control machinery by default;
- reconciliation, import, migration, and semantic reconstruction are first-class paths back into the same graph ecosystem;
- partially migrated legacy projects remain executable and can be progressively "digested" from opaque legacy aggregates into native graph units.

The active SSDP 7.0 branch remains the current development line for Protocol 7 closure and the latest manual/document-driven workflow fallback. This SSDS 8.0 design branch is intentionally isolated. Before implementation, the workplan SHALL be re-consolidated against the final accepted Protocol 7 recovery/semantic state and any material Protocol 7 inheritance obligations.

No SSDS 8 D4 implementation is authorized by this workplan.

## 1. Governing design objective

SSDS 8.0 SHALL move every mechanically decidable operation out of agent cognition and into deterministic machinery wherever practical.

The governing allocation is:

```text
mechanical identity / dependency / relevance / state / provenance /
impact / concurrency / synchronization / consistency question
    -> deterministic program

resolved semantic question
    -> accepted authority

unresolved semantic question
    -> agent

human-authority decision
    -> human gate

canonical workflow transition
    -> deterministic reducer
```

The agent is a semantic reasoning resource, not a graph database operator, dependency resolver, workflow tracker, Git coordinator, or bookkeeping engine.

The system SHALL minimize agent cognitive burden. Raw graph records, event streams, transaction internals, normalized relation tables, digests, and machine schemas remain inspectable but cold. The normal agent interface SHALL present the smallest decision-sufficient semantic projection.

## 2. Architectural planes and ownership

SSDS 8.0 separates five logical planes:

1. **Semantic Authority Plane** — D1-D3 accepted authority nodes and their canonical typed semantic relations.
2. **Executable / D4 Plane** — code, configuration, schemas, build definitions, tests, and other D4 artifacts; code remains authoritative for executable behavior.
3. **Work Plane** — accepted WorkGraph definitions, modular node plans, review/human/integration gates, and cycle-scoped transformation intent.
4. **Control Plane** — append-only accepted control events, deterministic reducer, derived runtime state, obligations, leases, transactions, and concurrency state.
5. **Interaction Plane** — semantic projection, Context Resolver, MCP/harness interfaces, TaskEnvelope/ResultEnvelope, human-gate presentation, and debugging views.

No plane may silently acquire another plane's semantic authority.

## 3. Canonical graph families

### 3.1 AuthorityGraph

D1-D3 authority SHALL be refactored from monolithic documents into graph-native authority families.

A native authority family consists of:

- stable logical node identity;
- immutable semantic revision identity;
- modular human-readable node/sub-authority document;
- canonical typed outgoing relations;
- lifecycle state and accepted revision binding;
- source/provenance sufficient to reconstruct current ownership.

Representative relations include:

- `USES_DEFINITION`
- `CONCRETIZES`
- `DEPENDS_ON`
- `ASSUMES`
- `CONSTRAINED_BY`
- `SUPERSEDES` / `REPLACES`
- `CHALLENGES` / `CONTRADICTS`
- `EVIDENCES`
- `GENERATED_BY`

For semantic prerequisite relations, stored direction is subject -> prerequisite. Reverse traversal is impact analysis, not a second authority relation.

D1-D4 abstraction ordering is a DAG after explicit condensation of legitimate simultaneous definitions. A higher abstraction may not depend semantically on a lower concretization. Lower layers may depend on same-layer prerequisites and applicable higher-layer authorities. Any nontrivial same-layer strongly connected component must be explicitly declared as a simultaneous/composite definition; accidental circular warrant is invalid.

### 3.2 WorkGraph

The WorkGraph is the canonical cycle-scoped execution plan. It defines **what transformations/gates exist and their structural relationships**. It does not store mutable runtime progress.

Each plan revision contains:

- node identities and node kinds;
- dependency and conditional edges;
- output slots and acceptance predicates;
- authority/read/write claims;
- required evidence and human gates;
- retry/iteration/rework routes;
- join/integration points;
- references to modular semantic node plans.

Node kinds include at minimum:

- work;
- review gate;
- human gate;
- qualification gate;
- integration gate;
- synchronization barrier;
- decision/router;
- reconciliation/recovery node.

The flowchart is a projection of the WorkGraph, never a second editable authority.

### 3.3 CodeGraph

The CodeGraph is derived from exact D4 source identity plus analyzer/tool version. It may include:

- files/modules/packages;
- symbols/types/functions;
- imports/calls/links;
- build dependencies;
- tests/consumers;
- generated/source relationships;
- mappings from D4 elements to governing D3 authority.

Mechanically derived code relations SHALL be regenerated from source, not manually edited to contradict the source. D4 code remains the authoritative executable artifact.

Language-specific graph providers MAY use compiler/build/language-native dependency machinery. Static incompleteness, reflection/dynamic registration, generated code, runtime configuration, and external consumers must remain explicit blind spots where material.

### 3.4 EvidenceGraph

Detailed evidence remains in native artifacts. The graph stores only bounded relationships and applicability metadata necessary to answer what claim/revision an evidence realization supports, what execution regime it exercised, whether it is current/admissible/stale/challenged, and which change invalidates it.

### 3.5 Graph relationships are typed, not flattened

Semantic dependency, execution dependency, evidence support, repository containment, historical relation, work sequencing, and generated/derived relation are distinct edge classes. No generic "related-to" edge may be used to manufacture deterministic closure where relation semantics matter.

## 4. Planning phase and frozen PlanRevision

SSDS 8.0 has two top-level lifecycle phases:

```text
PLANNING
  construct/revise WorkGraph
  -> review
  -> revise on NO-PASS
  -> independent PASS
  -> ACCEPTED_FROZEN PlanRevision

WORKING
  issue only tasks bound to accepted PlanRevision
  -> execute / review / integrate / reconcile
```

A WorkGraph under construction is never executable authority.

Planning lifecycle is intentionally small:

```text
CONSTRUCTING -> REVIEW_READY -> UNDER_REVIEW
      ^                              |
      |----------- NO_PASS ----------|
                                     |
                                    PASS
                                     v
                              ACCEPTED_FROZEN
```

Every accepted PlanRevision is immutable. A material topology/contract change creates a successor PlanRevision through the same review loop.

During replacement-plan review, the conservative default is to stop issuing new mutating tasks. Existing isolated candidates may finish, but integration waits for applicability reconciliation. Later implementations may permit scope-local replanning only after proving unaffected WorkGraph subgraphs can safely continue.

## 5. Modular node plans

A large workplan SHALL be represented as a small structural plan plus modular node documents rather than one continuously amended monolith.

Conceptually:

```text
workplans/<plan-id>/
  plan.<structured-format>
  nodes/
    <node-A>.md
    <node-B>.md
    ...
```

The structural plan owns topology, node identities, typed dependencies, gates, output bindings, claims, and references. Node documents own the human-readable objective, governing authority, rationale, delegated space, non-goals, affected surfaces, acceptance obligations, semantic questions, and reopen triggers for that node.

Mutable runtime states such as running/completed/blocked SHALL NOT be manually edited into the plan definition.

## 6. Authority revisions, epochs, and the freeze frontier

Every task binds to immutable accepted upstream authority revisions rather than "whatever is current."

An **AuthorityEpoch** is the accepted version-coherent snapshot of authority identities/revisions used by control decisions. It does not require copying all semantic content into the control store; it binds exact source identities.

Work may produce candidate authority revisions, but a candidate never becomes an upstream prerequisite merely because it exists. The sequence is:

```text
accepted authority revision
 -> work against exact revision
 -> candidate successor
 -> owning-domain Review / human gate where required
 -> accepted successor
 -> new AuthorityEpoch
 -> deterministic impact propagation
```

Lower-layer work is ready only when its complete material upstream prerequisite closure is accepted/frozen. This creates a **freeze frontier** through the authority DAG rather than a global D1-then-D2-then-D3 waterfall. Independent branches may advance concurrently when their own prerequisite closure is frozen.

A planned downstream node may depend on the accepted output slot of an upstream node. At issue time, the TaskEnvelope replaces that symbolic dependency with exact immutable authority revisions.

## 7. State decomposition, iteration, attempt, and revision identity

Runtime state SHALL use composed dimensions rather than a monolithic FSM.

Representative dimensions:

- Execution: `PENDING`, `READY`, `RUNNING`, `BLOCKED`, `WAITING_HUMAN`, `COMPLETED`, `CANCELLED`.
- Outcome: `NONE`, `PASS`, `NO_PASS`, `INCONCLUSIVE`, `CHALLENGE`, `SERIOUS_CHALLENGE`.
- Validity: `CURRENT`, `REVIEW_REQUIRED`, `STALE`, `INVALID`.
- Authority lifecycle: proposed, accepted-current, challenged, superseded, retired, provisional/risk-accepted as applicable.
- Evidence lifecycle: pending, admissible, inconclusive, challenged, stale, rejected, retired.

Distinguish:

- node definition — what work/gate exists;
- execution instance / iteration — a semantic rework cycle;
- attempt — retry of the same work after an execution/infrastructure failure;
- PlanRevision — changed work contract/topology;
- AuthorityRevision — changed semantic authority.

A design/implement/review loop creates new iteration identity rather than resetting historical completion.

## 8. Deterministic control kernel and event history

Canonical workflow history SHALL be append-only accepted events or an equivalently replayable representation satisfying:

```text
(protocol/system semantic version,
 control schema version,
 reducer/ruleset version,
 accepted PlanRevision,
 genesis/initial state,
 ordered accepted events)
 -> exactly one resulting control state
```

Historical events are not reinterpreted using the newest reducer. Schema/ruleset evolution requires compatible historical execution or explicit reviewable migration.

The reducer performs no nondeterministic I/O during replay. Wall clock, live filesystem, Git state, network, quota, resource availability, model output, human judgment, and other external mutable facts enter only as typed observations/decisions before deterministic reduction.

Derived current state, graph indexes, ready queues, flowchart views, snapshots, and caches are rebuildable. Canonical history wins if a derived projection disagrees.

## 9. Control persistence

The default canonical control store is a small transactional private/local store outside target repositories; SQLite is the initial preferred concretization unless deployment requirements justify more.

Canonical/private state includes:

- accepted event history;
- accepted control revisions;
- runtime node/gate state;
- obligations;
- leases/serialization;
- transaction metadata;
- scheduler/resource observations where required;
- candidate graph overlay metadata;
- migration/reconciliation state not itself semantic project authority.

Repositories retain semantic artifacts, WorkGraph definitions, authority graph definitions/node documents, D4 code, evidence artifacts, and bounded transport files where needed.

The architecture SHALL define atomic accepted-event publication, integrity checking, backup/export/restore, version compatibility, project identity mapping, and crash recovery. Loss of derived indexes may be rebuilt; loss of canonical accepted history may not be silently reconstructed from prose.

## 10. Scheduler boundary

The reducer/obligation engine owns legal workflow state, dependency/impact propagation, readiness/blocking, and next obligations.

The Scheduler owns only execution feasibility and route selection among already-ready work, including:

- resource/account/model availability;
- capability compatibility;
- cost/quota/resource metering;
- route selection;
- reservation.

The Scheduler cannot decide semantic completion or become a second reducer. Historical scheduling decisions are recorded and replayed as facts, not recomputed from current resources.

## 11. Work domains and conflict-free parallelism

Graph independence alone is insufficient to prove safe concurrent mutation. Each mutating work node SHALL declare a structured **WorkClaim** / read-write footprint over relevant domains.

Candidate claim classes include:

- semantic authority subjects;
- repository paths;
- D4 symbols/modules;
- schema/contracts;
- integration surfaces;
- resources/accounts/hardware;
- shared configuration/build files;
- authority owners.

Access modes include `READ`, `WRITE`, and `EXCLUSIVE`.

Parallel issuance requires:

```text
ready(A) AND ready(B)
AND graph dependencies permit concurrency
AND declared claims are compatible
AND required resources permit concurrency
```

Expected and actual write/read sets are compared at result time. Undeclared mutation triggers reconciliation rather than automatic acceptance.

## 12. Git isolation and integration

Every mutating execution instance receives:

- immutable repository base commit;
- isolated branch/worktree or equivalent workspace;
- immutable TaskEnvelope;
- declared WorkClaims;
- candidate identity;
- expected integration target.

Agents never concurrently mutate one shared working tree.

Git is the transaction/isolation and source-history substrate, not the owner of SSDS workflow semantics.

A clean textual merge is not proof of semantic orthogonality. An explicit **Integration Gate** validates:

1. predecessor/output bindings;
2. PlanRevision and AuthorityEpoch applicability;
3. declared versus actual write surface;
4. Git textual overlap;
5. semantic WorkClaim overlap;
6. candidate/current-base reconciliation;
7. integration candidate;
8. affected regression/evidence;
9. accepted integration event.

Unexpected conflict produces explicit reconciliation work rather than ad-hoc manual editing.

## 13. Context Resolver: graph-native retrieval

RAG is not a separate authority subsystem. Retrieval is primarily deterministic traversal over existing graph relationships.

A version-bound Context Resolver answers queries from:

- WorkGraph;
- AuthorityGraph;
- CodeGraph;
- EvidenceGraph;
- repository indexes;
- accepted project memory/history only when its activation predicate applies.

A `ContextBundle` binds at least:

- task;
- PlanRevision;
- AuthorityEpoch;
- repository revision;
- graph/schema/analyzer/retrieval-policy versions;
- query/purpose/anchors;
- selected objects;
- traversal paths;
- inclusion reasons;
- unresolved/missing/ambiguous relationships;
- bounded expansion options.

Retrieval policy is operation-specific. Implementation, Review, impact analysis, Serious Challenge investigation, migration, and reconciliation may traverse different relation classes and directions.

Graph traversal owns deterministic relevance. Full-text/vector/semantic search is secondary discovery machinery used when graph relationships are incomplete. Search results may propose candidate relationships but cannot self-authorize graph edges.

## 14. Agent-facing semantic projection and MCP/harness APIs

The agent-facing interface SHALL minimize cognitive burden.

Internal machine representation may contain normalized graph rows, event IDs, revisions, digests, SCCs, closures, transaction records, and low-level diffs. The normal agent interface does not require reading them.

A deterministic **Semantic Projection Layer** converts machine state into decision-oriented responses:

1. what fact is relevant;
2. why it is relevant;
3. what accepted authority/source establishes it;
4. what remains unresolved;
5. what actions are currently legal.

Normal agent API/MCP surfaces should be intention-oriented, for example:

- `task.open`
- `context.for_task`
- `context.for_issue`
- `context.expand`
- `authority.explain`
- `authority.what_governs`
- `authority.what_depends_on`
- `code.explain_symbol`
- `code.affected_by_change`
- `work.why_blocked`
- `work.explain_next_step`
- `change.preview_impact`
- `change.propose`
- `change.reconcile`
- `finding.report`
- `challenge.raise`
- `result.submit`

Raw graph traversal/event/transaction APIs remain expert/debug/qualification surfaces.

The projection layer itself should be template/schema driven where possible; routine context presentation must not require another LLM merely to translate deterministic state.

## 15. TaskEnvelope / ResultEnvelope

All local/web/agent harnesses use one logical task/result contract.

TaskEnvelope binds immutable:

- task/run/iteration/attempt identity;
- system/protocol/control schema versions;
- PlanRevision;
- base control revision;
- AuthorityEpoch and concrete prerequisite revisions;
- repository base/branch/workspace identity;
- requested action/capability;
- WorkClaims;
- required evidence/checks;
- applicable human gates;
- ContextManifest/initial context identity;
- allowed ResultEnvelope classifications.

ResultEnvelope binds the exact task and carries bounded structured assessment, findings, proposed actions, produced candidates/evidence, actual write-set/diff identity, blockers, human-gate request, and execution provenance.

Agent PASS remains recommendation. Canonical closure is a reducer decision only after all applicable authority, evidence, blocker, Serious Challenge, human-gate, staleness, and impact-closure requirements are satisfied.

## 16. Graph-aware write side: GraphTransaction

The write-side counterpart to Context Resolver is a **GraphTransaction**.

Every canonical mutation begins against immutable:

- PlanRevision;
- AuthorityEpoch;
- repository base;
- graph/control snapshot;
- task/claims.

The candidate transaction may modify:

- repository files;
- authority node content;
- proposed semantic relationships;
- WorkGraph plan candidates;
- evidence bindings;
- derived D4 graph state.

The transaction maintains a candidate graph overlay and `GraphDelta` recording nodes/edges added, modified, retired, invalidated, redirected, and affected reverse closures.

Derived relations are recomputed from their real owners. Semantic relations are proposed and reviewed where judgment is required.

A candidate cannot advance canonical repository/authority/control state while any required graph segment is stale, dirty, ambiguous, or inconsistent.

## 17. Direct-write compatibility and dirty reconciliation

MCP-mediated writes are preferred but SSDS SHALL NOT require every formatter/compiler/code generator/editor write to pass through a virtual filesystem.

Direct writes are permitted only in isolated candidate workspaces. Any out-of-band mutation marks affected graph projections `DIRTY`.

Before graph-sensitive use or finalization:

```text
Git/tree diff
 -> changed-path classification
 -> incremental analyzers
 -> candidate graph refresh/invalidation
 -> semantic ambiguity detection
 -> reconciliation if required
```

A dirty candidate may never be canonically integrated.

## 18. Incremental graph maintenance

Minor edits SHALL NOT require full repository graph rebuild.

Graph maintenance uses locality and reverse invalidation:

```text
changed owner/unit
 -> recompute local node/edges
 -> did outward interface/dependency fingerprint change?
      no -> stop
      yes -> invalidate/recompute affected reverse closure
```

AuthorityGraph updates are local explicit relation changes plus affected closure. CodeGraph updates reparse/reanalyze changed D4 units and propagate only where dependency signatures require it.

Full rebuild remains an integrity/qualification/recovery option and SHALL produce an equivalent graph under the same source/analyzer basis.

## 19. Graph history and structural diffs

Accepted graph revisions are immutable and history-addressable. Each accepted transition records enough identity to answer:

- what nodes/edges changed;
- what relationship was introduced/removed/redirected;
- what authority/repository revision caused it;
- which downstream subjects became affected/stale;
- why a current dependency exists;
- which historical qualification/evidence was executed against which graph revision.

`git diff` describes source/textual change; graph diff describes structural relationship change. The two are linked by GraphTransaction but neither replaces the other.

## 20. Repository explainability and reconciliation

Every materially active repository artifact SHALL be either:

- represented by the applicable graph system;
- explicitly classified as intentionally external/non-governing;
- quarantined/reconciliation-pending.

`UNKNOWN_BUT_ACTIVE` is invalid.

Unexpected state includes manual edits, untracked files, external commits, collaborator/foreign-agent work, build products, generated binaries, moved/deleted files, unknown documents, and partial failed effects.

At control boundaries the system mechanically detects repository drift and performs bounded intake:

```text
detect
 -> preserve exact identity
 -> classify
 -> reconstruct mechanical relationships
 -> map to current graph
 -> auto-reconcile if fully deterministic
 -> otherwise create semantic reconciliation work
```

Unresolved drift cannot silently enter authority, normal agent context, evidence applicability, or integration.

## 21. Artifact intake and trust

Initial classification may include:

- source code;
- authority candidate;
- documentation;
- test/configuration;
- generated output;
- build artifact;
- evidence candidate;
- run output;
- cache/temporary;
- binary opaque;
- external input;
- unknown.

Classification uses path, content type, Git history, known producers, build manifests, graph bindings, language parsers, provenance, and bounded metadata before semantic escalation.

Unknown or untrusted executable/binary content is never executed merely to classify it. Static inspection and provenance precede loading/execution. Potentially active content is treated as a trust boundary.

Reconciliation dispositions include:

- `ABSORB`
- `RECONCILE`
- `SPLIT`
- `ARCHIVE`
- `RETAIN_AS_EVIDENCE`
- `MARK_GENERATED`
- `QUARANTINE`
- `REJECT`
- `DISPOSABLE`

`DISPOSABLE` is a classified disposition, not automatic deletion authority.

## 22. Project Ingestion and Reconciliation Engine

The recovery path is generalized into a first-class **Project Ingestion and Reconciliation Engine** with operating modes:

- native drift reconciliation;
- external changeset/branch import;
- legacy SSDP/SSDS migration;
- unstructured scientific repository bootstrap.

It owns deterministic repository census, artifact classification, structural dependency extraction, candidate graph reconstruction, coverage accounting, semantic escalation generation, migration WorkGraph generation, and genesis/cutover preparation.

Recovery of one unexpected file and migration of a complete legacy repository use the same underlying architecture at different scales.

## 23. Discovery direction versus authority direction

For an unstructured legacy repository, semantic discovery may proceed bottom-up:

```text
D4 behavior
 -> candidate D3 architecture
 -> candidate D2 numerical method
 -> candidate D1 formulation
```

But accepted authority is established top-down:

```text
candidate D1 -> Review/accept
accepted D1 -> candidate D2 fidelity -> accept
accepted D2 -> candidate D3 fidelity -> accept
accepted D3 -> D4 reconciliation/verification
```

D4 code may provide evidence for reconstructing missing upstream intent but can never automatically manufacture accepted D3/D2/D1 authority.

## 24. Progressive migration and LegacyAggregate digestion

Repository migration is progressive and may coexist with ongoing production work.

An unresolved legacy region is represented by an exact-scope **LegacyAggregate** supernode. It does not claim the enclosed material is one semantic authority; it states that a bounded set of material exists whose internal semantic structure is unresolved.

Initial migration may contain one aggregate covering the entire project. Refinement progressively replaces an aggregate by:

- resolved native authority/code/evidence nodes;
- smaller residual LegacyAggregates;
- precise or still-coarse boundary relations.

Refinement obeys scope conservation:

```text
Scope(parent LegacyAggregate)
 =
 union(Scope(resolved children), Scope(residual aggregates))
```

with disjointness or explicitly declared shared representation.

Aggregates may first be structurally partitioned into smaller opaque aggregates before semantic reconstruction. This enables parallel migration.

Known cross-boundary relationships may point to/from an aggregate with explicit unresolved/coarse edge semantics. As the aggregate is digested, coarse edges are retired or redirected to precise native endpoints.

Superseded aggregate revisions remain in history through `REFINED_INTO` provenance.

Project-wide migration closes only when no materially active legacy residual remains; percentage-complete alone is not a closure criterion.

## 25. Partial migration and live production

During migration:

- native and legacy scopes may coexist;
- the same semantic scope never has two simultaneously current authorities;
- every legacy aggregate binds an exact repository/authority basis;
- CodeGraph coverage may be much more complete than upstream semantic migration;
- production D4 code remains executable unless a separate governed change says otherwise;
- migration is representation/dependency reconstruction by default and SHALL NOT silently alter scientific/numerical/runtime behavior;
- production edits that intersect a migration task invalidate/reconcile only the affected migration subgraph;
- independent production edits leave unrelated migration work applicable;
- cross-frontier changes create explicit reconciliation obligations.

Scope-local cutover is atomic:

```text
legacy-current scope
 -> candidate native representation
 -> migration-equivalence Review
 -> native-current scope
 -> legacy representation historical
```

Large-project adoption therefore uses an initial migration genesis followed by scope-local native cutovers, not one all-or-nothing project conversion.

## 26. Migration coverage and uncertainty

Migration tracks material coverage structurally, not merely by percentage.

The system must be able to answer:

- which D1/D2/D3 subgraphs are native, candidate, ambiguous, or legacy;
- which D4 nodes are structurally indexed and which have upstream authority mappings;
- which evidence is mapped/current/stale/unclassified;
- which active artifacts remain unresolved;
- which boundary dependencies remain coarse;
- which semantic reconstruction questions block cutover.

Legacy reconstruction may legitimately retain explicit `PROVISIONAL`, `REVIEW_REQUIRED`, or `UNKNOWN` status when historical intent cannot be recovered. Migration success requires visible uncertainty, not invented certainty.

## 27. Minimum-semantic-burden invariant

The orchestrator SHALL resolve mechanically decidable identity, dependency, relevance, state, impact, provenance, concurrency, and consistency questions before presenting work to an agent.

Agent interfaces SHALL expose the smallest decision-sufficient semantic representation of the unresolved issue and SHALL NOT require routine interpretation of canonical graph storage, event logs, transaction records, or other machine-control representation.

When machinery cannot decide, it should present a focused semantic question with the relevant distinctions and evidence already resolved rather than requiring repository archaeology by the agent.

## 28. External effects and crash safety

Agent launch, branch creation/push, tool invocation, reservation, and external file publication are effects outside reducer replay.

The architecture SHALL persist deterministic effect intent with stable idempotency identity before effect eligibility, perform the effect through a reconcilable adapter, record observed outcome as a new event, and reconcile ambiguous crash state before retry.

No effect is complete merely because the reducer intended it.

## 29. Plan repair and graph repair

Reviewers/agents propose structured `PlanPatch` / graph-repair operations rather than directly mutating canonical runtime state.

Candidate operations include:

- add/split/replace/obsolete node;
- add/remove/redirect dependency;
- change claims;
- change gate condition;
- change acceptance requirement;
- map/unmap authority/code/evidence relation;
- refine LegacyAggregate;
- propose semantic dependency/concretization.

The flow is:

```text
finding
 -> candidate patch
 -> schema/graph validation
 -> impact analysis
 -> owning semantic Review/human gate if required
 -> accepted new plan/authority revision
 -> deterministic invalidation/re-obligation
```

Running tasks remain bound to their original PlanRevision/AuthorityEpoch. New revisions never retroactively pretend an old agent saw new requirements.

## 30. Mandatory orchestrator semantics and fallback

After SSDS 8 native cutover for a governed scope, only the canonical reducer may advance SSDS workflow state for that scope.

Manual/foreign work can still occur, but it enters through reconciliation/import rather than silently becoming canonical.

Failure of the orchestrator/control store produces truthful non-closure for native SSDS workflow. It does not reactivate document editing as a hidden second workflow authority.

Legacy scopes under an explicit migration envelope may continue under their bound legacy process until scope-local cutover.

## 31. Architecture component model

The target logical structure is:

```text
                         Agent / Human
                              |
                     MCP / Harness API
                              |
                 Semantic Projection Layer
                    /                    \
            Context Resolver       Graph Transaction
                    \                    /
                     Graph/Query Services
             Authority / Work / Code / Evidence
                              |
                       CONTROL KERNEL
       event reducer / obligation engine / dependency engine /
       claim-conflict engine / gate validator / impact engine
                   /                         \
          Git/Repo Coordinator             Scheduler
                   \                         /
                      Agent Gateway
```

The Project Ingestion and Reconciliation Engine enters through the same graph/query and transaction services rather than maintaining a second migration control plane.

Current Tracker-like functionality becomes a derived read projection of canonical event/state history where retained.

## 32. Initial implementation bias

Unless D3 Review finds a material counterconstraint:

- use SQLite for private transactional control/event state;
- use repository-owned structured text for accepted WorkGraph and D1-D3 AuthorityGraph definitions;
- use human-readable Markdown (or equivalent) for modular semantic node content;
- use language/build-native analyzers for derived CodeGraph data;
- use Git branches/worktrees for isolated mutation candidates;
- use polling-first remote Git transport before webhook/broker infrastructure;
- expose typed internal services first, then wrap them through MCP/harness-specific adapters;
- avoid a dedicated graph database until demonstrated scale/query requirements justify it.

These are preferred initial concretizations, not immutable product doctrine unless accepted by later D3 architecture.

## 33. Explicit non-goals

SSDS 8.0 SHALL NOT:

- convert all scientific reasoning or evidence into machine JSON;
- encode scientific truth in reducer transition tables;
- require a universal graph database;
- infer independence from absent edges outside declared complete scope;
- let agents directly mutate canonical event/control state;
- let generated CodeGraph edges override actual source;
- let D4 behavior automatically create accepted D1-D3 authority;
- treat Git branch/commit/PR state as workflow semantics;
- require every filesystem write to pass through MCP;
- rebuild the full graph after every minor edit when bounded incremental maintenance suffices;
- expose raw machine graph/control representation as the routine agent UX;
- use semantic/vector search as the primary authority resolver where exact graph traversal exists;
- run/deserialize unknown artifacts merely to classify them;
- force all-at-once migration of legacy projects;
- stop otherwise valid production D4 solely because upper semantic migration is incomplete;
- allow legacy and native representations to be simultaneously current for the same semantic claim;
- use migration as a hidden refactor/redesign channel;
- preserve old document-driven workflow as a dual-current native SSDS fallback after cutover.

## 34. D3 closure obligations before D4

Independent D3 reassessment SHALL explicitly close at least:

1. canonical ownership and persistence of AuthorityGraph, WorkGraph, control events/state, CodeGraph cache, EvidenceGraph metadata, claims, leases, graph revisions, migration aggregates, and transaction overlays;
2. accepted PlanRevision construction/review/freeze semantics;
3. AuthorityEpoch and freeze-frontier semantics;
4. D1-D3 node/edge authority representation and layer-direction rules;
5. legitimate simultaneous-definition/SCC treatment;
6. WorkGraph node/gate/conditional-edge/loop/iteration/attempt type system;
7. semantic graph versus execution graph distinction;
8. WorkClaim/read-write-set compatibility and concurrency rules;
9. isolated Git candidate and Integration Gate policy;
10. conflict/reconciliation workflow;
11. PlanPatch / graph repair / stale-task applicability semantics;
12. deterministic Context Resolver and retrieval-policy contract;
13. ContextBundle provenance/staleness behavior;
14. Semantic Projection Layer and minimum-semantic-burden interface;
15. MCP/harness read/query/proposal/write boundaries;
16. GraphTransaction, candidate overlay, GraphDelta, and dirty-direct-write reconciliation;
17. incremental rebuild/invalidation and full-rebuild equivalence;
18. graph history/diff identity;
19. Repository Explainability invariant and drift detection;
20. artifact trust/classification/quarantine/disposition semantics;
21. Project Ingestion and Reconciliation Engine;
22. bottom-up discovery versus top-down authority reconstruction;
23. LegacyAggregate refinement/scope-conservation/cross-boundary-edge semantics;
24. partial migration/live-production/scope-local cutover;
25. migration coverage/uncertainty/legacy-envelope semantics;
26. reducer/Scheduler/repository coordinator/agent gateway ownership split;
27. event/schema/ruleset migration and deterministic replay;
28. canonical store durability/recovery/export/restore;
29. external-effect intent/reconciliation;
30. human decision ingestion and Serious Challenge preservation;
31. final SSDP 7 inheritance reconciliation and pre-cutover rollback baseline;
32. minimum justified architecture reassessment against the then-current accepted baseline.

No D4 implementation starts merely because this workplan exists.

## 35. Qualification program

The eventual implementation qualification SHALL include, at minimum:

### Determinism and replay
- identical state from identical accepted event history;
- ruleset/schema evolution fixture;
- wall-clock/live-resource independence during replay;
- snapshot/index corruption detection and rebuild;
- compatible export/restore.

### Planning and authority
- unreviewed WorkGraph cannot issue work;
- PlanRevision mutation invalidates only materially affected tasks;
- downstream task binds exact accepted upstream revisions;
- upstream candidate cannot serve as accepted prerequisite;
- forbidden lower-to-higher authority dependency is rejected;
- explicit simultaneous definitions survive SCC condensation while accidental cycles fail.

### Parallelism and Git
- independent claims execute concurrently;
- overlapping semantic/file claims do not;
- undeclared write overstep creates reconciliation;
- clean Git merge with semantic conflict is blocked;
- textual conflict becomes explicit reconciliation work;
- stale candidate/base divergence is detected.

### Context and agent burden
- deterministic context query returns identical ContextBundle for same versioned basis;
- inclusion reason/path is explainable;
- missing relationship returns explicit incomplete/ambiguous state;
- agent receives compact semantic projection rather than raw graph;
- graph search fallback cannot self-promote candidate edges;
- context becomes stale after relevant candidate mutation.

### Graph writes
- MCP-mediated change updates candidate overlay incrementally;
- direct isolated edit marks affected graph dirty;
- dirty candidate cannot integrate;
- local incremental update equals full rebuild for affected graph semantics;
- graph history/diff traces exact accepted mutation.

### Recovery/import
- manual edit detected;
- untracked generated file mechanically classified;
- opaque binary quarantined without execution;
- external branch imported through reconciliation;
- monolithic authority-like document escalated for semantic disposition;
- unknown active artifact cannot enter normal authoritative context.

### Migration
- entire legacy project may begin as one LegacyAggregate;
- aggregate refinement conserves exact covered scope;
- structural split into sub-aggregates requires no false semantic claims;
- coarse boundary edges are safely redirected after semantic refinement;
- partial migration permits production D4 execution;
- production edit invalidates only intersecting migration work;
- native and legacy scopes coexist without dual-current ownership;
- bottom-up reconstruction never self-accepts upstream authority;
- final residual aggregate disappearance closes material migration coverage.

### Failure and security
- crash before/after external effect reconciliation;
- malformed/unknown schema;
- duplicate/stale ResultEnvelope;
- unavailable network/Git/harness;
- unknown executable artifact cannot gain execution authority;
- private control state/secrets do not leak to repository transport.

## 36. Development sequence

The recommended sequence is:

- **Phase A — inheritance and reconsolidation.** After Protocol 7 closes, bind the exact accepted Protocol 7 recovery/candidate inputs, re-evaluate inherited guarantees, and update this workplan without silently adopting a new governing version.
- **Phase B — independent D3 architecture review.** Produce/Review the native SSDS 8 Architecture Manual covering all §34 obligations. D4 remains blocked until PASS and required stakeholder acceptance.
- **Phase C — schemas and deterministic kernel.** Implement versioned identities, events, reducer, persistence/recovery, WorkGraph/AuthorityGraph schemas, obligations, and graph query primitives.
- **Phase D — repository/code integration.** Implement CodeGraph providers, WorkClaims, Git isolation, Integration Gate, GraphTransaction, GraphDelta, incremental invalidation, and repository drift detection.
- **Phase E — interaction layer.** Implement Semantic Projection, Context Resolver, Task/Result envelopes, MCP/harness APIs, and debug/raw inspection surfaces.
- **Phase F — ingestion/migration.** Implement reconciliation/import modes, LegacyAggregate refinement, migration WorkGraph, coverage accounting, and scope-local cutover.
- **Phase G — shadow operation.** Run SSDS 8 machinery as non-authoritative shadow beside the accepted legacy baseline; explain every material difference in routing, dependency, evidence impact, readiness, and closure.
- **Phase H — migration pilot.** Migrate a bounded real legacy/SSDP project or self-hosting repository slice, preserving production D4 operation.
- **Phase I — adversarial/fault qualification.** Execute §35 and accepted D3 qualification.
- **Phase J — native cutover.** Only after accepted architecture, implementation evidence, independent Review, human/project ratification where required, and demonstrated rollback. Remove duplicate native workflow-control duties while preserving semantic/historical content.

## 37. Cutover and backward compatibility

SSDP 7.0 remains the latest manual/document-driven fallback baseline until SSDS 8 has independently qualified and explicitly cut over.

Older version-bound work remains governed by its declared version. SSDS 8 migration never reinterprets immutable historical records as though they were authored under the graph-native system.

During project migration, explicit LegacyAggregates/legacy scopes may continue under their original governing workflow until local native cutover. After a scope becomes native, no hidden document-controlled fallback may concurrently govern that same scope.

Rollback is version/state rollback to an immutable accepted pre-cutover baseline, not simultaneous dual authority.

## 38. Acceptance criteria for the architecture cycle

This prospective architecture is ready for D4 handoff only when:

1. final Protocol 7 inheritance is reconciled;
2. one accepted D3 Architecture Manual resolves all §34 obligations;
3. AuthorityGraph, WorkGraph, CodeGraph, EvidenceGraph, event/control state, and migration ownership are unambiguous;
4. exactly one canonical workflow writer exists;
5. planning/work phase separation and frozen PlanRevision semantics are accepted;
6. immutable authority binding/freeze-frontier semantics are accepted;
7. graph-aware read and write consistency is fully specified;
8. safe parallelism/integration/reconciliation is fully specified;
9. Context Resolver + Semantic Projection meet minimum-semantic-burden requirements;
10. repository drift/import/migration has one coherent route back to GraphTransaction;
11. LegacyAggregate progressive migration and live-production coexistence are fully specified;
12. persistence/replay/recovery semantics are accepted;
13. no duplicate graph/control authority or hidden dual-current fallback remains;
14. independent D3 Review/Challenge Pass finds no blocker or active governing Serious Challenge;
15. stakeholder/project acceptance required for this major architectural change is explicit.

## 39. Handoff state

```text
GOVERNING DESIGN PROTOCOL: SSDP 6.6.0
TARGET: SSDS 8.0.0 graph-native deterministic orchestration system
SOURCE SNAPSHOT: f96b7ccf90dede4150d0efa17264fff07ec12d0d
SOURCE LINE: ssdp-7.0-scientific-epistemic-closure
SSDP 7 STATUS: active closure development; major semantics largely complete but final accepted inheritance not yet frozen
THIS WORKPLAN: proposed architecture / not accepted-current
D3: requires fresh independent review after final Protocol 7 reconsolidation
D4: NOT AUTHORIZED
SERIOUS CHALLENGE: none currently recorded
NEXT ACTION:
  preserve this branch while SSDP 7 closes;
  then re-consolidate exact Protocol 7 inheritance and perform independent D3 review before implementation.
```

## 40. Final architectural principle

```text
semantic artifacts carry meaning;
graphs make relationships explicit;
programs resolve mechanical relationships;
agents receive only unresolved semantic work;
humans decide where human authority is required;
the reducer alone serializes canonical workflow state;
Git isolates and integrates candidates;
migration progressively digests opaque legacy material into native graph structure.
```

SSDS 8.0 succeeds only if increased deterministic machinery **reduces**, rather than transfers, complexity to the agent.
