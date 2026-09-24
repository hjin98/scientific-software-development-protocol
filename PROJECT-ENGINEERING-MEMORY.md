---
memory_schema_version: 1
maintained_under_protocol: 6.5.0
project_id: hjin98-scientific-software-development-protocol
repository: hjin98/scientific-software-development-protocol
scope: repository
coverage_state: PARTIAL
coverage_basis: "Reconciled through the frozen accepted Protocol 6.4 P0 control, including bounded Protocol 6.2-6.4 bootstrap/recovery, routing, frozen-profile and independent-Review evidence plus current 6.5 candidate implementation learning. Earlier unrelated project history is not claimed exhaustive."
reconciled_through: 55c085261eb827e3047637d045a8e6917ea6b962
accepted_base:
  project_state: 55c085261eb827e3047637d045a8e6917ea6b962
  basis: "Frozen Protocol 6.4 P0 integrated accepted repository state for this 6.5 cycle; mutable release identities remain owned by PROTOCOL-RELEASE-STATE.yaml."
candidate_overlay: "ssdp-6.5-frontier-model-re-evaluation candidate overlay; branch publication is implementation evidence only and is not self-declared accepted."
detail_files: []
---

# Project Engineering Memory

This is the Scientific Software Development Protocol (SSDP) repository's project-local engineering memory. It records evidence-backed lessons that may improve future engineering decisions, but it is not D1-D4 semantic authority. Current protocol/project/external owners define what must be true. Coverage remains deliberately bounded rather than exhaustive; absence here does not establish that no relevant historical lesson exists.

## Active summary

<!-- BEGIN DERIVED PEM SUMMARY -->
| ID | Kind | Temperature | Maturity/state | Binding | Guidance | Current evidence | Bounded lesson |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SP-002 | SUCCESS_PATTERN | HOT | SUPPORTED/CURRENT | EVIDENCE_ONLY/HEALTHY | OBSERVED | 3 supporting / 0 neutral / 0 contradicting / 0 inconclusive | Across accepted Protocol 6.2, 6.3, and 6.4 releases, constructing and qualifying an immutable self-reference-safe source snapshot before a later descendant publishes its exact fallback identity avoided impossible commit self-reference while keeping public fallback distinct from recovery. |
| FF-001 | FAILURE_FAMILY | WARM | SUPPORTED/CURRENT | EVIDENCE_ONLY/HEALTHY | OBSERVED | 2 confirmed | Publishing an immutable public-source fallback before the source state contains all required repaired routes can freeze a semantically stale bootstrap even when the branch later becomes correct. |
| DS-001 | DISCOVERY | UNASSESSED | SUPPORTED/CURRENT | EVIDENCE_ONLY/HEALTHY | OBSERVED | 2 evidence route(s) | A self-contained synthetic semantic fixture matrix can remain green while failing to discriminate real-owner semantic defects; qualification evidence must stay bounded to the property its method actually tests, while assembled prose adequacy requires independent semantic Review. |
| PC-001 | PRESERVATION_CAPABILITY | UNASSESSED | SUPPORTED/CURRENT | AUTHORITY_BOUND/HEALTHY | OBSERVED | 2 evidence route(s) | Successor protocol work must preserve version-bound frozen historical profiles/resources independently; adding a new profile is not permission to mutate prior-version bytes or recovery semantics. |
| SP-001 | SUCCESS_PATTERN | UNASSESSED | SUPPORTED/CURRENT | EVIDENCE_ONLY/HEALTHY | OBSERVED | 1 supporting / 0 neutral / 0 contradicting / 0 inconclusive | For source-to-package routing defects, repairing the canonical router first and regenerating derived packages restored both activation semantics and transport reachability without creating package-side shadow authority. |
<!-- END DERIVED PEM SUMMARY -->

## Families

### FF-001 — Premature immutable bootstrap publication

