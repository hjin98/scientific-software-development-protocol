---
kind: implementation-workplan
workplan_id: PROTOCOL-5.16-LONG-HORIZON-CODE-HEALTH-AND-AUTONOMOUS-QUALITY
protocol_version: 5.15.0
target_protocol_version: 5.16.0
status: completed
completed_date: 2026-09-06
base_commit: be3a461f98c2e958b110c7c8591612fc14eef073
---

# Protocol 5.16 Long-Horizon Code Health and Autonomous Quality Workplan

## Objective / problem invariants / non-goals

### Original problem

Protocol 5.15 has strong doctrine for product truth, Frozen architecture, delegated solution space, active simplicity, affected-surface validation, proxy-proof acceptance, convergence, and language-native engineering. It is already effective at preventing obvious patch-on-patch preservation of accidental implementation machinery.

The remaining long-horizon failure mode is different: a repository can still degrade gradually across many locally defensible changes before structural complexity becomes obvious enough to trigger active simplification. Current protocol control is therefore stronger at reasoning about already-visible complexity than at observing early longitudinal deterioration, independently falsifying apparently correct implementations, and scheduling maintenance before a crisis.

A second control-plane problem is now explicit: the protocol is used across heterogeneous agent harnesses. Skills are often installed locally, but may be absent or inaccessible in a web session. Human prompts therefore need a reliable, version-coherent way to activate the correct stage/skill locally when possible and fall back to the canonical public protocol source when not. Without that routing, a strong protocol can still fail simply because the wrong skill, wrong protocol version, or no skill was actually loaded.

Protocol 5.16 must strengthen the development system as a closed-loop engineering process:

```text
product truth
    -> design / implementation
    -> executable evidence
    -> independent review / adversarial falsification
    -> structural and test-effectiveness signals
    -> longitudinal health observations
    -> simplification / redesign trigger
    -> product truth
```

The protocol must improve early detection of architectural entropy, weak test oracles, change-risk concentration, lifecycle residue, stage-routing mistakes, and slowly growing maintenance burden without replacing engineering judgment with metric thresholds or adding bureaucratic approval machinery.

### Product invariants

1. **Preserve Protocol 5 authority.** Tier 1A product/problem truth, Tier 1B cycle-scoped Frozen high-level architecture, Tier 2 delegated solution machinery, and Tier 3 development economy remain unchanged.
2. **Preserve the two authority-bearing lifecycle roles.** `software-design -> software-implementation` remains the complete normative lifecycle. Verification, stabilization, health audit, qualification, documentation, and hygiene are modes/stages/specialists, not new approval authorities.
3. **Preserve existing functional-acceptance ordering.** Implementation must complete final accepted-contract reconciliation, final affected-surface regression/integration, and repository/project-required checks before an independent implementation review can claim review readiness. Protocol 5.16 must not move adversarial verification ahead of the existing final assembled acceptance boundary.
4. **Keep Review, Verification, Stabilization, and Health Audit semantically distinct.** Review asks whether the governing implementation contract was correctly realized; Verification independently falsifies high-risk scientific/product/architectural claims when warranted; Stabilization asks whether an otherwise accepted realization should be simplified; Health Audit examines longitudinal repository deterioration. They must not become duplicate mandatory review gates.
5. **Simplicity remains semantic, not numeric.** No universal CRAP, complexity, coverage, mutation-score, line-count, API-count, or similar threshold may define product correctness or architectural fitness by itself.
6. **Metrics are sensors, not product truth.** Complexity, churn, dependency, coverage, mutation, duplication, hotspot, public-surface, and similar observations may trigger investigation or prioritization but do not automatically require redesign or acceptance failure unless project/task authority explicitly elevates a threshold.
7. **Use quality ratchets rather than arbitrary repository-wide cleanup gates.** Existing debt does not excuse introducing new debt. A materially touched subsystem should ordinarily become no harder to reason about unless added complexity is required by Tier-1/Frozen requirements.
8. **Strengthen oracle quality.** High coverage or green tests are insufficient when semantically wrong implementations can survive. Mutation, differential, metamorphic, property, counterfactual, real-owner, and bounded fault-injection evidence should be used when they materially strengthen a claim.
9. **Independent verification should be genuinely adversarial.** Review/verification should attempt to falsify the implementation or claim rather than merely confirm the implementer's explanation. Operational separation of verifier context from implementation rationale is preferred when practical.
10. **Architecture fitness should become executable where the rule is objective.** Dependency direction, forbidden coupling, acyclicity, ownership boundaries, or equivalent structural invariants should be encoded as executable checks when doing so is cheap, stable, and semantically justified.
11. **Longitudinal maintenance is periodic and evidence-driven.** Repository-level health audits inspect trends such as churn x complexity x test weakness x architectural centrality, recurring defect families, dependency drift, duplicated concepts, public/configuration growth, and stale compatibility paths without turning every local change into a whole-repository audit.
12. **Scientific correctness remains primary.** Numerical/scientific invariants, trusted reference implementations, justified tolerances, differential/metamorphic relations, reproducibility, and relevant failure/restart semantics remain authoritative over test metrics or optimization goals.
13. **Maintenance findings do not mutate authority.** A health audit may identify risks and simplification opportunities, but it does not define new Frozen architecture or become workplan approval authority. Tier-2 work routes through ordinary Implementation authority; any material new/revised implementation contract or Frozen-architecture concern routes through Software Design.
14. **Protocol self-qualification must test behavior, not only wording.** Static phrase/structure tests remain useful regression guards, but real protocol-confidence claims should include bounded behavioral scenarios that distinguish good engineering decisions from attractive but wrong ones.
15. **Repository lifecycle state should converge.** Completed/superseded workplans and post-stage residue must not remain indefinitely active merely because cleanup is optional; closeout triggers should make stale lifecycle state observable and routinely correctable.
16. **Human-facing orchestration is part of the protocol control surface, not a parallel authority.** A canonical prompt reference must expose stage-specific parameter blocks, deterministic stage/skill routing, and portable skill resolution while remaining subordinate to the governing workplan, protocol version, and canonical skill/reference doctrine.
17. **Portable skill resolution is local-first and version-coherent.** When a required protocol skill is available through the current harness or an exposed installed-skill root, use the compatible local installation first. If unavailable, unreadable, or incompatible, fall back to the canonical public repository `https://github.com/hjin98/software-development-protocol`. Never silently reinterpret an older workplan under a newer protocol or claim a skill was loaded when it was not.

