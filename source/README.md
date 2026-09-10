# Scientific Software Development Protocol 6.2

`source/` is the canonical Protocol 6.2 source. Generated distributions and orchestrator snapshots are derivatives.

## Governing model

The Scientific Software Development Protocol (SSDP) separates D1 scientific/mathematical formulation, D2 algorithm/numerical method, D3 software architecture, and D4 specification/implementation. Read `shared/references/abstraction-and-concretization.md` for the universal authority, Challenge, and Lossless Representation rules.

A concretization is admissible only when it satisfies every applicable parent abstraction and directly governed constraint. Within the admissible set optimize domain engineering fitness, then minimum justified concretization complexity, then development economy. The D1->D4 relation is semantic, not a mandatory waterfall; reduced routes are normal when higher/intermediate semantics are unaffected.

## Authority-bearing roles

- D1: `roles/scientific-formulation/SKILL.md`
- D2: `roles/numerical-algorithm-design/SKILL.md`
- D3: `roles/software-design/SKILL.md`
- D4: `roles/software-implementation/SKILL.md`

Optional specialists: `software-documentation`, `software-maintenance-audit`, `repository-hygiene`. They support the lifecycle but do not create approval authority.

Logical normative families are D1 Scientific Method Paper, D2 Numerical & Algorithmic Method Paper, D3 Architecture Manual, and D4 Specification + executable concretization. Each material current normative claim has one semantic owner.

## Progressive-disclosure owner map

Load the role entrypoint plus universal kernel/owning domain, then only concern owners whose decision predicates fire. Ordinary hyperlinks, semantic dependency and package membership do not imply activation.

- universal authority / Challenge / representation -> `shared/references/abstraction-and-concretization.md`
- D1 -> `shared/references/scientific-formulation.md`
- D2 -> `shared/references/numerical-algorithm-design.md`
- D3 -> `shared/references/architecture-and-design.md`
- D4 -> `shared/references/specification-and-implementation.md`
- workflow/handoff -> `shared/references/workflow-and-workplans.md`
- evidence/evolution/dependency -> `shared/references/evidence-evolution-and-dependencies.md`
- testing/validation -> `shared/references/testing-and-validation.md`
- convergence/simplification -> `shared/references/convergence-and-cycle-economy.md`
- long-horizon health -> `shared/references/long-horizon-code-health.md`
- document lifecycle -> `shared/references/documentation-maintenance.md`
- technical writing -> `shared/references/scientific-technical-writing.md`
- version/recovery -> `shared/references/protocol-versioning-and-compatibility.md`
- language concern router -> `shared/references/language-profiles.md`
- relation/tool concern router -> `shared/references/tool-assisted-engineering.md`
- workflow prompts -> `shared/references/development-workflow-prompts.md`

Other security/performance/storage/configuration/concurrency/release/debugging/Git/repository concerns remain direct canonical owners and activate only when material.

## Lossless representation

Protocol 6.2 preserves every accepted Protocol 6.1 doctrine and still-valid historical capability while reducing repeated doctrine, amendment replay, unnecessary context and routing cost. Completeness is prerequisite; compactness never permits scope narrowing or information loss. Current documents state present truth; detailed chronology remains recoverable through semantic history and immutable version sources.

Current path uses `abstraction-and-concretization.md`. Historical 5.16/6.0/6.1 files/profiles retain their original identifiers/bytes under immutable recovery mappings.

## Build and acceptance

```bash
python -m pip install -r source/requirements-validation.txt
python -m unittest discover -s tests -v
python source/build_skills.py --output /tmp/protocol-dist
python source/validate_packages.py --dist /tmp/protocol-dist
python source/check_dist.py --expected /tmp/protocol-dist --committed dist
git diff --check
```

When orchestrator/profile resources change, also run snapshot parity and the Orchestrator Core suite. A required check that did not execute is blocking, not a pass.
