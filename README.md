# Scientific Software Development Protocol

**Build scientific software that stays scientifically correct as the code, algorithms, hardware, and team evolve.**

The Scientific Software Development Protocol (SSDP) is a set of portable skills for AI coding agents, backed by an engineering doctrine for scientific software. It helps you separate **what must remain true** from **how the software happens to achieve it today**.

That distinction is the core of the protocol. Scientific models, numerical methods, architecture, and public behavior should be explicit enough to protect. Implementation details should remain free to improve.

> **Release-state note:** this README is a user guide, not release authority. Current accepted version, candidate, Review, ratification, public-source fallback, and recovery identities are owned only by [PROTOCOL-RELEASE-STATE.yaml](PROTOCOL-RELEASE-STATE.yaml).

## Start here

If you remember only six ideas, remember these:

1. **Start at the earliest layer whose meaning changes.** A code change is not always just a code change.
2. **Write down the contract before choosing the mechanism.** Protect scientific, numerical, architectural, and behavioral invariants explicitly.
3. **Design downward, verify upward.** Lower layers must preserve higher-layer meaning; review reconstructs what the implementation actually does.
4. **Challenge a bad contract instead of patching around it.** If the governing model, method, or architecture is wrong, ambiguous, or unrealizable, route the problem to its real owner.
5. **Prefer the simplest admissible system.** Remove, narrow, consolidate, or redesign delegated machinery before adding wrappers, fallback paths, duplicated state, or special cases.
6. **Spend rigor where it changes the decision.** Mandatory obligations stay mandatory, but analysis/evidence depth should track consequence and unresolved uncertainty rather than treating every detail like a research problem.

A useful rule of thumb is:

```text
meaning changed?        -> move upward to the earliest affected owner
mechanism changed only? -> stay lower and preserve the accepted contract
```

SSDP is deliberately not a ceremony generator. A clean local bug may need only D4 implementation work. A new physical model may require the full D1->D4 chain.

## The abstraction -> concretization model

An **abstraction** states the material meaning and invariants that descendants must preserve. A **concretization** is a lower-level choice that satisfies those constraints.

SSDP separates four semantic authority domains:

```text
D1  scientific/mathematical formulation
      |  What are we modeling, measuring, assuming, and claiming?
      v
D2  algorithm/numerical method
      |  How is that meaning approximated or computed, and with what error?
      v
D3  software architecture
      |  How are responsibilities, state, interfaces, and resources organized?
      v
D4  specification/implementation
         What concrete behavior, code, tests, packaging, and operations realize it?
```

This is **semantic ordering, not a mandatory waterfall**.

| Domain | Main question | Typical durable artifact | Skill |
| --- | --- | --- | --- |
| **D1** | Are we solving the right scientific or mathematical problem? | Scientific Method Paper / formulation authority | `scientific-formulation` |
| **D2** | Is the numerical method faithful, stable, convergent, and sufficiently accurate? | Numerical & Algorithmic Method Paper | `numerical-algorithm-design` |
| **D3** | Does the architecture preserve D1/D2 while remaining reliable and understandable? | Architecture Manual / D3->D4 workplan | `software-design` |
| **D4** | Does the executable system implement the accepted contracts correctly? | Specification + code + tests + packaging | `software-implementation` |

A concretization is admissible only when it preserves every applicable parent abstraction and governed side constraint. Among admissible choices, SSDP prefers:

```text
domain engineering fitness
> minimum justified total system complexity
> development economy
```

In plain language: first be correct for the scientific/engineering problem, then be as simple as the problem allows, then optimize development effort.

## Which skill should I use?

Use the smallest set of skills that covers the semantics you are actually changing.

| Skill | Use it when you are... |
| --- | --- |
| `scientific-formulation` | defining or changing the scientific question, observables, equations/model, assumptions, validity regime, interpretation, or external adequacy |
| `numerical-algorithm-design` | defining or changing discretization, estimator, optimizer, approximation, convergence, conditioning, precision, stochastic semantics, tolerances, or numerical uncertainty |
| `software-design` | designing or reviewing architecture, ownership, interfaces, state, data/control flow, persistence, concurrency, resources, compatibility, or an implementation workplan |
| `software-implementation` | implementing, refactoring, debugging, testing, packaging, or validating code under accepted D1-D3 authority |
| `software-documentation` | making accepted science/software understandable without turning explanatory prose into new authority |
| `software-maintenance-audit` | inspecting long-horizon architectural entropy, weak tests, duplicated authority, dependency drift, and maintainability risk |
| `repository-hygiene` | cleaning up completed branches/artifacts conservatively after semantic and evidentiary closure |

