---
kind: candidate-identity-freeze-record
governing_protocol_version: 6.6.0
subject: Protocol 7.2.0 candidate (non-governing)
date_utc: 2026-10-07
authority: workplan SSDP-7X-SKILLS-ONLY-RELIABILITY-AND-QUALIFICATION-V2 O-9 and S3 gate; PEM FF-001 and PC-001; independent Review INDEPENDENT-D4-PROTOCOL-7X-S1-S3-REVIEW-2026-10-07.md (PASS after the delta check); stakeholder decisions SD-R6, SD-R12 to SD-R15
status: frozen as an offline D4 candidate identity; NOT qualified, NOT accepted, NOT ratified, NOT published
---

Governing SSDP version: 6.6.0. This record is data, not instructions.

# Protocol 7.2.0 candidate: frozen identity

**What is frozen.** The semantic content of commit `2dedcfa3408f62bc11a696ac3776183a87b40438` on `ssdp-7.0-scientific-epistemic-closure`, namely `source/`, `dist/` and the orchestrator 7.2 profile resources. Any later commit that changes any of them is a new candidate identity and needs a fresh independent Review (PEM FF-001). Verify with `git diff 2dedcfa HEAD -- source dist orchestrator/src` (empty while this identity stands).

| Identity | Value |
|---|---|
| Commit | `2dedcfa3408f62bc11a696ac3776183a87b40438` |
| `source/` git tree | `70c453e3f92551d0b20c267ba2054127b0a9ef0c` |
| `dist/skills/` git tree | `334f2640d3322b66fa140322e828d1f60b56dede` |
| `source/PROTOCOL_VERSION` | `7.2.0` |
| Orchestrator profile `ssdp-protocol-7.2` | prompts blob `f90c56b811639491f3c180bf33a59bf1a9ac23f3`, profile blob `5db36c8344c93d2fa98737e6ccdb18b6414888b6` |
| Frozen 7.1 profile (pinned in `generate_protocol_snapshot.py`) | prompts blob `f90c56b811639491f3c180bf33a59bf1a9ac23f3`, profile blob `002338dae03add91edf60113ff112e08af306bb0` |

| Skill | `dist/skills/<name>` git tree | Zip sha256 (first 16) | `SKILL.md` bytes |
|---|---|---|---|
| scientific-formulation | `148cba129b185b7b949ca8b93506e6c37431727b` | `2929ae7c3a02c1cd` | 16,512 |
| numerical-algorithm-design | `a8e6d9b2aab73d547faf9647fd90f1db9a14f8d4` | `a5a5bdf37e16256d` | 16,754 |
| software-design | `4e9f303364570f8aeef09198bf80ea3c2a6a030d` | `cb728ec9c2423575` | 17,905 |
| software-implementation | `381baba79d3aa10175df9fb6b70eec3cf55079cc` | `34d978d439978ee0` | 15,799 |
| software-documentation | `ed579eea5c0dc754ceb6869785c757e768e068b4` | `e0aee788078e014e` | 11,591 |
| software-maintenance-audit | `7251c077020f04acc442efaf2c6a74556b5e4e2b` | `66edb0f0fdc77ec6` | 9,842 |
| repository-hygiene | `0649462288659715579635c60ddfa02453642fba` | `7e9d3a10c08eb529` | 7,370 |

**Evidence behind the freeze.**
- S1: independent mapping check PASS after repairs (`INDEPENDENT-D4-PROTOCOL-7X-S1-MAPPING-CHECK-2026-10-07.md`); block sizes 97.7-104.1% of the 7.1 blocks, excess attributed (SD-R13).
- S2: consolidated harness; development-probe regression pinned; budget floor 10,364 / 4,672 lines (SD-R14, SD-R15b).
- S3: version boundary; Q5c static pre-measurement with no static breach (409 B headroom entrypoint-only); the independent S1-S3 Review returned PASS WITH GAPS, then PASS on the delta check (`INDEPENDENT-D4-PROTOCOL-7X-S1-S3-REVIEW-2026-10-07.md`, section 9).
- Repository acceptance on the frozen commit: `tests/` 429 OK, orchestrator core 384 OK, snapshot `--check`, package validation and committed-`dist/` parity.

**What this freeze does not claim.**
- No qualification campaign has been run. A later PASS would claim only improvement over accepted 6.6 on the gating flash executor and corpus at the stated operating characteristics.
- Not accepted and not ratified: `PROTOCOL-RELEASE-STATE.yaml` (stakeholder-owned, unchanged) lists no 7.2 candidate. Acceptance needs qualification, an independent assembled-candidate Review and explicit stakeholder ratification.
- 7.1.0 stays superseded and non-qualified (`PROTOCOL-7.1-DISPOSITION-RECORD-2026-10-07.md`).

**Entry conditions for S4 and a campaign** (SD-R15a and the Review's open items):
1. Custodian-authored O-8 inputs: the 40-item evaluator calibration set (at least 10 known failures), oracle known-good and known-bad fixtures, and the version-redacted evaluator input.
2. Re-freeze the evaluator profile with a model that is not the executor's, and the executor profile (it still pins the retired `package_ledger.py` and `package_premise.py`).
3. X6 is governed by SD-R16: S4 measures the T1/T8 owner-read rate q (at most 6% proceed, 6-15% back to the stakeholder, above 15% a surface-wording problem); the D4 entrypoint may not grow without the stakeholder's prior approval; shell-counted and native bytes are reported separately. The stakeholder receives the unconditional compound probability (including P(Q5c pass) from S4) before any campaign run.
4. Deferred harness items from the Review: matched-mode comparison and error-kind flag in H4; the family flag's pooled rate; package fingerprints in the evaluator copy; the shell-counted share of each run's bytes reported by S4.
