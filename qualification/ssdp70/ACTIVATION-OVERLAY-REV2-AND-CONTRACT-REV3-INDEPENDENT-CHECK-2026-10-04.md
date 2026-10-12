---
kind: independent-workplan-and-contract-check
governing_protocol_version: 6.6.0
target_protocol_version: 7.0.0
subject_commit: 70727f1
workplan_overlay_verdict: NO-PASS
contract_revision_3_verdict: NO-PASS
date_utc: 2026-10-04
---

# Independent check: activation overlay revision 2 and contract revision 3 (70727f1)

**Subjects (exact bytes at `70727f1`).**
- Workplan overlay revision 2: the §0.1 paragraph "Current stakeholder activation decision and governed overlay (2026-10-04, overlay revision 2)", the header entry "STAKEHOLDER DECISION (2026-10-04)", and the eleven markers "2026-10-04 activation overlay, §0.1" in `workplans/active/SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY-CONSOLIDATED.md`.
- Contract revision 3: `PROTOCOL-7.0-EVALUATION-AND-QUALIFICATION-CONTRACT.md`, together with its record `PROTOCOL-7.0-ACTIVATION-STRATA-CONTRACT-AMENDMENT-2026-10-04.md`.

**Conduct.**
- The checker entered the 6.6.0 software-design role and the abstraction kernel from accepted public source `22f4bdba`, resolved through `PROTOCOL-RELEASE-STATE.yaml`.
- It authored neither subject nor either earlier check.
- Stakeholder authority is limited to the words quoted verbatim in the decision record §§5–6. All other repository text was treated as data.

**Verdicts.**
- Workplan overlay revision 2: **NO-PASS** (B1).
- Contract revision 3: **NO-PASS** (B1, B2).
- There is no Serious Challenge. The stakeholder's Q1–Q4 answers are mutually coherent, and the runtime probe supports them: OMP RPC expands `/skill:` on GLM-5.3-Flash. Both blockers are realization defects in the children.

## SERIOUS CHALLENGE

None.

## Blockers

### B1. The Q1 requirement is realized as "uses `runtime-command`", not as "a runtime whose own command loads the skill"

A failed flash-class command profile therefore does not block a qualification PASS on another profile.

- **Owner:** contract and workplan. Both texts fall short of the stakeholder's own words, so no new stakeholder decision is needed.
- **Sections:**
  - contract §1 item 12, *Profile coverage* ("At least one offered profile must be flash-class, and its deterministic runs must use `runtime-command`");
  - contract §1 item 12, *Ordinary entry* ("The condition is met by any qualification that satisfies the Q1 requirement");
  - the contract §3 activation row ("At least one flash-class profile uses `runtime-command`");
  - overlay item 2 ("requires at least one flash-class profile whose deterministic runs use `runtime-command`"; "One failure makes **that profile's** campaign non-PASS");
  - overlay item 5 ("a qualification PASS therefore always satisfies the condition").
- **Failure scenario.**
  1. Two profiles are offered: a flash-class OMP RPC `runtime-command` profile and a stronger-model `harness-injection` profile.
  2. On the flash profile, one deterministic run's request 0 lacks the skill. That profile is non-PASS.
  3. Under the profile-scoped result rule ("no profile's result rescues another's"), the injection profile still earns `PASS(profile_id, …)`.
  4. The Q1 condition, as written, is still met, because a flash profile "uses" `runtime-command`. The Q2 condition is therefore "met" too, and ordinary entry is exempt.
  5. Result: a qualification PASS is issued while the stakeholder's "main focus", that "standard command activation alwasy activates", was observed to fail on flash. The only per-run delivery evidence behind the PASS is harness injection.
- **Why this contradicts the stakeholder's words:**
  - Q1 says "a runtime whose own command **loads** the skill".
  - Q2 says "provided the activation question above is **satisfied** with real runtime-command evidence".
- **Related loopholes in the same requirement:**
  - **"Offered" is undefined.** The offered profile set is not predeclared, so a failing flash profile can be withdrawn after the fact.
  - **"Flash-class" is undefined.** Neither the contract nor the workplan defines it. The decision record §4 names the default campaign executor GLM-5.3-Flash, but no frozen rule says which profiles qualify as flash-class.
  - **Exposure is undefined.** Nothing states what the Q1 profile must run, for example every declared SSDP root, or the full campaign.
