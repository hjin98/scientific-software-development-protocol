---
kind: protocol-qualification-contract
contract_id: SSDP-6.6-EVALUATION-AND-QUALIFICATION-CONTRACT
protocol_version: 6.5.0
target_protocol_version: 6.6.0
governing_workplan: SSDP-6.6-COGNITIVE-OPERATIONAL-OPTIMIZATION
status: proposed
---

# Protocol 6.6 Evaluation and Qualification Contract

This is the cold evaluation/qualification owner for the Protocol 6.6 cycle. Load it only when Stage A defines the evaluation basis, Stage F runs behavioral comparisons, Stage G qualifies the assembled candidate, or Review challenges evidence adequacy. Ordinary Stage B-E implementation does not preload it merely because it is linked or packaged.

It is evidence/acceptance coordination, not D1-D4 authority. Passing it cannot waive a governing Protocol 6.5 semantic obligation.

## 1. Empirical evaluation

Evaluation must determine whether 6.6 reduces real operational burden without trading away semantic protection.

Use a compact development set plus a smaller holdout/adversarial set. A holdout case becomes development data once its result is used to tune the candidate.

Each scenario records a durable initial repository/source snapshot, task, governing authority available to the agent, allowed tools/runtime constraints, intended evidence class, and outcome oracle/assessment route. Historical cases should use pre-solution snapshots and exclude later accepted repairs, review findings, workplans, or memory that leak the answer where practical.

The corpus should include both simplification cases and preservation sentinels. Representative classes include:

- first-clean local D4 repair;
- tolerance/sanity-check issue where research-grade escalation is unnecessary;
- genuine D2 semantic defect;
- architecture redesign or mature mechanism replacement;
- stale/defective evidence instrument;
- recurrence/shared-family repair;
- overengineering and stop-condition traps;
- protocol-version mismatch;
- weak/incorrect abstraction;
- PEM-applicable and PEM-not-applicable cases;
- specialized definition/import/parameter-binding;
- representative security, recovery/concurrency, and release/version cases.

Bind the baseline at two identities:

- canonical semantic source: `7f7b5e24858e813e45ace867a7f8ea5180f43bf0`;
- accepted-current installed/generated package/profile surface: cutover `2b8ce17b1f086dc85e6fa8014c4a7bcc45ef60cb`.

Use canonical source for semantic/source comparisons and the accepted-current generated package surface for discovery/selection/runtime-package comparisons. Do not substitute a stale locally installed approximation or mutable default branch.

Compare candidate 6.6 against the corresponding 6.5 baseline under the same model identity/version, reasoning mode, tool permissions, task snapshot, harness/install mode, and host configuration as practical. Record confounders and counterbalance run order when service/model drift could bias one variant.

Separate execution from assessment. Prefer deterministic owner/external oracles. Otherwise use an independent evaluator/reviewer that did not author the trajectory and, where practical, is blinded to protocol variant. The execution agent's own completion claim is never sufficient correctness evidence.

Measure four layers separately:

0. **catalog discovery/selection**: total exposed skill metadata footprint plus whether the harness selects an admissible SSDP root, avoids materially irrelevant roots, and honors explicit skill selection where supported;
1. **static mandatory-read closure after root selection**: source bytes/tokens and routing depth required by doctrine;
2. **observed active protocol context**: protocol material actually loaded in a live run;
3. **total trajectory behavior**: tool/agent steps, intervention, unnecessary evidence/tests, candidate/review churn, cost, stop behavior, and final outcome.

Selection scenarios define an **admissible root set**, not always one gold label. Include clear D1/D2/D3/D4 tasks, each specialist, mixed-domain tasks where safe rerouting is possible, explicit-skill requests where the harness supports them, and negative/no-SSDP cases. Record missed activation, materially irrelevant activation, and unnecessary multi-skill activation separately.

Static inspection of `description` text can establish size/content properties but cannot prove real harness selection. Live discovery/selection claims require the named harness/model/install mode actually exercised.

Correctness/semantic protection is a feasibility gate. Track final governed outcome, missed authority/affected surface, false acceptance, false/missed Serious Challenge, inappropriate escalation, and historical-capability preservation. Operational and cost signals are optimization evidence only.

A reproducible new substantive correctness/authority/evidence failure on a matched case that 6.5 correctly closes is a blocker unless independent Review establishes the 6.5 result was itself invalid or inapplicable. Aggregate efficiency cannot average away semantic regression.

Acceptance of an operational-improvement claim requires both structural hot-path reduction and bounded live evidence that an intended burden dimension improves without new correctness failure. The effect must be distinguishable from obvious run noise and large enough to justify any new permanent machinery. No universal percentage or composite score is authority.

Keep evaluation proportional. Prefer small high-information cases, repeat stochastic runs only when variance can change the decision, and stop when remaining uncertainty cannot change acceptance/design choice. Experimental helpers, query systems, indexes, subagent orchestration, or context tooling remain removable until evidence shows they materially help. Release qualification may use declared reference agent/runtime environments; these are evidence environments, not downstream runtime dependencies.

