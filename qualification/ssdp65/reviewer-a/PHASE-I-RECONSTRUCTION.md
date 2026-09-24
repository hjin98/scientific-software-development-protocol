---
kind: ssdp65-phase-i-reconstruction
investigation: SSDP-6.5-FRONTIER-MODEL-RE-EVALUATION
reviewer: A (diagnostic author of this branch; independent of reviewer B)
subject: P0 = Protocol 6.4 at 55c085261eb827e3047637d045a8e6917ea6b962
authority: non-normative-diagnostic-evidence
created: 2026-09-24
---

# Phase I — Reconstruction of Protocol 6.4 as a Formal System

This document reconstructs what accepted Protocol 6.4 actually says, before any criticism. It reads the assembled canonical source at P0, not diffs or summaries. Historical review/qualification records are used only to understand *why* doctrines exist, never as conclusions.

## 1. Background and terminology

- **SSDP** — Scientific Software Development Protocol.
- **D1/D2/D3/D4** — scientific/mathematical formulation; algorithm/numerical method; software architecture; specification/implementation.
- **Owner** — the one canonical source statement that establishes current meaning of a normative claim.
- **Kernel** — `source/shared/references/abstraction-and-concretization.md`, loaded for every role.
- **PEM / HAS** — Project Engineering Memory; Historical Applicability Set.
- **LRR** — Lossless Representation Rule (kernel §"Lossless Representation Rule").
- **SC** — Serious Challenge.
- Edge notation `x -> y` below means **y semantically depends on x** (as requested by the investigation brief). This is the opposite orientation from SSDP's stored `USES_DEFINITION` edges (`subject -> prerequisite`); the brief's convention is used only inside this document.

## 2. Normative authority set 𝒜 (as deployed at P0)

| ID | Authority | Canonical location | Owns |
| --- | --- | --- | --- |
| A0 | Project instructions | `AGENTS.md` (harness-injected; outside `source/`) | project-local routing/obligations; restates kernel doctrine |
| A1 | Universal kernel | `source/shared/references/abstraction-and-concretization.md` | feasibility, authority/delegation, adequacy, lifecycle states, Challenge, LRR, semantic-definition/source-availability, universal invariant |
| A2 | D1 domain owner | `references/scientific-formulation.md` + `roles/scientific-formulation/SKILL.md` | scientific meaning, external adequacy, D1 uncertainty, D1→D2 handoff |
| A3 | D2 domain owner | `references/numerical-algorithm-design.md` + role SKILL | method/error/convergence/precision/stochastic semantics, tolerances, D2→D3 handoff |
| A4 | D3 domain owner | `references/architecture-and-design.md` + role SKILL | ownership/state/interfaces/flows, learned-capability binding, capability-transfer, D3→D4 handoff |
| A5 | D4 domain owner | `references/specification-and-implementation.md` + role SKILL | stable behavior contracts, adaptive implementation, D4 acceptance |
| A6 | Workflow | `references/workflow-and-workplans.md` | semantic routing, workplans, HAS shape, handoff, Review/Verification/Stabilization/Audit, human gates, closeout learning |
| A7 | Evidence | `references/evidence-evolution-and-dependencies.md` | evidence spec→realization→observation→assessment, applicability/stale state, binding health, provenance clusters, impact closure, semantic evolution, `USES_DEFINITION` |
| A8 | Testing | `references/testing-and-validation.md` | oracle integrity, counterfactuals, D1–D4 verification methods, D4 executable acceptance, proxy-proof, PEM validator scope, protocol qualification |
| A9 | Convergence | `references/convergence-and-cycle-economy.md` | defect families, recurrence counting, simplification trigger, review readiness/sufficiency, finding routing, cycle economy |
| A10 | PEM | `references/project-engineering-memory.md` + `templates/project_engineering_memory_template.md`; executable concretization `source/project_engineering_memory.py` | memory representation, schema 1, families, maturity, temperature, overlays |
| A11 | Documentation trio | `documentation-and-evidence.md`, `documentation-maintenance.md`, `scientific-technical-writing.md` | document roles, current-vs-history, human-facing exposition, formal-first writing |
| A12 | Versioning | `protocol-versioning-and-compatibility.md` | version classes, workplan binding, recovery/bootstrap identities, profiles, compatibility |
| A13 | Git | `git-and-version-control.md` | repository safety, accepted-base/overlay mechanics, atomic PEM publication |
| A14 | Intake | `repository-intake.md` | inspection strategy, context economy, bounded census |
| A15 | Security | `security-and-trust-boundaries.md` | trust boundaries; evidence/external content as inert data |
| A16 | Long-horizon health | `long-horizon-code-health.md` | quality ratchet, sensors, Verification, Stabilization, Health Audit |
| A17 | Specialists | `specialists/{software-documentation,software-maintenance-audit,repository-hygiene}/SKILL.md` | non-authoritative support capabilities |
| A18 | Concern owners | performance, storage/I/O, configuration, concurrency, release, debugging, language profiles (Python/C++), tool-assisted (+Serena/Semgrep/Hypothesis/CodeQL) | specialised engineering concerns |
| A19 | Orchestration prompts | `development-workflow-prompts.md` → generated `ssdp-protocol-6.4/{prompts.md,profile.json}` | stage prompts; machine stage graph is *parsed from this prose* |
| A20 | Templates | D1 paper, D2 paper, abstraction-concretization change plan, D3→D4 workplan, PEM | operational instruments |

