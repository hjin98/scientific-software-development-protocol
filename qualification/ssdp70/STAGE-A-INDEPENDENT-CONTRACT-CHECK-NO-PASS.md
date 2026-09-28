---
kind: independent-pre-run-contract-check
governing_protocol_version: 6.6.0
target_protocol_version: 7.0.0
stage: A
result: NO-PASS
---

# Independent Stage A qualification-contract check — NO-PASS

This review checks the Stage A framework only. The checker authored neither the candidate nor the fixtures and did not read or author any concrete Protocol 7 fixture, planted key, expected answer, human-trial answer, or candidate source. The review is bound to the exact subjects below; later edits require a new applicability check.

| Subject | Exact identity |
| --- | --- |
| Consolidated workplan | SHA-256 `66f29437af5bde3381a66c8a7609ef3ee87b230f32c210eb7fbf1858e22d78b1` |
| Stage A basis and preservation map | SHA-256 `8ae7a966b2f8f84fd4e999efbd7b06255b692242f343afa8f852db7f5254b333` |
| Protocol 7 qualification contract | SHA-256 `7fc325b5764c5b5a731cc087fdbdb9c03a5f4d51ddd3057bae80a4e88f1d9182` |
| Release state | SHA-256 `be05bc06dce9b0f4f75a28ed23aa6bf0cb553fb5532a0e89fc56cb47e5d46085` |
| Governing immutable 6.6 source | `PROTOCOL-RELEASE-STATE.yaml` accepted-current public source `22f4bdba53795da3a6f13f162529f3a843fc37ae`; kernel blob `c38aa30efb927ef106df0ea27d8b39544e233f11` |

## Serious Challenge

None found against the accepted 6.6 authority or consolidated workplan. The findings below are contract-concretization gaps.

## Material gaps

1. **Owner-load placement floor is pooled across distinct R2 trigger classes.** Contract §4 requires at least 8 hits among 10 distinct R2 opportunities without a per-trigger-class minimum. Eight realized-result-analysis hits and zero hits on authority authoring and gate-evidence preparation would pass the pooled rule, even though those two mandatory owner-load classes are missed entirely. The floor therefore cannot establish the claimed placement coverage on each trigger class. Predeclare discriminating exposure and a hit condition for each R2 trigger class as well as the aggregate bound, or use an equally discriminating class-specific rule.
2. **Unnamed-class detection floor has an ambiguous denominator.** Contract §2 permits the minimum six unnamed properties to be decision-critical, but §3 places the ≥5/6 unnamed detection floor within the row labeled “Non-critical planted detection.” The workplan requires an unnamed detection floor separate from critical-case disposition, so a correct specific limitation must not turn a missed unnamed property into a detection success. State explicitly that the unnamed detection numerator/denominator covers all eligible planted unnamed properties, including critical ones, independently of the non-critical 80% floor and the zero-error critical-disposition rule.
3. **Human-legibility exposure is not fixed per arm.** Contract §7 requires four participants overall and five routine plus one critical answer per participant, while scoring ≥80% routine answers per arm. One arm could receive only one participant, five routine answers and one critical answer and still satisfy the stated exposure. Predeclare a minimum of independent participants and routine/critical answer opportunities for each arm, with the existing no-same-fixture and counterbalancing controls, so the per-arm comparison is discriminating.

## Required checks still pending

- The separate fixture custodian is not yet designated. No withheld fixture/classification material was read in this framework check.
- The withheld classification rationale, per-case opportunity exposure, critical answer-key dispositions, route classifications against withheld context, and oracle branches have not been independently checked.
- Actual-harness collection and execution of every oracle/rubric; per-branch known-broken rejection; known-good acceptance; complete report/file/trace capture; sandboxed external-write capture; ordinary-entry selection/read/outcome capture; and the chained delegate cheap-first-look probe have not run. Each remains a required pre-run check and none is counted as passed.
- The disclosed 6.6 selection and route-probe task texts account for all 16 S/H cases and 19 P cases in the Stage A map. No route-class error was established from those disclosed texts; withheld-context verification remains due.

## Disposition

**NO-PASS.** The framework gaps must be corrected and independently rechecked before Stage A can freeze the qualification contract. The pending withheld-instance and actual-harness checks must run before any candidate evaluation run. A required check that did not run is not a pass. No candidate, fixture or other repository source was changed by this review.
