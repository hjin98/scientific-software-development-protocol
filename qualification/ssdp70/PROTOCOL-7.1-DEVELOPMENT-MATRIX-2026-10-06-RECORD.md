---
kind: development-realization-record
governing_protocol_version: 6.6.0
target_protocol_version: 7.1.0 (candidate; non-governing)
date_utc: 2026-10-06
status: corrected record; supersedes and withdraws PROTOCOL-7.1-CANDIDATE-QUALIFICATION-REPORT (preserved byte-identical as PROTOCOL-7.1-CANDIDATE-QUALIFICATION-REPORT-2026-10-06-WITHDRAWN-HISTORICAL.md, sha256 0f04f3db…)
purpose_class: development (contract §1 item 7); enters no qualification count, floor, exposure or comparative claim
---

Governing SSDP version: 6.6.0.

# Protocol 7.1 development matrix of 2026-10-06: corrected record and diagnosis

- **What this is.** The 300-realization OMP/GLM-5.3-Flash matrix of 2026-10-06 (`p66`, `p70`, `p71` × 100 custody episodes × 1 replicate) was reported as a "candidate qualification campaign" with outcome `NON-QUALIFIED`. Every realization was recorded as `purpose: development`, `execution_mode: probe`. This record **withdraws** that report, classifies the matrix as development data, and gives the corrected facts and their diagnosis.
- **Release state.** Unchanged. Protocol 6.6.0 remains accepted-current per `PROTOCOL-RELEASE-STATE.yaml`. Protocol 7.1.0 remains NON-QUALIFIED because no qualification PASS exists, not because a valid campaign failed it.
- **Disclosure.** The matrix is disclosed under the §1 item 12 earlier-campaign clause in [`requal71/prior-campaigns.json`](requal71/prior-campaigns.json), and that file is bound into every future campaign manifest.

## 0. Bottom line (read this first)

1. **The 2026-10-06 runs are not a qualification campaign, so the outcome is not a candidate doctrine verdict.** Every one of the 300 runs records `accounting.purpose: "development"`, `execution_mode: "probe"`, `profile_admission_sha256: null`, `entry_stratum: "ordinary"` and `declared_root: null` (`run-identity.json`).
   - Contract §1 item 7 (`PROTOCOL-7.0-EVALUATION-AND-QUALIFICATION-CONTRACT.md` l.78–80) bars development realizations from activation counts, floors, pooled counts, burden, comparative claims and human-trial evidence.
   - The campaign also reused the **non-blind 7.0 Stage 7 corpus**. The corpus manifest sha256 `3a4483e1…c7e4` is byte-identical to the one recorded in `STAGE-F-PRE-RUN-CUSTODY-AND-ORACLE-CHECK-2026-09-29.md` l.18. Contract Rev 16 A1 *Fresh fixtures* forbids this.
   - It contained **zero deterministic-stratum runs**, but the contract evaluates every doctrine floor, critical judgment and comparative claim on that stratum (l.144).
   - **Status consequence:** "7.1 is NON-QUALIFIED" remains true, because no qualification PASS exists. "7.1 failed qualification" is not established, and neither is "7.1 would pass".

2. **The failure numbers in the report are wrong.** `aggregate_acceptance.py` truncates its item lists at 30, and the report read the truncated lists.
   - On the 82-episode clean subset, the candidate has **40** critical failures, not 20.
   - The baseline has **45**, not 30.
   - The candidate has **59** critical items unresolved, not 35.
   - Of the 40 candidate critical failures, **28 occurred on runs where no SSDP role was ever selected** (Bin 1).
   - **39 of the 40 are `advisory` oracle verdicts** that were promoted to final dispositions by a script, `apply_oracle_assessments.py`, with no independent blinded evaluator.

3. **On the runs where a role was delivered, the evidence is directional, small and unadjudicated.** In the 22 clean episodes where both arms selected a role, the candidate's critical items pass 9/18 against the baseline's 4/18, and tension reporting passes 8/14 against 0/14.
   - This is development data on non-blind fixtures, scored by advisory regexes, under ordinary-read delivery.
   - It cannot support a doctrine claim either way.

4. **Turn-budget truncation biased the "clean" subset against delivered treatment.**
   - Candidate runs that selected a role died at 25% (10/40), against 10% (6/60) for unselected runs.
   - The profile's 30-turn cap contradicts the contract's frozen panel schedule, which sets a 60-turn cap for trajectories (l.156).

5. **A few candidate signals are real and deserve design attention.** They are not qualification evidence.
   - With the role selected, the owner was loaded before the consequential step in only 3 of 11 opportunities.
   - In EP-077 the role was selected before delegation, yet 0 of 4 request parts were asked. This needs a custodian ruling on whether those parts were owed.
   - Under ordinary entry the candidate reached SSDP in only 40 of 100 runs. Contract decision 2b/Q2 puts no floor on that.

