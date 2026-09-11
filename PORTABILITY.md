# Agent Portability and Routing Qualification

## Installation contract

The supported portable runtime unit is the self-contained directory `dist/skills/<skill-name>/`; each top-level ZIP contains the same files under one enclosing skill directory. Install a skill as a direct child of the harness-supported skill root so `<skills-root>/<skill-name>/SKILL.md` exists. `source/` is canonical development source; ZIPs are transport artifacts. A shared/symlinked install is a separate harness capability and must be qualified on that harness.

Authority roles: `scientific-formulation`, `numerical-algorithm-design`, `software-design`, `software-implementation`. Optional non-authoritative specialists: `software-documentation`, `software-maintenance-audit`, `repository-hygiene`.

## Protocol 6.2 routing contract

The active role/specialist `SKILL.md` owns **root activation**. It routes to the universal kernel/owning concern; a canonical concern owner may conditionally dispatch to a narrower leaf only within that concern. Each activation edge states a decision predicate and resolvable resource, remains acyclic, adds/narrows material semantics, and reuses already-loaded applicable owners rather than reloading them.

The canonical universal-kernel source is `source/shared/references/abstraction-and-concretization.md`; inside a packaged skill it is reached as `references/abstraction-and-concretization.md`.

```text
activation -> required source/package reachability
reachability / ordinary Markdown link / semantic dependency / package membership != activation
```

`language-profiles.md` is the language concern router and conditionally activates Python/C++ leaves. `tool-assisted-engineering.md` is the relation-first engineering-tool router and conditionally activates analyzer/runtime/tool methods. Do not flatten all leaves into every role entrypoint or infer activation from the transitive files bundled for standalone transport.

Static package/routing validation can establish declared route and resource integrity. It **cannot prove** that a named harness/model actually followed the route, kept non-triggered material cold, or gained performance. Live claims require fresh-session evidence for the named harness/model/install mode; unavailable telemetry remains unavailable rather than inferred.

## Compatible source resolution

Resolve declared-version-compatible skills local first, canonical public source second. Never reinterpret an older workplan under the newest installed skill merely because it is available.

Accepted immutable mappings:

```text
5.16.0 recovery -> e151daaf5c8eebb351a85cfed86170fda80fb5e3
6.0.0 recovery  -> 21d5188f5bd9a0270d7a2ebf93d41a6b7842ccd2
6.1.0 public bootstrap -> 47e9155632c44493644b0b02fa1fa625703cf480
6.1.0 recovery -> 802e75af261efb4f70d71284d860613a2197b639
```

Canonical repository: `https://github.com/hjin98/scientific-software-development-protocol`.

The first Protocol 6.2 pre-acceptance bootstrap attempt, `1181c2031710c5d343194d87d08543290fded0ab`, is invalidated because it predates a required explicit `software-documentation` cold-route repair. It remains historical evidence only and must not be used as current 6.2 public fallback.

A replacement 6.2 bootstrap source snapshot intentionally cannot self-name. Until a later current-source mapping publishes its exact immutable validated SHA, **automatic current-6.2 public fallback is unavailable**: if no governing-version-compatible installed skill/exposed root is readable, report truthful non-closure rather than use the invalidated attempt, repository default branch, latest, or a guessed `6.2.0` ref. If the replacement snapshot has already been reached through an explicit immutable ref or a later exact mapping, continue using that resolved source rather than resolving again.

## Version-bound profiles

| Profile | Protocol | Schema | State |
| --- | --- | ---: | --- |
| `sdp-protocol-5.16` | 5.16.0 | 1 | frozen |
| `ssdp-protocol-6.0` | 6.0.0 | 2 | frozen |
| `ssdp-protocol-6.1` | 6.1.0 | 2 | accepted-current until 6.2 closeout |
| `ssdp-protocol-6.2` | 6.2.0 | 2 | candidate successor; accepted only after 6.2 qualification/Review/recovery closeout |

Historical profile/prompt bytes remain immutable. Workplan `protocol_version` selects compatible semantics before stage interpretation. Serious Challenge/human-pending state stops ordinary automatic closure; orchestration represents/routes state but never decides scientific truth.

## Packaging and external capabilities

Standalone bundles must contain every local resource any supported activation path can require and every local Markdown resource needed to keep the bundled document graph non-dangling. Current transport may therefore use bounded transitive local-Markdown closure; that transport choice does not make every bundled file active context.

Serena, Semgrep, Hypothesis, CodeQL, compilers/debuggers/sanitizers/profilers/fuzzers and similar tools are optional environment capabilities, not generic Agent Skill validity requirements unless project/task authority explicitly requires one. Generic bundles do not embed executables, credentials, hosted-service configuration, analysis databases, compiler toolchains, or project-specific query/rule settings. Static package validity cannot establish external-tool availability or invocation.

## Qualification classes

- **Static source/package tests:** route syntax, safe/reachable packaged resources, canonical-source parity, activation invariants that can be inspected from source, profile/version identities.
- **Reference-routing sentinel:** fresh-session evidence that a named harness/model can discover/activate a skill and read a required bundled reference.
- **Tool-routing qualification:** named harness/model/tool evidence for specialized invocation or an allowed concrete fallback; do not infer another environment from one run.
- **Protocol behavioral qualification:** current D1-D4 authority, Challenge, evidence, compatibility and Protocol 6.2 representation/routing scenarios.

For live routing, use normal supported entrypoints and fresh sessions; do not preload the preservation map or expected leaf. Where traces exist, verify required conditional resources activate, non-triggered concerns remain cold, and attention prioritization does not erase a lower-salience mandatory closure condition.

## Lossless portability

Compact routing/handoffs remain complete for governed scope. A reference can replace local repetition only when the receiving environment can resolve the version-bound owner; otherwise carry the minimum necessary semantics locally. Cold historical/specialized detail must remain discoverable through visible triggers. Generated routing graphs/matrices/traces are diagnostic evidence, not a second routing authority.

Protocol 6.1 remains accepted-current/rollback until 6.2 qualification, independent candidate Review, immutable recovery mapping, generated-artifact reconciliation and lifecycle closeout all pass.