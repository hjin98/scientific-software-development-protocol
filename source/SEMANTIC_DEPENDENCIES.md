# SSDP Current Semantic Dependency View

This is a bounded human/agent-readable view of material **current Protocol 6.2** relationships. It supports impact analysis; it is not a universal claim/source-code graph, activation registry, or independent authority. Absence of an edge outside explicitly complete mapped scope is not evidence of independence.

## Semantic authority chain

```text
D2 CONCRETIZES -> D1
D3 CONCRETIZES -> applicable D2
D3 CONSTRAINED_BY -> applicable D1/external constraints entering D3 directly
D4 CONCRETIZES -> applicable D3
D4 CONSTRAINED_BY -> applicable D1/D2/external constraints entering D4 directly
```

Current owners:

- universal relation/Challenge/representation: `source/shared/references/abstraction-and-concretization.md`;
- D1: `source/shared/references/scientific-formulation.md` + project Scientific Method Paper family;
- D2: `source/shared/references/numerical-algorithm-design.md` + project Numerical & Algorithmic Method Paper family;
- D3: `source/shared/references/architecture-and-design.md` + project Architecture Manual family;
- D4: `source/shared/references/specification-and-implementation.md` + accepted D4 Specification/executable implementation.

Frozen historical Protocol 6.0/6.1 sources may retain `abstraction-and-realization.md`; current 6.2 does not use that path as a compatibility alias.

## Evidence relationships

```text
evidence specification EVIDENCES -> governed claim
evidence realization INSTANTIATES -> evidence specification
evidence specification/realization EXECUTION_DEPENDS_ON -> implementation/harness/data/environment
observation GENERATED_BY -> evidence realization
```

`source/shared/references/evidence-evolution-and-dependencies.md` owns evidence lifecycle/applicability/dependency/evolution semantics. `testing-and-validation.md`, workflow and documentation owners consume those semantics rather than redefining them.

## Activation relationships

Activation is intentionally distinct from this semantic view. Root role/specialist `SKILL.md` files select canonical concern owners; a concern owner may conditionally activate a narrower leaf. Ordinary links, this dependency view and package membership are **not activation edges**. Any generated activation graph/trace is diagnostic evidence derived from canonical router prose, never another current routing authority.

Representative concern routers:

```text
role/specialist SKILL.md -> universal kernel + owning concern
material language/runtime/build question -> language-profiles.md -> python-engineering.md / cpp-engineering.md
material specialized engineering relation -> tool-assisted-engineering.md -> applicable tool-* method
```

## Human-facing documentation

`scientific-technical-writing.md` owns technical exposition/background/first-use abbreviation rules. `documentation-maintenance.md` owns current-vs-history/document lifecycle. `documentation-and-evidence.md` owns engineering-document/evidence communication. D1-D4 retain precise semantic ownership.

## Version/profile relationships

```text
ssdp-protocol-6.1 CONSTRAINED_BY -> immutable historical Protocol 6.1 rollback semantics
ssdp-protocol-6.2 CONSTRAINED_BY -> accepted-current Protocol 6.2 semantics
```

Frozen 5.16/6.0/6.1 profiles remain independent compatibility resources. Protocol 6.2 is accepted-current after qualification, independent Review, recovery mapping, generated-artifact reconciliation, Protocol 7 handoff reconciliation, and lifecycle closeout.

## Source/generated relationships

```text
source/ -> source/build_skills.py -> dist/skills/* + dist/*.zip
source/ + current protocol prompt/profile inputs -> orchestrator current profile/snapshot resources
```

Generated descendants are not independent authority. Package transport closure and runtime activation are separate relationships.

## Maintenance rule

When a mapped current endpoint is renamed/split/merged or materially changes meaning, reconcile this view during the same affected closeout. Preserve historical rationale in `history/SEMANTIC_EVOLUTION.md` rather than keeping obsolete current edges. Do not broaden this bounded view merely to make a graph look complete.