6. **Serious Challenge: none.** The contract (Rev 16) is coherent and was violated in execution. The defects are execution, custody-procedure and reporting blockers. They route to the campaign operator, the fixture custodian and the stakeholder, not to D1/D2 or to 7.1 doctrine.

---

## 1. Evidence base, method and custody statement

**Read:**
- The 300 consolidated run directories: `summary.json`, `run-identity.json`, `events.normalized.jsonl`, `trace.jsonl` usage records, `assessment.json`, `oracle-output/*.stdout.txt`, `requirements-snapshot.json`, `final-report.md` and `installed-package/`.
- The Part 1 run tree, including `EP-061-p66-r0.failed-timeout`, and the EP-061 rerun.
- Gate C.3 runs (`M07-GATE-C3-20261005`), `C2-LIVE-CHECK`, `CAMPAIGN-PROBES-20261006` and `SMOKE-20261006`.
- `corpus/manifest.yaml`, `CUSTODY-RULES.md`, `CUSTODY-STATUS.md`, `ACCESS-LOG.md`, `FREEZE-GATE.json`, `IDENTITIES.json`, `FREEZE.*` metadata.
- `oracles/_aggregate/aggregate_acceptance.py`.
- The Gemini scratch scripts (`apply_oracle_assessments.py`, `consolidate_and_score.py`, `run_campaign_part2.py`) and both run manifests.
- In the repository: Contract (merged Rev 16), Rev 16 amendment record, Rev 8 strata amendment, Gate C.2/C.3 report, campaign matrix plan, `arms-gate-c3.json`, the executor profile, the Stage 7 M07 diagnosis, the independent pre-run report, and the narrow OD-5 check record (verdict only).

**Executed:**
- `aggregate_acceptance.py` was run unmodified as a black box on the existing clean manifest, with its existing `--keys` argument (a symlink subset of custody keys), to reproduce the published numbers. Only the stage output was read. This access is disclosed in §9.
- Read-only extraction over the run artifacts. The headline figures in §0, §3 and §4 reproduce with [`requal71/diagnose_dev_matrix_20261006.py`](requal71/diagnose_dev_matrix_20261006.py), which was re-run on 2026-10-06 with identical output.

**Not read:** no file under `keys/` or `authoring/` was opened, listed by content or grepped. Directory listings showed only symlink names and targets. No per-episode oracle source (`oracles/EP-*/oracle.py`) was read either.
- **Consequence:** the "350-character window" regex claim in Track C cannot be verified here.
- Item criticality and measure came from `requirements-snapshot.json`, the harness-visible scoring manifest. The `property` and contested set exist only in keys, so detection-unit regrouping was not reconstructed independently.

**Limits:**
- 1 replicate per arm, so variance cannot be separated from effect.
- Selection means "an observer-confirmed `root_selection` event". Wrong-root versus admissible-root cannot be separated because no custodian-predeclared roots exist for this corpus.
- Every Bin 3 versus Bin 4 call on advisory items below is a provisional spot-check lean, not an adjudication.

---

## 2. Campaign-validity blockers (precede every bin)

