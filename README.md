# Software Development Protocol

Software Development Protocol 5 is an engineering-fitness-first workflow for AI-assisted software engineering. Current protocol version: **5.15**.

## Governing doctrine

```text
product engineering fitness > minimum justified product/system complexity > development economy
```

Tier 1 is intrinsic stakeholder/domain product truth plus high-level architecture explicitly Frozen by Software Design for the current implementation cycle. Lower-level realization remains Tier 2 and does not become invariant through existence, dependency, tests, documentation, prior plan wording, or previous repair. Development-process cost is Tier 3.

The durable stakeholder product is the objective. Workplans, tests, gates, metrics, reviews, reports, tools, language runtimes, and current implementation machinery are constraints, evidence, or solutions—not product truth.

## Active simplicity

Tier 2 is an active restoring policy. A clean local bug receives a clean owning-layer repair, but repeated patches, wrappers/fallbacks/special cases, duplicated state/authorities, repeated reconciliation, or a materially simpler equivalent realization require simplification/re-derivation before another additive durable repair.

## Two-role lifecycle

```text
software-design -> software-implementation
```

Design separates original product/problem invariants from cycle-scoped Frozen architecture and delegated solution space. Implementation preserves Tier 1 while remaining free to reduce, consolidate, refactor, or replace Tier-2 machinery. Evidence that invalidates Frozen architecture routes back to Design on the affected surface.

Affected-surface growth expands implementation/testing impact; it does not itself create requirements. Proxy-proof acceptance follows the real owner of the final accepted realization.

## Development workflow prompt entrypoint

For repeatable human-to-agent orchestration of Design, Implementation, Review, Verification, Stabilization, Alignment, Health Audit, and Closeout, use the canonical prompt reference:

- [`source/shared/references/development-workflow-prompts.md`](source/shared/references/development-workflow-prompts.md)

Each prompt exposes an `INPUTS` block so task-specific values such as workplan path, implementation target, governing authorities, and protocol source are defined once and referenced symbolically throughout the stage prompt. These prompts route into the protocol; they do not create a parallel authority model.

## Language-native engineering

Protocol 5.15 preserves one shared doctrine and adds thin differential language profiles:

```text
shared domain rule -> language profile(s) -> implementation-local realization
```

Material executable Python work loads the Python profile; material C++ work loads the C++ profile; mixed Python/C++ boundaries load both. Shared architecture, testing, scientific, security, performance, concurrency, storage, release, and versioning references remain canonical.

The profiles prevent lowest-common-denominator code: Python should exploit its high-level runtime/library model without denying compiled numerical performance, while C++ should exploit explicit lifetime/value/build semantics without importing dynamic-language machinery or gratuitous low-level cleverness.

## Performance and complexity

Shared performance doctrine prioritizes algorithm/work reduction, data representation and movement, established optimized kernels, effective resource discovery, appropriate execution classes, and representative profiling before low-level specialization.

A clearly equivalent efficiency improvement that removes work/copies/allocation without adding material complexity can proceed without pre-benchmark ceremony, but a quantitative performance claim requires comparable measurement. New native boundaries, bespoke kernels, explicit SIMD dispatch, additional parallel runtimes, custom allocators, backend matrices, governed PGO/LTO, and accelerator support require evidence that their total-system benefit earns their complexity.

GPU/accelerator implementation is dormant unless Tier-1/Frozen architecture explicitly enables it.

## Deterministic progressive disclosure

Protocol 5.15 preserves Protocol 5.13 relation-first optional-tool routing while generalizing the capability classes:

```text
literal/path/text -> ordinary repository search/read
symbol ownership/reference -> semantic capability
AST/syntax/structural family -> structural analyzer
broad input/state invariant -> language-appropriate property/generative method
interprocedural flow -> data-flow analyzer
runtime state/crash -> debugger evidence
memory/lifetime/UB -> language-appropriate instrumentation
race/synchronization -> concurrency/race evidence
performance/vectorization -> profiler/compiler/hardware evidence
```

Serena, Semgrep, Hypothesis, CodeQL, compiler-native C++ tools, sanitizers, debuggers, profilers, and fuzzers are bounded optional evidence instruments. Tool presence never creates a mandatory pipeline.

## Acceptance and convergence

Executable changes retain focused checks, stage-local affected regression for material behavior-changing stages, final affected-surface re-derivation/regression, integration through real product/consumer boundaries, project-required checks, proxy-proof real-owner acceptance, and separate production qualification where material.

A first clean local defect remains local. Material recurrence moves reasoning to the shared owner/mechanism; if recurrence also exposes solution complexity, simplification precedes another additive durable closure.

## Repository layout and validation

`source/` is canonical. `dist/skills/<skill-name>/` contains ready-to-install generated bundles; top-level ZIPs are backward-compatible generated transports. See `PORTABILITY.md` for installation and routing qualification.

Before a protocol revision is complete:

```bash
python -m pip install -r source/requirements-validation.txt
python -m unittest discover -s tests -v
python source/build_skills.py --output /tmp/protocol-dist
python source/validate_packages.py --dist /tmp/protocol-dist
python source/check_dist.py --expected /tmp/protocol-dist --committed dist
git diff --check
```

These Python commands are repository-local Tier-2 validation machinery, not language-specific protocol doctrine.