### Non-goals

- Do not replace Protocol 5.15's philosophy or authority model.
- Do not create a mandatory third approval role for testing, QA, verification, stabilization, or maintenance.
- Do not introduce a universal quality score, complexity ledger, deletion quota, refactoring quota, or permanent metric bureaucracy.
- Do not require mutation testing, fuzzing, CodeQL, Semgrep, Serena, Hypothesis, coverage, architecture linting, failure injection, or any other tool/method on every task.
- Do not require whole-repository health audits or stabilization after ordinary local changes.
- Do not turn maintainability tools into product truth or let agents optimize metrics at the expense of architecture.
- Do not introduce one specialist per tool category or one specialist per development stage.
- Do not mandate one Python linter/type checker, one C++ analyzer, one mutation engine, one coverage implementation, one architecture-test library, one fault-injection framework, or one hotspot-analysis product.
- Do not assume every harness can programmatically execute textual selectors such as `@software-design` or `/software-design`; they are examples of harness-native selectors, not shell commands.
- Do not create per-harness copies of protocol doctrine merely to support routing.
- Do not fetch the public repository when a readable governing-version-compatible local skill is already available merely for ceremony.
- Do not retroactively reinterpret older workplans under Protocol 5.16.

## Frozen high-level architecture and engineering envelope

### Frozen lifecycle architecture

Protocol 5.16 keeps the existing two-role lifecycle and adds bounded quality-feedback modes around the existing acceptance contract:

```text
baseline / change-health intake when material
        -> Software Design
        -> Software Implementation + stage-local semantic/functional validation
        -> final accepted-contract reconciliation
        -> final affected-surface regression + real-boundary integration + project checks
        -> independent Review & Update when warranted
             -> implementation repair or bounded Design reconsideration when blocked
        -> independent claim-level Verification when warranted
        -> Stabilization / architecture-GC at material convergence boundaries when warranted
             -> if change is required, route through Design/Implementation + fresh final acceptance/review
        -> production qualification when independently required
        -> documentation + repository closeout when affected

periodic Health Audit sits outside the per-change linear path
        -> ordinary Tier-2 repair/implementation path when sufficient
        -> Software Design when a workplan/Frozen-architecture decision is required
```

These are proportionate activities, not mandatory fixed gate counts. Small/local changes may still use the compact Protocol 5 workflow. Full production qualification remains separate and assumes regression/integration acceptance already exists.

### Stage semantics and orchestration boundaries

The quality-feedback modes have deliberately different questions and closure semantics:

- **Baseline / change-health intake:** for substantial or structurally risky work, capture only the task-local evidence needed to compare the touched system before/after. It may be an explicit user-facing stage or an explicitly triggered preamble to Design; it is not a permanent ledger.
- **Review & Update:** Software Design independently reviews an implementation that has already reached normal implementation completion evidence. It decides Pass / No-Pass against the governing workplan plus material engineering risks and routes rework.
- **Verification:** a separate optional Software Design mode for high-risk scientific, numerical, product, or architectural claims where deeper falsification across multiple sources of truth materially increases confidence. Verification does not replace ordinary workplan review and is not mandatory merely because Review exists.
- **Stabilization / architecture-GC:** a non-mutating review mode after ordinary implementation review has otherwise passed. It asks whether the accepted realization remains the minimum justified Tier-2 system. Any resulting code change must return through the normal Design/Implementation/acceptance/review path; Stabilization itself does not refactor production code.
- **Health Audit:** periodic repository-level trend analysis. It is not a feature gate, and it must report when longitudinal evidence is unavailable rather than pretending a static snapshot establishes a trend.
- **Closeout:** documentation/lifecycle/hygiene reconciliation after the relevant semantic and functional engineering stages close. It must not alter product behavior.

### Portable protocol-skill resolution architecture

The canonical human-facing workflow prompt reference must support a harness-neutral resolver:

1. Determine the required skill for the selected stage.
2. Under the default local-first mode, inspect the current harness's available skill/plugin/command registry or documented exposed installed-skill root and use the native selector/invocation mechanism when available. Examples such as `@software-design` or `/software-implementation` are harness selectors, not shell commands.
3. Prefer an exact governing-protocol installation. A newer skill may serve an older workplan only when it explicitly supports preserving that older protocol contract; backward-compatible release numbering alone does not authorize silently applying newer doctrine to an older accepted workplan.
4. If the required local skill is absent, inaccessible, unreadable, or cannot preserve the governing protocol contract, fall back read-only to `https://github.com/hjin98/software-development-protocol`. Use canonical `source/roles/<skill>/SKILL.md` or `source/specialists/<skill>/SKILL.md` plus the references that entrypoint requires. Do not treat generated `dist/` bundles as the canonical repository authority.
5. Resolve historical protocol versions by an explicit branch/tag/commit/release/version mapping or other repository evidence. Do not guess that a semantic version string is a Git ref. If a compatible historical source cannot be established, report the limitation instead of silently using `main`/latest.
6. If neither compatible local nor public source is readable, report truthful non-closure and use only an explicitly documented stage fallback. Do not execute a similarly named unrelated skill or claim protocol compliance from memory.

Exact harness syntax and local installation path are delegated portability details. The authority/version semantics above are Frozen for this cycle.

### Baseline and quality-ratchet model

For substantial or structurally risky work, establish only the baseline information needed to determine whether the changed subsystem regressed in maintainability or behavioral protection. Candidate baseline evidence may include:

- existing tests and important real-owner acceptance paths;
- affected dependency/ownership structure;
- selected complexity/hotspot indicators;
- reference numerical behavior;
- public/configuration surface relevant to the change;
- known recurring defect or compatibility paths;
- candidate identity needed for later comparison.

Do not require a persistent health ledger. The baseline may remain task-local unless project/release policy independently requires durable reporting.

The quality ratchet is semantic:

> A touched subsystem should ordinarily not become harder to reason about, more weakly tested, more cyclic, more duplicated in authority, or more dependent on special-case machinery unless the additional complexity is justified by Tier-1/Frozen requirements.

Metrics and structural scans can support that judgment but do not replace it.

### Adversarial review and verification model

Independent review remains a Software Design mode and starts from a candidate that has the existing final implementation/functional acceptance evidence or explicitly reports missing evidence as a blocker. For substantial/high-risk work, strengthen operational independence:

- reconstruct the product/Frozen contract from supplied authority and actual repository state;
- inspect the final candidate before relying on the implementer's rationale;
- attempt to falsify important claims through counterexamples, boundary cases, mutation-like perturbations, alternative state transitions, real-owner execution, affected-consumer inspection, numerical/metamorphic relations, structural violations, or bounded failure injection where the claim is about failure/recovery;
- prefer a fresh context/model instance when practical so the verifier is not anchored by the implementer's full reasoning trajectory;
- only after independent reconstruction, consult implementation rationale when it resolves a real ambiguity.

Ordinary Review still answers workplan conformance plus independent engineering challenge. The separate Verification stage is reserved for materially high-risk claim-level falsification and broader authority reconciliation. Neither creates a third authority role.

### Stabilization / architecture-GC model

At natural convergence boundaries such as completion of a major workplan, feature cluster, architecture migration, or release candidate, perform a bounded stabilization pass when accumulated change is material. Ask:

> If this implementation had appeared fully formed today, would this still be the minimum justified realization of the accepted product/Frozen architecture?

Inspect especially:

- duplicated concepts or authoritative representations;
- wrappers/adapters/fallbacks/special cases;
- compatibility paths whose support obligation has ended;
- unnecessary configuration/public API surface;
- ownership splits and repeated reconciliation;
- state transitions that primarily manage internal machinery;
- obsolete temporary seams or implementation scaffolding;
- dependency cycles or architecture-boundary drift;
- tests that mostly compensate for internal orchestration rather than protect product semantics.

Stabilization itself does not edit production implementation. If Tier-2 simplification is justified, create/reconcile the minimum bounded implementation contract needed and route the change through normal Implementation plus fresh final acceptance/review. Any required Frozen-architecture change routes to bounded Software Design reconsideration.

## Implementation obligations and delegated solution space

### Obligation 1 — Extend testing doctrine with test-effectiveness routing

**Concern / rationale:** Current testing doctrine correctly rejects green-test complacency but lacks a positive route for mutation-based oracle-strength analysis.

**Required end state:** `testing-and-validation.md` and tool-routing doctrine must explicitly recognize test-effectiveness/oracle-strength questions as a capability class. Mutation testing must remain conditional and non-authoritative. The doctrine should also include the bounded counterfactual: identify the smallest plausible semantically wrong implementation that could still pass the current tests, then strengthen the oracle when that counterexample is material and economically testable.

**Delegated solution space:** Exact wording, tool examples, and placement may vary. Python/C++ examples may name representative tools, but no tool identity is Frozen.

**Acceptance evidence:** Static protocol tests plus behavioral scenarios must demonstrate that mutation/counterfactual oracle challenge is neither universally mandatory nor ignored when an important weak-oracle question materially warrants it.

### Obligation 2 — Add differential and metamorphic testing explicitly

**Concern / rationale:** Scientific doctrine already supports invariants and trusted reference implementations, but the methodological categories should be explicit so agents reliably reach them when exact oracles are difficult.

**Required end state:** Testing/scientific references explicitly describe:

- differential testing between trusted/reference and optimized/new implementations;
- metamorphic testing through governed transformations and relations;
- property/stateful testing where broad input/state spaces matter;
- counterfactual tests that distinguish known-broken from corrected behavior.

For scientific/numerical work, examples should include transformations such as permutation, restart/continuation equivalence, unit-consistent transformation, symmetry/invariance/equivariance, backend equivalence, and normalized-weight invariants where relevant.

**Acceptance evidence:** Protocol tests and at least one bounded qualification scenario establish that an agent can choose metamorphic/differential evidence when fixture equality is insufficient.

### Obligation 3 — Add maintainability / architecture-fitness capability classes

**Concern / rationale:** Active simplicity is currently detected mostly through semantic inspection after complexity becomes visible.

**Required end state:** `tool-assisted-engineering.md` must gain non-authoritative capability classes for materially useful questions including:

```text
test effectiveness / oracle strength -> mutation or equivalent semantic perturbation evidence
changed-code behavioral protection -> diff/changed-surface coverage evidence
objective dependency/architecture invariant -> architecture/dependency fitness checks
complexity / duplication / maintainability hotspot -> language-appropriate static metrics
longitudinal maintenance risk -> VCS churn/change-coupling + structural/test-risk evidence
```

These routes must preserve the existing relation-first, minimum-sufficient-tool doctrine.

**Acceptance evidence:** New static/counterfactual routing tests demonstrate positive routing, permitted fallback, and explicit rejection of universal mandatory pipelines or metric authority.

### Obligation 4 — Strengthen Python static correctness routing

**Concern / rationale:** The C++ profile explicitly names compiler diagnostics and clang-tidy-class analysis, while the Python profile currently gives less explicit status to ordinary fast lint/type/static semantic checks.

**Required end state:** The Python profile should explicitly route ordinary Python static correctness to the project's configured fast lint/type/static analysis capabilities when material, with representative examples such as Ruff-class and Pyright/mypy-class tools. Tool identity remains delegated.

**Acceptance evidence:** Language-profile tests verify the routing semantics without requiring any exact vendor/tool.

### Obligation 5 — Define executable architecture-fitness guidance

**Concern / rationale:** Architectural ownership and dependency direction are central protocol concepts but are often left as prose-only constraints even where the rule is mechanically testable.

**Required end state:** Architecture/testing doctrine should state that objective, stable architectural rules may be encoded as executable checks, including examples such as:

- forbidden imports/dependencies;
- layer direction;
- acyclic package/subsystem relationships;
- independence constraints;
- structural absence/uniqueness of deprecated ownership paths.

Do not require a global machine-readable architecture manifest. Encode only rules with clear semantic value and stable ownership.

