---
kind: protocol-stage-evidence
governing_protocol_version: 6.6.0
target_protocol_version: 7.0.0
stage: A
status: predeclared-before-d4-draft-measurement
---

# Stage A static fixed-cost premeasurement declaration

This declaration precedes the first measurement of the current D4 wording. It is evidence coordination, not a relaxation of the stakeholder's fixed-cost backstop. The current workplan is the reviewed SHA-256 `ad0a4414c6492ee865784dc9e669d1e21d9194ebb0dfe2cdb639106ff236eea4`; the separate read-only Review is `WORKPLAN-REVIEW-PROTOCOL-7.0-AD0A441-PASS.md`. Accepted 6.6.0 public source `22f4bdba53795da3a6f13f162529f3a843fc37ae` and historical 6.5.0 source `7f7b5e24858e813e45ace867a7f8ea5180f43bf0` resolve from root `PROTOCOL-RELEASE-STATE.yaml`.

## Fixed decision rule and margin

The backstop is the workplan's median candidate active SSDP bytes at most 1.10 times the fresh paired accepted-6.5 median on **each** T1, T7 and T8 in 6.6 run mode. The 6.6 accounting includes the entire installed `SKILL.md` including description and framing, plus SSDP files read. The historical 6.5 entrypoint is 8,360 B and the 6.6 entrypoint is 7,057 B; 9,196 B is the planning cap from the historical T1/T8 6.5 median, not a substitute for fresh paired baseline runs.

**Predeclared static margin: 512 B**, independently on T1, T7 and T8, after accounting for the largest SSDP owner-read addition observed in each relevant historical mode. T1/T8 observed entrypoint-only mode. T7 observed both entrypoint-only and workflow-owner mode; the 6.6 owner-read addition was 24,800 − 7,057 = 17,743 B, while the 6.5 owner-read addition was 25,188 − 8,360 = 16,828 B. For the historical entrypoint-only planning mode this requires a drafted whole D4 entrypoint of at most 9,196 − 512 = **8,684 B**. For the historical T7 owner-read planning mode it requires draft entrypoint plus 17,743 B at most 27,706.8 − 512 = **27,194.8 B**. The stricter T1/T8 bound governs the Stage A draft. A draft over the cap, or leaving less than this margin, triggers a stop and stakeholder escalation before Stage B. The margin is a buffer for observed SSDP reads, not permission to drop or weaken a required element.

For later T7 live qualification, begin with three fresh paired, order-counterbalanced runs per arm. If either arm has both entrypoint-only and owner-read observations among those three, add two paired runs (five total); if either arm remains mixed, add two more paired runs (seven total), then stop replication and report the mode mixture and median-rule result or unresolved uncertainty. This mode-based rule applies symmetrically before seeing outcomes. Report every run's mode and matched-mode comparisons beside, never in place of, the stakeholder's median rule. Stage E must remeasure the generated D4 entrypoint and the T7-read workflow owner before any candidate live run.

The 1,000 B gross added-entrypoint target and per-element attribution remain separate from this fixed-cost backstop. A target excess attributable to lossless required elements is reported; non-required excess is a D4 defect. No candidate runs, fixture keys or expected answers are involved in this declaration.