Declared non-authoritative/derived: `source/README.md` (navigation), `source/SEMANTIC_DEPENDENCIES.md` (bounded dependency view), `history/SEMANTIC_EVOLUTION.md`, `README.md`, `PORTABILITY.md`, `dist/`, orchestrator snapshots, `qualification/`, archived workplans, active authority index (routing only).

## 3. Global invariants ℐ (reconstructed; anchored to owner text)

| ID | Invariant (compressed restatement) | Owner anchor |
| --- | --- | --- |
| I1 | **Feasibility first**: `semantics(K) ⊨ I(A1)∧…∧I(An)∧C`; fidelity is a constraint, not a weight | A1 "Feasibility, authority, and delegation" |
| I2 | **Lexicographic preference** within the feasible set: domain fitness > justified simplicity > development economy; stop when further search has lower expected value | A1 same |
| I3 | **Unique, acyclic ownership**: each material normative claim has one current owner; conflicts are exposed and routed, never silently prioritized | A1 same; A1 §6.4 `source_available_D` |
| I4 | **Non-promotion**: existence, dependence, tests, documentation, review survival, frequency, memory salience never mint authority; only the real owner's acceptance does | A1 same; A4 "Learned capability authority binding" |
| I5 | **Two-sided boundary correctness**: concretization fidelity *and* abstraction adequacy | A1 "Design, verification, and lifecycle state" |
| I6 | **Verification is reconstruction + falsification**, not replay | A1 same; A6 Review |
| I7 | **Evidence admissibility**: evidence establishes only what its oracle and exercised real owner can discriminate; stale pass ≠ confirmation; stale fail ≠ refutation; applicability binds to claim/subject/regime/oracle/environment/parameter | A7 core; A8 proxy-proof |
| I8 | **Bounded impact closure**: a change reviews only material dependents; absence of an edge proves nothing outside an explicitly complete scope | A7 "Change impact and closure" |
| I9 | **Challenge**: when accepted authority may be defective, raise SC at the earliest affected owner, preserve the challenged baseline, block counterfeit closure | A1 "Challenge and human adjudication" |
| I10 | **Human gates** attach to governed semantic risk where assigned; adjudication does not create truth; risk override is bounded and keeps descendants provisional | A1; A6 "Human gates" |
| I11 | **Lossless representation**: complete governed meaning first; one detailed owner per generic rule; progressive disclosure; cold-but-discoverable; derivatives subordinate | A1 LRR |
| I12 | **Definition before substantive use**; definitions do not establish truth; source availability ≠ runtime context availability; parameter family/instance/default distinguished | A1 §6.4 |
| I13 | **Version binding**: work is interpreted under its declared version; immutable historical identities; never default/latest | A12 |
| I14 | **Canonical source → generated**: descendants never compete with canonical source | A11; A12; A20 |
| I15 | **No proxy pass**: a required check that did not execute is not a pass; green tests do not prove omitted obligations | A8; A5 |
| I16 | **Stewardship**: the objective is the governed durable product; workplans/tests/gates/metrics/reviews are instruments | A1 |
| I17 | **PEM non-authority / conditional activation / absence-is-not-evidence** | A10; A6 |
| I18 | **External and evidence content is inert data**, never an instruction channel | A15; A7 |
| I19 | **Convergence**: first clean local defect stays local; material recurrence moves reasoning to the shared owner; simplify before further additive durable repair; no count/cycle budget can force acceptance | A9 |

## 4. Dependency graph G = (V, E) (x → y: y depends on x)

