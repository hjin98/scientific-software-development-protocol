---
kind: independent-assembled-candidate-review
status: no-pass
protocol_version: 6.4.0
target_protocol_version: 6.5.0
p0: 55c085261eb827e3047637d045a8e6917ea6b962
candidate_ref: f7874aa1fcaef04429fe4725d3ba20e570f9326d
semantic_ref: f7874aa1fcaef04429fe4725d3ba20e570f9326d
binding_descendant: 21689d27793ebe12cfecce0af74849abf5654461
readiness_descendant: c1c7ce128562b5570380764d0ce4fe0d9cbff023
exact_candidate_run: 36157280206
binding_run: 36157584333
readiness_run: 36157808134
serious_challenge: none
blocking_findings:
  - B65-P16-1
stakeholder_ratification: not_authorized
date: 2026-09-25
---

# Fresh Independent Assembled-Candidate Review — Protocol 6.5 P16

## Disposition

**NO-PASS.**

Exact immutable P16 `f7874aa1fcaef04429fe4725d3ba20e570f9326d` was reviewed against accepted
Protocol 6.4 control `55c085261eb827e3047637d045a8e6917ea6b962`. The binding/readiness descendants were
used only for lifecycle and mechanical evidence.

**SERIOUS CHALLENGE: NONE.** Accepted Protocol 6.5 D3 is coherent and implementable.

One genuine D4 blocker survived fresh holdout falsification:

**B65-P16-1 — accepted-current cutover can launder an incompletely validated prior candidate.**

P16 correctly repaired canonical accepted-current -> historical projection. However, on accepted-current advancement,
`validate_release_transition` checked only predecessor candidate version, PASS/RATIFIED labels, SHA-shaped
public/recovery refs, and mapping agreement. Full evidence subject/disposition realization and recovery-lineage
validation were performed only for the current candidate snapshot.

A fresh holdout used a fully shaped predecessor whose Review/ratification labels were PASS/RATIFIED but whose evidence
could bind the wrong subjects, then advanced accepted-current while simultaneously rolling the current candidate to a
new successor. The transition validator returned no error because the malformed promotion source was no longer the
current candidate inspected by `validate_release_state`.

Required repair: during accepted-current advancement, fully revalidate the exact predecessor candidate closure using
the existing evidence/publication/recovery validators and exact canonical predecessor boundary. Keep D3 closed and add
no parallel state machinery.

P16 remains immutable. This Review authorizes no stakeholder ratification, publication, recovery, accepted-current
cutover, PR merge, or Protocol 7 D3/D4 mutation.
