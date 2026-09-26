# Protocol 6.5 Frontier-Model Re-evaluation — Historical Evidence Directory

This directory preserves the non-normative investigation, qualification, Review, and release evidence for the Protocol 6.5 cycle. It is historical evidence, not a mutable release-state owner.

Protocol 6.5.0 is now accepted-current. The authoritative current/candidate/public/recovery identities are owned only by [`PROTOCOL-RELEASE-STATE.yaml`](../../PROTOCOL-RELEASE-STATE.yaml).

## Release outcome

The accepted semantic candidate is exact immutable:

`P21 = 7f7b5e24858e813e45ace867a7f8ea5180f43bf0`

The completed release chain is:

- independent assembled-candidate Review PASS: `INDEPENDENT-REVIEW-2026-09-25-PROTOCOL-6.5-P21-PASS.md`;
- explicit stakeholder ratification: `STAKEHOLDER-RATIFICATION-2026-09-25-PROTOCOL-6.5-P21.md`;
- exact-P21 public-source fallback publication;
- distinct recovery target/publication: `PROTOCOL-6.5-P21-RECOVERY-TARGET.md`;
- accepted-current cutover and closeout: `PROTOCOL-6.5-RELEASE-CLOSEOUT.md`.

Earlier P1-P20 candidates, NO-PASS records, repair qualifications, freeze/binding records, and handoffs remain immutable historical evidence for how the final P21 candidate was reached. Their entering-state statements must not be read as current release state.

## Governing workplans

The three Protocol 6.5 workplans are complete and archived under `workplans/archive/`:

- `SSDP-6.5-FRONTIER-MODEL-RE-EVALUATION.md`;
- `SSDP-6.5-D3-D4-IMPLEMENTATION-HANDOFF.md`;
- `SSDP-6.5-IMPORTANCE-WEIGHTED-ATTENTION-AND-PROPORTIONAL-RIGOR.md`.

Protocol 7 remains separately governed. The Protocol 6.5 closeout added only its inheritance-reconciliation revision; it did not authorize Protocol 7 D4 or mutate Protocol 7 D3 architecture.

## Key historical evidence

| Path | Status | Content |
| --- | --- | --- |
| `P0-BASELINE-BINDING-PROTOCOL-6.4.md` | frozen | exact Protocol 6.4 control and baseline acceptance realization |
| `BENCHMARK-AND-EVALUATION-DESIGN.md` | frozen historical design | P0/candidate dimensions, holdouts, and evidence-class corrections |
| `reviewer-a/` | frozen diagnostic evidence | frontier-model reconstruction, falsification, defect model, and mutation probe |
| `CROSS-MODEL-ADJUDICATION-2026-09-24.md` | complete | cross-model adjudication of the initial diagnostic findings |
| `PHASE-IV-V-DESIGN-CLOSURE.md` | PASS | principle extraction, D3 architecture, and implementation boundary |
| `PROTOCOL-6.4-TO-6.5-PRESERVATION-MAP.md` | complete evidence | preservation trace for core doctrine and historical capabilities |
| `INDEPENDENT-REVIEW-HANDOFF-PROTOCOL-6.5.md` | historical handoff | entering-state handoff for the final P21 independent Review |
| `PROTOCOL-6.5-RELEASE-CLOSEOUT.md` | accepted-current closeout | final lifecycle identities and closeout state |

The clean branch `ssdp-6.5-frontier-model-independent-review-b` remains only as an unused reserved surface for any future replication; it was not counted as completed qualification evidence for this release.

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
