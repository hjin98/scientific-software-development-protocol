# Scientific Software Development Protocol

**Build scientific software that stays scientifically correct while the software, algorithms, hardware, and team evolve.**

The Scientific Software Development Protocol (SSDP) is a set of portable AI-agent skills plus an engineering doctrine for designing, implementing, reviewing, and maintaining scientific software. Its central idea is simple: **separate what must be true from the mechanism that happens to implement it today**.

That separation lets you improve code aggressively without silently changing the scientific model, numerical method, architecture, or public behavior you meant to preserve.

> **Release-state note:** this README is a user guide, not release authority. Current accepted version, candidate, Review, ratification, public-source fallback, and recovery identities are owned only by [`PROTOCOL-RELEASE-STATE.yaml`](PROTOCOL-RELEASE-STATE.yaml).

## The idea in one minute

SSDP asks you to do seven things well:

1. **Start at the right semantic layer.** Change the earliest/highest layer whose meaning actually changes.
2. **State invariants before mechanisms.** Define the scientific, numerical, architectural, and behavioral truths that descendants must preserve.
3. **Concretize downward.** Choose lower-level solutions only inside the feasible set allowed by their parents.
4. **Verify upward.** Reconstruct what the implementation actually does and attempt to falsify conformity with every applicable parent.
5. **Challenge bad authority instead of patching around it.** If the governing model, method, or architecture is wrong or unrealizable, escalate the defect to its real owner.
6. **Prefer active simplicity.** Remove, narrow, consolidate, or redesign delegated machinery before adding wrappers, special cases, duplicated state, or another control plane.
7. **Treat evidence as evidence, not truth by repetition.** Tests, benchmarks, reviews, history, and project memory support decisions; they do not become semantic authority merely because they exist or are green.

A useful shorthand is:

```text
meaning changed?        -> move upward to the earliest affected owner
mechanism changed only? -> stay at the lower layer and preserve the contract
```

## The abstraction -> concretization hierarchy

SSDP separates four semantic authority domains:

```text
D1  scientific/mathematical formulation
      |  what phenomenon, model, observable, assumptions, validity?
      v
D2  algorithm/numerical method
      |  what approximation, estimator, discretization, error, precision?
      v
D3  software architecture
      |  what components, state, interfaces, data/control flow, resources?
      v
D4  specification/implementation
         what concrete behavior, code, tests, packaging, operations?
```

This is **semantic ordering, not a mandatory waterfall**. A local implementation bug may be D4-only. A new solver may require D2->D4. A new physical model may require the full D1->D4 path.

| Domain | Governing question | Typical durable artifact | Skill |
| --- | --- | --- | --- |
| **D1** | Are we solving the right scientific/mathematical problem? | Scientific Method Paper / formulation authority | `scientific-formulation` |
| **D2** | Is the numerical method faithful, stable, convergent, and sufficiently accurate? | Numerical & Algorithmic Method Paper | `numerical-algorithm-design` |
| **D3** | Does the architecture preserve D1/D2 while remaining reliable and simple? | Architecture Manual / D3->D4 workplan | `software-design` |
| **D4** | Does the executable system implement the accepted contracts correctly? | Specification + code + tests + packaging | `software-implementation` |

A concretization is admissible only when it preserves every applicable parent abstraction and governed side constraint. Among admissible choices, SSDP prefers:

```text
domain engineering fitness
> minimum justified total system complexity
> development economy
```

## The skills

The portable runtime unit is `dist/skills/<skill-name>/`; top-level ZIPs contain the same skill bundles for transport. Use your agent/harness's normal installed-skill mechanism to invoke a skill by name.

### Authority-bearing roles

| Skill | Use it when... |
| --- | --- |
| `scientific-formulation` | defining or changing the scientific question, observables, model/equations, assumptions, validity regime, interpretation, or external adequacy |
| `numerical-algorithm-design` | defining or changing discretization, estimator, optimizer, approximation, convergence, conditioning, precision, stochastic semantics, tolerances, or numerical uncertainty |
| `software-design` | designing/reviewing architecture, ownership, interfaces, data/control flow, persistence, concurrency, resources, compatibility, or an implementation workplan |
| `software-implementation` | implementing, refactoring, debugging, testing, packaging, or validating a D4 concretization under accepted D1-D3 authority |

### Optional specialists

| Skill | Purpose |
| --- | --- |
| `software-documentation` | make accepted science/software understandable without turning documentation into new authority |
| `software-maintenance-audit` | inspect long-horizon architectural entropy, weak tests, dependency drift, duplicated authority, change-risk concentration, and maintainability deterioration |
| `repository-hygiene` | conservative post-stage cleanup while preserving recoverable work, evidence, history, protected refs, and accepted state |

**You do not need every skill for every change.** Use the smallest set that covers the semantics you are actually changing.

## Quick start

### 1. Install or expose the skills

Use the ready-to-install bundle under `dist/skills/` or the corresponding ZIP for your agent environment. See [`PORTABILITY.md`](PORTABILITY.md) for the exact packaging and routing contract.

