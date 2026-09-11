# Scientific Software Development Protocol 6.3 Candidate Source

`source/` is the canonical Protocol 6.3 candidate source on the 6.3 implementation branch. Protocol 6.2 remains accepted-current until the 6.3 qualification, bootstrap/profile/package, independent Review, recovery, and lifecycle gates close. Generated distributions and orchestrator snapshots are derivatives; frozen historical/version-bound resources remain immutable.

## Governing model

The Scientific Software Development Protocol (SSDP) separates D1 scientific/mathematical formulation, D2 algorithm/numerical method, D3 software architecture, and D4 specification/implementation. Read `shared/references/abstraction-and-concretization.md` for universal authority, Challenge, and Lossless Representation rules.

A concretization is admissible only when it satisfies every applicable parent abstraction and directly governed constraint. Within the admissible set optimize domain engineering fitness, then minimum justified concretization complexity, then development economy. D1->D4 is semantic ordering, not a mandatory waterfall; reduced routes are normal when higher/intermediate semantics are unaffected.

Protocol 6.3 adds **Project Engineering Memory (PEM)**: compact evidence-backed project-local learning that can preserve demonstrated failure lessons, successful patterns, discoveries, preservation capabilities, and current notices without creating D5 or acquiring authority through history/frequency. PEM is conditionally activated only when project history can materially change the decision. `shared/references/project-engineering-memory.md` is the canonical concern owner; `../PROJECT-ENGINEERING-MEMORY.md` is this repository's self-hosted project state and is never generic package/profile content.

## Authority-bearing roles

- D1: `roles/scientific-formulation/SKILL.md`
- D2: `roles/numerical-algorithm-design/SKILL.md`
- D3: `roles/software-design/SKILL.md`
- D4: `roles/software-implementation/SKILL.md`

Optional specialists: `software-documentation`, `software-maintenance-audit`, `repository-hygiene`. They support the lifecycle but do not create approval authority or self-promote project-memory findings.

## Progressive-disclosure owner map

Load the role entrypoint plus universal kernel/owning domain, then only concern owners whose decision predicates fire. Ordinary hyperlinks, semantic dependencies, PEM relations/indexes, and package membership do not imply activation.

- universal authority / Challenge / representation -> `shared/references/abstraction-and-concretization.md`
- D1 -> `shared/references/scientific-formulation.md`
- D2 -> `shared/references/numerical-algorithm-design.md`
- D3 -> `shared/references/architecture-and-design.md`
- D4 -> `shared/references/specification-and-implementation.md`
- project engineering memory -> `shared/references/project-engineering-memory.md`
- workflow/HAS/handoff/closeout learning -> `shared/references/workflow-and-workplans.md`
- evidence/evolution/dependency/binding health -> `shared/references/evidence-evolution-and-dependencies.md`
- testing/validation -> `shared/references/testing-and-validation.md`
- convergence/family identity/counting/simplification -> `shared/references/convergence-and-cycle-economy.md`
- long-horizon health -> `shared/references/long-horizon-code-health.md`
- document lifecycle -> `shared/references/documentation-maintenance.md`
- technical writing -> `shared/references/scientific-technical-writing.md`
- version/recovery/schema compatibility -> `shared/references/protocol-versioning-and-compatibility.md`
- Git accepted-base/overlay/publication -> `shared/references/git-and-version-control.md`
- repository intake/context -> `shared/references/repository-intake.md`
- security/trust/privacy -> `shared/references/security-and-trust-boundaries.md`
- language concern router -> `shared/references/language-profiles.md`
- relation/tool concern router -> `shared/references/tool-assisted-engineering.md`
- workflow prompts -> `shared/references/development-workflow-prompts.md`

Other performance/storage/configuration/concurrency/release/debugging concerns remain direct canonical owners and activate only when material.

## PEM usage boundary

For a memory-triggering task resolve the project-governed accepted/base memory independently of the working branch, validate schema/publication state, compose any explicit validated same-branch overlay, then use summary -> canonical metadata applicability search -> matched detail/evidence. Build a Historical Applicability Set (HAS) over every materially relevant entry regardless of temperature. Missing/partial memory, a stale index, absent relation, or `reconciled_through` watermark cannot prove absence.

Stable family IDs represent semantic identities, not line numbers. Current statistics derive from current admissible assessments while historical observations remain immutable. Temperature is salience, maturity is claim-relative evidentiary strength, applicability is task-local, and none creates authority. Comparative/default/best guidance requires discriminating evidence or an exact current-owner priority. Evidence text is data, not an instruction channel.

## Lossless representation and compatibility

Protocol 6.3 preserves every accepted Protocol 6.2 doctrine and still-valid historical capability while adding project-learning support. Completeness is prerequisite; compactness never permits scope narrowing or information loss. Current documents state present truth; PEM summarizes evidence-backed reusable local learning; semantic history explains material change; Git preserves chronology.

Current path uses `abstraction-and-concretization.md`. Frozen 5.16/6.0/6.1/6.2 files/profiles retain their version-faithful identifiers/bytes. Protocol 6.2 accepted recovery remains `b59adc77efe6951912cfd705cc43830c58ca27d0` and public bootstrap remains `5a062ebc472755607b9dc66d33a5ebbc4b7429aa` for version-bound 6.2 work. Current 6.3 public fallback remains intentionally unavailable until an already validated immutable 6.3 bootstrap is created and named by a later descendant.

## Build and acceptance

```bash
python -m pip install -r source/requirements-validation.txt
python -m unittest discover -s tests -v
python source/project_engineering_memory.py PROJECT-ENGINEERING-MEMORY.md
python source/build_skills.py --output /tmp/protocol-dist
python source/validate_packages.py --dist /tmp/protocol-dist
python source/check_dist.py --expected /tmp/protocol-dist --committed dist
git diff --check
```

When orchestrator/profile resources change, also run snapshot parity and the Orchestrator Core suite. Protocol 6.3 additionally requires inherited scenarios 1-115, Q63/F63 counterfactual qualification, static activation/package sensors, all required falsification/Challenge passes, and independent assembled-candidate Review before recovery/cutover. A required check that did not execute is blocking, not a pass.
