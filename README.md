# Scientific Software Development Protocol

Current protocol version: **6.0**.

Protocol 6 generalizes the former Software Development Protocol into a recursive scientific-software development system:

```text
ABSTRACTION  --design / constrain-->  REALIZATION
ABSTRACTION  <--verify / reconstruct-- REALIZATION
```

An abstraction states the semantic invariants that must survive realization. A realization is admissible only when it satisfies every applicable upstream abstraction and governed external constraint. Within that feasible set optimize:

```text
domain engineering fitness
> minimum justified realization complexity
> development economy
```

## Four semantic domains

```text
D1  scientific-formulation
     Scientific & Mathematical Formulation
        |
D2  numerical-algorithm-design
     Algorithm & Numerical Methods
        |
D3  software-design
     Software Architecture
        |
D4  software-implementation
     Specification & executable implementation
```

This is a semantic hierarchy, not a mandatory four-stage waterfall. D4-only and D3->D4 work are normal when upstream meaning is unaffected; multi-parent constraints form a layered DAG.

Logical normative document families are D1 Scientific Method Paper, D2 Numerical & Algorithmic Method Paper, D3 Architecture Manual, and D4 Specification plus code/executable realization. Each material current normative claim has one semantic owner. Proposed, accepted-current, challenged, stale-dependent, superseded/historical, and release-pinned/publication states remain distinct.

## Verification and challenge

Verification reconstructs realization semantics and attempts to falsify conformity. It is opposite-direction reasoning, not a bijective inverse. Every material handoff checks both realization fidelity and abstraction adequacy. High-risk scientific claims may require composed closure:

```text
actual executable behavior
 -> governed numerical observables
 -> D2 error/equivalence envelope
 -> D1 scientific/mathematical meaning
 -> external adequacy / validation / proof / standards evidence
```

Every material Review includes a bounded **Challenge Pass**. A child that fails a coherent parent has an ordinary blocker. Strong evidence that accepted authority itself is materially false, contradictory, ambiguous, inadequate, or unrealizable produces a prominent **SERIOUS CHALLENGE** and human adjudication rather than silent compliance or downstream patching.

Authority governs mutation; evidence can challenge authority; neither human nor agent creates truth by assertion.

## Preserved engineering strengths

Protocol 6 preserves and generalizes Protocol 5's strongest controls: adaptive realization, active simplification, snapshot-complete handoff, version-bound workplans, stage-local plus final affected regression, proxy-proof real-owner evidence, evidence reuse/invalidation, differential/metamorphic testing, bounded fault injection, language/tool routing, long-horizon health sensing, and conservative closeout.

## Workflow and portable skills

Canonical human-facing orchestration prompts:

- [`source/shared/references/development-workflow-prompts.md`](source/shared/references/development-workflow-prompts.md)

Canonical role entrypoints:

- `source/roles/scientific-formulation/SKILL.md`
- `source/roles/numerical-algorithm-design/SKILL.md`
- `source/roles/software-design/SKILL.md`
- `source/roles/software-implementation/SKILL.md`

Optional specialists remain non-authoritative support capabilities: `software-documentation`, `software-maintenance-audit`, and `repository-hygiene`.

Skill resolution is compatible-local-first, canonical-public-source-second. Never silently reinterpret an older workplan under newer doctrine. Historical Protocol 5.16 is pinned to immutable commit `e151daaf5c8eebb351a85cfed86170fda80fb5e3` and the orchestrator retains its packaged `sdp-protocol-5.16` schema-v1 profile alongside current `ssdp-protocol-6.0` schema v2.

## Build and acceptance

`source/` is canonical. `dist/skills/` and top-level ZIPs are generated transport artifacts.

```bash
python -m pip install -r source/requirements-validation.txt
python -m unittest discover -s tests -v
python source/build_skills.py --output /tmp/protocol-dist
python source/validate_packages.py --dist /tmp/protocol-dist
python source/check_dist.py --expected /tmp/protocol-dist --committed dist
git diff --check

python -m pip install ./orchestrator -r orchestrator/requirements-dev.txt
python orchestrator/scripts/generate_protocol_snapshot.py --check
python orchestrator/scripts/run_core_tests.py
```

These Python commands are repository-local Tier-2 validation machinery in the historical Protocol 5 terminology—delegated D4 validation machinery under Protocol 6—not language-specific protocol doctrine.

A Protocol 6 release is not complete while a governing Serious Challenge is unresolved or any required assembled acceptance check has not executed.
