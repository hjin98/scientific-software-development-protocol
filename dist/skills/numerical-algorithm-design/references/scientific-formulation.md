# Scientific and Mathematical Formulation (D1)

D1 owns accepted scientific/mathematical meaning: the problem/context, observable or estimand, governing model/equations/definitions, assumptions, validity regime, interpretation, model-level uncertainty, limitations, and problem-appropriate external adequacy/falsification. It is not a documentation appendix to software design.

Universal authority/Challenge/representation rules are in [Abstraction, concretization, authority, challenge, and representation](abstraction-and-concretization.md); evidence lifecycle in [Evidence, evolution, and semantic dependencies](evidence-evolution-and-dependencies.md); human-facing exposition in [Scientific and technical writing](scientific-technical-writing.md).

## D1 normative content

A D1 abstraction may govern, as applicable: scientific/engineering question and context; observables/estimands/objectives and interpretation; equations/statistical models/constitutive or closure assumptions and mathematical definitions; scientifically meaningful units/sign/frame/coordinate/boundary/initial conventions; assumptions/validity/excluded regimes/limitations; model/data/parameter/assumption uncertainty and discrepancy semantics; and what external evidence counts as adequacy, falsification or validation.

Security, deployment, performance, compatibility and other engineering constraints attach at the domain where their semantics belong rather than being promoted into D1 automatically.

The logical current D1 owner is the **Scientific Method Paper** family. One family may span files, but each material current claim has one semantic owner. Distinguish normative core from rationale/evidence/literature/pedagogy. Literature can support/challenge project authority but does not become project authority automatically.

## Formulation and acceptance

Recover the actual question independently of code; identify stakeholder/external authority; state the minimum semantics needed to make the intended conclusion meaningful; separate assumptions, derivation, observations and interpretation; identify ambiguity admitting scientifically different descendants; keep numerical/software mechanisms delegated unless scientifically semantic; define external adequacy appropriate to the problem class; and identify evidence targets plus material execution/validity dependencies.

A material proposed D1 mutation remains proposed until its owning acceptance process completes, including independent falsification and required human ratification. Convenient computation or successful software tests cannot legitimize a model that answers the wrong question.

Human adjudication is normally warranted for consequential changes to question/interpretation, observable/estimand, governing model/equations/closures, material assumptions/validity, scientifically consequential discrepancy treatment, unexplained discrepancy acceptance, or conclusions. Agents may research/derive/check/design evidence/draft proposals but may not self-accept a designated human-gated change.

## External adequacy and uncertainty

Empirical/model-based science uses independent observation/experiment appropriate to context; mathematical/theoretical work uses proof/axiomatic consistency/limiting/reference theory; engineering/scientific computing uses standards, qualification experiments, safety margins, reference data or stakeholder context as appropriate. Internal D2-D4 correctness cannot substitute for D1 external adequacy, and external agreement cannot prove faithful downstream concretization.

D1 owns model/data/parameter/assumption uncertainty and structural/model discrepancy. D2 numerical uncertainty is distinct and should be propagated into D1 observables when material.

## D1 -> D2 handoff and Review

A D2 child must be faithful to accepted D1 and abstractly adequate: it must preserve enough D1 meaning that downstream software cannot satisfy D2 while solving a scientifically different problem. Hand D2 only the minimum material invariants, assumptions, observables, conventions, validity conditions and uncertainty/error expectations; do not prescribe numerical machinery without scientific need.

On accepted D1 change, perform bounded impact closure over dependent D2-D4, evidence, documentation/dependency views, re-ratification and semantic history; preserve unaffected siblings/still-valid evidence.

Material D1 Review seeks the smallest credible counterexample, hidden assumption, inconsistent equation/definition, dimensional/interpretive error, calibration-validation leakage, or wrong-problem formulation. If accepted D1 itself may be materially false, contradictory, ambiguous, inadequate or unrealizable, raise **SERIOUS CHALLENGE** rather than rewriting it to fit downstream behavior.

## Protocol 6.4 D1 formal-definition consequences

D1 authority uses formal-first, definition-before-substantive-use semantics for materially governed scientific/mathematical objects. Define or exactly import observables, estimands, states, distributions, fields, parameters, equations/models, constitutive/closure relations, predicates, assumptions and validity conditions before downstream inference depends on them. Every material symbol resolves to its domain/type/shape/unit and scope; physical equations are dimensionally coherent; bound/free-variable and quantifier direction are explicit when material.

For parameterized scientific families distinguish the family, concrete parameter binding, and any governed default. State whether parameters are fixed, free, derived, estimated or externally constrained, plus the regime/uncertainty/validity attached to the binding actually used. A software default cannot silently become D1 meaning.

Specialized external scientific results follow the exact-import rule: identify the intended theorem/model/law/data/value variant, material hypotheses and regime, stable source/version/locator, notation/unit/frame transformation, and empirical conditions/uncertainty when applicable. Citation supports a claim only to the extent the source actually does so and never mints project authority by itself.

Separate definitions from existence/uniqueness claims, assumptions, derived propositions, empirical observations, approximations and conclusions. A definition may conservatively extend vocabulary but cannot by notation prove scientific truth, adequacy or external validity. For every imported/derived result used normatively, discharge or propagate its material hypotheses. Ambiguous or conflicting current meanings that could change scientific interpretation are D1 Review/Challenge issues, not editorial choices.