**Acceptance evidence:** Behavioral qualification includes a scenario where an agent correctly prefers an executable dependency invariant over repeated prose-only review when the architectural rule is objective.

### Obligation 6 — Make independent review explicitly falsification-oriented while preserving review readiness

**Concern / rationale:** Independent review is already owned by Software Design, but operational independence and anti-anchoring behavior are under-specified. The original draft also placed adversarial verification before final regression/integration, which would have contradicted existing Protocol 5 implementation acceptance.

**Required end state:** `software-design`, workflow, and testing references must make clear that:

- substantial/high-risk independent Review attempts to falsify the candidate and reconstructs the contract independently;
- ordinary Review begins after final implementation reconciliation plus final affected regression/integration/project-required checks are available, or explicitly records those missing checks as blockers;
- a separate deeper Verification mode may follow Review when scientific/numerical/product/architectural claim risk warrants it;
- Verification does not replace ordinary workplan review or turn into a mandatory second review for routine changes;
- fresh-context verification is preferred when practical.

The protocol must not require hidden chain-of-thought transfer, private reasoning logs, or permanent review manifests.

**Acceptance evidence:** Qualification scenarios distinguish confirmation-biased review from independent reconstruction/falsification, reject verification-before-final-regression ordering, and reject mandatory duplicate Review+Verification for trivial work.

### Obligation 7 — Add milestone stabilization / architecture-GC guidance

**Concern / rationale:** Active simplification currently depends mainly on explicit complexity triggers during implementation. Some entropy is only visible after multiple individually acceptable changes accumulate.

**Required end state:** Workflow/convergence doctrine must recognize bounded stabilization passes at natural convergence boundaries. The pass is not mandatory after every change and not a new approval role. It runs only after ordinary implementation review has otherwise passed, remains non-mutating itself, and inspects accumulated Tier-2 machinery for justified simplification.

If stabilization identifies required change, the minimum coherent change routes back through Software Design when a workplan/architecture decision is required, then Software Implementation, final accepted-contract reconciliation, affected regression/integration, and ordinary review. Stabilization cannot directly bless unreviewed refactoring.

**Acceptance evidence:** Counterfactual tests reject all three failures: never performing stabilization despite material accumulated entropy, forcing whole-repository refactoring after trivial changes, and directly editing/accepting production code inside the stabilization review stage.

### Obligation 8 — Add one semantic maintenance-audit specialist

**Concern / rationale:** `repository-hygiene` intentionally cannot perform semantic product refactoring, while ordinary implementation/review is task-scoped. A repository-level semantic entropy audit has independent methodological value.

**Required end state:** Add one optional specialist, tentatively `software-maintenance-audit`, with scope:

- inspect long-lived repositories for architectural entropy and maintainability deterioration;
- combine semantic inspection with longitudinal evidence such as churn, temporal change coupling, complexity, duplication, dependency centrality/cycles, recurring defect families, public/configuration growth, mutation/test weakness, and documentation difficulty;
- identify high-risk hotspots and simplification opportunities;
- emit findings, evidence, and routing only;
- state explicitly when relevant VCS/history evidence is unavailable and downgrade trend claims accordingly;
- never define Frozen architecture, accept a new implementation contract, become an approval authority, or autonomously perform broad unrelated refactors solely because a metric is high.

Tier-2 findings may route directly to ordinary Implementation only when existing task/architecture authority is already sufficient for a local repair. When substantial maintenance requires a new/revised workplan, or when Frozen architecture is implicated, route to Software Design first.

The specialist should prefer risk concentration rather than raw complexity, conceptually:

```text
maintenance risk ~ change frequency x structural complexity x test weakness x architectural centrality
```

No exact formula is normative.

**Acceptance evidence:** Skill/package validation and behavioral scenarios prove that the specialist finds semantic entropy without inventing metric thresholds, fabricating longitudinal claims from a static snapshot, bypassing Design authority, or turning findings into automatic redesign.

### Obligation 9 — Strengthen workplan/release closeout triggers for documentation and repository hygiene

**Concern / rationale:** The repository currently demonstrates lifecycle residue: Protocol 5.14 and 5.15 workplans remain under `workplans/active/` despite the corresponding protocol revisions having been implemented. This shows that optional closeout capability exists but does not reliably execute.

**Required end state:** Workflow, repository-hygiene, and documentation routing should make milestone closeout observable and routine when a substantial workplan or release is genuinely complete:

- reconcile/close/archive completed workplans according to repository policy;
- reconcile affected current documentation when conceptual structure changed;
- inspect task-owned residue and generated artifacts;
- preserve all existing safety rules against destructive cleanup.

Do not automatically delete branches or files. High-risk cleanup authorization remains unchanged.

**Acceptance evidence:** Protocol repository cleanup during Protocol 5.16 implementation must reconcile the stale active Protocol 5.14/5.15 workplan state if their own authority confirms completion, otherwise record the exact unresolved lifecycle reason they remain active.

### Obligation 10 — Introduce behavioral protocol qualification for anti-entropy decisions

**Concern / rationale:** Current protocol tests include many phrase-presence checks. These are useful structural regressions but cannot establish actual model/harness compliance.

**Required end state:** Preserve static tests, but add bounded behavioral qualification scenarios where success requires the agent to apply protocol semantics rather than repeat keywords.

Include representative scenarios such as:

1. two synchronized representations cause a defect; the correct response removes/consolidates authority rather than adds synchronization validation;
2. a third fallback accumulates around broken ownership; the correct response challenges ownership rather than adds fallback #4;
3. high line coverage with weak assertions; the correct response identifies oracle weakness and routes to mutation/counterfactual strengthening;
4. an objective dependency rule is repeatedly violated; the correct response recommends an executable architecture fitness check rather than repeated manual review;
5. high-complexity but stable untouched code versus moderate-complexity high-churn hotspot; the audit prioritizes the latter without claiming the former is good;
6. a trivial local change does not trigger repository-wide health audit or stabilization bureaucracy;
7. a stateful/restart defect warrants bounded failure injection at the semantic boundary rather than resource-exhaustive chaos or no failure-path evidence;
8. a health audit without VCS history reports static risks but does not fabricate churn/change-coupling trends.

