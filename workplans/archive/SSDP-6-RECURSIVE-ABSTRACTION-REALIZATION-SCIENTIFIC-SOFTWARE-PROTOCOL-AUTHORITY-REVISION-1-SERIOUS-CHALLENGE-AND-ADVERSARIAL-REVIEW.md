---
kind: protocol-major-revision-authority-amendment
amends_workplan: SSDP-6-RECURSIVE-ABSTRACTION-REALIZATION-SCIENTIFIC-SOFTWARE-PROTOCOL
protocol_version: 5.16.0
target_protocol_version: 6.0.0
status: accepted-amendment
created_date: 2026-09-08
base_parent_commit: e00bb0d8f40f98c03c37dc03c4418b99c968338c
authority_entrypoint: workplans/active/SSDP-6-AUTHORITY.md
---

# SSDP 6.0 Authority Revision 1 — Serious Challenge and Adversarial Review Doctrine

## 1. Purpose and authority

This amendment is part of the current SSDP 6 transition authority identified by `SSDP-6-AUTHORITY.md`. It amends the parent workplan's review, verification, authority-state, human-adjudication, and narrowly related authority-clarification semantics without changing the accepted D1-D4 decomposition or recursive abstraction-realization model.

The failure mode it forbids is epistemic compliance: a reviewer discovers strong evidence that an accepted abstraction is false, contradictory, materially ambiguous, incomplete, fallacious, or unrealizable, but suppresses the defect merely because the abstraction is already settled.

Accepted authority controls mutation and realization. It is not immune from evidence-based challenge.

## 2. Governing epistemic invariant

```text
Authority governs what the project has accepted, who may mutate it, and what may be acted upon.
Authority does not manufacture correctness.

Empirical scientific claims remain answerable to reality and evidence in their context of use.
Mathematical/theoretical claims remain answerable to formal validity, assumptions, and justified reference theory.
Engineering claims remain answerable to governed requirements, constraints, and evidence.

Humans, agents, papers, workplans, architecture, specifications, code, and tests are instruments
for recovering, expressing, realizing, and checking those truths; none is infallible merely by status.

Evidence may challenge accepted authority.
No actor may counterfeit closure by suppressing a material contradiction because the contradicted
statement is settled or inconvenient to reopen.
```

The final workflow adjudicator for a consequential epistemic dispute is the human researcher or other explicitly designated human domain authority/committee. Human adjudication supplies stable accountable governance; it does not convert unsupported assertion into scientific, mathematical, or engineering truth. An agent challenge is likewise not correct merely because it is confident, elaborate, or accompanied by many sources.

## 3. Mandatory bounded Challenge Pass

Every **material Review or verification/acceptance boundary** shall include a bounded adversarial **Challenge Pass** before normal closure. This includes D4->D3, D3->D2, D2->D1, D1 external-adequacy review, protocol self-review, and any equivalent material acceptance boundary.

Operational independence or a fresh review context is preferred for substantial/high-risk claims when practical, but independence is not a prerequisite for the duty to challenge a serious defect. A role that discovers serious contradictory evidence during design, implementation, self-check, or any other activity must surface it even if a separate Review stage has not yet begun.

For this doctrine, a review/acceptance claim is **material** when a wrong conclusion could plausibly alter acceptance of a governing scientific/mathematical claim, numerical guarantee/error envelope, public or governed contract, architecture/ownership decision, safety/security/reliability requirement, significant resource/compatibility constraint, or release/production decision. Tiny local details with no plausible effect on those claims remain proportionate low-risk work.

The Challenge Pass asks whether the governing authority appears:

- internally consistent;
- sufficiently unambiguous to admit meaningful verification;
- jointly realizable under all applicable upstream and domain-local constraints;
- logically and mathematically coherent;
- adequate for the scientific, theoretical, or engineering claim it governs;
- complete enough to preserve material upstream semantics into the child abstraction;
- compatible with simultaneously applicable authorities;
- free from a material counterexample, contradiction, or fallacious inference known to the reviewer.

For tiny/local low-risk work the pass may be implicit and very short. It is a reasoning obligation, not a mandatory standalone workflow stage, checklist, or report.

