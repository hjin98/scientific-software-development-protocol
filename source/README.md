# Scientific Software Development Protocol 6.1

This directory is the canonical Protocol 6 source.

## Governing model

Read `shared/references/abstraction-and-realization.md` first. Protocol 6 treats scientific software as recursively constrained concretization across D1 scientific formulation, D2 algorithm/numerical method, D3 software architecture, and D4 specification/implementation.

A child is admissible only when its actual semantics satisfy every applicable parent abstraction and governed external constraint. Fidelity is a hard feasibility condition. Among admissible concretizations optimize domain engineering fitness, then minimum justified concretization complexity, then development economy.

Authority provenance is orthogonal to domain level. Safety, explicit stakeholder/project authority, and governed external contracts may constrain the semantic level where their effect belongs rather than being forced through D1.

## Authority-bearing roles

```text
scientific-formulation
 -> numerical-algorithm-design
 -> software-design
 -> software-implementation
```

These are semantic owners, not a mandatory sequential waterfall. Reduced routes are expected when higher domains are unaffected.

- D1 owner: `roles/scientific-formulation/SKILL.md`
- D2 owner: `roles/numerical-algorithm-design/SKILL.md`
- D3 owner: `roles/software-design/SKILL.md`
- D4 owner: `roles/software-implementation/SKILL.md`

Optional `software-documentation`, `software-maintenance-audit`, and `repository-hygiene` specialists support the lifecycle without creating approval authority.

## Normative document families

- D1 -> Scientific Method Paper
- D2 -> Numerical & Algorithmic Method Paper
- D3 -> Architecture Manual
- D4 -> accepted Specification + code/executable concretization

One logical family may span several physical files. Each material current normative claim has one semantic owner. Proposed/current/challenged/stale/historical/release-pinned state must remain distinguishable.

## Review and Serious Challenge

Every material review/verification boundary includes a bounded Challenge Pass. Review must actively test authority consistency, realizability, logical/mathematical coherence, abstraction adequacy, simultaneous-constraint compatibility, and credible counterexamples. A material potential defect in accepted authority is a Serious Challenge and blocks normal unqualified Pass pending resolution.

Human ratification is risk-triggered for consequential D1/D2 decisions; it is not required for routine delegated implementation. Human authority governs acceptance but does not make unsupported assertions true.

## Historical compatibility

Protocol 6 is the general theory and Protocol 5 is its narrower software-local specialization. Current Protocol 6 doctrine inherits Protocol 5 capabilities without retaining a parallel current vocabulary. The one current historical mapping owner is `shared/references/protocol-versioning-and-compatibility.md`.

Protocol 5.16 workplans retain 5.16 semantics and are not silently reinterpreted. Immutable historical source mapping:

```text
5.16.0 -> e151daaf5c8eebb351a85cfed86170fda80fb5e3
```

The orchestrator ships frozen `sdp-protocol-5.16` schema v1 and `ssdp-protocol-6.0` schema v2 profiles plus current `ssdp-protocol-6.1` schema v2.

## Canonical owners

- recursive authority/challenge -> `shared/references/abstraction-and-realization.md`
- D1 -> `shared/references/scientific-formulation.md`
- D2 -> `shared/references/numerical-algorithm-design.md`
- D3 -> `shared/references/architecture-and-design.md`
- D4 specification/code -> `shared/references/specification-and-implementation.md`
- workflow/handoffs -> `shared/references/workflow-and-workplans.md`
- evidence/evolution/dependencies -> `shared/references/evidence-evolution-and-dependencies.md`
- testing/validation -> `shared/references/testing-and-validation.md`
- scientific/numerical evidence -> `shared/references/scientific-software.md`
- documentation states -> `shared/references/documentation-maintenance.md`
- versioning -> `shared/references/protocol-versioning-and-compatibility.md`
- orchestration prompts -> `shared/references/development-workflow-prompts.md`

## Language and tool routing

Language, tool, security, performance, storage, release, debugging, configuration, convergence, and long-horizon references remain reusable cross-domain doctrine and are routed by material relation.

The common relation-first tool owner is `shared/references/tool-assisted-engineering.md`; specialized routes are `shared/references/tool-serena.md`, `shared/references/tool-semgrep.md`, `shared/references/tool-hypothesis.md`, and `shared/references/tool-codeql.md`. These are progressively disclosed by the D3/D4 executable roles rather than copied into every specialist.

Language engineering remains under `shared/references/language-profiles.md` plus the Python/C++ differential profiles. Shared domain authority outranks language-specific implementation advice.

## Repository acceptance

```bash
python -m pip install -r source/requirements-validation.txt
python -m unittest discover -s tests -v
python source/build_skills.py --output /tmp/protocol-dist
python source/validate_packages.py --dist /tmp/protocol-dist
python source/check_dist.py --expected /tmp/protocol-dist --committed dist
git diff --check
```

When orchestrator code/profile resources change also run its snapshot parity and Core suite. Required evidence that did not execute is blocking, not a pass.

These Python commands are repository-local delegated D4 validation machinery; they are not language-specific protocol doctrine.
