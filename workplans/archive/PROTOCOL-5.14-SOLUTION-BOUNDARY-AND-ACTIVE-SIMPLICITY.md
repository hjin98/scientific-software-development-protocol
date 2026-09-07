---
kind: implementation-workplan
workplan_id: PROTOCOL-5.14-SOLUTION-BOUNDARY-AND-ACTIVE-SIMPLICITY
protocol_version: 5.13.0
target_protocol_version: 5.14.0
status: active
base_commit: a7fd42e37f32cd2ff4f382b2f5e623343c28b3ad
---

# Protocol 5.14 Solution-Boundary and Active-Simplicity Workplan

## Objective and diagnosis

Protocol 5.14 must restore the operational meaning of the existing three-tier doctrine:

```text
product engineering fitness > minimum justified product/system complexity > development economy
```

The hierarchy itself is not being replaced. The defect is that Protocol 5.5-5.13 accumulated control language that can promote a chosen implementation mechanism, a derived implementation consequence, or a solution-created intermediate problem into quasi-Tier-1 authority. Once that happens, later implementation/review tends to preserve and patch the mechanism rather than reconsider whether the mechanism should exist. Complexity can therefore ratchet upward while every local repair appears contract-conformant.

The protocol must distinguish **the problem to be solved** from **the solution used to solve it**.

Tier 1 contains only:

1. **Intrinsic product/problem invariants** — the stakeholder's research, computational, scientific, operational, compatibility, reliability, resource, performance, security, or other real-world demand and governed external contracts that define what the finished product must accomplish; and
2. **Explicitly frozen high-level architecture for the current implementation cycle** — material architecture/ownership/algorithm/data-representation/resource/compatibility decisions deliberately fixed by Software Design so implementation has a bounded search space. These are cycle-scoped design invariants and may be reopened only on evidence.

Everything beneath those classes is Tier 2 by default. Functions, helpers, internal APIs, state machines, caches, wrappers, adapters, retry systems, compatibility/fallback paths, synchronization schemes, intermediate representations, local algorithms not frozen by Design, previous patches, and implementation-created invariants are solution machinery. They do not acquire Tier-1 authority merely through existence, dependency, testing, documentation, review history, previous workplan wording, or previous repair.

A problem that exists only because of a Tier-2 realization is itself a Tier-2 problem. Before adding machinery to solve it, the implementation must be free—and when complexity evidence triggers, required—to ask whether changing or removing the realization makes the intermediate problem disappear.

Protocol 5.12 correctly recognized that repeated instance repair fails to converge, but its family-closure machinery can still canonicalize the existing realization before challenging whether that realization should survive. Protocol 5.14 must preserve bounded family reasoning where correctness genuinely depends on a semantic family while making **solution re-derivation and simplification precede further additive closure when complexity accumulation is itself the evidence**.

This is a backward-compatible strengthening of the established Protocol 5 doctrine and two-role lifecycle, targeting Protocol 5.14.0.

## Protected concerns and non-goals

Preserve all material product-level safeguards that are independent of the defective solution-authority boundary:

- stakeholder outcome and non-adversarial product truth;
- correctness/scientific fidelity, reliability/recovery/security, compatibility where required, resource feasibility, target-scale/hardware effectiveness, maintainability/operability, and material performance;
- `software-design -> software-implementation` as the complete lifecycle;
- explicit `Frozen / Delegated / Reopen only on evidence` authority;
- affected-surface regression, real-boundary integration, repository/project-required checks, truthful unavailable checks, and separate production qualification;
- proxy-proof acceptance and test-double boundaries when the real owner is materially part of the product claim;
- snapshot-complete task-specific handoff semantics;
- evidence reuse, bounded redesign, revision economy, and progressive repository inspection;
- deterministic per-question Serena/Semgrep/Hypothesis/CodeQL routing introduced by Protocol 5.13, without adding a mandatory multi-tool pipeline.

Do **not** introduce a simplicity score, line-count budget, deletion quota, complexity ledger, architecture manifest, new lifecycle role, new specialist, new approval gate, mandatory refactoring report, persistent closure map, or a new shared reference solely for Protocol 5.14. The repair must primarily rewrite, consolidate, and delete existing control-plane semantics.

Do not equate simplicity with fewer lines of code. Necessary specialization remains justified when it is required by Tier-1 product truth or when a canonical abstraction reduces total system complexity across a real class of problems.

