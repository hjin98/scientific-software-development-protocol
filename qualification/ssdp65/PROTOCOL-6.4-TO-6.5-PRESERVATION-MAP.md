---
kind: preservation-supersession-map
protocol_from: 6.4.0
protocol_to: 6.5.0
status: pre-freeze-complete
p0: 55c085261eb827e3047637d045a8e6917ea6b962
review_authority: independent-review-required-after-p1-freeze
---

# Protocol 6.4 -> 6.5 Preservation / Supersession Map

## 1. Purpose and interpretation

This map satisfies I65-09. It maps accepted Protocol 6.4 capability, not obsolete wording or proxy-test representation, into the Protocol 6.5 candidate. It is implementation evidence for later independent Review; it is not acceptance authority.

Classification vocabulary:

`PRESERVED | CLARIFIED | GENERALIZED | COMPRESSED | RELOCATED | SUPERSEDED | INTENTIONALLY_REMOVED`.

`SUPERSEDED` and `INTENTIONALLY_REMOVED` apply only where an equal-or-stronger owner/qualification route is identified. Removing a test helper never removes the semantic capability it attempted to model.

## 2. Protocol 6.4 §1 parent invariants

| 6.4 invariant | 6.5 classification | Current 6.5 owner / realization | Evidence obligation |
| --- | --- | --- | --- |
| D1-D4 remain the only semantic authority domains; no D5/meta-authority | PRESERVED | `source/shared/references/abstraction-and-concretization.md`; four role/domain owners | Role routing + independent semantic Review |
| Current authority defines what must be true; literature/tests/evidence/docs/PEM/history do not mint authority | PRESERVED | kernel; evidence owner; PEM owner | inherited regression + semantic Review |
| External constraints obtain force only from real governing authority | PRESERVED | kernel; `security-and-trust-boundaries.md`; D1/D3/D4 owners as applicable | semantic Review |
| Concretization fidelity and abstraction adequacy remain distinct | PRESERVED | kernel | independent out-of-matrix abstraction-adequacy Review |
| One detailed owner, progressive disclosure, explicit routing, cold discoverability, derived-view subordination | PRESERVED / COMPRESSED | kernel + role/concern routers | package/routing tests + Review |
| Evidence specification -> realization -> observation -> assessment | PRESERVED | `evidence-evolution-and-dependencies.md` | inherited evidence tests |
| Serious Challenge, human adjudication, bounded impact closure, Review/Verification/Stabilization remain | CLARIFIED | kernel + `workflow-and-workplans.md` | semantic Review; Challenge counterexamples |
| PEM remains schema-1, project-local, conditionally activated, evidence-backed, non-authoritative | PRESERVED / CLARIFIED | PEM owner/template/validator | direct owner/template/validator parity + PEM regression |
| Frozen 5.16-6.4 version/profile/package/recovery/publication identities remain immutable | PRESERVED / GENERALIZED | versioning owner; release-state owner; frozen profile hash oracles | Core/profile frozen-resource tests |
| Public fallback remains distinct from recovery and exact-ref bound | PRESERVED / CLARIFIED | versioning owner + `PROTOCOL-RELEASE-STATE.yaml` | release-state transition negatives + exact-ref lifecycle Review |
| Protocol 7 architecture remains isolated | PRESERVED | Protocol-7 active authority/revision lineage; 6.5 workplan non-goal | no D3/D4 mutation before post-acceptance inheritance reconciliation |

## 3. P64-A..P64-O preservation obligations

