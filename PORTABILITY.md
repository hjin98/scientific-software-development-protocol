# Agent Portability and Routing Qualification

## Installation contract

The supported portable runtime unit is the self-contained directory `dist/skills/<skill-name>/`; each top-level ZIP contains the same files under one enclosing skill directory. Install a skill as a direct child of the harness-supported skill root so `<skills-root>/<skill-name>/SKILL.md` exists. `source/` is canonical development source; ZIPs are transport artifacts. A shared/symlinked install is a separate harness capability and must be qualified on that harness.

Authority roles: `scientific-formulation`, `numerical-algorithm-design`, `software-design`, `software-implementation`. Optional non-authoritative specialists: `software-documentation`, `software-maintenance-audit`, `repository-hygiene`.

## Protocol 6.3 candidate routing contract

The active role/specialist `SKILL.md` owns **root activation**. It routes to the universal kernel/owning concern; a canonical concern owner may conditionally dispatch to a narrower leaf only within that concern. Each activation edge states a decision predicate and resolvable resource, remains acyclic, adds/narrows material semantics, and reuses already-loaded applicable owners rather than reloading them.

The canonical universal-kernel source is `source/shared/references/abstraction-and-concretization.md`; inside a packaged skill it is reached as `references/abstraction-and-concretization.md`.

```text
activation -> required source/package reachability
reachability / ordinary Markdown link / semantic dependency / package membership != activation
```

`project-engineering-memory.md` is the Protocol 6.3 Project Engineering Memory (PEM) concern owner. It activates only when workflow/role predicates establish that demonstrated project history can materially change the decision. A project-local `PROJECT-ENGINEERING-MEMORY.md` is runtime/project state, not a portable skill dependency: generic bundles include the doctrine/template needed to interpret PEM but never copy a live project's memory, derived local summary, private evidence, or candidate overlay into the package.

`language-profiles.md` is the language concern router and conditionally activates Python/C++ leaves. `tool-assisted-engineering.md` is the relation-first engineering-tool router and conditionally activates analyzer/runtime/tool methods. Do not flatten all leaves or PEM history into every role entrypoint, and do not infer activation from transitive files bundled for standalone transport.

Static package/routing validation can establish declared route/resource integrity, schema/package exclusion, and deterministic generated parity. It **cannot prove** that a named harness/model followed the route, kept non-triggered material cold, gained performance, or benefited from memory. Live claims require fresh-session evidence for the named harness/model/install mode; unavailable telemetry remains unavailable rather than inferred. Do not infer another environment from one run.

## Compatible source resolution

Resolve declared-version-compatible skills local first, canonical public source second. Never reinterpret an older workplan under the newest installed skill merely because it is available.

Accepted immutable mappings:

```text
5.16.0 recovery -> e151daaf5c8eebb351a85cfed86170fda80fb5e3
6.0.0 recovery  -> 21d5188f5bd9a0270d7a2ebf93d41a6b7842ccd2
6.1.0 public bootstrap -> 47e9155632c44493644b0b02fa1fa625703cf480
6.1.0 recovery -> 802e75af261efb4f70d71284d860613a2197b639
6.2.0 public bootstrap -> 5a062ebc472755607b9dc66d33a5ebbc4b7429aa
6.2.0 recovery -> b59adc77efe6951912cfd705cc43830c58ca27d0
6.3.0 invalidated bootstrap attempt -> 1484c1d3caa49d87cc15bc52a5e775399c1dae1b
6.3.0 invalidated second bootstrap -> 5ee4b3ac3ca1666b0499f7a72f55adcc411bf4bb
6.3.0 invalidated owner-binding bootstrap -> e12572c021087308570abfa41657a910c6896457
6.3.0 invalidated D4R3 bootstrap -> dc22f09fd38dbbfeaeb0160152da9b284654f66e
6.3.0 public bootstrap -> UNAVAILABLE_PENDING_REPLACEMENT_BOOTSTRAP
6.3.0 recovery -> UNAVAILABLE_PENDING_6.3_ACCEPTANCE
```

Canonical repository: `https://github.com/hjin98/scientific-software-development-protocol`.

The first Protocol 6.2 bootstrap attempt `1181c2031710c5d343194d87d08543290fded0ab` remains invalidated historical evidence. Version-bound 6.2 public fallback uses exactly `5a062ebc472755607b9dc66d33a5ebbc4b7429aa`; accepted 6.2 recovery is separately `b59adc77efe6951912cfd705cc43830c58ca27d0`.

For Protocol 6.3, pre-repair bootstrap `1484c1d3caa49d87cc15bc52a5e775399c1dae1b`, second bootstrap `5ee4b3ac3ca1666b0499f7a72f55adcc411bf4bb`, owner-binding bootstrap `e12572c021087308570abfa41657a910c6896457`, and D4R3 bootstrap `dc22f09fd38dbbfeaeb0160152da9b284654f66e` are historical evidence only. D9 changed canonical validator semantics. No current 6.3 public fallback is authorized while a new self-reference-safe source snapshot is qualified; recovery remains unavailable. If neither compatible local source nor mapped compatible immutable public source can be read, report truthful non-closure.

