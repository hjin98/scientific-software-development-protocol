---
kind: qualification-campaign-plan
governing_protocol_version: 6.6.0
target_protocol_version: 7.1.0 (candidate; non-governing)
date_utc: 2026-10-06
authority: qualification contract revision 16 (PROTOCOL-7.0-EVALUATION-AND-QUALIFICATION-CONTRACT.md); this plan adds no threshold, floor, exposure minimum or budget
status: SD-1..SD-7 adopted 2026-10-06 (STAKEHOLDER-DECISION-2026-10-06-PROTOCOL-7.1-REQUALIFICATION.md); P1 done; P2 work order ready (requal71/DEV-PROBE-WORK-ORDER.md); P3 awaits the P2 go/no-go
supersedes: CAMPAIGN-MATRIX-PLAN-PROTOCOL-7.1.md
---

Governing SSDP version: 6.6.0.

# Protocol 7.1 requalification plan

## 0. Why this plan exists and what it changes

The 2026-10-06 matrix was not a qualification campaign; see [`PROTOCOL-7.1-DEVELOPMENT-MATRIX-2026-10-06-RECORD.md`](PROTOCOL-7.1-DEVELOPMENT-MATRIX-2026-10-06-RECORD.md).

**The qualification machinery already exists, and it already enforces the contract.**
- The harness supports deterministic entry (`entry: pinned:<root>` on a `runtime-command` key).
- `--mode qualification` refuses to launch without a frozen family and accounting manifest and an ADMITTED executor admission.
- `core70.validate_family` enforces the 60/8/3-turn panel schedule, RPC `runtime-command` keys and the complete criterion map.
- `assess70.py` is the blinded evaluator.

**The failure was that a single operator bypassed all of it** (`--mode probe`), reused a disclosed corpus, and replaced the evaluator with a script. Nothing mechanical stopped them.

This plan therefore changes **who decides what**. The single mechanical operator becomes a bounded role:
- every operator step has a machine-decided gate, and the operator never makes judgments;
- every judgment sits with a named role, and the independence-bearing roles stay independent.

**Mechanical layer:** [`eval/requal71.py`](eval/requal71.py), with its tests in [`eval/test_requal71.py`](eval/test_requal71.py).

Each 2026-10-06 blocker now maps to a gate that stops it:

| Blocker | Gate that now stops it |
|---|---|
| B1 probe or development purpose | `matrix-plan` emits only `--mode qualification` commands; `audit` flags any run whose purpose, mode or admission is wrong |
| B2 disclosed fixtures | `corpus-check` freshness against [`requal71/disclosed-material.json`](requal71/disclosed-material.json) (9 disclosed corpus roots, 7 distinct manifests; byte level). The pre-run checker judges semantic reuse. |
| B3 no strata or roots | `corpus-check` requires a `panel`, plus `pinned:<root>` on deterministic panels and `ordinary` with `admissible_roots` on the ordinary panel; `campaign-build` refuses a stratum or panel disagreement |
| B4 30-turn budget | `derive-key` and `family-build` take turn caps only from the frozen schedule; `corpus-check` refuses any other `max_turns` |
| B5 no evaluator | `audit --assessments` requires an `assessment-identity.json` bound to the run and to an admitted evaluator |
| B6 post-hoc omission | `audit` refuses undeclared directories, duplicates and missing slots; outputs are never overwritten; there is no subset path |
| B7 stratum-blind scoring | Custodian deliverable C-4 ([work package](PROTOCOL-7.1-REQUALIFICATION-CUSTODIAN-WORK-PACKAGE.md)), consumed only through the frozen family record |
| B8 custody log | `custody-stat` and `custody-compare` run around every non-operator role session (§3 P3/P5/P9), with the access log append-only and outside the freeze list |
| B9 pre-run check scope | §5 lists the checker's mandatory scope |

## 1. Subject and comparators

