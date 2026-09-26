---
kind: protocol-minor-revision-workplan
workplan_id: SSDP-6.6-COGNITIVE-OPERATIONAL-OPTIMIZATION
protocol_version: 6.5.0
target_protocol_version: 6.6.0
status: reviewed-implementation-ready
created_date: 2026-09-26
reviewed_date: 2026-09-26
workplan_review_state: PASS_NONINDEPENDENT
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

Skill/frontmatter and host-adapter descriptions are activation interfaces, not miniature protocol summaries. Keep them sufficient to route correctly, but do not duplicate child doctrine there. Prefer direct role -> concern-owner activation when the predicate is already knowable; an added routing hop must narrow the question or add material semantics rather than exist for taxonomy alone.

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

## 6. Empirical protocol-evaluation flywheel

### 6.1 Purpose

Protocol evolution SHALL gain bounded empirical evidence about whether protocol changes improve actual agent trajectories. Evaluation is evidence, never D1-D4 authority and never an automatic acceptance oracle.

The initial 6.6 corpus should include representative immutable/reconstructible scenarios drawn from project history plus synthetic counterfactuals where useful:

- first-clean local D4 defect;
- numerical-tolerance/sanity-check defect where research-grade escalation is unnecessary;
- genuine D2 semantic defect requiring escalation;
- architecture redesign;
- mature mechanism replacement;
- defective/stale evidence instrument;
- stale prior evidence;
- recurrence/shared-family repair;
- overengineering trap;
- stop-condition/opportunity-cost trap;
- protocol-version mismatch;
- workplan with deliberately weak/incorrect abstraction;
- PEM-applicable and PEM-not-applicable cases.

Each eval scenario should have a durable manifest containing the initial repository/source snapshot, task statement, governing authority available to the agent, allowed tools/runtime constraints, intended evidence class, and outcome oracle/assessment route. Historical cases should use pre-solution snapshots and exclude later accepted repairs, workplans, review findings, or memory entries that would leak the answer where practical. Synthetic cases may test routing/behavior but cannot establish universal engineering-outcome superiority.

The corpus should include both simplification opportunities and **preservation sentinels** where deep/cold doctrine is genuinely necessary, including representative semantic-definition/import/parameter-binding, scientific/numerical, security/recovery/concurrency, and release/version cases chosen from the preservation map. The goal is high-information coverage, not one fixture per clause.

### 6.2 Comparison discipline

Before semantic optimization begins, freeze a compact **development set** used for diagnosis/refinement and a smaller **holdout/adversarial set** used only after candidate behavior is substantially stable. Historical task snapshots should avoid later-solution leakage where practical.

For claims about protocol-caused behavioral improvement, compare candidate 6.6 against the exact accepted 6.5 source identity `7f7b5e24858e813e45ace867a7f8ea5180f43bf0`, not a stale installed approximation, under the same model identity/version, reasoning mode, tool permissions, task snapshot, and host configuration as practical. Record deviations that can confound interpretation. Counterbalance/alternate run order when temporal service/model drift could bias one variant.

Execution and outcome assessment must be separated enough to avoid self-confirmation. Prefer deterministic external/owner-based oracles where available; otherwise use an independent evaluator/reviewer that did not author the trajectory and, where practical, is blinded to which protocol variant produced it. The execution agent's own completion claim is never sufficient evidence of correctness.

A holdout/adversarial case becomes development data once its result is used to tune the candidate; do not continue calling it holdout. Replace or reserve fresh cases when further unbiased discrimination is still needed.

Use three distinct measurement layers:

1. **static mandatory-read closure** — source bytes/tokens and routing depth required by doctrine for a declared task class;
2. **observed active protocol context** — protocol material actually loaded during a live trajectory;
3. **total trajectory behavior** — tool/agent steps, interventions, tests/evidence work, candidate/review churn, cost, and final outcome.

Do not substitute layer 1 for layers 2-3 when claiming live behavioral improvement.

Measure at least:

**Correctness / semantic protection**
- final governed outcome;
- missed applicable authority;
- false acceptance;
- missed affected surface;
- false/missed Serious Challenge;
- inappropriate upward escalation;
- preservation of historical capability.