Preserve enough provenance to interpret live runs: exact protocol source, task snapshot, model/runtime identity as exposed, reasoning/configuration mode, tool permissions/versions where material, and trace/result artifacts or explicit host limitations.

## 2. Qualification counterfactuals

### Discovery, selection, kernel, and routing

Challenge at least:

- a clear D1/D2/D3/D4/specialist task whose admissible root is not selected;
- generic descriptions becoming so broad that unrelated/no-SSDP tasks spuriously activate skills;
- mixed-domain task being falsely failed because the evaluator insists on one arbitrary root despite safe internal rerouting;
- selection descriptions carrying detailed child doctrine or mutable accepted-version/release state;
- OpenAI-specific adapter metadata accidentally becoming a generic package-validity requirement;
- a live-selection claim inferred from static description inspection or from a different harness/model/install mode;

- local D4 work accidentally loading formal-semantics/PEM/history detail;
- specialized mathematical/import work whose cold semantic owner is unreachable;
- specialized semantic use occurring while the exact owner meaning is only discoverable, not loaded for inference;
- shortened routing that actually deletes a mandatory capability;
- duplicated local doctrine disagreeing with the canonical owner;
- cold resources correctly packaged for transport but treated as active merely because bundle membership/linkage exists.

### Representation and transient state

Challenge:

- compact handoff omitting an open blocker or reopen condition;
- Working State declaring acceptance;
- stale checkpoint reused after protocol/workplan/candidate/regime change;
- workplan mutation caused only by transient progress.

### Project memory

Challenge:

- first clean defect loading full PEM;
- relevant COLD entry hidden by summary;
- query/index output treated as canonical memory;
- stale authority-bound capability;
- simplified agent-facing memory guidance losing counterevidence/base/overlay protections.

### Cognitive resources and independent trajectories

Challenge:

- incidental child work inheriting maximal model/subagent treatment from a high-stakes parent;
- consequential unresolved uncertainty failing to escalate when an applicable capability exists;
- SSDP duplicating trustworthy host automatic resource routing without decision value;
- subagents sharing author conclusions while being described as independent;
- same-model/same-oracle common mode being mistaken for evidentiary independence;
- contradictory findings resolved by vote rather than evidence/owner adjudication.

### Review and convergence

Challenge:

- repeated related findings emitted one per cycle despite clear common cause;
- recurrence automatically forcing redesign where a clean local repair remains sufficient;
- family/review count used as pass/fail authority.

### Version, package, and profile/control boundary

Challenge:

- generic skill bundle being invalidated solely because a vendor adapter is absent/broken when the generic core remains valid;
- a named vendor adapter silently changing generic semantic ownership instead of only discovery/interface behavior;

- 6.5 skill used for explicit 6.6-bound work without resolving compatible source;
- 6.6 silently reinterpreting frozen 6.4/6.5 work;
- repository default/latest substituted for exact mapping;
- unversioned ordinary task paying needless remote source lookup;
- 6.6 prompt/profile regeneration changing orchestrator transition/control semantics or profile schema without D3 reopen;
- generated checkpoint/summary becoming required authority for manual/portable operation.

### Evaluation epistemology

Challenge:

- static token/byte reduction claimed as live productivity improvement;
- synthetic fixture claimed as semantic adequacy proof;
- execution agent self-grading success;
- later solution/review/memory leakage into a historical snapshot;
- tuned holdout still presented as unbiased;
- benchmark result waiving a correctness blocker;
- harness overfit to one model/runtime;
- apparent gain smaller than run variance or outweighed by new permanent machinery;
- evaluation continuing after remaining uncertainty cannot change the decision.

## 3. Final qualification boundary

Before independent Review, qualification must establish that:

- every accepted 6.5 capability is preserved at a current owner/route or reviewed equal-or-stronger generalization;
- accepted 6.5 discovery/selection portability capability is preserved: generic metadata remains sufficient for reliable root discovery in tested environments, live claims are environment-bound, and selection failure is distinguished from reference-routing failure;
- inherited repository/package/profile/Core/frozen-history checks pass where applicable;
- generic core validation remains distinct from named vendor-adapter validation;
- discovery/selection, transport closure, and internal activation are qualified as distinct stages;
- transport closure remains complete while membership/hyperlinks do not imply activation;
- ordinary routes have a clear structural hot-path reduction plus bounded live evidence of real burden reduction;
- specialized/high-risk sentinels still recover all applicable cold semantics, including source/context availability;
- transient/generated/eval/memory-query views remain non-authoritative;
- manual/portable use remains complete without hidden runtime state or mandatory orchestrator/service;
- version/source mismatch handling follows existing authority;
- 6.6 profile/snapshot changes preserve pre-7 lifecycle/control semantics/schema absent explicit D3 reopen;
- no Serious Challenge or material preservation gap remains.

This contract establishes only the properties its oracles actually discriminate. Fresh independent assembled-candidate Review remains required for semantic adequacy.