| ID | Protected capability | 6.5 classification | Current owner / implementation |
| --- | --- | --- | --- |
| P64-A | Accepted Protocol-6 inheritance, authority/evidence/Challenge/PEM/lossless/minimum-mechanism semantics | PRESERVED | kernel + domain/workflow/evidence/PEM owners |
| P64-B | Frozen version/recovery/package preservation; distinct bootstrap/recovery | PRESERVED / GENERALIZED | release-state owner + versioning + frozen profile hash tests |
| P64-C | Formal-first source availability before substantive use; context availability before inference | PRESERVED | kernel semantic-definition discipline + writing owner |
| P64-D | Unique current meaning; conflicting applicable owners cannot be resolved by order/latest/routing | PRESERVED | kernel |
| P64-E | Availability basis, role, novelty, support/evidence and normative force remain orthogonal | PRESERVED | kernel + evidence/writing owners |
| P64-F | Definitional conservativity and mathematical/logical/type/unit/well-definedness closure | PRESERVED | kernel + D1/D2 owners |
| P64-G | Parameter family/instance/default ownership and evidence binding | PRESERVED | kernel + D1/D2/D4 as applicable |
| P64-H | Exact import/source/variant/provenance/trust and inert external-content discipline | PRESERVED | kernel + writing + security/trust owners |
| P64-I | Typed semantic dependency/impact; USES_DEFINITION subordinate and directionally correct | PRESERVED / COMPRESSED | kernel + evidence dependency owner; derived view remains non-authoritative |
| P64-J | Validity/approximation/hypothesis propagation and non-circular warrant | PRESERVED | kernel + evidence + D1/D2 owners |
| P64-K | Semantic identity vs labels; coherent composition/equivalence/evolution | PRESERVED / GENERALIZED | versioning + evidence evolution |
| P64-L | D1/D2 strongest practical formalism; D3/D4 formal contracts without decorative math/upstream leakage | PRESERVED | four domain owners + kernel |
| P64-M | Human-facing definitions/abbreviations/presentation; self-hosting; frozen history | PRESERVED / GENERALIZED | writing/documentation owners + self-application kernel |
| P64-N | Version-bound adoption, semantic-dependency-not-activation, runtime prerequisite loading | PRESERVED | versioning + kernel + portability/routing |
| P64-O | Assembled source/generated/profile/Core qualification, exact lifecycle, Protocol-7 isolation | GENERALIZED | versioning + release-state owner + package/profile/Core acceptance; lifecycle reordered to Review -> ratification -> publication -> recovery |

## 4. QF64-A..QF64-P semantic capability map

The old `qf_a ... qf_p` dictionary predicates and one self-contained positive/negative fixture matrix were proxy qualification representations. Protocol 6.5 removes them from current acceptance because fixture self-consistency cannot establish arbitrary prose semantic adequacy. Their historical cases remain recoverable in the archived 6.4 workplan, Stage-C qualification, Review records and Git history. The protected semantic capabilities map as follows.

| QF64 | Protected capability from accepted 6.4 | 6.5 disposition / oracle |
| --- | --- | --- |
| A | foundational vs declared/imported availability; use-before-definition; hidden roots; exact imports | PRESERVED; semantic owner + independent Review; structural import/binding properties remain testable where represented |
| B | one compatible canonical owner vs silent conflicting-owner selection | PRESERVED; kernel + Review |
| C | primitive signature, scoped binders, open role vocabulary | PRESERVED; kernel + D1/D2 Review |
| D | conservative definition; separate warrant; no definition/truth laundering | PRESERVED; kernel/evidence + Review |
| E | domain/relation/logical/totality/choice/piecewise/unit closure | PRESERVED; kernel + D1/D2 Review |
| F | family/instance/binding/default ownership and evidence reconciliation | PRESERVED; kernel/evidence + targeted structural tests where machine represented |
| G | stochastic law/dependence/conditioning and hypothesis propagation; no approximation laundering | PRESERVED; D1/D2/kernel/evidence |
| H | direct typed semantic-use families; bounded absence/completeness; legitimate recursive composition | PRESERVED; evidence dependency owner; derived traces subordinate |
| I | independent typed warrant roots; no circular warrant/citation-as-authority/use-as-evidence | PRESERVED; evidence/testing + Review |
| J | external support/force separation, transformation lineage, inert external content | PRESERVED; writing/security/trust + Review |
| K | version snapshot/equivalence/lineage/impact reconciliation | PRESERVED / GENERALIZED; versioning + release-state owner + evidence evolution |
| L | lower-layer preservation; no D4 leakage/decorative formalism/downstream strengthening | PRESERVED; D3/D4 and upstream owner Challenge routing |
| M | source-resolvable and context-loaded prerequisites; dependency is not activation | PRESERVED; kernel + routing/portability |
| N | terminology/abbreviation/render integrity/example subordination | PRESERVED; writing/documentation + structural render/fence checks |
| O | frozen/generated/profile/bootstrap/recovery/Protocol-7 lifecycle polarity | GENERALIZED; release-state state machine + frozen-profile/Core tests |
| P | one current coherent lifecycle/workplan representation; recoverable history without amendment replay | GENERALIZED / COMPRESSED; release-state owner + current workplans/index route + history/archive |

**Proxy representation disposition:** current executable `QF64` helper predicates and arbitrary phrase pins are **INTENTIONALLY_REMOVED** as semantic acceptance oracles. Real schema/state/route/generated properties remain executable; arbitrary prose adequacy moves to fresh independent semantic Review.

## 5. F64-A..F64-L falsification capability map

