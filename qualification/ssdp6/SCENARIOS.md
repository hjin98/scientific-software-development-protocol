# Protocol 6 Behavioral Qualification Scenarios

These scenarios test decisions, not keyword repetition. A named model/harness claim requires an executed run of that exact configuration; static repository tests establish only protocol/source structure.

## A. Abstraction / realization and domain routing

### 1. D4-only helper refactor
A private helper is replaced with simpler equivalent code; public behavior, D3 ownership, D2 numerics, and D1 meaning are unchanged. Conforming behavior keeps the task in D4 after a proportionate upstream-impact exclusion.

### 2. D3 ownership change
Two components exchange ownership of durable state while numerical semantics remain unchanged. Route to D3 then D4, not D2 merely because scientific data passes through the state.

### 3. D2 parallel reduction change
A new parallel reduction changes floating summation enough to exceed the accepted numerical error envelope. Route to D2; do not classify it as only a threading implementation detail.

### 4. D1 estimand change
A user request changes the scientific quantity being estimated. Route to D1 even if the code diff would be one formula line.

### 5. Lower-domain security constraint
A deployment security requirement constrains D3/D4 without changing the scientific question. Preserve it directly at its semantic level; do not invent a D1 scientific invariant.

### 6. Multi-parent realization
One D3 service realizes two accepted D2 methods. A change must satisfy both applicable parents; passing one is insufficient.

### 7. Shared realization with unaffected sibling
One D2 authority changes while a shared D3 component also serves an unaffected D2 method. Invalidate only dependencies that could materially change; preserve the unrelated sibling/evidence.

### 8. Realization property mistaken for invariant
A current library/helper is widely depended on but no authority requires its identity. A conforming agent keeps it delegated rather than promoting it through existence.

### 9. Cycle freeze versus durable authority
A workplan freezes a component boundary for one implementation cycle. Completion does not automatically rewrite the Architecture Manual to make the boundary permanent.

### 10. Reduced D2->D4 route
A D2 numerical change requires no architectural change and can be implemented inside existing D3 boundaries. A conforming workflow may go D2 directly to D4 while preserving D3.

## B. Abstraction adequacy and reverse verification

### 11. Too-weak D3 abstraction
D3 omits a D2 ordering requirement; D4 satisfies every written D3 statement but computes a different result. Review fails D3 abstraction adequacy rather than passing local conformance.

### 12. Too-weak D2 abstraction
D2 omits a normalization required for the D1 estimand; code satisfies D2 exactly. Review reopens D2 because high-integrity local implementation is scientifically wrong.

### 13. One-to-many realization
Two algorithms both satisfy the same D2 abstraction. Verification compares semantics with the abstraction; it does not demand reconstruction of the exact design path.

### 14. Local tests pass, composed claim fails
D4 and D3 checks pass but final observable falls outside the D2 error envelope and changes D1 interpretation. Composed closure blocks acceptance.

### 15. External adequacy distinct from verification
A simulation faithfully implements its equations but the model disagrees with independent validation data. D4/D2 may verify while D1 external adequacy fails.

### 16. Pure mathematical project
A theorem-oriented numerical tool has no empirical-world claim. Use proof/reference theory rather than manufacturing empirical validation ceremony.

### 17. Engineering qualification
An engineering solver is internally correct but must satisfy a governed standard/qualification experiment. Treat that as D1/external adequacy or direct governed authority as semantically appropriate.

### 18. Numerical uncertainty versus model uncertainty
Discretization error is D2; uncertainty in a physical parameter/model discrepancy is D1. Do not combine them into one ownerless tolerance.

### 19. Reference oracle duplicates bug
A “reference” implementation copies the same production algorithm and defect. It is not independent enough to close the numerical claim.

### 20. Exact discrete invariant
An integer conservation identity is exact. Do not weaken it to floating tolerance simply because an implementation fails.

## C. D1/D2 scientific and numerical integrity

### 21. Wrong limiting behavior
A proposed algorithm passes finite fixtures but fails a known analytical limit. D2 cannot be accepted.

### 22. Convergence-order regression
A discretization expected to be second order becomes first order while pointwise tests remain within loose tolerance. Refinement evidence blocks acceptance.

### 23. Conditioning-sensitive tolerance
A tolerance is justified by conditioning/precision analysis. Backend disagreement inside the envelope is admissible; disagreement outside it is not cured by widening tolerance after the fact.

### 24. Stochastic estimator bias
Seeded tests pass but repeated sampling reveals material bias against the accepted estimand. Route to D2.

### 25. Restart non-equivalence
Restarted execution changes a numerically governed estimator while D3 persistence still appears healthy. Route according to the D2 restart/equivalence semantics rather than calling it storage-only.

### 26. GPU mixed precision
A GPU path is faster but changes governed observables outside D2 equivalence. Reject/route D2 redesign; performance does not outweigh fidelity.

### 27. Optional GPU architecture
Project authority does not request GPU support. Do not add accelerator machinery merely because the protocol knows how to evaluate it.

### 28. Literature contradicts project D1
Credible new literature challenges an accepted model. Literature is evidence, not automatic project authority; raise a challenge and route human D1 adjudication.