**Operational behavior**
- active protocol context loaded;
- routing/reference reads;
- tool/agent steps;
- unnecessary tests/evidence work;
- workplan/review amendment churn;
- candidate/review cycles;
- unnecessary architecture/process introduced;
- human interventions where measurable;
- completion/stop behavior.

**Cost signals where available**
- model tokens/compute;
- wall time;
- external tool cost.

No single score is protocol authority. Correctness/semantic preservation are feasibility gates; operational metrics are optimization evidence among semantically admissible candidates.

**Behavioral non-regression rule:** a reproducible new substantive correctness/authority/evidence failure on a matched case that 6.5 correctly closes is a 6.6 blocker unless independent review establishes that the 6.5 result itself was invalid/inapplicable. Aggregate efficiency cannot average away a semantic regression.

**Operational-improvement rule:** acceptance requires both (a) structural reduction of the declared ordinary hot path and (b) at least bounded live trajectory evidence that one or more intended burden dimensions actually improve without a new correctness failure in the evaluated regime. The improvement must be distinguishable from obvious measurement noise and large enough to justify any new permanent machinery it introduces. No universal percentage or composite score is authority; report per-case tradeoffs and uncertainty.

### 6.3 Evaluation economy, reversibility, and anti-overfitting

The eval system SHALL obey the same proportional-rigor doctrine it measures.

- Prefer a compact high-information corpus over a huge benchmark campaign.
- Separate qualification fixtures from at least some holdout/adversarial cases where practical.
- Do not tune prose solely to a named model's quirks when the capability can be expressed portably.
- Repeat stochastic runs only when variance can change the decision.
- Do not claim universal productivity/intelligence improvement from static token/byte metrics.
- A structural hot-path reduction claim requires structural evidence; a behavioral trajectory claim requires live agent evidence; an engineering-outcome claim requires outcome evidence.
- Stop evaluation when remaining uncertainty cannot change acceptance or design choice.
- Experimental helpers, indexes, memory-query commands, context tooling, or subagent orchestration SHALL remain removable until evidence shows they materially reduce burden or protect a governing capability. Delete/decline them when they merely move complexity from prose into machinery.
- Evaluation infrastructure itself is subject to minimum justified complexity; prefer existing repository tests/scripts and small task fixtures before introducing a framework.
- Release qualification may use one or more explicitly declared reference agent/runtime environments; this evidence is versioned evidence for the release, not a runtime dependency imposed on downstream SSDP users.
- Preserve enough provenance to interpret live runs: exact protocol source, task snapshot, model/runtime identity as exposed, reasoning/configuration mode, tool permissions/versions where material, and trace/result artifacts or explicit limitations when the host does not expose them.

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
- build/package/profile/snapshot generation and corresponding tests, including `protocol-manifest.json`/host-adapter metadata and the distinction between transport closure and activation;
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
4. Measure current static mandatory-read closure and, where practical, observed active protocol context for representative routes.
5. Freeze the compact development and holdout/adversarial eval sets plus their claim boundaries before optimizing the protocol.

**Gate:** no semantic source mutation until the memory-basis disposition, preservation obligations, baseline measurements, and eval-set identities are reviewable.

### Stage B — Kernel and routing reduction

1. Extract conditional semantic-definition/traceability material from the universal hot path.
2. Reduce role/specialist entrypoints to bounded routers/contracts.
3. Deduplicate generic doctrine to canonical owners plus local micro-invariants.
4. Rework workflow prompt representation toward invariants/boundaries/acceptance/escalation rather than procedural itineraries while retaining a complete manual/portable route.
5. Verify every moved capability remains discoverable from every materially applicable entrypoint.
6. Verify **transport closure separately from activation**: cold referenced owners required by a packaged skill must remain present/reachable in the bundle, while package membership or ordinary hyperlinks must not make them eagerly active.
7. Prefer deletion/extraction over adding new routing layers; a shorter file graph that requires more hops/inference is not an improvement.

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

1. Run structural context/routing comparisons.
2. Run selected live 6.5-vs-6.6 agent trajectory comparisons under matched environments where practical.
3. Inspect failures qualitatively; do not optimize a scalar score.
4. Remove or revise 6.6 machinery that adds cognitive/process burden without demonstrated semantic or operational value.
5. Repeat only the affected high-information cases after repair.

### Stage G — Final assembled acceptance