```yaml pem-family
id: FF-001
kind: FAILURE_FAMILY
state: CURRENT
maturity: SUPPORTED
temperature: WARM
summary: Publishing an immutable public-source fallback before the source state contains all required repaired routes can freeze a semantically stale bootstrap even when the branch later becomes correct.
semantic_identity:
  invariant_or_claim: A versioned public-source bootstrap must identify an already validated immutable source state that contains every required current route/capability for that fallback contract.
  owner_class: protocol versioning and source-resolution lifecycle
  mechanism_family: immutable fallback identity published from a source snapshot that predates a required semantic/routing repair
  applicability_dimensions: successor protocol bootstrap, exact-ref public fallback, source/package route closure, self-reference-safe publication
aggregation_scope: SSDP protocol-version public-source bootstrap and exact-ref fallback publication episodes
coverage_state: PARTIAL
coverage_basis: Reviewed the Protocol 6.2 invalidated bootstrap, bootstrap affected requalification, final independent Review, and accepted 6.2 recovery lineage; earlier bootstrap history is not claimed exhaustive.
applicability:
  - protocol bootstrap
  - public-source fallback
  - exact immutable ref
  - replacement bootstrap
  - route repair before publication
authority_binding: EVIDENCE_ONLY
binding_health: HEALTHY
guidance_level: OBSERVED
relations: []
occurrences:
  - id: O01
    event_identity: "hjin98/scientific-software-development-protocol@1181c2031710c5d343194d87d08543290fded0ab"
    lifecycle_context: Protocol 6.2 pre-acceptance public-source bootstrap
    source_project: local
    surfaces:
      - source version/fallback mapping
      - software-documentation cold-route reachability
      - standalone generated package closure
    observation: The first Protocol 6.2 bootstrap was published from a snapshot predating the later documentation cold-route repair and was subsequently invalidated rather than retained as current fallback.
    cause_claim: The bootstrap designation occurred before the source snapshot contained the required repaired cold routes, so later branch correctness could not make that already-immutable snapshot satisfy the current fallback contract.
    cause_evidence:
      - "hjin98/scientific-software-development-protocol@b59adc77efe6951912cfd705cc43830c58ca27d0:qualification/ssdp6/RESULTS-GPT-5.6-SOL-2026-09-10-PROTOCOL-6.2-BOOTSTRAP-REQUALIFICATION.md"
      - "hjin98/scientific-software-development-protocol@b59adc77efe6951912cfd705cc43830c58ca27d0:qualification/ssdp6/FINAL-REVIEW-GPT-5.6-SOL-2026-09-10-PROTOCOL-6.2.md"
    repair: "replacement bootstrap 5a062ebc472755607b9dc66d33a5ebbc4b7429aa; descendant semantic candidate ebbc4591bdfed039512026b8acb3a6749475c1c5 published that exact identity after validation"
    repair_acceptance: "Protocol 6.2 accepted recovery b59adc77efe6951912cfd705cc43830c58ca27d0"
    provenance_cluster: ssdp62-bootstrap-repair
    assessments:
      - id: AS01
        state: ADMISSIBLE
        conclusion: CONFIRMED
        evidence:
          - "hjin98/scientific-software-development-protocol@b59adc77efe6951912cfd705cc43830c58ca27d0:qualification/ssdp6/RESULTS-GPT-5.6-SOL-2026-09-10-PROTOCOL-6.2-BOOTSTRAP-REQUALIFICATION.md"
          - "hjin98/scientific-software-development-protocol@b59adc77efe6951912cfd705cc43830c58ca27d0:qualification/ssdp6/FINAL-REVIEW-GPT-5.6-SOL-2026-09-10-PROTOCOL-6.2.md"
  - id: O02
    event_identity: "hjin98/scientific-software-development-protocol@1484c1d3caa49d87cc15bc52a5e775399c1dae1b"
    lifecycle_context: Protocol 6.3 pre-acceptance public-source bootstrap
    source_project: local
    surfaces:
      - source version/fallback mapping
      - PEM/bootstrap validation lineage
      - exact-ref public-source publication
    observation: A later Protocol 6.3 bootstrap was also invalidated after subsequent qualification exposed defects that the immutable published snapshot could not inherit from later branch repairs.
    cause_claim: The immutable fallback identity again preceded completion of all repairs required by the eventual accepted public-source contract; this is a second confirmed mechanism occurrence but is not labeled schema-qualified recurrence because its historical repair acceptance predates the current structured recurrence_basis contract.
    cause_evidence:
      - "hjin98/scientific-software-development-protocol@55c085261eb827e3047637d045a8e6917ea6b962:history/SEMANTIC_EVOLUTION.md"
      - "hjin98/scientific-software-development-protocol@55c085261eb827e3047637d045a8e6917ea6b962:qualification/ssdp6/RESULTS-GPT-5.6-SOL-2026-09-11-PROTOCOL-6.3-BOOTSTRAP.md"
    repair: "later self-reference-safe 6.3 public bootstrap 86c13cab6bdd1991dffa94e277db8eacf87e2e11, published only after repaired exact-source qualification"
    repair_acceptance: "Protocol 6.3 accepted recovery 9f353097fab36e325a325f1c2f9d9cec32e86177"
    provenance_cluster: ssdp63-bootstrap-repair
    assessments:
      - id: AS02
        state: ADMISSIBLE
        conclusion: CONFIRMED
        evidence:
          - "hjin98/scientific-software-development-protocol@55c085261eb827e3047637d045a8e6917ea6b962:history/SEMANTIC_EVOLUTION.md"
          - "hjin98/scientific-software-development-protocol@55c085261eb827e3047637d045a8e6917ea6b962:qualification/ssdp6/RESULTS-GPT-5.6-SOL-2026-09-11-PROTOCOL-6.3-BOOTSTRAP.md"
```

