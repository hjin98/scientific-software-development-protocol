---
memory_schema_version: 1
maintained_under_protocol: 6.3.0
project_id: hjin98-scientific-software-development-protocol
repository: hjin98/scientific-software-development-protocol
scope: repository
coverage_state: PARTIAL
coverage_basis: "Bounded bootstrap from accepted Protocol 6.2 qualification/requalification, independent Review, frozen-profile evidence, and the accepted 6.2 recovery lineage. Earlier project history and unrelated development episodes are not claimed exhaustive."
reconciled_through: b59adc77efe6951912cfd705cc43830c58ca27d0
accepted_base: "Protocol 6.2 accepted recovery b59adc77efe6951912cfd705cc43830c58ca27d0; no prior accepted PEM exists because 6.3 introduces PEM."
candidate_overlay: "ssdp-6.3-engineering-memory candidate overlay; publication identity is the containing Git commit and is not self-declared accepted."
detail_files: []
---

# Project Engineering Memory

This is the Scientific Software Development Protocol (SSDP) repository's project-local engineering memory. It records evidence-backed lessons that may improve future engineering decisions, but it is not D1-D4 semantic authority. Current protocol/project/external owners define what must be true. Because this first backfill is deliberately partial, absence here does not establish that no relevant historical lesson exists.

## Active summary

<!-- BEGIN DERIVED PEM SUMMARY -->
| ID | Kind | Temperature | Maturity/state | Binding | Guidance | Current evidence | Bounded lesson |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FF-001 | FAILURE_FAMILY | UNASSESSED | SUPPORTED/CURRENT | EVIDENCE_ONLY/HEALTHY | OBSERVED | 1 confirmed | Publishing an immutable public-source fallback before the source state contains all required repaired routes can freeze a semantically stale bootstrap even when the branch later becomes correct. |
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
temperature: UNASSESSED
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
authority_owner: source/shared/references/protocol-versioning-and-compatibility.md
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

## Current notices

No current notices are admitted in this initial bounded backfill.

## Coverage note

This initial self-hosting publication intentionally favors defensible evidence binding over broad historical recall. It does not convert examples from the Protocol 6.3 workplan into facts, does not infer recurrence from commit chronology, and does not treat `reconciled_through` as a claim of exhaustive coverage. Future material SSDP work should perform bounded historical intake when a relevant decision cannot be closed from these current families alone.