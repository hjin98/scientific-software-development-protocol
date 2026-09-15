from pathlib import Path


def replace_once(path: str, old: str, new: str, label: str) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if old not in text:
        raise SystemExit(f"missing {label} anchor in {path}")
    p.write_text(text.replace(old, new, 1), encoding="utf-8")


workplan = "workplans/active/SSDP-6.4-AXIOMATIC-FORMAL-DEFINITION-AND-SEMANTIC-TRACEABILITY-CONSOLIDATED.md"
replace_once(
    workplan,
    "independent_review_state: repaired-awaiting-fresh-review",
    "independent_review_state: no-pass-reopened",
    "review state",
)
replace_once(
    workplan,
    "implementation_handoff: repair-complete-fresh-review-required",
    "implementation_handoff: repair-required",
    "implementation handoff",
)
replace_once(
    workplan,
    "**B64-R4/B64-R5 REPAIR COMPLETE; FRESH STAGE-E REVIEW REQUIRED.** The active lifecycle index now reflects completed Stage C qualification and the authorized Protocol 6.4 public bootstrap, and QF64-P now validates that real current index with discriminating stale-state counterfactuals. No Serious Challenge is active. The repair does not change the published public-source semantics or bootstrap identity. Protocol 6.3 remains accepted-current; Protocol 6.4 recovery remains unavailable; Stage F remains blocked. The next immutable assembled target is bound only from the descendant Stage-E handoff after exact-target ordinary PR CI; a fresh independent full Stage-E Review is still required before Stage F.",
    "**FRESH STAGE-E REVIEW: NO-PASS — REOPENED.** Independent Review of immutable assembled target `05b6d821dcdb885c86db79e38ce1e23a24863b3f`, bound by descendant handoff `34434c2e0ab6bdc5b69acaff56b1357677d28c85` and exact-target ordinary PR qualification run `34994976466`, found two blocking D4 qualification/current-lifecycle-oracle defects: B64-R6 and B64-R7. No Serious Challenge is active. Detailed findings and owner-layer repair instructions are in `qualification/ssdp6/INDEPENDENT-REVIEW-2026-09-15-PROTOCOL-6.4-05B6-NO-PASS.md`. Protocol 6.3 remains accepted-current; Protocol 6.4 recovery remains unavailable; Stage F remains blocked. After repair, freeze a new immutable assembled target, obtain exact-target ordinary PR CI, bind it from a later descendant handoff, and perform another fresh full Stage-E Review of all P64-A..P64-O, QF64-A..QF64-P and F64-A..F64-L.",
    "current disposition",
)

idx = "workplans/active/SSDP-6.1-7.0-WORKPLAN-AUTHORITY-INDEX.md"
replace_once(
    idx,
    "STAGE E INDEPENDENT REVIEW: NO-PASS - B64-R4/B64-R5 REPAIRED; FRESH REVIEW REQUIRED",
    "STAGE E INDEPENDENT REVIEW: NO-PASS - B64-R6/B64-R7 REPAIR REQUIRED; FRESH REVIEW REQUIRED",
    "authority-index Stage E disposition",
)