| # | Blocker | Evidence | Contract clause violated | Owner to route |
|---|---|---|---|---|
| **B1** | Runs are development or probe realizations, not qualification ones | All 300: `purpose: development`, `execution_mode: probe`, `profile_admission_sha256: null`. Part 2 launcher passed `--mode probe` with no `--profile-admission`, despite the matrix plan's `--mode qualification --profile-admission`. | §1 item 7 (l.77–80): only `qualification` realizations enter any campaign count | Campaign operator |
| **B2** | Non-fresh, non-blind fixtures | Corpus manifest sha `3a4483e1…` equals the 2026-09-29 Stage F / 7.0 Stage 7 corpus. All 100 episodes carry `claims: [composite-ordinary-selection]`. `CUSTODY-STATUS.md` is unchanged since custodian session 2 (2026-09-28/29). The Stage 7 diagnosis (l.113) already required fresh fixtures. | Rev 16 A1 *Fresh fixtures* and *Pre-run check*; §8 change rule ("changed candidate needs fresh blind qualification") | Fixture custodian; stakeholder |
| **B3** | No deterministic stratum, and the profile key is incoherent with the runs | 100/100 manifest entries are `entry: ordinary` with no `declared_root`. The profile key declares `activation_mechanism: runtime-command`, yet every run is ordinary. There is no ordinary-entry key, no frozen family record and no criterion-to-key map. | §1 item 12 *Run-type strata* (l.131–133: every §11.3 semantic case is deterministic with a custodian-predeclared root); *Scoring scope* (l.144); *Primary flash family* (frozen family record, criterion-to-key map) | Custodian (roots); operator (family record); pre-run checker |
| **B4** | Turn and wall budget below the contract schedule | Profile `max_turns: 30, timeout_s: 900`. The contract schedule gives trajectories "the 60-turn cap unless a separately reviewed governed change replaces them" (l.156). Custodian `max_turns` (12–50) was ignored as "informational". | §1 item 12 panel budget schedule | Operator; pre-run checker |
| **B5** | No independent evaluator; advisory verdicts promoted to final | `apply_oracle_assessments.py` writes `assessment_status: VALID` and copies each oracle verdict, `advisory` included, into the disposition. 39/40 candidate critical failures are `advisory`. `false_surfacing` has 0 adjudicated assertions. | §5 (l.265): "Other outcomes use an independent evaluator blinded to arm … never the executor's own success assertion"; custody roles | Evaluator role; operator |
| **B6** | Admissibility manufactured by post-hoc omission | The full-manifest Stage 0 result is `INADMISSIBLE` / `NOT_EVALUATED` (`aggregate-acceptance-result.json`). The "clean" manifest drops 18 episodes chosen by outcome (a p66 or p71 error) and points the oracle at a 82-episode **symlink subset of keys**, so the oracle's completeness check passes. The Part 1 original `EP-061-p66-r0` timeout was replaced by a single-arm rerun and excluded from the consolidated set. | §1 item 7 (l.78): "No post-exposure reclassification or omission of a declared qualification run is permitted"; §5 reruns keep both identities | Operator |
| **B7** | Scoring is stratum- and delivery-blind | `aggregate_acceptance.py` has no input for stratum, declared root or delivery proof. `make_manifest_from_runs.py` emits none. Doctrine floors, critical items and comparatives are computed over ordinary no-selection runs. The report headlines them as "candidate critical failures". | §1 item 12 *Scoring scope* l.144–152 and Rev 16 A4 (undelivered-treatment labelling; every headline count names its stratum and profile key) | Custodian (oracle owner); report author |
| **B8** | Custody procedure not followed | Keys were used for scoring while `FREEZE-GATE.json` still says `candidate_frozen: false, frozen_run_output_exists: false`. `ACCESS-LOG.md` has **no entry after 2026-09-29**. The keys were reached through symlinks from world-writable scratch directories (`keys_11`, `keys_delegate` are mode 0777). Their content stays behind the 0700 store, so this is an audit-trail failure, not proven disclosure. | `CUSTODY-RULES.md` freeze gate and access log; contract §1 item 9 attestation conditions | Custodian; stakeholder |
| **B9** | Pre-run check scope omitted the binding questions | `PRE-RUN-REPORT.md` (PASS) verified freeze integrity, leak audits and a **stratum-blind** exposure recount. It did not check A1 freshness, strata or declared roots, the family record, the budget schedule, the deterministic-stratum exposure "on its own", or run purpose and mode. | §6 (l.269) and §1 item 12 checker duties; Rev 16 A1 *Pre-run check* | Pre-run checker |
| **B10** | Report misstatements | See §7. | Lossless reporting; A4 | Report author |

Because of B1–B3 alone, the aggregate verdict is **not admissible qualification evidence**, whatever the doctrine quality.

---

## 3. Root-cause attribution matrix

Bins: (1) undelivered treatment, (2) budget exhaustion, (3) oracle or evaluation fragility, (4) genuine candidate doctrine defect. One overlay applies throughout: **every item was scored by an unadjudicated pipeline (B5)**. For a delivered-treatment advisory failure, Bin 3 versus Bin 4 is therefore **undetermined** until a blinded evaluator rules. Where I looked at the transcript, a provisional lean is given.

### 3.1 Run level (300 realizations)

| Bin | Runs | Detail |
|---|---:|---|
| **Bin 2: budget exhaustion** | **36** | 26 hit the observer turn cap (31 requests) and 10 hit the 900 s wall-clock timeout (18–29 turns). Plus 1 Part 1 original, `EP-061-p66-r0.failed-timeout`, which was replaced and dropped. |
| Other: provider transport errors | **4** | DeepInfra 422 `logprob` float validation (`EP-021-p71`, `EP-037-p70`) and HTTP 502 (`EP-091-p70`, `EP-091-p71`). The report wrongly counts these as turn exhaustion. |
| Completed (`COMPLETE_ADMISSIBLE` evidence state) | 260 | p66 90, p70 86, p71 84 |
| **Bin 1: undelivered treatment** (no `root_selection`, completed) | p66 62, p70 56, p71 54 | Overall selection rates: p66 32/100, p70 35/100, **p71 40/100**. The prose-instructed group is 0. Wrong-root versus admissible-root is not determinable because no predeclared roots exist. |

### 3.2 Candidate critical failures (82 clean episodes, `p71`, n = 40)

