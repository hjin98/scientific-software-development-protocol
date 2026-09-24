# Protocol 6.5 Frontier-Model Re-evaluation — Evidence Directory

Non-normative investigation evidence for `workplans/active/SSDP-6.5-FRONTIER-MODEL-RE-EVALUATION.md`. Nothing here is Protocol authority. The accepted-current protocol remains Protocol 6.4.

## Files

| Path | Visibility to independent reviewer B | Content |
| --- | --- | --- |
| `P0-BASELINE-BINDING-PROTOCOL-6.4.md` | shared | frozen control identities, canonical-source classification, baseline acceptance realization |
| `BENCHMARK-AND-EVALUATION-DESIGN.md` | shared | pre-registered dimensions, acceptance criteria, benchmark partitions, trial protocol, limitations |
| `INDEPENDENT-DIAGNOSTIC-HANDOFF.md` | shared | instructions and contamination rules for reviewer B |
| `reviewer-a/` | **sealed from reviewer B until reviewer B's findings are committed** | reviewer A's Phase I–III diagnostic artifacts, tools and evidence |
| `reviewer-b/` | created by reviewer B | reviewer B's independent Phase I–III artifacts |
| `CROSS-EXAMINATION.md` | created after both finding sets are frozen | intersection / symmetric-difference analysis |

## Reproducing reviewer A's executed probe

```bash
python -m venv .venv && . .venv/bin/activate
pip install -r source/requirements-validation.txt ./orchestrator -r orchestrator/requirements-dev.txt
python qualification/ssdp65/reviewer-a/tools/mutation_probe.py \
  --repo . --base 55c085261eb827e3047637d045a8e6917ea6b962 \
  --work /tmp/ssdp65-mutation --python "$(which python)" \
  --json /tmp/ssdp65-mutation/results.json
```

The probe creates and removes disposable Git worktrees under `--work`; it never edits the checked-out tree.