Static tests must not claim these scenarios were behaviorally qualified unless actually run against the named harness/model configuration.

### Obligation 11 — Add changed-code / affected-surface quality ratchet guidance

**Concern / rationale:** Whole-repository arbitrary thresholds are poor fits for mature codebases with existing debt, but agents need a practical monotonic-improvement rule.

**Required end state:** Testing/workflow doctrine should support changed-code or affected-surface ratchets when the project has suitable tools:

- adequate behavioral protection for new/modified important behavior;
- no new unexplained dependency cycle;
- no new objective architecture violation;
- no new unjustified high-complexity hotspot;
- no unjustified public/configuration expansion;
- no weakened mutation/oracle effectiveness on critical changed behavior where that evidence is available.

These are investigation/acceptance prompts grounded in product/Frozen semantics, not universal numeric gates.

**Acceptance evidence:** Counterfactual tests reject both arbitrary whole-repository thresholds and permission to worsen touched code merely because pre-existing debt exists.

### Obligation 12 — Keep protocol skill entrypoints compact

**Concern / rationale:** Adding every new method directly to `SKILL.md` would itself increase control-plane complexity.

**Required end state:** Keep `software-design` and `software-implementation` skill entrypoints concise. Put detailed long-horizon-maintainability methodology in shared references when necessary and route to it only for material maintainability, stabilization, adversarial verification, or health-audit questions.

Do not duplicate full testing/tool doctrine across lifecycle roles. The human-facing prompt reference may repeat the minimum high-salience stage guardrails necessary for reliable orchestration, but canonical semantic ownership remains in the skills/shared references and prompt text must be reconciled when those owners change.

**Acceptance evidence:** Package/contract tests verify direct reachability, non-duplication, progressive-disclosure routing, and absence of competing prompt-vs-skill authority.

### Obligation 13 — Make the canonical workflow-orchestration prompt reference a first-class portable entrypoint

**Concern / rationale:** User-to-agent stage prompts are a real control surface. Without a canonical parameterized router, users repeatedly hand-edit long prompts, stages blur together, locally installed skills may not activate, and web sessions may proceed without the intended protocol skill.

**Required end state:** Maintain a canonical human-facing entrypoint at:

`source/shared/references/development-workflow-prompts.md`

It must:

- be discoverable from `README.md`, `source/README.md`, and `PORTABILITY.md`;
- provide standalone parameterized `INPUTS` blocks so users define values such as workplan path, target repository, governing authorities, protocol source, and protocol ref once;
- cover Design/Workplan, Implementation, Review & Update, Verification, Stabilization/Architecture-GC, downstream-workplan Alignment, Health Audit, and Closeout;
- make Baseline/change-health intake explicitly discoverable, either as its own optional prompt or an unmistakable triggered preamble to Design, so the Frozen lifecycle does not name a stage that users cannot invoke;
- preserve the semantic distinction and ordering defined above rather than turning every stage into generic code review;
- default protocol resolution to harness-native compatible local skill first, canonical public repository second;
- permit harness-specific selectors such as `@skill` or `/skill` only as examples of native invocation and explicitly forbid treating them as shell commands;
- use an exposed local skill root when the harness provides one even if textual selectors are user-only rather than agent-invokable;
- fall back to `https://github.com/hjin98/software-development-protocol` when local skill resolution fails;
- resolve canonical repository source from `source/roles/...` / `source/specialists/...` plus required references;
- preserve governing protocol-version semantics and refuse to guess a historical Git ref or silently apply latest doctrine;
- report truthful limitation when neither compatible local nor public source can be read;
- remain a router/control surface, not a new source of product or architectural authority.

**Delegated solution space:** Exact variable names, stage numbering, whether Baseline is a standalone prompt or a clearly triggered Design preamble, exact harness examples, and exact repository-version lookup mechanics are delegated provided the authority/version guarantees above hold.

**Acceptance evidence:** Static/counterfactual and bounded live qualification where available must cover at least:

1. compatible local skill present -> use local skill without unnecessary remote fallback;
2. local skill absent/unreadable -> use canonical public source;
3. local skill newer but unable to preserve an older workplan contract -> resolve historical compatible source or report non-closure rather than silently upgrade;
4. selector examples are not executed as shell commands;
5. user-only selector but exposed installed skill root exists -> read/invoke the local skill through supported harness/filesystem capability rather than falsely declaring it absent;
6. neither source readable -> truthful limitation, no pretend skill execution;
7. each stage routes to the correct skill/mode and preserves Review/Verification/Stabilization/Health-Audit distinctions;
8. Baseline/change-health intake is discoverable for tasks where quality-ratchet comparison is material.

### Obligation 14 — Add bounded failure-injection routing for stateful/recovery claims

**Concern / rationale:** Long-term reliability defects often occur only on interruption, restart, stale state, partial persistence, duplicate delivery, or worker/I/O failure. Ordinary happy-path regression can leave these claims weak even when coverage is high.

**Required end state:** Testing/tool/scientific/storage/concurrency doctrine should route failure/recovery claims to bounded fault-injection or equivalent controlled simulation when materially useful. Representative cases may include interrupted checkpoint writes, truncated artifacts, missing/stale cache state, restart at material boundaries, worker/task death, controlled I/O failure, duplicate callback/event delivery, and partial transition state.

Prefer deterministic bounded simulation over actual resource exhaustion or indiscriminate chaos. The real semantic owner of recovery/state transition must still execute; a harness that reimplements the recovery algorithm is not sufficient evidence for the owner claim.

**Acceptance evidence:** Counterfactual tests establish that fault injection is conditional, real-owner/proxy-proof, resource-safe, and selected for genuine recovery/failure claims rather than becoming a universal test stage.

## Implementation authority

### Frozen

