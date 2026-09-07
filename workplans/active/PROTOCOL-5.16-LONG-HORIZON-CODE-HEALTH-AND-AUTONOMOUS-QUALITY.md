---
kind: implementation-workplan
workplan_id: PROTOCOL-5.16-LONG-HORIZON-CODE-HEALTH-AND-AUTONOMOUS-QUALITY
protocol_version: 5.15.0
target_protocol_version: 5.16.0
status: active
base_commit: be3a461f98c2e958b110c7c8591612fc14eef073
---

# Protocol 5.16 Long-Horizon Code Health and Autonomous Quality Workplan

## Objective / problem invariants / non-goals

### Original problem

Protocol 5.15 has strong doctrine for product truth, Frozen architecture, delegated solution space, active simplicity, affected-surface validation, proxy-proof acceptance, convergence, and language-native engineering. It is already effective at preventing obvious patch-on-patch preservation of accidental implementation machinery.

The remaining long-horizon failure mode is different: a repository can still degrade gradually across many locally defensible changes before structural complexity becomes obvious enough to trigger active simplification. Current protocol control is therefore stronger at reasoning about already-visible complexity than at observing early longitudinal deterioration, independently falsifying apparently correct implementations, and scheduling maintenance before a crisis.

Protocol 5.16 must strengthen the development system as a closed-loop engineering process:

```text
product truth
    -> design / implementation
    -> executable evidence
    -> adversarial falsification
    -> structural and test-effectiveness signals
    -> longitudinal health observations
    -> simplification / redesign trigger
    -> product truth
```

The protocol must improve early detection of architectural entropy, weak test oracles, change-risk concentration, lifecycle residue, and slowly growing maintenance burden without replacing engineering judgment with metric thresholds or adding bureaucratic approval machinery.

### Product invariants

1. **Preserve Protocol 5 authority.** Tier 1A product/problem truth, Tier 1B cycle-scoped Frozen architecture, Tier 2 delegated solution machinery, and Tier 3 development economy remain unchanged.
2. **Preserve the two authority-bearing lifecycle roles.** `software-design -> software-implementation` remains the complete normative lifecycle. New verification, stabilization, health-audit, documentation, and hygiene activities are modes/stages/specialists, not new approval authorities.
3. **Simplicity remains semantic, not numeric.** No universal CRAP, complexity, coverage, mutation-score, line-count, API-count, or similar threshold may define product correctness or architectural fitness by itself.
4. **Metrics are sensors, not product truth.** Complexity, churn, dependency, coverage, mutation, duplication, hotspot, public-surface, and similar observations may trigger investigation or prioritization but do not automatically require redesign or acceptance failure unless project/task authority explicitly elevates a threshold.
5. **Use quality ratchets rather than arbitrary repository-wide cleanup gates.** Existing debt does not excuse introducing new debt. A materially touched subsystem should ordinarily become no harder to reason about unless added complexity is required by Tier-1/Frozen requirements.
6. **Strengthen oracle quality.** High coverage or green tests are insufficient when semantically wrong implementations can survive. Mutation, differential, metamorphic, property, counterfactual, and real-owner testing should be used when they materially strengthen a claim.
7. **Independent verification should be genuinely adversarial.** Review should attempt to falsify the implementation, not merely confirm the implementer's explanation. Operational separation of verifier context from implementation rationale is preferred when practical.
8. **Architecture fitness should become executable where the rule is objective.** Dependency direction, forbidden coupling, acyclicity, ownership boundaries, or equivalent structural invariants should be encoded as executable checks when doing so is cheap, stable, and semantically justified.
9. **Longitudinal maintenance is periodic and evidence-driven.** Repository-level health audits inspect trends such as churn x complexity x test weakness x architectural centrality, recurring defect families, dependency drift, duplicated concepts, public/configuration growth, and stale compatibility paths without turning every local change into a whole-repository audit.
10. **Scientific correctness remains primary.** Numerical/scientific invariants, trusted reference implementations, justified tolerances, differential/metamorphic relations, and reproducibility remain authoritative over test metrics or optimization goals.
11. **Maintenance findings do not mutate authority.** A health audit may identify risks and simplification opportunities, but ordinary Tier-2 repairs route to Implementation and Frozen-architecture problems route to Design.
12. **Protocol self-qualification must test behavior, not only wording.** Static phrase/structure tests remain useful regression guards, but real protocol-confidence claims should include bounded behavioral scenarios that distinguish good engineering decisions from attractive but wrong ones.
13. **Repository lifecycle state should converge.** Completed/superseded workplans and post-stage residue must not remain indefinitely active merely because cleanup is optional; closeout triggers should make stale lifecycle state observable and routinely correctable.