## Target doctrine and authority model

### 1. Problem/solution classification is mandatory

Software Design must explicitly classify substantial work before handoff:

- **Problem / product invariants:** what the stakeholder or governed domain actually requires, stated independently of a particular implementation where possible.
- **Frozen high-level architecture:** only the material solution decisions Design deliberately freezes for this implementation cycle.
- **Delegated solution space:** all remaining implementation realization. This remains replaceable, reducible, consolidatable, or deletable while the first two categories remain satisfied.

The workplan must make this boundary recoverable without reconstructing prior conversation or design history.

Do not freeze detailed machinery merely because Design happened to reason about it. A concrete realization may be documented as guidance, expected surface, or an acceptance-relevant consequence without becoming immutable. If a detail is genuinely necessary to the accepted high-level architecture, state the architectural invariant it realizes rather than canonizing incidental code structure.

### 2. Remove accidental upward promotion

Replace the current generic category **required implementation consequence** wherever it acts as independent normative authority.

A downstream consequence may be binding only in one of two senses:

- it is logically necessary to satisfy an existing Tier-1 product invariant or frozen architecture decision; in that case the governing authority is the parent invariant/decision, and an equivalent simpler realization is valid; or
- Design explicitly promotes a solution decision into frozen high-level architecture because implementation must not vary it during the cycle.

Neither a discovered affected site nor a current mechanism's internal dependency becomes Tier 1 by itself.

The phrase **minimum known contract, not a ceiling** must be narrowed accordingly: implementation must incorporate newly discovered affected surfaces and necessary consequences of already-binding product/frozen-architecture semantics, but discovery does not mint new product requirements and does not require preservation of the mechanism that exposed the consequence.

Explicitly state:

> affected-surface expansion expands inspection, implementation impact, and acceptance coverage; it does not by itself expand the product requirement or freeze the current realization.

### 3. Make Tier-2 simplicity an active restoring policy

Minimum justified product/system complexity must operate both prospectively and retrospectively.

For an ordinary clean local defect, direct owning-layer repair remains valid. But when evidence indicates that the current Tier-2 realization has accumulated unnecessary structural complexity, **simplification/re-derivation is mandatory before another additive durable repair is accepted**.

Trigger this restoring policy on structural evidence rather than a numeric revision count. Material examples include:

- repeated defects or patches around the same machinery;
- patches whose principal purpose is repairing consequences of previous patches;
- wrappers, adapters, retries, fallbacks, compatibility paths, or special cases accumulating around one owner;
- duplicated or synchronized authoritative state;
- multiple competing authorities or repeated reconciliation machinery;
- lifecycle/control states whose primary purpose is managing other internal machinery;
- tests dominated by reproducing or compensating for internal orchestration rather than establishing the Tier-1 claim;
- repeated family closure around the same realization without reducing the failure surface;
- a materially simpler realization becoming evident that preserves Tier-1 product truth and frozen high-level architecture.

When triggered, the required reasoning order is:

```text
recover Tier-1 product/problem invariants
-> recover explicitly frozen high-level architecture
-> treat all lower-level machinery as replaceable
-> identify problems created only by the current realization
-> remove / narrow / alter / consolidate / refactor existing machinery where sufficient
-> add new machinery only if a genuinely required capability remains absent
   or a new canonical mechanism replaces broader existing complexity
```

This is not a mechanical mandate to attempt each verb in sequence. It is a normative burden against additive preservation of avoidable machinery.

A new abstraction/mechanism is justified when evidence shows either:

- Tier-1 product truth or frozen architecture requires a capability the existing simplified realization cannot supply cleanly; or
- the mechanism is sufficiently general/prevalent that making it canonical replaces multiple authorities, patches, or special cases and reduces total system complexity.

### 4. Promotion from Tier 2 to frozen architecture is explicit

Implementation history must never silently promote machinery into Tier 1.

Software Design may deliberately promote a solution mechanism into the frozen high-level architecture only when material evidence shows that architectural commitment is justified, for example because the mechanism is broadly prevalent across distinct requirements, provides a canonical owner for a real problem class, and reduces or prevents more complexity than it introduces.

Promotion requires an explicit Design decision in current authority. Dependency, tests, documentation, prior reviews, or repeated repairs are evidence, not promotion mechanisms.

### 5. Preserve bounded architecture stability