- Protocol 5 authority hierarchy and two-role lifecycle.
- Existing final implementation reconciliation + affected regression/integration/project checks remain before independent implementation review readiness.
- Review, Verification, Stabilization, Health Audit, qualification, documentation, and hygiene remain distinct non-authority modes/stages/specialists rather than extra lifecycle roles.
- Verification is risk-triggered and does not become a mandatory duplicate review.
- Stabilization is non-mutating; any resulting product-code change returns through normal Design/Implementation/final acceptance/review.
- Metrics/tools remain evidence rather than product truth.
- No universal simplicity or quality score.
- Independent review/verification remains a Software Design mode.
- One optional semantic maintenance-audit specialist is sufficient for repository-level entropy analysis; do not proliferate tool-specific lifecycle specialists.
- Maintenance audit does not define new Frozen architecture or accepted workplan authority.
- Stabilization and maintenance audit are proportionate modes/stages, not mandatory per-change gates.
- Mutation/differential/metamorphic/failure-injection/architecture-fitness/hotspot tooling is conditional and relation-driven.
- Quality-ratchet semantics apply to touched/affected code but do not impose arbitrary whole-repository thresholds.
- The canonical human-facing workflow prompt reference is part of the protocol control surface but remains subordinate to canonical skill/reference authority.
- Default portable skill resolution is compatible local first, canonical public repository second, with governing protocol-version preservation and truthful non-closure when neither source can be established.

### Delegated

- Exact naming of the new shared maintainability reference, if one is needed.
- Exact maintenance-audit specialist name, provided it is singular and semantically clear.
- Exact metric/analyzer/mutation/coverage/architecture/fault-injection tool examples.
- Exact behavioral scenario harness and fixtures.
- Exact phraseology/file distribution, provided progressive disclosure remains compact and coherent.
- Exact prompt variable names and stage numbering.
- Whether optional Baseline/change-health intake is a standalone prompt or an explicit triggered preamble to Design.
- Exact harness selector syntax and documented installed-skill roots.
- Exact repository-version lookup mechanics, provided no historical ref is guessed and older workplans are not silently upgraded.
- Exact CI integration; no new external-service dependency is required merely to implement the doctrine.

### Reopen only on evidence

Reopen Design only if implementation proves one of these Frozen assumptions wrong:

- long-horizon maintainability cannot be integrated cleanly without another authority-bearing lifecycle role;
- a single maintenance-audit specialist cannot cover the semantic repository-audit problem without incoherent scope;
- behavioral protocol qualification requires a fundamentally different packaging/qualification architecture;
- quality-ratchet semantics conflict materially with existing affected-surface or active-simplicity doctrine;
- the new capability classes materially duplicate existing owners in a way that cannot be consolidated cleanly;
- portable local-first/public-fallback skill resolution cannot preserve version-bound workplan semantics without changing the protocol packaging/version architecture;
- the human-facing prompt reference cannot remain a non-authoritative router without duplicating or overriding canonical doctrine;
- current two-role authority is demonstrably insufficient for adversarial review/verification despite operational context separation.

## Affected surface and task-specific acceptance

Expected affected surfaces include:

- `source/roles/software-design/SKILL.md`
- `source/roles/software-implementation/SKILL.md`
- `source/shared/references/workflow-and-workplans.md`
- `source/shared/references/development-workflow-prompts.md`
- `source/shared/references/testing-and-validation.md`
- `source/shared/references/architecture-and-design.md`
- `source/shared/references/convergence-and-cycle-economy.md`
- `source/shared/references/tool-assisted-engineering.md`
- `source/shared/references/python-engineering.md`
- `source/shared/references/scientific-software.md`
- storage/concurrency references where bounded failure-injection routing materially belongs
- `source/shared/references/documentation-maintenance.md` where milestone reconciliation changes are material
- `source/specialists/repository-hygiene/SKILL.md`
- new maintenance-audit specialist source/package
- build/package indexes and generated `dist/` bundles where the new specialist or canonical references affect packaged output
- `README.md`, `source/README.md`, and `PORTABILITY.md`
- qualification/reference-routing fixtures where portable orchestration behavior is exercised
- protocol contract/routing/counterfactual/live-qualification tests
- active/archive workplan lifecycle state if current authority establishes older protocol workplans are complete.

### Acceptance requirements

1. Existing Protocol 5.15 tests and package checks remain green unless deliberately updated to stronger 5.16 semantics.
2. New tests establish the 5.16 identity and preserve all prior authority/simplicity/tool-routing/language-profile contracts.
3. Existing final assembled acceptance ordering remains explicit: final accepted-contract reconciliation and final affected regression/integration/project checks precede independent implementation Review readiness.
4. Counterfactual tests protect against metric authority, universal mutation/failure-injection requirements, mandatory whole-repository audits, new lifecycle-role proliferation, confirmation-biased review, and duplicate mandatory Review+Verification.
5. Behavioral qualification covers the anti-entropy/failure-history cases listed in Obligation 10.
6. The canonical workflow prompt reference is discoverable and parameterized; stages route to the intended skill/mode and preserve stage semantics.
7. Portable skill-resolution qualification covers compatible local success, local absence/unreadability fallback, older-workplan version preservation, selector-not-shell behavior, exposed installed-skill-root use, and truthful no-source limitation.
8. Baseline/change-health intake is user-discoverable when material without becoming a mandatory per-change gate or persistent ledger.
9. New maintenance-audit package is self-contained, passes standard package validation, and does not fabricate longitudinal claims when history is unavailable.
10. Bounded failure-injection routing is conditional, resource-safe, and proxy-proof for real failure/recovery owner claims.
11. Generated `dist/` artifacts match canonical `source/` for all package surfaces that are generated by repository policy.
12. Existing optional tool routing remains relation-first and no new mandatory multi-tool pipeline appears.
13. Skill entrypoint growth remains controlled; detailed doctrine is progressively disclosed rather than duplicated. Prompt-reference guardrails do not become competing semantic authority.
14. `README.md`, `source/README.md`, and `PORTABILITY.md` describe the canonical workflow prompt entrypoint and local-first/public-fallback semantics consistently.
15. Protocol 5.14/5.15 stale active-workplan state is reconciled or explicitly proven still active.
16. Final repository checks documented by the governing protocol all pass.

Production qualification: unnecessary; this is protocol/control-plane work. Live harness/model qualification remains bounded and named when actually executed.

## Implementation sequence and genuine redesign / simplification triggers

### Stage 1 — Reconcile canonical long-horizon doctrine and workflow orchestration

