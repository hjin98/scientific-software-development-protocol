---
kind: protocol-stage-f-execution-architecture-amendment
governing_protocol_version: 6.6.0
target_protocol_version: 7.0.0
date: 2026-09-28
status: repaired-pending-fresh-independent-review
semantic_candidate: db94a2dfb7fef480f37227eab5c45256e89901b8
---

# Stage F portable agent/runtime execution architecture amendment

## Decision

Stage F implementation and qualification SHALL be **agent-, vendor-, and environment-agnostic**. A named CLI, model provider, local filesystem path, local Git checkout, operating system, or machine is not part of Protocol 7 qualification semantics.

The qualification architecture is split into:

1. a **portable qualification core** owning frozen subjects/cases/floors, matched-pair scheduling, custody roles, evidence/admissibility semantics and scoring inputs; and
2. **runtime adapters** that translate those semantic capabilities to a local CLI agent, cloud agent, hosted workspace, container/VM, API-backed agent or another environment.

An adapter is replaceable D4 machinery. It may not weaken the qualification contract to fit its host.

## Admission boundary

The **portable qualification core**, not an adapter, owns the semantics of execution-profile identity, capability classes, normalized events, admissibility/failure states, required evidence/scoring closure and profile-scoped PASS. Runtime adapters own only host realization and native translation.

### Execution-profile identity

An execution-profile key binds every exposed/controllable material execution condition: agent/model; provider/runtime and exposed version/build; reasoning configuration; adapter; material workspace/environment realization where exposed; install mechanism; resource/time/turn budgets; capability-manifest digest; containment-policy digest; network/external-write policy; credential/service-account policy; and declared provider-managed unknowns.

A provider-managed unknown is recorded, never guessed, and preclassified before runs as either:

- **arm-neutral stochastic/provider-managed** at the exposed interface, with no arm-selective adapter control and no evidence of arm dependence; or
- **materially uncontrolled/not demonstrably arm-neutral**, which makes the pair inadmissible for claims sensitive to that dimension.

A known provider/model/runtime migration inside a matched pair invalidates the pair.

### Capability, containment and custody

The core owns a versioned semantic capability manifest. Native capabilities map to `ALLOW`, `DENY` or `SANDBOX/MEDIATE` with scope for at least catalog/root activation; workspace read/search/list; workspace mutation including delete/rename/mode/symlink; command/process execution; delegation; issue/evidence-store access; repository/object-store operations crossing the workspace boundary; network/remote-service access; external mutation; and credential/secret/service-account access.

Unrestricted shell/code execution is admissible only when substrate containment still enforces the file/network/credential policy. A denied class may have no unmediated escape route. A prohibited external effect is blocked before the live effect or redirected to qualification-owned isolated state; merely logging a real prohibited live mutation is not containment. Regex-only detection is never sufficient.

For machine qualification, keys/answers remain outside executor-reachable capability and credential scope until output freeze. Role- and time-scoped checker/evaluator access and immutable audit evidence support this denial. The contract's stakeholder human-trial behavioral-access exception remains the only explicit exception and does not generalize to machine executors.

### Trace equivalence

The retained native/equivalent trace covers every externally observable event required by the frozen oracles; private chain-of-thought is not required. The normalized schema has common fields for schema/run/event identity, actor, kind, native-source linkage, status and exposed timing, and includes: `catalog_snapshot`, `root_selection`, `resource_access`, `tool_action`, `delegate_call`/`delegate_return`, `issue_evidence_access`, `mutation`, `network_external_action`, `termination`, `final_result`, and `usage_timing`. Oracle-relevant identities/inputs are complete or losslessly artifact-referenced and are never truncated.

Each adapter emits a raw-to-normalized completeness map. Every native observable capable of affecting a required oracle maps to normalized event id(s); every unmapped event is classified. An unclassified/unmappable oracle-relevant event makes the run inadmissible. Reduced summaries cannot be the sole evidence for a zero-tolerance oracle.

### Required evidence, scoring and failure states

Before runs the core freezes immutable run-bound `required_artifacts`, `required_oracles` and `expected_scoring_items` manifests. Expected scoring items have stable id, measure, criticality, applicable branch and allowed dispositions. Valid assessment requires exactly one disposition for every expected applicable item, no duplicates and no unknown ids; unresolved applicability is explicit `UNRESOLVED`, never omission.

Evidence state is separate from process transport status: `COMPLETE_ADMISSIBLE`, `INADMISSIBLE`, `MISSING_REQUIRED_EVIDENCE`, `MALFORMED_EVIDENCE_OR_ASSESSMENT`, `EXECUTION_ERROR`, or `UNRESOLVED`. Qualification outcome is separately `PASS`, `FAIL`, `UNRESOLVED` or `NOT_EVALUATED`. Only complete admissible evidence enters PASS/FAIL scoring. Missing terminal result, required artifact/oracle/scoring disposition or malformed assessment is non-PASS by construction.

### Provenance and cache identity

Run/evidence identity binds immutable subject commit and package digest; fixture/stub/oracle identities; execution-profile key; core/harness digest; normalized-event-schema version; adapter/normalizer digest; capability-manifest digest; required-artifact/oracle/scoring-manifest digests; replicate and pair order. Assessment reuse additionally binds evaluator identity/model/runtime/reasoning where applicable, evaluator-wrapper version, rubric/key digest and assessment-schema version.

If the host cannot enforce or expose a property required by a claim, that profile is **claim-scoped inadmissible**. This is STOP/BLOCKED for that claim, not permission to substitute a proxy.

## Fair comparison

Protocol arms are compared only within the same execution-profile key. Fresh 6.5/6.6 baselines used by a profile run in that same profile. Hard and zero-tolerance floors are evaluated inside the profile. Results from materially different profiles remain separate strata.

A separately reviewed, predeclared multi-profile analysis may summarize strata, but it cannot rescue an inadmissible profile, average away a hard/zero-tolerance failure in an included profile, or establish equivalence of materially different profiles.

The historical Protocol 6.6 Claude Code/`claude-sonnet-5` runs remain bounded historical evidence. They do not require Protocol 7 Stage F to use Claude. Historical 6.6 measures transport only when their required semantic observables transport: for T1/T7/T8 this includes explicit D4 root activation, equivalent capability restrictions, exact SSDP-resource consumption and the frozen active-byte accounting. If a runtime cannot expose those observables, it is inadmissible for that measure rather than scored by a weaker token/context proxy.

## D4 consequence

The current `qualification/ssdp70/eval/` scripts are evidence tooling, not architecture authority. The next implementation cycle may refactor or replace them with a portable core plus adapters. It must repair the blockers in `STAGE-F-PRE-RUN-QUALIFICATION-INTEGRITY-REVIEW-STOP-BLOCKED-2026-09-28.md`, run focused adapter/core regression, and then perform the required withheld-instance and actual-adapter known-good/known-broken pre-run qualification.

## Non-change

This amendment changes no Protocol 7 semantic candidate bytes, scientific doctrine, fixture content, scoring threshold, comparative target, human-trial floor, custody independence requirement or Stage G/H release semantics.

## Review state

This context authored the amendment and cannot independently accept it. Prior workplan and contract PASS records bind earlier exact bytes. A fresh independent Review must check this amendment against the governing workplan, frozen qualification intent and the Stage F STOP/BLOCKED findings before dependent tooling repair or candidate runs.