### PC-001 — Frozen prior-version profile/resource preservation

```yaml pem-family
id: PC-001
kind: PRESERVATION_CAPABILITY
state: CURRENT
maturity: SUPPORTED
temperature: UNASSESSED
summary: Successor protocol work must preserve version-bound frozen historical profiles/resources independently; adding a new profile is not permission to mutate prior-version bytes or recovery semantics.
semantic_identity:
  invariant_or_claim: New protocol/profile generations coexist with immutable prior-version recovery/profile resources whose historical bytes and version-bound behavior remain independently testable.
  owner_class: protocol versioning and compatibility
  mechanism_family: separate version-bound profile/resource generation with frozen historical trees used as preservation oracles
  applicability_dimensions: protocol minor/major successor implementation, profile generation, recovery, package/snapshot regeneration
aggregation_scope: SSDP successor protocol/profile implementations that retain supported historical recovery identities
coverage_state: PARTIAL
coverage_basis: Reviewed Protocol 6.2 frozen tree identities and independent Review evidence across 5.16, 6.0, and 6.1 plus the accepted 6.2 recovery mapping; older implementation rounds are not globally backfilled.
applicability:
  - frozen profile
  - historical resource
  - protocol recovery
  - successor profile generation
  - generated snapshot parity
authority_binding: AUTHORITY_BOUND
authority_owner: "hjin98/scientific-software-development-protocol@55c085261eb827e3047637d045a8e6917ea6b962:source/shared/references/protocol-versioning-and-compatibility.md"
authority_evidence:
  - "hjin98/scientific-software-development-protocol@55c085261eb827e3047637d045a8e6917ea6b962:source/shared/references/protocol-versioning-and-compatibility.md"
binding_health: HEALTHY
guidance_level: OBSERVED
relations: []
evidence:
  - "hjin98/scientific-software-development-protocol@b59adc77efe6951912cfd705cc43830c58ca27d0:qualification/ssdp6/FINAL-REVIEW-GPT-5.6-SOL-2026-09-10-PROTOCOL-6.2.md"
  - "hjin98/scientific-software-development-protocol@82e6e1badf2c88c00967155bb9d30c773b80d1ef:qualification/ssdp6/SSDP-6.3-PRESERVATION-CENSUS.md"
```

### SP-001 — Owner-layer route repair with derived regeneration

```yaml pem-family
id: SP-001
kind: SUCCESS_PATTERN
state: CURRENT
maturity: SUPPORTED
temperature: UNASSESSED
summary: For source-to-package routing defects, repairing the canonical router first and regenerating derived packages restored both activation semantics and transport reachability without creating package-side shadow authority.
semantic_identity:
  invariant_or_claim: A missing conditional route/package-closure defect can be corrected by repairing the canonical routing owner and regenerating descendants while preserving the distinction between activation semantics and package reachability.
  owner_class: routing ownership plus generated distribution integrity
  mechanism_family: canonical source-router repair followed by deterministic regeneration and affected requalification
  applicability_dimensions: Markdown resource routing, standalone skill package closure, generated distribution, cold conditional routes
aggregation_scope: SSDP source-to-generated-package routing repairs governed by canonical source ownership
coverage_state: PARTIAL
coverage_basis: Searched the Protocol 6.2 cold-route defect, its affected requalification, bootstrap requalification, and final independent Review for supporting and contradictory outcome evidence; no contradictory admissible episode was found in that bounded lineage, but broader project history is not claimed exhaustive.
applicability:
  - missing conditional route
  - package resource reachability
  - canonical router
  - regenerate dist
  - cold route repair
authority_binding: EVIDENCE_ONLY
binding_health: HEALTHY
guidance_level: OBSERVED
positive_guidance_eligible: false
comparative_basis: NONE
relations: []
applications:
  - id: A01
    episode_identity: "source repair dbb0db8c52a3f50a4cb7ee6a30b01028f419ea6a with generated repair 6f71812fe79bb9996fa467cc68dfe8d988d278d6"
    lifecycle_context: Protocol 6.2 documentation cold-route repair and affected requalification
    source_project: local
    surfaces:
      - software-documentation routing owner
      - source Markdown resource closure
      - dist/skills/software-documentation package closure
      - affected representation qualification
    provenance_cluster: ssdp62-cold-route-repair
    subject: canonical-router-first cold-route repair plus generated package regeneration
    comparator: NONE
    intended_benefit: Restore required conditional resource activation/reachability without hand-editing generated packages or turning package membership into routing authority.
    outcome: SUPPORTING
    observation: The repaired source router named all four required concern resources, regenerated packages contained them, focused affected requalification passed, and final independent Review found the cold-path defect genuinely repaired at the owning router.
    quantitative_effect: NONE
    uncertainty: One bounded Protocol 6.2 intervention; this does not establish universal superiority or an independent multi-episode success rate.
    costs_tradeoffs: Required affected requalification and regeneration of derived package surfaces after the semantic source repair.
    assessments:
      - id: AS01
        state: ADMISSIBLE
        conclusion: SUPPORTS_BOUNDED_CLAIM
        evidence:
          - "hjin98/scientific-software-development-protocol@b59adc77efe6951912cfd705cc43830c58ca27d0:qualification/ssdp6/RESULTS-GPT-5.6-SOL-2026-09-10-PROTOCOL-6.2-ROUTING-REQUALIFICATION.md"
          - "hjin98/scientific-software-development-protocol@b59adc77efe6951912cfd705cc43830c58ca27d0:qualification/ssdp6/FINAL-REVIEW-GPT-5.6-SOL-2026-09-10-PROTOCOL-6.2.md"
```