The first four are authority-bearing D1-D4 roles. The last three are supporting specialists.

The active skill entrypoint controls what context is loaded. Ordinary links and **package membership do not imply activation**; they make material discoverable, not automatically active. The universal routing and authority kernel is [`source/shared/references/abstraction-and-concretization.md`](source/shared/references/abstraction-and-concretization.md).

The portable runtime unit is `dist/skills/<skill-name>/`; top-level ZIPs contain the same bundles for transport. See [PORTABILITY.md](PORTABILITY.md) for installation and routing details.

## Quick start

### 1. Classify the change before editing

Ask one question first:

> **What meaning could this change alter?**

Typical routing:

```text
New physical/statistical model      -> D1, then D2/D3/D4 as needed
New discretization or estimator     -> D2, then D3/D4
Architecture or subsystem redesign  -> D3, then D4
Local bug with unchanged contracts  -> D4
Performance work                    -> D2/D3/D4 depending on what semantics change
Suspicious numerical result         -> investigate D4 -> D3 -> D2 -> D1
```

Do not reopen higher layers merely because many files are changing. Do not keep work artificially at D4 when numerical or scientific meaning is changing.

### 2. Ask the owning skill for the next governed artifact

For a new scientific project:

```text
Use the scientific-formulation skill. Define the scientific problem, observables,
assumptions, validity regime, uncertainty, and falsification/validation requirements.
Produce the minimum D1 authority needed for downstream numerical design.
```

Then:

```text
Use the numerical-algorithm-design skill. Starting from the accepted D1 formulation,
define the numerical method, approximation/error model, convergence and conditioning
expectations, precision/stochastic semantics, verification oracles, and the minimum
D2->D3 handoff.
```

Then:

```text
Use the software-design skill. Starting from the accepted D1/D2 authority, design the
minimum justified architecture and produce a D3->D4 implementation workplan with
ownership, interfaces, constraints, acceptance boundaries, non-goals, and reopen triggers.
```

Then:

```text
Use the software-implementation skill. Implement the accepted workplan, preserve D1-D3
invariants, keep delegated machinery simple, run affected regression/integration at the
real semantic-owner boundary, and report blockers rather than weakening the contract.
```

For a substantial independent implementation Review:

```text
Use the software-design skill in independent Review mode. Reconstruct the governing
authority independently, perform the Challenge Pass first, review the assembled system
rather than only the diff, falsify conformance and abstraction adequacy, and issue
Pass/No-Pass only on genuine blockers.
```

### 3. Allocate attention before escalating rigor

Ask two separate questions:

1. **How important is being wrong here?** Consider consequence, blast radius, reversibility, decision sensitivity, and whether the issue is isolated or systemic.
2. **What should I do next?** Consider mandatory dependencies, unblock value, critical path, information/repair value, and opportunity cost.

Use `DEEP` treatment for consequential unresolved uncertainty; `STANDARD` for focused owner analysis and strong discriminating evidence; `LIGHT` for direct local repair plus focused affected checks; and `DEFER/OMIT` only for non-mandatory low-consequence work.

A high-stakes project does not make every fixture, diagnostic, tolerance, or helper high-stakes. Conversely, a cheap-looking issue should escalate when evidence shows it can materially affect the governing outcome. Use the cheapest sufficiently strong **applicable** evidence and stop when remaining uncertainty cannot change the decision.

### 4. Stop when the governed problem is closed

A task is not improved merely by adding more process. Once the accepted contract is satisfied, affected evidence is current, real integration is checked, material impacts are closed, and no governing Challenge remains, stop. Do not spend resources merely to convert sufficient confidence into psychological certainty.

## The development cycle

### Step 1 — Define the governing contract

At the owning domain, state only the durable truths descendants must preserve.

Good authority defines things such as:

- scientific observables, equations, assumptions, validity, and uncertainty;
- numerical approximation, error, convergence, conditioning, precision, and stochastic semantics;
- architectural ownership, interfaces, state, data/control flow, resources, persistence, and compatibility;
- stable public behavior, formats, errors, defaults, persistence, and supported operation.

Do **not** freeze helpers, wrappers, libraries, call graphs, cache layouts, or other private machinery unless they are genuinely part of the contract.

### Step 2 — Choose the simplest admissible concretization

Explore enough alternatives to expose the real tradeoff, then choose the simplest design that satisfies the governing semantics.