Reconcile existing architecture, workflow, convergence, testing, versioning, and prompt-routing owners. Correct the lifecycle ordering so final assembled acceptance precedes independent Review. Make Review, Verification, Stabilization, Health Audit, and Closeout semantically distinct. Reconcile the canonical parameterized prompt reference and portable local-first/public-fallback resolver into the protocol without turning it into parallel authority.

Close with static/counterfactual tests for authority, stage ordering/selection, prompt reachability, version-bound skill resolution, metric-as-sensor semantics, quality ratchet, and non-bureaucracy.

### Stage 2 — Test-effectiveness, scientific/failure-path, and architecture-fitness routing

Add mutation/oracle-strength, changed-code coverage, differential/metamorphic testing, bounded fault-injection, architecture-fitness, complexity/hotspot, and longitudinal-maintenance capability classes. Extend Python static tooling and scientific reference guidance while keeping all routes conditional and claim-driven.

Close with relation-first routing tests, failure/recovery counterfactuals, scientific-method scenarios, and language-profile regression.

### Stage 3 — Adversarial Review/Verification and stabilization lifecycle integration

Strengthen Software Design independent Review for fresh-context falsification while preserving existing review readiness. Add separate risk-triggered Verification semantics and non-mutating milestone Stabilization with normal-cycle re-entry for any resulting changes.

Close with counterfactual scenarios for confirmation bias, verification-before-final-acceptance, duplicate mandatory verification, excessive stabilization, direct stabilization mutation, and missed entropy.

### Stage 4 — Maintenance-audit specialist

Implement the single semantic repository-health specialist with conservative routing boundaries, explicit history-evidence limitations, and no automatic authority promotion.

Close with skill/package validation and representative behavioral scenarios including missing-history behavior and routing to Design versus Implementation.

### Stage 5 — Behavioral and portable-routing qualification

Add anti-entropy behavioral scenarios plus prompt/skill-resolution scenarios. Update `PORTABILITY.md` so static protocol tests, reference routing, installed-skill resolution, public-repository fallback, tool routing, and live behavioral protocol compliance remain clearly distinct evidence classes.

Close with whichever live harness/model qualification is actually available; do not claim unexecuted configurations or selectors.

### Stage 6 — Documentation, packaging, and public-entrypoint reconciliation

Reconcile `README.md`, `source/README.md`, prompt reference, `PORTABILITY.md`, version documentation, build/package indexes, and generated distributions. Ensure the new maintenance-audit skill is packaged correctly and that the human-facing prompt entrypoint is discoverable without duplicating it gratuitously across every skill bundle unless the build/distribution architecture independently requires that.

Close with package validation, distribution equivalence checks, and prompt/source discoverability checks.

### Stage 7 — Lifecycle closeout and repository reconciliation

Inspect Protocol 5.14/5.15 active workplans and archive/close them only if their accepted state proves completion. Reconcile remaining documentation/indexes/generated artifacts and run the full protocol repository acceptance workflow.

### Simplification triggers

Before adding new durable protocol machinery, stop and simplify if implementation begins producing:

- multiple new shared references covering overlapping maintainability concepts;
- separate specialists for mutation, architecture, complexity, verification, stabilization, or prompt routing;
- a quality-score framework or permanent metric ledger;
- duplicated lifecycle semantics across Design and Implementation entrypoints;
- per-harness copies of the full workflow prompts or protocol doctrine;
- a new resolver service/wrapper when simple harness-native discovery plus public source fallback is sufficient;
- a mandatory fixed multi-stage pipeline for trivial changes;
- a persistent architecture manifest created solely to satisfy this workplan;
- repeated lexical tests that do not increase behavioral confidence;
- new wrappers/checkers whose only purpose is proving other protocol checkers ran.

### Genuine Design-reopen triggers

Reopen only the affected design surface if:

- implementing meaningful behavioral qualification requires changing the current skill packaging/qualification architecture;
- the maintenance-audit specialist cannot remain non-authoritative without losing its purpose;
- quality-ratchet semantics contradict an existing Tier-1/Frozen doctrine rather than merely requiring wording reconciliation;
- a new capability class cannot be cleanly expressed under relation-first tool routing;
- portable skill resolution cannot preserve older workplan semantics without a new version-distribution architecture;
- the prompt entrypoint cannot remain a thin orchestration control surface without conflicting with canonical skill/reference authority;
- current two-role authority is demonstrably insufficient for adversarial review/verification despite operational context separation.

## Expected end state

Protocol 5.16 should preserve the compact two-role system while making long-term agentic development materially more self-correcting and more reliably activated across harnesses:

```text
correct patches
    + strong oracles
    + executable architecture constraints
    + adversarial review / risk-triggered verification
    + quality ratchets
    + bounded failure-path evidence
    + longitudinal health sensing
    + milestone simplification
    + portable stage/skill routing
    + disciplined closeout
    = durable codebase coherence
```

The intended result is not a larger mandatory process. It is an earlier-warning, more falsifiable, more portable, and more autonomous control loop that helps agents preserve a coherent system over many development cycles instead of merely producing locally correct patches.

## Independent Review & Update — Protocol 5.16 implementation blockers

Independent Software Design review of implementation commit `642d9299d94690cd53d7c0d8db6da073c48221d0` returns **NO-PASS**. The Frozen Protocol 5.16 architecture remains valid; the findings below are bounded implementation nonconformances and do not authorize redesign.

### R1 — Make the orchestration prompt contract-complete at the actual copied-stage boundary

**Problem / violated authority:** Obligation 13 and acceptance requirements 6–8 require the canonical `source/shared/references/development-workflow-prompts.md` to make Baseline/change-health intake user-discoverable, preserve compatible-local-first/public-fallback/version-coherent resolution, use an exposed installed-skill root when selectors are user-only, report truthful non-closure when neither compatible source is readable, and keep Health Audit routing subordinate to existing Design/Implementation authority.

The current implementation violates that contract in four connected ways:

