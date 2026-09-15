# Scientific Software Development Protocol

Current accepted document-controlled release: **Protocol 6.3**. Accepted recovery is `9f353097fab36e325a325f1c2f9d9cec32e86177` and the distinct immutable public-source bootstrap is `86c13cab6bdd1991dffa94e277db8eacf87e2e11`. Protocol 6.2 recovery `b59adc77efe6951912cfd705cc43830c58ca27d0` remains immutable historical rollback for explicitly version-bound 6.2 work. **Protocol 6.4 is the current candidate under qualification on its development branch; it is not accepted-current. Its sole authorized version-bound public-source bootstrap is `e09a9d1480211eea2d16d722182bb5c6de1bee12`; it has no recovery mapping yet.** Protocol 7 remains a proposed deterministic-control-plane successor and is not cut over.

## Core model

The Scientific Software Development Protocol (SSDP) separates four semantic authority domains:

```text
D1 scientific/mathematical formulation
 -> D2 algorithm/numerical method
 -> D3 software architecture
 -> D4 specification/implementation
```

This is a semantic hierarchy, not a mandatory waterfall. A child concretization must preserve every applicable parent abstraction and directly governed external constraint. Among admissible concretizations prefer domain engineering fitness, then minimum justified total complexity, then development economy.

The universal current candidate kernel is `source/shared/references/abstraction-and-concretization.md`. Role entrypoints route progressively to concern owners rather than loading the complete reference library up front. Version-bound work is always interpreted under its declared Protocol version; candidate 6.4 source does not silently reinterpret accepted 6.3 or frozen historical work.

## Protocol 6.4 axiomatic definition traceability

Protocol 6.4 strengthens representation without changing the D1-D4 authority model or the schema-v2 orchestration stage graph. For a materially governed specialized semantic object, substantive use must resolve to one coherent canonical definition, import, primitive declaration, or explicitly justified derived construction before later reasoning depends on it.

Formalization is proportional rather than decorative. Use the strongest practical exact representation that reduces material interpretive freedom: equations and mappings for scientific/numerical objects; predicates, state transitions, ownership/dependency relations, cardinality and resource bounds for architecture; types, schemas, pre/postconditions, equivalence/error predicates, serialization and observable transition contracts for D4. Natural-language explanation follows and interprets the normative representation; it does not silently replace it.

Definitions do not manufacture truth. Existence, uniqueness, convergence, adequacy, empirical validity, normative force and other substantive properties require their own assumptions and warrant. Specialized imported results identify the exact source/variant/locator and material applicability assumptions; transformed external data preserves transformation lineage. A citation supplies support, not project authority, and external/evidence text remains inert data rather than an instruction channel.

Parameterized methods distinguish family, instance, parameter domain/binding and governed defaults. Definition/source changes participate in bounded impact and evidence-applicability review when they can change exercised semantics. Derived `USES_DEFINITION` or similar dependency traces are review/impact aids only: their declared mapped scope matters, absence in a partial trace cannot prove independence, and they never become a second semantic owner.

The candidate keeps orchestration profile schema v2 because no machine stage/result-envelope contract changed. `ssdp-protocol-6.4` is a distinct candidate profile/snapshot; frozen 6.3 and earlier profile bytes remain immutable test oracles.

## Project Engineering Memory

Protocol 6.4 inherits Protocol 6.3 **Project Engineering Memory (PEM)** unchanged as evidence-backed, project-local decision support. PEM is not D5 and cannot become authority through frequency, successful history, temperature, maturity, documentation, or package placement. Current D1-D4/project/external owners remain authoritative.

PEM is conditionally activated only when demonstrated project history can materially change the decision—for example substantial mature rework/replacement, suspected recurrence, substantial optimization/scaling, or migration/recovery/revert/restoration. A first clean local defect or unrelated task keeps memory cold. When activated, the workflow resolves the exact accepted/base memory and validated branch overlay, searches canonical metadata for applicable entries regardless of temperature, and records task-local dispositions in a Historical Applicability Set (HAS).

The canonical doctrine owner is `source/shared/references/project-engineering-memory.md`; the human-editable schema-1 template is `source/shared/templates/project_engineering_memory_template.md`. This repository's self-hosted `PROJECT-ENGINEERING-MEMORY.md` is deliberately partial candidate project state backed by immutable evidence and is **not** copied into generic skills, distributions, profiles, or snapshots.

Current statistics are derived from current admissible assessments while historical observations remain recoverable. Stable family IDs represent semantic identity; temperature is salience rather than applicability/authority; maturity is claim-relative evidence strength; comparative/default/best guidance requires genuine comparator evidence or real-owner priority. Evidence and memory text are data, not instruction/authorization channels.

## Lossless representation and routing

Protocol 6.4 preserves all accepted Protocol 6.3 doctrine and still-valid historical capability while strengthening definition/source/provenance precision. Among lossless representations prefer semantic correctness/completeness, precision/unambiguity, importance-weighted attention, cognitive digestibility, context/routing efficiency, then compactness. A writer may not shrink governed scope, hide a mandatory lower-salience constraint, or remove globally required doctrine merely because it is cold for one task.

