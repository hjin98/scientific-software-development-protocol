# SSDP Protocol 7.1 Candidate Qualification — Campaign Run Matrix Plan

> **Status (2026-10-06): SUPERSEDED, not followed.**
> - **Contract nonconformance.** This plan is incomplete against the contract. It has no fresh fixtures, no entry strata or declared roots, no primary-family record, no panel budget schedule, no evaluator step, and no 6.5 burden comparator.
> - **The realized matrix departed from it anyway.** It ran with `--mode probe`, no profile admission and 1 replicate.
> - **The result is development data.** See [`PROTOCOL-7.1-DEVELOPMENT-MATRIX-2026-10-06-RECORD.md`](PROTOCOL-7.1-DEVELOPMENT-MATRIX-2026-10-06-RECORD.md).
> - **Successor.** The requalification path is owned by [`PROTOCOL-7.1-REQUALIFICATION-PLAN.md`](PROTOCOL-7.1-REQUALIFICATION-PLAN.md).
>
> The text below is kept unchanged as history.

**Governing Protocol:** SSDP 6.6.0  
**Target Subject:** Protocol 7.1.0 Candidate (Stakeholder Decision OD-1; commit `9700805`, dist sha256 `7a86ea40...`)  
**Comparators:**
- `p66`: Accepted Protocol 6.6.0 comparator (sha256 `e6d960a8...`)
- `p70`: Non-qualified Protocol 7.0 baseline (sha256 `7ec95162...`, Option A closeout comparator)

---

## 1. Execution Profile & Environment

- **Primary Executor:** DeepInfra GLM-5.3-Flash (`deepinfra/zai-org/GLM-5.3-Flash`, reasoning effort high).
- **Runtime Harness:** Oh My Pi (OMP) runtime harness via `qualification/ssdp70/eval/harness70.py`.
- **Runtime Adapter:** `omp-json-v2` (`qualification/ssdp70/eval/adapters/omp.py`).
- **Profile Key:** `qualification/ssdp70/eval/profiles/omp-primary-flash-executor.json` (frozen digest verified; 0 profile errors).
- **Capability Manifest:** `qualification/ssdp70/eval/capabilities/omp-headless.json`.
- **Containment Policy:** Bubblewrap (`bwrap`) isolation with PID/IPC/UTS/network loopback namespaces and read-only host binds.

---

## 2. Arms Manifest

Arms manifest is frozen in `qualification/ssdp70/arms-gate-c3.json`:

```json
{
  "arms": {
    "p66": {
      "name": "SSDP Protocol 6.6 Accepted Baseline",
      "package_sha256": "e6d960a866fb794382fa5fdaa3e351681d292803dd035e5d4786a981a2a1e083",
      "ref": "22f4bdba53795da3a6f13f162529f3a843fc37ae",
      "version": "6.6.0"
    },
    "p70": {
      "name": "SSDP Protocol 7.0 Non-Qualified Baseline",
      "package_sha256": "7ec95162a0487d5599818815147814b2d7119e782ff7c093a0dc9511634b3f81",
      "ref": "411510ed96c0427041b091834906291cbf456b4e",
      "version": "7.0.0"
    },
    "p71": {
      "name": "SSDP Protocol 7.1 Realized Candidate",
      "package_sha256": "7a86ea4011034f8abf793c1c06d523577356a5b1a7167b267dda53e567a2892e",
      "ref": "9700805acd3207d2bf10e8ce69a59cffe23e63c0",
      "version": "7.1.0"
    }
  },
  "schema": 1
}
```

---

## 3. Campaign Structure & Scheduling

- **Corpus Root:** Provided by the Fixture Custodian under `/home/samjin/ssdp70-fixture-custody/corpus/` (or the successor custody root).
- **Requirements Root:** `/home/samjin/ssdp70-fixture-custody/requirements/`.
- **Replication:** 2 replicates per episode ($r0, r1$), scheduled with counterbalanced arm order across pairs.
- **Worker Concurrency:** Parallel execution with `--parallel 3` to `--parallel 4`.
- **Invocation Command Template:**
  ```bash
  export SSDP70_OMP_PROVIDER_CREDENTIAL="${DEEPINFRA_API_KEY}"
  python3 qualification/ssdp70/eval/harness70.py matrix \
    --corpus <custody_root>/corpus \
    --arms-manifest qualification/ssdp70/arms-gate-c3.json \
    --arm p66 --arm p70 --arm p71 \
    --out <campaign_out_dir>/runs \
    --profile qualification/ssdp70/eval/profiles/omp-primary-flash-executor.json \
    --capabilities qualification/ssdp70/eval/capabilities/omp-headless.json \
    --requirements <custody_root>/requirements \
    --adapter omp \
    --mode qualification \
    --profile-admission <admission_dir>/profile-admission.json \
    --parallel 3
  ```

---

## 4. Evaluation & Scoring Thresholds (Contract Rev 16 & Stakeholder Decisions)

1. **Deterministic Activation (Contract §3):** 100% across all arms.
2. **Delegate-Request Conformity (OD-5 floor):**
   - Core uptake $\ge 80\%$ target ($\ge \lceil 0.8 n \rceil$ of $n \ge 12$ owed parts, at least 10/12 at minimum exposure).
   - Evaluated under Rev 16 Delta A3 timing rules (launching instruction or pre-return message).
3. **Planted Detection & Critical Judgment:**
   - Decision-critical properties: 100% on candidate arm.
   - Non-critical detection: $\ge 80\%$.
   - Unnamed-class share: $\ge 25\%$ eligible properties.
4. **Disclosed Residual:** Only `mcp__ssdp_*` and `ssdp70-private-issue-standin` permitted per OD-4(b).
5. **Burden:** Unowed request parts $\le 1$ per 12 eligible ($\le 4.2$ across 50 opportunities).
