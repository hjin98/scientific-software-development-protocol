---
kind: abstraction-concretization-change-plan
workplan_id: PROTOCOL-6.3-EVIDENCE-BACKED-PROJECT-ENGINEERING-MEMORY
protocol_version: 6.2.0
target_protocol_version: 6.3.0
status: active
created_date: 2026-09-11
reviewed_date: 2026-09-12
design_closure_status: preserved-from-5de67c6a9509c1ede9104badc3ddae468c988311
implementation_handoff: authorized
implementation_review_state: reopened-after-independent-no-pass
reviewed_candidate_no_pass: 100cbde296de6c1a8db14151f34cfacfebc90eb3
reviewed_candidate_no_pass_2: 3bbbdfa8120646d76336c7b916e6a891c9ed38f2
reviewed_candidate_no_pass_3: 026eecf6ce382c3445ed218aeca80dcf2fb9a426
prior_current_workplan_state: 5de67c6a9509c1ede9104badc3ddae468c988311:workplans/active/PROTOCOL-6.3-EVIDENCE-BACKED-PROJECT-ENGINEERING-MEMORY-WORKPLAN.md
prior_public_bootstrap: dc22f09fd38dbbfeaeb0160152da9b284654f66e
prior_semantic_candidate: 026eecf6ce382c3445ed218aeca80dcf2fb9a426
prior_f3_qualification_commit: 5362f39107aa3f5760f501c02c66e3d25434cac7
prior_f3_qualification: qualification/ssdp6/RESULTS-GPT-5.6-SOL-2026-09-12-PROTOCOL-6.3-F3.md
reopened_stages: B,D,F
stage_g_recovery_gate: blocked-repair-and-fresh-independent-review
active_serious_challenge: none
parent_protocol_62_recovery: b59adc77efe6951912cfd705cc43830c58ca27d0
parent_protocol_62_semantic_candidate: ebbc4591bdfed039512026b8acb3a6749475c1c5
parent_protocol_62_public_bootstrap: 5a062ebc472755607b9dc66d33a5ebbc4b7429aa
parent_protocol_62_mapping_commit: bc76b16fda96be09f38a1b40a2ef877e8309534d
parent_protocol_62_generated_reconciliation: ca622ea2b1c33e70668060cf0cc2fe9138776f7f
branch_point: bf856f742d1744a8ff50f300ee6493fb93e5c9d0
---

# SSDP 6.3 Evidence-Backed Project Engineering Memory - Reopened Implementation Contract

## Current disposition

Protocol 6.3 remains **NO-PASS** and proposed. Accepted-current authority remains Protocol 6.2 recovery `b59adc77efe6951912cfd705cc43830c58ca27d0`. Stage G, recovery mapping, workplan archive, and `main` cutover remain blocked.

The independent assembled-candidate review of semantic candidate `026eecf6ce382c3445ed218aeca80dcf2fb9a426` found seven genuine D4/schema-validation and Stage-F oracle blockers and **no Serious Challenge** to accepted Protocol 6.2 or to the established Protocol 6.3 design. This workplan therefore reopens only Stages B, D, and F at the owning surfaces identified below.

## Lossless design basis

The complete pre-review Protocol 6.3 design contract is the immutable workplan at:

```text
5de67c6a9509c1ede9104badc3ddae468c988311:
workplans/active/PROTOCOL-6.3-EVIDENCE-BACKED-PROJECT-ENGINEERING-MEMORY-WORKPLAN.md
```

Every still-valid obligation, non-goal, T40-T120 preservation row, Q63-01..Q63-79 case, F63-A..F63-BJ falsification, four inherited Challenge passes, bootstrap/profile/package/frozen-resource rule, and Stage-G restriction in that snapshot remains binding unless this reopened contract explicitly strengthens it. This current workplan is the snapshot-complete current-state delta; it does not replay closed review chronology as authority.

Implementation and Review use the accepted Protocol 6.2 owners at `b59adc77efe6951912cfd705cc43830c58ca27d0`, especially:

- `source/roles/software-design/SKILL.md`;
- `source/shared/references/abstraction-and-concretization.md`;
- `source/shared/references/architecture-and-design.md`;
- `source/shared/references/workflow-and-workplans.md`;
- `source/shared/references/evidence-evolution-and-dependencies.md`;
- `source/shared/references/testing-and-validation.md`.

The 6.2 rules remain controlling: coherent D3 plus wrong D4 is a D4 blocker; workplans are bounded current contracts rather than proof scripts; executable claims require discriminating counterfactuals; evidence never becomes authority; repair existing owners before adding wrappers; and lossless representation precedes compactness.

## Governing repair invariant

The existing PEM representation and validator must become strong enough that the invalid counterfactuals discovered by independent Review cannot validate or receive a Stage-F PASS. Repair by alteration of the existing canonical validator/reconciliation/rendering path. Do **not** add a second memory database, registry, resolver daemon, compliance wrapper, shadow manifest, package-side patch, or alternate qualification authority.

## Reopened Stage B - schema/concretization repairs