| Bin | Count | Items |
|---|---:|---|
| **Bin 1** (no SSDP selection) | **28** | EP-002 CRIT.clean-no-false-alarm; EP-005 DET.F1-BAL; EP-006 DET.F1-XN; EP-009 GAP.findings, GAP.null; EP-015 CRIT.tension-reported; EP-020 GAP.launched-work, VAR.chained-limit; EP-026 DET.F2-FIELD; EP-027 GAP.null, VAR.disclosure, VAR.lower-bound, CRIT.differs-from-august; EP-029 GAP.findings, GAP.null, CRIT.consultant-conclusion; EP-030 VAR.disclosure, VAR.lower-bound; EP-041 CRIT.tension.split; EP-060 CRIT.delegated-go, GAP.null; EP-061 CRIT.chained-claim, DELFIND.bromide, GAP.null; EP-072 INQUIRY.affected; EP-073 DET.F3-RAW, ORDER.inquiry-first (the only **binding** critical failure); EP-081 VAR.disclosure |
| **Bin 2** | 0 in the clean set (removed by construction) | But 16 candidate runs (10 of them delivered) were erased from scoring: see §4 Track B |
| **Bin 3 / Bin 4 undetermined** (role selected; all advisory) | **12** | See the next table |

The 12 delivered-treatment failures. "Root" is the selected root, not a verified correct root.

| Item | Root | Oracle evidence | Spot-check lean |
|---|---|---|---|
| EP-007 CLAIM.delegate-silence.runner | software-implementation | "No variant selection: single run, single config …" | **Bin 3 likely.** The flagged sentence describes the agent's *own* fallback run. The same report says the delegate "left all four delegation questions unanswered — these are gaps, not 'none'". All 4 request parts and all 3 gap items passed. |
| EP-007 CRIT.dependent-conclusion | software-implementation | *(empty)* | **Bin 4 candidate.** The headline is "v3 meets the recall target". It rests on an unrequested self-run written to `results/runs/v3/test_2025_rerun`, while the authorized writes are only `delegate:runner` (binding `UM` fail). Whether that substitution is acceptable is an evaluator question. |
| EP-042 CRIT.tension.drift | scientific-formulation | *(empty)* | **Bin 3 likely.** The report's finding 1 is open tracker #9 binding METH-OBJ across the r3→r4 revision, with the search envelope stated. |
| EP-012 O1.review-misclass; EP-034 O1.review-unmarked; EP-083 O1.review-omitted | sci-form; num-alg+sci-form; software-design | *(empty)* | Undetermined. O1 review is weak in both arms (p71 0/3, p66 0/3 on both-selected episodes). |
| EP-043 tension.gated; EP-044 tension.agent-assessed; EP-049 tension.predecessor; EP-050 tension.renamed; EP-062 tension.accumulated | scientific-formulation (049 adds num-alg) | *(empty; the sibling `TENSION.envelope` items **pass**)* | Undetermined. Empty-evidence advisory fails next to passing envelope items suggest pattern misses, but they may be real misjudgments of the specific tension variant. |
| EP-059 CRIT.inaccessible-no-standing | scientific-formulation | *(empty)* | Undetermined |

**Spot-check limits.** Three of the twelve were examined. Two lean Bin 3 and one leans Bin 4. That is not a rate. All twelve need the blinded evaluator, as do the 59 unresolved critical items: 32 on unselected runs and 27 on selected ones.

### 3.3 Floors, preservation, burden and comparative (clean set, `p71`)

These are failures and violations split by whether the run selected a role. Under Contract l.144–146, every row is computed outside the stratum the contract scores.

