---
kind: stakeholder-decision-record
governing_protocol_version: 6.6.0
target_protocol_version: 7.0.0
decision_date_utc: 2026-10-04
status: stakeholder-directed; refined 2026-10-04 (§§5–6); workplan overlay and contract amendment pending fresh independent check
---

# Deterministic skill activation and activation as a qualification target

## 1. Stakeholder direction

After reviewing the Stage 7 treatment-delivery diagnosis and the selection probes (`STAGE-7-M07-DELEGATE-REQUEST-AND-TREATMENT-DELIVERY-DIAGNOSIS-2026-10-04.md`, `STAGE-7-M07-DOCTRINE-LOADED-PROBE-RESULT-2026-10-04.md`, `STAGE-7-SELECTION-STRONGER-EXECUTOR-PROBE-RESULT-2026-10-04.md`), the stakeholder directed:

> "rewrite the skill descriptions to cover copying, relaying, and delegating. Skill activation should be a qualification target, especially on the lighter models, as they tend to ignore skills sometimes. But more importantly, I think in reality, the protocol should always require the user to use deterministic activation commands such as "/software-design" or "$software-design" to ensure activation. Mere wording is always unreliable."

Read as three decisions:

1. **Description coverage.** The skill descriptions select copying, transcribing and relaying of scientific results or decisions, and delegated scientific work.
2. **Activation is a qualification target.** It is measured per execution profile and must include a lighter (flash-class) executor profile.
3. **Deterministic activation is the supported usage.** Users start governed tasks with the runtime's explicit skill command, not with wording. Wording-based or description-based selection is a fallback, not the activation mechanism.

## 2. Implemented in this change (development of the unqualified 7.0 candidate)

**Description coverage** (`source/roles/software-implementation/SKILL.md`, generated `dist/`):
- The implementation description now also selects "copy, transcribe or relay scientific results, memos or acceptance decisions; delegate any of this work to agents or tools".
- It keeps its scientific/technical scope and every earlier selection class.
- It is the only description changed. This keeps the frozen Stage D rule that only the D4 description is amended (`STAGE-D-ROUTING.md`; tests `test_catalog_frontmatter_is_unchanged_from_basis`, `test_no_accepted_66_entrypoint_text_removed_and_kernel_unchanged`). The test `test_selection_description_covers_new_classes_without_narrowing` now requires the new classes.
- **Why D4 only:** every task class added here (copying or relaying scientific results or decisions, delegating scientific work) already falls under the implementation route's results-review and delegate-request duties.

**User guidance** (`README.md`, `CHANGELOG.md`):
- README tells users to activate with deterministic commands (`/software-design` in Claude Code, `$software-design` in Codex, `/skill:software-design` in OMP).
- README states why wording is unreliable, and its examples now use the command form.
- CHANGELOG's Protocol 7 entry records both changes.

Repository acceptance passed:
- the inherited regression suite;
- release-state and project-memory checks;
- package build and independent validation;
- committed-distribution parity;
- `git diff --check`;
- the orchestrator snapshot check and Core suite.

No qualification claim follows from any of this. Candidate changes after exposure require fresh blind qualification (contract §8).

## 3. Finding that bears on decision 3: OMP headless mode does not execute skill commands

**Probe.** One Flash run, C042, p70, at `/home/samjin/ssdp70-omp-stagef/probes/DETERMINISTIC-ACTIVATION-*`. The pinned template was changed from "Use the {root} skill. {prompt}" to "/skill:{root} {prompt}". The profile was re-frozen through `freeze_profile`, differing only in that template and `profile_id`.

**Result.**
- OMP in headless print mode passed `/skill:software-implementation` to the model as **literal user text**; it did not expand the skill.
- The model then chose to read `SKILL.md` with a tool call.
- Activation succeeded in this run, but by model choice, not by the command. "Deterministic" activation is therefore not mechanically realized by this runtime in the mode the qualification harness uses.
- Whether interactive OMP expands the command was not tested.

**Consequence.** A runtime command counts as deterministic only where the runtime itself loads the skill when the command is given. Where it does not (OMP `-p` here), the harness must inject the selected entrypoint mechanically for a deterministic-entry stratum, and record that injection as the activation mechanism.

## 4. Amendments required (not made here; each needs governed change and fresh independent check per contract §8)

1. **Contract §1 / §4, workplan §8.3 / §11 — entry strata.** Qualification must report activation as separate strata within each execution profile:
   - **(a) deterministic entry:** a runtime command, or mechanical injection where the runtime does not execute commands. This is the supported usage, and activation is expected at 100%.
   - **(b) ordinary entry:** no command; this is the fallback. Its activation rate is a qualification target with its own floor. The floor value is a stakeholder decision still to be made.

   Doctrine measures are scored only on runs where the doctrine was actually delivered. A run with no root selected is a placement miss under stratum (b), not a doctrine failure (§11.3 *Route*).
