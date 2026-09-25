---
kind: ssdp65-p17-repair-qualification
status: repair-complete-candidate-frozen
protocol_version: 6.4.0
target_protocol_version: 6.5.0
p0: 55c085261eb827e3047637d045a8e6917ea6b962
failed_p16: f7874aa1fcaef04429fe4725d3ba20e570f9326d
p17: feca003e577fdfa2ae4219e0df2a2cdb38e5d757
exact_p17_pr_run: 36167091971
date: 2026-09-25
d3_reopened: false
serious_challenge: none
---

# Protocol 6.5 P17 Cutover-Promotion Closure Qualification

P17 is the immutable replacement semantic candidate:

`feca003e577fdfa2ae4219e0df2a2cdb38e5d757`

Exact-P17 workflow `36167091971` passed the complete repository build and Orchestrator Core jobs.

## Repaired blocker

P17 closes B65-P16-1 at the existing D4 release-state transition owner. Accepted-current advancement now revalidates
the complete exact predecessor release-state snapshot, including exact Review and ratification evidence realization,
candidate/public identity, recovery target state, and canonical recovery/publication ancestry.

The predecessor's exact material-boundary commit is preserved by transition-history discovery and used as the
publication endpoint for predecessor lifecycle evidence. This prevents a later successor candidate or merge-descendant
`HEAD` from laundering an invalid promotion source.

The repair additionally requires the predecessor public fallback to equal its exact semantic candidate during
advancement and adds focused regression coverage for predecessor revalidation, exact-boundary propagation, and
public/semantic mismatch.

No D1, D2, or D3 authority changed. No new state owner, registry, topology service, compatibility layer, or control
plane was introduced.

P17 requires a later lifecycle binding at Review `NOT_RUN`, mechanical binding qualification, and a fresh independent
assembled-candidate Review before any stakeholder ratification or release publication.
