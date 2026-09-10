---
kind: implementation-workplan-amendment
workplan_id: SSDP-6.1-SECOND-REOPENED-PORTABILITY-DOCUMENTATION-AND-RECOVERY-REPAIR-REVISION-1-PACKAGE-CLOSURE
amends_workplan: SSDP-6.1-SECOND-REOPENED-PORTABILITY-DOCUMENTATION-AND-RECOVERY-REPAIR
protocol_version: 6.1.0
status: active
created_date: 2026-09-10
reviewed_date: 2026-09-10
active_serious_challenge: none
---

# SSDP 6.1 Second-Reopen Revision 1 — Package Closure Reconciliation

## Background and terminology

The **Scientific Software Development Protocol (SSDP)** distributes each runtime role/specialist as a self-contained skill bundle. A `SKILL.md` **activation seed** is a reference or template directly linked from the skill entrypoint. The **transitive local-Markdown closure** is the finite set of local Markdown documents reachable from those seeds through ordinary relative Markdown links. A **dangling route** is a local link whose target is absent from the shipped bundle.

This amendment changes only the cycle-scoped D4 packaging decision in the parent second-reopen workplan. It was triggered by executable counterexample evidence; it does not change Protocol 6.1 D1/D2/D3 semantic doctrine, reference-routing semantics, or the public-fallback/documentation requirements in the parent repair.

## 1. Triggering evidence

The first strengthened package-closure regression was run before any repair source was committed. It rejected the existing direct-only bundle model:

- the focused closure test found missing transitive targets such as `scientific-software.md -> numerical-algorithm-design.md` and `workflow-and-workplans.md -> convergence-and-cycle-economy.md`;
- repository package validation reported 68 unresolved local Markdown edges across generated skill bundles;
- the synthetic nested-dangling counterexample itself correctly failed, proving the new oracle was live;
- the failure occurred before Stage-A commit, so no partially repaired source/package state was accepted.

This is material sibling recurrence at one shared packaging owner. Requiring each role entrypoint to duplicate dozens of transitively referenced files merely to force package membership would mix packaging topology into role-level semantic routing and create synchronization debt. The parent workplan explicitly allowed reconsideration if implementation evidence showed the direct-only membership model was not viable; that trigger has fired.

## 2. Superseded parent decisions

The following parent statements are superseded only for package-membership mechanics:

- parent Section R2-1 preference to preserve direct-only package membership;
- parent Section 3 decision 1, “Keep the existing direct `SKILL.md`-route package-membership model”;
- parent Section 3 decision 3 requiring all missing transitive payload solely through added direct writing-standard routes;
- parent Stage-A step 3 insofar as it requires direct entrypoint links merely to force package membership.

The parent acceptance goal remains unchanged: runtime bundles must be self-contained, progressive-disclosure routing must remain meaningful, and unrelated shared references must not be swept into a bundle merely because they exist in the repository.

## 3. Replacement package architecture

Use the minimum bounded graph closure already implied by the shipped Markdown documents:

1. `SKILL.md` direct `references/*.md` and `templates/*.md` links remain the authoritative **activation seeds** and role-routing contract.
2. `source/build_skills.py` SHALL package each seed plus the finite transitive closure of **local Markdown links reachable from that seed** while remaining inside `source/shared/references/` and `source/shared/templates/`.
3. External URI links, same-document fragments, non-Markdown links, and paths escaping the shared packageable roots SHALL NOT expand package membership.
4. A transitive resource is payload needed to make an already-routed document self-contained; its presence SHALL NOT be interpreted as a new mandatory direct activation route from `SKILL.md`.
5. `source/validate_packages.py` SHALL independently verify both:
   - every local Markdown link in every packaged Markdown file resolves inside the bundle; and
   - every packaged reference/template Markdown file is reachable from `SKILL.md` through the packaged local-link graph, preventing unrelated payload from being silently bundled.
6. Existing direct-route validation remains responsible for portable/safe `SKILL.md` activation-seed syntax.

This is bounded transitive closure, not a universal dependency graph, runtime resolver, or Protocol 7 control mechanism.

## 4. Documentation-writing route

Where a role or specialist itself materially instructs the agent to perform human-facing scientific/technical documentation work, a direct `scientific-technical-writing.md` route remains appropriate because it is an activation decision, not merely package transport. Do not add direct routes to every transitive reference solely to populate the bundle.

## 5. Acceptance counterfactuals

The repaired package owner is accepted only if all of these hold:

- a built bundle has zero unresolved local Markdown-to-Markdown routes;
- removing a transitively required target from an otherwise valid bundle makes validation fail;
- adding an unrelated shared Markdown file to the bundle without any route from `SKILL.md` makes validation fail as unreachable payload;
- the synthetic `SKILL.md -> references/a.md -> missing.md` counterexample fails;
- `SKILL.md` direct-route registry tests continue to describe activation seeds rather than being rewritten to claim every transitive payload file is a direct role route;
- all shipped directory and ZIP bundles pass the independent validator and canonical parity checks;
- frozen Protocol 5.16/6.0 profile bytes remain unchanged.

## 6. Disposition

```text
SERIOUS CHALLENGE: NONE
TRIGGERING PACKAGE-CLOSURE EVIDENCE: VALID
PARENT DIRECT-ONLY MEMBERSHIP FREEZE: SUPERSEDED AT D4 PACKAGING OWNER
REPLACEMENT: BOUNDED TRANSITIVE LOCAL-MARKDOWN CLOSURE FROM DIRECT SKILL ACTIVATION SEEDS
D1/D2/D3 SEMANTIC AUTHORITY CHANGE: NONE
IMPLEMENTATION: AUTHORIZED
```
