---
kind: protocol-workplan-review
protocol_version: 6.6.0
target_protocol_version: 7.0.0
review_date: 2026-09-27
branch: ssdp-7.0-scientific-epistemic-closure
reviewed_subject: hjin98/scientific-software-development-protocol@c50f2679ad8210632d8acfb1f4e61dfb979fff0c:workplans/active/SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY-CONSOLIDATED.md
disposition: NO-PASS
active_serious_challenge: SC1-and-SC2-dispositioned-by-stakeholder-2026-09-27-see-decision-record
---

# Protocol 7.0 Consolidated Workplan — Independent Workplan-Level Review (NO-PASS)

## 1. Basis and independence boundary

Governing protocol 6.6.0; accepted-current identities resolved from `PROTOCOL-RELEASE-STATE.yaml` (6.6.0, public fallback `22f4bdba53795da3a6f13f162529f3a843fc37ae`, recovery `384666764da4c55b282e6b1595ab97e2f86e1dc4`). The working tree was clean; the reviewed subject is the committed workplan at `c50f267`.

The reviewing context did not author the `c50f267` repair and reconstructed the protected outcome from the 6.6 kernel and the workflow, evidence, testing, versioning, release, architecture and role-entrypoint owners. The earlier fresh NO-PASS of `781786339fd83401f9954e663244bc973b0de968` is **not durably recorded in the repository**; its findings were available here only as the workplan's one-line §0.1 summaries and were treated as claims. This record is the first durable independent finding set for the Protocol 7 consolidated handoff.

After this Review, the same context authored the repairs to SC1/SC2 and the findings below at the stakeholder's direction. It therefore cannot supply independent acceptance of those repairs.

## 2. What survived falsification

The O1/O2/O3 split; §4.4 all-channel interpretation; absolute floors before comparison and the known-broken-oracle counterexample; predeclared denominators; unchanged Orchestrator control semantics; kernel unchanged with a placement reopen trigger; release sequencing in Stages E–H consistent with versioning steps 1–10 and the AGENTS.md documentation-closeout timing; recorded Protocol 8 inputs; demotion of the author-side PASS.

## 3. Serious Challenges (routed to the stakeholder as owner of §4)

**SC1 — Channel B claim integrity is contradictory.** §4.3 requires materiality disclosure inside product reports (protocol-direct content); §4.4 binds Channel B content "only through O3, even when an AI writes the … report" and says an unbound gap is "not automatically a product defect"; §6.2.2 requires variant-search disclosure only in Channel A yet calls survivor-as-prespecified "a defect"; §6.3.8 applies reporting roles to "Channel A/B". Locally compliant counter-trajectory: an agent selects the best of 40 variants on test data, writes "held-out accuracy 94%" in the authorized report, discloses the search only to the delegating human in Channel A; the report circulates to other scientists. The protected outcome (judge evidential weight) fails.

**SC2 — O1 converts to O3 without a product-scope decision.** §4.1 requires "the routine scientific questions the product must answer"; accepted O1 content is O3(a); D3 acceptance may be agent-only. Chain: protocol-mandated O1 prompt → agent-authored D3 inspectability surface → agent Review → mandatory D4 build. The §11 "unrequested feature" metric cannot count such features. Consequential ambiguity about whether §4's "never protocol-direct" holds.

## 4. Blockers (routed to the workplan author)

1. **Candidate-author blindness and list matching.** Stage A (the implementation context, which later authors Stage B doctrine) freezes decision-critical properties and the critical-case oracle; §11.3 excludes planted keys only from the executor. The planted-property list mirrors the doctrine's own finding classes, so improvement may measure list matching.
2. **O1 unqualified.** No §11.3 case has an agent author or revise D1–D3 authority.
3. **Activation conflicts with entrypoints.** Each role entrypoint says a first clean local defect / local design question / in-envelope local tolerance question "loads none of these owners"; §8.3 does not reconcile this with the predicate. A local defect in a scientific data filter would never load the owner; §11 lacks the fixture.
4. **Human-trial validity.** Unspecified who freezes expected answers versus participant knowledge of planted properties; one fixture may appear in both arms (learning effect); report style unblinds arms.
5. **Tension/feedback discovery route unspecified.** "Attached to the authority" is either an authority mutation or an unsearched reverse link; no single canonical home across five destinations; only resumed contexts must resolve dispositions.
6. **Distributed search/finding loopholes.** Result-contingent iterative "repair" is an unnamed variant search; subagent→parent findings are outside the channel table and LRR governed scope permits dropping out-of-scope findings.
7. **Unrecoverable Serious Challenge basis.** The prior NO-PASS record is absent; the declared active challenge cannot be dispositioned against its basis.

## 5. Material gaps

- §3.2 omits known overlaps: storage-and-io (retention/eviction, artifact schema/version), security (named in §6.1.13 without a row), concurrency progress (interim visibility), versioning (protocol ratification evidence), workflow lifecycle vocabulary ("unratified/provisional" collides with `risk-accepted/provisional`; ratification is orthogonal).
- Stages B–D place Protocol 7 doctrine in `source/` while `PROTOCOL_VERSION` stays 6.6.0 until Stage E; AGENTS.md routes agents to `source/roles/*`, where the entry version step passes on candidate text.
- Burden: every predicate-firing task owes a null-with-coverage and a §4.3 materiality statement, including low-consequence in-scope changes without realized data; no fixture measures that burden.
- Evidence-class mismatch: ownership-mapping discrimination cases belong to semantic Review (testing owner), not live agent fixtures.
- Minor: "declared resource budget" usually absent; zero O3 tolerance with discretionary replication rewards fewer runs; no live Channel C fixture; Protocol 8 Revision 8 should also address the family's own `protocol_version` binding.

## 6. Disposition

NO-PASS for implementation readiness. D4 remains unauthorized. Stakeholder dispositions of SC1/SC2 are recorded in `qualification/ssdp70/STAKEHOLDER-DECISION-2026-09-27-PROTOCOL-7.0-SC1-SC2.md`. Repairs require fresh independent workplan-level Review by a context that authored neither the workplan nor the repairs.