### B4.1 Accepted-family semantic identity cannot drift silently

Owner: `source/project_engineering_memory.py` reconciliation plus the canonical PEM semantic-identity contract.

For an accepted family ID present in both prior accepted memory and a candidate/current memory, compare the family kind, semantic identity envelope, and applicability meaning. A changed envelope under the same ID must not silently pass. Same-ID editorial clarification or evidence-backed narrowing may remain within the envelope only through an explicit evidence-bound reconciliation record that binds the previous envelope identity and states why the change remains within the existing family. A materially different claim, owner class, mechanism family, kind, or applicability meaning requires a different/successor/split/merge/reclassification identity and lineage.

**Required discriminator:** an unchanged `SP-001` whose `mechanism_family`, `owner_class`, governing claim, or applicability meaning is silently replaced must fail reconciliation. A correctly identified unchanged envelope passes. An explicitly evidence-bound within-envelope clarification may pass but remains reviewable; claimant assertion alone must not be mistaken for material-equivalence proof.

Owning cases: Q63-71, F63-BB, T112.

### B4.2 Candidate overlay must bind the exact accepted PEM publication

Owner: existing overlay/HAS validation seam.

`accepted_project_state`, `accepted_pem`, and `candidate_overlay_semantic_candidate` remain distinct identities. Overlay validation must receive the exact accepted PEM publication identity from project workflow/Git state; it must not infer that identity from the base PEM's internal `accepted_base.project_state`. A candidate overlay must explicitly declare `based_on_accepted_pem` equal to the externally selected accepted PEM publication and must preserve the accepted project-state basis separately.

**Required discriminator:** with project state `P`, accepted PEM publication `M`, and overlay `C`, `C` based on `P` must fail while `C` based on `M` passes; `C == M` must fail self-ratification.

Owning cases: Q63-53, Q63-64, Q63-77, F63-AJ, F63-AU, F63-BH, T94/T105/T118.

### B4.3 Evidence and authority locator health must include the stable locator

Owner: existing evidence-route realization/health path.

A local route is not `HEALTHY` merely because its commit and path resolve. When a route supplies `#stable-locator`, the immutable file at that revision must contain an interpretable matching locator under the supported text-locator semantics. A definitely absent locator is `UNAVAILABLE`; a locator form the validator cannot mechanically interpret is at most `REVIEW_REQUIRED`. Authority-owner validation inherits this rule.

**Required discriminator:** valid commit + valid path + nonexistent locator cannot support `HEALTHY`, `AUTHORITY_BOUND`, comparative-owner priority, repair acceptance, or a current material warrant.

Owning cases: Q63-06, Q63-45, Q63-68, F63-AB, F63-AY, T43/T86/T109.

### B4.4 Mechanism-specific failure causality requires discriminating warrant

Owner: failure-occurrence causal representation in the existing PEM validator.

Observation, association, and mechanism-specific causal attribution remain distinct. An occurrence that records a non-empty mechanism/cause claim must bind non-empty durable cause evidence. A record explicitly claiming mechanism-specific causal strength cannot contribute that stronger interpretation without such evidence. An occurrence may remain observation/association-only without inventing a mechanism.

**Required discriminator:** an admissible confirmed occurrence with a mechanism-specific causal claim but no cause evidence must fail; the same observed failure without a mechanism claim may remain bounded/provisional; a mechanism claim with durable evidence may pass structural validation while semantic causality remains independently reviewable.

Owning cases: Q63-09, Q63-47, Q63-66, F63-C, F63-AD, F63-AW, T49/T88/T107.

### B4.5 Positive guidance requires an explicit bounded counterevidence-search disposition

Owner: existing success-pattern positive-guidance eligibility path.

Before a success pattern becomes current recommended/comparative guidance, require a structured bounded counterevidence-search record that identifies the declared search scope/basis, confirms review of favorable and unfavorable/neutral/inconclusive outcome classes, states material blind spots, and binds durable search evidence. Only a search complete for the declared scope may support unqualified current positive guidance. Partial search may preserve an observed/provisional pattern but cannot become an unqualified project instinct.

Do not require global history scans. This is a bounded admission record over the declared aggregation/coverage scope and existing evidence routes.

**Required discriminator:** one supporting application with no counterevidence-search record cannot become positive guidance even when no contradiction is recorded. A bounded complete search with no applicable contradiction may pass eligibility.

Owning cases: Q63-15, Q63-33, Q63-42, Q63-50, F63-E, F63-P, F63-Y, F63-AG, T45/T73/T83/T91.

### B4.6 Unresolved notices must not be starved behind optional positive guidance

Owner: existing active-summary renderer/salience path.

Render current high-impact unresolved notices (`REVIEW_REQUIRED`, unhealthy/unavailable binding, or fired/indeterminate review trigger) before lower-consequence optional positive guidance. Do not invent a global scalar ranking. Preserve current family-table behavior and all lower-salience mandatory constraints; this repair only prevents the existing notice-after-all-families layout from structurally starving unresolved notice state.

