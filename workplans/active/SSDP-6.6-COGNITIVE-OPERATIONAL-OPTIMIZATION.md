---
kind: protocol-minor-revision-workplan
workplan_id: SSDP-6.6-COGNITIVE-OPERATIONAL-OPTIMIZATION
protocol_version: 6.5.0
target_protocol_version: 6.6.0
status: implementation-rework-required
created_date: 2026-09-26
reviewed_date: 2026-09-26
workplan_review_state: PASS_NONINDEPENDENT_R3
implementation_review_state: NO_PASS_R1
implementation_reviewed_date: 2026-09-26
implementation_review_basis: 26059544204c65b1e0292cd229e95f61b5f970bb
base_protocol: Protocol 6.5
base_accepted_source: 7f7b5e24858e813e45ace867a7f8ea5180f43bf0
base_recovery: c4d5da1e0acb0e9f27376bf69561e8762747cd2d
branch_base: 23e46543c174a8451bbadc402df63538105eab10
active_serious_challenge: none
---

# Protocol 6.6 Cognitive and Operational Optimization

## 1. Outcome and scope

Protocol 6.6 is a backward-compatible operational optimization of accepted Protocol 6.5.

The protected outcome is:

> Preserve the scientific/software correctness, authority, evidence, historical-learning, simplicity, Review, and proportional-rigor capabilities accumulated through Protocol 6.5 while materially reducing the amount of protocol machinery an agent must keep active, reconstruct, or procedurally replay during ordinary work.

The motivating failure mode is no longer primarily missing engineering doctrine. Recent protocol and downstream development campaigns show increasing trajectory complexity: repeated context reconstruction, long mandatory reads, large handoffs, repeated Review/repair cycles, formalization or evidence work whose decision value is low, and agent attention consumed by protocol mechanics rather than the governed engineering problem. Protocol 6.5 materially improved proportional rigor and stopping semantics; Protocol 6.6 must make the representation and runtime-facing organization of the protocol obey those principles more effectively.

Protocol 6.6 is therefore primarily a **cognitive/operational architecture and representation revision**, not an expansion of engineering scope.

### Success condition

A conforming 6.6 candidate SHALL:

1. preserve every still-valid accepted 6.5 capability and historical safeguard;
2. reduce the normal hot-path instruction/context burden and unnecessary routing/procedural work;
3. preserve cold-path discoverability and decision-changing semantics;
4. externalize transient coordination state where useful without creating new semantic/workflow authority;
5. improve long-horizon resumability and context compaction;
6. make empirical agent-trajectory evaluation part of protocol self-improvement without allowing benchmarks to become product authority;
7. remain usable without a mandatory orchestrator, hosted service, vendor-specific model, multi-agent runtime, or project memory service;
8. preserve the deliberate Protocol 7.0 architecture boundary.

## 2. Governing authority and preserved doctrine

Protocol 6.5 accepted-current semantics remain the parent authority. Capability rather than historical wording is the compatibility oracle.

At minimum, 6.6 SHALL preserve:

- D1 scientific/mathematical, D2 numerical/algorithmic, D3 software-architecture, and D4 specification/implementation ownership;
- recursive abstraction/concretization and earliest-owner routing;
- authority/evidence/concretization separation;
- accepted-authority versus cycle-scoped workplan freeze versus delegated machinery;
- Challenge and Serious Challenge semantics and required human adjudication where governed;
- minimum justified concretization complexity and active simplification;
- importance-weighted attention, proportional rigor, escalation/de-escalation, opportunity-cost and stop rules;
- evidence specification -> realization -> observation -> assessment, applicability/staleness, target-vs-execution dependency, real-owner/proxy-proof testing, and common-mode/independence discipline;
- affected regression/integration and bounded impact closure;
- Lossless Representation's protected property: no decision-changing governed semantic element may be silently lost through compression, routing, handoff, or generated views;
- progressive disclosure, one current semantic owner, cold but discoverable specialized/history paths, and derived-view subordination;
- semantic-definition/source-availability/parameter/import/warrant discipline where materially applicable, including the rule that a specialized substantive inference cannot use a merely discoverable definition/import until the exact needed owner meaning is available in the active reasoning context;
- Project Engineering Memory (PEM) as evidence-backed, project-local, non-authoritative learning rather than D5;
- Historical Applicability Set (HAS), capability-transfer, counterevidence, binding-health, and project-memory lifecycle protections where PEM is activated;
- convergence/review-saturation/family-level repair and Stabilization/maintenance-health capabilities;
- language/tool specialization, security/trust boundaries, release/recovery, documentation, and repository hygiene;
- immutable historical source/profile/recovery semantics and 6.5 release-state ownership;
- portable skill discovery/activation versus post-selection reference-routing as distinct evidence boundaries: metadata that helps a harness choose a skill is not proof that the chosen skill loaded/applied its required owners, and internal routing correctness cannot repair a skill that was never selected;
- generic Agent-Skills-style core validity versus vendor-adapter support as distinct contracts; vendor metadata may improve one harness but cannot define generic SSDP skill validity;
- current pre-7 orchestration/profile control semantics: Protocol 6.6 may update version-bound prompt/source bindings and generated descendants, but SHALL NOT change machine lifecycle authority, transition semantics, or orchestration profile/control schema merely to realize cognitive optimization.

Compression is acceptable only when the resulting current owner plus explicit retrieval routes preserves equal-or-stronger behavior. Protocol 6.6 must not obtain shorter prompts by weakening acceptance, hiding uncertainty, deleting an applicable cold path, or converting a specialized obligation into an optional suggestion.

## 3. Explicit non-goals and Protocol 7 boundary

Protocol 6.6 SHALL NOT:

- implement Protocol 7's deterministic workflow control plane;
- make the current Orchestrator mandatory;
- transfer D1-D4/workflow acceptance authority into machine state, a scheduler, a reducer, an index, an eval harness, or a memory service;
- replace human semantic adjudication with scores or automated lifecycle transitions;
- require a hosted external agent platform or vendor-specific API;
- require multi-agent execution for ordinary work;
- require formal semantic machinery for ordinary local engineering merely because the machinery exists;
- introduce a universal project ontology, universal dependency graph, or universal evidence database;
- optimize token count, file size, tool-call count, latency, or benchmark score at the expense of governed correctness;
- change the pre-7 orchestrator state machine/control ownership/profile schema as an incidental implementation detail. Evidence that such a change is necessary reopens D3 and the major-version boundary rather than being smuggled into 6.6.

Protocol 7 remains separately proposed. If 6.6 is later accepted before Protocol 7 implementation, Protocol 7 must receive a bounded inheritance reconciliation analogous to prior 6.x inheritance revisions. That reconciliation may adopt 6.6 capabilities but must not be pre-implemented by this work.

## 4. Project Engineering Memory / historical intake

This is substantial rework of mature protocol machinery and is memory-triggering. However, the current root `PROJECT-ENGINEERING-MEMORY.md` cannot safely be asserted as a reconciled accepted/base PEM for this cycle: its front matter is maintained under Protocol 6.5 but still names Protocol 6.4 P0 as `accepted_base.project_state` and a 6.5 candidate overlay even though Protocol 6.5 is now accepted-current.

Protocol 6.6 SHALL NOT guess the correct accepted-memory publication from `main`, latest, timestamps, or release-looking identities.

Current memory disposition:

```yaml
pem_basis:
  accepted_project_state: 23e46543c174a8451bbadc402df63538105eab10
  accepted_pem: REVIEW_REQUIRED
  candidate_overlay_semantic_candidate: NONE
```

Because missing/partial/stale memory metadata cannot prove absence, plan design performed bounded direct historical intake of every currently represented family/capability/discovery. These are **provisional applicability hypotheses**, not a canonical HAS until the accepted/base PEM is reconciled:

- `FF-001` — applicable hypothesis: 6.6 successor publication must not repeat premature immutable fallback publication.
- `PC-001` — applicable hypothesis: frozen 6.5 and older source/profile/recovery capability must be preserved.
- `SP-001` — applicable hypothesis: routing/representation repair should occur at canonical owners followed by deterministic regeneration rather than package-side shadow fixes.
- `SP-002` — applicable hypothesis: retain the demonstrated self-reference-safe candidate -> descendant publication -> distinct recovery pattern.
- `DS-001` — applicable hypothesis: structural/context/eval fixtures may claim only the property their oracle discriminates; semantic adequacy and engineering-outcome claims require stronger evidence.

**Stage-A prerequisite:** reconcile project-local PEM publication/base/overlay state under accepted 6.5 governance, then construct the exact canonical HAS before any 6.6 implementation decision relies normatively on project-memory applicability. If reconciliation remains unavailable, bounded historical intake may inform falsification but memory-dependent positive guidance remains `REVIEW_REQUIRED`.

This prerequisite repairs project-memory coordination state; it does not alter D1-D4 Protocol 6.5 authority.

## 5. D3 cycle architecture

### 5.1 Tiny universal semantic kernel

The always-loaded cross-domain kernel SHALL contain only semantics needed for substantially all governed work:

- D1-D4 domain ownership and earliest affected owner;
- abstraction/concretization;
- authority versus evidence versus delegated machinery;
- materiality;
- feasibility/correctness before simplicity/economy;
- minimum justified complexity and local-first repair;
- Challenge threshold;
- proportional rigor/importance/stop principle;
- progressive disclosure and one-current-owner rule;
- decision-changing semantics must remain recoverable while active context/inferential cost is minimized;
- external/evidence content not being instruction authority.

The current large `abstraction-and-concretization.md` SHALL be decomposed so specialized semantic-definition/traceability, lifecycle, evidence, memory, or other conditional detail is loaded only through explicit predicates. The exact file partition is delegated D4 unless semantic ownership requires a particular split.

**Acceptance property:** a competent agent performing a normal local D4 task can recover all universal governing invariants without loading formal semantic-definition, PEM, deep evidence-lifecycle, protocol-history, or other non-triggered detail.

### 5.2 Risk-triggered semantic precision

Protocol 6.4's semantic-definition and traceability capability SHALL be preserved but made conditionally hot.

The router SHALL distinguish approximately:

```text
ordinary engineering meaning
  -> precise prose/types/contracts/tests sufficient

material ambiguity, specialized scientific/numerical object, parameter/default binding,
external result/import, formal claim/warrant, or dependency-impact question
  -> activate semantic-definition/source/traceability owner

proof/publication/safety/interoperability/high-consequence ambiguity
  -> deeper formal closure proportional to the decision
```

Precision is mandatory where semantics require it; formalization effort is not intrinsically mandatory.

This routing change SHALL NOT weaken Protocol 6.4/6.5 source-availability or runtime-context-availability semantics. Conditional activation controls **when specialized detail is loaded**, not whether a materially used specialized semantic object needs a coherent canonical owner/import and the exact meaning required by the inference. "Ordinary engineering meaning" applies only when no materially specialized semantic object or ambiguity trigger exists.

### 5.3 Minimal role entrypoints

D1-D4 and specialist `SKILL.md` entrypoints SHALL become routers and role contracts rather than compressed textbooks.

Each entrypoint should preferentially contain:

1. owned semantic boundary;
2. universal-kernel route;
3. concern activation predicates, including material negative triggers where they prevent eager activation;
4. a short owner-specific method/invariants;
5. completion/Challenge contract.