## 4. Serious Challenge threshold

A **Serious Challenge** is reserved for a material potential defect in accepted authority. It is not the label for ordinary realization nonconformance or design preference.

Raise a Serious Challenge when there is specific, independently reasoned evidence for one or more of the following:

1. **Unrealizable abstraction** — no admissible realization appears capable of satisfying the accepted invariants and applicable constraints simultaneously.
2. **Contradictory invariants** — accepted requirements cannot all be true or satisfied together in the governed regime.
3. **Material ambiguity** — materially incompatible interpretations are possible, so correctness cannot be established without choosing hidden semantics.
4. **Logical inconsistency or fallacy** — a governing inference, derivation, proof step, premise, definition, or requirement contains a material logical defect.
5. **Mathematical/numerical counterexample** — an analytical, limiting, dimensional, convergence, conditioning, reference-method, or explicit counterexample contradicts the accepted abstraction.
6. **Scientific/model contradiction** — credible empirical, theoretical, literature, or domain evidence materially conflicts with the accepted formulation, validity regime, interpretation, or conclusion.
7. **Abstraction inadequacy** — a child abstraction omits/weakens an upstream invariant so local checks can pass while the composed claim is false.
8. **Authority conflict** — multiple applicable accepted authorities impose incompatible semantics with no existing precedence/adjudication that resolves them.
9. **Major conceptual/philosophical defect** — the governing decomposition, objective, definition, or model is materially self-defeating or solves the wrong problem and cannot be repaired as local realization detail.
10. **Counterfeit-closure requirement** — normal compliance would require hiding, rationalizing, documenting around, or weakening evidence of a material contradiction.

Do **not** raise a Serious Challenge merely because another equivalent realization is preferred, wording could be improved without semantic effect, a speculative alternative may be better, evidence is weak or remote, an ordinary lower-layer implementation defect exists under a coherent parent, or an unrelated future improvement can be imagined.

The threshold is deliberately high: challenge truth-risk, not human attention.

## 5. Evidence quality before escalation

A Serious Challenge must be inspectable rather than rhetorical. Before escalation, separate:

- **observed facts / executable observations**;
- **external source claims**;
- **reviewer inference/derivation**;
- **assumptions needed for the inference**;
- **uncertainty, applicability limits, and known counterevidence**.

For material external factual, literature, standards, API, or contemporary claims, verify the relevant claim against a primary, canonical, or otherwise suitably authoritative/current source when practical. Source count is not independent corroboration when several sources repeat one underlying claim. Do not escalate a Serious Challenge solely from vague model memory, rhetorical confidence, an unverified paraphrase, or the prestige of a source whose claim does not actually apply.

A direct mathematical contradiction, executable counterexample, or internally demonstrable inconsistency does not require external sourcing merely for ceremony. Evidence requirements should match the type of claim.

When evidence is plausible but not yet strong enough for Serious Challenge, report it as an ordinary risk/question and identify the cheapest discriminating check rather than overstating certainty.

## 6. Mandatory output when active

An active Serious Challenge must appear before ordinary `BLOCKERS`, findings, or Pass/No-Pass prose with a first-line status equivalent to:

```text
SERIOUS CHALLENGE — BLOCKED PENDING HUMAN ADJUDICATION
```

When the evidence specifically points to an upstream redesign:

```text
SERIOUS CHALLENGE — CONSIDER REDESIGN / UPSTREAM AUTHORITY REOPEN
```

The exact typography is delegated. Prominence and blocking semantics are not.

The challenge must identify:

1. **Challenged authority** — domain, artifact, invariant/claim, and scope.
2. **Why serious** — the concrete contradiction, impossibility, ambiguity, fallacy, counterexample, or truth-risk.
3. **Evidence/reasoning** — facts/sources/inference/assumptions sufficient for human inspection.
4. **Consequence if correct** — affected realizations, evidence, descendants, conclusions, or product claims.
5. **Suggested resolution direction** — advisory clarification, redesign, revised assumption, stronger oracle, alternative formulation, or experiment.
6. **What would resolve/falsify the challenge** — the discriminating evidence or reasoning that would make the current authority defensible.

