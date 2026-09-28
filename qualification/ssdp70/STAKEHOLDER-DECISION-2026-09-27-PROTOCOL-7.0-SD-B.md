---
kind: stakeholder-decision
protocol_version: 6.6.0
target_protocol_version: 7.0.0
decision_authority: stakeholder
date: 2026-09-27
review_evidence: qualification/ssdp70/WORKPLAN-REVIEW-PROTOCOL-7.0-665A5CC-NO-PASS.md
decided_question: SD-B ordinary-route burden (consolidated workplan section 11.5)
---

# Stakeholder Decision — Protocol 7.0 SD-B

## Question

The `665a5cc` Review found that the 6.6 ordinary-route burden capability was unprotected on 6.6's own reference routes and that the Protocol 7 entrypoint additions had no budget set in advance (B2). The repair asked the stakeholder to choose between preserving 6.6's final-rule cap of at most 1.10 × the per-route median, which leaves about 700 B for both additions on the 7,057 B D4 entrypoint, and superseding it with a 1,000 B per-role-entrypoint budget (about 1.14 on the D4 entrypoint, still below 6.5's 8,360 B).

## Decision: SUPERSEDE

The stakeholder selected supersession and stated the governing principle:

> A size budget is a compression recommendation, not a reason to break a lossless condition.

Consequences for the workplan:

- 6.6's 1.10 per-route cap is superseded for Protocol 7 and recorded as an explicit capability supersession (§13.16).
- The 1,000 B per role entrypoint is a **compression target**, subordinate to the frozen required clause elements. Every required element is a lossless condition: no element is dropped, weakened or moved out of the consumed surface to meet the target.
- Exceeding the target is admissible only when, after compression, the excess is attributable to carrying required elements losslessly. The excess is reported with that attribution. Excess from redundancy, inlined owner doctrine or non-required content is a D4 defect to fix.
- The target does not license inlining owner doctrine (I66-3) or kernel placement, and it does not relax non-size floors (owner and selection false activation, route probes, no-lookup, version rules).

## Boundary

This decision settles SD-B only. It does not accept the repaired workplan, close the Review's other findings, or authorize D4. The repaired workplan still requires fresh independent workplan-level Review.
