---
kind: protocol-stage-evidence
governing_protocol_version: 6.6.0
target_protocol_version: 7.0.0
stage: D
disposition: IMPLEMENTED-INDEPENDENTLY-CHECKED-PENDING-STAGE-E-REGRESSION
active_serious_challenge: none
---

# Protocol 7 Stage D — routing and placement

**Placement (§8.3, frozen).** Each role entrypoint carries one R1/R2 routing line and one clause headed "Scientific completion when the predicate above applies, including local repairs". The clause holds:

- elements 1–4 and 6 in all four roles;
- element 5 in `scientific-formulation` and `numerical-algorithm-design` only;
- element 7 in the D1/D2/D3 roles only.

The specialists are placed as follows:

- `software-documentation` has R1/R2 and elements 1, 4 and 6;
- `software-maintenance-audit` has R1/R2 and elements 1 and 4;
- `repository-hygiene` is unchanged.

Every R1/R2 line and element text has a single wording across entrypoints. No 6.6 entrypoint line is removed or reworded, and the kernel is unchanged. The only description amendment is the D4 one. It adds run/analyze, results-review and gate-evidence task classes and keeps the scientific/technical scope.

**D4 identity.** The generated D4 entrypoint is 14,331 B. It is byte-identical, apart from the version stamp, to the Stage A assembly that was independently fidelity-checked (`STAGE-A-D4-ENTRYPOINT-COMPRESSED-DRAFT.md`). It is under the static limit of 16,208 B, which is 2.0 × the 8,360 B planning denominator minus the 512 B margin. That limit is planning evidence, not a fresh paired live median.

**Gross generated additions** against the immutable 6.6 dist, excluding the description (`measure_entrypoint_additions.py`):

| Entrypoint | 6.6 B | Generated B | Gross added B | Description Δ | Removed 6.6 lines |
|---|---:|---:|---:|---:|---:|
| scientific-formulation | 6,317 | 15,131 | 8,814 | +0 | 0 |
| numerical-algorithm-design | 6,559 | 15,373 | 8,814 | +0 | 0 |
| software-design | 8,397 | 16,538 | 8,141 | +0 | 0 |
| software-implementation | 7,057 | 14,331 | 7,183 | +91 | 0 |
| software-documentation | 6,264 | 11,283 | 5,019 | +0 | 0 |
| software-maintenance-audit | 5,837 | 9,452 | 3,615 | +0 | 0 |
| repository-hygiene | 7,370 | 7,370 | 0 | +0 | 0 |

Per-element attribution (B): R1/R2 950 (948 as a specialist paragraph); heading 83; element 1 2,070; element 2 764; element 3 1,396; element 4 510; element 5 about 672; element 6 1,403; element 7 957; blank-line framing only. Every entrypoint exceeds the 1,000 B SD-B target. The independent check attributes the whole excess to required elements and their label meanings. Per SD-B, that excess is reported for the ratification package, not cut by dropping or weakening elements.

**Routed owners reconciled** (§3.2 ROUTES, one line each, no parallel definition): storage, configuration, testing, security and concurrency.

**Independent check.** A context that authored neither the workplan nor this wording checked attribution and losslessness.

- `STAGE-D-INDEPENDENT-WORDING-CHECK-NO-PASS.md` found one blocker, B1: element 5 said "stays proposed" where the frozen text says "marked proposed". It also reported minors m1–m5.
- B1 and m1–m4 are repaired. m5, the Markdown numbering of gapped element numbers, is cosmetic and allowed by §8.3.
- `STAGE-D-INDEPENDENT-WORDING-RECHECK-PASS.md` found every finding closed except the cosmetic m5, confirmed nothing else moved, and judged the 45,958 B owner not disproportionate to the doctrine.
- This check satisfies the §8.3/§12 Stage D pre-freeze attribution and losslessness requirement for this wording. A later wording change needs a new check.

**Regression.** Package validation passes on a scratch build. The repository suite shows the Stage B/C known set plus `test_registry_resources_are_exactly_directly_linked`, which reads the committed `dist/`. All of those are Stage E generated-descendant dependencies, and there is no source-level regression.