Consolidate multiple manifestations of one root defect into one Serious Challenge unless they genuinely have independent causes.

## 7. Serious Challenge versus ordinary blocker

```text
accepted abstraction is coherent;
realization fails to satisfy it
    -> ordinary BLOCKER / realization nonconformance

accepted abstraction itself may be materially wrong, contradictory,
ambiguous, incomplete, fallacious, or unrealizable
    -> SERIOUS CHALLENGE / human adjudication required
```

A review may contain both. A Serious Challenge blocks normal unqualified `Pass` for the affected claim until resolved. It does not automatically declare the challenged authority false.

## 8. Upstream authority is challenged, not silently mutated

During bottom-up realization -> abstraction verification, a Serious Challenge must not cause the reviewer to:

- silently rewrite the accepted invariant to make the realization pass;
- treat downstream realization as retroactive authority;
- relax tolerance, add exception/wrapper/fallback, or rewrite documentation merely to route around the contradiction;
- mark a proposed replacement as accepted current before adjudication.

Preserve the accepted authority as the explicit challenged baseline. If redesign is accepted, reopen the earliest/highest materially affected abstraction and invalidate only dependent descendants.

Unless an explicit human risk override is active, **dependent realization/acceptance work shall not proceed as though the challenged claim were settled**. Work may continue only where it is independent of the challenged surface or is itself the bounded derivation, experiment, reference comparison, prototype, or probe needed to resolve the challenge.

Existing descendant tests, calculations, benchmarks, or documents may remain useful observational evidence, but their ability to close the challenged semantic claim is suspended until the challenge is resolved or explicitly risk-overridden. Do not destroy still-useful evidence merely because its interpretation is provisional.

## 9. Human adjudication

The designated human adjudicator evaluates the challenge with the agent's evidence and reasoning. Normal outcomes are:

### 9.1 Challenge accepted

Reopen the earliest affected authority, revise it through proposed -> review/falsification -> required human ratification -> accepted-current transition, invalidate dependent descendants, and re-realize/re-verify proportionately.

### 9.2 Challenge rejected with satisfactory reasoning/evidence

The human demonstrates a false premise, missing governing assumption, misapplied theorem/model, invalid counterexample, misunderstood domain condition, applicable precedence rule, or other reason the alleged contradiction does not hold.

The agent must genuinely reconsider the challenge. If the rebuttal resolves it, close the challenge and resume normal Review. Record the **material resolution rationale** durably near the challenged authority or in its canonical rationale when doing so prevents a plausible recurrence. Keep that record concise and scoped rather than preserving the full conversation.

A resolved challenge record need only preserve the challenged claim/scope, resolution state, and material reasoning needed to prevent recurrence. Do not create a separate challenge database or permanent review transcript solely for this purpose.

### 9.3 Authority clarified or revised

If the intent was sound but the accepted invariant was materially ambiguous/incomplete, any clarification that changes the admissible realization set is an authority mutation, not editorial cleanup. Route it through the owning domain and invalidate dependent evidence as necessary.

### 9.4 More evidence required / adjudication deferred

The affected claim remains blocked. Identify the smallest disputed premise and the cheapest discriminating derivation, experiment, proof, primary reference, expert judgment, reference-method comparison, or implementation probe likely to resolve it.

### 9.5 Explicit human risk override

When safety/project rules permit, the human may direct bounded work to proceed despite an unresolved challenge. Preserve a status equivalent to:

```text
HUMAN OVERRIDE — UNRESOLVED SERIOUS CHALLENGE ACCEPTED AS RISK
```

This is authorization to proceed, **not epistemic resolution**.

Any descendant artifact or evidence whose validity depends on the challenged claim is **risk-accepted/provisional with respect to that claim**. It may support bounded continued work, experiments, or preparation, but it must not:

- be used to close the challenged claim;
- silently supersede the challenged authority;
- be represented as ordinary accepted-current scientific/numerical/engineering closure;
- propagate an unqualified `Pass` downstream.

Unaffected claims may still close normally. The risk marker follows only the dependent semantic surface.

