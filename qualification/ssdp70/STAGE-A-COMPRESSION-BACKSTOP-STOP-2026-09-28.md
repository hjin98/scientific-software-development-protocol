---
kind: protocol-stage-evidence
governing_protocol_version: 6.6.0
target_protocol_version: 7.0.0
stage: A
disposition: STOPPED-BEFORE-STAGE-B
active_serious_challenge: none-established
---

# Stage A continuation — reviewed O1 repair, compressed draft, fixed-cost stop

## Decision

The stakeholder authorized a narrow exception to the §8.3 label-table byte freeze to define element 6's O1-content condition, while keeping the fixed-cost backstop for one bounded compression pass. The workplan now has SHA-256 `69c6383b65e2a2badbafe2a4f148d0aca1bce03cd7d09889b9a037e844b07abd`; a fresh read-only independent Review returned **PASS**, recorded in `WORKPLAN-REVIEW-PROTOCOL-7.0-69C6383-PASS.md`. It found no remaining Serious Challenge in that scope. The earlier `STAGE-A-STOP-2026-09-28.md` remains historical evidence of the initial O1 gap and larger draft, not the current challenge state.

The exact compressed text is `STAGE-A-D4-ENTRYPOINT-COMPRESSED-DRAFT.md` (SHA-256 `61399a15a584f8618a0178ebd53a1a7ceda2ae0b29bd6af9f7d724c5a1b9f91f`). A context that authored neither it nor the workplan amendment independently checked R1/R2, frozen elements 1–4 and 6, the used label meanings including O1, per-entry status/binding/asserter relations, attribution and the unchanged 6.6 body. Its final disposition was **PASS for draft fidelity and attribution**: no clear non-required owner-depth excess. It did not read or author fixture keys or expected answers. Earlier draft-check failures and their focused corrections are preserved in the review trajectory, not counted as final PASSes.

The independently reconstructed assembled draft is **14,331 B** (SHA-256 `9a3b411054fd582ab16f4a4faff88b3edadca903d89b8087183c795e9c2771b4`): immutable accepted-6.6 D4 entrypoint **7,057 B**, routing addition **951 B**, completion addition **6,232 B**, and net catalog-description change **+91 B**. Gross added-entrypoint bytes are **7,183 B**, above the 1,000 B compression target; the independent check identified no clear non-required text to remove. The static historical T1/T8 6.5 planning cap is **9,196 B**, and Stage A predeclared a **512 B** margin before any draft measurement, yielding an **8,684 B** static limit. This checked draft exceeds the planning cap by **5,135 B** and the margin limit by **5,647 B**. This is a static measurement of exact proposed text, not a fresh-paired live median and not a proof that every possible lossless wording is this size.

**Stop before Stage B.** The existing §8.3 escalation rule sends this breach to the stakeholder; neither the author nor reviewer may relax the backstop, drop a required element, or move it off the consumed surface. The stakeholder may direct a further bounded compression attempt within the frozen duties, change placement through a governed workplan change and fresh independent Review, or relax the backstop by explicit decision. The current draft provides no identified non-required excess to cut. The final live backstop, owner-read and T7 mode accounting remain unexecuted and cannot be treated as passed.

## Reproduction and remaining work

Measurement command (Python 3.11 via uv; `UV_CACHE_DIR` points to a writable directory):

```bash
UV_CACHE_DIR=/tmp/ssdp70-uv-cache uv run --no-project --python 3.11 python qualification/ssdp70/measure_stage_a_d4.py --source-ref 22f4bdba53795da3a6f13f162529f3a843fc37ae --draft qualification/ssdp70/STAGE-A-D4-ENTRYPOINT-COMPRESSED-DRAFT.md --assembled /tmp/ssdp70-stage-a-d4-compressed-skill.md
```

No Protocol 7 canonical source, generated distribution, Orchestrator snapshot, kernel, release state or historical resource changed. Stage A's capability-preservation map, full §11 contract/thresholds, independent pre-run contract check and fixture-custodian designation remain unfinished because the static stop fired. No candidate or paired-baseline run, human trial, or later-stage acceptance occurred. The source/generated-descendant repository acceptance workflow was not triggered; these unexecuted checks are not passes. Next decision is the stakeholder's fixed-cost disposition before any dependent Stage B work.

Local checks after the workplan amendment and draft: `git diff --check` passed; `source/release_state.py` reported coherent release state; `source/project_engineering_memory.py PROJECT-ENGINEERING-MEMORY.md` validated schema 1 with five families and zero notices; `python -m unittest discover -s tests -v` ran **398 tests, OK, 3 skipped**, using Python 3.11 via uv and cached PyYAML 6.0.2. The three skips were the remote Protocol 6.2 public-fallback realization, remote Protocol 6.3 bootstrap realization, and exact-ref Protocol 6.4 bootstrap readiness; each requires CI or `SSDP_VALIDATE_PUBLIC_FALLBACK=1`. The tests do not establish Stage A contract completion or the unrun live backstop. Source package build/parity and Orchestrator Core snapshot/tests remain for their applicable source/generated stages.
