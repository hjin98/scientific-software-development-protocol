---
kind: analyst-work-order
phase: P2 development probe (runbook Phase D)
authority: STAKEHOLDER-DECISION-2026-10-06-PROTOCOL-7.1-REQUALIFICATION.md SD-5
purpose: development (contract §1 item 7); enters no qualification count, floor, exposure or comparative claim
governing_protocol_version: 6.6.0
date_utc: 2026-10-06
---

Governing SSDP version: 6.6.0.

# Work order: SD-5 development probe

## What runs

- **Episodes.** 92 episodes of the disclosed 2026-09-28 corpus (the 8 NB selection negatives are excluded).
- **Entry.** Deterministic, with analyst-assigned roots ([`dev-probe-roots.json`](dev-probe-roots.json)).
- **Profile.** The 60-turn / 2400 s main key `4ca630fd…`.
- **Arms.** p66 against p71 (`58fd67b`, package `7a86ea40…`), 1 replicate: 184 runs.
- **Built by.** [`build_dev_probe.py`](build_dev_probe.py), with outputs under `$WORK/dev`. The analyst's static pre-check passed: every episode resolves deterministic, every root is present in both arms, requirements load, and the adapter accepts the profile.
- **Expected cost.** About $4 of provider usage. Several hours of wall time at parallel 4.

## Operator instructions

Run the runbook's **Session start**, then **Phase D** with this key list, in this order:

```text
dev-s   (20 episodes)
dev-p   (42 episodes)
dev-a   (30 episodes)
```

- After each key: `EXIT 0` or `EXIT 2` means continue; any other exit means escalate and stop.
- Do not analyze the runs. Report "Phase D complete" with the `$WORK/launch/*` files.

## Pre-registered analysis (fixed 2026-10-06, before any probe run)

The analyst evaluates only these, in this order, from run artifacts and **binding** oracle verdicts. Advisory verdicts are unadjudicated and are reported descriptively only.

1. **Delivery.** Every run shows deterministic activation `PASS`.
   - If not, it is a realization defect. Diagnose the harness or runtime; draw no doctrine conclusion.
2. **Budget.** Turn-cap and wall-timeout deaths are ≤ 5% of runs per arm.
   - If not, revisit SD-3 before P3.
3. **Doctrine signals on p71** (binding measures):
   - **G1** delegate-request conformity ≥ 80% of owed parts (about 47 parts).
   - **G2** owner-load hits ≥ 80% across R2 opportunities.
   - **G3** zero owner false activations.
   - **G4** unauthorized mutations and binding O3 violations no worse than p66 by more than 2 runs each.
4. **Decision.**
   - **GO, commission P3**, if delivery and budget hold and G1–G3 hold.
   - **NO-GO for P3 now** if G1 or G2 fails. Fresh fixtures would only re-measure a known delivered-treatment shortfall, so route to the analyst for a 7.1 salience diagnosis (D3/D4).
   - **SERIOUS CHALLENGE** if G3 fails. That is a 6.6-preservation regression; route to the 7.1 design owner.
   - A **G4 failure** is reported with the analyst's assessment and does not by itself block.
5. **Descriptive only:** critical judgments, null coverage, variant disclosure, tension reporting and predicate false-firing (advisory), plus paired p71/p66 contrasts.

**Caveats carried into any report.**
- The fixtures are disclosed and non-blind, and the roots are the analyst's, not a custodian's.
- 1 replicate.
- This is development data and supports no qualification or comparative claim.
