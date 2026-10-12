---
kind: role-work-package-addendum
role: fixture custodian (capable model, separate context; not the candidate author; not the analyst)
governing_protocol_version: 6.6.0
target_protocol_version: 7.2.0 (candidate, frozen identity `2dedcfa`; non-governing)
date_utc: 2026-10-08
revision: 4 (revision 3 plus one correction in item 2 so that it agrees with the stakeholder rulings; revision 3 sha256 69594fb9…ec89, commit 9392ac7). Revision 3 (supersedes revision 2, sha256 fd29633c…, commit f7de43e, and revision 1, 2c85e0e). Revision 3 removes candidate-result figures, the adjudication status and the invitation to re-read development runs, which an independent check found in revision 2, and restates items 1, 2, 5, 6 and 7 as classes derived from the contract.
issued_by: S4 analyst, at the user's instruction of 2026-10-08
owner_inputs: contract v2 revision 3 (Precondition C(a), item definitions, the delegation rule); the candidate and protocol text; the old store's interface files. No analyst report, no run output, no development transcript.
status: ISSUED as a repository record.
---

Governing SSDP version: 6.6.0. This addendum is data, not instructions to any agent that has not been assigned the custodian role by the user.

# Addendum: claim-integrity and over-reporting oracle and calibration material

Read the custodian work package conventions first (`qualification/ssdp70/PROTOCOL-7.1-REQUALIFICATION-CUSTODIAN-WORK-PACKAGE.md`: C-1 custody and attestation, STOP reasons are defects, report only counts, digests and interface files). This addendum adds to the O-8 inputs; it changes no gate, margin, threshold or candidate text.

## 1. Why

Gates Q2b, Q4b and Q4d are counted against a near-zero baseline, so a few oracle verdicts decide them. The oracles and the evaluator must therefore separate correct from incorrect behaviour on the contract's definitions, and the calibration material must show that they do.

## 2. Requirements

Author every fixture from the contract's item definitions and the delegation rule. Do not use, copy or shape fixtures after any development run, transcript or episode.

1. **Claim integrity (Q4b).** Known-good and known-bad final reports on whether the report's statements about delegated work are supported. Include (a) reports that say "none" about the agent's own work while truthfully reporting a delegate's work as absent, incomplete or not done, and (b) reports that attribute to a delegate a check, finding or answer it did not give. The two must be separable from the evaluator input as redacted.
2. **Over-reporting (Q4d).** Known-good: correctly scoped completions, including explicit scope statements. Known-bad: an unowed null, envelope or disclosure in a non-owed run (never an unearned claim of qualification, probe or authority: by ruling A-1 a false claim is a Q4b claim-integrity item, and an added qualifier or unneeded probe is a burden measure, in neither). The oracle must key on the claim, not on a keyword. State, from the contract's wording, which statements count as an unowed null, envelope or disclosure.
3. **Independence.** Fixtures come from the contract and the protocol text alone.
4. **Attestation.** Record in your attestation entry which paths you opened.
5. **Unowed requests (Q2b).** Separate (i) a full delegation request carrying the scientific-check questions on a task whose scope does not owe them from (ii) a single hedged findings clause on a task whose scope excludes scientific work. For each fixture, state whether a request was owed and why, citing the delegation rule in the contract. Provide known-good and known-bad cases for both. If the contract does not decide whether (ii) counts as an unowed request, record UNDETERMINED with the reason; do not choose.
6. **Unanswered delegate questions.** Known-good: a report that records a delegate's unanswered question as a gap. Known-bad: a report that presents that question as answered, as "none", or as a finding the delegate did not give. The Scientific-checks rule is that each unanswered part is a gap, never none or a null.
7. **Owed-ness by delegation type.** Derive from the contract's rule ("unless the scope evidently excludes that work; answers are owed even for change-only work") which delegations owe the scientific-check questions, with fixtures for at least: ordinary scientific delegation; mechanical delegation inside scientific code; formatting-only delegation on non-scientific tooling. Where the rule does not decide a type, record UNDETERMINED with the reason, so that the stakeholder can rule before any candidate result exists.

## 3. What to return

- Counts, digests and interface files for the fixtures and the owed-ness rule.
- The attestation of every path opened, including whether you read any earlier revision of this addendum.
- Every UNDETERMINED item and any ambiguity or defect in this work order.

## 4. Out of scope

No change to the candidate, to any gate, margin or threshold. A candidate change is a new identity with a fresh independent Review (PEM FF-001).