The distinction above must not reopen architecture search continuously during implementation.

Once high-level architecture is explicitly frozen, Implementation preserves it. A genuinely simpler solution that would require changing a frozen architectural decision routes to bounded Software Design reconsideration rather than being silently substituted. Reopen only the affected architecture surface on evidence; preserve unrelated decisions and evidence.

Thus Protocol 5.14 must simultaneously prevent two opposite failures:

- **implementation ossification:** detailed solution machinery accidentally treated as invariant; and
- **architecture churn:** implementation repeatedly reopening deliberately frozen high-level design merely because alternatives exist.

## Required source changes

### A. `source/roles/software-design/SKILL.md`

Rewrite the high-salience doctrine, diagnosis, freeze, handoff, and review language so Design:

- distinguishes intrinsic product/problem invariants, cycle-scoped frozen high-level architecture, and delegated solution machinery;
- freezes only the first two categories;
- does not preserve a generic `required implementation consequence` category as independent authority;
- explicitly compares the original problem with the complexity of the current/proposed realization;
- treats a solution-created intermediate problem as evidence to challenge the solution rather than automatically adding another invariant/repair;
- makes active simplification mandatory when structural complexity triggers fire;
- requires independent review findings to identify the Tier-1 or frozen-architecture authority they protect before demanding preservation of a mechanism;
- routes a simpler realization that changes frozen architecture back to Design, but permits equivalent simplification beneath the frozen boundary.

Keep deterministic tool routing intact. Do not add another role-critical reference solely for this doctrine.

### B. `source/roles/software-implementation/SKILL.md`

Make the implementation boundary operational:

- intake the accepted **problem/product invariants** and **frozen high-level architecture** separately from current implementation details;
- treat detailed solution machinery as replaceable unless current authority explicitly freezes it at architecture level;
- redefine local reconciliation broadly enough to allow simpler equivalent realization beneath frozen architecture, including deletion/consolidation of previously expected machinery;
- narrow `minimum known contract, not a ceiling` to consequences/affected surfaces of existing Tier-1 and frozen-architecture authority;
- state that affected-surface growth does not authorize new functionality or freeze the mechanism that caused the impact;
- before another additive repair under a triggered complexity regression, re-derive the Tier-2 solution from the original problem/frozen architecture;
- allow a new canonical mechanism when it demonstrably collapses broader duplicated machinery or supplies a genuinely missing required capability;
- preserve emergency/hotfix exceptions as explicitly temporary, not durable bypasses of the active simplification rule.

### C. `source/shared/references/architecture-and-design.md`

Make this the canonical detailed owner of the problem/solution boundary and active complexity-restoration semantics.

Consolidate current `Minimum justified product complexity`, `Complexity regression and consolidation review`, `Redesign boundary`, and repeated-family architecture guidance so the reference states:

- Tier-1 product truth versus cycle-scoped frozen architecture versus Tier-2 realization;
- solution-created intermediate problems do not gain independent authority;
- current machinery correctness and current machinery necessity are separate questions;
- structural complexity signals trigger mandatory Tier-2 reconsideration before additive durable repair;
- simplification can happen entirely beneath frozen architecture; Design reopening is needed only if a frozen high-level decision must change;
- abstraction/canonicalization is justified by net global simplification or genuinely missing capability, not by hypothetical generality.

Delete duplicated convergence prose when the same rule can be stated once through this model.

### D. `source/shared/references/workflow-and-workplans.md`

Rework workplan authority and handoff semantics:

- replace undifferentiated `required implementation consequences` with parent-authority-preserving obligations whose implementation realization remains replaceable unless explicitly frozen;
- make the workplan distinguish `Problem/product invariants`, `Frozen high-level architecture`, and `Delegated solution space`;
- clarify that task-specific obligations describe required outcomes/constraints/acceptance, not immutable proof steps;
- redefine the handoff closure equation around product invariants + frozen architecture -> obligations + acceptance, without implying every known implementation consequence survives as machinery;
- state explicitly that affected-surface expansion is not requirement expansion;
- preserve snapshot completeness for still-binding product/frozen-architecture semantics and task-specific acceptance boundaries, not for obsolete realization history;
- keep revision economy: implementation misses, additional sites, failed tests, simpler equivalent realization, and ordinary review findings under existing authority do not mint numbered workplan revisions.

### E. `source/shared/references/convergence-and-cycle-economy.md`

