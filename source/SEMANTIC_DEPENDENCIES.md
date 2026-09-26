# SSDP Current Semantic Dependency View

This is a bounded human/agent-readable view of material relationships for the **declared current source version plus frozen historical protocol resources**. It supports impact analysis; it is not a universal claim/source-code graph, activation registry, Project Engineering Memory (PEM) index, semantic-definition authority, or independent authority. Absence of an edge outside explicitly complete mapped scope is not evidence of independence.

## Semantic authority chain

```text
D2 CONCRETIZES -> D1
D3 CONCRETIZES -> applicable D2
D3 CONSTRAINED_BY -> applicable D1/external constraints entering D3 directly
D4 CONCRETIZES -> applicable D3
D4 CONSTRAINED_BY -> applicable D1/D2/external constraints entering D4 directly
```

Current owners:

- universal relation/Challenge/representation semantics and the hard source/context-availability invariant: `source/shared/references/abstraction-and-concretization.md`;
- specialized semantic-definition/source-availability/parameter/import/warrant/trace detail: `source/shared/references/semantic-definition-and-traceability.md`;
- D1: `source/shared/references/scientific-formulation.md` + project Scientific Method Paper family;
- D2: `source/shared/references/numerical-algorithm-design.md` + project Numerical & Algorithmic Method Paper family;
- D3: `source/shared/references/architecture-and-design.md` + project Architecture Manual family;
- D4: `source/shared/references/specification-and-implementation.md` + accepted D4 Specification/executable implementation.

Frozen historical Protocol 6.0/6.1 sources may retain `abstraction-and-realization.md`; Protocol 6.2 and later use `abstraction-and-concretization.md` and do not create a current compatibility alias.

## Semantic-definition relationships

```text
material semantic object USES_DEFINITION -> direct material prerequisite semantic object
substantive source use REQUIRES -> source_available canonical meaning
runtime inference REQUIRES -> context_available exact canonical meaning
parameterized instance DERIVED_FROM -> parameterized family + material parameter binding/default source
imported specialized object DERIVED_FROM -> exact external source/version/locator + local transformation
claim ASSUMES -> material hypotheses/validity conditions
```

`USES_DEFINITION` is a direct semantic relation only and is stored as `subject -> prerequisite`: ordinary hyperlinks, package/import graphs, call graphs, evidence execution dependencies and incidental prose mentions are not definition edges. When a prerequisite changes, reverse traversal over stored `USES_DEFINITION` edges finds dependent subjects for impact review; that inverse query does not change the semantic relation direction. A generated dependency trace or strongly connected component condensation is a derived review/impact view and never supplies semantic meaning or warrant. Completeness/absence claims apply only to an explicitly declared reviewed scope.

Source-level availability and runtime context availability are distinct. A route to an exact owner may establish source availability while a runtime inference still requires that exact owner meaning to be loaded/supplied in the active context. Conflicting simultaneously applicable owners keep the object review-required until explicitly reconciled; file order, newest-version preference or route priority does not decide meaning.

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

`source/shared/references/evidence-evolution-and-dependencies.md` owns evidence lifecycle/applicability/dependency/evolution semantics, including parameter-sensitive evidence applicability and `USES_DEFINITION` trace semantics. `source/shared/references/project-engineering-memory.md` owns agent-facing PEM use: conditional activation, accepted-base/overlay use, Historical Applicability Set (HAS), applicability, authority binding and closeout learning. `source/shared/references/project-engineering-memory-schema.md` owns family/notice/schema/summary/partition/publication representation. `workflow-and-workplans.md` owns authority lifecycle/mutation, handoffs and Working State and routes memory questions to the PEM owner. No PEM/definition-trace edge recursively proves an endpoint, and no memory/trace relation creates D1-D4 authority.

The self-hosted repository `PROJECT-ENGINEERING-MEMORY.md` is project-local candidate state and is not copied into generic `dist/` packages or protocol profile snapshots.

## Activation relationships

Activation is intentionally distinct from this semantic view. Root role/specialist `SKILL.md` files select canonical concern owners; a concern owner may conditionally activate a narrower leaf. Ordinary links, this dependency view, semantic-definition traces, PEM relations, a derived memory index, and package membership are **not activation edges**. Any generated activation/definition graph or trace is diagnostic evidence derived from canonical router/owner prose, never another current routing/semantic authority.

Representative concern routers:

```text
role/specialist SKILL.md (with build-inlined entry contract) -> owning concern; universal kernel when its predicate fires
material specialized object/binding/import/formal claim -> semantic-definition-and-traceability.md
material mature rework/recurrence/replacement/recovery decision -> project-engineering-memory.md
memory authoring/validation/publication/partition question -> project-engineering-memory.md -> project-engineering-memory-schema.md
material language/runtime/build question -> language-profiles.md -> python-engineering.md / cpp-engineering.md
material specialized engineering relation -> tool-assisted-engineering.md -> applicable tool-* method
```

A memory-triggering route uses progressive disclosure: exact base/overlay -> schema/publication validation -> compact summary -> canonical metadata applicability search -> matched detail/evidence. Temperature/summary visibility ranks attention but never defines applicability.

## Human-facing documentation

`scientific-technical-writing.md` owns technical exposition/background/first-use abbreviation/formal-first presentation rules. `documentation-maintenance.md` owns current-vs-history/document lifecycle. `documentation-and-evidence.md` owns engineering-document/evidence communication. D1-D4 retain precise semantic ownership. Documentation may represent/reconcile PEM or definition traces but cannot admit, promote, reclassify, adjudicate owner conflicts, or turn derivatives into authority editorially.

## Version/profile relationships

```text
version-intrinsic source/profile semantics DISTINCT_FROM -> mutable repository release state
ssdp-protocol-6.6 PRESERVES -> frozen Protocol 6.5 profile/schema-v2 stage-graph and lifecycle/control capability
ssdp-protocol-6.5 PRESERVES -> frozen Protocol 6.4 profile/schema-v2 stage-graph capability
PEM schema 1 VERSIONED_INDEPENDENTLY_OF -> SSDP protocol/profile schema
```

All previously published 5.16/6.0/6.1/6.2/6.3/6.4/6.5 profile resources remain frozen historical/version-bound or predecessor resources. Current accepted/public/recovery/candidate mappings are not owned by this view; repository `PROTOCOL-RELEASE-STATE.yaml` owns those mutable facts. Unsupported PEM schemas fail safe for memory-dependent decisions without breaking unrelated protocol routes.

## Source/generated relationships

```text
source/ -> source/build_skills.py -> dist/skills/* + dist/*.zip
source/ + current protocol prompt/profile inputs -> orchestrator current profile/snapshot resources
PROJECT-ENGINEERING-MEMORY.md -X-> generic dist/profile/snapshot
PROTOCOL-RELEASE-STATE.yaml -X-> versioned generic dist/profile/snapshot
```

Generated descendants are not independent authority. Package transport closure and runtime activation are separate relationships. A partitioned PEM root + canonical cold partitions form one logical publication; any optional active index/summary is derived from canonical memory and cannot become a second owner.

## Maintenance rule

When a mapped current endpoint is renamed/split/merged or materially changes meaning, reconcile this view during the same affected closeout. When a materially depended-on semantic definition, parameter/default/source binding, evidence family/binding, or PEM family changes, perform bounded transitive/reverse impact closure and refresh only affected state rather than treating a stale relation as current. Preserve historical rationale in `history/SEMANTIC_EVOLUTION.md` rather than keeping obsolete current edges. Do not broaden this bounded view merely to make a graph look complete.