| F64 | 6.4 falsification target | 6.5 classification / current route |
| --- | --- | --- |
| A | alternate formalization admitting materially different meanings | PRESERVED / GENERALIZED -> independent semantic Review + out-of-matrix pass |
| B | hidden prerequisite/foundational laundering | PRESERVED -> definition/source-availability Review |
| C | competing current meanings/duplicate owners/order-latest resolution | PRESERVED -> owner-conflict Review + release-state census |
| D | definition/proof/evidence/citation/normative-force laundering; warrant cycles | PRESERVED -> evidence/warrant Review |
| E | well-definedness/parameterization/stochastic/temporal ambiguity | PRESERVED -> D1/D2 semantic Review |
| F | typed dependency/impact omissions and wrong relation classes | PRESERVED -> evidence/dependency Review; structural traces where applicable |
| G | mixed versions, alias/label identity, instance collapse, split/merge/retirement | PRESERVED -> version/evolution Review |
| H | source support/variant/transform/binding force/correction/trust/instruction injection | PRESERVED -> security/trust + source-support Review |
| I | cross-domain leakage, decorative formalism, frozen delegated mechanism, false strengthening | PRESERVED -> D1-D4 boundary Review |
| J | inference from unloaded prerequisite or eager semantic-edge activation | PRESERVED -> routing/portability Review |
| K | self-hosting, presentation, current-vs-history separation | GENERALIZED -> SSDP self-application + release-state census + presentation checks |
| L | lossless inherited capability/lifecycle/frozen resources/Protocol-7 isolation | PRESERVED / GENERALIZED -> preservation map + inherited regression + frozen-profile/Core/release-state Review |

## 6. Protocol 6.4 formal-definition owner preservation

The substantive 6.4 definition/traceability sections are integrated into timeless current owners rather than copied into a "6.5 amendment":

- universal semantic object/source/context availability, role openness, definition/warrant, well-definedness, parameterization and USES_DEFINITION direction -> `abstraction-and-concretization.md`;
- D1 formal formulation consequences -> `scientific-formulation.md`;
- D2 numerical consequences -> `numerical-algorithm-design.md`;
- D3 contract consequences -> `architecture-and-design.md`;
- D4 contract consequences -> `specification-and-implementation.md`;
- validity/evidence/dependency/applicability -> `evidence-evolution-and-dependencies.md`;
- human-facing formal-first writing/import/abbreviation/rendering -> `scientific-technical-writing.md`;
- documentation maintenance -> `documentation-maintenance.md`;
- external semantic-source trust -> `security-and-trust-boundaries.md`;
- workflow consequences -> `workflow-and-workplans.md`;
- qualification scope -> `testing-and-validation.md`;
- version/equivalence/adoption/profile compatibility -> `protocol-versioning-and-compatibility.md`.

## 7. 6.5 intentional supersessions

1. **Mutable lifecycle value copies in immutable/versioned semantic source** -> SUPERSEDED by root `PROTOCOL-RELEASE-STATE.yaml` plus references/projections.
2. **Review PASS treated as sufficient protocol-version acceptance** -> CLARIFIED: Review PASS is technical eligibility; explicit stakeholder ratification owns the acceptance decision.
3. **Bootstrap-before-final-Review lifecycle** -> SUPERSEDED by candidate -> acceptance -> freeze -> Review -> ratification -> public fallback -> verification -> distinct recovery -> cutover.
4. **Proxy-only QF fixture predicates as semantic proof** -> INTENTIONALLY_REMOVED from current acceptance; protected cases remain Review obligations or real structural tests.
5. **Protocol-number-labelled current-owner appendices** -> COMPRESSED into natural timeless owner sections; history remains in semantic history/archive.
6. **Executable-only PEM field meaning** -> RELOCATED into canonical PEM owner/template; validator is a concretization, not schema authority.
7. **Repeated current release-state SHAs in hot docs/prompts** -> INTENTIONALLY_REMOVED; exact current values live only in the release-state owner, while frozen historical/cycle inputs remain allowed.

## 8. Freeze readiness rule

P1 may freeze only after:
- this map remains complete against the assembled candidate;
- inherited regression/package/profile/Core acceptance is green;
- kernel non-growth and current-state projection census pass;
- PEM/history reconciliation is complete;
- temporary implementation-only infrastructure is removed;
- release state still truthfully says 6.4 accepted-current and 6.5 unreviewed/unratified/unpublished/unrecovered.

Any semantic mutation after freeze requires a new P1 identity and affected requalification.
