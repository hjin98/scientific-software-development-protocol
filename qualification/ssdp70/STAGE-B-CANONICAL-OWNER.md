---
kind: protocol-stage-evidence
governing_protocol_version: 6.6.0
target_protocol_version: 7.0.0
stage: B
disposition: IMPLEMENTED-PENDING-LATER-STAGE-REGRESSION
active_serious_challenge: none
---

# Protocol 7 Stage B — canonical owner

- `source/PROTOCOL_VERSION` is `7.0.0` in the same change as the first version-intrinsic Protocol 7 source edit (workplan §12 Stage B). This labels the working source only. It adopts nothing for this 6.6-governed cycle and leaves `PROTOCOL-RELEASE-STATE.yaml` unchanged. `source/release_state.py` still reports coherent.
- New owner `source/shared/references/scientific-inspectability-and-initiative.md` (46,421 B, SHA-256 `b71daa8cc5d3afd565c206a2f50ae677477ffa1f35a6a2a4abc04ade270bf29d`) carries the following:
  - the §3.1 terms;
  - §4 obligation binding (O1–O3, the no-O1 default and §4.5 floor);
  - §5 channels;
  - §6.1–§6.5 doctrine;
  - the §6.6 gate-evidence summary, routed to workflow;
  - the §7 D4 consequence;
  - the frozen §8.2 predicate and owner-load trigger text, verbatim, with the §8.2/§8.3 evaluation and local-work-exemption rules;
  - §9–§10;
  - the §8.3/§15 consumed-surface route limitations and adoption guidance.
- ROUTES rows are cited by link and not redefined. REFINES content lands in the respective owners in Stage C.
- **Size.** The owner is close to the lossless size of the workplan's doctrine sections (§3.1, §4–§7, §9 and §10 total about 47 KB). An earlier 51.6 KB wording was compressed without dropping normative content. Contract §4 requires the owner size to be reported before live runs. The independent pre-run checker judges whether the class-(iii) bound stays discriminating with it. That bound is paired 6.6 plus the entrypoint delta plus one owner read plus 512 B. No entrypoint routes to the owner yet; Stage D adds R1/R2.

**Regression.** Python 3.11 via uv, `python -m unittest discover -s tests`: 398 run, **16 failures and 2 errors**, 3 skipped. Every failure is one of three known Stage E dependencies:

- current-version identity pins that still expect major version 6;
- committed `dist/` entry contracts still stamped `6.6.0`, which regeneration fixes;
- the missing `ssdp-protocol-7.0` Orchestrator profile resource.

The exact failing set is recorded in the Stage B commit message. Stage E must clear it, and any new failure in later stages is a regression. `git diff --check` is clean. Package build, parity and Orchestrator checks run at Stage E/F.
