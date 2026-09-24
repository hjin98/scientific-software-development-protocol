---
kind: ssdp65-p4-freeze-binding
status: frozen-candidate-bound
protocol_version: 6.4.0
target_protocol_version: 6.5.0
p0: 55c085261eb827e3047637d045a8e6917ea6b962
failed_p1: b565e28aeacea002cefe27e6b9594fe99d653c0a
failed_p2: e8edb353e172aef933ed5e58eeabe897d0cc98d1
failed_p3: 89ccc71a7b0e9458a3e77306be2a773d4059f0f2
p4: 43ff4273fbdaf46b9677cffdb091b741ce754a7d
p4_pr_qualification_run: 36041360949
review_state: NOT_RUN
ratification_state: NOT_REQUESTED
public_source_ref: UNAVAILABLE
recovery_ref: UNAVAILABLE
---

# Protocol 6.5 P4 Freeze Binding

## Exact identities

- P0 accepted control: `55c085261eb827e3047637d045a8e6917ea6b962`.
- Failed immutable P1: `b565e28aeacea002cefe27e6b9594fe99d653c0a`.
- Failed immutable P2: `e8edb353e172aef933ed5e58eeabe897d0cc98d1`.
- Failed immutable P3: `89ccc71a7b0e9458a3e77306be2a773d4059f0f2`.
- Replacement immutable P4: `43ff4273fbdaf46b9677cffdb091b741ce754a7d`.
- Exact-P4 ordinary PR qualification: run `36041360949`.

P4 contains the D4/current-representation repairs for the two P3 Review blockers. P4 itself does not self-name as current mutable candidate.

## Lifecycle boundary

This descendant binds P4 after P4 already exists immutably.

```text
P4: FROZEN / MECHANICALLY QUALIFIED
INDEPENDENT ASSEMBLED-CANDIDATE REVIEW: NOT RUN
STAKEHOLDER RATIFICATION: NOT REQUESTED
PROTOCOL 6.5 PUBLIC FALLBACK: UNAVAILABLE
PROTOCOL 6.5 RECOVERY: UNAVAILABLE
ACCEPTED CURRENT: Protocol 6.4
PROTOCOL 7 D3/D4: UNCHANGED
```

P1-P3 NO-PASS evidence remains immutable historical evidence and is not transferred.

Any material semantic mutation after P4 creates another candidate identity and invalidates P4-specific Review/qualification applicability.
