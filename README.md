# Scientific Software Development Protocol

The Scientific Software Development Protocol (SSDP) is a recursive D1-D4 authority/concretization system for scientific software engineering.

**Current mutable release state is owned only by [`PROTOCOL-RELEASE-STATE.yaml`](PROTOCOL-RELEASE-STATE.yaml).** Do not infer accepted-current, public fallback, recovery, candidate Review, or ratification state from this README, branch position, repository default/latest, or immutable versioned source.

## Core model

```text
D1 scientific/mathematical formulation
 -> D2 algorithm/numerical method
 -> D3 software architecture
 -> D4 specification/implementation
```

This is semantic ordering, not a mandatory waterfall. A child concretization preserves every applicable parent abstraction and directly governed external constraint. Among admissible concretizations prefer domain engineering fitness, minimum justified total complexity, then development economy.

The universal kernel is `source/shared/references/abstraction-and-concretization.md`. It owns materiality, authority, Challenge, self-application, semantic-definition/source-availability, abstraction adequacy and Lossless Representation.

## Formal definition and traceability

Materially governed specialized semantic objects resolve to coherent canonical definitions, imports, primitives or justified derivations before substantive dependent reasoning. Formalization is proportional: equations/mappings for scientific/numerical objects, exact ownership/state/dependency relations for architecture, and types/schemas/pre-postconditions/equivalence/error/persistence/security contracts for D4 where they materially distinguish outcomes.

Definition does not manufacture truth. Existence, uniqueness, convergence, adequacy, empirical validity and normative force require their own assumptions/warrant. Parameterized methods distinguish family, instance, parameter binding and governed defaults. `USES_DEFINITION` traces are bounded review/impact aids, never a second semantic owner.

## Project Engineering Memory

Project Engineering Memory (PEM) is evidence-backed, project-local decision support. It is not D5 and cannot acquire authority through frequency, temperature, maturity, tests, documentation or historical survival. The canonical schema/doctrine is `source/shared/references/project-engineering-memory.md`; the repository's live `PROJECT-ENGINEERING-MEMORY.md` is project state and is excluded from generic distributions/profiles.

## Lossless representation and routing

Roles and specialists route progressively to canonical owners. Ordinary Markdown links, semantic dependencies, generated traces, PEM relations/indexes and package membership do not activate context. **Package membership is not activation.** Source availability is distinct from runtime context availability.

Authority roles: `scientific-formulation`, `numerical-algorithm-design`, `software-design`, `software-implementation`. Optional non-authoritative specialists: `software-documentation`, `software-maintenance-audit`, `repository-hygiene`.

## Version compatibility and release state

Version-intrinsic source/profile/package semantics are distinct from mutable repository release state. Exact historical/public/recovery mappings are in `PROTOCOL-RELEASE-STATE.yaml`; detailed rationale/chronology belongs in `history/SEMANTIC_EVOLUTION.md`.

Version-bound work is interpreted under its declared `protocol_version`. Frozen historical resources are not rewritten under current terminology. Public-source fallback and recovery are distinct identities.

For an SSDP protocol release:

```text
candidate -> implementation acceptance -> freeze
-> independent assembled-candidate Review
-> explicit stakeholder ratification
-> public fallback publication
-> exact-ref verification
-> distinct recovery
-> accepted-current cutover
```

Review PASS is technical eligibility; it is not stakeholder ratification.

## Canonical source and acceptance

`source/` is canonical version-intrinsic source. `dist/` and orchestrator protocol resources are generated descendants.

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

Mechanical qualification must state the exact subject/property it discriminates. Semantic protocol adequacy is separately tested by fresh independent Review of the assembled candidate, including an out-of-matrix attempt to find locally compliant/global-failure trajectories.
