---
kind: protocol-stage-evidence
governing_protocol_version: 6.6.0
target_protocol_version: 7.0.0
stage: C
disposition: IMPLEMENTED-PENDING-LATER-STAGE-REGRESSION
active_serious_challenge: none
---

# Protocol 7 Stage C — existing-owner deltas

Each §3.2 REFINES row is realized as a local delta plus a route to the new owner, without redefining a routed concept.

| §3.2 / §12 Stage C item | Owner | Delta |
|---|---|---|
| D1 O1 and §7 D1 consequences | `scientific-formulation.md` | "Scientific inspectability need (O1)": (i) need items, (ii) marked surface with product-scope acceptance, exploratory/confirmatory selection accounting, no plots/storage unless scientifically necessary |
| D2 O1 and §7 D2 consequences | `numerical-algorithm-design.md` | "Numerical inspectability need (O1)": trajectories, intermediate states, sensitivity/conditioning, decision quantities, failure/fallback regimes; not every loop variable |
| D3 O1, marked surface and §7 D3 consequences | `architecture-and-design.md` | "Realized-record architecture (O1)": RSR ownership, canonical versus derived projection, per-unit drill-down keys, retention/destructive boundaries, interim exposure, restart continuity, privacy/security/resource; no universal database; marked items not accepted by technical Review |
| Evidence: RSR/observation overlap; inquiry status on `CHALLENGES` | `evidence-evolution-and-dependencies.md` | Overlap mapping with observation existence realization-based and lifecycle unchanged; exploratory/confirmatory inquiry status separate from strength, applicability and disposition |
| Writing: reporting roles | `scientific-technical-writing.md` | Adds recommendation/next probe and authority Challenge; specializes the semantic-definition roles and adds no second taxonomy |
| Workflow: reverse-direction Review, Channel C and product-scope acceptance | `workflow-and-workplans.md` | "Bidirectional scientific Review", "Gate evidence (Channel C)" (anchoring, revision-gate assessments, semantic adequacy) and "Product-scope acceptance" at existing gates, with no new gate type |
| Change-plan template | `abstraction_concretization_change_plan_template.md` | §3a O1 prompts and marked-surface field; §3b revision record with predecessor identity, envelope and per-tension revision-scoped assessments with content-stated asserter, proposed status and gate carry |
| Implementation workplan template | `implementation_workplan_template.md` | §1a O1 prompts; marked-surface field with product-scope acceptance status and binding, or "proposed"; variant-search disclosure field |

The workflow owner, which T7 reads, grew by the Channel C, bidirectional Review and product-scope text. Stage E remeasures it before any live run, as the §8.3 backstop requires.

**Regression.** Python 3.11 via uv, `python -m unittest discover -s tests`: the same **16 failures and 2 errors** as Stage B, with 3 skips. That set is the known Stage E version-identity, dist and Orchestrator-profile set, and there are no new failures. `git diff --check` is clean.