### Non-goals

- Do not replace Protocol 5.15's philosophy or authority model.
- Do not create a mandatory third approval role for testing, QA, verification, or maintenance.
- Do not introduce a universal quality score, complexity ledger, deletion quota, refactoring quota, or permanent metric bureaucracy.
- Do not require mutation testing, fuzzing, CodeQL, Semgrep, Serena, Hypothesis, coverage, architecture linting, or any other tool on every task.
- Do not require whole-repository health audits after ordinary local changes.
- Do not turn maintainability tools into product truth or let agents optimize metrics at the expense of architecture.
- Do not introduce one specialist per tool category.
- Do not mandate one Python linter/type checker, one C++ analyzer, one mutation engine, one coverage implementation, one architecture-test library, or one hotspot-analysis product.
- Do not retroactively reinterpret older workplans under Protocol 5.16.

## Frozen high-level architecture and engineering envelope

### Frozen architecture

Protocol 5.16 keeps the existing lifecycle and adds bounded quality-feedback modes around it:

```text
baseline / health intake when material
        -> Software Design
        -> Software Implementation + stage-local validation
        -> adversarial independent verification when warranted
        -> stabilization / simplification at milestone boundaries when warranted
        -> final regression / integration
        -> production qualification when independently required
        -> documentation + repository closeout when affected
        -> periodic semantic health audit
             -> Implementation for Tier-2 repair
             -> Design for Frozen-architecture reconsideration
```

These are proportionate activities, not mandatory fixed gate counts. Small/local changes may still use the compact Protocol 5 workflow.

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

### Adversarial verification model

Independent review remains a Software Design mode. For substantial/high-risk work, strengthen its operational independence:

- reconstruct the product/Frozen contract from supplied authority and actual repository state;
- inspect the final candidate before relying on the implementer's rationale;
- attempt to falsify important claims through counterexamples, boundary cases, mutation-like perturbations, alternative state transitions, real-owner execution, affected-consumer inspection, numerical/metamorphic relations, or structural violations;
- prefer a fresh context/model instance when practical so the verifier is not anchored by the implementer's full reasoning trajectory;
- only after independent reconstruction, consult implementation rationale when it resolves a real ambiguity.

This is a verification method, not a third authority role.

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

Simplify Tier 2 where justified. Route any required Frozen-architecture change back to Software Design.

## Implementation obligations and delegated solution space

### Obligation 1 — Extend testing doctrine with test-effectiveness routing

**Concern / rationale:** Current testing doctrine correctly rejects green-test complacency but lacks a positive route for mutation-based oracle-strength analysis.

**Required end state:** `testing-and-validation.md` and tool-routing doctrine must explicitly recognize test-effectiveness/oracle-strength questions as a capability class. Mutation testing must remain conditional and non-authoritative.

**Delegated solution space:** Exact wording, tool examples, and placement may vary. Python/C++ examples may name representative tools, but no tool identity is Frozen.

**Acceptance evidence:** Static protocol tests plus behavioral scenarios must demonstrate that mutation testing is neither universally mandatory nor ignored when an important weak-oracle question materially warrants it.

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

### Obligation 6 — Make independent review explicitly falsification-oriented

**Concern / rationale:** Independent review is already owned by Software Design, but operational independence and anti-anchoring behavior are under-specified.

**Required end state:** `software-design`, workflow, and testing references should make clear that substantial/high-risk independent review attempts to falsify the candidate, reconstructs the contract independently, and should prefer fresh-context verification when practical.

The protocol must not require hidden chain-of-thought transfer, private reasoning logs, or permanent review manifests.

**Acceptance evidence:** Qualification scenarios distinguish:

- confirmation-biased review that repeats the implementation explanation; and
- independent reconstruction plus targeted falsification.

### Obligation 7 — Add milestone stabilization / architecture-GC guidance

**Concern / rationale:** Active simplification currently depends mainly on explicit complexity triggers during implementation. Some entropy is only visible after multiple individually acceptable changes accumulate.

**Required end state:** Workflow/convergence doctrine must recognize bounded stabilization passes at natural convergence boundaries. The pass is not mandatory after every change and not a new approval role.

