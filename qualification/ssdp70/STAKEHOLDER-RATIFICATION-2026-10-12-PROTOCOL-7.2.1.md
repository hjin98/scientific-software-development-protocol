---
kind: stakeholder-ratification
status: ratified
protocol_version: 6.6.0
target_protocol_version: 7.2.1
candidate_ref: aaeaf8b6b2121b9fb8aba31917c8265649c43954
semantic_ref: aaeaf8b6b2121b9fb8aba31917c8265649c43954
review_evidence: hjin98/scientific-software-development-protocol@04827e657cd156a6ea664a04869f73d15e8bcbed:qualification/ssdp70/INDEPENDENT-REVIEW-2026-10-12-PROTOCOL-7.2.1-PASS.md
ratification_authority: stakeholder
authorization_source: eighteenth-ruling-set
designation: accepted-with-conditions
date: 2026-10-12
---

# Stakeholder Ratification — Protocol 7.2.1 (Accepted with conditions)

The stakeholder accepted Protocol 7.2.1, the exact independently reviewed semantic candidate

`P721 = aaeaf8b6b2121b9fb8aba31917c8265649c43954`

(protocol `source/` and `dist/` identical to the S3-reviewed `52ac475ce81d89b3e8ccb7c393fa0daa028d01b0`; documentation
closeout only). The governing independent Review is the PASS record named in `review_evidence` above. Authority: the
eighteenth ruling set and its designation amendment in `qualification/ssdp70/qual-v2/S4-STAKEHOLDER-RULINGS-2026-10-08.md`.

## The decision, in the stakeholder's words

> "I think we should conclude regardless. 7.2.1 is fragile, but in my opinion, passable. And since the evidence of current
> and further improvement are slim, we should accept 7.2.1 as a weakly qualified, accepted version. Any further improvement
> in my opinion would really require deterministic machinery, which is the work of the future SSDS 8.0+ design. I believe
> we've reached the success limit of a semantic-based protocol."

Designation amendment, same day:

> "change that wording to "Accepted" or "Accepted with conditions", where the condition is a user warning that the protocol
> should not be taken as statistically robust. The user of the protocol should be warned that a purely language-based skill
> can never guarantee 100% compliance rate, and reliability depends on the model's strength and intelligence. This is what
> our multiple-round, eventually failed qualification process have showed us. You should include the lessons we learned as
> part of the ratification summary [...]"

Later the same day: "Complete the remaining closeout yourself."

## Designation and condition

**Accepted with conditions.** 7.2.1 is accepted by stakeholder decision over a statistical no-go. It is not statistically
qualified and must never be described as qualified or as a statistical go.

The condition is the user warning, carried as the closing section of the root README and in the CHANGELOG 7.2.1 entry:
the protocol is not statistically robust; a purely language-based skill can never guarantee 100% compliance; reliability
depends on the strength and capability of the model.

## Basis

- Independent S3 review PASS (semantic content) and S7 review PASS (frozen candidate, documentation, release state,
  acceptance); repository acceptance complete (438 regression tests with no skips, 385 Core tests).
- Measurement: 7.2.1 vs 7.2.0 on the same 122 main-panel episodes (executor GLM-5.3-Flash, evaluator MiMo-V2.6-Flash), frozen
  rule: **no-go**. Narration improvement (P1) FRAGILE — favourable on resolved items (10.4% vs 17.1% failing) but not robust
  to evaluator-unresolved items; retained duties (P2) and outcome items (P3) robustly non-inferior; one harm flag
  (delegate_request.unowed.R, a single failure vs none), knowingly accepted.
- The design lead had recommended no ratification under the frozen rule; plan §7 makes "go" a recommendation, not a
  precondition of the stakeholder's decision. The frozen rule's own operating characteristics gave a favourable candidate
  only about a 13% chance of "go", so the no-go is weak evidence against the candidate.
- 7.2.0 remains NOT QUALIFIED history and is not separately accepted. The 7.x semantic-protocol line concludes at 7.2.1.

## Ratification summary: what the study taught

Full record: `qualification/ssdp70/PROTOCOL-7X-QUALIFICATION-STUDY-EVIDENCE-AND-LESSONS-2026-10-12.md`.

About language-based protocols:
1. Compliance is probabilistic and model-dependent at every layer — activation (a skill loaded in 13 of 122 Flash runs),
   loading further text, asking each owed question. Stronger models do better, never reliably.
2. Only text in context acts: conditional "read the owner when ..." instructions hit 37%; inline structured checklists
   raised uptake from 28% to 92%.
3. Activation must be deterministic (explicit commands), never wording.
4. Errors are two-sided: more inline duty text produced narration where none was owed.
5. Some behaviours (detection, claim integrity, unauthorized mutation, version ordering) did not respond to protocol text
   in any arm, 6.6 included.

About measuring them:
6. Absolute floors measure the model; paired, calibrated comparisons measure the protocol.
7. The LLM evaluator's unassessable tail (about 4–11%), not sample size, set the power of both campaigns; simulate operating
   characteristics before spending and redesign when a good candidate cannot pass.
8. Validate oracles and instruments before runs; additive repair loops on measurement machinery diverge.
9. Frozen rules, custody, blinding and independent review worked and caught real defects each round.

Direction (stakeholder, not a plan): further reliability requires deterministic machinery — the future SSDS 8.0+ design.

This record is the human acceptance decision. It does not replace the independent Review and does not by itself publish a
public fallback, establish recovery, advance `accepted_current`, or merge to `main`.