### SP-002 — Self-reference-safe descendant publication

```yaml pem-family
id: SP-002
kind: SUCCESS_PATTERN
state: CURRENT
maturity: SUPPORTED
temperature: HOT
summary: Across accepted Protocol 6.2, 6.3, and 6.4 releases, constructing and qualifying an immutable self-reference-safe source snapshot before a later descendant publishes its exact fallback identity avoided impossible commit self-reference while keeping public fallback distinct from recovery.
semantic_identity:
  invariant_or_claim: Version-bound public fallback publication is reliable when the candidate snapshot is immutable and qualified before a later descendant names that exact identity, with recovery selected and published separately.
  owner_class: protocol versioning and source-resolution lifecycle
  mechanism_family: immutable self-reference-safe candidate followed by descendant identity publication and later distinct recovery mapping
  applicability_dimensions: protocol successor release, exact-ref public fallback, Git commit self-reference, recovery separation
aggregation_scope: Accepted SSDP Protocol 6.2, 6.3, and 6.4 public-source publication lifecycles
coverage_state: PARTIAL
coverage_basis: Reviewed accepted semantic-evolution/review lineage for Protocol 6.2, 6.3, and 6.4. This supports a repeated bounded pattern but does not claim all repository releases or other projects.
applicability:
  - protocol bootstrap
  - exact immutable public fallback
  - self-reference-safe publication
  - distinct recovery
authority_binding: EVIDENCE_ONLY
binding_health: HEALTHY
guidance_level: OBSERVED
positive_guidance_eligible: false
comparative_basis: NONE
relations:
  - type: SUPPORTS_LEARNING_FROM
    target: FF-001
applications:
  - id: A01
    episode_identity: "protocol-6.2-publication-5a062ebc472755607b9dc66d33a5ebbc4b7429aa"
    lifecycle_context: accepted Protocol 6.2 publication/recovery lifecycle
    source_project: local
    surfaces: [public-source fallback, exact-ref bootstrap, recovery publication]
    provenance_cluster: ssdp62-release
    subject: immutable candidate first, descendant fallback publication second, recovery later
    comparator: NONE
    intended_benefit: avoid impossible self-reference and prevent premature immutable fallback publication
    outcome: SUPPORTING
    observation: The replacement Protocol 6.2 bootstrap was qualified as an immutable source snapshot, later named by descendant state, and kept distinct from recovery.
    quantitative_effect: NONE
    uncertainty: One accepted protocol release episode.
    costs_tradeoffs: Requires an additional descendant publication transaction and exact-ref verification.
    assessments:
      - id: AS01
        state: ADMISSIBLE
        conclusion: SUPPORTS_BOUNDED_CLAIM
        evidence:
          - "hjin98/scientific-software-development-protocol@55c085261eb827e3047637d045a8e6917ea6b962:history/SEMANTIC_EVOLUTION.md"
  - id: A02
    episode_identity: "protocol-6.3-publication-86c13cab6bdd1991dffa94e277db8eacf87e2e11"
    lifecycle_context: accepted Protocol 6.3 publication/recovery lifecycle
    source_project: local
    surfaces: [public-source fallback, exact-ref bootstrap, recovery publication]
    provenance_cluster: ssdp63-release
    subject: immutable candidate first, descendant fallback publication second, recovery later
    comparator: NONE
    intended_benefit: avoid self-reference and keep repaired source identity separate from later recovery authority
    outcome: SUPPORTING
    observation: The accepted 6.3 lineage explicitly replaced invalidated bootstrap attempts with a self-reference-safe source snapshot, later publication, and separate Review/recovery.
    quantitative_effect: NONE
    uncertainty: One accepted protocol release episode.
    costs_tradeoffs: Requires explicit invalidation/republication when an earlier immutable bootstrap is found defective.
    assessments:
      - id: AS02
        state: ADMISSIBLE
        conclusion: SUPPORTS_BOUNDED_CLAIM
        evidence:
          - "hjin98/scientific-software-development-protocol@55c085261eb827e3047637d045a8e6917ea6b962:history/SEMANTIC_EVOLUTION.md"
  - id: A03
    episode_identity: "protocol-6.4-publication-e09a9d1480211eea2d16d722182bb5c6de1bee12"
    lifecycle_context: accepted Protocol 6.4 publication/recovery lifecycle
    source_project: local
    surfaces: [public-source fallback, exact-ref bootstrap, recovery publication]
    provenance_cluster: ssdp64-release
    subject: immutable candidate first, descendant fallback publication second, recovery later
    comparator: NONE
    intended_benefit: preserve exact immutable bootstrap/recovery separation through accepted closeout
    outcome: SUPPORTING
    observation: Protocol 6.4 completed exact bootstrap publication and later distinct recovery publication without mutating the frozen bootstrap identity.
    quantitative_effect: NONE
    uncertainty: One accepted protocol release episode.
    costs_tradeoffs: Requires lifecycle bookkeeping and mapping-bearing descendant reconciliation.
    assessments:
      - id: AS03
        state: ADMISSIBLE
        conclusion: SUPPORTS_BOUNDED_CLAIM
        evidence:
          - "hjin98/scientific-software-development-protocol@55c085261eb827e3047637d045a8e6917ea6b962:history/SEMANTIC_EVOLUTION.md"
```

