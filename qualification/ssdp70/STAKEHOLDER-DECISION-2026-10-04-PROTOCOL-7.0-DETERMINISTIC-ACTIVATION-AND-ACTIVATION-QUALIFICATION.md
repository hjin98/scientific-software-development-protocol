---
kind: stakeholder-decision-record
governing_protocol_version: 6.6.0
target_protocol_version: 7.0.0
decision_date_utc: 2026-10-04
status: stakeholder-directed; contract/workplan amendments pending governed change and fresh independent check
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

The stakeholder then approved the resulting plan: a governed workplan amendment, a contract revision, fresh independent checks, and runtime command-activation runs.

**Effective decisions (superseding §1 item 2 where they differ):**

- **(2a)** The qualification target is that deterministic command activation always activates. This is stakeholder-stated.
- **(2b)** Ordinary-entry (plain-word or description-driven) activation is regarded as unreliable and carries no pass floor. This is stakeholder-stated.

**Recorder's derivations.** These are not the stakeholder's words, and the independent check and stakeholder may correct them:

- **(D1)** "Always activates" holds on every profile offered for qualification, and a flash-class profile is required among them. This applies the earlier "especially on the lighter models".
- **(D2)** Ordinary-entry activation is still measured and reported, since the stakeholder said it "can simply be regarded as unreliable", not that it is unobserved.
- **(D3)** The 6.6 ordinary-selection preservation floors become report-only by the same reasoning.
- **(D4)** Owner false-activation (zero tolerance) and the other entry-independent floors are unchanged.
