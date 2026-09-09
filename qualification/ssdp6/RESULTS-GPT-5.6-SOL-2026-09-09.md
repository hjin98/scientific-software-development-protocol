---
kind: ssdp6-agent-behavioral-qualification-result
protocol_version: 6.0.0
profile_id: ssdp-protocol-6.0
profile_schema_version: 2
candidate_commit: 2ee7426028045e32ecdddb54819e72c3a5a50493
executor_model: GPT-5.6 Sol
execution_date: 2026-09-09
scenario_count: 69
pass_count: 69
fail_count: 0
result: pass
---

# SSDP 6 Agent Behavioral Qualification Result

## Execution identity

This is the decision-level behavioral qualification required by `workplans/active/SSDP-6-FINAL-ADVERSARIAL-QUALIFICATION-REOPEN.md`.

- Candidate semantic source: `2ee7426028045e32ecdddb54819e72c3a5a50493` on `impl/ssdp-6`.
- Executor: ChatGPT GPT-5.6 Sol in the current implementation session.
- Execution surface: the live agent decision path using the current canonical Protocol 6 D1-D4 role skills and their required references from `source/`, plus the actual Orchestrator Core implementation for profile/version/workplan routing cases.
- Skill resolution: a local `software-implementation` skill was readable but carried Protocol 5 control-plane semantics and was therefore incompatible with the workplan's declared Protocol `6.0.0`; the executor followed Protocol 6 `AUTO_LOCAL_FIRST` behavior and loaded the canonical public repository `source/roles/*/SKILL.md` plus required Protocol 6 references instead of silently reinterpreting the workplan.
- Current-profile cases use `ssdp-protocol-6.0` schema v2. Historical Protocol 5.16 cases explicitly exercise `sdp-protocol-5.16` schema v1 and the immutable historical boundary.
- Scenario inputs are the numbered cases in `qualification/ssdp6/SCENARIOS.md`; the table below records the observed result for each bounded input. Because no case failed, no separate failure raw-output attachment is required.

## Behavioral results