**Required discriminator:** a memory containing many positive current patterns plus an unresolved current notice must render the unresolved notice before those optional positive rows.

Owning cases: Q63-14, Q63-50, Q63-69, F63-AZ, Challenge-Priority, T69/T91/T110.

### B4.7 Temperature override evidence must use the normal evidence path

Owner: existing temperature override and material-route health logic.

A temperature override whose final value differs from the derived base must carry a reason and a non-empty list of syntactically valid evidence routes. Those routes are material family warrants and therefore participate in existing binding-health realization. Arbitrary text, a broken locator, or an unavailable route cannot qualify as evidence-bound promotion.

**Required discriminator:** an override with arbitrary/unparseable evidence fails; a declared `HEALTHY` current family whose override warrant is unavailable fails binding-health validation.

Owning cases: Q63-13, Q63-14, F63-B, F63-R, T47/T75/T86.

## Reopened Stage D - qualification-oracle repairs

The seven repairs above are mechanically decidable at the current validator/renderer boundary. Their qualification rows therefore must be backed by executable valid/counterfactual discriminators rather than doctrine-only prose.

Add focused tests, preferably in one review-repair test module, covering at minimum:

```text
D8-01 same-ID semantic-envelope drift rejected
D8-02 accepted project state != accepted PEM publication overlay test
D8-03 missing stable locator cannot be HEALTHY
D8-04 mechanism-specific cause without cause evidence rejected
D8-05 wins-only positive guidance rejected without bounded counterevidence search
D8-06 unresolved notice precedes optional positive guidance in summary
D8-07 temperature override evidence parsed and health-realized
```

Remap the following previously non-discriminating or mis-bound Stage-F rows to the new executable discriminators where their decisive behavior is mechanical: Q63-06, Q63-13, Q63-42, Q63-64, Q63-66, Q63-69, Q63-71 and F63-Y, F63-AU, F63-AW, F63-AZ, F63-BB, plus any other row whose old oracle is falsified by these tests. Historical F2/F3 PASS records remain immutable evidence and may not be rewritten into current acceptance.

## Reopened Stage F - fresh repaired candidate

After B4/D8 repair:

1. run focused review-repair tests first;
2. run all Protocol 6.3 PEM/bootstrap/reopened tests;
3. run the complete source repository regression;
4. validate self-hosted `PROJECT-ENGINEERING-MEMORY.md` with the repaired validator;
5. rebuild canonical skill packages and independently validate them;
6. verify committed `dist/` parity if canonical packaged source changed;
7. recheck Protocol 6.3 profile/snapshot parity and Orchestrator Core acceptance when affected;
8. recheck frozen 5.16/6.0/6.1/6.2 resources against accepted Protocol 6.2;
9. execute all 115 inherited scenarios, Q63-01..Q63-79, F63-A..F63-BJ, and all four inherited Challenge dimensions against one repaired semantic candidate, explicitly replacing invalid F2/F3 oracles;
10. issue a new snapshot-complete independent-review handoff and perform a fresh independent assembled-candidate Review.

Prior bootstrap `dc22f09fd38dbbfeaeb0160152da9b284654f66e` is not automatically preserved as current 6.3 fallback. If any canonical source semantics required by that immutable bootstrap change in this repair, apply the existing replacement-bootstrap rule: preserve it as historical evidence, validate a new already-existing repaired source snapshot, publish that exact snapshot only from a later descendant, and rerun exact-ref qualification.

## Preservation and non-goals

The repair must preserve accepted Protocol 6.2 T01-T39, the still-valid Protocol 6.3 T40-T120 contract, prior frozen profile/resource bytes, current-vs-history separation, cold-route/progressive-disclosure behavior, owner-layer simplification, exact bootstrap/recovery separation, source/generated/package parity, and all unaffected admissible evidence with explicit applicability.

Do not broaden this repair into Protocol 7, a general evidence database, global history crawler, generic ranking engine, external evidence service, new acceptance registry, or schema-2 migration. The smallest correct repair is preferred.

## PASS / NO-PASS for this reopened cycle

**PASS** requires all seven B4 repairs implemented at existing owners, all seven D8 counterfactuals discriminating correctly, every affected Q63/F63/Challenge row remapped to a valid oracle, full affected/final assembled regression green, generated/package/profile/frozen integrity closed as applicable, a new immutable semantic candidate and any required replacement bootstrap lifecycle closed, and fresh independent assembled-candidate Review PASS with no blocker or Serious Challenge.

**NO-PASS** includes any remaining silent same-ID semantic drift, overlay basis conflation, path-only locator health, unsupported mechanism causality, wins-only positive guidance, unresolved-notice starvation, nominal temperature-override evidence, stale/non-discriminating Stage-F PASS mapping, package/profile/frozen drift, or use of earlier qualification as current acceptance after the candidate changes.

## Current next action

Implement B4.1-B4.7 in the existing PEM validator/reconciliation/renderer, add D8.1-D8.7 executable discriminators, run the affected/full acceptance surface, then bind a repaired immutable candidate. Stage G remains blocked until the resulting candidate passes fresh independent Review.