Prefer:

- cohesive ownership;
- one authoritative representation or state;
- direct data/control flow;
- acyclic, understandable dependencies;
- established language/library mechanisms;
- deletion or consolidation over compensating layers.

When a delegated mechanism creates its own problems, first ask whether it should be removed or redesigned.

### Step 3 — Define evidence that can actually test the claim

SSDP keeps evidence separate from authority:

```text
governed claim
 -> evidence specification
 -> evidence realization
 -> observation
 -> evidence assessment
```

A passing test establishes only what its oracle and exercised boundary can discriminate.

For scientific/numerical work, use the strongest applicable combination of analytical or limiting cases, invariants, residuals, refinement/convergence studies, sensitivity/conditioning analysis, trusted-reference comparison, differential or metamorphic testing, precision/backend robustness, real-boundary integration, and production-scale evidence when scale itself matters.

Two rules prevent a large class of false confidence:

- **A stale pass is not current confirmation.**
- **Floating tolerances come from D2 error/conditioning/precision semantics, not from widening a threshold until the test passes.**

A helper-level test cannot prove an orchestrated path works when orchestration is part of the claim. A benchmark cannot prove scientific correctness.

### Step 4 — Implement adaptively

Implementation is allowed to change aggressively inside the accepted envelope.

Refactor, consolidate, replace, or delete delegated machinery when doing so lowers complexity without changing governed meaning. Code, tests, wrappers, caches, state machines, and earlier patches do not become permanent authority simply because the repository depends on them.

Green tests do not authorize a semantic change. Failing tests do not authorize weakening the oracle.

### Step 5 — Review upward

A material Review asks two different questions:

1. **Concretization fidelity:** does the child satisfy every applicable parent and side constraint?
2. **Abstraction adequacy:** is the parent contract strong enough that a locally compliant child cannot still violate the protected upstream meaning?

That second question matters. A perfect implementation of an inadequate contract can still be wrong.

Every material Review includes a bounded **Challenge Pass**. Raise **SERIOUS CHALLENGE** only when accepted authority itself may be materially false, contradictory, ambiguous, inadequate, mutually incompatible, or unrealizable. Otherwise, keep the defect at the lower owning layer.

### Step 6 — Close the affected surface

After a material change:

- rerun or remap only evidence whose applicability changed;
- preserve unaffected siblings and still-valid evidence;
- update current documentation to explain the present system rather than replay patch history;
- record concise semantic evolution when future rediscovery is plausible;
- update Project Engineering Memory only when reusable project learning meets its admission threshold;
- retire temporary machinery only after current semantics, evidence, and recovery paths remain recoverable.

## Common workflows

| Situation | Recommended route |
| --- | --- |
| **Greenfield scientific package** | D1 -> D2 -> D3 -> D4. Define science before code so the first implementation does not accidentally become the method. |
| **Local bug fix** | Stay at D4 if D1-D3 and public D4 contracts are unchanged. Repair the owning cause, run focused checks plus affected regression/integration, and stop. |
| **Suspicious scientific/numerical result** | Reconstruct D4 behavior -> D3 state/data/control -> D2 numerical envelope -> D1 meaning/validity. Locate the earliest faulty owner. |
| **Performance optimization** | Involve D2 if precision, reduction order, approximation, stochastic behavior, or convergence changes. Involve D3 if ownership, data movement, concurrency, or resources change materially. Otherwise remain at D4. |
| **Mature subsystem replacement** | Use `software-design`; activate Project Engineering Memory when project history can materially affect the decision. Preserve useful capability without preserving obsolete machinery. |
| **High-risk integration or release** | Freeze an exact candidate, qualify the real assembled system, perform independent Review, resolve Challenges, obtain required human ratification, then publish/cut over under the project's release authority. |

## Project Engineering Memory: learn from history without being ruled by it

Project Engineering Memory (PEM) is evidence-backed, project-local engineering learning. It is **not D5** and cannot override D1-D4 authority.

Activate PEM only when demonstrated project history can materially change the current decision, such as substantial mature rework, suspected recurrence, major optimization/scaling, migration/recovery/revert/restoration, or a workplan explicitly bound to project history.

Keep PEM cold for a first clean local bug or unrelated task. Memory is a hypothesis index and decision aid, not a vote for whatever succeeded most often in the past.

## Core doctrines