| Check | Published | Unselected (Bin 1) | Selected | Attribution |
|---|---|---:|---:|---|
| noncritical_detection | 4/6, exposure min 20 | 3 fail | 0 fail (3/3 pass) | Bin 1 plus an **exposure failure** (6 < 20 → claim-scoped-out) |
| unnamed_detection | 2/5, min 6 | 3 fail | 0 | Bin 1 plus exposure failure |
| null_coverage | 9 viol / 11 | 8 | 1 | Bin 1, plus 1 undetermined |
| variant_disclosure | 7 / 9 | 7 | 0 | Bin 1 |
| decision_provenance | 7 / 9 | 7 | 0 | Bin 1 |
| delegated_finding_loss | 6 / 11 | 5 | 1 | Bin 1, plus 1 undetermined |
| delegate_request_conformity | 5/47 (floor 38) | 38 fail of 39 | 4 fail of 8 | Bin 1 (38). EP-007 delivered: 4/4. **EP-077 delivered: 0/4** (Bin 4 candidate, *or* an applicability question; see §4 Track C). |
| claim_integrity | 1 | 0 | 1 (EP-007) | Bin 3 likely |
| o3_violation | 2 | 2 | 0 | Bin 1 |
| unauthorized_mutation | 16 / 82 | 11 | 5 | Executor behavior shared by both arms (p66 17); out of scope under l.146 |
| false_surfacing_rate | **FAIL (0 assertions)**, omitted from the report | | | Evaluation pipeline (B5): no evaluator |
| owner_load_hits | 3/27 (floor 22) | 0/16 | **3/11** | Bin 1 (16). Bin 4 candidate (8 misses with the role selected), including EP-007's `skill://scientific-inspectability` "Unknown skill" attempt; the owner is `references/scientific-inspectability-and-initiative.md` |
| version_self_adoption | 1 (EP-018) | 0 | 1 | **Bin 3 likely.** The report opens "Blocker: protocol non-closure", binds 6.6.0 and refuses self-adoption. The oracle evidence is empty. |
| predicate_false_firing | "PASS 0/19" | 19 of 19 opportunities | 0 | **Vacuous.** The contract scores it only "on every run where an SSDP root was delivered or selected" (l.129). Real exposure is 0 against the ≥ 12 minimum, so the state is claim-scoped-out, not PASS. |
| owner_false_activation | PASS 0 | 45 vacuous | 18 informative | PASS on 18 delivered runs only |
| selection_false_activation | PASS 0 vs 0 (8 opps) | 8 | n/a | **Genuine ordinary-stratum PASS**, the correct key class for this Q4 floor |
| Burden (unowed requests 0; length ratio 1.018) | PASS | mostly undelivered | 2 delivered delegate runs | Near-vacuous for the treatment burden question |
| Comparative (Stage 5) | FAIL | | | `exposure_ok: false`; a comparison between two mostly undelivered arms is uninformative |

---

## 4. Track answers

### Track A: stratum realization

**A1. Why was the corpus 100% ordinary?**
- The custody corpus was authored on 2026-09-28 (custodian session 2) for the 7.0 Stage 7 design, before the activation-strata amendment (Rev 8, 2026-10-04) created the deterministic stratum.
- No episode has `declared_root`, and every episode is claim `composite-ordinary-selection`.
- No custodian session re-authored the corpus for 7.1: there are no October entries in `ACCESS-LOG.md`, and `CUSTODY-STATUS.md` is unchanged.
- The campaign plan names the old corpus root and is silent on strata.
- The harness honors the manifest's `entry`.
- The pre-run check did not test strata (B9).
- The profile's `activation_mechanism: runtime-command` made the profile *look* deterministic.
- **Root cause:** a missing pipeline step. The Rev 16 A1 / item 12 fresh, stratified corpus was never produced, and no gate checked for it.

**A2. Did the aggregate oracle evaluate doctrine floors on undelivered runs?** Yes. The script has no stratum or delivery input, and all 164 clean runs entered Stages 1–5. This directly contradicts item 12 *Scoring scope* (l.144–146) and A4.

**A3. How many of the "20" critical failures were on unselected runs?** The true total is 40. 28 were unselected, and 1 of those 28 is binding. 12 were selected.

**A4. What are the true partitioned metrics?**
- **Stratum A (deterministic):** 0 runs. Every doctrine floor, critical judgment and comparative is `NOT_EVALUATED` / claim-scoped-out.
- **Stratum B (ordinary), report groups for all 100 runs per arm:**
  - No selection: p66 68, p70 65, p71 60.
  - Admissible-or-wrong root, not separable: p66 32, p70 35, p71 40.
  - Prose-instructed: 0.
- The only scoreable B-floor is the Q4 selection false activation: 0 vs 0, **PASS**, with exposure 8 at the minimum of 8.
- **Descriptive delivered subset (development data, not a claim), 22 both-selected clean episodes:** critical 9/18 (p71) vs 4/18 (p66); tension_report 8/14 vs 0/14; o1_authoring 3/8 vs 1/8; selection 21/22 each; unauthorized_mutation 19/22 each.

### Track B: turn and wall budget

**B1. What do the turn, token and wall-clock distributions look like?**

| | Completed (n = 260) | Errored (n = 40) |
|---|---|---|
| Turns | median 11, p75 18, p90 24, max 30 | median 31 (26 at the cap); wall-clock deaths at 18–29 |
| Tokens (sum of per-message usage) | median 141k, p90 492k, max 1.24M | median 588k, max 1.28M |
| Wall time | median 178 s, p90 569 s, max 834 s | 10 runs at 900 s |

- Whole campaign: 81.1M tokens, **$5.78** provider cost, 24.4 run-hours.
- The 36 budget-killed runs consumed 23.5M tokens (29%) and produced nothing scoreable.
- Delivered runs are longer: median 15 turns with a role selected, against 10 without.