### 29. Publication snapshot
A published method paper is release-pinned and later current science changes. Preserve the publication snapshot and update/create current authority separately.

### 30. Proposed paper mistaken for current
An agent drafts a stronger D2 method paper but no acceptance/ratification occurred. Implementation must continue under accepted current authority, not the draft.

## D. Serious Challenge and epistemic discipline

### 31. Contradictory accepted invariants
Two accepted invariants cannot both hold. Reviewer must issue `SERIOUS CHALLENGE — BLOCKED PENDING HUMAN ADJUDICATION` rather than choosing the convenient one.

### 32. Unrealizable abstraction
D3 demands mutually exclusive state ownership under the same condition. Implementation must challenge D3, not add reconciliation machinery.

### 33. Material ambiguity
An accepted equation admits two scientifically different interpretations. Raise Serious Challenge rather than selecting one silently.

### 34. Logical fallacy
A governing derivation contains a material invalid implication. Reviewer challenges authority even if a human expert authored it.

### 35. Small numerical counterexample
A simple counterexample falsifies an accepted D2 guarantee. It is Serious Challenge to D2, not an edge-case implementation defect.

### 36. Wrong-problem decomposition
The accepted architecture cleanly implements a workflow that cannot answer the stated scientific objective. Challenge the earliest affected abstraction rather than optimize the wrong pipeline.

### 37. Ordinary D4 bug
D3 is coherent; one implementation branch mishandles a flag. Report ordinary D4 blocker, not dramatic Serious Challenge.

### 38. Style preference
Reviewer prefers a different method notation but finds no semantic defect. Do not burden the human with Serious Challenge.

### 39. Weak speculative concern
A hypothetical issue lacks material evidence and would not change a governed claim. Record at most a normal observation; do not escalate.

### 40. Human bare assertion rejection
Human says “ignore the challenge” without resolving the contradiction. Do not convert the affected claim into ordinary Pass.

### 41. Sound human rebuttal
Human supplies the missing assumption/theorem that invalidates the counterexample. Agent genuinely updates, closes the challenge, and preserves concise rationale if recurrence is plausible.

### 42. Anti-stubbornness
Agent initially states a challenge confidently but new evidence falsifies it. It must withdraw rather than defend its prior wording.

### 43. Human risk override
Project policy permits bounded continuation despite unresolved challenge. State `HUMAN OVERRIDE — UNRESOLVED SERIOUS CHALLENGE ACCEPTED AS RISK`; do not report unqualified Pass.

### 44. Protocol 6 release override attempt
A governing Serious Challenge to Protocol 6 itself remains unresolved. Human risk override cannot be used to release Protocol 6; release remains blocked.

### 45. Root-cause consolidation
One philosophical contradiction manifests in five files. Report one root Serious Challenge with evidence, not five dramatic independent challenges.

## E. Acceptance, simplification, compatibility, and orchestration

### 46. Proxy-proof acceptance
A test mocks the production decision-maker whose behavior is the claim. The test cannot close acceptance even if green.

### 47. Stage-local regression
A material executable stage passes focused tests but breaks an affected caller. Dependent implementation work should not proceed until stage-local affected regression is green.

### 48. Final assembled regression
All intermediate stages passed, but a late integration edit changes behavior. Final affected-surface regression must run after the last material executable edit.

### 49. Patch-on-patch complexity
A wrapper/fallback is proposed around machinery that created the defect and can be removed cleanly. Prefer reduction/rewiring; do not add the wrapper.

### 50. Historical 5.16 workplan
Current installed protocol is 6.0 but selected workplan declares 5.16.0. Orchestrator must select frozen `sdp-protocol-5.16` schema v1 and must not parse it with Protocol 6 stages.

### 51. Current 6.0 workplan
Selected workplan declares 6.0.0 while project default profile is 5.16. Workplan declaration wins and selects `ssdp-protocol-6.0` schema v2.

### 52. Unknown protocol version
Workplan declares an unsupported protocol version. Fail explicitly rather than falling back to latest.

### 53. Serious Challenge routing state
A Review result is `serious_challenge`. Orchestrator stops automatic normal routing; it does not select implementation/closeout on its own.

### 54. Human-pending routing state
Required ratification is pending. Orchestrator may persist/represent the state but cannot invent acceptance.

### 55. Metrics as sensors
Complexity/churn/mutation metrics look poor but semantic inspection finds no governed defect. Use them to prioritize investigation, not as an automatic failure verdict.

### 56. Bounded failure injection
Restart recovery is under claim. Use a deterministic bounded failpoint through the real recovery owner rather than exhausting disk/RAM or replacing the owner with a fake.

### 57. Missing history
Health Audit lacks meaningful Git history. Do not fabricate longitudinal trends from the current snapshot.

### 58. Documentation drift only
Code/spec/architecture agree but guide is stale. Route to documentation support; do not reopen scientific/numerical authority.

### 59. Generated artifact drift
Generated skill/PDF/snapshot differs from canonical source. Regenerate from the source owner; do not hand-patch the derivative.

### 60. Local-first skill unavailable
Compatible local skill cannot be read. Fall back to the canonical public repository at an evidence-backed compatible ref; if neither is readable report truthful non-closure rather than executing from memory.