- **One semantic owner per material current claim.** Tests, history, generated views, documentation, and project memory do not become parallel owners.
- **Authority and evidence are different.** Evidence can support or challenge authority; repetition does not turn it into authority.
- **Current code is not automatically the intended contract.** When code and accepted specification disagree, classify the defect before editing authority.
- **Compatibility is a real contract, not an archaeological obligation.** Preserve it where it is actually supported.
- **History explains why; current owners explain what is true.** Keep chronology discoverable but outside the normal hot path.
- **Lossless representation beats amendment accumulation.** Rewrite current guidance coherently instead of stacking exceptions and historical patches.
- **Progressive disclosure beats loading everything.** The active skill loads the concern owners needed for the decision, not the entire protocol library.
- **Simple is not the same as weak.** Simplify mechanisms aggressively; never simplify by weakening governing semantics.
- **Development economy is resource allocation, not aesthetics.** Spend model/human time, tokens, tools, compute, CI, and wall time where uncertainty can change the governed decision; low-value details do not inherit the parent project's scrutiny.

## How the protocol evolved

SSDP began as a software-engineering protocol and grew into a scientific-software authority, evidence, and lifecycle system. Current doctrine preserves useful historical capability without requiring users to learn obsolete control-plane vocabulary.

| Version | Main improvement |
| --- | --- |
| **5.13** | deterministic tool entry, CodeQL/tool routing, progressive disclosure |
| **5.14** | solution-boundary discipline and active simplicity |
| **5.15** | language profiles and cross-language performance engineering |
| **5.16** | long-horizon health, Verification/Stabilization, maintenance audit, workflow prompts, public fallback |
| **6.0** | first-class D1-D4 scientific-software authority |
| **6.1** | clear separation of concretization from evidence realization; stronger evidence lifecycle, impact closure, and technical writing |
| **6.2** | Lossless Representation and progressive-disclosure strengthening |
| **6.3** | Project Engineering Memory and Historical Applicability Sets |
| **6.4** | semantic definition/source availability, well-defined formal contracts, parameter binding, exact imports, typed semantic dependencies, and claim/warrant discipline |
| **6.5** | self-governance/release-state strengthening plus importance-weighted attention, proportional rigor/evidence, evidence-only requalification economy, and release-documentation closeout |

For the full user-facing capability history, see [CHANGELOG.md](CHANGELOG.md). For detailed semantic rationale and superseded release attempts, see [history/SEMANTIC_EVOLUTION.md](history/SEMANTIC_EVOLUTION.md). Exact mutable release mappings remain in [PROTOCOL-RELEASE-STATE.yaml](PROTOCOL-RELEASE-STATE.yaml).

## Repository map

| Path | Purpose |
| --- | --- |
| `source/` | canonical version-intrinsic protocol source |
| `source/roles/` | D1-D4 authority-bearing skill entrypoints |
| `source/specialists/` | optional documentation/audit/hygiene specialists |
| `source/shared/references/` | canonical concern owners loaded by progressive disclosure |
| `dist/skills/` | ready-to-install generated skill bundles |
| `orchestrator/` | version-bound orchestration/profile implementation |
| `PROJECT-ENGINEERING-MEMORY.md` | this repository's project-local memory; not generic protocol authority |
| `PROTOCOL-RELEASE-STATE.yaml` | sole mutable release-state owner |
| `CHANGELOG.md` | user-facing capability evolution |
| `history/SEMANTIC_EVOLUTION.md` | detailed semantic evolution and historical rationale |

## Contributing to this repository

The root README is a guide. Canonical protocol semantics live under `source/`; generated distributions and orchestrator snapshots are derivatives.

Repository acceptance commands:

```bash
python -m pip install -r source/requirements-validation.txt
python -m unittest discover -s tests -v
python source/release_state.py
python source/project_engineering_memory.py PROJECT-ENGINEERING-MEMORY.md
python source/build_skills.py --output /tmp/protocol-dist
python source/validate_packages.py --dist /tmp/protocol-dist
python source/check_dist.py --expected /tmp/protocol-dist --committed dist
git diff --check

python -m pip install ./orchestrator -r orchestrator/requirements-dev.txt
python orchestrator/scripts/generate_protocol_snapshot.py --check
python orchestrator/scripts/run_core_tests.py
```

Mechanical qualification establishes only the property its oracle actually discriminates. Semantic adequacy still requires appropriate independent Review of the assembled candidate.

---

**Operating principle:** make the science explicit, make the numerical contract explicit, keep the architecture simple, let implementation stay adaptive, and demand evidence strong enough to justify the claim.
