---
kind: protocol-major-revision-workplan-amendment
workplan_id: SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-1-SECOND-REVIEW-CLOSURE
amends_workplan: SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION
protocol_version: 6.1.0
target_protocol_version: 7.0.0
status: proposed
created_date: 2026-09-09
review_round: 2
requires_completed_workplan: SSDP-6.1-EVIDENCE-EVOLUTION-AND-CONCRETIZATION-ALIGNMENT
active_serious_challenge: none
---

# SSDP 7.0 Deterministic Control Plane and Mandatory Orchestrator Migration — Revision 1 Second-Review Closure

## 1. Status and authority

This amendment is a **mandatory current companion** to `SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION.md` once the Protocol 7 workplan becomes active. It closes specification gaps identified by a second Protocol 6 review.

The parent plus this amendment form the complete Protocol 7 design handoff. Where this amendment narrows or corrects parent wording, this amendment governs that ambiguity. All other parent obligations remain binding.

No Serious Challenge was found to the Protocol 7 objective. The identified issues concern ownership separation, replay/version semantics, cutover atomicity, semantic/control binding, and transport persistence.

## 2. Correct Scheduler/control-kernel ownership

The parent section 3 lists as potentially superseded an assumption that Scheduler does not participate in deterministic workflow transition selection. That wording is too broad and risks collapsing **workflow control** into **resource scheduling**.

Protocol 7 SHALL preserve this ownership separation unless an independently reviewed D3 redesign demonstrates a materially superior coherent decomposition without duplicate authority:

```text
workflow reducer / obligation engine
    owns legal workflow-state transitions,
    dependency/impact propagation,
    readiness/blocking,
    and required next obligations

Scheduler
    owns resource/account/model/route feasibility,
    metering/prediction/reservation,
    and selection among execution routes for work
    that the workflow control kernel has already declared ready
```

Scheduler may provide resource facts that cause a ready obligation to become execution-blocked or may reject a route on hard feasibility grounds. It does not decide that a scientific/design/implementation/review stage is semantically complete, invent the next authority mutation, or become a second reducer.

Preserve the existing higher-level invariant that scheduling remains subordinate to workflow intent. Protocol 7 changes the owner of deterministic workflow state from document interpretation to the control kernel; it does not make resource optimization the workflow authority.

The D3 architecture reopen SHALL explicitly place reducer, obligation, graph, scheduling, and agent-execution ownership and verify one-way dependency boundaries among them.

## 3. Semantic authority versus control projection

The parent calls the Protocol 7 graph machine-authoritative for control decisions. Clarify the boundary:

- D1-D4 semantic artifacts and accepted governed external authority remain the owners of substantive meaning;
- the control plane is authoritative for **workflow/control facts** such as accepted identity bindings, lifecycle state, obligation readiness, admissibility classification, and legal transitions;
- graph/state records representing semantic relationships are accepted **projections/bindings of semantic facts**, not an independent source entitled to redefine the underlying scientific/engineering meaning.

Required invariant:

> A control record may bind to and operationalize an accepted semantic fact, but it may not silently replace the semantic owner of that fact.

If a current semantic artifact and its canonical control projection disagree materially, classify this as a **control/semantic integrity defect**. Stop dependent canonical transitions until the disagreement is reconciled at the proper owner. Do not automatically prefer JSON because it is machine-readable, and do not automatically overwrite JSON from prose without a validated transition.

Every accepted semantic-classification fact used for deterministic propagation must carry sufficient provenance to identify:

- the semantic subject/revision;
- the owning domain/authority;
- the assessment/decision that established the classification;
- required independent/human ratification state where applicable.

The orchestrator validates authorization and transition legality; it does not manufacture semantic acceptance.

## 4. Canonical control-store boundary and repository containment

Protocol 7 SHALL distinguish **canonical control persistence** from **transport artifacts**.

Default architectural requirement, preserving the existing private-state boundary:

- canonical event history, current control state, leases, scheduler/account telemetry, and private coordination data live in the orchestrator's governed user-local/private state root outside target/project repositories;
- project repositories contain semantic artifacts and only bounded transport/control artifacts when required for a transport such as web-agent Git handoff;
- secrets and private account/resource telemetry never enter project/run branches merely because TaskEnvelope/ResultEnvelope uses Git transport.