### 2. Start with the earliest affected domain

For a new scientific codebase, the full path is usually D1 -> D2 -> D3 -> D4. For an existing codebase, classify the change before doing work.

Examples:

```text
New physical/statistical model      -> D1, then D2/D3/D4 as needed
New discretization or estimator     -> D2, then D3/D4
Architecture or subsystem redesign  -> D3, then D4
Local bug with unchanged contracts  -> D4
Performance work                    -> D2/D3/D4 depending on whether numerics or architecture change
Numerical discrepancy               -> investigate D4, D3, D2, then D1; do not assume the bug is in code
```

### 3. Ask the skill to produce the next governed artifact

Example prompts you can paste into an agent:

```text
Use the scientific-formulation skill. Define the scientific problem, observables, assumptions, validity regime, uncertainty, and falsification/validation requirements for this project. Produce the minimum D1 authority needed for downstream numerical design.
```

```text
Use the numerical-algorithm-design skill. Starting from the accepted D1 formulation, define the numerical method, approximation/error model, convergence and conditioning expectations, precision/stochastic semantics, verification oracles, and the minimum D2->D3 handoff.
```

```text
Use the software-design skill. Starting from the accepted D1/D2 authority, design the minimum justified architecture and produce a D3->D4 implementation workplan with ownership, interfaces, constraints, acceptance boundaries, non-goals, and reopen triggers.
```

```text
Use the software-implementation skill. Implement the accepted workplan, preserve D1-D3 invariants, keep delegated machinery simple, run affected regression/integration at the real semantic-owner boundary, and report blockers rather than weakening the contract.
```

```text
Use the software-design skill in independent Review mode. Reconstruct the governing authority independently, perform the Challenge Pass first, review the assembled implementation rather than only the diff, falsify conformance and abstraction adequacy, and issue Pass/No-Pass only on genuine blockers.
```

## A practical development cycle

### Step 0 — Classify the change

Before editing code, ask: **what meaning can this change alter?** Start at the earliest affected D1-D4 owner. Do not reopen higher layers merely because many files are changing, and do not keep work artificially at D4 when the numerical or scientific semantics are actually changing.

### Step 1 — Define the parent contract

At the owning domain, state the minimum durable truths that descendants must preserve. Good authority defines outcomes, invariants, assumptions, validity, error/equivalence semantics, ownership, or observable behavior. It does **not** freeze incidental helpers, libraries, wrappers, call graphs, or file layout unless those details are genuinely governed.

### Step 2 — Design inside the admissible set

Enumerate enough alternatives to expose the real tradeoff, then choose the simplest admissible concretization. Prefer one authoritative representation/state, cohesive ownership, direct flow, understandable dependencies, and established language/library mechanisms.

Do not add a compensating layer when removing or rewiring the underlying cause is cleaner.

### Step 3 — Define evidence before claiming success

Evidence has its own lifecycle:

```text
governed claim
 -> evidence specification
 -> evidence realization
 -> observation
 -> evidence assessment
```

Design evidence that can actually discriminate the claim. A helper-level unit test cannot prove an orchestrator path works when orchestration is part of the claim. A benchmark does not prove scientific correctness. A stale pass is not current confirmation.

For scientific/numerical work, use the strongest applicable combination of:

- analytical, exact, limiting, or manufactured cases;
- residuals, conservation laws, invariants, and dimensional/type checks;
- refinement/convergence and conditioning/sensitivity studies;
- trusted-reference or differential testing;
- authority-backed metamorphic relations;
- precision/backend/seed robustness;
- real-boundary integration/end-to-end tests;
- bounded deterministic fault injection for recovery/failure claims;
- production-scale evidence only when scale itself is part of the claim.

Floating tolerances come from D2 error/conditioning/precision semantics—not from widening a threshold until the test passes.

### Step 4 — Implement adaptively

Implementation is allowed to improve the mechanism as long as it preserves accepted semantics. Refactor, consolidate, replace, or delete delegated machinery freely when that lowers total complexity and does not violate the parent contract.

Green tests do not authorize a semantic change. Failing tests do not authorize weakening the oracle.

### Step 5 — Review upward, not just sideways

A material Review checks two independent questions:

1. **Concretization fidelity:** does the child satisfy its parents and side constraints?
2. **Abstraction adequacy:** is the parent contract itself strong enough to prevent a locally compliant but globally wrong child?

Every material Review includes a bounded **Challenge Pass**. If accepted authority may itself be false, contradictory, materially ambiguous, inadequate, or unrealizable, raise a **SERIOUS CHALLENGE** at the earliest affected owner instead of patching around it.

### Step 6 — Close impact, documentation, and history

After a material change:

- rerun/remap only evidence whose applicability changed;
- preserve unaffected siblings and still-valid evidence;
- update current documentation to explain the present system, not patch chronology;
- record concise semantic evolution when future rediscovery is plausible;
- update Project Engineering Memory only when reusable project learning meets its admission threshold;
- archive or clean up temporary machinery only after current semantics/evidence remain recoverable.

