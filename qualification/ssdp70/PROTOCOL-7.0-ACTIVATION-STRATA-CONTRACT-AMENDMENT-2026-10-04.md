---
kind: qualification-contract-amendment
governing_protocol_version: 6.6.0
target_protocol_version: 7.0.0
date_utc: 2026-10-04
amends: qualification/ssdp70/PROTOCOL-7.0-EVALUATION-AND-QUALIFICATION-CONTRACT.md
revision: 2
status: revision 2 drafted; fresh independent check required (contract) together with fresh independent workplan Review (overlay)
---

# Activation-strata amendment to the Protocol 7.0 qualification contract (revision 2)

## 1. Authority and status

- **Stakeholder decision.** `STAKEHOLDER-DECISION-2026-10-04-PROTOCOL-7.0-DETERMINISTIC-ACTIVATION-AND-ACTIVATION-QUALIFICATION.md` §§1 and 5. The binding words are: "Our main focus should be that standard command activation alwasy activates. If that works, we don't necessarily need the plain-word version, and it can simply be regarded as unreliable." Recorder derivations D1–D4 are listed in that record's §5 and are labelled as derivations wherever they are used here.
- **Workplan.** The governed overlay "Current stakeholder activation decision and governed overlay (2026-10-04)" in the active workplan's §0.1. It supersedes ordinary-entry requirements in §§8.3, 11.3, 11.5, 13 and 14 on entry mode only, and needs its own fresh independent Review.
- **Revision 1** (commit `d370193`) received an independent NO-PASS (`ACTIVATION-STRATA-AMENDMENT-INDEPENDENT-CHECK-2026-10-04.md`). The same context that authored revision 1 authored this revision, so it cannot accept it.

## 2. Evidence
- **Stage 7 measured activation, not doctrine.** The executor loaded an SSDP root in 13/122 p70 runs. 42/43 p70 critical failures came from runs with no root loaded (`STAGE-7-M07-DELEGATE-REQUEST-AND-TREATMENT-DELIVERY-DIAGNOSIS-2026-10-04.md`).
- **Ordinary selection depends on model and framing.** It was 2/10 on Flash and 4/10 on GLM-5.3, and copy/relay/delegate framings never triggered catalog consultation (`STAGE-7-SELECTION-STRONGER-EXECUTOR-PROBE-RESULT-2026-10-04.md`).
- **Delivery and conformity are distinct.** With delivery, delegate-request conformity was 6–10/25 (`STAGE-7-M07-DOCTRINE-LOADED-PROBE-RESULT-2026-10-04.md`).
- **Runtime command activation is mode-dependent** (`STAGE-7-RUNTIME-COMMAND-ACTIVATION-PROBE-RESULT-2026-10-04.md`):
  - Claude Code print mode and OMP RPC mode expand the command;
  - OMP print mode, which the Stage 7 adapter uses, and Codex `exec` do not.

## 3. Contract changes in revision 2

