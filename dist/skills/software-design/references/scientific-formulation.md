# Scientific and Mathematical Formulation (D1)

D1 owns the accepted scientific or mathematical meaning that downstream numerical methods and software must realize. It is not a documentation appendix to Software Design.

## D1 authority

A D1 abstraction may include, as applicable:

- the scientific/engineering question and intended context of use;
- observables, estimands, objective functions, response quantities, and interpretation;
- governing equations, statistical models, constitutive/closure assumptions, and mathematical definitions;
- units, sign/frame conventions, coordinate meanings, boundary/initial conditions when they are part of the modeled problem;
- material assumptions, validity regime, approximation/model scope, excluded regimes, and known limitations;
- scientific model/data/parameter/assumption uncertainty and model discrepancy semantics;
- what external evidence would count as adequacy, falsification, or validation for the problem class.

Security, deployment, performance, compatibility, and other external constraints are not automatically D1. They attach where their semantics belong.

## Scientific Method Paper

The logical D1 normative document family is the **Scientific Method Paper**. A project may use one file or several coordinated files, but each material D1 claim has exactly one accepted-current semantic owner.

Distinguish within the document family:

- **normative semantic core** — the accepted D1 claims that constrain downstream realization;
- **rationale/evidence/literature** — support for those claims;
- **explanation/pedagogy** — material useful for understanding but not independently normative.

Literature does not automatically become project authority. External evidence can support or challenge the project's D1 authority, but accepted project semantics change only through the owning D1 decision process.

Use authority states from [Abstraction, realization, authority, and challenge](abstraction-and-realization.md). Proposed edits are not accepted current authority. Release-pinned/publication copies remain historical snapshots and are not silently rewritten to follow later science.

## D1 design

When formulating or changing D1:

1. recover the actual scientific/theoretical/engineering question independently of current software;
2. identify external/stakeholder authority and applicable governed constraints;
3. state the minimum semantic invariants needed to make the intended conclusion meaningful;
4. separate assumptions from derived consequences and observations from interpretation;
5. identify ambiguity that could admit scientifically different downstream realizations;
6. keep lower-level numerical/architectural/implementation mechanisms delegated unless they are themselves scientifically semantic;
7. define the external adequacy/falsification route appropriate to the problem class.

A scientific model that is convenient to compute but does not answer the intended question is inadmissible even if all software tests pass.

## External adequacy

D1 has an external boundary in addition to internal realization verification.

- **Empirical/model-based science:** compare against intended context and independent observation/experiment; separate calibration/fitting from validation where the distinction matters.
- **Mathematical/theoretical software:** use proof, axiomatic consistency, limiting/reference theory, or other justified mathematical authority rather than meaningless empirical-validation ceremony.
- **Engineering/scientific computing:** use standards, qualification experiments, safety margins, reference data, or stakeholder context-of-use evidence as appropriate.

Internal D2/D3/D4 verification cannot substitute for an external adequacy claim, and external validation cannot substitute for faithful numerical/software realization.

## Uncertainty and robustness

D1 owns uncertainty whose meaning belongs to the model/problem rather than to its numerical realization. Consider, proportionately:

- data/measurement uncertainty;
- parameter uncertainty and identifiability;
- structural/model discrepancy;
- uncertainty from material assumptions or validity regime;
- sensitivity of conclusions to plausible alternative models/closures;
- robustness of interpretation to those uncertainties.

D2 numerical uncertainty is separate and should be propagated into D1 observables when material.

## Human ratification

Human adjudication is risk-sensitive, not universal. Human ratification is normally required for consequential changes to one or more of:

- scientific question or interpretation;
- observable/estimand/objective whose meaning changes the conclusion;
- governing model/equations/closures;
- material assumptions or validity regime;
- scientifically consequential approximation/model-discrepancy treatment;
- unexplained discrepancy acceptance;
- a scientific conclusion whose meaning changes materially.

Agents may autonomously gather literature, derive equations, reconstruct assumptions, generate alternatives, perform symbolic/numerical checks, design discriminating experiments, and draft proposed authority. They may not self-accept a consequential human-gated D1 mutation.

## D1 -> D2 handoff

Before accepting a D2 child abstraction, verify both:

- **fidelity:** the numerical/algorithmic formulation realizes the accepted D1 semantics; and
- **adequacy:** the D2 abstraction preserves enough D1 meaning to prevent downstream software from passing while solving a scientifically different problem.

Pass the minimum material invariants, assumptions, observables, conventions, validity conditions, and uncertainty/error expectations needed by D2. Do not prescribe numerical machinery unless the scientific semantics truly require it.

## D1 review and Serious Challenge

Material D1 review is falsification-oriented. Seek the smallest credible counterexample to the formulation, hidden assumptions necessary for its conclusion, inconsistent equations/definitions, invalid dimensional interpretation, calibration/validation leakage, and evidence that the formulation solves the wrong problem.

A material contradiction in accepted D1 authority raises the Serious Challenge path defined by [Abstraction, realization, authority, and challenge](abstraction-and-realization.md); downstream code must not be used to rewrite the science silently.