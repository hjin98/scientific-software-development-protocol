---
kind: protocol-minor-revision-workplan-amendment
workplan_id: SSDP-6.1-EVIDENCE-EVOLUTION-AND-CONCRETIZATION-ALIGNMENT-REVISION-1-SECOND-REVIEW-CLOSURE
amends_workplan: SSDP-6.1-EVIDENCE-EVOLUTION-AND-CONCRETIZATION-ALIGNMENT
protocol_version: 6.0.0
target_protocol_version: 6.1.0
status: active
created_date: 2026-09-09
review_round: 2
active_serious_challenge: none
---

# SSDP 6.1 Evidence, Evolution, and Concretization Alignment — Revision 1 Second-Review Closure

## 1. Status and authority

This amendment is a **mandatory current companion** to `SSDP-6.1-EVIDENCE-EVOLUTION-AND-CONCRETIZATION-ALIGNMENT.md`. It closes gaps found by a second Protocol 6 review without changing the parent workplan's objective or pre-automation control boundary.

The parent workplan plus this amendment form the complete current 6.1 implementation handoff. Where this amendment narrows or clarifies parent wording, this amendment governs that ambiguity. All parent requirements not explicitly changed here remain binding.

No Serious Challenge was found to the 6.1 objective. The remaining issues were specification completeness and boundary precision.

## 2. Preserve semantic capability, not legacy lexemes or accidental path churn

The parent correctly makes `abstraction <-> concretization` the current 6.1 semantic relation and reserves `realization` for evidence instantiation. The implementation SHALL apply that terminology semantically rather than performing a blind repository-wide rename.

### 2.1 Legacy identifiers may remain opaque compatibility identifiers

Historical/version-pinned artifacts retain their original terminology as already required.

In addition, a **protocol-stable identifier or path** created under an earlier version MAY retain a legacy `realization` lexeme when renaming it would create unnecessary compatibility breakage, link churn, package/profile incompatibility, or historical ambiguity. Examples can include an old filename, workplan ID, profile key, serialized identifier, or public API token.

Such retained text is an **opaque compatibility identifier**, not current 6.1 semantic vocabulary. Current prose, newly introduced identifiers, headings, relationships, and normative explanations SHALL use `concretization` for abstraction descent and `evidence realization` for evidence instantiation.

Where a retained identifier could confuse a reader, provide one concise compatibility mapping at the owning current reference rather than maintaining two competing vocabularies.

Do not rename an externally/version-governed identifier merely to make a grep result lexically uniform. Do not preserve legacy wording in current prose merely because a stable identifier still contains it.

### 2.2 Version boundary remains semantic

A 6.0 artifact using `realization` for abstraction descent remains correct **for Protocol 6.0**. A current 6.1 artifact using that word with the old semantic meaning without an explicit compatibility context is drift.

This distinction must be covered by source/package/profile validation and behavioral qualification.

## 3. Reference integrity for bounded dependency and evolution records

The parent correctly rejects a universal identity registry, but dependency/history records still need enough identity to survive ordinary maintenance.

Every material relationship recorded under sections 6, 10, or 11 of the parent SHALL identify its endpoints unambiguously enough for a later reviewer to recover the intended subject without hidden chat. Use the cheapest sufficient combination, such as:

- stable logical name or existing domain/workplan ID;
- repository path and section/anchor;
- governing protocol/release identity;
- Git commit/tag when the referenced historical revision matters;
- other already-governed project identity where superior.

A new globally unique ID is **not** required when existing repository/version identity is sufficient.

If a current artifact is renamed/moved/split/merged and a maintained dependency record would otherwise become ambiguous or dangling, reconcile the affected reference as part of the same closeout. Historical entries that intentionally refer to an old revision retain the old immutable reference.

### 3.1 Current dependency view versus evolution history

Do not turn the current dependency record into append-only patch history.

- the **current dependency representation** describes currently applicable material relationships needed for impact analysis and verification;
- the **semantic evolution record** explains material supersession/rejection/generalization and why the current state changed;
- Git retains detailed file chronology.

When a current relationship is superseded, remove/replace it from the current dependency view as appropriate and preserve the material reason in evolution history when the historical rationale meets the parent's recording threshold.

This prevents stale dependency edges from becoming the graph equivalent of stale tests.

## 4. Maintenance ownership and authority boundary

Dependency/history records are support/coordination artifacts; they do not become a fifth semantic authority.

Responsibility follows the semantic change:

1. the D1/D2/D3/D4 owner responsible for accepting or executing the material semantic change is responsible for ensuring materially affected dependency references and evolution-history obligations are identified;
2. `software-documentation` may reconcile, restructure, and publish those records as support, but may not decide a D1-D4 semantic relationship when that relationship is disputed;
3. a material disagreement about whether `A CONCRETIZES B`, whether an assumption is still governing, or whether an evidence oracle remains semantically applicable routes to the earliest owning domain rather than being resolved editorially;
4. Closeout verifies that required record updates are complete but does not invent product/scientific truth.