Skill/frontmatter and host-adapter descriptions are **pre-load discovery/selection interfaces**, not miniature protocol summaries. Keep them sufficient to make the skill's owned task class and important exclusions distinguishable without duplicating child doctrine or mutable release state.

Treat selection and internal routing separately:

```text
catalog metadata exposed
  -> zero/one/admissible skill root selected
  -> SKILL.md loaded
  -> conditional concern owners loaded
  -> governed decision
```

A bad selection cannot be repaired by a perfect cold-reference graph that is never reached. Conversely, selecting the right root does not prove its conditional owners were read or applied. Optimize both boundaries independently.

Do not overfit selection to a rigid single-label taxonomy. For mixed/ambiguous tasks define an **admissible root set** whose members can safely reconstruct/reroute to the earliest semantic owner; evaluate false activation, missed activation, and materially wasteful multi-activation rather than requiring one arbitrary exact root when several are semantically safe.

Generic frontmatter `name`/`description` remains the portable core selection surface. `agents/openai.yaml` and future vendor adapters are separately scoped host interfaces: they may be optimized and qualified for their named harness but SHALL NOT become generic validity or hidden authority.

Prefer direct role -> concern-owner activation when the predicate is already knowable; an added routing hop must narrow the question or add material semantics rather than exist for taxonomy alone.

Long generic doctrine, duplicated evidence rules, repeated PEM schema mechanics, repeated workflow choreography, and examples that do not change routing should live at canonical conditional owners.

Local restatement is permitted only when it materially lowers total inferential cost; repeated multi-paragraph doctrine is not.

### 5.4 Decision-sufficient projections under Lossless Representation

Protocol 6.6 SHALL preserve the semantic guarantee of Lossless Representation while strengthening its operational objective:

> Minimize the active representation subject to preservation and recoverability of every decision-changing governed semantic element.

A compact handoff/workplan/review MAY replace locally replayed detail with exact resolvable current-owner references when the consumer has a supported retrieval route. If the receiver cannot resolve the governing version/owner, the representation must carry the minimum semantics needed for the governed decision rather than relying on hidden context. The hot representation should prefer:

- objective/governed outcome;
- exact authority/workplan/candidate identities;
- local decisions and delegated space;
- open blockers/uncertainty/Challenge;
- applicable evidence state;
- next action;
- genuine reopen/stop conditions.

Raw chronology, generic doctrine, settled rationale, long evidence logs, and cold project history should remain retrievable rather than active.

This is an operational strengthening of Lossless Representation, not permission for lossy summarization.

### 5.5 Operationalize existing transient Working State / Context Checkpoint

Protocol 6.5 already owns the concept of compact temporary working state for long/interruption-prone work. Protocol 6.6 SHALL **operationalize and simplify that existing capability**, not create a second lifecycle/state owner.

Working State remains derived, non-authoritative coordination cache for long or interruption-prone work. It may record:

```text
governed objective
protocol/authority/workplan/candidate identities
current stage or action
open/closed material obligations
current evidence/applicability state
blockers/risks/Challenge
next action
reopen conditions
```

It SHALL NOT:

- create or mutate D1-D4 authority;
- self-declare acceptance;
- replace a canonical workplan/evidence record;
- become a required repository artifact for local work;
- remain current after its protocol/authority/workplan/candidate/regime basis changes.

The representation may be Markdown, YAML, JSON, host session state, or another equivalent form. The protocol defines only the minimum semantics needed for safe compaction/resume; the host/runtime representation remains delegated.

Do not add a permanent Working-State schema/tool merely for symmetry. Standardize additional structure only when baseline/evaluation evidence shows it materially reduces reconstruction cost or ambiguity.

### 5.6 Workplan/state separation

Workplans SHALL remain bounded semantic/cycle contracts. Frequently changing execution state SHOULD move to Working State or native issue/task/agent state rather than amendment accumulation in the workplan.

A workplan should change when its governed contract changes, not merely because:

- one task completed;
- a command ran;
- a test passed;
- a transient blocker cleared;
- the next action changed;
- an implementation-local repair occurred within delegated space.

Version-controlled workplan amendments remain warranted for material cycle-decision changes, newly binding obligations, genuine reopen, or acceptance/lifecycle state that the project deliberately owns there.

### 5.7 PEM agent-facing simplification

PEM's evidence/authority safeguards SHALL remain intact, but ordinary agents should not need to ingest the storage/governance schema to use project learning.

Provide a compact agent-facing contract centered on:

```text
when memory activates
how to retrieve relevant entries
how to decide applicability
how authority binding differs from evidence-only learning
how to preserve counterevidence/uncertainty
when a durable memory update is justified
```

Schema identifiers, lineage mechanics, counters, publication/base/overlay integrity, validation, indexes, and derived statistics SHOULD be enforced or exposed through existing/project-local tooling where mechanically decidable, remaining cold unless a memory-governance question triggers them.

A CLI/API/query convenience MAY be added, but no memory service is mandatory and canonical Markdown/project files remain usable without it.

### 5.8 Cognitive-resource escalation

Extend Protocol 6.5's LIGHT/STANDARD/DEEP treatment so it may govern cognitive resources in addition to engineering evidence depth.

When the host supports such controls, unresolved decision-sensitive uncertainty may justify escalating one or more of:

- model capability;
- reasoning budget;
- context budget;
- tool breadth;
- independent review trajectory;
- specialist/subagent decomposition.

No vendor/model name is normative. Hosts without such controls remain conforming.

The escalation rule is:

> Use the least expensive cognitive configuration that can reliably resolve the governed decision; escalate only when remaining uncertainty/consequence justifies it; de-escalate/stop once it does not.

Do not turn resource selection into a new optimization subproblem. Use the host/project default when it is adequate; escalate on concrete risk, failed/ambiguous attempts, or known capability requirements. If the host already performs trustworthy automatic resource routing, do not duplicate it with a parallel SSDP scheduler.

