---
kind: ssdp65-p2-freeze-binding
status: frozen-candidate-bound
protocol_version: 6.4.0
target_protocol_version: 6.5.0
p0: 55c085261eb827e3047637d045a8e6917ea6b962
failed_p1: b565e28aeacea002cefe27e6b9594fe99d653c0a
p2: e8edb353e172aef933ed5e58eeabe897d0cc98d1
p2_pr_qualification_run: 35996488794
review_state: NOT_RUN
ratification_state: NOT_REQUESTED
public_source_ref: UNAVAILABLE
recovery_ref: UNAVAILABLE
---

# Protocol 6.5 P2 Freeze Binding

## Exact identities

- P0 accepted control: `55c085261eb827e3047637d045a8e6917ea6b962`.
- Failed immutable P1: `b565e28aeacea002cefe27e6b9594fe99d653c0a`.
- Replacement immutable P2: `e8edb353e172aef933ed5e58eeabe897d0cc98d1`.
- Exact-P2 ordinary PR qualification: run `35996488794`.

P2 contains the D4 repairs for B65-R1 through B65-R3 and the inherited sibling lifecycle-phase oracle discovered during repair. P2 itself does not self-name.

## Lifecycle boundary

This descendant binds P2 after P2 already exists immutably.

```text
P2: FROZEN / MECHANICALLY QUALIFIED
INDEPENDENT ASSEMBLED-CANDIDATE REVIEW: NOT RUN
STAKEHOLDER RATIFICATION: NOT REQUESTED
PROTOCOL 6.5 PUBLIC FALLBACK: UNAVAILABLE
PROTOCOL 6.5 RECOVERY: UNAVAILABLE
ACCEPTED CURRENT: Protocol 6.4
PROTOCOL 7 D3/D4: UNCHANGED
```

P1 NO-PASS evidence remains immutable historical evidence and is not overwritten or transferred.

Any material semantic mutation after P2 creates another candidate identity and invalidates P2-specific Review/qualification applicability.