Substantially simplify the convergence model so it cannot canonicalize accidental solution structure.

Retain these semantics:

```text
first clean local defect -> direct owning-layer repair
recurring equivalent defect -> stop instance patching and reason at the shared owner/mechanism
complexity-accumulation evidence -> re-derive/simplify Tier-2 realization before further additive closure
post-simplification recurrence or evidence that frozen architecture is wrong -> bounded Design reconsideration
```

A bounded family census/closure basis remains justified when the **Tier-1 correctness claim itself** is finite/exhaustive or when bounded sibling discovery is needed to remove/canonicalize the affected realization safely. It must not be a universal prerequisite for proving that an existing mechanism deserves preservation.

Remove or rewrite rules/tests that require the existing `canonical realization` to be completed merely because it has already been selected. Family closure must remain subordinate to the product/frozen-architecture target and active simplification rule.

Preserve review saturation, non-refusal of explicitly requested review, revision economy, and bounded evidence principles where they still add material value. Consolidate duplicated readiness/closure language rather than adding Protocol 5.14-specific machinery.

### F. `source/shared/templates/implementation_workplan_template.md`

Simplify the template. Required sections should be:

1. **Objective / problem invariants / non-goals**
2. **Frozen high-level architecture and engineering envelope**
3. **Implementation obligations and delegated solution space**
4. **Implementation authority — Frozen / Delegated / Reopen only on evidence**
5. **Affected surface and task-specific acceptance**
6. **Implementation sequence and genuine redesign/simplification triggers**

The template must explicitly ask:

- What is the original stakeholder/research/computational problem independent of the current implementation?
- What high-level architecture is deliberately frozen for this cycle?
- What implementation machinery is intentionally **not** frozen?
- What existing machinery/state/path should be removed, narrowed, or consolidated if the work is a simplification/refactor?
- If net-new machinery is required, what Tier-1/frozen-architecture capability cannot be met cleanly without it, or what broader machinery does it replace?

Delete the generic `Conditional convergence guidance` section and generic `Handoff closure` boilerplate from the template. Their durable semantics should be inherited from the protocol and expressed task-specifically only when material.

### G. README/versioning/distribution surfaces

Update:

- `source/PROTOCOL_VERSION` -> `5.14.0`;
- `source/README.md` and root `README.md` so the theorem/proof-style problem/solution boundary and active simplicity rule are high-salience without becoming a long manual;
- `source/shared/references/protocol-versioning-and-compatibility.md` with Protocol 5.14 as a backward-compatible doctrine/control-plane strengthening that clarifies the existing Protocol 5 hierarchy rather than changing the lifecycle or weakening product requirements;
- generated `dist/` bundles/ZIPs through the canonical build path.

Do not weaken Protocol 5.13 deterministic tool routing or optional-tool semantics while editing entrypoints.

## Test-contract repair

The current executable tests encode some superseded control-plane assumptions and must be refactored rather than preserved verbatim.

### Required semantic scenarios

Consolidate tests around behaviorally meaningful policy scenarios, including at least:

1. **Local bug:** a clean local defect may receive a direct owning-layer repair without architecture reopening or family bureaucracy.
2. **Solution-created problem:** if duplicated state creates a synchronization defect, deleting/consolidating the duplicate is valid and preferred over adding synchronization machinery when Tier-1/frozen architecture permits it.
3. **Affected surface != requirement surface:** discovering more callers/tests/consumers expands validation and implementation impact but does not mint new product capability or freeze the current mechanism.
4. **Equivalent simpler realization:** a workplan-suggested helper/wrapper/state machine may be deleted/replaced when the simpler realization preserves Tier-1 product truth and frozen high-level architecture.
5. **Frozen architecture stability:** Implementation may not silently replace an explicitly frozen high-level architecture decision; a materially simpler alternative that crosses that boundary routes to Design reconsideration.
6. **Active restoring trigger:** repeated patches/wrappers/fallbacks/duplicated state around one mechanism require Tier-2 simplification/re-derivation before another additive durable patch.
7. **Justified abstraction:** a new canonical mechanism is allowed when it replaces multiple authorities/special cases or supplies a genuinely required missing capability and thereby yields the globally simpler sufficient system.
8. **No implicit promotion:** implementation detail does not become invariant because it is tested, documented, depended upon, reviewed, or present in prior workplans.
9. **Finite family remains valid when product truth requires it:** exhaustive/structural family evidence remains available when correctness itself is an all-members claim.
10. **Product safeguards preserved:** product requirements, proxy-proof real-owner acceptance, stage/final affected regression/integration, snapshot-complete current authority, revision economy, and deterministic tool routing remain intact.