Model tier, reasoning budget, token budget, or subagent count is execution policy, never semantic authority or a pass threshold. A stronger model does not substitute for an independently required Review.

A high-stakes parent does not force the strongest model/subagent path for every child detail.

### 5.9 Optional independent cognitive trajectories

For substantial/high-risk work with low coupling between review questions, Protocol 6.6 MAY use separate agents/contexts for independent falsification, e.g.:

- conformance/affected-surface review;
- abstraction-adequacy/Challenge;
- simplification/complexity challenge;
- scientific/numerical specialist review;
- evidence/oracle challenge.

Independence requires materially separate reasoning context; subagents that merely receive the author's conclusions do not qualify as independent. Separate context improves process independence but does not by itself prove epistemic independence when agents share the same model, source corpus, toolchain, or oracle. Record material common-mode dependencies when the claim relies on independence, and add a distinct evidence route or perspective only when it materially reduces that risk.

Multi-agent execution is not required when:

- the task is local/trivial;
- the questions are tightly coupled to one live execution state;
- decomposition overhead exceeds likely information gain;
- the host cannot provide independent contexts.

A synthesizer may reconcile findings but cannot erase unresolved contradictory material evidence by vote.

### 5.10 Review strategy after recurrence

Repeated related Review failures SHALL change the search strategy before another narrow repair/review loop.

When evidence shows a shared family, review saturation, or repeated candidate churn, the next review/reconsideration should proportionately switch from isolated finding discovery toward:

- bounded sibling/family closure;
- simplification/re-derivation;
- evidence-method challenge;
- upstream abstraction adequacy;
- common-mode cause analysis.

No numeric review count changes the pass threshold. A small repeated count may be used only as an information-policy trigger when the evidence already indicates common cause.

### 5.11 Operationalize existing version/source coherence rule

Protocol 6.5 already requires governing-version-compatible source resolution and forbids silent latest/default reinterpretation. Protocol 6.6 SHALL make that existing rule cheap and explicit at execution entry rather than invent a second version authority.

When a task declares or can cheaply resolve a governing SSDP version, the execution path SHALL compare that version with the loaded skill/source identity before substantive protocol-dependent reasoning.

```text
governing version == loaded compatible source
  -> continue

governing version != loaded source
  -> resolve exact compatible local or immutable public source

version unavailable and task not version-bound
  -> ordinary installed/current routing
```

A mismatch must not silently reinterpret version-bound work with latest/default doctrine. The handshake should reuse existing `PROTOCOL_VERSION`, manifests, release state, and source-resolution rules rather than create a second version authority.

Mechanically checkable mismatch behavior SHOULD be tested. The preflight itself must stay cheap, reuse existing `PROTOCOL_VERSION`/manifest/release-state authority, and must not turn every ordinary repository task into a remote protocol lookup or a parallel control plane.

## 6. Empirical protocol evaluation

Protocol 6.6 requires bounded empirical evidence that operational changes help rather than merely making source files look smaller. Detailed scenario, matched-comparison, provenance, holdout, non-regression, anti-overfitting, and evaluation-economy semantics are owned by [Protocol 6.6 Evaluation and Qualification Contract](../../qualification/ssdp66/PROTOCOL-6.6-EVALUATION-AND-QUALIFICATION-CONTRACT.md).

Keep these hot invariants:

- evaluation is evidence, never D1-D4 authority or an automatic acceptance oracle;
- compare against exact accepted 6.5 under matched conditions as practical;
- execution-agent self-assertion is not sufficient correctness evidence;
- semantic correctness/non-regression is a feasibility gate before operational optimization;
- static context reduction does not prove live trajectory improvement;
- claimed improvement remains bounded to tested task/model/runtime regimes;
- evaluation infrastructure itself must satisfy minimum justified complexity.

Load the cold contract only when the evaluation/qualification decision is active.

## 7. Required implementation surfaces

Implementation is expected to touch, as justified by final design:

- `source/shared/references/abstraction-and-concretization.md`;
- one or more new/extracted conditional semantic-definition/traceability references;
- D1-D4 `source/roles/*/SKILL.md` entrypoints;
- supporting specialist entrypoints where duplicated hot doctrine exists;
- `workflow-and-workplans.md`;
- `convergence-and-cycle-economy.md`;
- `repository-intake.md`;
- `project-engineering-memory.md`;
- `testing-and-validation.md`;
- `tool-assisted-engineering.md` where cognitive/subagent/eval tooling relations require routing;
- `development-workflow-prompts.md` or its replacement representation, while preserving a complete manual/portable execution path that does not depend on hidden orchestrator state;
- versioning/source-resolution surfaces needed for the cheap version handshake;
- protocol self-evaluation fixtures/harness and tests;
- all role/specialist frontmatter `name`/`description` selection metadata and supported host adapters such as `agents/openai.yaml`, with generic-core versus adapter validation kept distinct;
- build/package/profile/snapshot generation and corresponding tests, including `protocol-manifest.json`/host-adapter metadata and the distinction between discovery, activation, transport closure, and conditional reference loading;
- root README/CHANGELOG and semantic history at closeout.

This list is an initial affected surface, not a license to edit every file. Implementation should touch the smallest owner set that closes the accepted design.

## 8. D4 delegated design space

Unless semantic Review shows otherwise, D4 may choose:

- exact file partition/names for extracted references;
- whether a compact kernel is generated or hand-authored, provided it has one canonical owner and generated derivatives do not become parallel authority;
- exact Working State encoding and whether any helper script exists;
- PEM query/index command shape;
- eval harness language/format;
- scenario fixture format;
- model/runtime adapters;
- static context-footprint measurement method;
- implementation of version preflight using existing manifests/release state;
- generated package/profile mechanics consistent with current release architecture.

