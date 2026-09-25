---
kind: independent-assembled-candidate-review
status: no-pass
protocol_version: 6.5.0
candidate_ref: 142eb22376270af6155657dcbf150112f3871cb2
accepted_control_p0: 55c085261eb827e3047637d045a8e6917ea6b962
serious_challenge: none
blocking_findings:
  - B65-P20-1
preservation_review: pass
date: 2026-09-25
---

# Protocol 6.5 P20 Independent Review — NO-PASS

## Disposition

Exact P20 `142eb22376270af6155657dcbf150112f3871cb2` is **NO-PASS**. No Serious Challenge survives.

The separate preservation pass is **PASS**: accepted D1-D4 doctrine, Protocol 5 engineering safeguards, Protocol 6.0-6.4
improvements, frozen historical resources, PEM semantics, active simplicity, proportional-rigor doctrine, and Protocol 7
isolation remain preserved. No D1-D3 reopen is justified.

## B65-P20-1 — merge-parent transition overreach

The D4 release-state history walker treats every owner-present merge parent whose state differs from the merge child as
if that parent independently executed the child's accepted-current advancement.

A legitimate topology therefore fails:

`governed A -> stale unrelated sibling F(A)`

while the release lineage independently completes:

`A -> reviewed/ratified/public/recovery promotion source -> accepted-current B`

and a later merge `B + F(A) -> B` retains B's release-state snapshot.

The merge does not promote from F. F is a stale but valid sibling. Full `validate_release_transition(F, B)` nevertheless
requires F itself to contain B's immediately previous candidate Review/ratification/publication/recovery state, falsely
rejecting the merge.

The same false predecessor interpretation is present in final nearest-boundary collection, which can return the stale
sibling as an independent transition predecessor even when the merge exactly inherits another parent's release state.

## Required repair

Keep the existing release-state owner, canonical Git traversal, full transition validator, and P20 exact-parent
repository-backed validation.

For a merge that exactly inherits the release-state snapshot of at least one parent:

- follow the inheriting parent lineage as the transition lineage;
- treat differing owner-present siblings as merge-compatibility inputs, not independent promotion transitions;
- preserve sibling historical mappings and prevent accepted-current rollback;
- continue recursively validating each sibling's own ancestry so an illegal transition inside that lineage cannot be
  hidden by the merge.

A novel merge resolution matching no parent remains subject to full transition scrutiny.

Focused regression must include:

1. valid promotion lineage + stale unrelated sibling + merge retaining promoted state => PASS;
2. the same shape with an actually illegal transition inside the sibling lineage => reject;
3. merge retaining an older accepted state while a sibling is newer => reject.

Do not add a topology service, replay engine, merge registry, compatibility state plane, or lifecycle role.

## Lifecycle boundary

P20 remains immutable failed Review evidence. This review does not ratify, publish, establish recovery, advance
accepted-current, merge PR #33, or mutate Protocol 7.
