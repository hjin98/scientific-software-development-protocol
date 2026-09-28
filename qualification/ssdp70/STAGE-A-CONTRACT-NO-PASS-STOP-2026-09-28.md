---
kind: protocol-stage-evidence
governing_protocol_version: 6.6.0
target_protocol_version: 7.0.0
stage: A
disposition: STOPPED-BEFORE-STAGE-B
active_serious_challenge: none-established
---

# Stage A stop — qualification framework NO-PASS

## Decision and completed evidence

The stakeholder relaxed the Protocol 7 fixed-cost multiplier to **2.0 ×** the fresh paired accepted-6.5 median on each T1/T7/T8 route, preserving the 512 B predeclared static margin, all non-size floors and lossless required elements. The durable decision is `STAKEHOLDER-DECISION-2026-09-28-PROTOCOL-7.0-BACKSTOP-RELAXATION.md`. A fresh independent Review **PASS** on exact workplan SHA-256 `66f29437af5bde3381a66c8a7609ef3ee87b230f32c210eb7fbf1858e22d78b1` and decision SHA-256 `b1ae718c37e17c085146eac085f69e3fc7b6ae5825003fe2c0be746d86cc85e2` is recorded in `WORKPLAN-REVIEW-PROTOCOL-7.0-66F2943-PASS.md`. Frozen §8.3 and §14 remain byte-identical to the preceding reviewed handoff.

The independently fidelity-checked compressed D4 draft remains **14,331 B**, SHA-256 `9a3b411054fd582ab16f4a4faff88b3edadca903d89b8087183c795e9c2771b4`. It has 7,183 B gross added entrypoint text, attributable to R1/R2 and required elements. Against the historical T1/T8 6.5 8,360 B entrypoint-only median, the revised static planning cap is **16,720 B** and the predeclared-margin limit is **16,208 B**; the draft leaves **2,389 B** to the cap and **1,877 B** beyond the margin. The measurement is static planning evidence, not a fresh paired T1/T7/T8 median. Stage E generated D4 and T7-read owner remeasurement and all live runs remain due.

Stage A drafted `STAGE-A-BASIS-AND-PRESERVATION.md` (PEM basis/HAS, immutable 6.6 owner comparison, Protocol 8/index boundary, capability map, route classes and hygiene sentinel) and `PROTOCOL-7.0-EVALUATION-AND-QUALIFICATION-CONTRACT.md` (numeric thresholds and custody framework). The independent framework check returned **NO-PASS**, not a frozen §11 contract. Its three material gaps are:

1. A pooled ≥8/10 owner-load-hit floor could pass while every authority-authoring and gate-evidence R2 opportunity misses; it does not protect each trigger class.
2. The unnamed-class ≥5/6 detection floor is labeled under non-critical detection although the minimum unnamed set may consist of critical properties; its denominator and independent operation are unclear.
3. Four human participants total with no per-arm exposure floor can leave one arm represented by one participant, five routine answers and one critical answer; the human comparison is underexposed.

The checker also identified **required pre-run evidence not yet available**: separate fixture custodian designation; withheld classification, opportunity and oracle-branch check; actual-harness known-broken/known-good, side-effect capture, composite-mode and cheap-first-look probes. Their absence is not a pass. No Protocol 7 fixture keys or expected answers were authored/read by this context. No candidate run or human trial occurred. The independent route-class review found no proven misclassification from the visible task text; withheld-context verification remains due.

**Stop before Stage B.** The user's blocker rule requires reporting this NO-PASS rather than silently repairing the framework or treating unrun checks as passed. The next stop point is an authorized Stage A contract correction followed by a fresh independent check, custodian separation and the remaining pre-run evidence. Stages B–F, Stage G Review and Stage H release have not begun.

## Repository checks and limits

Using Python 3.11 via uv, the current workplan/evidence-only state passed `source/release_state.py` (coherent), `source/project_engineering_memory.py PROJECT-ENGINEERING-MEMORY.md` (schema 1; five families, zero notices), and `python -m unittest discover -s tests -v` (**398 OK, 3 skipped**); `git diff --check` passed. The three existing skips are remote Protocol 6.2 fallback, Protocol 6.3 bootstrap and Protocol 6.4 exact-ref bootstrap readiness (CI or `SSDP_VALIDATE_PUBLIC_FALLBACK=1`). Source/generated-descendant package build, committed distribution parity, frozen-resource integrity and Orchestrator Core snapshot/tests are not triggered by this Stage A evidence-only attempt; they remain required in later applicable stages. These passing checks do not close the three contract gaps or unrun evidence.