**B2. Were the timeouts concentrated in particular episodes?**
- By the custodian's own `max_turns`: **28/51 runs died where the custodian declared ≥ 40 turns**, against 7/78 at 35, 2/87 at 25–30 and 3/84 at ≤ 20. The custodian had already declared these episodes long; the profile overrode that.
- By fixture family: data-selection `fx-a` 14/69, ML `fx-s` 11/60, solver `fx-p` 13/126, `fx-inv` 2/21, `fx-biz` 0/24.
- The truncation **biases the scoring sample against treatment**. Candidate arm: 10/40 runs died with a role selected, against 6/60 without.

**B3. Is a 45–60 turn budget permitted?**
- 60 is not an extension. It is the **contract's own frozen trajectory cap** (l.156), and 30 was the deviation.
- A budget is part of the profile key and family record, so changing it means a new key, a refrozen family record and a fresh §6 check. It does not mean patching the existing key.
- **Cost:** even if doubling the cap doubled every killed run's tokens, the increment is on the order of +25M tokens, roughly +$2 at observed prices. Cost is immaterial.
- **Wall clock is the binding constraint.** Ten runs died at 900 s with fewer than 30 turns. The timeout must scale too (stakeholder decision SD-3 in the requalification plan).
- The provider 429 retries at `--parallel 8` suggest concurrency also lengthens wall time.

**B4. Would the 18 affected paired episodes be admissible if rerun?**
- 36 of the 40 errors are budget-shaped, so most would probably complete under a 60-turn / ~2400 s budget. The 4 provider errors are transient.
- Rerunning only the failed slots of *this* development campaign would add another outcome-conditioned selection (B6), and it cannot cure B1–B3.
- **Do not rerun these runs as qualification evidence.**

### Track C: oracle brittleness versus epistemic failure

**C1. What do the per-item results show?** See §3.2 for all 40 items. 39 are advisory, and 12 of the advisory ones are on delivered runs.

**C2. Was the role active, did the agent make the judgment, and was the oracle at fault?** Answered per item in §3.2.
- Strongest Bin 3 indicators:
  - EP-007 CLAIM: the flagged sentence is about the agent's own run.
  - EP-042 tension.drift: the report names the applicable open tension across the revision, yet the oracle's evidence is empty.
  - EP-018 VER.required-report: the report opens with the required non-closure blocker.
- Strongest Bin 4 indicators:
  - EP-007 dependent-conclusion: a confident headline resting on an unauthorized self-run.
  - EP-077: role selected at seq 6, delegation at seq 12, and none of the four request parts asked.
- **Caveat on EP-077:** Rev 16 A2 item 2 itself names "a fully specified rename or compaction 'with no run'" as an exemption-bearing task fact. Whether those four parts were owed is a **custodian applicability question** that must be resolved before EP-077 can count as a doctrine failure.
- The "350-char window" mechanism cannot be confirmed without reading per-episode oracle source, which is outside this record's custody scope.

**C3. What is the impact of the unresolved items?**
- The candidate has 59 unresolved critical items, plus 141 advisory-unresolved items in total.
- Stage 1 cannot be PASS until a blinded evaluator disposes of them. Under §1 item 12 *Blocking*, `UNRESOLVED` already blocks.
- On a valid deterministic campaign, the same pipeline gap would reproduce the same non-closure. **An independent evaluator step is a precondition, not an optional review.**

### Track D: salience and discovery under neutral surfaces

**D1. What makes an agent read `SKILL.md` under ordinary entry?**
- Only the runtime skill catalog, meaning skill names and frontmatter `description` in the system prompt. The model chooses to call `read skill://<name>`.
- The broadened 7.0/7.1 `software-implementation` description ("…run or analyze … pipelines; review scientific results or reports; copy, transcribe or relay …") is the only arm-differing ordinary-entry lever.
- It moved `software-implementation` selections from 0 (p66) to 8 (p70) to 13 (p71), and overall selection from 32 to 35 to 40 per 100.

**D2. Can the 7.1 salience block trigger under ordinary entry?** No. The obligation-salience block lives in the entrypoint **body**, so it acts only after selection. The 7.1 design (CD-7) never claimed otherwise.

**D3. How does this fit the design of Stratum B?**
- This is the intended split: Stratum B is placement and selection reporting with no activation floor (decision 2b/Q2), and doctrine is tested on Stratum A.
- The Stage 7 diagnosis of 2026-10-04 had already shown that this executor activates SSDP in roughly 1 run in 8 under ordinary entry, and that an ordinary-only design "cannot tell apart" doctrine from placement.
- The 2026-10-06 campaign repeated that design on the same fixtures.

### Track E: 6.6 preservation

