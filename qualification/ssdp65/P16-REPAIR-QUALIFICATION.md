---
kind: ssdp65-p16-repair-qualification
status: repair-complete-candidate-frozen
protocol_version: 6.4.0
target_protocol_version: 6.5.0
p0: 55c085261eb827e3047637d045a8e6917ea6b962
superseded_ratified_p15: 4fced41c4d8cc7af02938334f7cd1d0b587c408a
p16: f7874aa1fcaef04429fe4725d3ba20e570f9326d
exact_p16_pr_run: 36157280206
date: 2026-09-25
d3_reopened: false
serious_challenge: none
---

# Protocol 6.5 P16 Release-Cutover Validator Repair Qualification

P16 is the immutable replacement semantic candidate:

`f7874aa1fcaef04429fe4725d3ba20e570f9326d`

Exact-P16 workflow `36157280206` passed the complete repository build and Orchestrator Core jobs.

## Defect discovered after P15 ratification

During the first authorized release-cutover preparation after stakeholder ratification of P15, a phase-independent
transition test exposed a genuine D4 defect in `source/release_state.py`.

The accepted-current advancement validator compared the new historical record directly with the former
`accepted_current` mapping. Those representations intentionally differ:

```yaml
accepted_current:
  version: "6.4.0"
  public_source_ref: <sha>
  recovery_ref: <sha>

historical:
  "6.4.0":
    public_source_ref: <sha>
    recovery_ref: <sha>
```

A schema-correct cutover therefore failed the transition check unless the historical record redundantly carried a
`version` field. The old unit oracle had hidden that mismatch by copying the complete accepted-current mapping into
the synthetic historical record.

## P16 repair

P16 changes only the existing D4 release-state transition owner and directly affected tests:

- project the former accepted-current state to the canonical historical payload
  `{public_source_ref, recovery_ref}` before equality comparison;
- retain exact previous-version key transfer and immutable mapping equality;
- reject missing, mutated, or redundant-version history transfer;
- separate the live repository-state integration fixture from neutral validator unit-test state;
- split the former monolithic cutover oracle into focused transition cases;
- remove temporary diagnostic CI instrumentation.

No D1, D2, or D3 authority changed. No new state owner, compatibility layer, release registry, or control plane was
introduced.

P15, its independent Review PASS, and its explicit stakeholder ratification remain immutable historical evidence.
They do not apply to P16 because P16 changes semantic D4 behavior.

P16 requires a later lifecycle binding at Review `NOT_RUN`, fresh independent assembled-candidate Review, and new
stakeholder ratification before publication/recovery/cutover.
