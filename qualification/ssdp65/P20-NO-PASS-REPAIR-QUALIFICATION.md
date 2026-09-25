---
kind: blocking-repair-qualification
status: implementation-complete-awaiting-exact-candidate-ci
protocol_version: 6.4.0
target_protocol_version: 6.5.0
source_review: qualification/ssdp65/INDEPENDENT-REVIEW-2026-09-25-PROTOCOL-6.5-P20-NO-PASS.md
blocking_finding: B65-P20-1
superseded_candidate: 142eb22376270af6155657dcbf150112f3871cb2
repair_owner: source/release_state.py
serious_challenge: none
preservation_review: pass
stakeholder_ratification: not_authorized
date: 2026-09-25
---

# Protocol 6.5 P20 NO-PASS Repair Qualification

## Scope

This is the bounded D4 repair for B65-P20-1. The independent preservation pass found no lost core doctrine or historical
capability. D1-D3 and the proportional-rigor doctrine remain closed.

## Repair

The existing release-state transition logic now factors its protected project/schema/historical/accepted-current
continuity checks into one reusable primitive.

A merge that exactly inherits one parent's release-state snapshot no longer treats every differing sibling as if that
sibling independently executed the inherited accepted-current promotion. Instead:

- the inheriting parent remains the transition lineage;
- differing owner-present siblings must preserve protected historical mappings and cannot be newer than the inherited
  accepted-current state;
- each sibling's own ancestry still receives ordinary full transition validation, including P20's exact-parent
  repository-backed predecessor realization;
- a novel merge resolution matching no parent still receives full transition validation.

The nearest-predecessor walk follows the same distinction, so a stale sibling is not returned as a false promotion
predecessor after a normal inherited-state merge.

No new release owner, topology service, replay engine, merge registry, evidence database, compatibility state plane, or
lifecycle role was added.

## Regression

Three focused merge-topology regressions cover the repaired family:

1. valid accepted-current promotion + stale unrelated sibling + merge retaining the promoted snapshot must pass;
2. an illegal protected-history transition inside the stale sibling must still be rejected recursively;
3. a merge that retains an older accepted-current snapshot while another sibling has already advanced must fail closed.

Existing tests continue to cover hidden promotion-source evidence realization, multiple legal transitions, owner
deletion/reintroduction, protected-history rewrite, synthetic merges, canonical Git behavior, missing objects, and
exact-predecessor validation.

## Lifecycle

The contents commit containing this record and the code/test repair is the replacement semantic candidate once its exact
identity is known. It requires exact-candidate mechanical qualification before any binding descendant is created.

No stakeholder ratification, publication, recovery, accepted-current cutover, PR #33 merge, or Protocol 7 mutation is
authorized.