| Section | Change |
|---|---|
| §1 item 4 | `root_selection` carries the stratum, the mechanism and the **delivery record** (runtime expansion event or injection record, with entrypoint hash, delivered bytes and a position before the first model request). |
| §1 item 12 | Rewritten.<br>• **Mechanisms.** Deterministic entry is realized by `runtime-command` (only where expansion is demonstrated for that exact mode) or by `harness-injection` (reproducing the runtime's demonstrated delivery, with wrapper bytes recorded; it supports a delivery claim, not a claim that "this runtime's user command works").<br>• **Delivery proof.** Each run needs per-run proof; a model-initiated read never counts. A missing or late record makes the run inadmissible **and** fails the profile's activation criterion, with no rerun rescue.<br>• **Ordinary entry.** Unreliable, no floor. `ordinary-read`, `instructed-read` and no-selection are reported separately.<br>• **Run-type strata.** Assigned for every run type.<br>• **Scoring scope.** Floors apply only to deterministic runs. Ordinary runs are reported with every critical failure listed. The owner false activation rule applies everywhere.<br>• **Profile coverage.** At least one flash-class profile must be among those offered; each profile stands alone. The mechanism is in the profile key. |
| §3 | Order: harness/admissibility → **deterministic activation** → critical → floors → … A new first row requires 100% delivery per profile. The proposed ordinary floor is withdrawn. |
| §4 | **Selection routes:** S01–S11/H01–H05 are report-only (derivation D3).<br>**T1/T7/T8:**<br>• activation is deterministic;<br>• active bytes = delivered entrypoint + wrapper bytes;<br>• a later re-read counts as an additional read;<br>• the 6.5/6.6 denominators use the same mechanism. |
| §5 | Every inadmissible run and its replacement are recorded with both identities. |
| §6 | Canary-skill demonstration for `runtime-command`. Delivery-format check for `harness-injection`. Known-broken probes: withheld entrypoint, passthrough command with model read, late delivery record, hash mismatch. |
| §8 | Records revision 2 and the pending checks. |

## 4. Response to the revision-1 independent check

| Finding | Disposition |
|---|---|
| **SC-1** — the workplan requires ordinary entry (§8.3, §11.3, §11.5, §13 criterion 13, §14) | Answered by a governed workplan overlay (§0.1) with inline supersession markers at each bound location, following the 2026-09-28 fixed-cost overlay precedent. It needs a fresh independent workplan Review. |
| **B1** — "fully accountable" ordinary runs vs deterministic-only floors; "doctrine measures" undefined; a wrong root drops out | All floors are deterministic-only, and ordinary runs are report-only. The undefined term is removed. On deterministic runs the root is predeclared, and a delivery record for any other root is a hash mismatch, so the run is inadmissible and the activation criterion fails. |
| **B2** — mislabelled mechanism undetectable; no per-run delivery proof | Per-run delivery record with hash and pre-first-request position (§1 items 4 and 12). A model read never counts. §6 known-broken probes cover passthrough-plus-read, late record and hash mismatch. |
| **B3** — PROPOSED floor not fail-closed | Withdrawn. Ordinary entry has no floor, by stakeholder decision §5 (2b). |
| **B4** — `instructed-read` could satisfy the floor | No ordinary floor remains. `instructed-read` is reported separately and can never count as deterministic (§6 probe). |
| **M1** — injection placement and wrapper; stratum vs profile key; claim scope; T1/T7/T8 bytes | Injection reproduces the runtime's demonstrated delivery; for OMP that is the RPC-mode `custom` message format. The mechanism is in the profile key, and stratum and mechanism are in run identity. The claim scope is stated. Byte rules are stated in §4. |
| **M2** — new classes not required; "at least one flash-class" vs the per-profile rule | The ordinary report must cover the new classes (workplan overlay item 4). Profile coverage: each offered profile stands alone, and at least one must be flash-class. |
| **M3** — derivations credited to the stakeholder | The decision record §5 separates stakeholder words (2a, 2b) from derivations D1–D4, and this record labels each use. |
| **M4** — run types without a stratum | Every run type is assigned in §1 item 12. |
| **M5** — exposure feasibility | Deterministic runs alone must meet the §2 minimums. Fresh fixtures are required, since the Stage 7 set is development data. |
| **Minor** — order vs table placement | The order and the first table row now agree. |
| **Minor** — cross-route cites an untracked closeout record and a wildcard path | The overlay names the closeout record as not yet committed and cites the exact corrigendum directory. |
| **Minor** — replacement runs unrecorded | §5 record rule added. |

## 5. Questions for the fresh independent check
1. Does the workplan overlay validly supersede the frozen §8.3 bullet and §13 criterion 13 on entry mode, under the 2026-09-28 precedent? Or does it change acceptance criteria in a way that needs more than an overlay?
2. Is derivation D3 (6.6 ordinary-selection preservation becomes report-only) within the stakeholder's words, or must it wait for explicit confirmation before any run?
3. Is per-run delivery proof achievable and tamper-evident with the existing observer and normalizer design? In particular, can OMP RPC-mode expansion events or harness injection be linked into the normalized stream before the first model request?
4. Is "every critical failure listed" for ordinary runs enough visibility, given that ordinary usage is unsupported?
5. Is there any remaining way to pass a floor without delivered doctrine, or to fail one because of an undelivered entrypoint?

## 6. Still blocked until both checks pass
- adapter/harness changes (OMP RPC mode or injection, delivery records);
- profile freezes;
- the §6 pre-run check;
- fresh fixtures;
- any qualification run.
