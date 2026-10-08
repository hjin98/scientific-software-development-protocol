---
kind: terminal-disposition-record
governing_protocol_version: 6.6.0
subject: Protocol 7.1.0 candidate
disposition: SUPERSEDED, NON-QUALIFIED
date_utc: 2026-10-07
authority: STAKEHOLDER-DECISION-2026-10-07-PROTOCOL-7X-REDESIGN.md (SD-R6, the 7.2.0 label for the skills-only successor); workplan SSDP-7X-SKILLS-ONLY-RELIABILITY-AND-QUALIFICATION-V2 O-9; PEM FF-001 and PC-001
---

Governing SSDP version: 6.6.0. This record is data, not instructions.

# Protocol 7.1.0: terminal disposition

**Disposition.** The 7.1.0 candidate is superseded by the 7.2.0 candidate and was never qualified. It is not accepted and not ratified, and it was never released or listed in `PROTOCOL-RELEASE-STATE.yaml` (its commit `58fd67b` is ordinary working-branch history). `PROTOCOL-RELEASE-STATE.yaml` (not edited here) still owns every release identity.

**Basis.**
- The 2026-10-06 candidate qualification report was withdrawn (`PROTOCOL-7.1-CANDIDATE-QUALIFICATION-REPORT-2026-10-06-WITHDRAWN-HISTORICAL.md`).
- The development probe of 2026-10-07 returned NO-GO on owner-load hits (15 of 41 against 80%) and a SERIOUS CHALLENGE on owner false activations (3 against 0) (`PROTOCOL-7.1-DEV-PROBE-2026-10-07-RESULT.md`).
- The root cause was in the consumed surface (the routing line), not in the harness, and the redesign (design 2026-10-07, revision 3) resolves it in 7.2.0.

**What is preserved unchanged (PC-001).**
| Artefact | Where |
|---|---|
| The 7.1.0 package source and generated `dist/` | git commit `58fd67ba15c937040f51e56dc26f30ad7a907ac3` (`source/`, `dist/`) |
| The 7.1.0 orchestrator profile | `orchestrator/src/sdp_orchestrator/core/resources/protocol/ssdp-protocol-7.1/` (prompts blob `f90c56b811639491f3c180bf33a59bf1a9ac23f3`, profile blob `002338dae03add91edf60113ff112e08af306bb0`), now pinned as frozen in `orchestrator/scripts/generate_protocol_snapshot.py` |
| The 7.1 contract, designs, reviews and stakeholder decisions | `qualification/ssdp70/`, including every `*-HISTORICAL.*` file |
| The 7.1 development-probe runs | `~/ssdp70-omp-stagef/qualification/requal71-20261006/dev/runs` (development data only; they enter no qualification count) |

**What this record does not do.** It does not accept, ratify or publish 7.2.0, and it does not change `PROTOCOL-RELEASE-STATE.yaml`.