### DS-001 — Semantic proxy qualification can overclaim

```yaml pem-family
id: DS-001
kind: DISCOVERY
state: CURRENT
maturity: SUPPORTED
temperature: UNASSESSED
summary: A self-contained synthetic semantic fixture matrix can remain green while failing to discriminate real-owner semantic defects; qualification evidence must stay bounded to the property its method actually tests, while assembled prose adequacy requires independent semantic Review.
semantic_identity:
  invariant_or_claim: Passing a synthetic model of a semantic rule does not by itself establish that the canonical prose authority is adequate or that all material counterexamples are represented.
  owner_class: qualification epistemology and independent Review
  mechanism_family: proxy fixture or phrase oracle overclaims arbitrary prose-semantic conformance
  applicability_dimensions: protocol qualification, prose authority, synthetic fixtures, semantic Review, claim-method alignment
aggregation_scope: Protocol 6.4 Review defects plus frozen Protocol 6.5 frontier diagnostic evidence concerning qualification/Review scope
coverage_state: PARTIAL
coverage_basis: Bounded to accepted Protocol 6.4 Review evidence and the frozen Protocol 6.5 diagnostic that independently identified the same proxy-proof mechanism class.
applicability:
  - semantic qualification
  - synthetic fixture oracle
  - phrase pin
  - independent Review
  - claim-method alignment
authority_binding: EVIDENCE_ONLY
binding_health: HEALTHY
guidance_level: OBSERVED
relations: []
evidence:
  - "hjin98/scientific-software-development-protocol@55c085261eb827e3047637d045a8e6917ea6b962:qualification/ssdp6/INDEPENDENT-REVIEW-2026-09-15-PROTOCOL-6.4-31818-NO-PASS.md"
  - "hjin98/scientific-software-development-protocol@81375d8142a8130b80cd82f2304d3e16bc3fc390:qualification/ssdp65/reviewer-a/PHASE-II-FALSIFICATION.md"
```

## Current notices

No current notices are admitted in this initial bounded backfill.

## Coverage note

This reconciliation intentionally favors defensible evidence binding over broad historical recall. The later 6.3 bootstrap defect is a second confirmed mechanism occurrence but is not counted as schema-qualified recurrence because the historical repair-acceptance representation predates the current structured `recurrence_basis` contract. `reconciled_through` is an accepted-state identity horizon, not proof of exhaustive history. Current 6.5 candidate implementation evidence may inform future closeout learning but does not self-ratify a success pattern before acceptance.