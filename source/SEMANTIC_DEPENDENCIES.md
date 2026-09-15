# SSDP Current Semantic Dependency View

This is a bounded human/agent-readable view of material **accepted Protocol 6.3 plus proposed Protocol 6.4 candidate** relationships. It supports impact analysis; it is not a universal claim/source-code graph, activation registry, Project Engineering Memory (PEM) index, semantic-definition authority, or independent authority. Absence of an edge outside explicitly complete mapped scope is not evidence of independence.

## Semantic authority chain

```text
D2 CONCRETIZES -> D1
D3 CONCRETIZES -> applicable D2
D3 CONSTRAINED_BY -> applicable D1/external constraints entering D3 directly
D4 CONCRETIZES -> applicable D3
D4 CONSTRAINED_BY -> applicable D1/D2/external constraints entering D4 directly
```

Current owners:

- universal relation/Challenge/representation/Protocol-6.4 source-availability semantics: `source/shared/references/abstraction-and-concretization.md`;
- D1: `source/shared/references/scientific-formulation.md` + project Scientific Method Paper family;
- D2: `source/shared/references/numerical-algorithm-design.md` + project Numerical & Algorithmic Method Paper family;
- D3: `source/shared/references/architecture-and-design.md` + project Architecture Manual family;
- D4: `source/shared/references/specification-and-implementation.md` + accepted D4 Specification/executable implementation.

Frozen historical Protocol 6.0/6.1 sources may retain `abstraction-and-realization.md`; current 6.2/6.3 and proposed 6.4 use `abstraction-and-concretization.md` and do not create a current compatibility alias.

## Protocol 6.4 semantic-definition relationships

```text
material semantic object USES_DEFINITION -> direct material prerequisite semantic object
substantive source use REQUIRES -> source_available canonical meaning
runtime inference REQUIRES -> context_available exact canonical meaning
parameterized instance DERIVED_FROM -> parameterized family + material parameter binding/default source
imported specialized object DERIVED_FROM -> exact external source/version/locator + local transformation
claim ASSUMES -> material hypotheses/validity conditions
```

`USES_DEFINITION` is a direct semantic relation only: ordinary hyperlinks, package/import graphs, call graphs, evidence execution dependencies and incidental prose mentions are not definition edges. A generated dependency trace or strongly connected component condensation is a derived review/impact view and never supplies semantic meaning or warrant. Completeness/absence claims apply only to an explicitly declared reviewed scope.

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

`source/shared/references/evidence-evolution-and-dependencies.md` owns evidence lifecycle/applicability/dependency/evolution semantics, including parameter-sensitive evidence applicability and `USES_DEFINITION` trace semantics. `source/shared/references/project-engineering-memory.md` owns PEM representation, family/notice/schema/summary/partition semantics. `workflow-and-workplans.md` owns conditional activation, accepted-base/overlay use, Historical Applicability Set (HAS), and closeout learning. No PEM/definition-trace edge recursively proves an endpoint, and no memory/trace relation creates D1-D4 authority.

The self-hosted repository `PROJECT-ENGINEERING-MEMORY.md` is project-local candidate state and is not copied into generic `dist/` packages or protocol profile snapshots.

## Activation relationships

Activation is intentionally distinct from this semantic view. Root role/specialist `SKILL.md` files select canonical concern owners; a concern owner may conditionally activate a narrower leaf. Ordinary links, this dependency view, semantic-definition traces, PEM relations, a derived memory index, and package membership are **not activation edges**. Any generated activation/definition graph or trace is diagnostic evidence derived from canonical router/owner prose, never another current routing/semantic authority.

Representative concern routers:

```text
role/specialist SKILL.md -> universal kernel + owning concern
material mature rework/recurrence/replacement/recovery decision -> project-engineering-memory.md + workflow HAS rules
material language/runtime/build question -> language-profiles.md -> python-engineering.md / cpp-engineering.md
material specialized engineering relation -> tool-assisted-engineering.md -> applicable tool-* method
```

A memory-triggering route uses progressive disclosure: exact base/overlay -> schema/publication validation -> compact summary -> canonical metadata applicability search -> matched detail/evidence. Temperature/summary visibility ranks attention but never defines applicability.

## Human-facing documentation

`scientific-technical-writing.md` owns technical exposition/background/first-use abbreviation/formal-first presentation rules. `documentation-maintenance.md` owns current-vs-history/document lifecycle. `documentation-and-evidence.md` owns engineering-document/evidence communication. D1-D4 retain precise semantic ownership. Documentation may represent/reconcile PEM or definition traces but cannot admit, promote, reclassify, adjudicate owner conflicts, or turn derivatives into authority editorially.

## Version/profile relationships

```text
ssdp-protocol-6.1 CONSTRAINED_BY -> immutable historical Protocol 6.1 rollback semantics
ssdp-protocol-6.2 CONSTRAINED_BY -> immutable historical Protocol 6.2 rollback semantics
ssdp-protocol-6.3 CONSTRAINED_BY -> accepted-current Protocol 6.3 semantics
ssdp-protocol-6.4 CONSTRAINED_BY -> proposed Protocol 6.4 candidate semantics
ssdp-protocol-6.4 PRESERVES -> frozen Protocol 6.3 profile/schema-v2 stage-graph capability
PEM schema 1 VERSIONED_INDEPENDENTLY_OF -> SSDP protocol/profile schema
```

Frozen 5.16/6.0/6.1/6.2 profiles remain independent compatibility/rollback resources, and 6.3 becomes the immediate frozen predecessor oracle for candidate 6.4 profile generation. Protocol 6.3 remains accepted-current until 6.4 qualification, independent assembled-candidate Review, bootstrap/recovery publication, generated reconciliation, impact closure and lifecycle cutover all pass. Unsupported PEM schemas fail safe for memory-dependent decisions without breaking unrelated protocol routes.

## Source/generated relationships

```text
source/ -> source/build_skills.py -> dist/skills/* + dist/*.zip
source/ + current protocol prompt/profile inputs -> orchestrator current profile/snapshot resources
PROJECT-ENGINEERING-MEMORY.md -X-> generic dist/profile/snapshot
```

Generated descendants are not independent authority. Package transport closure and runtime activation are separate relationships. A partitioned PEM root + canonical cold partitions form one logical publication; any optional active index/summary is derived from canonical memory and cannot become a second owner.

## Maintenance rule

When a mapped current endpoint is renamed/split/merged or materially changes meaning, reconcile this view during the same affected closeout. When a materially depended-on semantic definition, parameter/default/source binding, evidence family/binding, or PEM family changes, perform bounded transitive/reverse impact closure and refresh only affected state rather than treating a stale relation as current. Preserve historical rationale in `history/SEMANTIC_EVOLUTION.md` rather than keeping obsolete current edges. Do not broaden this bounded view merely to make a graph look complete.
