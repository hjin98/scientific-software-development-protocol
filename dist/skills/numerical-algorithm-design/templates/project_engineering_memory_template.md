---
memory_schema_version: 1
maintained_under_protocol: 6.3.0
project_id: REPLACE_WITH_STABLE_PROJECT_ID
repository: REPLACE_WITH_REPOSITORY_OR_PROJECT_IDENTITY
scope: repository
coverage_state: UNINITIALIZED
coverage_basis: "No historical backfill has been claimed."
reconciled_through: REPLACE_WITH_ALREADY_EXISTING_ACCEPTED_PROJECT_IDENTITY
accepted_base: REPLACE_WITH_ACCEPTED_PROJECT_MEMORY_BASIS
candidate_overlay: NONE
detail_files: []
---

# Project Engineering Memory

This is compact project-local engineering memory, not D1-D4 semantic authority. Current owners define what must be true; this file records evidence-backed lessons and routes to their warrant. Missing or partial memory never proves that no relevant historical lesson exists.

## Active summary

<!-- BEGIN DERIVED PEM SUMMARY -->
_No current entries._
<!-- END DERIVED PEM SUMMARY -->

## Families

Add a family only when the Protocol 6.3 admission threshold is met. Keep one canonical fenced `yaml pem-family` record beneath each family heading. Do not copy this explanatory example into a live memory unchanged.

### FF-001 — Example failure family

```yaml pem-family
id: FF-001
kind: FAILURE_FAMILY
state: CURRENT
maturity: PROVISIONAL
temperature: UNASSESSED
summary: Replace with one bounded evidence-backed lesson.
semantic_identity:
  invariant_or_claim: Replace with the governing bounded invariant or claim.
  owner_class: Replace with the current semantic owner class.
  mechanism_family: Replace with the repair-relevant failure mechanism.
  applicability_dimensions: Replace with material regime dimensions.
aggregation_scope: Replace with the bounded aggregation regime.
coverage_state: PARTIAL
coverage_basis: Replace with reviewed sources/surfaces/range and material blind spots.
applicability:
  - replace-with-searchable-owner-surface-mechanism-or-regime-cue
authority_binding: EVIDENCE_ONLY
guidance_level: OBSERVED
relations: []
occurrences:
  - id: O01
    event_identity: REPLACE_WITH_IMMUTABLE_EVENT_IDENTITY
    lifecycle_context: qualification
    source_project: local
    surfaces:
      - replace-with-affected-surface
    observation: Replace with the observation; do not rewrite it to match later interpretation.
    cause_claim: Replace with bounded causal interpretation or mark unknown/provisional.
    cause_evidence:
      - REPLACE_WITH_IMMUTABLE_EVIDENCE_ROUTE
    repair: REPLACE_WITH_IMMUTABLE_REPAIR_IDENTITY_OR_NONE
    repair_acceptance: REPLACE_WITH_ACCEPTANCE_IDENTITY_OR_NONE
    provenance_cluster: REPLACE_WITH_CLUSTER_OR_NONE
    assessments:
      - id: AS01
        state: ADMISSIBLE
        conclusion: CONFIRMED
        evidence:
          - REPLACE_WITH_IMMUTABLE_EVIDENCE_ROUTE
```

### SP-001 — Example success pattern

```yaml pem-family
id: SP-001
kind: SUCCESS_PATTERN
state: CURRENT
maturity: PROVISIONAL
temperature: UNASSESSED
summary: Replace with one bounded evidence-backed positive lesson.
semantic_identity:
  invariant_or_claim: Replace with the exact bounded benefit claim.
  owner_class: Replace with current semantic owner class.
  mechanism_family: Replace with the learned engineering mechanism/pattern.
  applicability_dimensions: Replace with material regime dimensions.
aggregation_scope: Replace with the bounded aggregation regime.
coverage_state: PARTIAL
coverage_basis: Replace with favorable and unfavorable history searched plus blind spots.
applicability:
  - replace-with-searchable-applicability-cue
authority_binding: EVIDENCE_ONLY
guidance_level: OBSERVED
positive_guidance_eligible: false
comparative_basis: NONE
relations: []
applications:
  - id: A01
    episode_identity: REPLACE_WITH_IMMUTABLE_INTERVENTION_IDENTITY
    lifecycle_context: qualification
    source_project: local
    surfaces:
      - replace-with-affected-surface
    provenance_cluster: REPLACE_WITH_CLUSTER_OR_NONE
    subject: REPLACE_WITH_SUBJECT
    comparator: REPLACE_WITH_COMPARATOR_OR_NONE
    intended_benefit: REPLACE_WITH_BOUNDED_BENEFIT
    outcome: SUPPORTING
    observation: Replace with the observed outcome.
    quantitative_effect: REPLACE_WITH_EFFECT_OR_NONE
    uncertainty: REPLACE_WITH_UNCERTAINTY_OR_NONE
    costs_tradeoffs: REPLACE_WITH_COSTS_OR_NONE
    assessments:
      - id: AS01
        state: ADMISSIBLE
        conclusion: SUPPORTS_BOUNDED_CLAIM
        evidence:
          - REPLACE_WITH_IMMUTABLE_EVIDENCE_ROUTE
```

When a later assessment replaces an earlier current interpretation, append it with explicit lineage rather than relying on list order, for example `supersedes: [AS01]`. If competent assessments remain materially conflicting, preserve both as live or append an explicit `REVIEW_REQUIRED` adjudication that supersedes the resolved prior state; do not use latest-editor position or vote count as current truth.

## Current notices

Use notices only for high-impact current facts that are not yet honest generalized families. Current notices use typed, evaluable triggers. For an accepted-base/owner/binding-change trigger, capture the admitted basis when the notice is created; do not replace it with opaque prose.

### NT-001 — Example current notice

```yaml pem-notice
id: NT-001
state: REVIEW_REQUIRED
summary: Replace with bounded current fact.
normative_status: NON_AUTHORITATIVE
owner: NONE
applicability:
  - replace-with-applicability-cue
binding_health: REVIEW_REQUIRED
evidence:
  - REPLACE_WITH_IMMUTABLE_EVIDENCE_ROUTE
review_trigger:
  type: accepted_base_change
  basis: REPLACE_WITH_EXACT_ACCEPTED_BASE_AT_NOTICE_ADMISSION
```

## Historical Applicability Set handoff shape

A workplan that triggers PEM records the exact basis used; this block normally belongs in that workplan/handoff rather than in the project memory itself. These three basis fields are the canonical executable interface; do not substitute `accepted_base`, `candidate_overlay`, or another translation alias.

```yaml pem-has
pem_basis:
  accepted_project_state: REPLACE_WITH_EXACT_ACCEPTED_PROJECT_STATE
  accepted_pem: REPLACE_WITH_EXACT_ACCEPTED_PEM_PUBLICATION_OR_NONE
  candidate_overlay_semantic_candidate: REPLACE_WITH_EXACT_CANDIDATE_OR_NONE
has:
  - id: FF-001
    disposition: REVIEW_REQUIRED
    reason: Replace with bounded current-task reason.
```

If the accepted memory basis materially advances before integration/closeout, reconcile the changed interval/surfaces and refresh the HAS rather than silently keeping the old decision.
