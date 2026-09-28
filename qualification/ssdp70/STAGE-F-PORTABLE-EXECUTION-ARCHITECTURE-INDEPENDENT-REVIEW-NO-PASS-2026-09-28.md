---
kind: independent-stage-f-portable-execution-architecture-review
governing_protocol_version: 6.6.0
target_protocol_version: 7.0.0
review_date: 2026-09-28
reviewed_branch: ssdp-7.0-scientific-epistemic-closure
reviewed_commit: 62aa1bbaa9d2d1dfef1b48cede6bc1500837658f
comparison_commit: 75c58ababcdc4810c4e4b5c1e65c7a48810f5299
semantic_candidate: db94a2dfb7fef480f37227eab5c45256e89901b8
result: NO-PASS
active_serious_challenge: none
d4_tooling_repair_authorized: false
qualification_campaign_authorized: false
---

# Protocol 7.0 Stage F portable execution architecture — fresh independent Review — NO-PASS

## Disposition

**NO-PASS. Do not begin dependent D4 portable-runner repair and do not begin the fresh 6.5/6.6/7.0 qualification campaign from the reviewed architecture bytes.**

The architectural direction is sound: a portable qualification core owning qualification semantics, with replaceable runtime adapters owning host transport, is the correct D3 boundary. The reviewed amendment also correctly rejects Claude Code, a named model/provider, local Git, a local filesystem layout, an operating system, or one machine as Protocol 7 qualification semantics.

This is **not** a Serious Challenge. The architecture is capable of preserving qualification semantics, and the immutable Protocol 7 semantic candidate remains untouched. The NO-PASS is narrower: five material equivalence/admissibility contracts remain underspecified, so a D4 implementer would have to invent qualification policy. That discretion could let two materially different runtimes be called equivalent, let incomplete assessment become green evidence, or let cross-profile pooling conceal a failed stratum.

No candidate, 6.5 baseline, 6.6 baseline, human trial, or Stage F qualification run was executed in this Review. No D4 tooling repair was made.

## Authority reconstructed independently

The reviewed branch head was exactly 62aa1bbaa9d2d1dfef1b48cede6bc1500837658f when this Review began. Its direct parent is exactly 75c58ababcdc4810c4e4b5c1e65c7a48810f5299. The amendment commit changes only the expected workplan/qualification/index surfaces and adds the portability amendment record; it does not change the Protocol 7 semantic candidate.

The cycle is governed by Protocol 6.6.0 as declared by the current workplan and qualification contract, targeting Protocol 7.0.0. PROTOCOL-RELEASE-STATE.yaml still identifies accepted-current Protocol 6.6.0. source/PROTOCOL_VERSION at the reviewed commit is 7.0.0 because Stages B-E assembled the target candidate. The immutable semantic candidate remains db94a2dfb7fef480f37227eab5c45256e89901b8.

The principal reviewed authorities/evidence were:

- workplans/active/SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY-CONSOLIDATED.md
- qualification/ssdp70/PROTOCOL-7.0-EVALUATION-AND-QUALIFICATION-CONTRACT.md
- qualification/ssdp70/STAGE-F-PORTABLE-EXECUTION-ARCHITECTURE-AMENDMENT-2026-09-28.md
- workplans/active/SSDP-6.1-7.0-WORKPLAN-AUTHORITY-INDEX.md
- qualification/ssdp70/STAGE-F-PRE-RUN-QUALIFICATION-INTEGRITY-REVIEW-STOP-BLOCKED-2026-09-28.md
- the accepted Protocol 6.6 qualification contract, Stage A preservation record, final simplification freeze, and live-matrix driver.

## What the amendment gets right

### Correct abstraction boundary

The D3 boundary is correct if read as follows:

- the **portable core** owns semantic identities, frozen cases/floors, matched-pair constraints, required evidence, admissibility/failure semantics, custody roles, scoring obligations, and the meaning of normalized capabilities/events;
- an **adapter** owns only realization: how a host starts the agent, installs an arm, exposes tools, obtains native events, enforces the declared capability policy, and translates native observations into the core-owned semantic schema.

Pair ordering is a core-owned invariant; the mechanism that starts the second arm after the first finishes is D4. Likewise containment semantics are D3; container namespaces, hosted-workspace policies, proxies, ACLs, or VM machinery are D4.

No named CLI, vendor, OS, local path, or local Git operation belongs in the D3 contract.

### Environment-local matched comparisons are correct