A project MAY deliberately persist selected non-secret control state in-repository only if a later D3 authority explicitly adopts that storage/trust model and resolves concurrency, privacy, history, and ownership consequences. It is not the default.

This separation prevents the lightweight control plane from becoming a large committed project data stream.

## 5. Task/Result transport artifacts are not semantic repository content

For Git/web execution, TaskEnvelope and ResultEnvelope files on an isolated run branch are **transport records**.

They SHALL NOT be merged automatically into the project's canonical semantic branch merely because the agent's implementation commit is accepted.

Normal acceptance flow should conceptually separate:

```text
run branch
  -> validate Task/Result binding and candidate lineage
  -> ingest accepted ResultEnvelope/control facts into canonical control store
  -> integrate only the intended semantic/product commits/artifacts
  -> retire/delete/archive the transport branch according to policy
```

Preserve a durable control/audit reference to the accepted remote commit/result as required, but do not pollute project history with every ephemeral TaskEnvelope unless project policy explicitly chooses that representation.

Agents SHALL NOT modify the issued TaskEnvelope. They also SHALL NOT gain authority to modify canonical schemas, reducer policy, event history, or control rules merely because those files are visible in a repository checkout. Such changes require their own explicitly authorized Protocol task.

Result validation must detect unauthorized modification of protected task/control surfaces.

## 6. Candidate identity and non-self-referential ResultEnvelope publication

A ResultEnvelope committed together with its own result file cannot safely require its own enclosing Git commit SHA as a pre-existing field without creating a self-reference problem.

Protocol 7 SHALL define candidate/result identity so publication is realizable. Acceptable patterns include, depending on D3 design:

- ResultEnvelope binds to the task/base state and identifies the **semantic candidate parent commit**, while the enclosing later commit adds only the result/transport record;
- ResultEnvelope is stored outside the semantic candidate commit and the orchestrator records the publication commit after ingestion;
- another equivalent two-phase identity model with explicit semantics.

Do not require a file to contain the hash of the commit that cannot exist until after that file is committed.

This follows the existing Protocol distinction between a semantic candidate and later evidence/lifecycle-only commits.

## 7. Version-bound replay semantics

The parent's deterministic replay equation is incomplete unless the reducer/action/schema semantics used to interpret historical events are themselves version-bound.

Required stronger invariant:

```text
(protocol semantic version,
 control-schema version,
 transition/reducer ruleset version,
 initial/genesis state,
 ordered accepted events)
 -> exactly one resulting control state
```

Historical accepted events SHALL NOT be silently reinterpreted through whatever reducer happens to be latest.

When reducer/schema/control semantics evolve:

- preserve compatibility with the historical ruleset where practical; or
- perform an explicit, reviewable migration producing a new versioned genesis/snapshot/event lineage while preserving the old immutable history; or
- use another deterministic migration mechanism with equivalent auditability.

Migration must distinguish mechanical schema evolution from semantic reinterpretation. A migration cannot silently turn an old ambiguous/blocked result into a new PASS.

Derived snapshots may accelerate replay, but their provenance must identify the exact event/ruleset boundary they summarize and they remain rebuildable/verifiable against canonical history.

Add qualification demonstrating replay stability across at least one schema/ruleset evolution or a controlled compatibility fixture.

## 8. Cutover quiescence and in-flight Protocol 6.1 work

The parent forbids dual-current control but does not fully specify what happens to work already in progress at cutover.

Before Protocol 7 canonical cutover, every active Protocol 6.1 task/workplan/run within the migration scope SHALL be placed in exactly one category:

1. **drained under 6.1** — finish/close under its pinned 6.1 authority before cutover;
2. **remain pinned to 6.1** — intentionally continue only in an isolated 6.1 release/workspace with no Protocol 7 authority over the same run;
3. **explicitly migrate to 7.0** — reconcile the governing semantic snapshot, outstanding obligations, evidence validity, Serious Challenges/human gates, and current candidate; then create a Protocol 7 genesis/import event or equivalent typed migration record.