- **Candidate.** Package `7a86ea4011034f8abf793c1c06d523577356a5b1a7167b267dda53e567a2892e`. It is byte-identical at every commit from `58fd67b` (the last change to `dist/skills`) through `ee3a2b5`; that was verified by extraction on 2026-10-06. Which commit to bind is SD-1.
- **Comparators** (`requal71.ARMS_BY_KEY`):
  - p66 `22f4bdba…` (package `e6d960a8…`) on every key.
  - p65 `7f7b5e24…` (package `7d61d8b7…`) on the burden key only, because the §4 backstop is "≤ 2.0 × fresh paired accepted-6.5 median".
- **p70 is not an arm.** 7.0 is closed NON-QUALIFIED and is not a contract comparator.
- **Arm packages** are extracted from immutable refs (`requal71 prepare-arms`), never taken from the live `dist/`.

## 2. Role boundary

The operating rule: **the operator turns frozen inputs into frozen outputs with tools whose verdict is binary. Everything else is a judgment, and every judgment belongs to a named role above the operator.** Note that "light model" and "independent role" are different axes. The custodian, pre-run checker and evaluator need independence from the candidate author *and* real capability, so they are neither the analyst nor the operator.

| Role | Who | Does | Never does |
|---|---|---|---|
| **Stakeholder** | the user | Decides SD-1..SD-7; accepts or rejects the final result | — |
| **Analyst** | capable model (this session's role) | Maintains this plan, `requal71.py` and its tests, the parameter file and tool pins. Answers every escalation packet. Decides predeclared rerun or replacement questions only where the contract allows them. Writes the result record. | Edits a frozen artifact after its gate; authors fixtures, keys or oracles; finalizes an admission; scores items; runs scored realizations by hand |
| **Operator** | lighter model | Executes [the runbook](PROTOCOL-7.1-REQUALIFICATION-OPERATOR-RUNBOOK.md) step by step. Runs only printed commands; saves every verdict; on any non-PASS, writes an escalation packet and stops. | Chooses a value, edits any input or tool, reruns, subsets, skips, retries, reads `keys/`, `authoring/` or `human-trial/` content, interprets a result, writes conclusions, commits |
| **Fixture custodian** | capable model, separate context; not the candidate author; does not interpret results | Builds the fresh custody store and corpus, keys, oracles, the stratum-aware aggregate oracle and the preservation-panel import ([work package](PROTOCOL-7.1-REQUALIFICATION-CUSTODIAN-WORK-PACKAGE.md)) | Sees candidate-arm results before scoring; touches the frozen store after its freeze |
| **Independent pre-run checker** | capable model, separate context from custodian, author and analyst | §5 scope; reports counts and pass/fail only. Finalizes executor admissions from the operator-produced evidence. | Authors fixtures or tools under check |
| **Evaluator** | admitted evaluator profile run by `assess70.py` / `batch_assess70.py` (the operator launches it) | Disposes of advisory and unresolved items blind to arm | — |
| **Executor** | GLM-5.3-Flash under OMP (the system under test) | — | — |

**Tool pins (analyst duty).** After any change to a pinned file, the analyst regenerates the pins from the repository root, re-runs `test_requal71`, and only then hands the operator a work order:

```bash
sha256sum qualification/ssdp70/eval/{requal71,test_requal71,core70,harness70,assess70,batch_assess70,prepare_arms70}.py \
  qualification/ssdp70/eval/adapters/{omp,omp_eval}.py qualification/ssdp70/requal71/{operator-lib.sh,campaign-parameters.env,disclosed-material.json,prior-campaigns.json} \
  qualification/ssdp70/PROTOCOL-7.1-REQUALIFICATION-{OPERATOR-RUNBOOK,PLAN}.md > qualification/ssdp70/requal71/tool-pins.sha256
```

**Escalation classes**, which the operator never resolves:
- **INTEGRITY** (a frozen identity, purpose or declaration mismatch). The analyst stops the campaign; a fix needs a new campaign record and is never a patch.
- **ESCALATE** (a run not `COMPLETE_ADMISSIBLE`, a failed deterministic activation, a missing or invalid assessment). The analyst applies the contract:
  - an undelivered deterministic run fails the profile, with no rescue;
  - a rerun only through a slot declared before launch (§6 G-2);
  - otherwise the criterion stays non-PASS.
- **TOOL** (a usage or I/O error). The analyst fixes the tool or the parameters, re-pins, and the operator restarts the step.

## 3. Phases and gates

| Phase | Owner | Output | Gate (machine verdict) | Then |
|---|---|---|---|---|
| P0 Record correction | analyst | Development record, withdrawn report preserved, plan banner, lineage, denylist | done 2026-10-06 | — |
| P1 Decisions | stakeholder | SD-1..SD-7 recorded; analyst fills `requal71/campaign-parameters.env` and re-pins tools | runbook session start R0 (`need`, pins verify, unit tests green) | P2 or P3 |
| P2 *(optional, SD-5)* Development probe | operator → analyst | Development-purpose deterministic run on the disclosed corpus with the analyst's root overlay | runbook Phase D | go/no-go on P3 |
| P3 Fresh custody and corpus | custodian (operator snapshots around the session) | New store; deliverables C-1..C-6 | `custody-compare` before/after; `corpus-check` PASS | P4 |
| P4 Arms, keys, family, manifest | operator | `arms.json`; 4 key profiles; `family.json`; `accounting-manifest.json` | `prepare-arms`, `derive-key` ×4, `family-build`, `campaign-build` all PASS | P5 |
| P5 Admissions | operator runs the evidence; checker finalizes | ADMITTED executor bundle per key; re-admitted evaluator | executor bundles validate in `verify-launch` (P6); the evaluator bundle is validated by the checker at P6 and again by `assess70.py` itself at P9 | P6 |
| P6 Pre-run check | independent checker | Counts/pass-fail report (§5) | report verdict PASS, then `verify-launch` PASS | P7 |
| P7 Freeze and launch | operator | Run trees per key | `matrix-plan` PASS; every printed command exits; `audit` PASS | P8 |
| P8 Escalations | analyst | Written disposition of each packet | no open packet | P9 |
| P9 Evaluation | operator launches the evaluator | `assessment.json` + `assessment-identity.json` per run | `audit --assessments` PASS | P10 |
| P10 Aggregate | operator runs the custodian's C-4 oracle on the **complete** manifest | Oracle result | runbook P10: the C-4 oracle refuses omitted runs (exit 3) | P11 |
| P11 Human trial | stakeholder and participants under `human-trial/PROTOCOL.md` | Trial result | the trial's own protocol | P12 |
| P12 Result record | analyst → stakeholder | Qualification result record (stratum- and key-labelled) | stakeholder decision | — |

**Critical path.**
- Run cost is small: the 2026-10-06 matrix was 300 runs, 81M tokens and $5.78.
- The cost sits in **P3 fixture authoring** and in **P5 admissions** for four keys plus the evaluator. On 2026-10-06 the evaluator admission of 2026-10-04 no longer validates (profile key and core digest changed), and no executor bundle has ever been ADMITTED.
- The checker may judge which invariant admission evidence (containment, custody) applies across keys that differ only in budget or mechanism. That is an evidence-applicability judgment, not an operator shortcut.

## 4. Stakeholder decisions (adopted 2026-10-06 as recommended; record: `STAKEHOLDER-DECISION-2026-10-06-PROTOCOL-7.1-REQUALIFICATION.md`)

| # | Decision | Recommendation | Blocks |
|---|---|---|---|
| SD-1 | Candidate identity to bind (commit + package) | Package `7a86ea40…` at commit `58fd67b` (first commit carrying it; identical through `ee3a2b5`) | P4 |
| SD-2 | Custody arrangement for the fresh store, so that `custody_denial` can PASS | (b) Contract §1 item 9 attestation path from day one: access log outside the freeze list, `custody-stat` before and after every role session, written role attestations. Alternative (a): `sudo operator/custody-lock.sh` with a dedicated uid, which gives technical denial and a cleaner audit if you can run sudo. | P3, P5 |
| SD-3 | Wall-clock timeouts per key and worker parallelism (R-op values; turn caps are contract-fixed) | main 2400 s, burden 2400 s, routing 900 s, ordinary 600 s; `--parallel 4` (2026-10-06: 10 runs hit 900 s below 30 turns; 429s at parallel 8) | P4, P7 |
| SD-4 | Replicates per episode | 1 or 3, **not 2**: the aggregate oracle's strict-majority rule turns 2 replicates into "both must pass". Recommend 1 for the first campaign. | P3 |
| SD-5 | Run the optional P2 development probe before commissioning fresh fixtures? | Yes. It is cheap (~$2 per 100 runs) and shows whether the candidate is plausibly viable *when delivered* before the expensive P3. | P3 timing |
| SD-6 | Who acts as custodian and as pre-run checker (separate capable contexts) | Two fresh contexts, briefed only with their documents and §2 of this plan | P3, P6 |
| SD-7 | Predeclared transient-provider rerun rule (422/502 before any scored action) | None for the first campaign: such a run stays non-PASS, and the analyst reports it. Adopting a rule requires G-2 first. | P4 |

## 5. Pre-run checker mandatory scope (adds to contract §6)

- **Freshness.** Verify A1 by digest against `requal71/disclosed-material.json`, and judge semantic reuse: re-skinned planted properties and the same cases under new bytes.
- **Strata.** Every §11.3 semantic case, R2 opportunity, predicate-excluded opportunity and T-sentinel sits on a deterministic panel with a plausible `declared_root`. Ordinary episodes carry correct `admissible_roots`.
- **Family.** Reproduce the family id and digest. Confirm the panel budget schedule and the criterion-to-key map, using `core70.validate_family` and `requal71 family-build` output.
- **Exposure.** Recount every §2 minimum **on the deterministic stratum alone**, using keys. `corpus-check` proves only the necessary conditions.
- **Run plan.** Confirm the run declarations cover the corpus × arms × replicates exactly, that the 6.5 arm appears on the burden key only, and that purpose is `qualification`.
- **Applicability rulings.** The custodian rules (C-3) on owed parts in exemption-bearing delegate cases, for example "compaction with no run".
- **Oracle.** C-4 is stratum-aware per the work package; run the integrity probes, including a deliberately undelivered deterministic run and a development-purpose run, both of which must be refused.
- **Admissions.** Every key's executor bundle and the evaluator bundle validate against the exact current profile, adapter and core.
- **Custody.** The attestation trail (SD-2) is complete from store creation.

## 6. Open design items (analyst-owned; none blocks P1–P3)

- **G-1. Burden key.** `derive-key` removes the delegate tool from the burden key's profile and capabilities. Whether the OMP mediator then hides it from the live catalog is unverified. Executor admission of that key will observe it. If the live catalog still shows `delegate`, the key is inadmissible and the analyst owns the adapter or mediator change.
- **G-2. Rerun slots.** The harness accepts only realizations enumerated before launch. A contract §5 rerun or a SD-7 replacement therefore needs reserve slots declared in the accounting manifest before freeze, and `audit` must treat unused reserve slots as expected. This is not built. **The default is no reruns**, which is fail-closed.
- **G-3. Executor admission finalization.** No tool converts an operator-produced CANDIDATE bundle (`omp_stage7_admission.py emit-candidate`) plus the checker's verdict into the ADMITTED form that `core70.validate_profile_admission` accepts. The checker finalizes by hand under the existing admission contract, or the analyst supplies a mechanical finalizer that records the checker's verdict without making one. Decide at P5.
- **G-4. Manifest builder.** `make_manifest_from_runs.py` (custody `operator/`) must carry `entry_stratum`, `declared_root`, `profile_key_sha256`, `purpose` and the delivery verdict into the aggregate manifest. This is custodian deliverable C-4.
- **G-5. Ordinary groups.** `audit` classifies ordinary runs from the first selected root against `admissible_roots`. A run that selects several roots is counted by its first selection. The pre-run checker confirms the rule, or the custodian refines it in C-4.