A 6.6 version-bound profile/snapshot may bind updated 6.6 skills/prompts while retaining the current pre-7 machine lifecycle/control schema. Any required change to orchestrator transition authority, state graph, reducer/control ownership, or profile schema is outside delegated D4 space and reopens D3/major-version classification.

Avoid new permanent frameworks when existing Markdown, Python validation/build scripts, and current package/profile machinery suffice.

## 9. Implementation stages

### Stage A — Baseline and preservation map

1. Freeze the exact 6.5 accepted source/recovery and current branch base.
2. Reconcile the project-local PEM accepted/base/overlay state or retain explicit `REVIEW_REQUIRED`; construct the canonical HAS only after that basis is valid.
3. Build a bounded capability-preservation map from current 6.5 and accepted historical lineage, with special attention to 6.2 progressive disclosure, 6.3 PEM, 6.4 semantic precision, and 6.5 proportional rigor. Treat the map as review evidence, not a new semantic registry; organize by capability family/current owner/activation/acceptance sentinel rather than replaying every historical clause.
4. Bind the exact accepted 6.5 behavioral baseline at both layers: canonical semantic source `7f7b5e24858e813e45ace867a7f8ea5180f43bf0` and accepted-current installed/generated package/profile surface at cutover `2b8ce17b1f086dc85e6fa8014c4a7bcc45ef60cb`.
5. Measure current catalog-selection metadata footprint, static mandatory-read closure after root selection, and, where practical, observed live selection/active protocol context for representative routes.
6. Load the cold evaluation/qualification contract and freeze the compact development and holdout/adversarial eval sets plus their claim boundaries before optimizing the protocol.

**Gate:** no semantic source mutation until the memory-basis disposition, preservation obligations, baseline measurements, and eval-set identities are reviewable.

### Stage B — Kernel and routing reduction

1. Extract conditional semantic-definition/traceability material from the universal hot path.
2. Reduce role/specialist entrypoints to bounded routers/contracts.
3. Refine generic skill descriptions and named host-adapter descriptions only as needed to improve discovery/selection while reducing metadata burden; do not encode mutable protocol lifecycle state or detailed child doctrine in selection metadata.
4. Deduplicate generic doctrine to canonical owners plus local micro-invariants.
5. Rework workflow prompt representation toward invariants/boundaries/acceptance/escalation rather than procedural itineraries while retaining a complete manual/portable route.
6. Verify every moved capability remains discoverable from every materially applicable entrypoint.
7. Verify **discovery, transport, and activation separately**: selection metadata must make the appropriate root reachable; cold owners required by that root must remain present/reachable in the bundle; package membership or ordinary hyperlinks must not make them eagerly active.
8. Prefer deletion/extraction over adding new routing layers; a shorter file graph that requires more hops/inference is not an improvement.

**Gate:** routing/closure tests plus semantic Review of capability preservation.

### Stage C — Working-state and memory-use optimization

1. Define Working State semantics and compaction/resume expectations.
2. Make the already-accepted workplan-contract versus transient-working-state distinction operationally clear; do not create a competing state authority.
3. Expose compact PEM agent-facing usage; add query support only if baseline/eval evidence justifies permanent machinery.
4. Preserve full PEM governance/schema validation on cold paths.
5. Add negative cases proving transient state/summary/index cannot become authority.

### Stage D — Cognitive resource and independent-review routing

1. Add vendor-neutral cognitive escalation/de-escalation semantics without duplicating trustworthy host automatic routing.
2. Define optional independent subagent/reviewer decomposition predicates and common-mode limits.
3. Strengthen recurrence/review-saturation strategy switching.
4. Ensure ordinary/local work does not activate these capabilities merely because available.

### Stage E — Version coherence

1. Implement the cheapest execution preflight for the already-accepted version/source identity rule, consistent with current source-resolution authority.
2. Add positive/mismatch/offline/unversioned cases.
3. Prove frozen historical work is not silently reinterpreted by 6.6/latest.

### Stage F — Empirical evaluation and refinement

Load the cold evaluation/qualification contract.

1. Run structural context/routing comparisons.
2. Run selected live 6.5-vs-6.6 agent trajectory comparisons under matched environments where practical.
3. Inspect failures qualitatively; do not optimize a scalar score.
4. Remove or revise 6.6 machinery that adds cognitive/process burden without demonstrated semantic or operational value.
5. Repeat only the affected high-information cases after repair.

### Stage G — Final assembled acceptance

Load the cold evaluation/qualification contract for its counterfactual/claim-scope obligations.

Run the repository's inherited source tests, PEM checks when applicable, package validation, generated-dist parity, profile/snapshot/Core checks, exact-ref/source-resolution checks, and new 6.6 qualification.

Additionally verify:

- universal hot path is materially smaller than 6.5 for designated ordinary routes;
- no accepted capability lacks a reachable activation path;
- generic skill metadata preserves reliable discovery/selection for the declared task classes without bloating every prompt with child doctrine or mutable release state;
- package transport closure remains complete while package membership/hyperlinks do not imply activation;
- generic Agent Skill validity remains separable from vendor adapters, and any live host compatibility claim is bounded to the exact harness/model/install mode exercised;
- local/simple tasks do not automatically activate semantic formalism, PEM, multi-agent review, deep evaluation, or Protocol 7 machinery;
- substantial/high-risk tasks can still recover the full applicable doctrine;
- Working State/derived summaries cannot self-promote into authority;
- version mismatch is detected/resolved according to existing source authority;
- 6.6 profile/snapshot generation has not changed pre-7 lifecycle/control schema or orchestrator authority without an explicit D3 reopen;
- live trajectory evidence supports any claimed behavioral efficiency gain through an assessment route that is not merely the execution agent self-grading its own result;
- no stronger engineering-outcome claim is made than evidence supports.

