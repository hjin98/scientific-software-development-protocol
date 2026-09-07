# Software Development Protocol

Software Development Protocol 5 is an engineering-fitness-first workflow for AI-assisted software engineering. Current protocol version: **5.16**.

## Governing doctrine

```text
product engineering fitness > minimum justified product/system complexity > development economy
```

Tier 1 is intrinsic stakeholder/domain product truth plus high-level architecture explicitly Frozen by Software Design for the current implementation cycle. Lower-level realization remains Tier 2 and does not become invariant through existence, dependency, tests, documentation, prior plan wording, or previous repair. Development-process cost is Tier 3.

The durable stakeholder product is the objective. Workplans, tests, gates, metrics, reviews, reports, tools, language runtimes, and current implementation machinery are constraints, evidence, or solutions—not product truth.

## Active simplicity and long-horizon quality

A clean local bug receives a clean owning-layer repair. Repeated patches, wrappers/fallbacks/special cases, duplicated state/authorities, repeated reconciliation, or a materially simpler equivalent realization require Tier-2 simplification/re-derivation before another additive durable repair.

Protocol 5.16 adds an earlier-warning quality loop without replacing engineering judgment with scores. Complexity, churn, dependency structure, coverage, mutation survival, duplication, API/configuration growth, and related observations are **sensors, not verdicts**. Touched code follows a semantic quality ratchet: existing debt does not excuse making an affected subsystem harder to reason about unless Tier-1/Frozen requirements justify the added complexity.

The shared owner for these semantics is `source/shared/references/long-horizon-code-health.md`.

## Two-role lifecycle

```text
software-design -> software-implementation
```

Design separates original product/problem invariants from cycle-scoped Frozen architecture and delegated solution space. Implementation preserves Tier 1 while remaining free to reduce, consolidate, refactor, or replace Tier-2 machinery. Evidence that invalidates Frozen architecture routes back to Design on the affected surface.

Final accepted-contract reconciliation, final affected regression/integration, and project-required checks remain Implementation acceptance. Independent Review follows that evidence when warranted. Verification is a deeper risk-triggered Software Design mode; Stabilization is a non-mutating architecture-GC mode; Health Audit is periodic and longitudinal. These are not extra authority-bearing lifecycle roles.

## Development workflow prompt entrypoint

For repeatable human-to-agent orchestration use the canonical prompt reference:

- [`source/shared/references/development-workflow-prompts.md`](source/shared/references/development-workflow-prompts.md)

It provides parameterized entrypoints for optional Baseline/Change-Health Intake, Design/Workplan, Implementation, Review & Update, risk-triggered Verification, Stabilization/Architecture GC, downstream-workplan Alignment, periodic Health Audit, and Closeout.

By default, prompt orchestration resolves protocol skills **local first, public repository second**. Use the current harness's native installed-skill mechanism or exposed installed-skill root where available (for example `@software-design`, `/software-implementation`, or a harness-equivalent selector; these are not shell commands). If the required skill is absent, unreadable, or cannot preserve the governing protocol contract, fall back to the canonical public repository at `https://github.com/hjin98/software-development-protocol` and read the appropriate canonical `source/` skill plus required references. Never silently reinterpret an older accepted workplan under newer doctrine.

## Test effectiveness, architecture fitness, and failure paths

Protocol 5.16 makes several evidence classes explicit while keeping them conditional:

- mutation/counterfactual evidence for test-oracle strength;
- differential and metamorphic testing where exact fixture oracles are weak;
- executable architecture-fitness checks for objective, stable dependency/ownership rules;
- changed-code/affected-surface quality ratchets rather than arbitrary whole-repository thresholds;
- bounded deterministic fault injection for material restart/recovery/failure claims through the real semantic owner.

Tool identity remains delegated. Optional capabilities never form a mandatory pipeline.

## Language-native engineering

Protocol 5.15 introduced thin differential language profiles, preserved by 5.16:

```text
shared domain rule -> language profile(s) -> implementation-local realization
```

Material executable Python work loads the Python profile; material C++ work loads the C++ profile; mixed Python/C++ boundaries load both. Protocol 5.16 additionally gives Python project-configured fast lint/static typing first-class routing parity with the existing C++ compiler/static-analysis path.

## Periodic software maintenance audit

Protocol 5.16 adds one optional `software-maintenance-audit` specialist. It combines semantic inspection with available longitudinal evidence such as churn, temporal change coupling, complexity, centrality, recurring defects, weak tests, duplicated authority, dependency drift, configuration/API growth, and documentation difficulty. Metrics remain sensors. If history is unavailable, the audit must not fabricate trends. Findings route back through ordinary Design/Implementation, documentation, or repository-hygiene authority.

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

When the SDP Orchestrator under `orchestrator/` is affected, also run its acceptance suite:

```bash
python -m pip install ./orchestrator/packages/core -r orchestrator/packages/core/requirements-dev.txt
python orchestrator/scripts/generate_protocol_snapshot.py --check
python orchestrator/scripts/run_core_tests.py
```

All orchestrator implementation, test, fixture, script, and documentation files live under `orchestrator/`; repository-level CI invokes those commands but hosts no orchestrator logic. See `orchestrator/docs/core-user-guide.md`.

These Python commands are repository-local Tier-2 validation machinery, not language-specific protocol doctrine.