Do not require a permanent centralized historian role or separate approval gate.

## 5. Evidence hierarchy is a durability preference, not a substitution hierarchy

The test/evidence durability ordering in the parent applies **only among evidence capable of establishing the same governed claim with comparable strength**.

It SHALL NOT be interpreted as:

- D1 evidence replacing required D2 numerical verification;
- D1/D2 invariant evidence replacing required D4 functional/integration evidence;
- a high-level end-to-end result proving lower-level conformance that it cannot discriminate;
- a lower-level unit test establishing scientific adequacy merely because it is precise.

Evidence may satisfy only claims that its oracle and exercised semantic owner can actually establish.

Therefore preserve both dimensions:

```text
durability preference
AND
claim-specific evidentiary sufficiency
```

Proxy-proof/real-owner rules remain controlling. Higher abstraction level does not compensate for a proxy oracle, and lower-level precision does not compensate for testing the wrong claim.

Add an explicit adversarial qualification scenario demonstrating this non-substitution rule.

## 6. Evidence realization applicability and identity

A prior evidence realization is reusable only when the dimensions capable of altering its claim remain materially equivalent under Protocol 6 evidence-reuse doctrine.

Where material, enough provenance must be recoverable to determine applicability, including the relevant combination of:

- evidence specification revision;
- subject/candidate revision;
- governed claim/authority revision;
- input or validity regime;
- oracle semantics;
- execution environment/backend/precision/configuration when capable of changing interpretation;
- required protocol obligation.

Do not require a universal manifest/hash envelope for every ordinary test run. Native CI/test/benchmark/experiment artifacts remain sufficient when they already establish the needed identity and interpretation.

A rerun against a changed candidate creates a new evidence realization; it does not mutate the historical result into evidence for the new candidate.

## 7. Staleness is epistemic applicability, not automatic falsity

Clarify the parent's stale-evidence doctrine:

- `stale` means the prior evidence realization/specification mapping cannot currently support or refute the target claim without review/re-execution/remapping;
- it does **not** by itself prove that the underlying claim became false;
- `review_required` is appropriate when applicability is uncertain rather than known invalid;
- a stale passing result and stale failing result are both inadmissible for current closure until reconciled.

This prevents invalidation machinery from converting uncertainty into a false negative or false positive.

## 8. Dependency-record proportionality test

Create/maintain an explicit Markdown dependency record only when it reduces material ambiguity, invalidation risk, rediscovery, or stale-evidence confusion better than existing links/anchors/workplan mappings.

A useful counterfactual is:

> If this record were absent, could a competent reviewer still identify the materially dependent authority/evidence surface reliably and economically from current canonical artifacts?

If yes, existing references are sufficient. If no, add the bounded record.

This preserves Protocol 6's prohibition against registry construction for symmetry alone.

## 9. Additional implementation obligations

The 6.1 implementation sequence SHALL additionally:

1. inventory protocol-stable identifiers/paths containing legacy `realization` vocabulary and classify each as rename-safe current semantics, immutable history, or retained compatibility identifier;
2. define the minimal Markdown convention/location for current semantic dependency records and semantic evolution history without creating duplicate authority;
3. state the maintenance owner/closeout trigger for those records;
4. ensure current dependency views do not retain superseded relationships as though current;
5. preserve enough evidence-realization identity to evaluate reuse without introducing universal evidence manifests;
6. add qualification for evidence-level non-substitution and retained legacy-identifier compatibility.

## 10. Additional acceptance criteria

The parent workplan cannot PASS until these additional conditions hold:

1. no current 6.1 prose uses `realization` for abstraction descent except an explicit historical/compatibility explanation;
2. retained legacy lexemes in stable IDs/paths are explicitly treated as opaque compatibility identity rather than current semantic vocabulary;
3. every material maintained dependency/history reference is unambiguous and non-dangling for its intended current or historical revision;
4. current dependency views and historical evolution records have distinct purposes and do not compete as current authority;
5. responsibility for maintaining those records is tied to the owning semantic change/Closeout without inventing a fifth authority role;
6. evidence durability preference cannot substitute higher-level evidence for required lower-level conformance/functional evidence or vice versa;
7. staleness is treated as loss/uncertainty of applicability, not automatic falsification;
8. evidence reuse can identify the materially relevant realization/candidate/claim regime without requiring unnecessary universal manifests;
9. behavioral qualification covers legacy-identifier compatibility, stale-evidence applicability, and cross-level evidence non-substitution.

## 11. Second-review disposition

```text
SERIOUS CHALLENGE: NONE
SECOND REVIEW: PASS AFTER THIS AMENDMENT
BLOCKING DESIGN GAPS: CLOSED BY REVISION 1
IMPLEMENTATION AUTHORITY: PARENT WORKPLAN + THIS MANDATORY COMPANION
```

The amendment does not authorize Protocol 7 machinery under 6.1 and does not alter the requirement to preserve an immutable qualified 6.1 pre-automation recovery release.