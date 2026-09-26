# Protocol 6.6 Historical Qualification and Release Evidence

This directory preserves non-normative design, qualification, Review, ratification, recovery, and release evidence for the completed Protocol 6.6 cognitive/operational optimization cycle. Protocol 6.6.0 is accepted-current; mutable release identities resolve only from [`PROTOCOL-RELEASE-STATE.yaml`](../../PROTOCOL-RELEASE-STATE.yaml). The governing workplan is archived at `workplans/archive/SSDP-6.6-COGNITIVE-OPERATIONAL-OPTIMIZATION.md`.

| Path | Content |
| --- | --- |
| `PROTOCOL-6.6-EVALUATION-AND-QUALIFICATION-CONTRACT.md` | cold evaluation/qualification contract (loaded for Stage A/F/G and evidence-adequacy Review) |
| `STAGE-A-BASELINE-AND-PRESERVATION.md` | frozen baselines, PEM basis + HAS, capability-preservation map, evaluation freeze |
| `STAGE-F-G-EVALUATION-AND-QUALIFICATION.md` | structural + live comparison, acceptance reconciliation, findings for Review; section 10 holds the current implementation-Review rework state |
| `REWORK-R0-FREEZE.md` | rework R0: fresh version-bound holdout, ordinary burden route, entry/burden oracle and pass rules frozen before the R1 repair |
| `D3-REOPEN-QUALIFICATION-FREEZE.md` | D3 reopen (workplan 16.10): fresh ordinary route T8, strict version gate, and the burden decision rule frozen before the redesigned candidate ran; harness evidence repairs |
| `FINAL-SIMPLIFICATION-FREEZE.md` | final whole-entrypoint simplification (workplan 16.11): routing-preservation map (`eval/routing-preservation-map.yaml`), ordering-oracle identity exemption, and the final qualification rule, frozen before any entrypoint change or candidate run |
| `eval/` | removable harness (`harness.py`, `run_matrix.py`), frozen scenarios, fixtures, hidden oracles, rubrics, and reduced run records |
| `FINAL-SIMPLIFICATION-EVIDENCE-CORRECTION.md` | post-Review correction of the non-discriminating selection differential and designed `error_max_turns` termination classification; no semantic mutation or rerun |
| `FINAL-CANDIDATE-FREEZE-BINDING.md` | immutable Protocol 6.6 semantic candidate binding and entering Review/ratification/publication lifecycle state |
| `INDEPENDENT-REVIEW-HANDOFF-PROTOCOL-6.6.md` | fresh assembled-candidate Review entrypoint for immutable semantic candidate `22f4bdba53795da3a6f13f162529f3a843fc37ae` after final live qualification and normal PR CI |

| `INDEPENDENT-REVIEW-2026-09-26-PROTOCOL-6.6-PASS.md` | fresh assembled-candidate Review PASS for exact P66 |
| `STAKEHOLDER-RATIFICATION-2026-09-26-PROTOCOL-6.6.md` | explicit stakeholder ratification |
| `PROTOCOL-6.6-RECOVERY-TARGET.md` | distinct immutable recovery target selected after public-source publication |
| `PROTOCOL-6.6-RELEASE-CLOSEOUT.md` | accepted-current release closeout and lifecycle identities |