It should inspect accumulated Tier-2 machinery and simplify where doing so materially reduces total system complexity while preserving product/Frozen requirements.

**Acceptance evidence:** Counterfactual tests reject both extremes: never performing stabilization despite material accumulated entropy, and forcing whole-repository refactoring after trivial changes.

### Obligation 8 — Add one semantic maintenance-audit specialist

**Concern / rationale:** `repository-hygiene` intentionally cannot perform semantic product refactoring, while ordinary implementation/review is task-scoped. A repository-level semantic entropy audit has independent methodological value.

**Required end state:** Add one optional specialist, tentatively `software-maintenance-audit`, with scope:

- inspect long-lived repositories for architectural entropy and maintainability deterioration;
- combine semantic inspection with longitudinal evidence such as churn, temporal change coupling, complexity, duplication, dependency centrality/cycles, recurring defect families, public/configuration growth, mutation/test weakness, and documentation difficulty;
- identify high-risk hotspots and simplification opportunities;
- emit findings and routing only;
- route Tier-2 repair to Implementation and Frozen-architecture problems to Design;
- never become an approval authority or autonomously perform broad unrelated refactors solely because a metric is high.

The specialist should prefer risk concentration rather than raw complexity, conceptually:

```text
maintenance risk ~ change frequency x structural complexity x test weakness x architectural centrality
```

No exact formula is normative.

**Acceptance evidence:** Skill/package validation and behavioral scenarios prove that the specialist finds semantic entropy without inventing metric thresholds or turning findings into automatic redesign.

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
6. a trivial local change does not trigger repository-wide health audit or stabilization bureaucracy.

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

### Obligation 12 — Keep protocol entrypoints compact

**Concern / rationale:** Adding every new method directly to `SKILL.md` would itself increase control-plane complexity.

**Required end state:** Keep `software-design` and `software-implementation` entrypoints concise. Put detailed long-horizon-maintainability methodology in a shared reference when necessary and route to it only for material maintainability, stabilization, adversarial verification, or health-audit questions.

Do not duplicate full testing/tool doctrine across lifecycle roles.

**Acceptance evidence:** Package/contract tests verify direct reachability, non-duplication, and progressive-disclosure routing.

## Implementation authority

### Frozen

- Protocol 5 authority hierarchy and two-role lifecycle.
- Metrics/tools remain evidence rather than product truth.
- No universal simplicity or quality score.
- Independent review remains a Software Design mode.
- One optional semantic maintenance-audit specialist is sufficient for repository-level entropy analysis; do not proliferate tool-specific lifecycle specialists.
- Stabilization and maintenance audit are proportionate modes/stages, not mandatory per-change gates.
- Mutation/differential/metamorphic/architecture-fitness/hotspot tooling is conditional and relation-driven.
- Quality-ratchet semantics apply to touched/affected code but do not impose arbitrary whole-repository thresholds.

### Delegated

- Exact naming of the new shared maintainability reference, if one is needed.
- Exact maintenance-audit specialist name, provided it is singular and semantically clear.
- Exact metric/analyzer/mutation/coverage/architecture-tool examples.
- Exact behavioral scenario harness and fixtures.
- Exact phraseology and file distribution, provided progressive disclosure remains compact and coherent.
- Exact CI integration; no new external-service dependency is required merely to implement the doctrine.

### Reopen only on evidence

Reopen Design only if implementation proves one of these Frozen assumptions wrong:

- long-horizon maintainability cannot be integrated cleanly without another authority-bearing lifecycle role;
- a single maintenance-audit specialist cannot cover the semantic repository-audit problem without incoherent scope;
- behavioral protocol qualification requires a fundamentally different packaging/qualification architecture;
- quality-ratchet semantics conflict materially with existing affected-surface or active-simplicity doctrine;
- the new capability classes materially duplicate existing owners in a way that cannot be consolidated cleanly.

## Affected surface and task-specific acceptance

Expected affected surfaces include:

- `source/roles/software-design/SKILL.md`
- `source/roles/software-implementation/SKILL.md`
- `source/shared/references/workflow-and-workplans.md`
- `source/shared/references/testing-and-validation.md`
- `source/shared/references/architecture-and-design.md`
- `source/shared/references/convergence-and-cycle-economy.md`
- `source/shared/references/tool-assisted-engineering.md`
- `source/shared/references/python-engineering.md`
- `source/shared/references/scientific-software.md`
- `source/shared/references/documentation-maintenance.md` where milestone reconciliation changes are material
- `source/specialists/repository-hygiene/SKILL.md`
- new maintenance-audit specialist source/package
- build/package indexes and generated `dist/` bundles
- `README.md`, `source/README.md`, `PORTABILITY.md`, and qualification scenarios where public protocol semantics change
- protocol contract/routing/counterfactual/live-qualification tests
- active/archive workplan lifecycle state if current authority establishes older protocol workplans are complete.

### Acceptance requirements

1. Existing Protocol 5.15 tests and package checks remain green unless deliberately updated to stronger 5.16 semantics.
2. New tests establish the 5.16 identity and preserve all prior authority/simplicity/tool-routing/language-profile contracts.
3. Counterfactual tests protect against metric authority, universal mutation requirements, mandatory whole-repository audits, new lifecycle-role proliferation, and confirmation-biased review.
4. Behavioral qualification scenarios cover at least the six anti-entropy cases listed above.
5. New maintenance-audit package is self-contained and passes standard package validation.
6. Generated `dist/` artifacts match canonical `source/`.
7. Existing optional tool routing remains relation-first and no new mandatory multi-tool pipeline appears.
8. Entry-point growth remains controlled; detailed doctrine is progressively disclosed rather than duplicated.
9. Protocol 5.14/5.15 stale active-workplan state is reconciled or explicitly proven still active.
10. Final repository checks documented by the current protocol all pass.

Production qualification: unnecessary; this is protocol/control-plane work. Live harness/model qualification remains bounded and named when actually executed.

## Implementation sequence and genuine redesign / simplification triggers

### Stage 1 — Canonical long-horizon maintainability doctrine

Reconcile existing architecture, workflow, convergence, testing, and tool owners. Add only the minimum new shared owner needed for long-horizon maintainability/stabilization/adversarial-verification semantics. Avoid duplicating existing active-simplicity doctrine.

Close with protocol static/counterfactual tests for authority, metric-as-sensor semantics, quality ratchet, and non-bureaucracy.

### Stage 2 — Test-effectiveness and architecture-fitness capability routing

Add mutation/oracle-strength, changed-code coverage, architecture-fitness, complexity/hotspot, and longitudinal-maintenance capability classes. Extend Python static tooling and scientific differential/metamorphic guidance.

Close with relation-first routing tests and language-profile regression.

### Stage 3 — Adversarial verification and stabilization lifecycle integration

Strengthen Software Design independent review and workflow guidance for fresh-context falsification and milestone stabilization without creating new authority roles or mandatory gates.

Close with counterfactual scenarios for confirmation bias, excessive stabilization, and missed entropy.

### Stage 4 — Maintenance-audit specialist

Implement the single semantic repository-health specialist with conservative routing boundaries and no automatic authority promotion.

Close with skill/package validation and representative behavioral scenarios.

### Stage 5 — Protocol behavioral qualification

Add anti-entropy behavioral scenarios and update `PORTABILITY.md` so static protocol tests, reference routing, tool routing, and live behavioral protocol compliance remain clearly distinct evidence classes.

Close with whichever live harness/model qualification is actually available; do not claim unexecuted configurations.

### Stage 6 — Lifecycle closeout and repository reconciliation

Inspect Protocol 5.14/5.15 active workplans and archive/close them only if their accepted state proves completion. Reconcile documentation/indexes/generated distributions and run the full protocol repository acceptance workflow.

### Simplification triggers

Before adding new durable protocol machinery, stop and simplify if implementation begins producing:

- multiple new shared references covering overlapping maintainability concepts;
- separate specialists for mutation, architecture, complexity, or verification;
- a quality-score framework or permanent metric ledger;
- duplicated lifecycle semantics across Design and Implementation entrypoints;
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
- current two-role authority is demonstrably insufficient for adversarial verification despite operational context separation.

## Expected end state

Protocol 5.16 should preserve the compact two-role system while making long-term agentic development materially more self-correcting:

```text
correct patches
    + strong oracles
    + executable architecture constraints
    + adversarial verification
    + quality ratchets
    + longitudinal health sensing
    + milestone simplification
    + disciplined closeout
    = durable codebase coherence
```

The intended result is not a larger process. It is an earlier-warning, more falsifiable, more autonomous control loop that helps agents preserve a coherent system over many development cycles instead of merely producing locally correct patches.