1. the visible prompt lifecycle starts at Design and the Design block has no Baseline/change-health prompt or unmistakable triggered preamble, while `README.md` and `source/README.md` claim the prompt provides an optional Baseline/Change-Health Intake entrypoint;
2. `tests/test_protocol_516_orchestration.py` checks Baseline wording in `workflow-and-workplans.md` instead of asserting Baseline discoverability in the actual user-facing prompt, so the oracle can remain green while the accepted prompt contract is broken;
3. individual stage blocks are documented as self-contained/copyable but do not independently preserve the exposed-installed-skill-root case and terminal `neither compatible local nor public source is readable -> truthful non-closure` behavior required by the workplan; and
4. the Health Audit block routes a Tier-2 simplification candidate to a “bounded workplan and software-implementation” without preserving the accepted distinction that direct Implementation is valid only for a local Tier-2 repair under already-sufficient authority, while substantial maintenance needing a new/revised workplan must route through Software Design first.

**Required end state / repair instructions:**

- Add either a standalone optional **Baseline / Change-Health Intake** prompt or an unmistakable triggered Baseline preamble inside Design. It must be visible in the human-facing lifecycle and usable for substantial/structurally risky work without becoming a mandatory per-change gate or persistent metric ledger.
- Keep each stage genuinely standalone. At the copied-stage boundary, resolve the required skill through: harness-native selector **or exposed governing-version-compatible installed-skill root** -> canonical public `source/` fallback -> truthful non-closure if neither compatible source is readable. Preserve selector-not-shell semantics and prohibit silent protocol-version upgrades. Do not add a resolver service, wrapper, new specialist, or per-harness doctrine copy.
- Correct Health Audit routing: local Tier-2 repair under existing sufficient authority -> `software-implementation`; substantial maintenance/new or revised workplan -> `software-design` first; Frozen-architecture concern -> `software-design`.
- Rewrite `tests/test_protocol_516_orchestration.py` to exercise the actual prompt/stage blocks rather than proxy wording in another reference. It must fail when Baseline is absent, an exposed installed-skill root is ignored, terminal no-source handling disappears, or Health Audit bypasses Design for a new/revised workplan.
- Extend `qualification/long-horizon/SCENARIOS.md` with Baseline/change-health discoverability/conditionality. Reconcile `README.md`, `source/README.md`, and `PORTABILITY.md` only as needed so their claims match the actual prompt surface; include optional Baseline/change-health intake in the workflow-stage description where appropriate.

**Acceptance:** the prompt itself satisfies all Obligation 13 portable-resolution cases and Baseline discoverability; stage-block tests protect those semantics counterfactually; no new lifecycle authority or resolver machinery is introduced; all prior Review/Verification/Stabilization/Health-Audit distinctions and version binding remain intact.

### R2 — Remove exact Python checker identity from the acceptance oracle

**Problem / violated authority:** `tests/test_protocol_516_long_horizon_quality.py::test_python_static_correctness_has_first_class_route` currently requires the literal tool names `ruff`, `pyright`, and `mypy`. Obligation 4 explicitly defines those as representative examples, keeps tool identity delegated, and requires language-profile tests to verify the route **without requiring any exact vendor/tool**. The Python profile prose is acceptable; the test oracle is the nonconforming surface.

**Required end state / repair instructions:**

- Replace exact checker-name assertions with semantic assertions that material Python work uses the project's configured fast lint/type/static analysis capabilities when they provide high-information evidence; that such tools are evidence rather than product truth; and that the protocol does not introduce a second checker/type/schema system solely for symmetry.
- Keep representative tool names in prose if useful, but do not make their identities acceptance requirements.
- Prefer a counterfactual test showing that replacing representative checker names with equivalent examples does not fail the protocol contract while removing the capability route does fail it.

**Acceptance:** the executable test contract protects capability semantics and project configuration while allowing equivalent vendor/tool substitutions; no exact Python checker identity becomes Frozen or quasi-Frozen.

### Rework scope and closure

Expected repair surface is bounded to this active workplan/review record, `source/shared/references/development-workflow-prompts.md`, `tests/test_protocol_516_orchestration.py`, `tests/test_protocol_516_long_horizon_quality.py`, `qualification/long-horizon/SCENARIOS.md`, and `README.md` / `source/README.md` / `PORTABILITY.md` only where needed for consistency. Regenerate `dist/` only for canonical source surfaces that repository packaging actually includes and that changed.

Do not introduce a new role, new specialist, resolver service, per-harness protocol copy, compatibility wrapper, or new testing framework to repair these findings. Prefer correcting the existing prompt and oracle surfaces.

Re-run the complete repository acceptance workflow:

```bash
python -m pip install -r source/requirements-validation.txt
python -m unittest discover -s tests -v
python source/build_skills.py --output /tmp/protocol-dist
python source/validate_packages.py --dist /tmp/protocol-dist
python source/check_dist.py --expected /tmp/protocol-dist --committed dist
git diff --check
```

Return the assembled repaired candidate for fresh Software Design Review & Update. The Protocol 5.16 workplan remains active until that review passes.

### Design verdict

**NO-PASS — bounded implementation repair required; Frozen architecture unchanged.**

## Final Independent Review & Update — Closure

Independent Software Design re-review of repaired implementation commit `c567a11866e4ea55ebf78d0b9fa0df846566b60c` returns **PASS**.

- **R1 closed:** the canonical human-facing prompt now exposes conditional Baseline / Change-Health Intake, every copied stage preserves governing-version-compatible harness selector or exposed installed-skill-root resolution before canonical public-source fallback and truthful non-closure, and Health Audit routes substantial maintenance needing a new/revised implementation contract through Software Design first.
- **R2 closed:** Python fast static-correctness acceptance is capability-semantic and vendor-neutral; representative checker names remain examples rather than acceptance identities.
- **Regression/packaging closed:** the reviewed candidate passed the repository regression suite, canonical skill-package build, independent package validation, committed distribution parity, and whitespace validation.
- **Architecture unchanged:** no review evidence invalidated the Protocol 5 hierarchy, two-role lifecycle, non-authoritative quality-sensor model, risk-triggered Verification, non-mutating Stabilization, or singular maintenance-audit specialist architecture.
- **Qualification boundary preserved:** static/counterfactual/package evidence is accepted for this control-plane revision; no unexecuted live harness/model configuration is claimed as qualified.

**Final Design verdict: PASS — Protocol 5.16 implementation accepted; this workplan is completed and archived.**
