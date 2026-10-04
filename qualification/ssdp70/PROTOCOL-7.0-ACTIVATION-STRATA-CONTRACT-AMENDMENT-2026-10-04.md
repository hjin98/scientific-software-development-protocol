---
kind: qualification-contract-amendment
governing_protocol_version: 6.6.0
target_protocol_version: 7.0.0
date_utc: 2026-10-04
amends: qualification/ssdp70/PROTOCOL-7.0-EVALUATION-AND-QUALIFICATION-CONTRACT.md
status: drafted; stakeholder floor value open; fresh independent check required
---

# Activation-strata amendment to the Protocol 7.0 qualification contract

## 1. Authority and status

- **Authority.** `STAKEHOLDER-DECISION-2026-10-04-PROTOCOL-7.0-DETERMINISTIC-ACTIVATION-AND-ACTIVATION-QUALIFICATION.md`. In it the stakeholder decided that:
  - activation is a qualification target, especially on lighter models;
  - users activate skills with deterministic commands, because wording is unreliable.
- **Governing process.** This is a governed contract change under contract §8.
- **Authorship and acceptance.** The context that authored the Stage 7 diagnosis and probes authored it, so it cannot accept it. **A fresh independent check of these exact bytes is required** before any harness change, profile freeze or run relies on them.
- **Open stakeholder decision.** The ordinary-entry activation floor (§3 row) is marked PROPOSED.

## 2. Why

1. **Stage 7 measured activation, not doctrine.** The executor (GLM-5.3-Flash) loaded an SSDP root in only 13/122 p70 runs. All 50 delegate-request opportunities and 42 of p70's 43 critical failures came from runs where no root was loaded (`STAGE-7-M07-DELEGATE-REQUEST-AND-TREATMENT-DELIVERY-DIAGNOSIS-2026-10-04.md`).
2. **The scoring did not separate delivery.** The contract and scoring manifest had no stratum that keeps doctrine scoring to runs where the doctrine was delivered. Workplan §11.3 *Route* calls non-selection a placement miss, but nothing in the contract realized that.
3. **Ordinary selection depends on the model and the task framing.** A stronger model in the same family selected 4/10 against Flash's 2/10. Both selected only when they chose to consult the catalog, and copy/relay/delegate framings never triggered that (`STAGE-7-SELECTION-STRONGER-EXECUTOR-PROBE-RESULT-2026-10-04.md`).
4. **Delivered doctrine is a separate question.** With the doctrine delivered, delegate-request conformity rose from about 0 to 6–10 of 25 owed parts but stayed far below the floor (`STAGE-7-M07-DOCTRINE-LOADED-PROBE-RESULT-2026-10-04.md`). Delivery and conformity therefore need separate strata.
5. **The existing "explicit" realization is wording.** The T1/T7/T8 prefix "Use the software-implementation skill." is a prose instruction. OMP headless mode passes even its `/skill:<name>` command through as literal text (decision record §3), so a command is deterministic only where the runtime is shown to execute it.

## 3. Changes (contract sections)

| Section | Change |
|---|---|
| §1 item 4 | `root_selection` records the entry stratum and the activation mechanism: `runtime-command`, `harness-injection`, `instructed-read` or `ordinary-read`. |
| §1 item 12 (new) | **Entry strata.** *Deterministic entry* is the supported usage and requires 100% activation; a miss is an inadmissible adapter defect. It is realized only by a runtime command demonstrated to load the skill, or by injection of the exact installed entrypoint bytes. *Ordinary entry* is the fallback, scored as activation; prose instructions count as ordinary. Matched arms share stratum and mechanism. Doctrine floors apply only where the doctrine was delivered. Activated ordinary runs are fully accountable. |
| §3 order and scope | **Activation** is inserted after the absolute floors. The absolute floors and the comparative claim are evaluated on the deterministic stratum, which must meet every §2 exposure minimum on its own. |
| §3 new row | **Activation (ordinary entry), PROPOSED:**<br>• ⌈0.8 n⌉ of n ≥ 20 SSDP-applicable ordinary episodes per profile select an admissible root before their first consequential step;<br>• candidate at least paired 6.6 minus 2;<br>• negative-case bounds unchanged;<br>• must pass on at least one flash-class profile, and a stronger profile cannot rescue a light-profile failure. |
| §4 selection routes | S01–S11 and H01–H05 are ordinary-entry runs; their bounds are unchanged. |
| §4 T1/T7/T8 | D4 activation is deterministic. The historical prose prefix is ordinary instructed entry and no longer an admissible realization of this panel. |
| §6 | The pre-run checker demonstrates, per stratum, that:<br>• a withheld deterministic entrypoint is rejected;<br>• the recorded mechanism matches what reached the subject;<br>• for `runtime-command`, the runtime itself loads the skill. |
| §8 | Records this drafted revision and the fresh-check requirement. |

**Unchanged:**
- every numeric floor other than the new row;
- custody (including the non-executor attestation amendment);
- the human trial;
- burden metrics. The whole installed `SKILL.md` already counts as active bytes, and an injected entrypoint is counted the same way.

## 4. Interaction with the workplan

- **§8.3 reopen trigger, "Selection or placement miss".** It names, in order, a specialist entrypoint carrying the predicate and then kernel placement as the next candidates for ordinary-task misses due to non-selection. The stakeholder's decision makes deterministic activation the supported usage instead. Ordinary-entry misses are now a measured activation shortfall against the new row, which feeds the reopen trigger only when that row fails.
- **Whether that preemption is valid.** Whether the decision legitimately replaces the trigger's candidate order, or whether the trigger must also be amended, is for the independent check. It may need a governed workplan change.
- **Cross-route.** The workplan's current-state section routes to this record.
- **§11.3 *Route*.** "placement-miss rule for non-selection" is unchanged, and §1 item 12 realizes it.

## 5. Proposed floor: rationale (for the stakeholder)

- **Basis.** ⌈0.8 n⌉ matches the per-class owner-load floor discrimination already in §4. At n = 20 it rejects a true activation rate of 0.5 with high probability.
- **Comparator.** Paired 6.6 minus 2 reuses the existing selection-route allowance.
- **Expected outcome.** Stage 7's Flash rate (about 11%) would fail by a wide margin. That is the intended outcome given the stakeholder's statement that lighter models tend to ignore skills.
- **Alternatives.** The stakeholder may fix a different value. Alternatively the ordinary stratum can be report-only, with no floor, if deterministic activation is meant to be the only qualified path.

## 6. Independent-check request

The checker should try to falsify at least the following:
1. Whether item 12's delivery rule could let a candidate pass doctrine floors while users following ordinary usage get no protection, given the stakeholder's statement that deterministic activation is required.
2. Whether `harness-injection` is equivalent enough to a runtime skill command for qualification. Points to examine: placement in context, system vs user role, and the effect on the T1/T7/T8 byte metric and comparability with 6.5 runs.
3. Whether excluding non-activated ordinary runs from doctrine floors hides critical failures that the protected outcome needs counted.
4. Whether the workplan §8.3 reopen-trigger interaction needs a governed workplan amendment.
5. Whether the §6 additions are enough to detect a mislabelled mechanism, such as an `instructed-read` recorded as deterministic.
6. Whether the exposure minimums remain feasible when the deterministic stratum alone must meet them.

## 7. What remains blocked until the check passes
- Adapter and harness support for the deterministic stratum: OMP injection, since its headless mode does not execute skill commands.
- New profile freezes and the §6 pre-run check.
- Fresh fixtures: the Stage 7 set is now development data.
- Any qualification run.