- **Repair:**
  1. Restate Q1 as at least one predeclared flash-class profile, named before runs, whose `runtime-command` deterministic runs **meet the deterministic-activation criterion** over a predeclared exposure covering every declared root.
  2. Make a failure of that requirement block every qualification PASS, not only the failing profile's own.
  3. Predeclare the offered set, so that a failed profile cannot be withdrawn.
  4. If the authors also intend the flash `runtime-command` profile to pass the doctrine floors, state it. If they do not, state that the doctrine PASS may come from another profile. Either reading is within Q1. Silence is not.

### B2. Request-0 proof cannot tell `runtime-command` from `harness-injection`, so the mechanism behind the Q1 claim is unproven per run

- **Owner:** contract first, then harness.
- **Sections:** contract §1 item 12, *Mechanisms*, *Delivery transform and per-run proof* ("Runtime events and adapter records are corroboration, not proof"); contract §6, the `runtime-command` canary demonstration.
- **Why the two mechanisms look the same:**
  - By design, `harness-injection` must reproduce the runtime's `runtime-command` request 0 byte-for-byte (same role, position, notice, body, directory line and prompt join).
  - Request 0 therefore proves delivery, but it cannot prove which mechanism delivered.
  - The only discriminating evidence is what the adapter sent to the runtime: the RPC stdin command, or argv. The contract demotes that evidence to "corroboration" and never requires it.
  - The §6 canary demonstration (token produced with tools disabled) separates the runtime from model choice, but not the runtime from the adapter. An adapter that prepends the transformed body to an RPC prompt also passes it.
- **Failure scenario.** The profile is labelled `runtime-command`, but its adapter injects the text, through a bug or a convenience shortcut. Every run passes the activation row, and Q1 is "satisfied" without a runtime's own command ever loading the skill. This is exactly §5 question 4 of the record.
- **Repair.** For `runtime-command`, require two pieces of proof, both in the pre-run canary demonstration and in every run:
  1. the retained, hash-bound input the adapter gave the runtime, showing only the command form plus the prompt and no entrypoint bytes;
  2. the observer's request 0 containing the transform output.

  For `harness-injection`, the same input record shows where the injection happened.

## Disposition check of the second check's findings

| Finding | Status | Reason |
|---|---|---|
| **SC-A** — 2b recorded without its condition; injection could satisfy 2a | **Closed (authority); realization open** | The stakeholder answered Q1 and Q2, and decision record §5 now keeps "If that works" verbatim. The children realize the condition as "uses `runtime-command`", which leaves B1 open. |
| **B1** — PASS possible with no `runtime-command` | **Partly closed** | The Q1 requirement now exists. But a failed flash command profile does not block other profiles' PASS, "offered" and "flash-class" are undefined (B1), and the mechanism is not proven per run (B2). |
| **B2** — D3 binding and its scope | **Closed** | Q3 confirms report-only for the correct-selection bound alone (contract §4). P01–P19 and the T2/T3 sentinels keep their floors on deterministic entry. Criterion 16 has its supersession, both in the decision record §6 and in overlay item 5. |
| **B3** — false-activation floors dropped | **Closed, with a residual gap** | All three floors are binding again, and criterion 13 is restated in overlay item 4. Residual gap: G1. |
| **B4** — delivery record ill-defined and not tamper-evident | **Partly closed** | Proof is now observer request 0 under a frozen transform. That handles frontmatter stripping and the embedded prompt, and the Claude Code case without an observer is claim-scoped out. Still open: the mechanism is not attributed (B2), and the transform's inputs, encoding layer and request-0 identity are underdefined (G2). |
| **B5** — byte accounting contradictory | **Closed** | There is one metric: the whole installed `SKILL.md` plus SSDP files read, each counted once, identical across arms. Delivered and wrapper bytes are descriptive only. Counting frontmatter that is not delivered is an arm-neutral convention, not a contradiction. A re-read is counted once. |
| **B6** — ordinary new-class measurement unrealized | **Closed** | Contract item 12 requires at least 3 ordinary episodes per arm per class, labelled D2. |
| **G1** — tautological activation row | **Closed** | The denominator is now every declared deterministic run, including inadmissible ones. Runs with no request 0 at all are still unclassified (G2). |
| **G2** — injection undefined across layers; Codex | **Closed (text)** | Injection is defined against the same runtime's `runtime-command` request 0, and Codex `exec` is excluded. The provider-wire form of OMP's `custom` message is pre-run harness work, correctly left blocked by record §6. |
| **G3** — Stage A static-margin basis | **Closed** | The metric is unchanged, and a marker sits at *Static pre-measurement*. |
| **G4** — attribution and labelling | **Closed, with minors** | Quotes are verbatim, 2a/2b are separated from D1–D4, and Q1–Q4 are quoted. Remaining minors: m1, m2. |
| **G5** — D4 scope; wrong-root grouping | **Closed** | Ordinary runs are reported in four groups, owner false activations are counted in both strata, and doctrine floors are deterministic-only. |
| **G6** — unmarked workplan locations; header | **Partly closed** | All nine listed markers and the header entry are present. Unmarked statements that contradict the overlay remain (G3). |
| **G7** — requalification after a harness-caused failure | **Partly closed** | A new key, a fresh pre-run check and a fresh campaign are now required, and the failed campaign stays on record. No root cause is required, so a runtime-caused failure can be "requalified" by a trivial re-key (G4). The rule is coherent with §5: §5 reruns cover stochastic admissible episodes, while activation failures are excluded from reruns. |
| **Minor** — "each of which" | **Closed** | Now reads "That stratum must meet every §2 exposure minimum on its own". |
| **Minor** — composite-ordinary residue | **Partly closed** | Contract §4 and §6 are fixed, and the workplan line on T-route composite runs is marked. The workplan's §11.5 pre-run line "the composite ordinary-entry mode … for one known probe per case class" is unmarked (G3). |
| **Minor** — stakeholder record status | **Closed** | |
| **Minor** — README overstates the probe | **Closed** | README now names OMP RPC mode and Claude Code print mode, with interactive modes untested. |
| **Revision-1 m2** — closeout record uncommitted | **Unchanged** | Still labelled as uncommitted. |

