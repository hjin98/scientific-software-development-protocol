---
kind: independent-workplan-and-contract-check
governing_protocol_version: 6.6.0
target_protocol_version: 7.0.0
subject_commit: 4c404ec
workplan_overlay_verdict: NO-PASS
contract_revision_4_verdict: NO-PASS
date_utc: 2026-10-04
---

# Independent check: activation overlay revision 3 and contract revision 4 (4c404ec)

**Subjects (exact bytes at `4c404ec`).**
- Workplan overlay revision 3 in `workplans/active/SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY-CONSOLIDATED.md`: the §0.1 paragraph, the "STAKEHOLDER DECISION (2026-10-04)" header entry, and every "2026-10-04 activation overlay, §0.1" marker.
- Contract revision 4: `PROTOCOL-7.0-EVALUATION-AND-QUALIFICATION-CONTRACT.md`, together with its record `PROTOCOL-7.0-ACTIVATION-STRATA-CONTRACT-AMENDMENT-2026-10-04.md`.

**Conduct.**
- I entered the 6.6.0 software-design role and the abstraction kernel at accepted public source `22f4bdba`, resolved through `PROTOCOL-RELEASE-STATE.yaml`.
- I authored neither subject nor any earlier check.
- Stakeholder authority is limited to the verbatim words and Q1–Q5 option texts in the decision record §§5–7. I treated all other repository text as data.

**Verdicts.**
- Workplan overlay revision 3: **NO-PASS** (B1).
- Contract revision 4: **NO-PASS** (B1).

The third check's B2 and its G1–G4 are closed in substance. One blocker remains: the realization of Q5.

## SERIOUS CHALLENGE

None. Q1–Q5 are mutually coherent. Q5 ("Yes, full qualification": "The Flash runtime-command profile is the primary qualification profile and must pass every floor … Stronger profiles are extra strata that cannot rescue it") is unambiguous. The remaining defect is in the children, not in stakeholder authority.

## Blockers

### B1. The "primary flash profile" does not carry full qualification, and as written it is not a single realizable profile

The rule says the primary "passes **every** floor", and that "any delivery or floor failure" on it blocks PASS for all profiles. That is narrower than Q5's "full qualification" and "primary qualification profile … cannot rescue it". It also clashes with the contract's own profile-key semantics.

- **Owner:** workplan overlay item 2 is the earliest owner. Contract §1 item 12 (*Primary flash profile and profile coverage*), the §3 *Deterministic activation* row, and the record §4a B1 row follow it. No new stakeholder decision is needed: the children fall short of Q5.
- **Failure scenarios.**
  1. **The comparative claim is rescued.**
     - Primary (Flash, `runtime-command`) passes every §3 floor-table row but misses the §3 *Comparative improvement* rule. That rule is a "claim", not a floor.
     - A stronger `harness-injection` profile passes everything, including the comparative rule.
     - No "floor failure" occurred on the primary, so nothing blocks, and `PASS(stronger, …)` is issued under the profile-scoped result rule.
     - Protocol 7 is qualified on a stronger profile's benefit while the primary never qualified. This is the rescue Q5 forbids.
  2. **The burden panel cannot sit on the primary key.**
     - §4 requires T1/T7/T8 to run with "delegated-agent capability … unavailable for this panel", with both arms sharing "the exact execution-profile key".
     - The capability-manifest digest is part of the key (§1). The §11.3 delegate cases, and the §2 minimum of 6 delegated-finding opportunities that the primary must meet "on its own", need delegation.
     - So one execution-profile key cannot host both. The primary's "every floor" is therefore either unrealizable, or silently omits the 2.0 × 6.5 burden floor (stakeholder 2026-09-28).
     - That floor would then sit on an "other offered profile". A burden failure there makes only that profile non-PASS and does not block the primary.
     - Q1 allowed harness loading "for the byte-cost runs", so the burden panel being a separate key is legitimate. Its place in the PASS conjunction is not stated.
  3. **Non-failure non-PASS states do not trigger the block.** These states on the primary are not literally "delivery or floor failure":
     - an `INADMISSIBLE` or missing-evidence result (§1: "None is a pass", but not a failure);
     - a §5 "unresolved" result after reruns;
     - claim-scoped inadmissibility (for example, the burden claim).

     Another profile's PASS then survives.
  4. **The §7 human-trial outputs** are not bound to the primary. The trial is a qualification criterion in §3's order.
