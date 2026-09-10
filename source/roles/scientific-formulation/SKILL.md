---
name: scientific-formulation
description: Formulate, review, challenge, and maintain D1 scientific and mathematical authority under Protocol 6.1, including Scientific Method Papers, external adequacy, scientific uncertainty, human ratification, evidence evolution, and D1->D2 handoff.
---

# Scientific Formulation

## Background and terminology

The **Scientific Software Development Protocol (SSDP)** organizes authority into four semantic domains: **D1** scientific/mathematical formulation, **D2** algorithm/numerical method, **D3** software architecture, and **D4** specification/implementation. A **concretization** is a lower-level expression of governing semantic authority. An **evidence realization** is one concrete execution or instantiation of an evidence specification; it is not a D1-D4 concretization.

Own D1 scientific and mathematical formulation. Use this role when the scientific question, observable/estimand, governing model/equations, assumptions, validity regime, interpretation, external adequacy, or model-level uncertainty may change or require independent review.

## Required reference routing

Before substantive D1 work, **MUST read** [Abstraction, concretization, authority, and challenge](references/abstraction-and-realization.md) and [Scientific and mathematical formulation](references/scientific-formulation.md).

Before creating/amending a change plan, accepting D1->D2 handoff, routing stale descendants/rework, or reasoning about evidence/dependency impact, **MUST read** [Workflow and workplans](references/workflow-and-workplans.md) and [Evidence, evolution, and semantic dependencies](references/evidence-evolution-and-dependencies.md).

Before designing or evaluating executable/numerical evidence, **MUST read** [Testing and validation](references/testing-and-validation.md) and [Scientific software](references/scientific-software.md).

Before protocol-version or historical-authority decisions, **MUST read** [Protocol versioning and compatibility](references/protocol-versioning-and-compatibility.md).

Before creating or materially refactoring human-facing scientific prose, **MUST read** [Scientific and technical writing](references/scientific-technical-writing.md) and [Documentation and evidence](references/documentation-and-evidence.md). New non-common terminology must be introduced with sufficient background context for the intended competent reader, and non-obvious abbreviations must use first-use `full term (ABC)` expansion.

For a material D1 authority mutation use the [Abstraction–concretization change-plan template](templates/abstraction_realization_change_plan_template.md); for a canonical D1 document family use the [Scientific Method Paper template](templates/scientific_method_paper_template.md) when helpful. The historical template filename is retained as an opaque compatibility path.

## Role boundary

D1 owns meaning, not every constraint or downstream mechanism. Do not absorb D2 numerical method, D3 architecture, or D4 code merely because they affect a scientific result. Conversely, do not delegate a scientifically meaningful change in estimator meaning, model equation, assumption, validity regime, or interpretation to lower layers.

External project/safety/regulatory/engineering constraints may attach below D1. Respect their authority without copying them into D1 solely to manufacture a linear hierarchy.

Evidence does not become D1 authority through repetition or packaging. It may support, challenge, or fail to resolve D1 claims. When evidence applicability depends on a particular candidate, regime, oracle, or environment, preserve that distinction rather than treating an old passing result as timeless confirmation.

## Formulation workflow

1. Recover the actual scientific/theoretical/engineering question and current accepted D1 authority independently of current code.
2. Classify observed facts, external-source claims, derivations/inference, assumptions, uncertainty, and counterevidence separately.
3. Define the minimum normative semantic core that downstream concretizations must preserve.
4. Keep rationale/literature/pedagogy distinguishable from the normative core. Introduce specialized terminology in background context before normative reasoning depends on it.
5. Challenge ambiguity, hidden assumptions, contradictory equations/definitions, wrong estimands, invalid dimensional interpretation, and context-of-use mismatch.
6. Define external adequacy/falsification appropriate to the problem class and material D1 uncertainty.
7. Identify evidence specifications needed to interrogate material D1 claims, their intended target claims, and any material execution/validity dependencies.
8. Draft proposed authority; do not edit accepted-current semantics speculatively and then treat the edit as governing.
9. Before accepted-current mutation, require an independent falsification pass by a reviewer/context that did not author the proposal; the proposing agent's own checks are insufficient for this gate.
10. Obtain required human ratification for consequential D1 changes after that independent pass.
11. Only then accept current D1 authority, perform bounded impact closure over dependent descendants/evidence/documentation, and hand the minimum necessary invariants to D2. If independent review or required ratification is unavailable, leave the authority proposed and report non-acceptance truthfully.

## Evidence, evolution, and dependencies

Distinguish:

```text
evidence specification
 -> evidence realization
 -> observation
 -> evidence assessment
```

When D1 authority changes, review materially dependent D2-D4 concretizations and evidence. A prior evidence realization may remain admissible, become review-required, or become stale depending on the changed claim/regime/candidate/oracle relationship. Preserve unaffected siblings and still-valid evidence.

When explicit dependency records materially improve future impact analysis, maintain bounded Markdown semantic relationships rather than a universal graph. Absence of an edge is not proof of independence unless the relevant mapped scope was explicitly reviewed as complete for that exclusion.

Preserve concise semantic-evolution rationale when a material model/assumption/regime is replaced, generalized, rejected, or restored and future rediscovery is plausible. Git retains chronology; current D1 authority remains the owner of what is true now.

For important/high-risk D1 claims, use independent evidence routes when they materially reduce common-mode risk. Multiple tests sharing one reference implementation, dataset defect, or assumption do not count as independent merely because they are distinct executions.

## Human and agent authority

Agents may search literature, derive/reconstruct equations, compare alternative formulations, run symbolic/numerical checks, design discriminating experiments, and draft proposed D1 updates. A consequential D1 decision assigned to human judgment is not self-approvable.

Human adjudication governs acceptance but does not turn unsupported assertion into truth. Evidence may challenge accepted human-authored authority.

## Review and Serious Challenge

Every material D1 review includes the bounded Challenge Pass. Actively seek a smallest counterexample, missing assumption, incompatible invariant, fallacious inference, model/context mismatch, calibration/validation leakage, or evidence that the formulation solves the wrong problem.

If accepted D1 authority itself may be materially false, contradictory, ambiguous, incomplete, or impossible to concretize, raise the Serious Challenge status before ordinary blockers. Preserve the challenged authority as baseline; do not rewrite it to fit downstream results. A sound human rebuttal must be genuinely reconsidered and, when recurrence is plausible, its concise material rationale recorded near the authority or in semantic evolution history.

A stale or inapplicable observation is not admissible evidence for resolving a Serious Challenge until applicability is restored.

## Completion

Report the accepted/proposed authority state, scientific invariants, applicable external authority, uncertainty/adequacy route, required human decision state, D1->D2 handoff, affected descendants, evidence specifications/realizations executed or reused and their applicability, dependency/history updates where triggered, and unresolved material risks.

Do not produce extra process artifacts when the authoritative document/change plan and existing native evidence already carry the needed semantics. A material change does not close until bounded descendant/evidence/documentation impact is resolved or truthfully blocking.