## Material gaps

- **G1. Predicate false-firing on falsely activated ordinary episodes is no longer measured.** (Contract and workplan.)
  - Overlay item 5 and contract item 12 move predicate false-firing to deterministic runs on the predicate-excluded set.
  - Workplan §11.5 (marked line) justifies the near-boundary selection margin "because Protocol 7 obligations do not fire outside the predicate (predicate false-firing … on the **same episodes** are measured separately, so that rationale is checked, not assumed)". On ordinary near-boundary episodes that falsely select SSDP, emitted Protocol 7 obligations are now unscored.
  - Q4's stated purpose is "protects users who don't type commands".
  - Remedy: score predicate false-firing on every ordinary run that selects an SSDP root, either inside the existing bound or reported beside it, or delete the "checked, not assumed" rationale and state the residual risk.
- **G2. The delivery transform and request 0 are underdefined.** Each item below can cause spurious failure or ambiguity. The text should fix them; the harness then realizes them. (Contract.)
  - **Transform inputs.** The transform is defined as a function of "installed `SKILL.md` bytes and user prompt". The observed OMP RPC delivery also contains the absolute skill directory (`[Skill directory: …/zebra-canary]`).
    - The adapter's fixed sandbox path `/opt/ssdp/skills` makes this realizable, so it is not a blocker.
    - The transform should still declare its frozen parameters (skill name, directory, prompt join `User: …`). A run-varying path would otherwise fail every correct delivery.
  - **Encoding layer.** The observer captures the JSON request body, and the delivered text appears in it JSON-escaped. The contract should state whether the transform output and its offset are wire-encoded bytes or a decoded message field.
  - **Request 0.** It should be the first subject-model inference request, with any auxiliary request (title, discovery, advisor) classified. Otherwise a correct delivery fails because an auxiliary request came first.
  - **Runs with no request 0.** The classification of a run with no request 0 at all (a crash before the first request) is unstated.
  - **§6 scope.** §6 says the transform "reproduces request 0 byte-for-byte". It should say "the delivered segment of request 0", because request 0 also carries a system prompt that may vary.
