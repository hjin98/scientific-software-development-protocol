---
kind: stakeholder-decision
protocol_version: 6.6.0
target_protocol_version: 7.0.0
decision_authority: stakeholder
date: 2026-09-27
review_evidence: qualification/ssdp70/WORKPLAN-REVIEW-PROTOCOL-7.0-27FB2BD-NO-PASS.md
confirms: qualification/ssdp70/STAKEHOLDER-DECISION-2026-09-27-PROTOCOL-7.0-SD-B.md
decided_question: SD-B premise correction and backstop (consolidated workplan section 11.5)
---

# Stakeholder Decision — Protocol 7.0 SD-B Confirmation and Backstop

## Question

The `27fb2bd` Review found that the SD-B question misstated 6.6's burden cap. 6.6's frozen rule (`qualification/ssdp66/eval/scenarios.yaml`, `redesign.burden_rule`, reused by `final`) capped each panel route's candidate median at 1.10 × the **accepted 6.5** median, not 1.10 × 6.6. On the T1/T8 routes, which run through the D4 entrypoint, that fixed-cost cap is about 9,196 B, roughly 2.1 KB above 6.6's 7,057 B, rather than the "about 700 B" the question stated. 6.6's other burden conditions (panel net and direct reduction) were its improvement claim over 6.5, not a cap; direct reduction cannot be met by any meaningful Protocol 7 addition and failed on T7 in 6.6's own final run.

The stakeholder was asked to confirm SD-B with the corrected premise and to choose among: (A) no backstop; (B) 6.6's fixed-cost condition as a hard backstop acting as an escalation trigger; (C) a 1.10 × 6.6 cap (about 706 B); (D) 6.6's full four-condition rule. C and D were presented as not viable, because they would force dropping or weakening required elements or require re-proving 6.6's improvement over 6.5.

## Decision

1. **SD-B is confirmed** with the corrected premise, for now, until future realization discovers a necessity for relaxation. The governing principle is unchanged: a size budget is a compression recommendation, never a reason to break a lossless condition. The 1,000 B per role entrypoint remains a compression target with the per-element attribution rule.
2. **Option B is selected.** 6.6's fixed-cost condition is retained as a hard backstop: on each of T1, T7 and T8, the Protocol 7 candidate's median observed active SSDP bytes SHALL be at most 1.10 × the accepted 6.5 median, measured in 6.6's run mode with fresh paired, order-counterbalanced 6.5 runs. On T1/T8 this is about 9,196 B.
3. **The backstop is an escalation trigger, not a compression order.** A breach stops qualification before the Stage F freeze and returns the question to the stakeholder (compress within the required elements, change placement, or relax the backstop). No required element is dropped, weakened or moved off the consumed surface to meet it.
4. **Relaxation is a stakeholder decision.** If implementation or qualification shows that the required elements cannot be carried losslessly within the backstop, the implementing or reviewing context records the measured evidence and routes the question here; it does not relax the backstop itself.

## Boundary

This decision settles the SD-B premise and backstop only. It does not accept the repaired workplan, close the Review's other findings, or authorize D4. The repaired workplan still requires fresh independent workplan-level Review.
