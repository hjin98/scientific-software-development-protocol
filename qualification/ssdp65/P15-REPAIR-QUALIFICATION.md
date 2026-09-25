---
kind: ssdp65-p15-repair-qualification
status: repair-complete-candidate-frozen
protocol_version: 6.4.0
target_protocol_version: 6.5.0
p0: 55c085261eb827e3047637d045a8e6917ea6b962
failed_p14: d792f219ad361b6acb2663833beec1c179ea5793
p15: 4fced41c4d8cc7af02938334f7cd1d0b587c408a
exact_p15_pr_run: 36138585609
date: 2026-09-25
d3_reopened: false
serious_challenge: none
p14_review: qualification/ssdp65/INDEPENDENT-REVIEW-2026-09-25-PROTOCOL-6.5-P14-NO-PASS.md
---

# Protocol 6.5 P15 Final Stabilization Qualification

P15 is the immutable replacement semantic candidate:

`4fced41c4d8cc7af02938334f7cd1d0b587c408a`

Exact-P15 workflow `36138585609` passed the complete build and Orchestrator Core jobs.

This stabilization closes the bounded D4 evidence-realization family in one coherent repair:

- movable branch/tag/revision aliases cannot become HEALTHY local durable evidence;
- exact immutable object identity remains the local durable binding basis;
- replacement/graft resistance and raw-parent canonical ancestry remain intact;
- evidence paths must resolve to Git blob/file artifacts;
- repository evidence paths use repository-relative POSIX syntax;
- missing canonical parent/tree/blob/path objects remain fail-closed;
- readable alternate/promisor-backed objects remain supported;
- canonical patch-ID behavior remains replacement-independent;
- PEM YAML readers reject duplicate mapping keys;
- orphan canonical family/notice blocks cannot hide outside canonical headings;
- exactly one active-summary marker pair is permitted.

Fresh holdouts cover branch and tag retargeting, movable repair-acceptance evidence, directory/tree evidence paths,
backslash path ambiguity, duplicate root/family/repair-acceptance keys, orphan canonical blocks, and duplicate summary
markers.

Two prospective stabilization commits were not frozen because regression exposed compatibility overreach. Those were
reconciled without weakening the protected semantics. Exact P15 then passed the full normal workflow.

P15 remains immutable. Any later semantic mutation requires a new candidate identity. This record is mechanical
qualification only; it is not independent Review PASS, stakeholder ratification, publication, recovery establishment,
accepted-current cutover, PR merge, or Protocol 7 mutation.