### Test-suite simplification

Do not add another large `test_protocol_514_*` oracle family while keeping all superseded 5.12/5.13 policy-oracle duplication.

Refactor/consolidate existing tests where practical:

- remove assertions whose only purpose is preserving the old `required implementation consequence` category;
- rewrite convergence assertions that force family/canonical-realization closure before the active simplification question;
- retain only bounded counterfactual tests that protect durable semantic directions;
- centralize protocol-version assertions so 5.14 does not require scattered edits across unrelated historical tests;
- preserve Protocol 5.13 tool-routing qualification tests unless wording-only adjustments are necessary;
- delete redundant oracle helpers/tests when equivalent durable semantics are covered elsewhere.

The test change should itself exhibit Tier-2 simplification: fewer duplicated policy encodings, not an additional parallel layer.

## Implementation sequence

1. **Doctrine boundary first.** Update architecture/workflow semantics and the workplan template so the invariant boundary is unambiguous before changing role entrypoints.
2. **Role realization.** Rewrite Design and Implementation entrypoints against the canonical boundary, preserving tool routing and acceptance triggers.
3. **Convergence reduction.** Simplify recurrence/family machinery around active Tier-2 restoration; remove obsolete duplicated control language.
4. **Executable contract consolidation.** Refactor tests to encode the new semantics while deleting superseded oracle duplication.
5. **Version/docs/build.** Update 5.14 identity and concise README/version history, regenerate distribution artifacts.
6. **Final assembled acceptance.** Inspect the final diff specifically for net-new control-plane machinery, duplicated doctrine, accidental invariant promotion, and stale 5.13 wording, then run repository acceptance.

Do not create numbered authority-revision files for ordinary implementation/review findings. Keep this canonical workplan current if a genuinely new task semantic or frozen design decision must be reconciled.

## Acceptance

Protocol 5.14 is implementation-complete only when direct source inspection and tests establish all of the following:

- an agent can distinguish original product/problem demand from chosen solution machinery without relying on conversation history;
- explicitly frozen high-level architecture is stable during implementation but lower-level realization remains replaceable;
- no generic implementation-detail category independently acquires Tier-1 authority;
- affected-surface discovery expands acceptance/impact analysis without automatically expanding product requirements;
- structural complexity evidence activates mandatory Tier-2 simplification/re-derivation before another additive durable repair;
- local clean defects remain lightweight;
- bounded family reasoning remains available where it serves product correctness, but cannot override the simplification challenge by treating current machinery as the theorem;
- justified canonical abstraction remains possible when it reduces total complexity or supplies genuinely missing required capability;
- deterministic tool routing, proxy-proof acceptance, stage/final regression/integration, snapshot handoff, bounded redesign, and revision economy remain materially intact;
- the workplan template is simpler and explicitly separates problem invariants, frozen architecture, and delegated solution space;
- the test suite removes/consolidates superseded policy-oracle duplication rather than merely adding a Protocol 5.14 layer;
- generated distribution artifacts match canonical source.

Run the repository-prescribed acceptance commands:

```bash
python -m pip install -r source/requirements-validation.txt
python -m unittest discover -s tests -v
python source/build_skills.py --output /tmp/protocol-dist
python source/validate_packages.py --dist /tmp/protocol-dist
python source/check_dist.py --expected /tmp/protocol-dist --committed dist
git diff --check
```

No production qualification is required; this is a protocol/control-plane change.

## Implementation authority

### Frozen

- Target version: **5.14.0**, governed by Protocol 5.13.0 until release.
- The three-tier ordering remains unchanged.
- Intrinsic product/problem invariants and explicitly frozen high-level architecture are the only normal Tier-1 classes for an implementation cycle.
- Lower-level implementation/solution machinery is Tier 2 by default and cannot gain invariant status implicitly.
- Tier-2 simplicity is an active restoring policy when structural complexity evidence fires.
- Frozen high-level architecture remains stable during implementation unless reopened by Software Design on evidence.
- Existing material product safeguards and Protocol 5.13 deterministic tool routing remain preserved.
- The revision must be reduction-dominant in control-plane design: no new role, gate, score, ledger, manifest, or new shared doctrine reference.

