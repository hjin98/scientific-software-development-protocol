---
kind: protocol-workplan-review
protocol_version: 6.6.0
target_protocol_version: 7.0.0
reviewed_subject: hjin98/scientific-software-development-protocol@d255a9265aeb6aaf2432193b327beb07b9c4740c:workplans/active/SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY-CONSOLIDATED.md
disposition: NO-PASS
active_serious_challenge: none-established
---

# Protocol 7.0 Consolidated Workplan — Review of d255a92

## Basis and independence

This records the independent workplan-level Review delivered in the task before the stakeholder instructed "Repair." The reviewing context authored neither the reviewed subject nor its `88a82b5` repairs. It subsequently authored the proposed repair at that instruction and cannot independently accept that repair. This record preserves the original NO-PASS assessment; it is not evidence that the repair is correct.

The clean checkout matched the exact reviewed subject. Release identities were resolved from `PROTOCOL-RELEASE-STATE.yaml`: accepted Protocol 6.6.0, public source `22f4bdba53795da3a6f13f162529f3a843fc37ae`, recovery `384666764da4c55b282e6b1595ab97e2f86e1dc4`. Canonical `source/` bytes matched that public source. Section 4 is byte-identical between `88a82b5` and `d255a92`; the stakeholder's §4 decisions were accepted inputs. The `88a82b5` NO-PASS record and the §0.1 repair map were treated as claims. The reviewer likely shares a model family with earlier authors and reviewers; that common-mode limit is recorded rather than resolved.

## Serious Challenges

None established against accepted 6.6 or the stakeholder's §4 decisions. The findings concern the proposed realization.

## Implementation-readiness blockers

**B1 — The §8.3 placement cannot reach the §8.2 run, analysis-review and gate-evidence scope (out-of-matrix).** The predicate covers tasks that run pipelines or campaigns, review analyses or reports, or prepare gate evidence. Placement is only in role `SKILL.md` bodies. Under 6.6 the frontmatter description is the selection interface (`history/SEMANTIC_EVOLUTION.md`, 6.6 replacement; `qualification/ssdp66/FINAL-SIMPLIFICATION-EVIDENCE-CORRECTION.md`), and an unselected body is never consumed. No current role description covers running a campaign and reporting, analyzing realized results, or preparing gate evidence. This is §2's motivating case. §11.3's ordinary-entry cases are all D4 code tasks, and "through the installed skill" does not state whether selection is part of the subject. §8.3's "always-loaded" wording is inaccurate for skill bodies. Repair: freeze the pre-activation selection-surface decision, or narrow the claim; qualify ordinary entry for these task classes with selection counted.

**B2 — The PEM basis/HAS repair leaves the 6.6 interval unreconciled and undispositioned.** The bound identities resolve: `2585b73f` is `main`; blob `1561797125622f355f84eb27319f87e8fa4227d9` is identical at `bdd2064c`, `22f4bdba`, `2585b73f` and the subject; the validator passes. But the PEM's own `reconciled_through` and `accepted_base.project_state` remain `23e46543` (6.5) and its coverage basis stops at 6.5. The 45-commit 6.6 interval was not assessed: the 6.6 closeout (`2818ccf`) records no closeout-learning assessment, and `qualification/ssdp66/STAGE-F-G-EVALUATION-AND-QUALIFICATION.md` §9 deferred three candidates to it (a DS-001 application, a possible prose-only entry/mandatory-read discovery, unrecorded SP-002 release episodes). Those and other 6.6 lessons (uncollected hidden oracles, a rubric branch that passed self-adoption, the selection-surface correction) bear on §8.3 and §11. The PEM owner requires bounded historical intake or explicit `REVIEW_REQUIRED` for stale memory; "Coverage remains PARTIAL" does neither. The 6.6 workplan met the same front-matter mismatch with `REVIEW_REQUIRED` plus a reconciliation prerequisite; this subject declared the stale overlay text historical by assertion. Minor: `accepted_pem` names pre-Review candidate commit `bdd2064c` rather than an accepted publication; "88a82b5 PEM" is a stale self-reference.

**B3 — Tension retrieval loses findings across authority revision.** Persistence binds the "exact authority binding" and the search is an "authority-identity search". Counterexample: tension T in issue B is bound to D1@r3; D1 is revised to r4 without changing the challenged claim, possibly declaring a new location; a later task relying on r4 searches r4 and misses applicable T. Nothing requires lineage-identity search or requires the revising author to reconcile tensions against the prior revision; the evidence owner already permits stable logical endpoint identity. The same gap hides a finding bound to D2 whose real target is D1. This is the third related finding on the tension-discovery route (`c50f267` B5, `88a82b5` B1); the convergence owner calls for one re-derived retrieval-key invariant rather than another clause.

## Material gaps

- **G1** Out-of-list classification, custody and checker rules survive falsification, but unnamed-class results have no predeclared decision consequence; an underpowered share can be reported without affecting the pass.
- **G2** When an inaccessible tension home qualifies versus blocks a judgment is undefined, risking both over-blocking offline agents and an ambiguous §11.3 oracle.
- **G3** §6.5's "Fresh tasks reach relevant findings through the §6.4 bounded search" over-claims for persisted findings not bound to authority.
- **G4** §11.3 tests retrieval of a custodian-planted issue but not whether a persisting agent writes a searchable binding.
- **G5** The capability-transfer map covers only the five PEM families. Touched 6.6 capabilities—ordinary-route active protocol material (criterion 4), the frontmatter selection interface, entry-contract version ordering and the local-work exemption—lack a preservation map and qualification route; §11.4 omits observed active protocol bytes and selection measures.

Minor: §6.4 lets O1 declare a finding location for D3 while tensions are defined only against D1/D2. Separately, the 6.6 lifecycle appears to have closed without the closeout-learning assessment; route that to the repository lifecycle/PEM owner.

## Falsification results that did not establish another defect

- §4 is preserved; §4.5 and O1(ii) remain consistent.
- Mechanism-based out-of-list classification excludes relabeled or instantiated listed mechanisms, keeps keys withheld from author and executor, and preserves the custody split.
- The split-location A→B case itself is closed by the identity search.
- PC-001's force is correctly re-anchored to the accepted 6.6 versioning owner; FF-001, SP-002 and SP-001 stage mappings are sound.

## Executed evidence and disposition

- HEAD, source, PEM blob identity and ancestry checks; §4 hash comparison.
- `PYTHONDONTWRITEBYTECODE=1 python3 source/project_engineering_memory.py PROJECT-ENGINEERING-MEMORY.md`: PASS, schema 1, five families, zero notices. It does not check front-matter basis against integration state.
- `PYTHONDONTWRITEBYTECODE=1 python3 source/release_state.py`: PASS, coherent.
- Package acceptance, live qualification and human trials: not executed; future implementation obligations.
- No files were edited during the Review. This durable record was added during the subsequently authorized repair.

**NO-PASS for implementation readiness.** D4 remains unauthorized. Proposed repairs require fresh independent workplan-level Review by a context that authored neither the workplan nor those repairs.