## Common usage patterns

### Greenfield scientific package

Use D1 -> D2 -> D3 -> D4. Define science first, then numerical semantics, then architecture, then code. Do not let the first implementation accidentally define the method.

### Local bug fix

If D1-D3 and public D4 contracts are unchanged, stay at D4. Fix the owning cause, run focused tests plus affected regression/integration, and stop. SSDP is not a mandate for ceremony.

### Numerical disagreement or suspicious result

Do not immediately patch code. Reconstruct the chain:

```text
D4 executable behavior
 -> D3 state/data/control semantics
 -> D2 numerical error/equivalence envelope
 -> D1 scientific meaning and validity
```

Locate the earliest faulty owner. A scientifically wrong model cannot be repaired by a software workaround.

### Performance optimization

First decide whether the optimization changes numerical semantics. If precision, reduction order, approximation, stochastic behavior, or convergence changes, involve D2. If ownership/data movement/concurrency/resources change materially, involve D3. Otherwise keep the optimization at D4 and verify final governed observables.

### Replacing a mature subsystem

Use `software-design`; activate Project Engineering Memory when prior project history can materially change the decision. Build a capability-transfer map so useful properties survive even when the historical mechanism does not.

### Release or high-risk integration

Freeze an exact candidate, qualify the real assembled system, perform fresh independent Review, resolve any Serious Challenge, obtain whatever human ratification the project requires, and only then publish/cut over according to the project's release authority.

## Project Engineering Memory: use history without becoming trapped by it

Project Engineering Memory (PEM) is evidence-backed, project-local learning. It is **not D5** and cannot override D1-D4 authority.

Activate PEM when demonstrated project history can materially change a decision—for example:

- substantial mature rework or replacement;
- suspected recurrence after an accepted repair;
- substantial optimization/scaling;
- migration, recovery, revert, or restoration;
- an active workplan explicitly bound to project history.

Keep PEM cold for a first clean local bug or unrelated task. Memory is a hypothesis index and decision aid, not a leaderboard of old solutions.

## Doctrines worth remembering

- **One semantic owner per material current claim.** Tests, generated views, history, and documentation do not become parallel owners.
- **Authority and evidence are different.** Evidence can support or challenge authority; it does not become authority through repetition.
- **Current code is not automatically the intended contract.** When code and accepted specification disagree, classify the defect before editing authority.
- **Compatibility is a real contract, not an archaeological obligation.** Preserve it only where actually supported.
- **History explains why; current owners explain what is true.** Keep chronology discoverable but out of the hot path.
- **Lossless representation beats append-only documentation.** Rewrite current guidance coherently rather than stacking amendments.
- **Progressive disclosure beats loading everything.** The active skill routes only to concern owners that matter for the decision.
- **Simple is not the same as weak.** Simplify mechanisms aggressively; never simplify by weakening governing semantics.

## What changed over time?

SSDP evolved from a software-engineering protocol into a scientific-software authority/evidence system. The important capability milestones are:

| Version | Main improvement |
| --- | --- |
| **5.13** | deterministic tool entry, CodeQL/tool routing, progressive disclosure |
| **5.14** | solution-boundary discipline and active simplicity |
| **5.15** | language profiles and cross-language performance engineering |
| **5.16** | long-horizon health, Verification/Stabilization, maintenance audit, workflow prompts, public fallback |
| **6.0** | generalized the software-only model into first-class D1-D4 scientific software authority |
| **6.1** | separated concretization from evidence realization; strengthened evidence lifecycle, dependency/impact closure, and human-facing technical writing |
| **6.2** | Lossless Representation and progressive-disclosure strengthening |
| **6.3** | Project Engineering Memory and Historical Applicability Sets as non-authoritative project learning |
| **6.4** | definition/source availability, well-defined formal contracts, parameter family/instance/default semantics, exact imports, typed semantic dependencies, and claim/warrant discipline |
| **6.5** | self-governance/release-state strengthening: mutable lifecycle state separated from immutable semantics, sharper Review-vs-ratification boundaries, evidence-claim congruence, out-of-matrix Review, and hardened durable Git/evidence realization |

For the full user-facing capability history, see [`CHANGELOG.md`](CHANGELOG.md). For detailed semantic rationale and superseded release attempts, see [`history/SEMANTIC_EVOLUTION.md`](history/SEMANTIC_EVOLUTION.md). Exact mutable release mappings remain in [`PROTOCOL-RELEASE-STATE.yaml`](PROTOCOL-RELEASE-STATE.yaml).

## Repository map

| Path | Meaning |
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

## Contributing to the protocol repository

The root guide is non-authoritative. Canonical protocol semantics live under `source/`. Generated distributions and orchestrator snapshots are derivatives.

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

**The operating principle:** make the science explicit, make the numerical contract explicit, keep the architecture simple, let implementation stay adaptive, and demand evidence strong enough to justify the claim you are making.