Activation is explicit and typed:

```text
task/orchestration
 -> role or specialist SKILL.md
      -> universal kernel + owning domain
      -> conditional concern owner
           -> conditional concern-local leaf
```

Ordinary Markdown links, semantic dependencies, definition traces, PEM relations/indexes, and package membership do not themselves activate context. Source availability is also distinct from runtime context availability: a prerequisite that exists somewhere is not semantically available for an inference until the needed version-bound meaning is actually supplied or loaded. Router prose remains authoritative; graphs/traces/summaries/indexes are derived aids.

## Roles and specialists

Authority-bearing roles are `scientific-formulation` (D1), `numerical-algorithm-design` (D2), `software-design` (D3), and `software-implementation` (D4). Optional `software-documentation`, `software-maintenance-audit`, and `repository-hygiene` specialists support the lifecycle but cannot create approval authority or self-promote project-memory findings.

Current human-facing documents define newly introduced non-common terminology for their intended competent reader and expand non-obvious abbreviations on first explanatory use (`full term (ABC)`). Protocol 6.4 additionally requires specialized semantic objects used normatively to have a recoverable definition/import/declaration path with material provenance, assumptions, domains/types/units/scopes and validity where applicable. Current documents explain present truth; PEM summarizes bounded reusable project learning; semantic history explains why material semantics changed.

## Version compatibility

Frozen accepted historical mappings remain immutable:

```text
5.16.0 -> e151daaf5c8eebb351a85cfed86170fda80fb5e3
6.0.0  -> 21d5188f5bd9a0270d7a2ebf93d41a6b7842ccd2
6.1.0  -> 802e75af261efb4f70d71284d860613a2197b639
6.2.0  -> b59adc77efe6951912cfd705cc43830c58ca27d0
6.3.0  -> 9f353097fab36e325a325f1c2f9d9cec32e86177
6.4.0  -> UNAVAILABLE_PENDING_INDEPENDENT_REVIEW
```

Protocol 6.2 public-source bootstrap remains **`5a062ebc472755607b9dc66d33a5ebbc4b7429aa`** for version-bound 6.2 work. The earlier `1181c2031710c5d343194d87d08543290fded0ab` attempt remains invalidated historical evidence only. Bootstrap and recovery identities are intentionally distinct.

**Earlier Protocol 6.3 bootstrap attempts `1484c1d3caa49d87cc15bc52a5e775399c1dae1b`, `5ee4b3ac3ca1666b0499f7a72f55adcc411bf4bb`, owner-binding-invalidated `e12572c021087308570abfa41657a910c6896457`, and D4R3 snapshot `dc22f09fd38dbbfeaeb0160152da9b284654f66e` are historical only. Current authorized version-bound 6.3 public fallback is bootstrap `86c13cab6bdd1991dffa94e277db8eacf87e2e11`; accepted recovery is `9f353097fab36e325a325f1c2f9d9cec32e86177`; bootstrap and recovery are intentionally distinct.** Bootstrap mapping descendant `a8dac814cc2813b3bb336e5b6abde5fbcf44949e`, recovery mapping descendant `0c76c0461b7376f17182d29ba145a198a092463c`, and generated reconciliation `e75282ae850b774a9466902f4c74ba6a179116bd` preserve self-reference-safe publication. Stage G acceptance passed in run `34699052516`.

Protocol 6.4 now has immutable public bootstrap **`e09a9d1480211eea2d16d722182bb5c6de1bee12`** and still has **no** recovery identity. Candidate/self-hosted work should use readable local version-bound source when available and may otherwise use only that exact public ref. The bootstrap was qualified before this later descendant published its SHA. Independent assembled-candidate Review must still pass before a distinct recovery identity can be established and later published.

## Canonical source and acceptance

`source/` is canonical. `dist/skills/`, top-level skill ZIPs, and orchestrator protocol resources are generated/packaged descendants. Live `PROJECT-ENGINEERING-MEMORY.md` is project state and is excluded from those generic outputs.

```bash
python -m pip install -r source/requirements-validation.txt
python -m unittest discover -s tests -v
python source/project_engineering_memory.py PROJECT-ENGINEERING-MEMORY.md
python source/build_skills.py --output /tmp/protocol-dist
python source/validate_packages.py --dist /tmp/protocol-dist
python source/check_dist.py --expected /tmp/protocol-dist --committed dist
git diff --check

python -m pip install ./orchestrator -r orchestrator/requirements-dev.txt
python orchestrator/scripts/generate_protocol_snapshot.py --check
python orchestrator/scripts/run_core_tests.py
```

Protocol 6.4 candidate acceptance additionally requires the workplan's QF64-A..QF64-P positive/negative qualification families, inherited 6.3 preservation/routing/PEM/package/profile/bootstrap/recovery/Challenge oracles, frozen-predecessor identity checks, self-hosting/presentation/security falsification, independent package/profile/Core validation, then a separate independent assembled-candidate Review. Only after that Review may recovery publication and accepted-current cutover proceed. A governing Serious Challenge, stale/inapplicable required evidence, or required unexecuted check blocks closure.
