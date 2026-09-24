# Protocol 6.5 Frontier-Model Re-evaluation — Evidence Directory

Non-normative investigation/design evidence for `workplans/active/SSDP-6.5-FRONTIER-MODEL-RE-EVALUATION.md`. Nothing in this directory is accepted Protocol 6.5 authority. Accepted-current remains Protocol 6.4 until final Review, explicit stakeholder ratification, publication/recovery and cutover complete.

## Current evidence chain

| Path | Status | Content |
| --- | --- | --- |
| `P0-BASELINE-BINDING-PROTOCOL-6.4.md` | frozen | exact Protocol 6.4 control and baseline acceptance realization |
| `BENCHMARK-AND-EVALUATION-DESIGN.md` | preregistered + dated benchmark repairs | P0/P1 dimensions, holdouts, evidence-class corrections |
| `reviewer-a/` | frozen at diagnostic commit | Opus 5.5 Phase I-III reconstruction, falsification, defect model, mutation probe |
| `CROSS-MODEL-ADJUDICATION-2026-09-24.md` | complete | Opus findings cross-checked against GPT-5.6 Sol history/current P0 and narrowed to four defect families |
| `PHASE-IV-V-DESIGN-CLOSURE.md` | **PASS** | P65-1..P65-6 principle extraction, D3 architecture and implementation boundary |
| `INDEPENDENT-DIAGNOSTIC-HANDOFF.md` | reserved | original clean second-frontier handoff; waived for this cycle but retained for future replication |

The clean branch `ssdp-6.5-frontier-model-independent-review-b` remains reserved for a later genuinely independent frontier replication. It is not treated as completed evidence in the current cycle.

## Current execution authority

Implementation is governed by:

`workplans/active/SSDP-6.5-D3-D4-IMPLEMENTATION-HANDOFF.md`

P1 has not yet been frozen. No 6.5 public fallback, recovery, Review PASS or stakeholder ratification exists yet.

## Reproducing reviewer A's P0 mutation probe

```bash
python -m venv .venv && . .venv/bin/activate
pip install -r source/requirements-validation.txt ./orchestrator -r orchestrator/requirements-dev.txt
python qualification/ssdp65/reviewer-a/tools/mutation_probe.py \
  --repo . --base 55c085261eb827e3047637d045a8e6917ea6b962 \
  --work /tmp/ssdp65-mutation --python "$(which python)" \
  --json /tmp/ssdp65-mutation/results.json
```

The probe creates/removes disposable worktrees under `--work`; it does not edit the checked-out tree.
