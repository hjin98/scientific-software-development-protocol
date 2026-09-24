# Scientific Software Development Protocol Source

`source/` is the canonical version-intrinsic SSDP source. Its declared version is `source/PROTOCOL_VERSION`. Mutable repository release state—accepted-current version, public fallback, recovery and active candidate Review/ratification—is owned outside this immutable semantic payload by root `../PROTOCOL-RELEASE-STATE.yaml`. Generated distributions and orchestrator snapshots are derivatives; frozen historical/version-bound resources remain immutable.

## Governing model

SSDP separates D1 scientific/mathematical formulation, D2 algorithm/numerical method, D3 software architecture, and D4 specification/implementation. Read `shared/references/abstraction-and-concretization.md` for universal authority, materiality, Challenge, self-application, Lossless Representation, semantic-definition/source-availability and abstraction-adequacy rules.

A concretization is admissible only when it satisfies every applicable parent abstraction and directly governed constraint. Within the admissible set optimize domain engineering fitness, minimum justified total complexity, then development economy. D1->D4 is semantic ordering, not a mandatory waterfall.

Project Engineering Memory (PEM) remains evidence-backed project-local decision support, not D5. Its canonical owner is `shared/references/project-engineering-memory.md`; this repository's live `../PROJECT-ENGINEERING-MEMORY.md` is project state and is never generic package/profile content.

## Formal-definition boundary

A materially governed specialized semantic object has a recoverable canonical definition/import/primitive/derived path before substantive reuse. Use the strongest practical exact representation that reduces material interpretive freedom without decorative mathematics or freezing delegated lower-level mechanisms.

Define material domains/types/shapes/units, binders/scope, relation direction, validity assumptions, stochastic semantics, parameter family/instance/default binding, and external source variant/locator/transformation lineage where applicable. Definition alone does not establish existence, uniqueness, convergence, adequacy, empirical truth or normative force.

Typed semantic-use traces such as `USES_DEFINITION` are bounded derived evidence for impact/review, not authority or recursive warrant.

## Authority-bearing roles

- D1: `roles/scientific-formulation/SKILL.md`
- D2: `roles/numerical-algorithm-design/SKILL.md`
- D3: `roles/software-design/SKILL.md`
- D4: `roles/software-implementation/SKILL.md`

Optional specialists `software-documentation`, `software-maintenance-audit`, and `repository-hygiene` support the lifecycle but cannot create approval authority.

## Progressive-disclosure owner map

Load the role entrypoint plus universal kernel/owning domain, then only concern owners whose decision predicates fire. Ordinary links, dependency traces, PEM relations/indexes, and package membership do not imply activation.

Key owners:

- universal authority / Challenge / representation / definition closure -> `shared/references/abstraction-and-concretization.md`
- D1/D2/D3/D4 -> their matching domain references
- workflow/HAS/Review/closeout -> `shared/references/workflow-and-workplans.md`
- evidence/dependency/applicability -> `shared/references/evidence-evolution-and-dependencies.md`
- testing/qualification -> `shared/references/testing-and-validation.md`
- PEM schema/representation -> `shared/references/project-engineering-memory.md`
- version/fallback/recovery/acceptance semantics -> `shared/references/protocol-versioning-and-compatibility.md`
- Git accepted-base/overlay/publication -> `shared/references/git-and-version-control.md`
- technical writing/document lifecycle -> their documentation owners
- language/tool/security/performance/storage/configuration/concurrency/release concerns -> their direct owners when material.

## Build and acceptance

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

Mechanical acceptance establishes only structural/executable properties its oracles discriminate. Semantic adequacy requires independent assembled-candidate Review, including an out-of-matrix abstraction-adequacy pass. Claims that a protocol successor improves engineering outcomes require separate outcome evidence. Current release identities resolve from `../PROTOCOL-RELEASE-STATE.yaml`.