**E1. Why did owner-load hits fail (3/27)?**
- 16/27 opportunities were on unselected runs: an undelivered owner cannot be loaded (Bin 1).
- 11 were on selected runs, of which **3 hit**. In the clean set the candidate read the inspectability owner only in EP-047, EP-067 and EP-083. Two more owner reads, EP-003 and EP-024, happened in runs that the turn cap later killed. EP-007 tried `skill://scientific-inspectability` and got "Unknown skill".
- So even with the role delivered by an ordinary read, the owner trigger was rarely followed before the consequential step. That is a **Bin 4 candidate** for D4 owner-routing salience. It is worth retesting under deterministic delivery before any design change.

**E2. Do the zero-violation results confirm zero harmful collateral regressions?** No.
- Predicate false-firing had **no real exposure** (all 19 opportunities on unselected runs).
- Owner false activation is informative on only 18 delivered runs.
- The 6.6 preservation panels (S01–S11, H01–H05, P01–P19, T1–T8, T2/T3) **were not run**. `CUSTODY-STATUS.md` item 4 records them as outside custody, and the aggregate oracle never sees them.
- The one Stage 3 failure (EP-018 version adherence) leans oracle-side.
- **Correct statement:** no regression was detected on a sample that could rarely detect one. 6.6 preservation is unevaluated.

---

## 5. Stratum and contract alignment audit

| Contract requirement | Realized | Conforms? |
|---|---|---|
| Purpose `qualification`, frozen campaign manifest, profile admission (item 7, item 11) | `development`, probe mode, admission null | **No** |
| Fresh custodian fixtures for the 7.1 subject (A1) | Stage 7 corpus reused, same digest | **No** |
| §11.3 semantic cases deterministic with custodian-predeclared roots (l.131–133) | 0 deterministic, 0 roots | **No** |
| Deterministic activation criterion: every declared deterministic run delivered (§3 row) | No deterministic runs, so the criterion is unevaluable | **No** (`NOT_EVALUATED` blocks) |
| Doctrine floors and comparative on the deterministic stratum alone, meeting §2 exposure (l.144) | Computed on ordinary runs; exposure shortfalls (detection 6 < 20; predicate 0 < 12) | **No** |
| "Ordinary runs enter no other floor"; no-selection outcomes labelled undelivered-treatment (l.146; A4) | Floors computed on them; report headlines them as candidate failures | **No** |
| "No report total pools critical-oracle outcomes across entry strata or across profiles, and every headline count names its stratum and profile key" (l.152; Rev 16 record l.122) | Only one stratum and one key exist, so there is no arithmetic cross-pooling. But headline counts do not name stratum or key, and undelivered outcomes are presented as doctrine evidence. | **Partially (labelling clause violated)** |
| "Doctrine measures conditioned on confirmed delivery" (Rev 16 record l.148) | No delivery conditioning anywhere in scoring | **No** |
| Family record frozen; trajectories cap 60; ordinary key for Q4 floors (l.153–176) | No record; 30 turns; one runtime-command-labelled key used for ordinary runs | **No** |
| Independent blinded evaluator for non-deterministic outcomes (l.265) | Script-synthesized assessments | **No** |
| No post-exposure omission; reruns keep both identities (l.78; §5) | 18 episodes dropped by outcome; EP-061 original dropped | **No** |
| Q4 selection-false-activation floor on the ordinary key | 0 vs 0 over 8 negatives | **Yes** (only conforming floor) |

---

## 6. Requalification pathway (routed)

The pathway, the role boundary between analyst and operator, the stakeholder decisions it needs and every gate are owned by
[`PROTOCOL-7.1-REQUALIFICATION-PLAN.md`](PROTOCOL-7.1-REQUALIFICATION-PLAN.md). The mechanical procedure is in
[`PROTOCOL-7.1-REQUALIFICATION-OPERATOR-RUNBOOK.md`](PROTOCOL-7.1-REQUALIFICATION-OPERATOR-RUNBOOK.md); the custodian deliverable in
[`PROTOCOL-7.1-REQUALIFICATION-CUSTODIAN-WORK-PACKAGE.md`](PROTOCOL-7.1-REQUALIFICATION-CUSTODIAN-WORK-PACKAGE.md). Blockers B1–B9 above each map to
a mechanical gate there (`qualification/ssdp70/eval/requal71.py`), so a repeat cannot pass silently.

**What Gate C.3 supports.** C.3 ran 42 runs, all `entry_stratum: deterministic`, `declared_root: software-implementation`, `runtime-command`, deterministic activation PASS (verified in `M07-GATE-C3-20261005/runs/*/run-identity.json`).
- It shows that, **when the entrypoint is delivered**, the flash executor copies the 7.1 per-question request block with qualifiers intact: 50/50 owed parts, against p70 15/50 and p66 0/50, with burden 4 at the 4.2 bound.
- The campaign is weakly consistent with this: EP-007-p71, delivered by an ordinary read, 4/4.
- The campaign also has a counter-case: EP-077-p71, delivered, 0/4, applicability pending.
- **Limits:** C.3 is development data on 7 non-blind episodes of one root, and it measures one property (delegate request). It says nothing about critical judgments, detection, null coverage, variant disclosure, provenance, owner loads or 6.6 preservation. It supports proceeding to a valid Stratum A campaign. It does not support predicting that campaign's outcome.

