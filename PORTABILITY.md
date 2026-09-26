# Agent Portability and Routing Qualification

## Installation contract

The supported portable runtime unit is `dist/skills/<skill-name>/`; each top-level ZIP contains the same files under one enclosing skill directory. `source/` is canonical development source and ZIPs are transport artifacts.

Authority roles are `scientific-formulation`, `numerical-algorithm-design`, `software-design`, and `software-implementation`. Optional non-authoritative specialists are `software-documentation`, `software-maintenance-audit`, and `repository-hygiene`.

## Routing contract

The universal routing/representation kernel is `source/shared/references/abstraction-and-concretization.md`; it holds only cross-domain semantics, while specialized semantic-definition detail, authority lifecycle, and the Project Engineering Memory schema load from their own owners when a predicate fires. Package membership is not activation.

Four boundaries are qualified separately:

```text
catalog discovery/selection (frontmatter name/description; optional vendor adapters)
 -> root activation (SKILL.md loaded)
 -> conditional concern-owner loading (explicit predicates)
package transport closure (every routed owner present in the bundle) is a fourth, separate property
```

Frontmatter `name`/`description` is the portable selection surface: a short task-class plus exclusion interface, never compressed doctrine or mutable release state. `agents/openai.yaml` is a vendor adapter validated separately; a missing or broken adapter does not invalidate the generic core bundle. Selection metadata that finds the right root does not prove its conditional owners were read, and correct internal routing cannot repair a root that was never selected.

The active role/specialist `SKILL.md` owns root activation and carries a build-inlined entry contract (governing-version step plus the kernel's minimal pre-routing safety kernel), because the entrypoint is the surface a portable runtime reliably consumes. It routes to its owning concern and, when a materiality, delegation, rigor, verification or representation question arises, the full universal kernel; a concern owner may conditionally dispatch to a narrower leaf only within that concern.

```text
activation -> required source/package reachability
reachability / ordinary Markdown link / semantic dependency / definition trace / package membership != activation
```

A canonical semantic prerequisite can be source-resolvable yet unavailable to a current inference until its exact version-bound content is supplied/loaded. Progressive disclosure loads required owners while keeping unrelated concerns cold.

PEM doctrine/template may be packaged; live project `PROJECT-ENGINEERING-MEMORY.md`, derived local summaries/overlays, and root `PROTOCOL-RELEASE-STATE.yaml` are project state and are never copied into generic skill/profile packages.

## Compatible source resolution

Resolve a local/installed source of the declared version first; a newer installed successor is not that source and is never adopted without an explicit decision by the authority over the task/workplan. Remote fallback, when allowed, uses only an exact immutable ref supplied by task/project authority or the designated project release-state mapping. Never use default/latest or guess a semantic-version Git ref.

For this repository, current exact public/recovery mappings are owned by `PROTOCOL-RELEASE-STATE.yaml`; detailed release chronology remains in semantic history. Immutable version-bound mappings remain distinct from the mutable accepted-current designation.

## Version-bound profiles

| Profile | Protocol | Schema | State |
| --- | --- | ---: | --- |
| `sdp-protocol-5.16` | 5.16.0 | 1 | frozen historical |
| `ssdp-protocol-6.0` | 6.0.0 | 2 | frozen historical |
| `ssdp-protocol-6.1` | 6.1.0 | 2 | frozen historical |
| `ssdp-protocol-6.2` | 6.2.0 | 2 | frozen historical |
| `ssdp-protocol-6.3` | 6.3.0 | 2 | frozen historical |
| `ssdp-protocol-6.4` | 6.4.0 | 2 | frozen historical |
| `ssdp-protocol-6.5` | 6.5.0 | 2 | frozen version-bound |
| `ssdp-protocol-6.6` | 6.6.0 | 2 | current source profile |

Which profile is accepted-current is release state, resolved from `PROTOCOL-RELEASE-STATE.yaml`. The 6.x family retains schema v2 because current semantic strengthening, including 6.6's representation changes, does not change the machine stage/result-envelope graph or lifecycle/control ownership. Every previously published profile remains byte-stable and independently testable.

## Manual operation and transient state

Every skill is usable by hand from its installed files: no Orchestrator, hosted service, vendor model, multi-agent runtime, memory service or evaluation harness is required. Working State checkpoints, handoff projections, memory query/index output and evaluation results are derived coordination views, never hidden runtime authority. At entry, a task or workplan that declares a `protocol_version` is compared with the package `PROTOCOL_VERSION`; a mismatch resolves a source of the declared version or its exact immutable source, else reports non-closure, rather than reinterpreting or self-adopting the loaded package (this repository ships an offline helper, `source/version_preflight.py`).

## Formal-definition portability boundary

Portable packages carry enough canonical owner routes to recover materially required definition/import/source/warrant semantics without hidden chat. Generated traces may reduce search cost but are not semantic authority and may claim completeness only for an explicitly bounded reviewed scope.

## Project-memory portability boundary

PEM remains conditionally activated. Generic packages include the agent-facing memory contract, the cold schema/governance owner and the template only; project-local memory stays with the governed project. Missing/partial memory cannot prove historical absence.

## Optional environment capabilities and live tool qualification

External analyzers and tool integrations are **optional environment capabilities**, not generic agent skill validity requirements. Install a skill as a direct child of the supported skills root independently of whether optional external tools are installed.

A **reference-routing sentinel** and other static package/routing validation can establish that the correct reference path is packaged and discoverable. Static package/routing validation cannot prove live tool availability, invocation, behavioral correctness, or model/harness routing behavior.

Tool-routing qualification is bound to the **named harness/model/install mode** and tool environment actually exercised. Record named harness/model/tool evidence and concrete fallback behavior. Do not infer another environment from one run, and do not generalize one live result to an untested harness/model/tool combination.

## Packaging and qualification

Static validation can establish route/resource integrity, schema/package exclusion, generated parity and other mechanically decidable properties. It cannot prove that a model followed a route, loaded a prerequisite before inference, obtained semantic correctness from prose, or improved engineering outcomes.

Mechanical qualification therefore names its exact subject/property. Semantic adequacy is independently reviewed against the assembled protocol; live harness/model performance claims require live evidence.

## Lossless portability

A package need not eagerly include every historical narrative in active context, but every materially required current owner must remain resolvable. One detailed generic owner plus local consequence is preferred over duplicated current rules. Historical resources remain frozen and discoverable without becoming competing current authority.