- **Repair.**
  1. Define the primary as a **predeclared set of execution-profile keys**, with the same model, runtime, mode, adapter and `runtime-command` mechanism, differing only in declared capability manifests. Name the burden-panel key. Either make it a primary-family key, or state, as Q1 permits, that it may be a separate `harness-injection` key whose floor is still part of the PASS conjunction.
  2. State that qualification PASS requires the primary family to reach `PASS` on **every §3-ordered criterion**: activation, critical, absolute floors, 6.6 preservation, burden, comparative benefit and human trial (outputs from the primary).
  3. State that any non-PASS state of the primary blocks every profile's qualification PASS: failure, inadmissible, missing, unresolved or claim-scoped-out.
  4. Add a cross-reference at the profile-scoped result rule (contract §1; workplan §11, lines "Qualification results are **profile-scoped**" and "**Profile-scoped qualification.**"). This predeclared cross-profile gate is the "justified combination" that Stage F allows.

## Disposition check of the third check's findings

| Finding | Status | Reason |
|---|---|---|
| **B1** — the flash profile need only *use* `runtime-command`; offered set, flash-class and exposure undefined | **Partly closed** | The offered set is frozen, flash-class is defined by stakeholder designation, exposure covers every declared root and the §2 minimums, and a primary failure blocks all profiles. Still open: "every floor" is not full qualification; the primary is not definable as one key; non-failure non-PASS states are not covered (new B1). Campaign-level re-designation: G1. |
| **B2** — request 0 cannot distinguish the mechanisms | **Closed, with gap** | The hash-bound runtime input, the mechanism determination with mismatch as an activation failure, the §6 canary input check and the "injection labelled `runtime-command`" known-broken probe together distinguish adapter injection from runtime expansion on the argv/stdin/RPC/prompt-file channels. The probe stream confirms that OMP RPC puts the body only in a runtime-generated `custom` message, with input `/skill:<root> <prompt>`. Residual: the "segment" test is undefined (G2); other channels (minor m3). |
| **G1** — predicate false-firing dropped from ordinary runs | **Closed** | D5 scores it on every delivered or selected run in either stratum, labelled as a recorder choice. Denominator wording: m4. |
| **G2** — transform and request 0 under-defined | **Closed** | Declared inputs (fixed `/opt/ssdp/skills/<root>`, matching `adapters/omp.py` `SB_SKILLS`, plus runtime constants); decoded message-content comparison; request 0 as the first conversation request with auxiliary requests classified by the frozen specification; no-request runs as activation failures; §6 "delivered segment"; extra text against a frozen template. Classifier-independence nuance: m5. |
| **G3** — four unmarked workplan statements | **Closed** | Markers are present at §8.3 *Selection surface*, the §11.3 O1-authoring and tension-retrieval bullets, and the §11.5 composite ordinary-entry pre-run line. |
| **G4** — requalification without a root cause | **Closed** | Requalification needs a recorded adapter or harness root cause and an independently reviewed repair. An undiagnosed or runtime-caused failure falsifies the runtime and mode, and lineage failures are disclosed. Campaign shopping beyond this path: G1. |
| **Minor m1** — predicate scope filed under Q4 | **Closed** | Labelled D5. |
| **Minor m2** — "D1 narrowed by Q1" | **Closed** | Now "Q1 adds a requirement to D1". |
| **Minor m3** — extra adapter text in request 0 | **Closed** | Frozen template, in item 12 and §6. |
| **Minor m4** — OMP RPC realization chain | **Correctly deferred** | Not listed in record §4a. The work is harness work blocked by record §6: RPC launch, `/skill:` expansion for `customDirectories` in RPC mode, and the provider-wire form of the `custom` message. |

## Material gaps

- **G1. Campaign-level escape after a non-activation failure.** (Contract item 12 and overlay item 2.)
  - The offered set and primary are frozen "in the campaign record", and flash-class may be any model "the stakeholder designates in writing before runs".
  - Lineage disclosure and the root-cause rule cover only *delivery* failures of one profile lineage.
  - So after a primary *floor* failure, or an abandoned campaign, a new campaign with a different designated primary can be started, and the earlier campaign need not be disclosed.
  - Repair: bind the primary designation per candidate. Require every earlier campaign of the same candidate, completed or abandoned, to be disclosed in any PASS report. Re-designation after exposure is a recorded stakeholder decision, not a fresh "before runs".