2. **Profile coverage.** Activation floors must be met on a flash-class profile (the default campaign executor, GLM-5.3-Flash). Results on stronger profiles are reported as separate strata and cannot rescue a light-profile failure.
3. **Harness realization.** Replace the wording template "Use the {root} skill." for stratum (a) with a runtime-verified deterministic mechanism:
   - the runtime's command, where it is executed;
   - otherwise injection of the entrypoint.

   The harness must record which mechanism was used. This changes the profile key and requires a fresh pre-run check (§6).
4. **Doctrine conformity remains separate.** The doctrine-loaded M07 probe showed that a loaded entrypoint still yields only partial delegate-request conformity. Activation closes the delivery gap, not the doctrine-uptake gap.

Protocol 7.0 remains NON-QUALIFIED. Protocol 6.6.0 remains the governing protocol.

## 5. Refinement (2026-10-04, later the same day)

After seeing that Stage 7's ordinary-entry rate was far below the proposed 80% floor, the stakeholder refined decision 2:

> "Is it really important if we have the standard activation route using the commands? Our main focus should be that standard command activation alwasy activates. If that works, we don't necessarily need the plain-word version, and it can simply be regarded as unreliable."

The stakeholder then said: "yes, do steps 1–3 and the runtime runs, commit the review". Steps 1–3 were a governed workplan amendment, a contract revision and fresh independent checks.

**Effective decisions (superseding §1 item 2 where they differ):**

- **(2a)** The qualification target is that "standard command activation alwasy [sic] activates". This is stakeholder-stated. The recorder operationalizes it as *deterministic* activation: the entrypoint reaches the model before its first request, independent of model choice.
- **(2b)** "If that works, we don't necessarily need the plain-word version, and it can simply be regarded as unreliable." This is stakeholder-stated and **conditional** on 2a working; §6 Q2 fixes the condition.

**Recorder's derivations.** These are not the stakeholder's words, and the independent check and stakeholder may correct them:

- **(D1)** "Always activates" holds on every profile offered for qualification, and a flash-class profile is required among them. This applies the earlier "especially on the lighter models".
- **(D2)** Ordinary-entry activation is still measured and reported, since the stakeholder said it "can simply be regarded as unreliable", not that it is unobserved.
- **(D3)** The 6.6 ordinary-selection preservation floors become report-only by the same reasoning.
- **(D4)** Owner false-activation (zero tolerance) and the other entry-independent floors are unchanged.

## 6. Stakeholder answers to the second independent check (2026-10-04)

The second independent check (`ACTIVATION-OVERLAY-AND-CONTRACT-REV2-INDEPENDENT-CHECK-2026-10-04.md`) raised Serious Challenge SC-A and blockers B1–B3 for the stakeholder. The stakeholder chose these options, quoted as presented:

| Question as asked | Option chosen and its stated meaning |
|---|---|
| Q1. "Can the harness loading the skill itself count as 'standard command activation', or must qualification show a runtime's own command loading the skill?" | **"Real command on ≥1 Flash"**: "At least one Flash-class profile must use a runtime whose own command loads the skill (OMP RPC mode does this on Flash). Harness loading is allowed for other profiles and for the byte-cost runs, but can't be the only evidence." |
| Q2. "Is 'plain wording has no pass floor' unconditional, or only where a runtime's command is shown to activate?" | **"Conditional on proof"**: "No ordinary-entry floor, provided the activation question above is satisfied with real runtime-command evidence. If it isn't, plain wording is not exempt." |
| Q3. "Protocol 7 must currently select skills from plain prompts no worse than 6.6 (within 2 of 32 episodes). Keep that as a pass/fail floor?" | **"Report only"**: "Measure and report the 6.6 comparison without pass/fail, consistent with plain wording being unreliable and unsupported." |
| Q4. "Keep the floors that stop skills activating where they shouldn't (non-scientific near-miss tasks), now that descriptions were widened to copy/relay/delegate?" | **"Keep these floors"**: "No floor on activating, but keep the guard against activating wrongly, so wider descriptions can't start firing on non-scientific tasks. Cheap, and it protects users who don't type commands." |

**Effect on §5.**
- Q3 confirms derivation D3, narrowed to the 6.6 *correct-selection* non-inferiority bound. This is the explicit stakeholder supersession that workplan criterion 16 requires for that 6.6 capability.
- Q4 keeps every false-activation floor binding. These are the 6.6 negative-selection bound, the near-boundary negative bound and predicate false-firing.
- D1, D2 and D4 remain recorder derivations. D1 is narrowed by Q1.