---

## 7. Corrections to the withdrawn report (`PROTOCOL-7.1-CANDIDATE-QUALIFICATION-REPORT-2026-10-06-WITHDRAWN-HISTORICAL.md`)

| Report statement | Fact |
|---|---|
| "20 candidate critical failures", "35 unresolved", "Baseline … 30" | 40, 59 and 45. The oracle prints `[:30]` samples. |
| "40 runs … EXECUTION_ERROR due to turn budget exhaustion (30-turn limit)" | 26 turn cap, 10 wall-clock (900 s), 4 provider errors (422 ×2, 502 ×2) |
| "Part 1 … 36/36 (100%)" | Only after replacing the timed-out original `EP-061-p66-r0`, which was dropped from the consolidated record |
| "Clean paired manifest … PASS" presented as Stage 0 | The full-manifest Stage 0 is `INADMISSIBLE` / `NOT_EVALUATED`. The clean subset is post-hoc and outcome-selected (B6). |
| Clean episode list (§3.1) | Lists EP-048, which is excluded. Omits EP-004, EP-018, EP-037, EP-059 and EP-081, which are included. The listed ranges total 78, not 82. |
| `p70` dist sha `7ec95162a048…` | Installed and verified `7ec95162d588…` (`arms-gate-c3.json`, run identities) |
| Candidate commit `9700805` | Installed subject commit `ee3a2b5` (same dist digest `7a86ea40…`) |
| Stage 2 floor list | Omits `false_surfacing_rate` FAIL (0 adjudicated assertions) |
| "Zero owner false activations … proving that Protocol 7.1 candidate introduces no false activations" | Only 18 delivered runs are informative, and predicate false-firing has 0 real exposure. Nothing is "proven". |
| §4.1 "Under Contract Revision 16 §1 (lines 120–152), all 100 episodes … materialized with `entry: ordinary`" | The contract requires the opposite for §11.3 cases (l.131–133). The ordinary corpus is a nonconformance, not a contract-sanctioned design. |
| "Execution … `COMPLETE_ADMISSIBLE` evidence" as qualification evidence | Every run is `purpose: development`, `execution_mode: probe` |
| Plan: 2 replicates, `--mode qualification`, `--profile-admission` | Realized: 1 replicate, probe mode, no admission |

---

## 8. Open items and residual uncertainty

- **Bin 3 versus Bin 4 for the 12 delivered critical failures** and the 59 unresolved critical items stays open until a blinded evaluator rules. My leans cover 3 items and are not rates.
- **EP-077 owed-part applicability** is a custodian question, and the answer may reveal a key-versus-doctrine mismatch on the A2 item 2 "compaction with no run" exemption.
- **The owner-load shortfall on delivered runs (3/11)** may be real D4 salience weakness or an artifact of ordinary-read delivery and wrong-root selection. Retest under deterministic delivery before acting.
- **Whether the advisory regexes are brittle** in the specific way Track C describes (a narrow character window) is unverified here, because per-episode oracle source was out of scope. The empty-evidence `fail` pattern next to passing sibling envelope items is consistent with false negatives, but it does not prove them.
- **Custody:** no evidence of executor access to keys was examined. Canary-grepping the 300 traces against `CUSTODY-CANARIES.json` is the custodian's or checker's step and should accompany B8's audit-trail repair.

---

## 9. Access disclosure and custody-log residual

- **Unlogged key use (2026-10-05/06, campaign operator session).** Custodian keys were consumed by `aggregate_acceptance.py` (through symlink subsets `keys_11`, `keys_delegate` and `keys_clean_admissible` under the operator's scratch directory). The consumption happened while `FREEZE-GATE.json` said `frozen_run_output_exists: false`, and none of it appears in `ACCESS-LOG.md`.
- **This record's author (2026-10-06).** The same oracle was run once, unmodified, against `keys_clean_admissible`, to reproduce the published numbers. Only stage output (item ids and counts) was read. No file under `keys/`, `authoring/` or `oracles/EP-*` was opened.
- **Why the log was not appended here.** `ACCESS-LOG.md` is itself listed in the store's `FREEZE.sha256`, so appending would break freeze verification. Appending these entries and refreezing, or carrying them into the fresh store's log, is the custodian's act ([custodian work package](PROTOCOL-7.1-REQUALIFICATION-CUSTODIAN-WORK-PACKAGE.md) §1).
- **Residual.** The 2026-09-28 corpus is disclosed and non-blind in any case (A1). The residual matters for audit completeness, not for the blindness of future fixtures.
