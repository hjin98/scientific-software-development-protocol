---
kind: stakeholder-decision-record
governing_protocol_version: 6.6.0
target_protocol_version: 7.0.0
decision_date: 2026-09-28
---

# Protocol 7.0 fixed-cost backstop relaxation

After the Stage A compressed D4 draft measured 14,331 B and breached the earlier 1.10 × accepted-6.5 fixed-cost planning backstop, the stakeholder directed: “Relax the backstop. This is a large revision so a large increase in size is justified.” Asked for the replacement multiplier on each T1/T7/T8 route relative to its fresh paired 6.5 median, the stakeholder selected **2.0 ×**.

For Protocol 7.0 only, replace the numeric **1.10 ×** in the fixed-cost backstop with **2.0 ×** on each T1, T7 and T8. The denominator remains the fresh paired accepted-6.5 median, measured in 6.6 run mode with the same accounting, counterbalancing and T7 mode-replication rule. The Stage A predeclared **512 B static margin** remains. The 1,000 B gross addition compression target, lossless required-element attribution, all non-size floors and the stop/escalation rule remain. No required element may be dropped, weakened or moved off its consumed surface to satisfy size.

This stakeholder decision supersedes the earlier 1.10 × Protocol 7 planning backstop wherever it appears in the handoff, including frozen §8.3. That section's bytes remain unchanged under the freeze; this record and the handoff's current-disposition note supply the explicit override. The historical 6.6 acceptance rule and the 2026-09-27 stakeholder decision records are unchanged. Because this changes the handoff's substance, a fresh independent workplan Review of the exact handoff plus this decision record is required before dependent Stage A closure or Stage B work.

On the historical T1/T8 6.5 entrypoint-only median of 8,360 B, the revised planning cap is 16,720 B; after the 512 B margin, the static draft limit is 16,208 B. The reviewed 14,331 B draft leaves 2,389 B to the cap and 1,877 B beyond the required margin. These are planning calculations only, not fresh paired live results. T7's owner-read mode and the generated Stage E D4/owner sizes must be remeasured before a live run.