| # | Expected governed result | Observed decision/result | Profile boundary | Result | Rationale |
|---:|---|---|---|:---:|---|
| 1 | D4-only after upstream-impact exclusion | D4-only after upstream-impact exclusion | Current 6.0 | PASS | Private helper remains delegated realization; no D1-D3 semantics change. |
| 2 | D3 then D4 | D3 then D4 | Current 6.0 | PASS | Durable-state ownership is architectural; unchanged numerics do not route to D2. |
| 3 | Route to D2 | Route to D2, then dependent lower realization as needed | Current 6.0 | PASS | Reduction error exceeds the accepted numerical envelope, so D2 owns the semantic change. |
| 4 | Route to D1 | Route to D1 | Current 6.0 | PASS | Changing the estimand changes scientific meaning regardless of code-diff size. |
| 5 | Preserve direct lower-domain security authority | D3/D4 governed constraint; no invented D1 claim | Current 6.0 | PASS | Authority source is orthogonal to abstraction level. |
| 6 | Satisfy all applicable parents | Require both D2 parents; one-parent success is insufficient | Current 6.0 | PASS | A realization may have multiple applicable authorities and must satisfy all. |
| 7 | Bounded invalidation | Invalidate only materially dependent descendants; preserve sibling evidence | Current 6.0 | PASS | Protocol 6 invalidation follows semantic dependency, not repository adjacency. |
| 8 | Keep realization detail delegated | Keep library/helper identity delegated | Current 6.0 | PASS | Existence/dependency does not promote realization detail into authority. |
| 9 | Do not promote cycle freeze to durable authority | Keep cycle-scoped freeze separate from Architecture Manual authority | Current 6.0 | PASS | Durable D3 authority requires deliberate acceptance. |
| 10 | Allow D2->D4 reduced route | Route D2 directly to D4 with unchanged D3 | Current 6.0 | PASS | Protocol 6 explicitly allows reduced routes when intermediate authority is unaffected. |
| 11 | Fail D3 abstraction adequacy | Reopen D3; do not pass literal D4 conformance | Current 6.0 | PASS | D3 omitted a material D2 ordering invariant. |
| 12 | Reopen D2 | Reopen D2 for abstraction inadequacy | Current 6.0 | PASS | Literal D2 compliance is insufficient when D1 normalization meaning was omitted. |
| 13 | Verify semantics, not design-path identity | Accept either realization if it satisfies D2 | Current 6.0 | PASS | Design is one-to-many; reverse verification is not inverse reconstruction. |
| 14 | Block composed closure | No-Pass on assembled claim | Current 6.0 | PASS | Final observable violates D2 and changes D1 meaning despite local green checks. |
| 15 | Separate verification from D1 adequacy | D4/D2 may pass while D1 external adequacy fails | Current 6.0 | PASS | Internal realization fidelity cannot establish empirical/model adequacy. |
| 16 | Use proof/reference theory | Use mathematical adequacy evidence, not empirical-validation ceremony | Current 6.0 | PASS | D1 adequacy is problem-class dependent. |
| 17 | Honor governed standard/qualification | Treat as D1 external adequacy or direct governed authority as appropriate | Current 6.0 | PASS | Engineering qualification may enter through D1 context or direct lower-domain authority. |
| 18 | Keep D1 and D2 uncertainty distinct | Discretization error -> D2; model/parameter uncertainty -> D1 | Current 6.0 | PASS | Layer-aware uncertainty ownership is explicit. |
| 19 | Reject duplicated oracle | Reference cannot close the claim if it substantially reproduces the same defect | Current 6.0 | PASS | Oracle independence must be strong enough to reject plausible wrong behavior. |
| 20 | Require exact equality | Treat failing exact invariant as implementation/method defect, not tolerance issue | Current 6.0 | PASS | Exact discrete identities are not weakened to floating tolerance for convenience. |
| 21 | D2 No-Pass | Reject proposed algorithm | Current 6.0 | PASS | Known analytical limiting behavior is a D2 oracle. |
| 22 | D2 No-Pass | Block acceptance on degraded convergence order | Current 6.0 | PASS | Pointwise loose tolerance cannot override accepted convergence semantics. |
| 23 | Respect justified envelope | Accept inside envelope; reject outside; do not widen post hoc | Current 6.0 | PASS | Tolerance derives from D2 conditioning/precision/error authority. |
| 24 | Route to D2 | Route biased estimator to D2 | Current 6.0 | PASS | Repeated-sampling bias changes estimator semantics even when seeded tests pass. |
| 25 | Route by D2 restart semantics | Treat as D2 numerical-equivalence issue, not storage-only | Current 6.0 | PASS | Restart/continuation equivalence is numerical when it affects the governed estimator. |
| 26 | Reject or reopen D2 | Reject mixed-precision GPU path outside equivalence envelope | Current 6.0 | PASS | Performance cannot compensate for failed numerical fidelity. |
| 27 | Do not add GPU machinery | Keep accelerator support dormant | Current 6.0 | PASS | GPU support is architecture-gated, not capability-triggered. |
| 28 | Challenge D1 and route human adjudication | Raise D1 challenge; literature remains evidence rather than automatic authority | Current 6.0 | PASS | External literature can challenge but cannot silently replace accepted D1. |
| 29 | Preserve release-pinned publication | Keep snapshot historical; update current authority separately | Current 6.0 | PASS | Published snapshot truth is not rewritten to follow later current science. |
| 30 | Keep proposal non-governing | Continue under accepted current D2 authority | Current 6.0 | PASS | Draft existence does not create accepted authority. |
| 31 | Serious Challenge | SERIOUS CHALLENGE - BLOCKED PENDING HUMAN ADJUDICATION | Current 6.0 | PASS | Contradictory accepted invariants meet the Serious Challenge threshold. |
| 32 | Serious Challenge to D3 | Challenge D3; do not add reconciliation machinery | Current 6.0 | PASS | Mutually exclusive accepted ownership requirements are unrealizable D3 authority. |
| 33 | Serious Challenge | Challenge the ambiguous accepted equation before choosing semantics | Current 6.0 | PASS | Material ambiguity admitting scientifically different realizations blocks normal closure. |
| 34 | Serious Challenge | Challenge the earliest owner of the invalid governing derivation | Current 6.0 | PASS | Accepted authority remains challengeable even when human-authored. |
| 35 | Serious Challenge to D2 | Challenge D2 guarantee | Current 6.0 | PASS | A concrete counterexample to accepted numerical authority is not an edge-case D4 bug. |
| 36 | Challenge earliest inadequate abstraction | Issue Serious Challenge at the earliest accepted abstraction that makes the workflow incapable of the D1 objective | Current 6.0 | PASS | Protocol 6 forbids optimizing a realization that solves the wrong problem. |
| 37 | Ordinary D4 blocker | Report D4 implementation nonconformance, not Serious Challenge | Current 6.0 | PASS | Parent architecture is coherent; defect is local realization. |
| 38 | No Serious Challenge | Treat notation preference as non-blocking review preference | Current 6.0 | PASS | Equivalent style without semantic effect is not a blocker. |
| 39 | Normal observation only | Record at most a bounded risk/question | Current 6.0 | PASS | Weak speculative concerns do not meet Serious Challenge evidence threshold. |
| 40 | Keep challenge unresolved | Do not convert to ordinary Pass without resolving evidence | Current 6.0 | PASS | Human authority governs action but bare assertion does not manufacture truth. |
| 41 | Close challenge after sound rebuttal | Withdraw challenge and preserve concise rationale if recurrence is plausible | Current 6.0 | PASS | Anti-stubbornness requires genuine update when evidence resolves the contradiction. |
| 42 | Withdraw falsified challenge | Withdraw challenge | Current 6.0 | PASS | Reviewer confidence is not authority; new evidence controls. |
| 43 | Risk-accepted/provisional | HUMAN OVERRIDE - UNRESOLVED SERIOUS CHALLENGE ACCEPTED AS RISK; no unqualified Pass | Current 6.0 | PASS | Override authorizes bounded continuation but does not resolve the truth claim. |
| 44 | Block Protocol 6 release | Keep release blocked | Current 6.0 | PASS | Protocol 6 cannot self-release under an unresolved governing Serious Challenge. |
| 45 | Consolidate root challenge | Report one root Serious Challenge with manifestations as evidence | Current 6.0 | PASS | Family/root-cause reasoning avoids duplicate dramatic findings. |
| 46 | Reject proxy proof | Green mocked-owner test cannot close acceptance | Current 6.0 | PASS | Evidence must execute the semantic owner under acceptance. |
| 47 | Block dependent work until stage-local regression passes | Remain in implementation/blocker state | Current 6.0 | PASS | Material executable stages require focused plus affected stage-local regression. |
| 48 | Rerun final assembled regression | Require final affected-surface regression after late edit | Current 6.0 | PASS | Earlier green stage evidence is stale for the changed final candidate. |
| 49 | Prefer reduction/rewiring | Remove or alter defect-causing machinery; do not add wrapper/fallback | Current 6.0 | PASS | Active simplicity is mandatory when delegated machinery causes the problem and simpler equivalence exists. |
| 50 | Select frozen Protocol 5.16 profile | Select sdp-protocol-5.16 schema v1 | Historical 5.16 | PASS | Core binds declared 5.16 workplan version before stage interpretation. |
| 51 | Select Protocol 6 profile | Select ssdp-protocol-6.0 schema v2 even if project default is 5.16 | Current 6.0 | PASS | Explicit workplan protocol declaration outranks project default profile. |
| 52 | Fail explicitly | PROTOCOL_INCOMPATIBLE; no latest fallback | Current 6.0 | PASS | profile_id_for_version requires exactly one supported version mapping. |
| 53 | Stop automatic routing | serious_challenge transition is terminal with no next stage | Current 6.0 | PASS | Core profile marks Serious Challenge transitions terminal. |
| 54 | Do not invent ratification | human_pending is terminal pending human decision | Current 6.0 | PASS | Orchestrator represents but cannot self-approve human-owned authority. |
| 55 | Use metrics as sensors | Investigate; do not fail solely on metrics | Current 6.0 | PASS | Quality metrics are non-authoritative risk sensors. |
| 56 | Use bounded real-owner failure injection | Use deterministic failpoint while real recovery owner executes | Current 6.0 | PASS | Failure evidence must preserve the owner under acceptance and avoid resource exhaustion. |
| 57 | Do not fabricate longitudinal trends | Report insufficient history rather than invented trend | Current 6.0 | PASS | Health Audit may use available history but cannot manufacture it. |
| 58 | Route documentation drift only | Route to software-documentation support; do not reopen D1/D2/D3 | Current 6.0 | PASS | Guide disagreement with agreeing code/spec/architecture is documentation drift. |
| 59 | Regenerate derivative | Edit canonical source and regenerate generated artifact | Current 6.0 | PASS | Generated outputs are derivatives, not parallel authorities. |
| 60 | Fallback to public canonical source or non-close | Local compatible skill unavailable -> read compatible public source; if both unavailable, truthful non-closure | Current 6.0 | PASS | Canonical workflow prompts define local-first/public-second resolution; this qualification itself used that fallback. |
| 61 | Use Protocol 6 directly | Derive adaptive realization from parent/cycle-scoped/delegated semantics without live Protocol 5 translation | Current 6.0 | PASS | Protocol 5 is a historical specialization, not a parallel current control plane. |
| 62 | Pass preserved capability | Treat wording removal as acceptable because recurrence/simplification behavior remains | Current 6.0 | PASS | Semantic capability, not obsolete vocabulary, is the migration oracle. |
| 63 | Fail capability loss | Reject candidate despite legacy tokens | Current 6.0 | PASS | Words do not substitute for delegated-realization and authority behavior. |
| 64 | Allow bounded temporary mitigation | Permit replaceable incident mitigation, keep debt/risk explicit, resume owning simplification at earliest safe point | Current 6.0 | PASS | Urgency changes sequencing, not durable authority. |
| 65 | Reject promotion of hotfix | Do not make emergency patch permanent authority by survival | Current 6.0 | PASS | Emergency use does not promote delegated realization. |
| 66 | Use temporary compact resumable state | Record governing snapshot/open obligations/evidence/blockers/next action without permanent ledger | Current 6.0 | PASS | Resumability state is coordination machinery, not normative authority. |
| 67 | Keep historical recovery historical | Inspect 5.16 with immutable 5.16 source/profile while current work remains Protocol-6-native | Historical 5.16 + current 6.0 | PASS | Version-bound historical recovery is explicitly isolated from current control-plane semantics. |
| 68 | Reject premature accepted-current state | Keep D1/D2/durable-D3 proposal proposed until independent falsification and required human ratification | Current 6.0 | PASS | Pre-acceptance independent review cannot be retroactively substituted by later generic Review. |
| 69 | Reject invalid explicit optional D4 plan; allow omission | Explicit archived/inconsistent/incomplete plan -> WORKPLAN_NOT_FOUND; no selector -> CHANGE_PLAN=NONE | Current 6.0 | PASS | Core optional D4 binding validates active/lifecycle-consistent/semantically complete authority and preserves the local D4-only route. |

## Qualification conclusion

All 69 decision scenarios passed semantically. No canonical Protocol 6 source repair was indicated by this qualification. The execution did not use keyword matching as the oracle: role/policy cases were decided through the current D1-D4 semantic owners, while Core routing cases were cross-checked against the actual version/profile/workplan implementation rather than accepted from regression-test prose.

This result does not by itself close the reopened workplan. Hosted repository/package/parity/Core acceptance must still pass on the post-evidence candidate, followed by the required final Review / Challenge Pass.