Requiring a fresh 6.5 or 6.6 baseline in the same admitted execution profile as its matched Protocol 7 arm is the correct control. The amendment correctly prevents historical Claude observations from being silently reused as a baseline for a different cloud/API/runtime profile.

The historical 6.6 evidence itself supports this interpretation. Its qualification contract explicitly treated reference agent/runtime environments as evidence environments rather than downstream runtime dependencies, and separated generic package validity from vendor adapters.

### Logical 6.6 profile is faithful in principle

Replacing the historical literal prefix and Claude flags with a logical 6.6 execution profile is valid. What must be preserved is the demonstrated capability:

- D4 root is explicitly selected before task work on the T1/T7/T8 burden panel;
- the same 6.6 allow/deny capability meaning applies to both arms;
- delegated-agent capability is unavailable for that panel;
- exact package material is installed for the arm;
- active SSDP material and owner reads are observable under the same semantic accounting;
- both arms share the profile except protocol subject.

The historical spelling Use the software-implementation skill. and the Claude Code flags are one realization, not authority.

There is one honest portability limit: an environment that cannot establish which root was activated, which exact SSDP resources were consumed, or the full active material needed by the frozen byte metric **cannot qualify the T1/T7/T8 burden claim**. It may be usable for another claim whose required observables it can expose. The correct response is claim-scoped INADMISSIBLE, not a weaker token/context proxy.

### F1/F7 and much of F2/F3/F5/F8/F9/F10 now have the right route

The amendment correctly requires immutable subject commit plus package digest, complete deterministic-oracle evidence, non-regex containment, complete raw/equivalent trajectory, full action inputs or equivalent records, explicit missing-evidence inadmissibility, actual-adapter known-good/known-broken probes, and cache identity over subject/profile/adapter/replicate/order.

Those are material improvements over the STOP/BLOCKED state. The remaining blockers below are about making those statements operationally unambiguous.

## Blocking findings

### B1 — execution-profile equality is not defined tightly enough when provider-managed state is hidden

The contract says a provider-managed setting that cannot be fixed is recorded as unknown/provider-managed, and it also says both arms in a matched pair use the same execution profile except protocol arm. That is not yet a complete equivalence rule.

A profile label can be identical while a provider silently changes model snapshot, system prompt, tool semantics, hosted-workspace policy, context injection, region/backend, or another material setting between arms. Merely recording unknown does not establish matched equality. Conversely, requiring observation of every hidden implementation detail would make hosted/API execution impossible and contradict the portability objective.

**Minimal repair:** define a two-level identity.

1. execution_profile_key contains every exposed/controllable material setting and a declared list of provider-managed unknown dimensions.
2. run_identity adds the immutable protocol subject/package and run-specific identities.

For each provider-managed unknown dimension, classify it before runs as either:
- arm-neutral stochastic/provider-managed inside one profile, meaning the adapter has no arm-dependent control over it and pair counterbalancing treats it as uncontrolled run variance; or
- materially uncontrolled/not demonstrably arm-neutral, in which case the pair is INADMISSIBLE for claims sensitive to that dimension.

A known provider/runtime migration inside a matched pair invalidates the pair. Unknown values must never be guessed. This preserves cloud admissibility without pretending hidden state is matched when it is not.

The execution_profile_key should bind at least: agent/model identity; provider/runtime identity and exposed version/build; reasoning configuration; adapter identity; environment/workspace realization where material and exposed; install mechanism; resource/time/turn budgets; capability-manifest digest; isolation/containment policy digest; network/external-write policy; credential/service-account policy; and all declared provider-managed unknowns.

### B2 — semantic capability equivalence and containment/custody still leave material policy to adapters

The current class list is directionally correct but too coarse to decide whether two native toolsets are equivalent. For example, unrestricted Python or shell execution can bypass a nominal file/network denial; a hosted repository tool may mutate remote state without looking like a file write; a service-account credential can expose custody material without an explicit Read event.

The phrase prevent or capture is also unsafe if capture can mean permit a real prohibited side effect and log it afterward. The stronger existing oracle language requires sandboxed stand-ins, but the portable D3 contract should make the invariant explicit rather than rely on composition across sections.

**Minimal repair:** make the core own a versioned capability manifest. Every native operation maps to one or more semantic classes with ALLOW, DENY, or SANDBOX/MEDIATE, plus scope. At minimum cover:

- catalog/skill discovery and explicit root activation;
- workspace read/search/list;
- workspace create/modify/delete/rename/mode/symlink operations;
- process/command execution;
- delegation/subagent launch;
- issue/evidence-store read/search/write;
- repository/version-control or object-store operations that can cross the workspace boundary;
- network/remote-service access;
- external writes/mutations;
- credential/secret/service-account access.

An unrestricted code/process capability is admissible only when substrate containment still enforces the file/network/credential policy. A denied capability may not have an unmediated equivalent escape route.

For prohibited external effects, capture means **blocked before the live effect or redirected to an isolated stand-in/test endpoint whose state is qualification-owned**. Logging a real unauthorized live mutation afterward is not containment.

For machine qualification custody, fixture keys/answers must be outside executor-reachable capability and credential scope until output freeze. Immutable audit logs are supporting evidence, not a substitute for executor non-reachability. The human-trial behavioral-access exception remains the explicit special case already frozen in section 7; it should not silently generalize to machine executors. Pre-run checker and evaluator access remains role-scoped and time-scoped.

### B3 — trace portability lacks a core-owned minimum normalized event schema and completeness proof

Complete native/equivalent raw trajectory + normalized event stream is the right architecture, but sufficient and semantically equivalent are presently adapter judgments. That is too much D4 discretion for zero-tolerance owner-read, unauthorized-mutation, O3, ordering, delegate-gap, and termination oracles.

The contract must not require hidden chain-of-thought. Complete means complete **externally observable execution trajectory needed by the frozen qualification**, not private model reasoning.

**Minimal normalized event contract:** every event has a stable schema version, run id, monotonically ordered sequence/event id, actor id, semantic event kind, native-source reference, status, and timing fields when exposed. Unknown timing/usage remains explicit unknown rather than fabricated. Required event kinds and payloads are:

1. catalog_snapshot — logical skill ids, exact arm/package identity, multiplicity;
2. root_selection — selected logical root, explicit/ordinary selection mechanism, resolved package identity;
3. resource_access — read/search/list operation, complete logical resource identity, full query/action input, result status and result/artifact reference; no truncation on fields used by an oracle;
4. tool_action — semantic capability class(es), native operation identity, complete action input or a lossless artifact reference, start/result/error status, output reference;
5. delegate_call / delegate_return — stable delegate id, parent actor, complete request, returned result/reference, launched-work relation when observable, delegate capability/profile identity where material;
6. issue_evidence_access — store identity, operation, query/object ids, before/after object version for mutation;
7. mutation — create/modify/delete/rename/mode/symlink or equivalent, logical target, workspace/external class, authorization decision, blocked/sandboxed/live disposition, before/after identities where applicable;
8. network_external_action — destination/service identity at the granularity exposed, operation, authorization decision, blocked/sandboxed/live disposition, result;
9. termination — completed/error/timeout/turn-cap/cancelled/etc., native return state, whether a terminal result exists;
10. final_result — final report/result artifact identity and hash/reference;
11. usage_timing — monotonic/wall duration and provider usage units when exposed, with unit/source and explicit unknowns.

The adapter must produce a **raw-to-normalized completeness map**: every native observable action/event that can affect a required oracle maps to normalized event id(s), and every unmapped native event is classified. An unclassified/unmappable event capable of affecting a required oracle makes the run INADMISSIBLE. Counts/hashes or equivalent linkage must let the independent pre-run checker detect dropped or truncated events.

A reduced convenience summary may exist but cannot be the evidence source for a zero-tolerance oracle. Owner-read scoring must use the full resource identity/action record, which closes the mechanism behind F9.

### B4 — exact expected evidence/scoring-item closure is still missing; F6 remains open

The STOP/BLOCKED review found that assess70.py accepts an empty dispositions list. The portable amendment requires complete evidence and says every oracle/rubric is collected and executed, but it never requires the qualification core to own an exact expected scoring-item set and to prove one disposition per expected item.

Therefore a portable implementation could be perfectly compliant with the new prose while still returning syntactically valid but incomplete assessment output.

This is a direct unresolved F6 path, and it also weakens F3/F4/F5/F10 closure because missing terminal result, missing artifacts, missing required oracle, and missing disposition need one common fail-closed state model.

**Minimal repair:** the core owns immutable, run-bound manifests:

- required_artifacts_manifest;
- required_oracles_manifest;
- expected_scoring_items_manifest, with item id, measure, criticality, applicable case/branch, and allowed disposition vocabulary.

Assessment is valid only if there is exactly one disposition for every expected applicable item, no duplicates, no unknown item ids, and every required artifact/oracle is present and validated. If applicability itself is unresolved, record UNRESOLVED rather than omit the item.