### Stage H — Independent assembled-candidate Review and release lifecycle

1. Freeze an immutable 6.6 semantic candidate only after semantic implementation and qualification stabilize.
2. Perform fresh independent Review against accepted 6.5 with explicit preservation, abstraction-adequacy, cognitive-debt, and operational-evidence challenge.
3. Require stakeholder ratification under accepted release governance.
4. Use the accepted self-reference-safe public-source/recovery lifecycle; do not repeat premature immutable bootstrap publication.
5. If 6.6 becomes accepted before Protocol 7 cutover, feed its operational evidence and accepted capabilities into Protocol 7's already-required deliberate D3 Orchestrator architecture reopen. Do not treat this as a mechanical inheritance-only update: the reopen must reconsider whether Protocol 7's mandatory control-plane/orchestrator design remains the minimum justified architecture in light of 6.6 evidence.
6. Regenerate mapping-bearing descendants and complete release/documentation closeout.

## 10. Qualification and falsification

Detailed evaluation/qualification counterfactuals are owned by [Protocol 6.6 Evaluation and Qualification Contract](../../qualification/ssdp66/PROTOCOL-6.6-EVALUATION-AND-QUALIFICATION-CONTRACT.md).

Load that cold contract for Stage A evaluation design, Stage F live comparison, Stage G qualification, or Review of evidence adequacy. Ordinary implementation does not preload it.

The hot invariant is simple: structural evidence proves structure, live trajectory evidence proves only the tested behavior/regime, semantic Review proves assembled semantic adequacy, and no benchmark/eval result can waive a correctness or authority blocker.

## 11. Acceptance criteria

Protocol 6.6 is technically eligible for independent Review only when:

1. all accepted 6.5 capabilities are mapped to preserved current owners/routes or an explicitly reviewed equal-or-stronger generalization;
2. inherited repository regression/package/profile/Core/frozen-history checks pass where applicable;
3. new routing/context/state/version/eval counterfactuals pass;
4. designated ordinary task routes show a clear structural reduction in declared mandatory-read closure, and bounded matched live evidence demonstrates reduced actual burden on at least one intended operational dimension by more than obvious measurement noise and enough to justify any new permanent machinery, without weakening the acceptance contract;
5. designated specialized/high-risk preservation sentinels still recover every applicable cold capability, including specialized source/context availability semantics;
6. no mandatory orchestrator/service/vendor/model/subagent requirement has been introduced;
7. Working State, eval state, generated summaries, indexes, and memory-query views remain explicitly non-authoritative;
8. empirical live evidence exists for any claim that agent trajectory behavior improved; claims remain bounded to tested task/model/runtime regimes;
9. no open Serious Challenge or material preservation gap remains;
10. the candidate remains a minimum-justified operational architecture rather than adding a second control framework beside Protocol 7;
11. manual/portable skill use remains complete without hidden runtime state, hosted services, or mandatory Orchestrator participation;
12. accepted 6.5 compact-working-state and version-source-resolution semantics have been consolidated rather than duplicated under new names;
13. discovery/selection, package transport closure, and post-selection activation remain distinct and mechanically/behaviorally qualified after metadata/reference optimization;
14. selection qualification uses admissible-root semantics for mixed tasks and demonstrates no material increase in missed or wasteful activation on the tested reference environments;
15. generic package validity remains independent of vendor adapters, while each claimed host adapter is qualified only for its named environment;
16. live evaluation uses durable scenario/provenance identities and an outcome assessment route independent enough that execution-agent self-assertion cannot manufacture non-regression;
17. 6.6 profile/snapshot changes preserve current pre-7 lifecycle/control semantics and schema unless a reviewed D3 reopen explicitly changes the version boundary.

A smaller prompt/package is not sufficient. A candidate that is shorter but loses a materially applicable doctrine is No-Pass.

## 12. Documentation and release closeout

Before freezing the replacement semantic candidate:

- recompile root `README.md` as the current concise user-facing guide;
- update `CHANGELOG.md` with the 6.6 capability story rather than implementation chronology;
- update `history/SEMANTIC_EVOLUTION.md` with the material rationale and superseded design decisions;
- keep mutable release identities only in `PROTOCOL-RELEASE-STATE.yaml`;
- update `source/README.md` only as needed for contributor/source navigation;
- preserve frozen prior-version source/profile/recovery bytes;
- ensure the 6.6 source/package/profile can be resolved independently of mutable default-branch state.

## 13. Reopen / Challenge triggers

Reopen D3 design if implementation evidence shows any of the following:

- the tiny-kernel split cannot preserve a mandatory cross-domain invariant without broad eager loading;
- semantic-definition extraction creates ambiguous/conflicting ownership;
- description/metadata compression causes materially worse skill discovery or selection, or reliable selection appears to require copying child doctrine into the catalog metadata;
- portable selection behavior cannot be preserved without vendor-specific semantics becoming generic core requirements;
- Working State requires workflow authority rather than remaining derived cache;
- useful PEM simplification requires changing memory authority/evidence semantics rather than only its agent-facing interface;
- empirical evaluation shows the proposed routing consistently increases substantive error or hidden-constraint loss;
- cognitive-resource/multi-agent routing requires host-specific semantics that cannot be expressed portably;
- version preflight cannot be made cheap without introducing a second version authority;
- 6.6 overlaps Protocol 7's control-plane ownership rather than remaining a compatible pre-7 optimization;
- empirical 6.6 results materially undermine the assumptions supporting Protocol 7's currently proposed mandatory-control-plane architecture, in which case route that evidence into the required Protocol 7 D3 reopen rather than preserving the older proposal by inertia.