A project/product release may proceed under an explicit visible risk-accepted classification only where project policy permits and every independently binding release/safety/compliance requirement is still satisfied. **The SSDP 6 protocol itself may not use risk override to satisfy its own final release acceptance criteria.** An unresolved Serious Challenge to governing Protocol 6 authority blocks Protocol 6 release until resolved because the parent workplan requires final review with no genuine blocking defect.

## 10. Durable domain authority versus cycle-scoped realization freeze

The parent workplan's durable D1-D4 documentation authority and its generalized Protocol 5 `Frozen` concept are related but not identical.

- **Accepted-current domain authority** is the durable current D1/D2/D3/D4 semantic record. It remains current until explicitly superseded through its owning authority.
- **Cycle-scoped realization freeze** is the subset of solution decisions a specific change plan deliberately fixes to bound one realization cycle. It constrains that cycle but does not become durable domain authority merely because it was frozen in a workplan.

A cycle-scoped decision becomes part of the durable current Scientific Method Paper, Numerical/Algorithmic Method Paper, Architecture Manual, or D4 Specification only when the owning domain explicitly accepts it as a current semantic claim that should govern future work.

Conversely, a workplan must not treat durable current D1-D4 authority as optional merely because it was not restated in the cycle freeze. The cycle freeze is a bounded child-realization contract inside the larger current authority set, not a replacement for that set.

This clarification preserves Protocol 5's useful implementation-cycle bounding without turning transient realization choices into permanent science, numerical method, architecture, or specification truth.

## 11. Single semantic owner versus multiple applicable authorities

The parent's rule that each material claim has exactly one current normative semantic owner prevents duplicated/competing ownership. It does **not** mean a realization may have only one governing authority.

A concrete realization can simultaneously be constrained by:

- one or more upstream domain claims;
- domain-local governed external constraints;
- safety/project/stakeholder/regulatory/public-contract authority;
- ratified current domain decisions.

Each individual claim should have one normative owner/source; the realization must satisfy **all applicable claims**. Do not copy an external governed contract into a D1/D2/D3/D4 document merely to manufacture local ownership. Domain documents should reference or incorporate its applicability without usurping the external source unless the project explicitly adopts a derived domain claim.

If two applicable authorities genuinely conflict, route the conflict through the Serious Challenge/adjudication path rather than inventing duplicate ownership or silently choosing one.

## 12. Snapshot-complete transition handoff

`workplans/active/SSDP-6-AUTHORITY.md` is the canonical composition entrypoint for this transition. Supplying only the parent workplan while omitting an accepted amendment listed by that index is **not** snapshot-complete SSDP 6 transition authority.

Agents asked to execute or review this SSDP 6 parent workplan should resolve the authority index first when it is available. No chat history or Git-history archaeology is required or authoritative once the listed current files are supplied.

This is transition scaffolding only. Before Protocol 6 release, fold these semantics into the minimum canonical Protocol 6 role/reference owners so released operation does not depend on a parallel amendment/index layer.

## 13. Anti-deference, anti-stubbornness, and debate convergence

### Anti-deference

Do not suppress a serious contradiction because a human expert wrote it, a workplan was accepted, a paper/manual states it confidently, reopening is expensive, implementation has already invested in it, prior reviewers missed it, or the user appears to expect a Pass.

### Anti-stubbornness

Do not preserve a challenge merely because the reviewer stated it confidently, changing position feels inconsistent, or new context contradicts the reviewer's first model. Update the conclusion when evidence/reasoning actually resolves the issue.

### Convergence

A Serious Challenge is not an unlimited conversational veto. Once repeated debate adds no new evidence, stop restating the same arguments. Isolate the smallest unresolved premise and route to a discriminating experiment, formal derivation, primary/canonical source, additional designated human/domain expert, or explicit risk-override state. Preserve unresolved status honestly rather than cycling indefinitely.

## 14. Constructive adversarialism

Material Review should default to constructive adversarialism rather than compliance checking. Actively attempt, proportionately, to find:

- the smallest counterexample to an important invariant;
- hidden assumptions required for realizability;
- mutually incompatible requirements;
- materially different interpretations of ambiguous wording;
- a realization that passes local checks while violating upstream meaning;
- evidence that the accepted decomposition solves the wrong problem;
- oracle weaknesses that permit incorrect claims to survive;
- authority that appears copied from the current realization rather than independently justified.

The objective is not objection production. It is to maximize discovery of high-consequence defects before they are deeply realized. Style preferences, speculative alternatives, and low-value questions remain ordinary review material, not Serious Challenges.

## 15. Recursive application

The rule applies at every authority boundary:

```text
D4 -> D3:
    architecture contains an impossible/contradictory ownership requirement
    -> challenge D3

D3 -> D2:
    software decomposition cannot preserve accepted estimator/solver semantics
    -> challenge D2

D2 -> D1:
    numerical analysis exposes a contradiction in the accepted mathematical/scientific target
    -> challenge D1

D1 -> external adequacy:
    governing model conflicts with decisive empirical/theoretical/engineering evidence
    -> challenge D1 / human adjudication

Protocol self-review:
    the governing protocol doctrine is materially inconsistent or unrealizable
    -> challenge the protocol parent authority
```

A serious flaw discovered from a lower review scope must route upward to the earliest potentially wrong authority rather than being artificially contained in the original scope.

## 16. Workflow and orchestrator representation

SSDP 6 workflow/profile semantics must be able to represent an unresolved Serious Challenge without making the orchestrator an epistemic authority. It may need outcomes/states equivalent to:

```text
serious_challenge
human_adjudication_pending
challenge_resolved
human_risk_override
risk_accepted_provisional
```

Exact field/outcome names and whether they are stage results, authority states, or Tracker projections are delegated to profile design.

The orchestrator may persist/route the state and prevent counterfeit normal closure. It must never decide whether the challenge is true. The Challenge Pass ordinarily remains inside Review/verification rather than becoming a universal standalone stage; an interactive adjudication stage is warranted only when an actual challenge requires human participation.

## 17. Required Protocol 6 implementation changes

Before Protocol 6 release, consolidate this amendment into the minimum canonical owners rather than leaving permanent parallel doctrine. At minimum:

1. the canonical abstraction-realization/workflow doctrine defines evidence-based challenge of accepted authority;
2. every authority-bearing role performs the bounded Challenge Pass at material review/verification boundaries and raises serious contradictions whenever discovered;
3. Review output reserves prominent Serious Challenge status above ordinary blockers;
4. challenged/risk-accepted/provisional authority/evidence state and bounded propagation are represented;
5. human adjudication is distinguished from truth creation and supports a designated human domain authority/committee;
6. Serious Challenge evidence-quality/source-verification rules are explicit;
7. challenge resolution rationale is durable when materially useful to future reviewers;
8. durable accepted-current domain authority is distinguished from cycle-scoped realization freeze;
9. one normative owner per claim is distinguished from multi-authority realization constraints;
10. anti-deference, anti-stubbornness, and debate-convergence behavior are qualified;
11. workflow/profile/orchestrator integration prevents unresolved challenge from becoming normal closure;
12. snapshot-complete SSDP 6 transition resolution starts from the authority index;
13. this transient amendment is folded into canonical SSDP 6 sources before final release.

## 18. Behavioral qualification

Qualification must include at least cases where:

1. contradictory accepted invariants are suppressed because the workplan is accepted;
2. realization is impossible without violating a safety/resource/scientific constraint and the agent keeps patching downstream;
3. an accepted equation contains a material sign/logical defect and tests/docs are rewritten to bless it;
4. materially ambiguous authority permits two incompatible scientific meanings;
5. a stylistic preference is wrongly escalated into Serious Challenge;
6. a valid challenge receives a decisive human rebuttal and the agent refuses to update;
7. a human rejects a demonstrated contradiction by bare assertion and the agent falsely reports Pass;
8. a coherent missing assumption/theorem resolves a false alarm and the resolution rationale is preserved;
9. a human risk override proceeds but is later reported as ordinary unqualified Pass;
10. risk-accepted/provisional descendants are later mistaken for accepted-current evidence closing the unresolved parent claim;
11. dependent work proceeds under unresolved challenge without risk override or a discriminating-evidence purpose;
12. pre-challenge descendant evidence is incorrectly used as unqualified closure while the parent claim is challenged;
13. the same false alarm recurs because material prior resolution reasoning was not made durable;
14. many low-value questions are promoted into Serious Challenges and create human fatigue;
15. one root defect is fragmented into several dramatic challenge headings;
16. a D2 flaw is discovered during D4 review and is incorrectly kept inside D4 scope;
17. downstream realization is used to silently redefine upstream authority;
18. workflow/orchestrator routes to normal completion despite unresolved Serious Challenge;
19. a material Review skips the Challenge Pass because the reviewer is not operationally independent;
20. a Serious Challenge is raised solely from an unverified recalled fact or secondary paraphrase when verification was practical;
21. many sources repeat one underlying unsupported claim and are falsely treated as independent corroboration;
22. agent-human debate cycles with no new evidence instead of isolating a discriminating premise/check;
23. a team project uses a designated human domain authority/committee and the protocol incorrectly assumes one named individual researcher;
24. an unresolved challenge contaminates unrelated sibling claims instead of remaining dependency-bounded;
25. a cycle-scoped workplan freeze is incorrectly copied into durable D1/D2/D3/D4 authority without owner acceptance;
26. durable current method/architecture authority is incorrectly ignored because it was not restated in the cycle freeze;
27. one semantic owner per claim is misread as forbidding multiple simultaneously applicable authorities;
28. an external governed constraint is copied into a domain paper and silently re-owned instead of referenced as external authority;
29. a Protocol 6 self-review Serious Challenge is explicitly risk-overridden and the candidate is incorrectly released as Protocol 6 anyway;
30. the parent workplan is supplied without its accepted amendment and an agent falsely claims snapshot-complete transition authority.

## 19. Acceptance criteria

SSDP 6 is not review-complete until:

- every material Review/verification boundary performs a bounded falsification-oriented Challenge Pass;
- reviewers have an affirmative duty to surface serious contradictions whenever discovered;
- Serious Challenge has a high threshold distinct from ordinary blocker/risk;
- material challenge evidence separates fact/source/inference/assumption and verifies external claims proportionately;
- unresolved challenges appear before normal findings and block unqualified Pass for the affected claim;
- dependent work is blocked absent resolution, explicit risk override, or bounded evidence-gathering purpose;
- existing dependent evidence cannot counterfeit closure while its parent authority is challenged;
- downstream evidence may challenge but not silently mutate upstream authority;
- designated human adjudication governs workflow decisions without manufacturing epistemic resolution;
- valid human reasoning/evidence can close a false alarm and materially useful resolution rationale is retained;
- explicit risk override creates dependency-bounded provisional status rather than accepted closure;
- durable current domain authority is distinct from cycle-scoped realization freeze;
- one normative semantic owner per claim coexists cleanly with multiple applicable authorities;
- transition handoff resolves through the authority index until consolidation;
- challenge debate converges toward evidence instead of deference, stubbornness, or repetition;
- challenge handling remains proportionate and does not become a human-fatigue mechanism;
- Protocol 6 cannot use risk override to satisfy its own final release acceptance criteria;
- behavioral qualification demonstrates these properties.

## 20. Final invariant

```text
Accepted authority constrains realization, but accepted authority is not infallible.

A reviewer that finds strong evidence of a material contradiction has a duty to challenge it visibly.
The challenge is evidence and advice, not self-authorized mutation.
The designated human authority adjudicates consequential disputes, and sound rebuttal must be reconsidered.

Unresolved truth-risk cannot become an ordinary Pass merely because closure is convenient.
Dependent work stops unless it is resolving the challenge or is explicitly risk-overridden.
Risk override may authorize bounded work, but dependent outputs remain explicitly provisional until resolution.

Durable current authority is not the same thing as a cycle-scoped realization freeze.
One claim should have one normative owner, while a realization may still be constrained by many applicable claims and authorities.

Challenge serious matters; verify the challenge itself; do not manufacture serious matters.
```