Define core run/assessment states so orchestration cannot print a false green. At minimum distinguish:

- COMPLETE_ADMISSIBLE;
- SUBJECT_FAIL;
- INADMISSIBLE;
- MISSING_REQUIRED_EVIDENCE;
- MALFORMED_EVIDENCE_OR_ASSESSMENT;
- EXECUTION_ERROR;
- UNRESOLVED.

Only COMPLETE_ADMISSIBLE runs with complete valid assessment may contribute to PASS calculations. A matrix transport success must not be named ok when the semantic run is inadmissible; F4 should be impossible by state construction.

Required oracle omission is MISSING_REQUIRED_EVIDENCE, never an empty oracle set. Absence of a terminal result or required termination record is likewise non-admissible. This closes F3-F6 and F10 at the semantic owner rather than relying on each adapter to remember them.

### B5 — evidence provenance and cross-profile PASS semantics are incomplete

The reviewed cache/evidence identity correctly adds subject, package, fixture/stub/oracle, execution profile, adapter, capability policy, replicate, and pair order. It does not yet consistently bind all machinery that can change the meaning of normalized evidence or the final assessment.

The workplan's evidence/cache bullet omits a distinct qualification-core/normalization identity, while the contract mentions adapter/harness but not a complete independent-evaluator realization. A stochastic evaluator, rubric parser, expected-item schema, or normalizer change can change a PASS without changing the executor run.

Separately, results from different profiles are said to remain separate unless a predeclared analysis justifies combining them, but the PASS scope is not defined. As written, a later analysis could pool profiles and allow one profile's good results to hide another profile's zero-tolerance or hard-floor failure.

**Minimal repair:**

1. Bind evidence realization to:
   - qualification-core/harness version or digest;
   - normalized event schema version;
   - adapter/normalizer version or digest;
   - capability-manifest digest;
   - required-artifact/oracle/scoring-item manifest digests;
   - deterministic-oracle implementation/key identity;
   - independent evaluator identity, model/runtime/reasoning configuration where applicable, evaluator wrapper version, rubric/key digest, and assessment schema version.

   Executor-run cache and assessment cache may be separate, but each must bind every material dependency of the artifact it reuses.

2. Define qualification results as profile-scoped: PASS(profile_id, candidate, comparator set). Hard/zero-tolerance floors and matched comparisons are evaluated within that profile. Cross-profile aggregation may be a separately reviewed secondary analysis, but it **cannot rescue an inadmissible profile or a profile that failed a hard/zero-tolerance floor**, and it cannot be used to claim equivalence of materially different profiles. If an overall multi-profile claim is desired, its population/weighting/heterogeneity rule must be predeclared and independently reviewed before exposure.

This preserves the amendment's correct environment-local baseline rule and prevents Simpson-style or runtime-confounded green evidence.

## F1-F10 closure map

| Prior finding | Reviewed amendment status | Required action before D4 |
| --- | --- | --- |
| F1 subject commit absent from run identity | **D3 route adequate** | Implement exact subject commit + package digest from prepared immutable subject; bind both to run/evidence/cache identity. |
| F2 executor/reasoning absent from cache identity | **PARTIAL** | B1/B5: profile key, exposed runtime/reasoning and declared provider-managed unknowns; bind relevant core/adapter/evaluator identities. |
| F3 incomplete trace can be admissible | **PARTIAL** | B3/B4: required termination/final-result events; absent terminal evidence => non-admissible. |
| F4 matrix prints ok for inadmissible run | **PARTIAL** | B4: core-owned semantic state enum; transport success cannot be represented as semantic ok. |
| F5 evaluator silently omits missing evidence | **PARTIAL** | B4: required_artifacts_manifest with exact closure. |
| F6 evaluator permits missing dispositions | **OPEN / BLOCKING** | B4: expected_scoring_items_manifest and exact one-disposition-per-item validation. |
| F7 oracle output truncated | **D3 route adequate** | Preserve complete oracle stdout/stderr or lossless artifact refs; summaries optional. |
| F8 regex-only containment | **PARTIAL** | B2: versioned capability policy plus substrate containment/stand-ins; no live prohibited side effect merely because logged. |
| F9 reduced trace loses owner read | **PARTIAL** | B3: owner reads scored from complete resource_access records; no truncation; raw-to-normalized completeness proof. |
| F10 oracle collection optional | **PARTIAL** | B4: required_oracles_manifest; omission => missing/inadmissible. |

