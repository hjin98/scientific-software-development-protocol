---
kind: independent-workplan-and-contract-check
governing_protocol_version: 6.6.0
target_protocol_version: 7.0.0
subject_commit: 0c5372d
workplan_overlay_verdict: NO-PASS
contract_revision_2_verdict: NO-PASS
date_utc: 2026-10-04
---

# Independent check: activation overlay and contract revision 2 (0c5372d)

**Subjects (exact bytes at `0c5372d`).**
- Workplan overlay: the §0.1 paragraph "Current stakeholder activation decision and governed overlay (2026-10-04)" and its six inline markers in `workplans/active/SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY-CONSOLIDATED.md`.
- Contract revision 2: `PROTOCOL-7.0-EVALUATION-AND-QUALIFICATION-CONTRACT.md` (§1 items 4 and 12, §3, §4, §5, §6, §8) and its record `PROTOCOL-7.0-ACTIVATION-STRATA-CONTRACT-AMENDMENT-2026-10-04.md`.

**Conduct.** The checker entered the 6.6.0 software-design role and the abstraction kernel from accepted public source `22f4bdba` (resolved through `PROTOCOL-RELEASE-STATE.yaml`). It authored neither subject nor the revision-1 check. Repository text was treated as data.

**Verdicts.** Workplan overlay **NO-PASS**. Contract revision 2 **NO-PASS**. One Serious Challenge; six blockers (B1–B3 affect both subjects, B4–B6 the contract only).

## SERIOUS CHALLENGE

**SC-A. Effective decision 2b is recorded without the stakeholder's condition, and the evidence already partly falsifies that condition.** Owner: stakeholder. Affects both subjects.