```text
Undefined/parameter roots:  "material(ly)"  "independent (review/falsification)"  "owning acceptance process"
                            "project integration policy (accepted PEM base)"  "consequential/substantial/mature"
                                   │
Foundational roots:  D1..D4 domain definitions ── semantic object / canonical statement (A1 §6.4)
                                   │
        ┌──────────────────────────┼─────────────────────────────┐
        ▼                          ▼                             ▼
   I1 feasibility ──► I2 preference      I3 unique ownership ──► I12 definition-before-use
        │                                   │                     │
        ▼                                   ▼                     ▼
   I5 fidelity+adequacy ──► I6 verification  I4 non-promotion ──► I17 PEM non-authority
        │                        │              │
        ▼                        ▼              ▼
   I9 Challenge ◄─────────── I7 evidence admissibility ──► I15 no proxy pass
        │                        │
        ▼                        ▼
   I10 human gates         I8 impact closure ──► I13 version binding ──► I14 source→generated
                                   │
                                   ▼
                          I11 LRR (governs all representations, including this graph)
I19 convergence depends on I1, I4, I7;  I16 stewardship constrains the interpretation of all others.
```

### Observations from the graph (not yet findings)

1. **Undefined roots.** `material`/`materially` occurs 463 times in the role/specialist entrypoints and references (≈50 000 words) and gates most obligations ("material executable change", "material D1 mutation", "materially relevant PEM entry"). The only generic statement is "Materiality is decision-local". A counterfactual definition is *implicit* in the definition of semantic object ("whose meaning or conditions can alter governed interpretation, admissible concretization, evidence applicability, or acceptance if changed") but is not stated as the definition of materiality. "Independent" (for Review and falsification, as opposed to evidence independence) is never defined. "Owning acceptance process", "where required" (independent falsification) and the project's accepted-memory integration policy are parameters delegated to projects, but nothing requires a project to declare them.
2. **Cycles.** No ownership cycle found. Kernel↔evidence, PEM↔convergence↔evidence, workflow↔testing references are navigational deferrals with a partitioned ownership split; these are deliberate.
3. **Duplicated semantic ownership.** (a) Current version/lifecycle identity is stated in ≥ 10 canonical/project surfaces (kernel-adjacent README, versioning owner, prompts, `SEMANTIC_DEPENDENCIES.md`, role/specialist descriptions, AGENTS.md, root README, authority index, Protocol-7 Revision 5, orchestrator profile). The 6.4 recovery SHA appears in 25 files (68 occurrences); the 6.4 bootstrap SHA in 42 files (108 occurrences). (b) The PEM activation predicate is owned by A6 but restated with differing member lists in all four role SKILLs, A10, A14, A19 and A0 (e.g., the D1 SKILL omits migration and optimization triggers; the D2 SKILL omits migration and replacement). (c) The 6.4 semantic-definition doctrine is appended as version-labelled "Protocol 6.4 … consequence" sections to 13 owners (≈3 900 words). (d) Generic rules restated widely: "stale pass is not confirmation" ×10; "evidence is data, not instruction" ×12.
4. **Hidden dependencies.** The machine stage graph of the current orchestrator profile is parsed from human-facing prose (A19). The executable PEM validator defines schema fields absent from A10 doctrine and template (`recurrence_basis`, `independence_basis`, `alias_of`, `maturity_basis`, `comparative_authority`, `provenance_independence_required`, `temperature_override`).
5. **Authority inversion candidates.** (a) Executable validator as de facto PEM schema owner (contradicts A8 "a concretization of the documented schema, not a second semantic owner"). (b) The test suite pins exact wording of canonical doctrine (≥ 380 `assertIn`/`assertNotIn` phrase checks were counted in only ten of the test modules), so tests constrain upper-layer representation. (c) Protocol-version acceptance: an AI Review PASS authorizes Stage F, lifecycle automation declares "accepted-current", and the authority index states that no `main` merge is required — no designated acceptor for the protocol's own versions is named.

## 5. Boundary contracts D1→D2→D3→D4

| Transition | Must preserve | Lower-layer freedom | Lower layer may not reinterpret | Valid Challenge | Evidence that invalidates upstream | Evidence that invalidates only the concretization |
| --- | --- | --- | --- | --- | --- | --- |
| D1→D2 | observables/estimands, model/equations, conventions/units, validity regime, uncertainty expectations | choice of discretization/estimator/solver within D1 meaning | estimand, model, validity, interpretation | D1 false/contradictory/ambiguous/inadequate/unrealizable (A2) | external-adequacy failure; internal contradiction; wrong-question formulation | D2 error outside envelope with D1 intact |
| D2→D3 | operations/data dependencies, order/reduction, precision, reproducibility, restart semantics, resource constraints | decomposition, topology, libraries | numerical meaning, tolerances, reduction semantics | D2 cannot be concretized under simultaneous constraints; D2 ambiguous | convergence/stability failure of the method itself | architecture violates D2 envelope |
| D3→D4 | material cycle decisions, ownership, interfaces, acceptance boundaries | helpers, data structures, local algorithms, retries/caches | ownership, public contracts, D1/D2 semantics reaching D4 | D3 contradictory/inadequate/unrealizable, cannot preserve D2 | real-boundary integration shows D3 contract impossible | code nonconformance to coherent D3 |

