# SSDP Current Semantic Dependency View

This is a bounded human/agent-readable view of material **current Protocol 6.3 candidate** relationships. It supports impact analysis; it is not a universal claim/source-code graph, activation registry, Project Engineering Memory (PEM) index, or independent authority. Absence of an edge outside explicitly complete mapped scope is not evidence of independence.

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

Frozen historical Protocol 6.0/6.1 sources may retain `abstraction-and-realization.md`; current 6.2/6.3 uses `abstraction-and-concretization.md` and does not create a current compatibility alias.

## Evidence and project-learning relationships

```text
evidence specification EVIDENCES -> governed claim
evidence realization INSTANTIATES -> evidence specification
evidence specification/realization EXECUTION_DEPENDS_ON -> implementation/harness/data/environment
observation GENERATED_BY -> evidence realization
PEM family/notice SUPPORTS_LEARNING_FROM -> durable evidence route(s)
PEM capability AUTHORITY_BOUND -> exact current owner/claim when independently required
active workplan HAS DERIVED_FROM -> exact accepted PEM base + validated candidate overlay
```

`source/shared/references/evidence-evolution-and-dependencies.md` owns evidence lifecycle/applicability/dependency/evolution semantics. `source/shared/references/project-engineering-memory.md` owns PEM representation, family/notice/schema/summary/partition semantics. `workflow-and-workplans.md` owns conditional activation, accepted-base/overlay use, Historical Applicability Set (HAS), and closeout learning. No PEM edge recursively proves an endpoint, and no memory relation creates D1-D4 authority.

The self-hosted repository `PROJECT-ENGINEERING-MEMORY.md` is project-local candidate state and is not copied into generic `dist/` packages or protocol profile snapshots.

## Activation relationships

Activation is intentionally distinct from this semantic view. Root role/specialist `SKILL.md` files select canonical concern owners; a concern owner may conditionally activate a narrower leaf. Ordinary links, this dependency view, PEM relations, a derived memory index, and package membership are **not activation edges**. Any generated activation graph/trace is diagnostic evidence derived from canonical router prose, never another current routing authority.

Representative concern routers:

```text
role/specialist SKILL.md -> universal kernel + owning concern
material mature rework/recurrence/replacement/recovery decision -> project-engineering-memory.md + workflow HAS rules
material language/runtime/build question -> language-profiles.md -> python-engineering.md / cpp-engineering.md
material specialized engineering relation -> tool-assisted-engineering.md -> applicable tool-* method
```

A memory-triggering route uses progressive disclosure: exact base/overlay -> schema/publication validation -> compact summary -> canonical metadata applicability search -> matched detail/evidence. Temperature/summary visibility ranks attention but never defines applicability.

## Human-facing documentation

`scientific-technical-writing.md` owns technical exposition/background/first-use abbreviation rules. `documentation-maintenance.md` owns current-vs-history/document lifecycle. `documentation-and-evidence.md` owns engineering-document/evidence communication. D1-D4 retain precise semantic ownership. Documentation may represent/reconcile PEM but cannot admit, promote, reclassify, or turn it into authority editorially.

## Version/profile relationships

```text
ssdp-protocol-6.1 CONSTRAINED_BY -> immutable historical Protocol 6.1 rollback semantics
ssdp-protocol-6.2 CONSTRAINED_BY -> accepted-current Protocol 6.2 semantics
ssdp-protocol-6.3 CONSTRAINED_BY -> Protocol 6.3 candidate semantics until qualification/Review/recovery cutover
PEM schema 1 VERSIONED_INDEPENDENTLY_OF -> SSDP protocol/profile schema
```

Frozen 5.16/6.0/6.1/6.2 profiles remain independent compatibility/rollback resources during 6.3 implementation. Protocol 6.2 remains accepted-current until Protocol 6.3 completes qualification, immutable bootstrap/profile generation, independent Review, recovery mapping, generated-artifact/Core parity, and lifecycle closeout. Unsupported PEM schemas fail safe for memory-dependent decisions without breaking unrelated protocol routes.

## Source/generated relationships

```text
source/ -> source/build_skills.py -> dist/skills/* + dist/*.zip
source/ + current protocol prompt/profile inputs -> orchestrator current profile/snapshot resources
PROJECT-ENGINEERING-MEMORY.md -X-> generic dist/profile/snapshot
```

Generated descendants are not independent authority. Package transport closure and runtime activation are separate relationships. A partitioned PEM root + canonical cold partitions form one logical publication; any optional active index/summary is derived from canonical memory and cannot become a second owner.

## Maintenance rule

When a mapped current endpoint is renamed/split/merged or materially changes meaning, reconcile this view during the same affected closeout. When a materially depended-on PEM family/binding changes, perform bounded transitive/reverse impact closure and refresh affected HAS state rather than treating a stale relation as current. Preserve historical rationale in `history/SEMANTIC_EVOLUTION.md` rather than keeping obsolete current edges. Do not broaden this bounded view merely to make a graph look complete.
