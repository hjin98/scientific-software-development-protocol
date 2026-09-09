# SSDP Current Semantic Dependency View

This is a bounded human/agent-readable view of material current relationships inside the Scientific Software Development Protocol (SSDP) repository. It supports impact analysis and evidence reconciliation under Protocol 6.1. It is not a universal claim graph, source-code dependency graph, or independent authority.

## Scope and completeness

This view is intentionally complete only for the protocol-wide relationships listed below. Absence of an edge outside this declared scope is not evidence of independence. Repository/code/document inspection remains required for affected-surface reasoning when a scope has not been explicitly mapped here.

## Protocol semantic chain

```text
D2 algorithm/numerical authority
  CONCRETIZES -> D1 scientific/mathematical authority

D3 architecture authority
  CONCRETIZES -> applicable D2 authority
  CONSTRAINED_BY -> applicable D1/external invariants that enter D3 directly

D4 specification/implementation authority
  CONCRETIZES -> applicable D3 authority
  CONSTRAINED_BY -> applicable D1/D2/external invariants that enter D4 directly
```

Current canonical domain owners:

- D1: `source/shared/references/scientific-formulation.md` and project Scientific Method Paper families;
- D2: `source/shared/references/numerical-algorithm-design.md` and project Numerical & Algorithmic Method Paper families;
- D3: `source/shared/references/architecture-and-design.md` and project Architecture Manual families;
- D4: `source/shared/references/specification-and-implementation.md`, accepted D4 specifications, and executable implementation.

The governing recursive relation is defined in `source/shared/references/abstraction-and-realization.md`; the filename is retained as a Protocol 6.0 compatibility identifier while Protocol 6.1 prose uses abstraction/concretization terminology.

## Evidence doctrine relationships

```text
source/shared/references/testing-and-validation.md
  DEPENDS_ON -> source/shared/references/evidence-evolution-and-dependencies.md

source/shared/references/workflow-and-workplans.md
  DEPENDS_ON -> source/shared/references/evidence-evolution-and-dependencies.md

source/shared/references/documentation-and-evidence.md
  DEPENDS_ON -> source/shared/references/evidence-evolution-and-dependencies.md

source/shared/references/documentation-maintenance.md
  DEPENDS_ON -> source/shared/references/evidence-evolution-and-dependencies.md

source/shared/references/protocol-versioning-and-compatibility.md
  DEPENDS_ON -> source/shared/references/evidence-evolution-and-dependencies.md
```

Evidence specifications `EVIDENCES` the governed claims their oracles are designed to discriminate. Evidence realizations `INSTANTIATES` those specifications and `EXECUTION_DEPENDS_ON` the concrete implementation/harness/data/environment needed to execute them. Observations are `GENERATED_BY` evidence realizations.

## Human-facing documentation relationships

```text
source/specialists/software-documentation/SKILL.md
  DEPENDS_ON -> source/shared/references/scientific-technical-writing.md

source/shared/templates/scientific_method_paper_template.md
  DEPENDS_ON -> source/shared/references/scientific-technical-writing.md

source/shared/templates/numerical_algorithmic_method_paper_template.md
  DEPENDS_ON -> source/shared/references/scientific-technical-writing.md
```

The scientific-technical-writing reference owns the Protocol 6.1 human-facing background/terminology and first-use abbreviation standard. D1-D4 owners retain authority over precise normative definitions.

## Version/profile relationships

```text
ssdp-protocol-6.1
  SUPERSEDES -> ssdp-protocol-6.0 as the default/current profile after 6.1 acceptance

ssdp-protocol-6.1
  CONSTRAINED_BY -> Protocol 6.1 canonical source

ssdp-protocol-6.0
  CONSTRAINED_BY -> immutable Protocol 6.0 recovery semantics
```

`ssdp-protocol-6.0` remains a frozen compatibility profile for workplans declared under Protocol 6.0. `ssdp-protocol-6.1` is a separate profile identity; Protocol 6.0 bytes are not edited into Protocol 6.1.

## Build/source-chain relationships

```text
source/
  -> source/build_skills.py
  -> dist/skills/* and dist/*.zip

source/ + current protocol profile resources
  -> orchestrator packaged protocol snapshot/resources
```

Generated distribution/profile descendants are not independently authoritative and must be regenerated from their canonical current source rather than patched as competing truth.

## Maintenance rule

When one of the mapped current endpoints is renamed, split, merged, superseded, or materially changes meaning, reconcile the affected current relationships during the same closeout. Preserve material reasons for supersession in `history/SEMANTIC_EVOLUTION.md`; do not retain obsolete edges here merely to preserve history.
