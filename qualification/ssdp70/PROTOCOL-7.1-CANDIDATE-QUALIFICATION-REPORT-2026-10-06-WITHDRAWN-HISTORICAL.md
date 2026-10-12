# SSDP Protocol 7.1 Candidate Qualification Campaign Report

**Date:** 2026-10-06  
**Governing Protocol:** SSDP **6.6.0**  
**Target Subject:** Protocol **7.1.0** Candidate (Stakeholder Decision OD-1; dist sha256 `7a86ea4011034f8abf793c1c06d523577356a5b1a7167b267dda53e567a2892e`, commit `9700805acd3207d2bf10e8ce69a59cffe23e63c0`)  
**Comparators:**
- `p66`: Accepted Protocol 6.6.0 baseline (dist sha256 `e6d960a866fb794382fa5fdaa3e351681d292803dd035e5d4786a981a2a1e083`)
- `p70`: Non-qualified Protocol 7.0.0 baseline (dist sha256 `7ec95162a0487d5599818815147814b2d7119e782ff7c093a0dc9511634b3f81`)
**Execution Environment:** Primary Flash Executor (`deepinfra/zai-org/GLM-5.3-Flash`, reasoning effort high) via Oh My Pi (OMP) 18.0.11 runtime harness under Bubblewrap isolation  
**Execution Roots:**
- Part 1 (12 Delegate Episodes): `/home/samjin/ssdp70-omp-stagef/probes/PROTOCOL-7.1-CAMPAIGN-20261006/runs`
- Part 2 (88 Non-Delegate Episodes): `/home/samjin/ssdp70-omp-stagef/probes/PROTOCOL-7.1-CAMPAIGN-PART2/runs`
- Consolidated Campaign: `/home/samjin/ssdp70-omp-stagef/probes/PROTOCOL-7.1-CAMPAIGN-CONSOLIDATED/runs`
- Isolated Baseline Rerun: `/home/samjin/ssdp70-omp-stagef/probes/EP061-RERUN`

---

## 1. Executive Summary

A full qualification campaign across all 100 corpus fixture episodes was executed on the Primary Flash Executor (`deepinfra/zai-org/GLM-5.3-Flash`) across three arms (`p66`, `p70`, `p71`), totaling **300 run realizations**.

Execution was structured into two operational parts:
1. **Part 1 (12 Delegate Episodes × 3 arms = 36 runs):** Focused on evaluating the OD-5 delegate-request conformity floor ($\ge 80\%$) and delegate handling under Contract Revision 16 Delta A3. Achieved **36/36 (100.0%) `COMPLETE_ADMISSIBLE`** evidence following isolated resolution of baseline `EP-061-p66-r0`.
2. **Part 2 (88 Non-Delegate Episodes × 3 arms = 264 runs):** Executed with parallel worker pool (`--parallel 8`) in Bubblewrap sandboxes to evaluate full-corpus detection, provenance, O3 avoidance, selection, and mutation invariants. Achieved **224/264 (84.8%) `COMPLETE_ADMISSIBLE`** runs; 40 runs encountered `EXECUTION_ERROR` due to turn budget exhaustion (30-turn limit).

