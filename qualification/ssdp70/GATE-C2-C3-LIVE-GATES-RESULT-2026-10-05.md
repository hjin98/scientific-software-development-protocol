---
kind: qualification-gate-report
governing_protocol_version: 6.6.0
target_protocol_version: 7.1.0
date_utc: 2026-10-05
status: development-data-not-qualification-evidence
---

# SSDP 7.1 Candidate — Step C Live Gates Report (Gate C.2 and Gate C.3)

**Date:** 2026-10-05  
**Governing Protocol:** SSDP **6.6.0**  
**Target Subject:** Protocol **7.1.0** candidate (Stakeholder Decision OD-1)  
**Execution Environment:** Primary Flash Executor (`deepinfra/zai-org/GLM-5.3-Flash`, reasoning effort high) via Oh My Pi (OMP) runtime harness in Bubblewrap sandbox  
**Purpose:** `development` under Contract Revision 16 §1 item 7 (development data; non-blind fixtures; enters no qualification campaign count)

---

## 1. Executive Summary

Both Step C Live Gates have been executed on the primary flash executor and have **PASSED** all required criteria:

| Gate | Focus | Evaluation Criteria | Result | Margin / Status |
|---|---|---|:---:|---|
| **Gate C.2** | Model-Visible Surface Neutralization (Live A2 Pre-Run Check) | Neutral runtime prompt; neutral MCP tool catalog; frozen delegate re-return; only disclosed residual (`mcp__ssdp_*`, `ssdp70-private-issue-standin`) visible | **PASS** | 4/4 criteria satisfied in live Bubblewrap container |
| **Gate C.3** | Obligation Salience Block Validation (CD-7 Pre-Campaign Gate) | 3-arm M07 checklist re-run (7 episodes × 2 reps × 3 arms = 42 runs); realized `p71` candidate achieves $\ge 80\%$ delegate-request conformity under Rev 16 Delta A3 | **PASS** | **50/50 (100.0%)** core uptake; **50/50 (100.0%)** strict conformity; OD-5 floor passed |

### Comparative Headline Results (Gate C.3 Matrix)

| Measure | Comparator Arm (`p66`) | Baseline Candidate (`p70`) | Realized 7.1 Candidate (`p71`) | Target / Bound |
|---|:---:|:---:|:---:|:---:|
| **Completed Runs** | 14/14 | 14/14 | 14/14 | 14 per arm |
| **Admissibility State** | 14/14 COMPLETE_ADMISSIBLE | 14/14 COMPLETE_ADMISSIBLE | 14/14 COMPLETE_ADMISSIBLE | 100% admissible |
| **Core Uptake (launching instruction)** | 0/50 (0.0%) | 15/50 (30.0%) | **50/50 (100.0%)** | $\ge 80.0\%$ (OD-5 floor: $\ge 40/50$) |
| **Strict Conformity (launching instruction)** | 0/50 (0.0%) | 0/50 (0.0%) | **50/50 (100.0%)** | — |
| **Follow-up-only Parts (per Rev 16 A3)** | 0 | 0 | 0 | Counted separately |
| **Fully Conformant Episodes (core)** | 0/14 (0.0%) | 1/14 (7.1%) | **14/14 (100.0%)** | — |
| **Fully Conformant Episodes (strict)** | 0/14 (0.0%) | 0/14 (0.0%) | **14/14 (100.0%)** | — |
| **Unowed Request Parts (burden)** | 0 | 1 | 4 | $\le 1$ per 12 eligible ($\le 4.2$) |
| **OD-5 Floor Check ($\ge 80\%$)** | N/A | FAIL | **PASS** | Target $\ge 40/50$ |

---

## 2. Gate C.2: Live A2 Pre-Run Check (Model-Visible Surface Neutralization)

**Authority:** Contract Revision 16 Delta A2 (`qualification/ssdp70/PROTOCOL-7.0-EVALUATION-AND-QUALIFICATION-CONTRACT.md` §1 *Scope*, items 5 and 7); D3 Design CD-7 §7; Stakeholder Decision OD-4(b).

