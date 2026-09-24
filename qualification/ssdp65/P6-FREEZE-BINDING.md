---
kind: ssdp65-p6-freeze-binding
status: frozen-candidate-bound
protocol_version: 6.4.0
target_protocol_version: 6.5.0
p0: 55c085261eb827e3047637d045a8e6917ea6b962
failed_p1: b565e28aeacea002cefe27e6b9594fe99d653c0a
failed_p2: e8edb353e172aef933ed5e58eeabe897d0cc98d1
failed_p3: 89ccc71a7b0e9458a3e77306be2a773d4059f0f2
failed_p4: 43ff4273fbdaf46b9677cffdb091b741ce754a7d
failed_p5: d2d672a3e814438fb618f901137f88c8698a205d
p6: dd06da8136416e67644586c44880b466f982b8ff
p6_pr_qualification_run: 36051369390
review_state: NOT_RUN
ratification_state: NOT_REQUESTED
public_source_ref: UNAVAILABLE
recovery_ref: UNAVAILABLE
---

# Protocol 6.5 P6 Freeze Binding

## Exact identities

- P0 accepted control: `55c085261eb827e3047637d045a8e6917ea6b962`.
- Failed immutable P1: `b565e28aeacea002cefe27e6b9594fe99d653c0a`.
- Failed immutable P2: `e8edb353e172aef933ed5e58eeabe897d0cc98d1`.
- Failed immutable P3: `89ccc71a7b0e9458a3e77306be2a773d4059f0f2`.
- Failed immutable P4: `43ff4273fbdaf46b9677cffdb091b741ce754a7d`.
- Failed immutable P5: `d2d672a3e814438fb618f901137f88c8698a205d`.
- Replacement immutable candidate P6: `dd06da8136416e67644586c44880b466f982b8ff`.
- Exact-P6 ordinary PR qualification: run `36051369390`.

P6 contains the bounded D4 repairs for B65-P5-1 and B65-P5-2. P6 itself does not self-name as current mutable candidate.

## Lifecycle boundary

P6: FROZEN / MECHANICALLY QUALIFIED  
INDEPENDENT ASSEMBLED-CANDIDATE REVIEW: NOT RUN  
STAKEHOLDER RATIFICATION: NOT REQUESTED  
PROTOCOL 6.5 PUBLIC FALLBACK: UNAVAILABLE  
PROTOCOL 6.5 RECOVERY: UNAVAILABLE  
ACCEPTED CURRENT: Protocol 6.4  
PROTOCOL 7 D3/D4: UNCHANGED

P1-P5 NO-PASS evidence remains immutable historical evidence and is not transferred.

Any material semantic mutation after P6 creates another candidate identity and invalidates P6-specific Review/qualification applicability.