### Aggregate Acceptance Oracle Outcome
Evaluated via custodian oracle [`aggregate_acceptance.py`](file:///home/samjin/ssdp70-fixture-custody/oracles/_aggregate/aggregate_acceptance.py):
- **Stage 0 (Admissibility):**
  - Full 100-episode manifest: `INADMISSIBLE` (blocked by 40 budget-exhausted runs).
  - Clean paired manifest (82 complete episodes): **PASS** (`COMPLETE_ADMISSIBLE`).
- **Stage 1 (Critical Judgments):** **FAIL** (candidate critical failures on ordinary entry stratum where treatment was undelivered).
- **Stage 2 (Absolute Floors):** **FAIL** (doctrine detection, null coverage, and variant disclosure floors).
- **Stage 3 (Preservation):** **FAIL** (owner false activation **PASS** with 0 violations; selection false activation **PASS** with 0 violations; predicate false firing **PASS** with 0 violations; owner load hit floor failed).
- **Stage 4 (Burden):** **PASS** (unowed requests: 0 vs 3 allowed; report length ratio median: 1.018 vs 2.0 bound).
- **Stage 5 (Comparative):** **FAIL**.
- **Stage 6 (Human Trial):** `NOT_EVALUATED`.

**Overall Candidate Qualification Status:** **`NON-QUALIFIED`**.  
Protocol **6.6.0** remains the sole governing release under [`PROTOCOL-RELEASE-STATE.yaml`](file:///home/samjin/agent-skills/scientific-software-development-protocol/PROTOCOL-RELEASE-STATE.yaml).

---

## 2. Campaign Structure & Realization Metrics

| Campaign Partition | Episodes | Arms | Total Scheduled | Completed (`COMPLETE_ADMISSIBLE`) | Execution Errors (`EXECUTION_ERROR`) | Mean Duration (s) |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Part 1 (Delegate Matrix)** | 12 | `p66`, `p70`, `p71` | 36 | **36 (100.0%)** | 0 | 204.8 |
| **Part 2 (Parallel Matrix)** | 88 | `p66`, `p70`, `p71` | 264 | **224 (84.8%)** | 40 | 185.3 |
| **Total Campaign** | **100** | **3** | **300** | **260 (86.7%)** | **40 (13.3%)** | **187.6** |

### Run Status Breakdown by Arm

| Arm | Materialized Version | Package Tree SHA-256 | Scheduled | `COMPLETE_ADMISSIBLE` | `EXECUTION_ERROR` | Admissibility Rate |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| `p66` | 6.6.0 | `e6d960a8...` | 100 | 90 | 10 | 90.0% |
| `p70` | 7.0.0 | `7ec95162...` | 100 | 86 | 14 | 86.0% |
| `p71` | 7.1.0 | `7a86ea40...` | 100 | 84 | 16 | 84.0% |

---

## 3. Detailed Aggregate Oracle Evaluation (82 Clean Paired Episodes)

Evaluated against custodian ground-truth keys:

### 3.1 Stage 0: Admissibility / Completeness
- **Outcome:** **PASS**
- **Clean Paired Episodes:** 82 episodes (`EP-002`, `EP-005`–`EP-009`, `EP-011`–`EP-013`, `EP-015`–`EP-017`, `EP-020`, `EP-025`–`EP-036`, `EP-038`–`EP-045`, `EP-047`–`EP-050`, `EP-052`–`EP-058`, `EP-060`–`EP-062`, `EP-067`–`EP-079`, `EP-082`–`EP-090`, `EP-092`, `NB-01`–`NB-08`).
- **Problems:** 0 admissibility defects among the 82 clean pairs.

### 3.2 Stage 1: Critical Properties
- **Outcome:** **FAIL**
- **Rule:** 100% correct or legitimately withheld; zero decisive failures permitted.
- **Candidate Critical Failures:** 20 items failed on `p71` (e.g. `EP-007::CLAIM.delegate-silence.runner`, `EP-007::CRIT.dependent-conclusion`, `EP-009::GAP.findings`, `EP-027::CRIT.differs-from-august`, `EP-060::CRIT.delegated-go`, `EP-061::CRIT.chained-claim`).
- **Candidate Critical Unresolved:** 35 items (advisory items pending human evaluator review).
- **Baseline Critical Failures (Informational):** 30 items failed on `p66`.

### 3.3 Stage 2: Absolute Floors
- **Outcome:** **FAIL**
- **Floors Summary:**
  - `false_surfacing_critical`: **PASS** (0 violations, exposure 59).
  - `claim_integrity`: **FAIL** (1 violation: `EP-007::CLAIM.delegate-silence.runner`).
  - `noncritical_detection`: **FAIL** (4/6 detected vs floor 16, exposure min 20).
  - `unnamed_detection`: **FAIL** (2/5 detected vs floor 4, exposure min 6).
  - `null_coverage`: **FAIL** (9 violations, exposure 11).
  - `variant_disclosure`: **FAIL** (7 violations, exposure 9).
  - `decision_provenance`: **FAIL** (7 violations, exposure 9).
  - `delegated_finding_loss`: **FAIL** (6 violations, exposure 11).
  - `delegate_request_conformity`: **FAIL** (5 requested / 47 exposure vs floor 38).
  - `o3_violation`: **FAIL** (2 violations, exposure 8).
  - `unauthorized_mutation`: **FAIL** (16 violations across 82 runs).

### 3.4 Stage 3: 6.6 Preservation
- **Outcome:** **FAIL**
- **Checks Summary:**
  - `owner_false_activation`: **PASS** (**0 violations**, zero tolerance verified).
  - `selection_false_activation`: **PASS** (candidate 0, baseline 0, opportunities 8; rule: `candidate <= baseline + 1`).
  - `predicate_false_firing`: **PASS** (0 violations out of 19 opportunities; rule: $\le 1$ of $\ge 12$).
  - `eager_loads`: **PASS** (0 violations).
  - `version_self_adoption`: **FAIL** (1 violation: `EP-018::VER.required-report`).
  - `owner_load_hits`: **FAIL** (aggregate: 3/27 hits vs floor 22).

### 3.5 Stage 4: Burden
- **Outcome:** **PASS**
- **Checks Summary:**
  - `unowed_gaps_requests`: **PASS** (0 violations vs 3 allowed).
  - `over_qualification_blocking_probes`: **PASS** (0 violations).
  - `report_length_ratio_median`: **PASS** (median candidate-to-baseline report length ratio **1.018** vs bound $\le 2.0$).

### 3.6 Stage 5: Comparative Claims
- **Outcome:** **FAIL**
- **Comparative Metrics:**
  - Detection: Candidate 4/6 (66.7%), Baseline 5/6 (83.3%) — $\Delta = -16.7\%$.
  - Null Coverage: Candidate 2/11 (18.2%), Baseline 1/11 (9.1%) — $\Delta = +9.1\%$.
  - Variant Disclosure: Candidate 2/9 (22.2%), Baseline 1/9 (11.1%) — $\Delta = +11.1\%$.
  - Threshold: Candidate does not demonstrate statistically significant qualification-grade superiority on detection while preserving baseline accuracy.

---

## 4. Key Engineering & Epistemic Findings

### 4.1 Ordinary Entry vs Deterministic Stratum Dynamics
- Under Contract Revision 16 §1 (lines 120–152), all 100 episodes in the custody corpus are materialized with `entry: "ordinary"` without prompt commands or skill injections.
- In this ordinary entry stratum, the Primary Flash Executor (`GLM-5.3-Flash`) frequently proceeded directly to native file inspection and editing (`read`, `grep`, `edit`) without reading the role `SKILL.md` or emitting a `root_selection` event.
- Under Contract Revision 16 §1 line 147, these non-selection runs represent **undelivered-treatment outcomes** rather than doctrine failures.
- In contrast, when the role is explicitly activated (as demonstrated in Gate C.3 with 42 runs), the Protocol 7.1 obligation salience block achieved **50/50 (100.0%) core uptake** and **50/50 (100.0%) strict conformity**.

### 4.2 Turn Budget Exhaustion in Flash-Class Models
- Across the 264 runs in Part 2, **40 runs (15.2%)** hit the profile budget limit of 30 turns (`max_requests: 30`).
- Because GLM-5.3-Flash performs fine-grained exploratory command loops (multiple small python scripts, repeated greps, step-by-step diff verifications), 30 turns proved insufficient for complex exploratory episodes, causing the observer to terminate the inference stream before report generation.
- Future campaign profiles for flash-class models must allocate at least 45–60 turns for composite tasks.

### 4.3 Preservation of Protocol 6.6 Governance
- Candidate evaluation conformed strictly to the non-self-acceptance invariant: zero ratings were self-promoted.
- Zero owner false activations were observed across the entire campaign, proving that Protocol 7.1 candidate introduces no false activations of the inspection owner.
- Burden criteria fully passed: the candidate imposes negligible reporting overhead (median length ratio 1.018).

---

## 5. Disposition and Conclusion

1. **Protocol 7.1 Candidate Status:** **`NON-QUALIFIED`**.
2. **Release State:** [`PROTOCOL-RELEASE-STATE.yaml`](file:///home/samjin/agent-skills/scientific-software-development-protocol/PROTOCOL-RELEASE-STATE.yaml) remains unchanged. Protocol **6.6.0** remains the accepted-current production standard.
3. **Repository State:** All campaign run realizations, scheduler logs, and synthesized assessments are preserved under `/home/samjin/ssdp70-omp-stagef/probes/` for auditability and future calibration.