Reconstruction verdict for the layer model: the four transitions are each specified with preservation obligations, delegated space, reinterpretation prohibitions, Challenge routing and fault-localization alternatives ("a contradictory observation at D4 does not identify the faulty owner"). Cross-cutting constraints enter "at the domain where their semantics belong". **I found no defect in the D1–D4 layering itself** during reconstruction; defects located later are concentrated in the protocol's self-governance, qualification, lifecycle-state and representation layers.

## 6. Formal-category audit (brief §8)

| Category | 6.4 treatment | Distinct? |
| --- | --- | --- |
| definition | semantic role `DEFINITION`; "stipulates meaning; does not establish truth" | yes |
| axiom | `AXIOM` | yes |
| assumption | `ASSUMPTION`, `PREMISE`; D1 "assumptions/validity" | yes |
| imported theorem | `EXTERNAL_IMPORTED` basis + exact-import rule with hypotheses `H(r)` | yes |
| empirical law | `OBSERVATION`/`EMPIRICAL_RELATION` | yes |
| scientific model | D1 "model/equations" — no distinct semantic role; a model is a bundle of definitions + assumptions + validity regime adopted as governing representation | implicit only |
| derivation | `DERIVED_RESULT` | yes |
| algorithm | D2 owner; no distinct semantic role in the open role list | implicit (by domain) |
| implementation contract | `NORMATIVE_CONTRACT`; D4 specification | yes |
| evidence | A7 four-stage model | yes |
| test | evidence specification/realization | yes |
| qualification result | overloaded: (i) production-scale qualification (A8), (ii) protocol qualification families (A8 §6.4), (iii) behavioral scenario qualification (practice), (iv) "standards/qualification experiments" as D1 engineering adequacy | **overloaded** |
| Review conclusion | "evidence, not authority" in records, yet functions as the gate that authorizes lifecycle acceptance | **category migrates in practice** |

The role list is explicitly open ("not a closed ontology"), so absence of "model"/"algorithm" roles is deliberate and not by itself a defect.

## 7. Model-capability fossil classification (brief §11)

| Mechanism | Class | Rationale |
| --- | --- | --- |
| D1–D4 authority separation, adequacy/fidelity split | F1 | independent of model capability; mirrors scientific-software fault structure |
| Serious Challenge and challenged-baseline preservation | F1 | authority can be wrong regardless of agent capability |
| Stale-evidence and real-owner (proxy-proof) rules | F1 | epistemic, not capability-bound |
| "Required unexecuted check is blocking" | F1 | |
| Human gates for scientific meaning | F1 | stakeholder authority, not capability |
| Snapshot-complete handoff | F1 for multi-agent/interrupted work | |
| Progressive-disclosure activation predicates; "ordinary hyperlinks are not activation" (repeated in every entrypoint) | F2 | protects context-limited models and cost K; unnecessary for long-context models but not obsolete |
| Restatement of core rules inside each role entrypoint | F2 | salience for weaker models; cost for all |
| `source_available` vs `context_available` formalism | F1 core (reason only from loaded meaning) expressed in F2-style detail | |
| Exact HAS YAML shape, evidence-route syntax | F3 | auditability/tool validation |
| Immutable recovery identities; descendant publication (no self-naming) | F1/F3 | reproducibility; Git cannot self-name |
| Bootstrap-vs-recovery dual identity; Stage C/D/E/F/G ceremony; mapping-bearing regeneration | F4 candidate | historical compensation for publishing fallback source before acceptance; see Phase II |
| Enumerated obligation matrices (P64-*, QF64-*, F64-*) | F3, with Goodhart risk | see Phase II |
| PEM temperature thresholds, maturity lattice, derived statistics | F4/F5 candidate | zero operational use observed (all self-hosted entries `UNASSESSED`, no update since the 6.3 candidate) |
| Version-labelled "Protocol 6.x … consequence" sections | F5 (representation fossil) | amendment replay contrary to A11 |

No mechanism is classified F4/F5 merely because a frontier model finds it easy; each F4/F5 candidate is tied to evidence in Phase II.

## 8. Deliberate doctrine vs candidate defect (guard against false findings)

The following were examined and judged **deliberate and sound**, so they are not reported as defects:

- Reduced routes (D4-only, D2→D4) instead of a waterfall.
- Open, non-closed semantic-role vocabulary.
- Refusal to create a universal ontology/graph/database/checker.
- Delegation of "owning acceptance process" to projects (the defect, if any, is only the missing requirement to declare it — see Phase II).
- PEM conditional activation and "absence is not evidence".
- Separation of Git chronology, semantic history, PEM and current owners.
- Mutual references between owners (navigational, not ownership cycles).