Never infer a Protocol 7 canonical state merely by scraping `status:` text or `workplans/active` placement from an in-flight 6.1 artifact.

A migrated task's old document lifecycle fields become historical/provenance input. The Protocol 7 reducer owns the newly established current control state after the explicit migration boundary.

Cutover acceptance SHALL include an inventory proving that no in-scope run is simultaneously live under both authorities.

## 9. Workplan/frontmatter lifecycle migration

Protocol 7 workplans remain semantic plans, but existing templates/frontmatter currently contain lifecycle fields such as `status` and filesystem placement such as `workplans/active`.

At cutover the protocol SHALL choose one coherent compatibility strategy:

- remove canonical lifecycle fields from new Protocol 7 semantic workplans; or
- retain them only as **derived/advisory human-readable projections** generated from the control state and clearly non-authoritative.

Do not permit manually edited `status: completed` or directory movement to enact a Protocol 7 transition.

Historical 6.1 and older workplans remain immutable under their original lifecycle semantics. Do not rewrite their metadata to look like Protocol 7.

Any generated current-state annotation must be reproducible from the control plane and cannot become a second independent writer.

## 10. Human decisions use the same single-writer boundary

The parent correctly prevents agents from self-ratifying human gates. Extend the single-writer rule to all external actors:

- agent output is a proposal/assessment/evidence input;
- human input is an authenticated decision/ratification/override input;
- system/tool observations are typed observations;
- only the reducer commits the resulting canonical transition/event.

A human may have semantic authority to decide a claim, but the machine workflow state representing that decision is still committed through the canonical reducer so event ordering, provenance, replay, and dependency propagation remain coherent.

This does not subordinate human scientific authority to the orchestrator; it separates **who is authorized to decide meaning** from **who serializes workflow state**.

## 11. Bootstrap discoverability for web/manual agents

The minimized activation prompt is valid only if the agent can deterministically locate the immutable TaskEnvelope.

Given the activation information, a competent compatible agent must be able to resolve without guessing:

- repository identity/remote when not already fixed by harness context;
- run branch/ref;
- task path or standardized run-ID-to-task-path convention;
- governing Protocol/control version source;
- required skill/capability resolution route.

If `Execute SSDP run <run-id>` is sufficient because repository/ref/path are already bound by the environment, keep it that small. If not, the bootstrap must include the minimum missing locator information. Do not re-expand it with task semantics that belong in the TaskEnvelope.

Add a web-transport qualification scenario where no prior conversational context exists beyond the defined bootstrap contract.

## 12. Manual agent work remains possible, but not manual canonical control

Protocol 7 removes **independently complete manual document control**, not the ability for a human to invoke or supervise an agent manually.

A manually activated web/local agent may:

- read the TaskEnvelope and semantic artifacts;
- perform authorized reasoning/implementation/review;
- write the ResultEnvelope and semantic changes;
- request human intervention.

Without successful orchestrator ingestion/reduction, however, that work has not advanced canonical Protocol 7 workflow state.

Likewise exploratory/report-only scientific or engineering work may occur while the orchestrator is unavailable, but it cannot claim Protocol 7 canonical lifecycle completion until represented and accepted through the control plane.

## 13. Graph completeness must be scoped to deterministic decisions

Protocol 7 does not require formalizing every semantic relationship in the repository.

The machine graph must be complete enough for the deterministic control claims it actually makes. If the orchestrator cannot establish the material dependency closure for a requested transition because required semantic relationships are absent/ambiguous, it SHALL create a review/discovery obligation or block rather than assuming no dependency exists.

Therefore:

> absence of an edge is not automatically evidence of independence unless the governing schema/authority explicitly guarantees graph completeness for that relation/scope.

This prevents a partial graph from producing false non-invalidation.

Graph-completeness declarations themselves must be scoped/versioned and evidence-backed where they are used to justify automatic closure.

## 14. Control-schema forward compatibility

Preserve the existing orchestrator principle that public records tolerate additive optional fields while unsupported required semantics fail explicitly.

For Protocol 7 control records:

- unknown optional non-transition-critical fields may be preserved/ignored according to the declared schema compatibility contract;
- an unknown action, required state, transition-critical edge type, or mandatory field is not silently dropped;
- unsupported required semantics produce a structured incompatible/blocked result;
- action/state vocabularies may evolve through explicit versioning rather than pretending one enum is permanently complete.

This is required for deterministic behavior across independently upgraded agents/orchestrator components.

## 15. Additional D3 design obligations

The Protocol 7 D3 architecture redesign SHALL explicitly decide and document:

1. canonical ownership and persistence location of reducer, event history, derived state, graph/index, obligations, leases, scheduler state, and transport metadata;
2. the reducer/Scheduler/Adapter/Core/Tracker responsibility split and dependency direction;
3. canonical versus derived versus transport-only data classifications;
4. semantic-owner/control-projection consistency handling;
5. event/reducer/schema versioning and migration/replay semantics;
6. in-flight 6.1 cutover/migration behavior;
7. protected control surfaces agents may read but not mutate;
8. semantic-candidate versus result-publication commit identity;
9. run-branch retirement/integration policy;
10. graph completeness/unknown-dependency behavior;
11. authenticated human-decision ingestion;
12. bootstrap locator contract for zero-context web execution.

Do not defer these as incidental D4 implementation details because they define the control/trust architecture.

## 16. Additional deterministic and adversarial qualification

Add bounded tests/scenarios for at least:

- Scheduler cannot enact semantic workflow transitions and remains subordinate to reducer readiness;
- a semantic artifact/control-projection mismatch blocks rather than allowing JSON to silently redefine semantic authority;
- canonical control/private state does not leak into a project repository by default;
- accepted semantic changes can be integrated without merging ephemeral TaskEnvelope/ResultEnvelope transport files;
- an agent-modified TaskEnvelope/protected control file is rejected;
- ResultEnvelope publication avoids Git self-reference and preserves semantic candidate identity;
- replay remains deterministic under the declared reducer/schema/ruleset version;
- an in-flight 6.1 task is drained, pinned, or explicitly migrated without dual authority;
- manually editing Protocol 7 workplan `status` cannot transition canonical state;
- authenticated human decision enters through the reducer while retaining human semantic authority;
- zero-context web activation can locate the correct immutable task using only the declared bootstrap contract;
- partial graph coverage cannot be interpreted as proven independence;
- unknown required action/state semantics fail explicitly rather than being ignored.

## 17. Additional cutover acceptance criteria

Protocol 7 cannot cut over until, in addition to the parent criteria:

1. reducer and Scheduler ownership are unambiguous and no resource-routing module is a second workflow reducer;
2. semantic authority and machine control projection have an explicit consistency/error rule;
3. canonical control persistence and Git transport persistence are separated, with private state outside target repositories by default;
4. ephemeral run Task/Result artifacts are not automatically merged into semantic project history;
5. candidate/result publication has a non-self-referential identity contract;
6. deterministic replay is bound to explicit reducer/schema/ruleset versions and migration behavior;
7. all in-scope in-flight Protocol 6.1 work has been drained, pinned, or explicitly migrated with no dual-current run;
8. Protocol 7 workplan lifecycle metadata cannot independently transition canonical state;
9. human decisions are serialized through the single canonical reducer without transferring semantic authority to the reducer;
10. web/manual bootstrap is deterministically discoverable without hidden conversation state;
11. graph incompleteness cannot silently suppress required impact invalidation;
12. unsupported transition-critical schema/action semantics fail explicitly;
13. the new D3 Architecture Manual resolves every ownership/storage/versioning/migration item in section 15 of this amendment.

## 18. Second-review disposition

```text
SERIOUS CHALLENGE: NONE
SECOND REVIEW: PASS AFTER THIS AMENDMENT
BLOCKING DESIGN GAPS: CLOSED BY REVISION 1
PROTOCOL 7 IMPLEMENTATION: STILL PROPOSED / BLOCKED ON COMPLETED QUALIFIED 6.1
IMPLEMENTATION AUTHORITY WHEN ACTIVATED: PARENT WORKPLAN + THIS MANDATORY COMPANION
```

This amendment strengthens the deterministic control boundary without moving substantive scientific/engineering meaning into the control plane or weakening the Protocol 6.1 recovery path.