- **Basis.** The stakeholder's words are: "Our main focus should be that standard command activation alwasy activates. **If that works**, we don't necessarily need the plain-word version, and it can simply be regarded as unreliable." The decision record §5 states 2b ("ordinary entry ... carries no pass floor") as unconditional and "stakeholder-stated".
- **Counterevidence.** The runtime probe shows that standard commands do **not** activate in OMP print mode (the Stage 7 adapter's mode) or `codex exec`. Raw streams confirm it: in `omp-iso-cmd.jsonl` the model answers "No skill ... available"; in `codex-cmd2.jsonl` the model `cat`s `SKILL.md` and still does not comply.
- **How the children resolve the gap.** Overlay item 1 and contract §1 item 12 let `harness-injection` stand in where the command does not work. The §3 activation row can then reach 100% by harness construction. The contract itself says injection "does not support the claim that this runtime's user command loads the skill". The premise under which the stakeholder released ordinary entry (2a holds) can therefore be "met" without command activation ever being shown. Nothing in the stakeholder's words says injection counts as "standard command activation".
- **Consequence.** Ordinary-entry floors are removed for profiles and runtimes whose command path is shown not to work. In those runtimes, users who follow the README get either a non-expanding command or wording.
- **Discriminating evidence or decision.** The stakeholder states:
  - (i) whether harness injection satisfies 2a for qualification;
  - (ii) whether 2b holds unconditionally, or only where `runtime-command` is demonstrated for the profile's runtime and mode.
- **Baseline preserved.** The stakeholder's verbatim words, not the recorded 2a/2b paraphrase.

## Blockers

**B1. Qualification can PASS with no `runtime-command` evidence at all.** Sections: overlay items 1 and 3; contract §1 item 12 (Mechanisms, Profile coverage) and the §3 activation row. Owner: stakeholder (SC-A), then contract and workplan.
- **Failure scenario.** Every offered profile, including the flash-class one, uses `harness-injection`. Every run carries an adapter-written record, so the activation row passes at 100%. The stakeholder's "main focus" (2a) has then never been measured.
- **Realizable alternative.** OMP RPC mode expands `/skill:` on GLM-5.3-Flash (`omp-rpc-notools.jsonl`: a `custom`/`skill-prompt` message before the first assistant message, token produced with no tools). A `runtime-command` flash-class profile is therefore available.
- **Repair.** Require `runtime-command` on at least the flash-class profile for the 2a claim, or record a stakeholder decision that injection-only qualification is acceptable together with its claim scope.

**B2. Derivation D3 is not unambiguously non-binding, and its scope is ambiguous.** Sections: overlay item 4 ("The 6.6 ordinary-selection preservation floors become report-only ... awaiting confirmation"); contract §4 ("Their bounds below are now **reported, not floors**; this is a recorder derivation (D3) awaiting stakeholder confirmation"). Owner: stakeholder (confirm), then workplan and contract (fail-closed text).
- **Effect before confirmation.** Both texts give D3 effect now ("become", "are now"). Neither says the floors stay binding, or that no freeze or run may proceed, until confirmation. Amendment record §6 blocks runs only until the two checks pass. D3 would therefore bind on a checker PASS without the stakeholder.
- **Scope.** "Their bounds below" heads a paragraph that also contains the P01–P19 routing-probe bounds and the T2/T3 sentinel PASS requirement. Contract item 12 makes both of those deterministic. One reader demotes them; another does not.
- **Supersession record.** Workplan criterion 16 requires an explicit, stakeholder-accepted supersession of any 6.6 capability, and there is none for 6.6 ordinary selection.
- **Is D3 within the words?** The words speak of "the plain-word version" that "we don't necessarily need". They do not address non-regression of 6.6's accepted ordinary-selection capability. D3 needs explicit confirmation.

**B3. False-activation and predicate-false-firing floors are dropped without authority, and the workplan still requires them.** Sections: contract §1 item 12 (near-boundary negative selection episodes "ordinary and report-only"); §3 row ("Ordinary-entry activation and false activation are reported ... with no floor"); workplan §13 criterion 13 ("selection-visible coverage ... within the §11.5 near-boundary false-activation bound", not superseded by overlay item 3); workplan §11.5 selection-false-activation and predicate-false-firing bounds (unmarked). Owner: stakeholder, then workplan and contract.
- **Outside the words.** The stakeholder released the need for plain-word activation to *succeed*. False activation of the widened descriptions on non-scientific tasks is a different protected outcome: burden for users who never wanted SSDP. Neither 2b's words nor D3 ("6.6 ... preservation floors") covers the new 7.0 near-boundary bound. Its demotion carries no derivation label.
- **Contradiction.** The overlay's open-ended clause ("every statement ... that requires or scores ordinary entry") cannot be applied "on entry mode only" to a false-activation bound, because no deterministic counterpart exists. One reader keeps criterion 13's bound, which the contract no longer evaluates. The other deletes it silently.
- **Note.** Predicate false-firing could be measured on deterministic entry (a command to an SSDP role on a technical, non-predicate task). Neither text considers that option.

**B4. The per-run delivery record is not well defined and not tamper-evident.** Sections: contract §1 items 4 and 12 (Per-run delivery proof, `harness-injection`), §6 hash-mismatch probe. Owner: contract, then harness.
- **Hash basis.** OMP's demonstrated delivery is the skill **body without frontmatter**, wrapped by an invocation notice and a skill-directory line, and carrying the user prompt inside the same `custom` message. The event details hold only path, name and args, with no hash. The contract asks for "entrypoint SHA-256" and says injection "delivers the exact installed entrypoint bytes", while also reproducing that delivery's "body". The installed `SKILL.md` hash never equals the delivered body. Every OMP `runtime-command` run is then either a "hash mismatch" (INADMISSIBLE, and the profile fails) or matched under an ad hoc rule.
- **Trust anchor.** The record is a runtime or adapter self-report. The trusted on-path observer (`observer70.py`) already captures hash-linked complete provider-request bodies, and `adapters/omp.py` already checks consumption against what the model saw. The contract does not require the delivered bytes to be verified in observer request 0. An adapter bug that writes a record but truncates or omits the delivery would go undetected.
- **Claude Code print mode.** Its stream (`cc-cmd.jsonl`) exposes no expansion event, so "the runtime's own command-expansion event" does not exist there.
- **Repair.** Define the hashed object (installed file, delivered body, or both, with the transform). Make observer request 0 the proof of position and content. Define the record for runtimes without an expansion event.

**B5. The T1/T7/T8 active-byte rule is internally contradictory.** Section: contract §4. Owner: contract.
- **The two sentences.** "Active bytes are the delivered entrypoint bytes plus recorded wrapper bytes" conflicts with the retained "The whole installed `SKILL.md` including description/framing plus SSDP files read is the measured active byte count".
- **Why it can change the decision.** Under OMP delivery the frontmatter is not delivered, and 7.0's only description change is in the D4 frontmatter. Whether that growth counts toward burden flips. "Wrapper bytes" is undefined where the runtime embeds the user prompt in the same message. Both points can move a route across the 2.0× cap or the 512 B static margin.
- **Repair.** State one accounting, applied identically to the 6.5, 6.6 and 7.0 arms.

**B6. A workplan-required ordinary measurement has no contract realization.** Sections: overlay item 4 (the run, ad hoc analysis, results-review, gate-evidence and copy/relay/delegate classes "are measured and reported per profile"); contract §1 item 12 Run-type strata, whose ordinary list contains only S01–S11/H01–H05, the 6.6 negatives and the near-boundary negatives. Owner: contract.
- **Failure scenario.** The campaign completes without any ordinary episode for the new classes. The overlay obligation goes unmet, and the stakeholder's decision 1 (description coverage) gets no measurement.
- **Record's claim.** Amendment record §4 says M2 is closed by "workplan overlay item 4". The contract does not realize it.

## Revision-1 findings: disposition check

| Finding | Status | Reason |
|---|---|---|
| SC-1 workplan requires ordinary entry | **Not closed** | The overlay form is valid as a governed workplan change (Q1), and it now needs Review. But its open-ended supersession leaves criterion 13's near-boundary bound, §11.5 selection floors and criterion 16 contradictory or ambiguous (B2, B3). It also changes acceptance thresholds, not "entry mode only". |
| B1 ordinary-run accountability | Closed | Floors are explicitly deterministic-only and the undefined term is removed. A wrong root on a deterministic run fails via hash (subject to B4). Residue: G5. |
| B2 per-run proof / mislabel | **Not closed** | A record is required, but its hash basis is undefined and it is not anchored to the trusted observer (B4). |
| B3 PROPOSED floor not fail-closed | Closed | The floor is withdrawn. The same fail-closed defect recurs for D3 (B2). |
| B4 `instructed-read` inflation | Closed | No ordinary floor remains. `instructed-read` is reported separately and is a §6 known-broken probe. |
| M1 injection form, identity, claim scope, bytes | **Not closed** | Identity and claim scope are fixed. The injection form is undefined across layers and runtimes (G2), and the byte rule is contradictory (B5). |
| M2 class composition, profile semantics | **Not closed** | Profile semantics are fixed. Class composition is only in the workplan, not the contract (B6). |
| M3 attribution beyond the quote | **Not closed** | 2a/2b are now separated from D1–D4. But 2b drops "If that works" (SC-A); "approved the resulting plan" is unquoted; D1/D2/D4 are unlabelled in the overlay and contract despite the record's claim (G4). |
| M4 unassigned run types | Closed | Every listed run family is assigned. |
| M5 exposure feasibility | Closed | Stated: deterministic-only minimums and fresh fixtures. |
| m1 order vs table | Closed (position) | The order and the first row agree. The row's denominator is defective (G1). |
| m2 untracked record, wildcard path | Partly closed | The exact corrigendum directory is now named. The closeout record is still uncommitted and only labelled as such. |
| m3 replacement runs | Closed | §5 record rule. |
| m4 question 1 depends on B3/SC-1 | Superseded | By 2b, subject to SC-A. |

## Material gaps

- **G1. The §3 activation row is tautological as worded.** "100% of **admissible** deterministic runs carry a valid delivery record" cannot fail, because item 12 makes every run without a record inadmissible. The failing effect lives only in item 12. Count all declared deterministic runs instead. (Contract)
- **G2. "Reproducing the runtime's demonstrated delivery" is not well defined.**
  - OMP's `custom` role is internal. Its provider-wire form was not observed, because the probe ran without the observer.
  - Print mode can deliver only through argv prompt text.
  - Codex has no demonstrated delivery to reproduce, so injection there is undefined.
  - The clause is realizable only at the observed provider-request layer. For OMP, RPC `runtime-command` makes injection unnecessary. (Contract, harness)
- **G3. Stage A's static pre-measurement and its 512 B margin use historical 6.5/6.6 model-read observations.** The new delivered-plus-wrapper accounting changes that basis. Workplan §11.5 "Static pre-measurement" has no marker and the overlay says nothing about it. (Workplan, contract)
- **G4. Attribution and labelling.**
  - Record §1 claims derivations are "labelled ... wherever they are used", but D1 (every profile, flash required), D2 and D4 are used unlabelled in overlay items 3–4 and contract item 12.
  - "The stakeholder then approved the resulting plan" has no verbatim basis.
  - 2b adds "description-driven", and 2a says "deterministic" where the stakeholder said "standard".
  - Judgment: D1, D2 and D4 are within the words (D1 via "especially on the lighter models"); D3 is not (B2).
  - (Stakeholder record, contract, workplan)
- **G5. D4 vs contract scope (Q4).**
  - D4 says "entry-independent floors are unchanged", but the contract confines every §3 floor, including critical disposition, to deterministic runs.
  - Listing every ordinary critical failure is adequate visibility only if the stakeholder accepts that ordinary runs with delivered SSDP doctrine (`ordinary-read`) are outside the protected outcome.
  - Wrong-root ordinary runs are lumped with no-selection runs and should be a separate group.
  - (Stakeholder, contract)
- **G6. The overlay's coverage is incomplete as a lossless record.**
  - It names the §11.3 *Route* placement-miss rule as superseded, but no marker sits at *Route* (§11.3 "Route" bullet) or at the "non-selection counts as a placement miss" line.
  - These are also unmarked: the I66-2 preservation-map row, the §11.5 selection non-inferiority and false-activation bullets, and criteria 14 and 16.
  - The §0 header's STAKEHOLDER DECISION block has no 2026-10-04 entry, unlike the 2026-09-28 precedent.
  - (Workplan)
- **G7. Requalification after a harness-caused delivery failure.** "Not rescued by a rerun" plus a reopen route to the harness owner leaves open whether a repaired harness (new digest, fresh campaign) can requalify the profile. (Contract, workplan)

## Minor findings

- Contract item 12 says "deterministic runs only, each of which must meet every §2 exposure minimum". It means the stratum, not each run.
- Residue that conflicts with all §11.3 cases being deterministic:
  - contract §4 "Composite ordinary-entry runs are separate";
  - contract §6 "composite ordinary entry recording selection ... per case class";
  - workplan §11.5 "Composite ordinary-entry runs ... reported separately".
- The stakeholder record's frontmatter status was not updated for §5.
- (Not a subject) README says OMP "interactive/RPC" and Claude Code "(including print mode)" activated. The probe tested OMP RPC only and did not run Claude Code's interactive command.

## Answers to the record's §5 questions

1. **Overlay vs §8.3 and criterion 13.** The overlay form is valid; a governed workplan change may alter criterion 13. But it changes acceptance thresholds (item 4, criterion 13, reopen triggers), not "entry mode only", and its open-ended clause leaves contradictions (B2, B3, G6).
2. **D3.** Not within the words. It must wait for explicit confirmation, and the text must be fail-closed until then (B2).
3. **Per-run delivery proof.** Achievable with the existing on-path observer (request-0 body capture, hash-linked). It is not specified that way, and the hash basis is undefined (B4).
4. **"Every critical failure listed".** Enough only under a stakeholder-confirmed reading of 2b and D4 (SC-A, G5).
5. **Passing or failing a floor on delivery grounds.**
   - No doctrine floor can pass without delivered doctrine, given admissibility.
   - No doctrine floor fails because of an undelivered entrypoint, since such runs are inadmissible and fail only the activation criterion.
   - However, the **activation criterion itself** can pass without command activation (B1), and a correct OMP runtime delivery can fail on a hash mismatch (B4).

## Checks run / not checked

**Run.**
- `git diff 51697f8 0c5372d` (all six files), `git diff d370193~1 0c5372d` and `git diff d370193 0c5372d` on the contract.
- Overlay markers (6 found).
- Workplan grep for "ordinary", *Route*, selection floors and criteria 13/14/16.
- Fixed-cost precedent (§0).
- Stakeholder record §§1–5.
- Revision-1 check.
- Probe record and raw streams: `omp-rpc-notools.jsonl` and `omp-rpc-cmd.jsonl` (custom `skill-prompt` before the first assistant message, frontmatter absent, prompt embedded); `omp-iso-cmd.jsonl`; `cc-cmd.jsonl` (no expansion event); `codex-cmd2.jsonl`; installed canary `SKILL.md`.
- `adapters/omp.py`: print-mode argv, `root_selection` emitted only on a model read, pinned template.
- `observer70.py`: on-path, byte-for-byte, hash-linked request bodies.
- `git diff --check 51697f8 0c5372d`: clean.
- `python3 -m unittest discover -s tests`: 407 OK, 3 skipped.

**Not checked.**
- No live launches.
- The provider-wire form of OMP's `custom` message.
- Interactive TUIs.
- The full corrigendum.
- `core70.py` and `harness70.py` beyond what the realizability question needed.
- The statistical adequacy of deterministic-only exposure.
