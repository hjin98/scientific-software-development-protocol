---
kind: ssdp65-post-freeze-semantic-mutation-set
status: executed-semantic-review-no-pass
p1: b565e28aeacea002cefe27e6b9594fe99d653c0a
author: fresh-independent-GPT-5.6-Sol-review-context
date: 2026-09-24
---

# Fresh Post-freeze Semantic Mutation / Counterexample Set

## 1. Oracle split

Machine-readable/state/schema/generated properties are judged by executable/structural owners where available. Arbitrary prose-semantic adequacy is judged by independent semantic Review. No exact-string semantic theorem prover is introduced.

“Detected” below means the current P1 owner/oracle rejects the mutated meaning for the property it actually owns. “Survives” means a materially wrong state/representation can satisfy the current P1 check or current operational text.

## 2. Fresh mutants

| ID | Class | Fresh mutation/counterexample | Oracle / outcome |
| --- | --- | --- | --- |
| PF65-M01 | state/evidence | Set Review PASS with a syntactically valid immutable evidence route whose commit/path does not contain a Review record for the candidate. | SURVIVES release_state validation because evidence_ref is regex-checked only. B65-R1. |
| PF65-M02 | state/evidence | Point Review PASS at immutable Review evidence for a different semantic candidate. | SURVIVES release_state validation; exact candidate binding is not inspected. B65-R1. |
| PF65-M03 | lifecycle | Perform a legitimate owner-only transition from review NOT_RUN to NO_PASS/PASS while keeping accepted-current/ratification/public/recovery otherwise legal. | Schema permits it, but live test hardcodes NOT_RUN and fails. B65-R2. |
| PF65-M04 | lifecycle | Promote accepted_current to 6.5 before terminal Review/ratification/public/recovery agreement. | DETECTED by release_state terminal-state rule. |
| PF65-M05 | lifecycle | Publish a candidate public fallback different from semantic_ref after PASS/RATIFIED. | DETECTED by exact-candidate equality rule. |
| PF65-M06 | lifecycle | Set candidate recovery_ref equal to public_source_ref. | DETECTED by distinctness rule. |
| PF65-M07 | lifecycle | Add historical 6.4 while 6.4 remains accepted_current. | DETECTED as duplicate current/historical version. |
| PF65-M08 | frozen resource | Mutate a previously published 5.16-6.4 profile/resource while adding 6.5. | DETECTED by inherited frozen-resource evidence; independent P0/P1 object comparison found zero differences in 12 frozen resource paths. |
| PF65-M09 | generated | Change generated 6.5 prompts without changing canonical workflow prompt. | DETECTED by canonical/generated equality and snapshot parity. |
| PF65-M10 | lifecycle | Set Review PASS while candidate.semantic_ref is UNFROZEN. | DETECTED. |
| PF65-M11 | prose | Redefine Review independence so an author context can self-review if it uses a different model family. | DETECTED by workflow P65-4 authorship/conclusion independence. |
| PF65-M12 | prose | State that a synthetic fixture matrix proves arbitrary canonical prose semantics. | DETECTED by testing/evidence P65-3 evidence-class boundary. |
| PF65-M13 | prose | Allow a Serious Challenge from a remote possibility or wording discomfort alone. | DETECTED by credible-basis/materiality owner. |
| PF65-M14 | prose | Allow public fallback publication immediately after mechanical qualification, before Review and ratification. | DETECTED by versioning P65-2 lifecycle. |
| PF65-M15 | prose | Make HOT PEM or historical frequency normative D1-D4 authority. | DETECTED by kernel/PEM authority boundary. |
| PF65-M16 | prose | Reverse stored USES_DEFINITION direction to prerequisite -> subject and call it the same relation. | DETECTED by evidence/kernel P64-I semantics. |
| PF65-M17 | cross-layer | Permit D4 to narrow an upstream approximate/set-valued D2 relation into exact/unique behavior without upstream authority. | DETECTED by D3/D4 abstraction-adequacy and formal-contract rules. |
| PF65-M18 | versioning | Allow default/latest branch position to select the governing protocol source. | DETECTED by versioning/portability source-resolution rules. |
| PF65-M19 | routing | Permit inference from a source-resolvable but unloaded specialized prerequisite. | DETECTED by source-vs-context availability rule. |
| PF65-M20 | current representation | In the 6.5 workflow prompt, state key inherited duties as “For Protocol 6.4…” / “Under Protocol 6.4…”. | ACTUAL P1 COUNTEREXAMPLE; survives canonical-to-generated parity and can narrow 6.5 operational obligations. B65-R3. |

PF65-M01/M02/M03 are executable-state counterexamples discovered by source-level oracle inspection. This Review did not create mutated repository branches merely to raise a mutation score. Their discriminating logic is direct: the current validator never resolves evidence_ref, and the current live test explicitly asserts the mutable phase values.

## 3. Meaning-preserving paraphrase controls

| ID | Control | Semantic result |
| --- | --- | --- |
| PF65-C01 | “one current semantic owner” -> “exactly one authoritative current semantic owner for the material claim” | ACCEPT |
| PF65-C02 | “Review PASS -> technically eligible” -> “a successful independent Review establishes technical eligibility, not ratification” | ACCEPT |
| PF65-C03 | reorder the evidence tuple explanation without changing subject/property/method/result/limitations | ACCEPT |
| PF65-C04 | replace “remote ungrounded possibility” with “speculation lacking a governed evidentiary path” | ACCEPT |
| PF65-C05 | explain public fallback/recovery distinction in equivalent prose while preserving order/identity | ACCEPT |
| PF65-C06 | restate PEM temperature as attention/salience only, with identical non-authority meaning | ACCEPT |

No control is rejected by semantic Review. This Review did not claim a separate mechanical mutated-branch run for these paraphrases; the current acceptance doctrine correctly says arbitrary prose wording is not a machine contract.

## 4. Result

Fresh semantic mutation Review is NO-PASS because PF65-M01, M02, M03 and M20 expose three underlying blocker families: unbound Review evidence, duplicated live lifecycle phase state, and predecessor-gated current operational semantics.
