---
kind: ssdp65-p14-repair-qualification
status: repair-complete-candidate-frozen
protocol_version: 6.4.0
target_protocol_version: 6.5.0
p0: 55c085261eb827e3047637d045a8e6917ea6b962
failed_p13: 05a2b62550adadf271a27f6555da7173902c491c
p14: d792f219ad361b6acb2663833beec1c179ea5793
exact_p14_pr_run: 36133381631
date: 2026-09-25
d3_reopened: false
serious_challenge: none
p13_review: qualification/ssdp65/INDEPENDENT-REVIEW-2026-09-25-PROTOCOL-6.5-P13-NO-PASS.md
---

# Protocol 6.5 P14 Repair Qualification

## Scope and identity

This record qualifies the bounded D4 repair ordered by the fresh independent P13 Review.

- accepted control P0: `55c085261eb827e3047637d045a8e6917ea6b962`
- immutable failed P13: `05a2b62550adadf271a27f6555da7173902c491c`
- immutable replacement P14: `d792f219ad361b6acb2663833beec1c179ea5793`
- exact-P14 normal workflow: `36133381631`

Accepted Protocol 6.5 D3 was not reopened and no Serious Challenge was raised.

## B65-P13-1 closure

Canonical local-Git semantics are now consolidated in `source/canonical_git.py`.

Both release-state and PEM validators derive ancestry from raw commit-parent objects with replacement refs disabled.
PEM immutable object/content reads also disable replacement objects, while ancestry no longer delegates to
overlay-sensitive `merge-base --is-ancestor`.

The repair covers:

- accepted/base PEM containment;
- authority/evidence binding;
- repair-acceptance containment;
- recurrence chronology;
- immutable evidence path/locator reads;
- patch-id independence evidence from canonical parent/tree diffs.

Fresh real-Git tests reject replace-ref and graft-rewritten sibling ancestry, preserve canonical evidence bytes under a
replacement ref, reject an overlay at a repair-acceptance consumer, preserve patch-id under replacement objects, and
retain readable alternate object-store behavior.

## Mechanical evidence

Exact-P14 run `36133381631` passed:

- repository release-state validation;
- project engineering memory validation;
- complete protocol regression;
- canonical skill-package build;
- independent generated-package validation;
- committed distribution parity;
- whitespace validation;
- Protocol 6.5 snapshot parity;
- complete Orchestrator Core acceptance.

## Candidate boundary

P14 is frozen at `d792f219ad361b6acb2663833beec1c179ea5793`.

Any semantic mutation creates another candidate identity. Later descendants may carry lifecycle/qualification evidence
only.

This record is mechanical repair qualification, not independent semantic Review PASS, stakeholder ratification,
publication, recovery establishment, accepted-current cutover, PR merge, or Protocol 7 mutation.