## Version-bound profiles

| Profile | Protocol | Schema | State |
| --- | --- | ---: | --- |
| `sdp-protocol-5.16` | 5.16.0 | 1 | frozen |
| `ssdp-protocol-6.0` | 6.0.0 | 2 | frozen |
| `ssdp-protocol-6.1` | 6.1.0 | 2 | frozen historical rollback |
| `ssdp-protocol-6.2` | 6.2.0 | 2 | accepted current |
| `ssdp-protocol-6.3` | 6.3.0 | 2 | candidate after distinct generation/qualification |

During Protocol 6.3 candidate qualification, the 6.2 resource is an immutable predecessor snapshot while Protocol 6.2 remains accepted-current operational authority until cutover. Historical profile/prompt bytes remain immutable. Workplan `protocol_version` selects compatible semantics before stage interpretation. Serious Challenge/human-pending state stops ordinary automatic closure; orchestration represents/routes state but never decides scientific truth. PEM schema versioning is independent of orchestration profile schema; Protocol 6.3 supports PEM schema 1 and fails safe for unsupported memory-dependent decisions.

## Project-memory portability boundary

A harness may discover project PEM from the project/repository context when Protocol 6.3 activation fires, but must resolve its accepted/base identity according to project integration policy rather than treating the newest/default-branch file as accepted. A same-branch candidate overlay remains candidate. Temperature and active-summary visibility are salience aids, not applicability filters; bounded canonical metadata search must still surface materially relevant lower-salience entries.

Missing/partial PEM, stale index, or unsupported schema cannot be interpreted as historical absence. Unsupported memory blocks only memory-dependent decisions; unrelated protocol work continues under its governing owners. Cross-project/fork memory keeps source-project provenance and cannot manufacture local incidence.

## Packaging and external capabilities

Standalone bundles contain every local resource a supported activation path can require and every local Markdown resource needed to keep the bundled document graph non-dangling. Current transport may therefore use bounded transitive local-Markdown closure; that does not make every bundled file active context.

Generic bundles may include `project-engineering-memory.md`, the schema template, and deterministic validator documentation when reachable, but **must exclude** repository-root live `PROJECT-ENGINEERING-MEMORY.md`, its cold partitions/indexes, secrets/private evidence, and project-specific candidate state.

Serena, Semgrep, Hypothesis, CodeQL, compilers/debuggers/sanitizers/profilers/fuzzers and similar tools are optional environment capabilities, not generic Agent Skill validity requirements unless project/task authority explicitly requires one. Generic bundles do not embed executables, credentials, hosted-service configuration, analysis databases, compiler toolchains, or project-specific query/rule settings. Static package validity cannot establish external-tool availability or invocation.

## Qualification classes

- **Static source/package tests:** route syntax, safe/reachable packaged resources, canonical-source parity, activation invariants, PEM schema/package exclusion, profile/version identities.
- **Reference-routing sentinel:** fresh-session evidence that a named harness/model can discover/activate a skill and read a required bundled reference.
- **Tool-routing qualification:** named harness/model/tool evidence for specialized invocation or an allowed concrete fallback.
- **Protocol behavioral qualification:** inherited D1-D4/Challenge/evidence/compatibility scenarios plus Protocol 6.3 Q63/F63 memory semantics.

For live routing, use normal supported entrypoints and fresh sessions; do not preload the preservation map, expected leaf, or PEM family. Where traces exist, verify required conditional resources activate, unrelated memory/concerns remain cold, applicable lower-salience memory remains discoverable, and attention prioritization does not erase a mandatory closure condition.

## Lossless portability

Compact routing/handoffs remain complete for governed scope. A reference can replace local repetition only when the receiving environment can resolve the version-bound owner; otherwise carry the minimum necessary semantics locally. Cold historical/specialized/project-memory detail must remain discoverable through visible triggers. Generated routing graphs/matrices/traces and derived PEM summaries/indexes are diagnostic/derived evidence, not second routing/memory authority.

Protocol 6.2 remains accepted-current while 6.3 is a candidate. Version-bound 6.2 public fallback remains exact bootstrap `5a062ebc472755607b9dc66d33a5ebbc4b7429aa` and accepted recovery remains `b59adc77efe6951912cfd705cc43830c58ca27d0`. Version-bound 6.3 public fallback is usable only when the `6.3.0 public bootstrap` mapping above contains an immutable Git SHA; an unavailable sentinel means no 6.3 fallback is currently authorized. This does not make 6.3 accepted-current. Protocol 6.3 cannot displace the 6.2 baseline until complete qualification, independent Review, recovery mapping, regenerated parity, and lifecycle gates close.