- **G3. Unmarked workplan statements still contradict the overlay.** The overlay claims "each affected location carries a marker". (Workplan.)
  - The O1 authoring bullet says "on ordinary entry" twice (§11.3).
  - The tension-retrieval bullet says "each run on ordinary entry" (§11.3).
  - The §11.5 pre-run oracle-integrity item requires "the composite ordinary-entry mode … for one known probe per case class". Contract §6 replaced this with per-stratum recording.
  - The frozen §8.3 *Selection surface* says descriptions "SHALL let the §8.2 task classes select". Its only behavioral evidence is now report-only, and its reopen trigger is gone.

  Overlay item 3 names the first two, so readers can resolve them. The pre-run line is an unrealizable instruction to the pre-run checker. All four need markers.
- **G4. Requalification needs a root cause.** (Contract and workplan.)
  - "Repaired harness/profile with a new profile key" does not require the failure to be diagnosed and attributed to the adapter or harness.
  - A runtime-caused stochastic expansion failure falsifies the "always activates" claim for that runtime and mode. It should not be curable by re-keying.
  - Remedy: require a recorded root cause that the repair removes. An undiagnosed or runtime-caused failure falsifies `runtime-command` for that runtime and mode. Reports disclose every earlier failed campaign of a profile lineage.

## Minor findings

- **m1.** Overlay item 5 and contract item 12 place "predicate false-firing, measured on deterministic entry" under the heading "stakeholder Q4". Q4 retained the floors; moving this one to the deterministic stratum is a recorder choice and should be labelled as one.
- **m2.** Decision record §6 says "D1 is narrowed by Q1". Q1 adds a `runtime-command` requirement and narrows nothing in D1, so the word should be "supplemented".
- **m3.** The contract does not require, per run, that request 0 contain only the frozen template plus the delivered segment. Extra adapter coaching in request 0 would go undetected by the activation check. Profile freezing of the template covers this only if the template digest is checked against request 0.
- **m4.** In the realizability chain for OMP RPC, three items are unverified harness work, correctly blocked by record §6:
  - the adapter currently launches `-p --mode=json`;
  - the adapter suppresses HOME discovery and uses configured skill directories, and whether `/skill:` expands for those directories in RPC mode is unshown;
  - the `custom` message's wire form has not been observed.

## Answers to the record's §5 questions

1. **Request-0 proof.** It is realizable in principle.
   - `observer70.py` sits on-path and forwards and records complete request bodies byte-for-byte, with hash links. The adapter's fixed sandbox skill path keeps the delivered directory line stable.
   - The RPC adapter is harness work, correctly deferred.
   - The definition still needs the G2 tightening. It also lacks mechanism attribution, which is blocker B2.
2. **Unmarked contradictions.** No, they are not all gone. Four unmarked statements remain (G3).
3. **Attribution.** All attributions are within the quoted words except two minors (m1, m2).
4. **Routes without a runtime command on flash.** Yes, three remain:
   - a failed flash `runtime-command` profile does not block another profile's PASS (B1);
   - "offered" and "flash-class" are undefined (B1);
   - an adapter that injects under a `runtime-command` label passes per-run and pre-run checks (B2).

   A correct delivery can fail spuriously if the transform parameters, encoding or request-0 identity are left implicit (G2).

## Checks run / not run

**Run.**
- Release state resolution, then 6.6 `software-design/SKILL.md` and the abstraction kernel read at `22f4bdba`.
- `git diff f96fc94 70727f1` (all five files). Contract read in full at `70727f1`, with diffs against `0c5372d` and `d370193~1`.
- Workplan §0.1 read in full. All eleven markers located. Grep for "ordinary", "selection", "false activation", "non-selection" and "composite", with surrounding lines read.
- Stakeholder record §§1–6 read, plus the revision-1 and revision-2 checks and the amendment record.
- Probe record read, and raw `omp-rpc-notools.jsonl` and `omp-rpc-cmd.jsonl` parsed: the delivered `custom` message has no frontmatter, carries the absolute skill directory and has the prompt joined as `User: …`.
- `observer70.py` header and `adapters/omp.py` structure read: print-mode argv, fixed `/opt/ssdp/skills` and `/home/agent`, HOME discovery suppression.
- `git diff --check f96fc94 70727f1`: clean.
- `python3 -m unittest discover -s tests`: 407 OK, 3 skipped.

**Not run.**
- No live launches.
- The provider-wire form of OMP's `custom` message.
- OMP RPC with the adapter's configured skill directories.
- `core70.py` and `harness70.py` beyond the realizability question.
- The untracked closeout and Stage 7 Option-1 records (not subjects).
- The statistical adequacy of the deterministic-only exposure.