Raise Serious Challenge to accepted 6.5 only if credible evidence shows an accepted 6.5 doctrine itself is materially false, contradictory, inadequate, or unrealizable. Mere verbosity/operational inefficiency is a successor-design problem, not by itself a Challenge to the truth of 6.5 authority.

## 14. Implementation handoff

Implementation should begin from the accepted 6.5 baseline and this workplan only after workplan-level review closes material design gaps.

The implementer SHALL:

1. preserve semantics before optimizing representation;
2. prefer deletion/extraction/routing simplification over adding a parallel framework;
3. maintain a capability-preservation map throughout implementation;
4. keep protocol evaluation proportional and claim-bounded;
5. use transient state to reduce context replay without turning state into authority;
6. stop adding optimization machinery when the same decision can be achieved more simply;
7. freeze a semantic candidate only after source semantics and documentation stabilize;
8. leave independent Review, stakeholder ratification, publication/recovery, and accepted-current cutover to their governed lifecycle.


## 15. Workplan review disposition

Three adversarial, non-independent workplan review passes have been incorporated into the current text. Review chronology remains recoverable in Git rather than accumulating as binding amendment prose here.

Current disposition:

```text
SERIOUS CHALLENGE: NONE
WORKPLAN REVIEW: PASS_NONINDEPENDENT_R3
IMPLEMENTATION REVIEW: NO_PASS_R1
IMPLEMENTATION: REWORK REQUIRED BEFORE CANDIDATE FREEZE
FRESH INDEPENDENT ASSEMBLED-CANDIDATE REVIEW: BLOCKED PENDING REWORK
```

The implementation Review at branch head `26059544204c65b1e0292cd229e95f61b5f970bb` found no Serious Challenge to accepted Protocol 6.5, but candidate freeze is blocked by the bounded rework cycle in section 16. This review does not substitute for the fresh independent assembled-candidate Review required after rework.


## 16. Post-implementation Review rework cycle

### 16.1 Review disposition and governing problem

Implementation Review of branch head `26059544204c65b1e0292cd229e95f61b5f970bb` is **NO-PASS** at the implementation-complete / candidate-freeze boundary. Accepted Protocol 6.5 remains coherent; the findings are 6.6 concretization/evidence nonconformance, not a Serious Challenge to the parent protocol.

Three linked findings govern this rework:

1. **Execution-entry/version-source coherence is not reliably realized in the portable skill path.** The repository-only `source/version_preflight.py` correctly discriminates version mismatch when invoked, but the live skill path silently proceeded on version-bound work in most final-candidate runs. A helper that is not executed at the real boundary is proxy evidence, not closure.
2. **The declared universal hot path is not the observed hot path in the reference runtime.** Live trajectories often consumed the invoked `SKILL.md` but did not read the separately routed universal kernel/domain owner before acting. A smaller declared mandatory closure therefore proves structure only unless the required universal contract is actually present in the consumed execution surface.
3. **Acceptance criterion 4 lacks a demonstrated live burden reduction.** Selection correctness improved, but turns/tokens/cost on full trajectories were within noise. Selection accuracy is a distinct quality metric and cannot be relabeled as user intervention or cognitive burden without measuring that consequence.

Candidate freeze, independent assembled-candidate Review, ratification, publication/recovery and accepted-current cutover remain blocked until this bounded rework closes.

### 16.2 Rework objective and non-goals

The rework SHALL make the already-accepted 6.6 design effective at the real portable execution boundary and repair its evidence accounting with minimum justified change.

Protected constraints:

- do **not** add another control plane, mandatory Orchestrator/service, vendor dependency, model scheduler or permanent evaluation framework;
- do **not** repeat stronger-imperative prompt wording experiments as the primary fix; the existing evidence already shows wording strength alone is not a reliable mechanism;
- do **not** broaden this into Protocol 7 implementation or unrelated protocol redesign;
- preserve the accepted 6.5 capability map and every already-valid 6.6 simplification;
- preserve one canonical semantic owner for each invariant; generated/inlined derivatives must remain mechanically subordinate and parity-checkable;
- keep ordinary unversioned/local work cheap and free of remote lookup.

If these requirements cannot be realized in the generic portable skill architecture without hidden runtime control, duplicated authority, or broad eager loading, **stop and reopen D3** rather than layering more prose or machinery.

### 16.3 Rework Stage R0 — freeze discriminating evidence before semantic repair

Before changing the execution-entry/kernel realization:

1. Add and freeze one **fresh version-bound holdout** distinct from T4/T5, using a historical supported Protocol 6 version and a task whose product implementation can succeed even if the version rule is silently ignored. Freeze its task snapshot, expected governing version, oracle/rubric and provenance before the repair is exercised against it.
2. Record T4 as development evidence and T5 as a post-finding fresh challenge case; neither is to be represented as part of the untouched original Stage-A holdout after being introduced/reclassified during repair.
3. Predeclare at least one direct live **burden** metric for criterion 4. Preferred low-noise measures are observed active SSDP material on an activated route (invoked entrypoint plus actually loaded SSDP references), protocol-specific read/tool turns, unnecessary protocol/evidence actions, or actual correction/intervention/rework. Selection correctness remains reported separately and does not satisfy criterion 4 by itself.
4. Bind the exact 6.5 baseline, candidate source, harness/model/install mode and assessment route used for the rework comparison.

Keep the corpus small. Add only evidence capable of changing the acceptance decision.

**Gate R0:** no execution-entry/kernel semantic repair until the fresh holdout and burden metric are frozen.

### 16.4 Rework Stage R1 — realize the execution-entry and universal contract

Repair the real path consumed after a skill activates.

Required behavior:

- when a task or governing workplan declares an SSDP version, the loaded skill path must compare it with the loaded package/source identity **before substantive protocol-dependent action**;
- mismatch must route to a compatible installed/local source or exact immutable mapped source, or report truthful non-closure; it must not silently apply the loaded/latest doctrine;
- unversioned ordinary work must continue without remote lookup;
- the minimum universal invariants needed before domain action must be in a surface that the supported portable execution path actually consumes, rather than depending solely on a prose instruction to read a reference that live agents routinely skip.

D4 may choose the smallest realization consistent with section 8, including a generated/inlined micro-kernel or another mechanically subordinate entry surface, provided there is one canonical owner and generated derivatives cannot drift into parallel authority. The existing offline `version_preflight.py` may remain a convenience/testable realization, but it is not sufficient evidence unless the real path actually invokes or equivalently enforces the rule.

Do not solve this by copying the entire kernel or conditional doctrine into every entrypoint. Preserve progressive disclosure and keep the universal contract minimal.

**R1 acceptance:**

- the frozen fresh version-bound holdout shows **zero silent mismatch** across the predeclared bounded confirmation runs and detects/resolves/reports the governing-version mismatch before substantive implementation;
- at least one ordinary unversioned case proves no needless source lookup/control-plane activation;
- historical exact-source resolution remains exact-ref and never default/latest;
- the assembled package makes the universal pre-action contract mechanically recoverable from the actually consumed entry surface;
- generic package validity remains independent of vendor adapters.

A failure of the fresh holdout after the bounded repair is a blocker, not a finding to defer to Protocol 7.

### 16.5 Rework Stage R2 — demonstrate an actual live burden gain

Re-evaluate criterion 4 against the final repaired semantic state.

The comparison SHALL distinguish:

- selection/discovery correctness;
- structural declared closure;
- observed active protocol material/actions;
- total trajectory behavior.

At least one intended ordinary route must show a direct live burden reduction beyond measurement noise and large enough to justify the permanent 6.6 representation machinery, while semantic/correctness acceptance remains non-regressed. A deterministic active-context/read/action count may be preferable to noisy total-token/cost measurements when it more directly measures the protocol burden.

Do not claim:

- static byte reduction as live productivity;
- improved selection accuracy as reduced intervention unless intervention was actually observed/measured;
- unchanged turns/tokens/cost as an efficiency gain.

If no live burden dimension improves after the minimum repair, remove unjustified permanent machinery where possible and reopen the affected D3 success criterion/design rather than manufacturing a favorable metric.

### 16.6 Rework Stage R3 — repair evidence applicability and qualification state

After the final semantic repair:

1. Treat every changed `SKILL.md` entrypoint as part of any explicit-skill trajectory that consumed it, even when no changed reference file was separately read. Do not reuse T2/T3 or other prior trajectory evidence across an entrypoint mutation merely because the trace did not open a changed reference.
2. Re-run only the compact affected final-candidate trajectory/selection set needed to close correctness, R1 and R2. Evidence from unchanged selection metadata may be reused only for the property it still discriminates.
3. Regenerate static/package/profile evidence from the exact final semantic state.
4. Rewrite `qualification/ssdp66/STAGE-F-G-EVALUATION-AND-QUALIFICATION.md` so its disposition follows the evidence. Until R1/R2 pass it must not state `IMPLEMENTATION BLOCKERS: NONE KNOWN` or `READY FOR FRESH INDEPENDENT REVIEW: YES`.
5. Correct any README/CHANGELOG/semantic-history statement whose lifecycle or evidence claim became stale through this Review/rework.
6. Preserve failed/superseded runs as evidence; do not rewrite them away.

### 16.7 Final rework acceptance

The implementation becomes eligible for immutable candidate freeze only when all of the following hold on one final semantic state:

1. R1 real-boundary version/source coherence passes the fresh untouched holdout with no silent mismatch.
2. The supported portable execution path actually consumes the minimum universal pre-action contract; declared mandatory reads are not used as proof when the runtime skips them.
3. Criterion 4 has both structural reduction and a directly measured live burden reduction on at least one intended route; selection correctness is reported separately.
4. No new substantive correctness/authority/evidence regression versus accepted 6.5 is observed on the bounded matched cases.
5. The capability-preservation map remains closed; specialized/high-risk routes still recover their cold owners.
6. All evidence used for final qualification remains applicable to the exact final semantic candidate; semantic entrypoint changes invalidate affected prior live runs.
7. Repository regressions, PEM validation, canonical build, independent package validation, committed-dist parity, profile/snapshot frozen-history checks, Core acceptance and whitespace checks pass after the final semantic change.
8. No mandatory Orchestrator/service/vendor/model/subagent dependency or second version/control authority has been introduced.
9. Stage F/G evidence states no open implementation blocker and makes no claim stronger than its actual oracle/runtime supports.
10. Documentation/release-state surfaces remain coherent, with 6.5 still accepted-current until the later governed Stage-H lifecycle.

Only then freeze the immutable 6.6 semantic candidate and request the fresh independent assembled-candidate Review required by Stage H.

### 16.8 Rework D3 reopen triggers

Reopen D3 before further implementation if any of these become true:

- a portable generic skill cannot make the version-entry/universal pre-action contract reliably effective without mandatory hidden host behavior or a new control plane;
- guaranteeing the universal contract requires broad eager loading or duplicate semantic authority that defeats the 6.6 representation architecture;
- criterion 4 cannot be satisfied by any honest direct burden measure without adding more machinery than the measured gain justifies;
- the repair requires changing pre-7 Orchestrator transition authority/state graph/profile schema;
- the simplest successful realization materially changes a cycle-scoped D3 decision rather than remaining equivalent D4 concretization.

These triggers are intentionally narrow. Ordinary entrypoint generation, package plumbing, harness changes, qualification repair, or regenerated descendants remain delegated D4 work when they preserve the accepted D3 contract.
