# Scientific Software Development Protocol Source

`source/` is the canonical version-intrinsic SSDP source. Its declared version is `source/PROTOCOL_VERSION`. Mutable repository release state—accepted-current version, public fallback, recovery and active candidate Review/ratification—is owned outside this immutable semantic payload by root `../PROTOCOL-RELEASE-STATE.yaml`. Generated distributions and orchestrator snapshots are derivatives; frozen historical/version-bound resources remain immutable.

## Governing model

SSDP separates D1 scientific/mathematical formulation, D2 algorithm/numerical method, D3 software architecture, and D4 specification/implementation. Read `shared/references/abstraction-and-concretization.md`, the small universal kernel, for authority, materiality, Challenge, proportional rigor, self-application, Lossless Representation, and the hard specialized-semantics availability invariant; everything else loads from conditional owners.

A concretization is admissible only when it satisfies every applicable parent abstraction and directly governed constraint. Within the admissible set optimize domain engineering fitness, minimum justified total complexity, then development economy. Development economy is operational: allocate analysis/evidence by consequence and decision-sensitive uncertainty, use the cheapest sufficiently strong applicable route, and stop when further certainty cannot change the governed decision. Mandatory obligations remain closure conditions. D1->D4 is semantic ordering, not a mandatory waterfall.

Project Engineering Memory (PEM) remains evidence-backed project-local decision support, not D5. Its agent-facing owner is `shared/references/project-engineering-memory.md` and its cold schema/governance owner is `shared/references/project-engineering-memory-schema.md`; this repository's live `../PROJECT-ENGINEERING-MEMORY.md` is project state and is never generic package/profile content.

## Formal-definition boundary

Detail is owned by `shared/references/semantic-definition-and-traceability.md` and loads only when specialized semantics are material. A materially governed specialized semantic object has a recoverable canonical definition/import/primitive/derived path before substantive reuse. Use the strongest practical exact representation that reduces material interpretive freedom without decorative mathematics or freezing delegated lower-level mechanisms.

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

- universal authority / Challenge / rigor / representation -> `shared/references/abstraction-and-concretization.md`
- specialized definitions / imports / parameter bindings / `USES_DEFINITION` -> `shared/references/semantic-definition-and-traceability.md`
- D1/D2/D3/D4 -> their matching domain references
- authority lifecycle / workplans / handoffs / Working State / Review / closeout -> `shared/references/workflow-and-workplans.md`
- recurrence / rigor / cognitive-resource escalation -> `shared/references/convergence-and-cycle-economy.md`
- evidence/dependency/applicability -> `shared/references/evidence-evolution-and-dependencies.md`
- testing/qualification -> `shared/references/testing-and-validation.md`
- relation-first optional engineering tools -> `shared/references/tool-assisted-engineering.md`
- language/runtime routing -> `shared/references/language-profiles.md`
- PEM use/HAS/closeout learning -> `shared/references/project-engineering-memory.md`; PEM schema/publication -> `shared/references/project-engineering-memory-schema.md`
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

`source/version_preflight.py` is an optional offline entry check (`--skill-root <bundle> --workplan <plan.md> --release-state PROTOCOL-RELEASE-STATE.yaml`); it applies the versioning owner's rule and is not a version authority. `qualification/ssdp66/eval/` holds the removable Protocol 6.6 evaluation harness.

Mechanical acceptance establishes only structural/executable properties its oracles discriminate. Semantic adequacy requires independent assembled-candidate Review, including an out-of-matrix abstraction-adequacy pass. Claims that a protocol successor improves engineering outcomes require separate outcome evidence. Current release identities resolve from `../PROTOCOL-RELEASE-STATE.yaml`.