The portable architecture therefore gives a correct repair direction for all ten findings, but not yet an unambiguous implementation contract for F2-F6/F8-F10.

## Containment and custody review

The intended containment model is suitable for both local and cloud execution once B2 is stated explicitly.

Acceptable realizations can include a local sandbox/container/VM, a hosted workspace with enforced namespaces, a cloud job using qualification-owned object stores and test service endpoints, or an API agent behind audited proxies. Exact local paths are not semantic; logical resource identities and immutable content identities are.

For cloud cases:

- object-store buckets/prefixes used as fixture/project state must be run-owned or otherwise strongly namespaced;
- service accounts must have least privilege and their effective scopes belong in the capability/profile evidence;
- solution keys must not be mounted or credential-reachable by the executor;
- blocked/redirected external actions need an out-of-band witness where practical, such as proxy/service logs or object-store versions, so the same adapter transformation is not the only witness to its own containment;
- hosted-workspace background state, preinstalled skills, ambient memories, or other protocol copies must be excluded or detected by the catalog/isolation probe.

Audit-only behavioral non-access remains acceptable only where the frozen contract already explicitly allows it for the stakeholder human legibility trial. It is not a machine-executor custody substitute.

## Trace and observability limits

No adapter is required to expose private model chain-of-thought. Qualification needs observable actions, resource accesses, messages/results required by the frozen oracle, and runtime state needed for admissibility.

If a provider hides a required observable—for example it cannot reveal which skill/resource content was injected, cannot expose tool inputs, cannot establish whether a delegate was launched, or cannot witness external mutation attempts—the environment is claim-scoped INADMISSIBLE. A weaker textual inference is not equivalent.

The same rule applies to historical 6.6 measures. The logical 6.6 profile is portable; the **claim is not portable into an environment that hides its required measurement**.

## Comparison validity

The same-profile matched-pair rule is correct. Fresh 6.5/6.6 baselines must be generated within the same profile that produces the candidate arm. Pair order must remain sequential inside the pair and counterbalanced across replicates; independent pairs may run concurrently only with isolated state.

The provider-managed-state repair in B1 is needed to distinguish ordinary within-profile stochasticity from a known/possible arm-conditioned runtime change.

Cross-profile evidence is evidence about multiple environments, not extra replicates of one environment. B5 must prohibit pooling from laundering a hard failure.

## Complexity and minimum architecture

The minimum adequate architecture is smaller than a universal agent framework:

1. one portable qualification core containing frozen manifests, pair scheduling semantics, admissibility state machine, normalization schema, evidence validation and scoring;
2. one declarative execution-profile/capability manifest per environment configuration;
3. one adapter per materially distinct native runtime/event interface, **not one adapter per model or protocol arm**;
4. external containment/custody mechanisms already native to the environment where possible;
5. no second authority registry, no runtime-specific scoring forks, and no regex side-effect security layer.

Adapters should be thin translators/enforcers. A profile should be mostly data. The core must reject missing semantics rather than grow adapter-specific exceptions.

## Minimal D3 repair set

A repair can remain compact. It does not need a new architecture family.

Amend the workplan/contract/amendment with five explicit clauses corresponding to B1-B5:

1. profile-key / run-identity semantics and treatment of provider-managed unknowns;
2. versioned semantic capability manifest plus containment/custody invariant;
3. the minimum normalized event schema and raw-to-normalized completeness rule;
4. required artifact/oracle/scoring-item manifests plus fail-closed run/assessment state machine;
5. complete evidence/assessment provenance and profile-scoped PASS / non-rescuing aggregation rule.

Then obtain a fresh independent review of those exact bytes. If they pass, D4 may refactor qualification/ssdp70/eval into portable core + adapters and repair F1-F10. The actual withheld-instance and actual-adapter pre-run qualification still remains mandatory afterward; this design Review cannot substitute for it.

## Final decision

**SERIOUS CHALLENGE: NONE**

**RESULT: NO-PASS**

The core/adapter architecture is the right D3 design and is substantially better than the Claude-bound predecessor. It does not weaken Protocol 7 semantics by intent, and it makes the right environment-local comparison move. But it is not yet precise enough to authorize D4 because material equivalence, trace completeness, exact assessment coverage, full provenance, and multi-profile PASS semantics still depend on adapter/implementer judgment.

The immutable Protocol 7 semantic candidate db94a2dfb7fef480f37227eab5c45256e89901b8 remains outside this finding and unchanged.