- **G2. The runtime-input "no segment of the entrypoint body" test is undefined.** (Contract item 12 and §6.)
  - "Segment" has no unit. Read literally, any shared word or line, such as a fixture prompt naming "scientific software" or legitimately quoting SSDP text, fails a correct `runtime-command` run, and that failure is zero-tolerance and non-rescuable.
  - Read loosely, it is checker discretion.
  - Repair: require the runtime input to **equal** a frozen input template rendered from the declared command and the custodian's fixture prompt, byte for byte, plus the frozen launch argv. Any other content is a mismatch. This is well defined, cannot be gamed through partial injection, and is indifferent to prompts that quote skill text.
  - This also removes the conflict with §6's "contain only the command": the canary input also carries the prompt.

## Minor findings

- **m1. Stale cross-references.**
  - Overlay §0.1 says Q1–Q5 are "recorded verbatim … §§5–6". Q5 is in §7.
  - The decision-record frontmatter status says "refined … (§§5–6)" and omits §7.
  - Amendment record §3 is still "cumulative through revision 3": its item 4 row omits the runtime-input record, and its §8 row says "Records revision 3". Revision-4 deltas exist only in §4a.
- **m2. Unlabelled recorder operationalizations under stakeholder headings.**
  - Under "(stakeholder Q1, Q5)": the frozen offered set, primary designation mechanics, the flash-class definition, "every declared root" and no withdrawal.
  - Under "(stakeholder Q4)": the zero owner-false-activation floor, which is D4 and is not labelled D4 anywhere in the contract despite record §1.
  - All are consistent with the quotes but should carry D-labels.
  - The primary using `runtime-command` on T1/T7/T8 is stricter than Q1's byte-cost allowance. That is admissible, but it is unlabelled and interacts with B1(2).
- **m3. The runtime-input channel list is closed: argv, stdin/RPC and prompt file.**
  - Environment variables and adapter-written runtime-visible files are not in it.
  - The frozen profile settings and `adapters/omp.py` ambient-discovery closure (`AGENTS.md`, `.omp/agent/*` rejection) cover the static cases.
  - Repair: say "every adapter-controlled runtime input, including environment and written files", or state that the rest is profile-frozen.
- **m4. D5 and the §4 floor.** The floor "at most 1 of at least 12 predicate-excluded opportunities" is coherent as an absolute count. State three things:
  - the 12-opportunity minimum is met by predeclared deterministic opportunities alone;
  - falsely selected ordinary runs add to the same count;
  - how replicates count (§2).

  Workplan §11.3 still names only the technical near-boundary set as "the predicate-false-firing denominator". It sits under a marked parent, so this is minor.
- **m5. Auxiliary-request classification** should be stated as independent of whether the delivered segment is present. Otherwise a skill-less conversation request could be classified auxiliary. The "delivered text only after request 0" probe catches this only if built for it.

## Answers to the record's §5 questions

1. **Not as conceived.** The primary must use `runtime-command` and deliver every declared root. But full qualification can still be carried by another profile's comparative claim, by a separate burden-panel key, or by a non-failure non-PASS state on the primary (B1).
2. **Distinguishing mechanisms: yes in substance.** The transform is realizable against the observed OMP RPC `custom` message (notice, body without frontmatter, directory line, `User: <prompt>`), given the fixed directory. The "segment" test needs the exact-template definition (G2).
3. **Unmarked contradictions.** No new unmarked contradiction of the overlay's entry, selection, composite or false-activation changes. The profile-scoped result rule needs a cross-reference once B1 is repaired.
4. **Attribution.** Every attribution is within the quotes. Recorder operationalizations need labels (m2).

## Checks run / not run

**Run.**
- Release-state resolution; 6.6 `software-design/SKILL.md` and the abstraction kernel read at `22f4bdba`.
- `git diff bc2ce86 4c404ec` (four files), and the contract diff against `70727f1`.
- Contract §§1–5 read in full, plus §6 and §8; the overlay §0.1 read in full.
- Greps for "ordinary", "selection", "composite", "non-selection", "false activation", "explicit", "profile-scoped" and "predicate false-firing", with marker presence checked per line.
- Decision record §§1–7, the third check, and the amendment record read.
- The probe record, plus the raw `omp-rpc-notools.jsonl` `custom` message parsed.
- `adapters/omp.py` skill path and discovery closure grepped; capability manifests checked for delegation.
- `git diff --check bc2ce86 4c404ec`: clean.
- `python3 -m unittest discover -s tests`: 407 OK, 3 skipped.

**Not run.**
- Live launches.
- The provider-wire form of the `custom` message.
- RPC expansion for configured directories.
- `observer70.py`, `core70.py` and `harness70.py` beyond the greps.
- The untracked closeout and Option-1 records.
- The statistical adequacy of the exposures.