Run the repository's inherited source tests, PEM checks when applicable, package validation, generated-dist parity, profile/snapshot/Core checks, exact-ref/source-resolution checks, and new 6.6 qualification.

Additionally verify:

- universal hot path is materially smaller than 6.5 for designated ordinary routes;
- no accepted capability lacks a reachable activation path;
- package transport closure remains complete while package membership/hyperlinks do not imply activation;
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

## 10. Qualification and falsification matrix

At minimum include counterfactuals for:

### Kernel/routing
- a local D4 task that accidentally loads semantic-definition/PEM/history detail;
- a specialized mathematical/import task whose cold semantic-definition owner becomes unreachable;
- a specialized object that is discoverable but improperly used without loading the exact owner meaning required by the inference;
- a route shortened by deleting a mandatory capability rather than moving it;
- duplicate local doctrine disagreeing with its canonical owner;
- a cold resource correctly packaged for transport but accidentally treated as active merely because bundle membership/linkage exists.

### Representation/state
- a compact handoff that omits an open blocker/reopen condition;
- Working State declaring acceptance without canonical authority;
- a stale checkpoint reused after candidate/workplan/protocol change;
- workplan churn caused only by transient progress.

### PEM
- local first defect incorrectly activating full PEM;
- relevant COLD entry hidden by a compact summary;
- query/index output treated as canonical memory;
- authority-bound capability whose owner binding is stale;
- simplified agent-facing memory guidance that loses counterevidence/base/overlay safety.

### Cognitive-resource routing
- high-stakes parent causing maximal reasoning/subagents for an incidental child;
- materially uncertain high-consequence decision never escalating despite host capability;
- SSDP duplicating a trustworthy host's automatic resource routing without decision value;
- multiple subagents sharing author conclusions while being called independent;
- separate-context agents sharing a common model/oracle being treated as fully independent when the claim depends on evidentiary independence;
- contradictory independent findings resolved by vote rather than evidence/owner adjudication.

### Review/convergence
- repeated related findings emitted one per cycle despite clear family/common cause;
- recurrence causing automatic architecture redesign where a clean local repair remains sufficient;
- family/review count being used as pass/fail authority.

### Version coherence
- installed 6.5 skill used on explicit 6.6-bound work without resolving compatible source;
- 6.6 skill reinterpreting frozen 6.4/6.5 work;
- repository default/latest substituted for an exact version mapping;
- unversioned ordinary task paying unnecessary remote lookup cost.

### Evaluation epistemology
- static byte/token reduction claimed as productivity improvement;
- synthetic fixtures claimed as proof of semantic adequacy;
- execution agent self-grading its own success with no independent/owner oracle;
- later solution/review/memory leakage into a historical task snapshot;
- a tuned holdout case still being represented as unbiased holdout evidence;
- benchmark score used to waive a correctness blocker;
- eval harness overfitted to one named model/runtime;
- apparent efficiency gain smaller than obvious run variance or outweighed by new permanent machinery;
- evaluation campaign continuing after remaining uncertainty cannot change the decision.

### Profile/control-plane boundary
- 6.6 prompt/profile regeneration changing orchestrator transition semantics or control schema without D3 reopen;
- a generated runtime summary/checkpoint becoming required authority for manual/portable execution;
- 6.6 introducing hidden state that Protocol 7 is supposed to own only after its separate major-version architecture acceptance.

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
13. package transport closure and activation remain distinct and mechanically/semantically qualified after reference extraction;
14. live evaluation uses durable scenario/provenance identities and an outcome assessment route independent enough that execution-agent self-assertion cannot manufacture non-regression;
15. 6.6 profile/snapshot changes preserve current pre-7 lifecycle/control semantics and schema unless a reviewed D3 reopen explicitly changes the version boundary.

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

Two adversarial, non-independent workplan review passes have been incorporated into the current text. Review chronology remains recoverable in Git rather than accumulating as binding amendment prose here.

Current disposition:

```text
SERIOUS CHALLENGE: NONE
WORKPLAN REVIEW: PASS_NONINDEPENDENT_R2
IMPLEMENTATION: READY SUBJECT TO NORMAL IMPLEMENTATION-TIME DISCOVERY
```

This review does not substitute for the fresh independent assembled-candidate Review required before Protocol 6.6 acceptance.
