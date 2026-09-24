---
kind: ssdp65-p7-freeze-binding
status: frozen-candidate-ready-for-binding
protocol_version: 6.4.0
target_protocol_version: 6.5.0
p0: 55c085261eb827e3047637d045a8e6917ea6b962
failed_p6: dd06da8136416e67644586c44880b466f982b8ff
p7: 133c747a1f9ab4372c9e1af7a7e9666316dc892b
p7_pr_qualification_run: 36058860629
review_state: NOT_RUN
ratification_state: NOT_REQUESTED
public_source_ref: UNAVAILABLE
recovery_ref: UNAVAILABLE
---

# Protocol 6.5 P7 Freeze Binding

P7 is the immutable replacement semantic candidate:

`133c747a1f9ab4372c9e1af7a7e9666316dc892b`

Exact-P7 ordinary PR qualification run `36058860629` passed the complete build and Orchestrator Core jobs.

P6 remains immutable and failed Review. The descendant containing this record binds the already-existing P7 identity in the sole mutable release-state owner with Review reset to `NOT_RUN`. It does not perform stakeholder ratification, publication, recovery establishment, accepted-current cutover, PR merge, or Protocol 7 mutation.

Any material semantic mutation after P7 requires a new candidate identity and affected requalification.
