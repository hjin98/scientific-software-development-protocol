---
kind: protocol-stage-evidence
governing_protocol_version: 6.6.0
target_protocol_version: 7.0.0
stage: A
disposition: STOPPED-BEFORE-STAGE-B
active_serious_challenge: consumed-surface-O1-meaning-vs-frozen-label-table
---

# Stage A stop — D4 static backstop and consumed-surface meaning

## Serious Challenge and stop decision

The Stage A independent check found that the D4 completion draft uses **“Without O1 content”** in element 6. O1 is defined in workplan §4.1, but the frozen §8.3 consumed-surface label table gives no meaning for it. An ordinary D4 agent may consume only its entrypoint; that agent cannot determine when the retention/projection default applies from this draft alone. Frozen §8.3 directs a newly found missing consumed label meaning to a **governed workplan change** adding it to that table. The stakeholder's current task requires the label table to remain byte-identical. Both constraints cannot be satisfied by D4 wording at the point the independent check has found the gap. This is a Serious Challenge to the workplan's consumed-surface sufficiency under the current freeze; it is not repaired by loading the owner or weakening element 6. The original §8.3 text remains the baseline pending owner/stakeholder adjudication and a fresh independent Review of any substantive workplan change.

The independently checked draft also crosses the Stage A static fixed-cost stop. `STAGE-A-STATIC-PREMEASUREMENT.md` declared a 512 B margin before the draft was measured. The corrected exact draft in `STAGE-A-D4-ENTRYPOINT-DRAFT.md`, assembled by `measure_stage_a_d4.py` from the immutable accepted-6.6 public source, has SHA-256 `f8622a688efb5018998ee818c39c723833888067c07e29faf88dad40767b9422` and is **14,861 B**: 7,057 B baseline + 7,679 B gross additions + 125 B description delta. The historical 6.5 T1/T8 entrypoint is 8,360 B, giving the **9,196 B planning cap** at 1.10 × and an **8,684 B** limit after the predeclared margin. This draft exceeds the planning cap by **5,665 B** and misses the static margin by **6,177 B**. These are static planning observations, not the unrun fresh-paired live medians. The draft has not passed lossless attribution because of the O1 gap; the measurement demonstrates the size of these exact bytes, not an unavoidable minimum.

**Stage B is not started.** Under §8.3, a static cap breach or insufficient predeclared margin is returned to the stakeholder before Stage B. The stakeholder's options under the existing workplan are to compress while preserving every required element, change placement through a governed workplan change and fresh independent Review, or relax the backstop. The O1 meaning conflict separately needs owner/stakeholder adjudication; no D4-only workaround is claimed. This record requests neither automatic relaxation nor permission to edit a frozen section.

## Evidence and incomplete obligations

- The stakeholder accepted the b2d1f4e Review Minors 1–3 wording and authorized D4 Stages A–F. The resulting workplan bytes have SHA-256 `ad0a4414c6492ee865784dc9e669d1e21d9194ebb0dfe2cdb639106ff236eea4`; a separate read-only Review returned PASS in `WORKPLAN-REVIEW-PROTOCOL-7.0-AD0A441-PASS.md`, confirming all protected sections byte-identical. Minor 4 remains as reviewed.
- A context that did not author the D4 draft reconstructed its installed assembly and static byte count independently, then checked R1/R2 and elements 1–4, 6. It found and rechecked two corrected element-1 defects, then found the unresolved element-6 O1 gap. Its final draft-fidelity disposition is **NO-PASS**. No fixture, key or expected answer was read or authored by this context or the D4 author.
- No Protocol 7 source, generated distribution, Orchestrator snapshot, kernel, release state or historical resource changed. No candidate run, fresh paired 6.5 baseline, fixture-custodian work, full §11 qualification contract, human trial, Stage A capability-preservation map, or stage acceptance suite ran. None is counted as a pass. Stage A is incomplete because the mandated stop fired before its remaining obligations. The repository acceptance workflow for semantic source/generated descendants has not yet become applicable. `git diff --check` passed; using Python 3.11 through uv and the read-only cached PyYAML 6.0.2 package, `source/release_state.py` passed (coherent) and `source/project_engineering_memory.py PROJECT-ENGINEERING-MEMORY.md` passed (5 families, 0 notices). The first attempts lacked PyYAML in uv's isolated environment; online resolution failed because DNS was unavailable, so those attempts are not counted as checks.

Next stop point: stakeholder disposition of the measured backstop breach and the frozen label-table conflict, then a fresh independent Review for any change to workplan substance before dependent work proceeds.