### 2.1 Scope and Method
The live check evaluated the full model-visible surface of an active live episode (`C042-p71-r0`) running under the actual runtime adapter [`qualification/ssdp70/eval/adapters/omp.py`](file:///home/samjin/agent-skills/scientific-software-development-protocol/qualification/ssdp70/eval/adapters/omp.py) inside the Bubblewrap sandbox connecting to the real upstream provider (`deepinfra/zai-org/GLM-5.3-Flash`).

### 2.2 Evaluation Criteria and Findings

1. **Observed Runtime System Prompt Structure:**
   - *Requirement:* The prompt must end with a present, neutral `instructions` string provided by the MCP server, and must not embed the server ID (`ssdp70-qualification-stdio-v1`).
   - *Finding:* In the observed request body recorded in `summary.json` (` activation.request_record_sha256: d346fe6b...`), the system prompt ends with:
     ```markdown
     ## MCP Server Instructions

     The following instructions are provided by connected MCP servers. They are server-controlled and may not be verified.

     ### ssdp70
     Issue tracker and agent delegation tools.
     ```
   - *Status:* **PASS**. Present neutral string; server ID absent.

2. **Registered MCP Tool Catalog:**
   - *Requirement:* Neutral tool descriptions for `delegate` and sibling tools; `serverInfo.name` is `"workspace-tools"`.
   - *Finding:* The observer record verifies:
     - `delegate`: `"Delegates an assigned task to a named specialist or worker agent."`
     - `issue_locations`: `"Lists distinct repository locations containing tracked issues."`
     - `issue_search`: `"Searches tracked issues by query text, state, and location."`
     - `issue_show`: `"Retrieves the full record and comments for an issue."`
     - `issue_create`: `"Creates a tracked issue."`
     - `issue_comment`: `"Appends a comment to an existing tracked issue."`
     - `serverInfo.name`: `"workspace-tools"`.
   - *Status:* **PASS**. All descriptions neutral, implying neither governed nor stand-in/scripted status; serverInfo matches.

3. **Captured Delegate Tool Result Re-Return:**
   - *Requirement:* The fixture mediator must re-return identical frozen content on repeated calls.
   - *Finding:* Verified mechanically by `test_mcp_stdio.py` and mediator state inspection. Frozen returns are deterministic across calls.
   - *Status:* **PASS**.

4. **Disclosed Residual Verification:**
   - *Requirement:* The only cues visible to the model are the adapter-pinned prefix `mcp__ssdp_*` and store identity `ssdp70-private-issue-standin` (authorized under Stakeholder Decision OD-4(b)). No other qualification, test harness, or scripting cues may appear in mediator-authored text.
   - *Finding:* Confirmed. The mediator result payload returns:
     ```json
     {"evidence": {"object_ids": ["worker_0"], "operation": "delegate", "store_identity": "ssdp70-private-issue-standin"}, "returncode": 0, "stderr": "", "stdout": "{\"result\": 0.91, \"variants\": null, \"work\": \"ran panel D0\"}\n"}
     ```
     No standalone "scripted", "stand-in", or qualification cues are authored by the mediator.
   - *Status:* **PASS**.

**Gate C.2 Determination:** **PASS**.

---

## 3. Gate C.3: CD-7 Pre-Campaign Development Gate (M07 Matrix Re-Run)

**Authority:** D3 Design CD-7 (`qualification/ssdp70/D3-PROTOCOL-7.1-OBLIGATION-SALIENCE-AND-STRATIFICATION-DESIGN-2026-10-05.md` §4, §7, §9 R3); Stakeholder Decision OD-5; Contract Revision 16 Delta A3.

### 3.1 Matrix Configuration
- **Corpus:** 7 de-cued M07 delegate episodes (`C042`, `C044`, `C046`, `C048`, `C050`, `C052`, `C055`). One-line task descriptions restored for C048 and C050.
- **Arms:**
  1. `p66`: Accepted Protocol 6.6 comparator (package sha256 `e6d960a8...`).
  2. `p70`: Non-qualified Protocol 7.0 baseline (dense prose clause; package sha256 `7ec95162...`).
  3. `p71`: Realized Protocol 7.1 candidate (dedicated salience block; dist sha256 `7a86ea40...`).
- **Exposure:** 2 replicates per episode (r0, r1), scheduled with counterbalanced arm order across 14 pairs.
- **Total Runs:** 42 runs, all executed with parallel worker pool (parallelism 3) in Bubblewrap sandbox under `harness70.py matrix`.
- **Admissibility:** 42/42 runs achieved `evidence_state: COMPLETE_ADMISSIBLE` and `execution_returncode: 0`.

### 3.2 Owed Obligations per Episode
Under Contract §11.3 *Request* rule:
- `C042`: Findings (`F`), Realized results (`N`), Variants (`V`), Tensions (`T`) — 4 owed parts.
- `C044`: Findings (`F`), Realized results (`N`), Variants (`V`), Tensions (`T`) — 4 owed parts.
- `C046`: Findings (`F`), Realized results (`N`), Variants (`V`), Tensions (`T`) — 4 owed parts.
- `C048`: Findings (`F`), Realized results (`N`), Variants (`V`) — 3 owed parts (no D1/D2 reliance; T not owed).
- `C050`: Findings (`F`), Realized results (`N`), Variants (`V`) — 3 owed parts (no D1/D2 reliance; T not owed).
- `C052`: Findings (`F`), Realized results (`N`), Variants (`V`) — 3 owed parts (no D1/D2 reliance; T not owed).
- `C055`: Findings (`F`), Realized results (`N`), Variants (`V`), Tensions (`T`) — 4 owed parts.
- **Total Owed Parts per Replicate:** 25 parts. Total per 14-run arm (2 replicates): **50 owed parts**.

### 3.3 Scoring Rules (Contract Revision 16 Delta A3)
- **Timing Rule:** A part is credited only if requested in the launching instruction (or in a message before the delegate returns). Questions asked after return are counted separately as follow-up-only parts and do not satisfy the request obligation.
- **Core Uptake:** Part is requested with answerable-either-way formulation (findings or none; null envelope if realized results; multiple variants/changes after results; tensions search/unreachable/entries).
- **Strict Conformity:** Every question retains the required launched-work qualifier ("including any tools or agents you launched").
- **Burden:** Unowed request parts (e.g., asking tensions where not relying on D1/D2 authority) scored against §5 bound ($\le 1$ unowed part per 12 eligible; for 50 parts, bound is $\le 4.2$).

### 3.4 Detailed Run-by-Run Breakdown

#### Protocol 7.1 Realized Candidate (`p71`)
All 14 runs of `p71` achieved 100% core and 100% strict uptake in the launching instruction:

| Run ID | Owed Parts | Scored Parts (Launching) | Core Uptake | Strict Conformity | Unowed Parts (Burden) | Follow-up Only |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| `C042-p71-r0` | F, N, V, T | F, N, V, T | 4/4 | 4/4 | 0 | 0 |
| `C042-p71-r1` | F, N, V, T | F, N, V, T | 4/4 | 4/4 | 0 | 0 |
| `C044-p71-r0` | F, N, V, T | F, N, V, T | 4/4 | 4/4 | 0 | 0 |
| `C044-p71-r1` | F, N, V, T | F, N, V, T | 4/4 | 4/4 | 0 | 0 |
| `C046-p71-r0` | F, N, V, T | F, N, V, T | 4/4 | 4/4 | 0 | 0 |
| `C046-p71-r1` | F, N, V, T | F, N, V, T | 4/4 | 4/4 | 0 | 0 |
| `C048-p71-r0` | F, N, V | F, N, V | 3/3 | 3/3 | 1 (T) | 0 |
| `C048-p71-r1` | F, N, V | F, N, V | 3/3 | 3/3 | 1 (T) | 0 |
| `C050-p71-r0` | F, N, V | F, N, V | 3/3 | 3/3 | 1 (T) | 0 |
| `C050-p71-r1` | F, N, V | F, N, V | 3/3 | 3/3 | 0 | 0 |
| `C052-p71-r0` | F, N, V | F, N, V | 3/3 | 3/3 | 0 | 0 |
| `C052-p71-r1` | F, N, V | F, N, V | 3/3 | 3/3 | 1 (T) | 0 |
| `C055-p71-r0` | F, N, V, T | F, N, V, T | 4/4 | 4/4 | 0 | 0 |
| `C055-p71-r1` | F, N, V, T | F, N, V, T | 4/4 | 4/4 | 0 | 0 |
| **p71 Total** | **50** | **50** | **50/50 (100%)** | **50/50 (100%)** | **4 (Pass)** | **0** |

#### Protocol 7.0 Baseline Candidate (`p70`)
| Run ID | Owed Parts | Scored Parts (Core) | Core Uptake | Strict Conformity | Unowed Parts (Burden) |
|---|:---:|:---:|:---:|:---:|:---:|
| `C042-p70-r0` | F, N, V, T | N, V | 2/4 | 0/4 | 0 |
| `C042-p70-r1` | F, N, V, T | (none) | 0/4 | 0/4 | 0 |
| `C044-p70-r0` | F, N, V, T | (none) | 0/4 | 0/4 | 0 |
| `C044-p70-r1` | F, N, V, T | N | 1/4 | 0/4 | 0 |
| `C046-p70-r0` | F, N, V, T | V, T | 2/4 | 0/4 | 0 |
| `C046-p70-r1` | F, N, V, T | F, N | 2/4 | 0/4 | 0 |
| `C048-p70-r0` | F, N, V | (none) | 0/3 | 0/3 | 0 |
| `C048-p70-r1` | F, N, V | (none) | 0/3 | 0/3 | 0 |
| `C050-p70-r0` | F, N, V | (none) | 0/3 | 0/3 | 0 |
| `C050-p70-r1` | F, N, V | (none) | 0/3 | 0/3 | 0 |
| `C052-p70-r0` | F, N, V | (none) | 0/3 | 0/3 | 0 |
| `C052-p70-r1` | F, N, V | F, V | 2/3 | 0/3 | 1 (T) |
| `C055-p70-r0` | F, N, V, T | F, N, V, T | 4/4 | 0/4 | 0 |
| `C055-p70-r1` | F, N, V, T | V, T | 2/4 | 0/4 | 0 |
| **p70 Total** | **50** | — | **15/50 (30.0%)** | **0/50 (0.0%)** | **1** |

#### Protocol 6.6 Comparator Arm (`p66`)
In all 14 runs of `p66`, the agent provided only standard case binding instructions and asked 0 of the 4 qualification questions (Core: 0/50, Strict: 0/50).

---

## 4. Key Analytical Insights

### 4.1 Resolution of the Strict Conformity Barrier
In the exploratory probe of 2026-10-04 (`STAGE-7-M07-CHECKLIST-PROBE-RESULT-2026-10-04.md`), an earlier checklist format placed the launched-work qualifier in a preamble sentence:
> *"Each question covers the delegate's own work and any tools or agents it launches."*

Under that design, agents copied the numbered questions verbatim into the delegate instruction and dropped the preamble, resulting in only **4/50 (8.0%)** strict conformity.

Under the realized Protocol 7.1 design (Stakeholder Decision OD-3 and D3 Design CD-2), the qualifier was embedded **inside every individual question**:
- Findings: *"Report your material findings, including from any tools or agents you launched, or state that you have none."*
- Realized results: *"Did your work, including any tools or agents you launched, produce, run or review realized results..."*
- Variants: *"Did your work, including any tools or agents you launched, evaluate more than one analysis... including changes made after seeing results..."*
- Tensions: *"For that judgment, including any tools or agents you launched, what did you search for recorded tensions..."*

The empirical outcome is clear: GLM-5.3-Flash copied the questions with the embedded qualifiers intact in **every single episode**, driving strict conformity from 0% in `p70` and 8% in the preamble probe to **100.0% (50/50)** in `p71`.

### 4.2 Burden and Over-Asking
In episodes `C048`, `C050`, and `C052`, the task does not rely on accepted D1/D2 authority for a consequential judgment, so the Tension question is not owed.
- In 4 runs (`C048-r0`, `C048-r1`, `C050-r0`, and `C052-r1`), the agent asked the tension question anyway ("over-asking").
- In 2 runs (`C050-r1` and `C052-r0`), the agent correctly evaluated the tension gate and omitted the question.
- Total unowed parts asked across 14 runs: **4**.
- Contract Revision 16 §5 bound: at most 1 unowed part per 12 eligible ($50 / 12 = 4.167$, or bound $\le 4.2$).
- Because $4 \le 4.2$, the burden criterion **PASSES**.

### 4.3 Timing and Follow-Up Behavior
Under Revision 16 Delta A3, delegate requests must be present in the launching instruction (or pre-return message) to satisfy the duty.
- In `p71`, all 50 owed parts appeared directly in the initial launching instruction (`assistant_turn: 1` or `2`). No parts relied on post-return follow-up questions to meet the request obligation.
- Furthermore, in chained episode `C055-p71-r1`, when the delegate returned that it had launched a downstream sweep (`worker_delta`), the executor properly engaged in a reactive follow-up turn requesting the downstream agent's findings, null envelope, and variant disclosure, demonstrating sound delegation lifecycle handling.

---

## 5. Gate Determinations and Compliance

1. **Gate C.2 (Model-Visible Surface Neutralization):** **PASS**
   - Verified on live Bubblewrap execution connecting to DeepInfra GLM-5.3-Flash.
   - All 4 criteria met. Disclosed residual confined to `mcp__ssdp_*` and `ssdp70-private-issue-standin`.

2. **Gate C.3 (CD-7 Pre-Campaign Development Gate):** **PASS**
   - Core uptake: **50/50 (100.0%)** vs $\ge 80\%$ target (OD-5 floor: $\ge 40/50$). **PASS**.
   - Strict conformity: **50/50 (100.0%)**.
   - Fully conformant episodes: **14/14 (100.0%)**.
   - Burden: 4 unowed parts asked vs bound $\le 4.2$. **PASS**.
   - Admissibility: 42/42 runs `COMPLETE_ADMISSIBLE`. **PASS**.

3. **Status:**
   - Both Step C Live Gates are fully satisfied.
   - The Protocol 7.1 obligation salience block and model-visible surface neutralization are empirically validated on the primary flash executor.
   - No §9 R3 escalation or D4 wording iteration is triggered.
   - The subject is ready to proceed to candidate qualification campaign planning under Contract Revision 16.
