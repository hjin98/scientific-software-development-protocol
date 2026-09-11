# Scientific Software Development Protocol

Current source candidate: **Protocol 6.2**. Accepted rollback/current release remains Protocol 6.1 until Protocol 6.2 qualification, independent Review, recovery mapping, generated-artifact reconciliation, and lifecycle closeout complete.

## Core model

The Scientific Software Development Protocol (SSDP) separates four semantic authority domains:

```text
D1 scientific/mathematical formulation
 -> D2 algorithm/numerical method
 -> D3 software architecture
 -> D4 specification/implementation
```

This is a semantic hierarchy, not a mandatory waterfall. A child concretization must preserve every applicable parent abstraction and directly governed external constraint. Among admissible concretizations prefer domain engineering fitness, then minimum justified total complexity, then development economy.

The universal current kernel is `source/shared/references/abstraction-and-concretization.md`. It owns authority/concretization, Challenge, and Protocol 6.2 Lossless Representation rules. Role entrypoints route progressively to concern owners rather than loading the complete reference library up front.

## Protocol 6.2 representation rule

Protocol 6.2 preserves all accepted Protocol 6.1 doctrine and still-valid historical capability as a prerequisite while improving how that information is communicated. Among lossless representations prefer semantic precision, importance-weighted attention, cognitive digestibility, context/routing efficiency, then compactness. A writer may not shrink governed scope, hide a mandatory lower-salience constraint, or remove globally required doctrine merely because it is cold for one task.

Activation is explicit and typed:

```text
task/orchestration
 -> role or specialist SKILL.md
      -> universal kernel + owning domain
      -> conditional concern owner
           -> conditional concern-local leaf
```

Ordinary Markdown links, semantic dependencies, and package membership do not themselves activate context. Router prose is authoritative; graphs/traces are diagnostic derivatives.

## Roles, specialists, and documentation

Authority-bearing roles:

- `scientific-formulation` (D1)
- `numerical-algorithm-design` (D2)
- `software-design` (D3)
- `software-implementation` (D4)

Optional specialists: `software-documentation`, `software-maintenance-audit`, `repository-hygiene`.

Current human-facing documents define newly introduced non-common terminology for their intended competent reader and expand non-obvious abbreviations on first explanatory use (`full term (ABC)`). Current documents explain present truth; semantic history explains why it changed.

## Version compatibility

Frozen historical mappings remain immutable:

```text
5.16.0 -> e151daaf5c8eebb351a85cfed86170fda80fb5e3
6.0.0  -> 21d5188f5bd9a0270d7a2ebf93d41a6b7842ccd2
6.1.0  -> 802e75af261efb4f70d71284d860613a2197b639
```

Protocol 6.1 public-source bootstrap remains `47e9155632c44493644b0b02fa1fa625703cf480`. The first 6.2 bootstrap attempt, `1181c2031710c5d343194d87d08543290fded0ab`, is invalidated pre-acceptance because it predates a required explicit cold-route repair and must not be used as current 6.2 fallback.

Protocol 6.2 replacement public-source bootstrap is **`5a062ebc472755607b9dc66d33a5ebbc4b7429aa`**. That immutable self-reference-safe source snapshot passed source regression, canonical package build, and independent standalone package/link validation before its SHA was published by a descendant. Current 6.2 public fallback, when no compatible installed source is readable, resolves only to that exact ref. Repository default branch is never a protocol-version oracle.

## Canonical source and acceptance

`source/` is canonical. `dist/skills/`, top-level skill ZIPs, and orchestrator protocol resources are generated/packaged descendants.

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

A release cannot close while a governing Serious Challenge or required assembled acceptance check remains unresolved/unexecuted.