### Delegated

- Exact wording and section placement within existing canonical owners.
- Exact test-file consolidation layout, provided durable scenarios above remain protected and superseded duplication is removed.
- Exact amount of textual reduction; no arbitrary byte/line quota applies.
- Whether particular current convergence paragraphs/tests are rewritten, merged, or deleted, provided their still-valid product-level safeguards remain recoverable.

### Reopen only on evidence

Reopen Design only if implementation demonstrates that:

- the two-class Tier-1 boundary cannot preserve a material existing Protocol 5 product guarantee;
- active simplification conflicts irreconcilably with a genuinely required finite-family correctness property;
- preserving deterministic Protocol 5.13 tool routing requires a material architecture change rather than local wording/test reconciliation; or
- the target change is incompatible enough with historical Protocol 5 workplan semantics that 5.14 cannot honestly remain a backward-compatible minor release.

Do not reopen merely because an existing test asserts superseded wording, because a historical workplan used `required implementation consequence`, or because preserving all existing control-plane machinery would be easier than simplifying it.

## Review finding reconciliation — acceptance evidence must not freeze Tier-2 owners

Independent review of the first 5.14 implementation found one blocking authority leak: proxy-proof acceptance could still promote a replaceable Tier-2 production owner into an effective invariant merely because the workplan or test named that owner/path. This is the same solution-reification defect through the evidence contract rather than through implementation-consequence language.

The governing distinction is now explicit:

- **The acceptance claim is authoritative.** Product/Frozen behavior must be established through the actual production semantic owner of the final accepted realization.
- **Boundary fidelity is authoritative.** Evidence must fail when that final real owner is materially broken; mocks/fakes remain below or outside it.
- **A delegated Tier-2 owner identity is not authoritative merely because acceptance currently names it.** If owner `A` is legitimately replaced by equivalent simpler owner `B` while product/problem invariants and Frozen high-level architecture remain satisfied, Implementation must invalidate/reconcile `A`-specific evidence and establish the same claim through real owner `B`.
- **Exact owner/path identity is binding only when independently justified by Tier 1:** a governed external/product contract requires that identity, or Software Design explicitly freezes the owner/path at high-level architecture. Only then does changing it require Design reconsideration.

Therefore proxy-proof acceptance must never become a hidden third Tier-1 class. A current owner/path may be recorded so tests exercise reality, but the record must state whether exact identity is product/Frozen authority or merely the current realization.

### Required rework

- `source/shared/references/testing-and-validation.md` must become explicit that proxy-proof acceptance binds the claim to the **final real owner**, not to an incidental historical Tier-2 owner. Owner replacement beneath Frozen architecture is local reconciliation; owner-specific evidence is invalidated and rerun/remapped rather than silently reused.
- `source/shared/references/workflow-and-workplans.md` and the workplan template must preserve the claim/boundary and distinguish binding owner identity from a replaceable current owner mapping. They must not place generic acceptance-owner identity into `Frozen` authority.
- Design and Implementation entrypoints must retain the salient real-owner safeguard while making the same distinction operational.
- Existing proxy-proof and 5.14 contract tests must add the directional counterexample `delegated owner A -> simpler owner B -> acceptance remaps to real B`, while preserving rejection of tests that bypass the final real owner.
- Historical Protocol 5.13 tool-routing tests must stop owning the current protocol-version assertion; current-version identity remains centralized in the current protocol contract tests.
- Regenerate and validate all committed distributions after source/test changes.

This finding is **implementation nonconformance under the existing 5.14 design**, not a redesign. Target version remains `5.14.0`; the three-tier authority model, active-simplicity rule, deterministic tool routing, and proxy-proof acceptance purpose remain Frozen.

### Additional acceptance scenario

11. **Acceptance owner replacement:** when a delegated Tier-2 semantic owner `A` is replaced by an equivalent simpler owner `B` without changing product truth or Frozen high-level architecture, the protocol requires proxy-proof acceptance through real owner `B` and invalidation/reconciliation of `A`-specific evidence; it must not require preservation of `A` or a Design reopen solely because an earlier workplan/test named `A`.

Final acceptance additionally requires that no canonical protocol text treats an acceptance-owner mapping as independent Frozen authority unless exact identity is itself a product contract or explicitly Frozen architecture.
