---
kind: stakeholder-decision-record
governing_protocol_version: 6.6.0
target_protocol_version: 7.1.0 (candidate; non-governing)
decision_date_utc: 2026-10-06
status: stakeholder-adopted
decides: PROTOCOL-7.1-REQUALIFICATION-PLAN.md §4 SD-1..SD-7
---

Governing SSDP version: 6.6.0.

# Stakeholder decision: Protocol 7.1 requalification parameters

**Verbatim answer.** After the analyst presented SD-1..SD-7, each with a recommendation (requalification plan §4), the stakeholder answered: **"Proceedwith your recommendation."** Each recommendation is adopted as written:

| # | Decision adopted | Realized in |
|---|---|---|
| SD-1 | Candidate subject: package `7a86ea4011034f8abf793c1c06d523577356a5b1a7167b267dda53e567a2892e` bound at commit `58fd67ba15c937040f51e56dc26f30ad7a907ac3`. That is the first commit carrying the package; it is byte-identical through `ee3a2b5`. | `requal71/campaign-parameters.env` `P71_ARM`, `P71_SHA` |
| SD-2 | Fresh custody store under contract §1 item 9's attestation path from creation: access log append-only and outside the freeze list; `custody-stat` before and after every role session; written role attestations. The store lives at `/home/samjin/ssdp71-fixture-custody` (new; never the 2026-09-28 store). | `CUSTODY`; custodian work package C-1; runbook custody procedure |
| SD-3 | Wall-clock timeouts: main 2400 s, burden 2400 s, routing 900 s, ordinary 600 s; worker parallelism 4. Turn caps stay contract-fixed (60/60/8/3). | `TIMEOUT_*`, `PARALLEL` |
| SD-4 | 1 replicate per episode for the first campaign | Custodian C-2 `replicates: 1` |
| SD-5 | Run the development probe (plan phase P2, runbook Phase D) before commissioning fresh fixtures | `requal71/dev-probe/` work order (this date) |
| SD-6 | Custodian and pre-run checker are two fresh capable contexts, briefed only with their own documents and plan §2 | Commissioned after the SD-5 go/no-go |
| SD-7 | No transient-provider rerun rule for the first campaign. Such a run stays non-PASS and is reported. | Plan §6 G-2 remains unbuilt (fail-closed) |

**Scope.**
- These are R-op and identification values within contract revision 16. None changes a floor, threshold, exposure minimum, turn cap or comparator.
- SD-1 identifies the subject before runs, as Rev 16 A1 requires.
- The P2 probe is `development` purpose (contract §1 item 7). It runs on the disclosed 2026-09-28 corpus, enters no qualification count, and informs only the go/no-go on commissioning P3.
