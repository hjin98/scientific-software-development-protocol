---
kind: independent-review-handoff
protocol_under_review: 6.5.0
status: ready-p12
accepted_control_p0: 55c085261eb827e3047637d045a8e6917ea6b962
failed_candidate_p1: b565e28aeacea002cefe27e6b9594fe99d653c0a
failed_candidate_p2: e8edb353e172aef933ed5e58eeabe897d0cc98d1
failed_candidate_p3: 89ccc71a7b0e9458a3e77306be2a773d4059f0f2
failed_candidate_p4: 43ff4273fbdaf46b9677cffdb091b741ce754a7d
failed_candidate_p5: d2d672a3e814438fb618f901137f88c8698a205d
failed_candidate_p6: dd06da8136416e67644586c44880b466f982b8ff
failed_candidate_p7: 133c747a1f9ab4372c9e1af7a7e9666316dc892b
failed_candidate_p8: ed782ccad73b43c9052ecc926177c36846b9328d
failed_candidate_p9: fb347272c70b6225743fdc99e9bec8b4197aad49
failed_candidate_p10: 275b23bfa45cc72145d2079c8d945a6ff5a5c216
failed_candidate_p11: 6352accc7962fc188976fc1bcea5e081681d99c5
immutable_candidate_p12: c6a0e9b2ad54fd2cea39bc9a4a1a480c0b9c25f6
candidate_branch: ssdp-6.5-frontier-model-re-evaluation
draft_pr: 33
p12_mechanical_qualification_run: 36121450601
p12_binding_descendant: dc1595219ebfd76ee2451b406a549a4a012370e0
p12_binding_qualification_run: 36121601230
p12_repair_qualification: qualification/ssdp65/P12-REPAIR-QUALIFICATION.md
p12_freeze_binding: qualification/ssdp65/P12-FREEZE-BINDING.md
p12_binding_qualification: qualification/ssdp65/P12-BINDING-QUALIFICATION.md
p11_review: qualification/ssdp65/INDEPENDENT-REVIEW-2026-09-25-PROTOCOL-6.5-P11-NO-PASS.md
historical_capability_preservation_review: qualification/ssdp65/HISTORICAL-CAPABILITY-PRESERVATION-REVIEW-2026-09-25-P9.md
authoring_context_verdict: none
stakeholder_ratification: NOT_REQUESTED
---

# Independent Review Handoff — Protocol 6.5 P12

## Immutable Review target

Perform a genuinely fresh independent assembled-candidate Review of:

`P12 = c6a0e9b2ad54fd2cea39bc9a4a1a480c0b9c25f6`

against accepted Protocol 6.4 control:

`P0 = 55c085261eb827e3047637d045a8e6917ea6b962`

P1-P11 are immutable failed candidates and historical evidence only. P12 itself is the semantic Review target.
Do not substitute the mutable branch head or binding descendant for P12. Later descendants are qualification/lifecycle
evidence only.

## Current lifecycle boundary

Binding descendant:

`dc1595219ebfd76ee2451b406a549a4a012370e0`

Binding workflow:

`36121601230`

Expected entering Review:

- accepted-current: Protocol 6.4;
- candidate version: 6.5.0;
- candidate semantic ref: exact P12;
- Review: `NOT_RUN`;
- stakeholder ratification: `NOT_REQUESTED`;
- public fallback: `UNAVAILABLE`;
- recovery: `UNAVAILABLE`;
- Protocol 7 D3/D4: unchanged.

Independently verify this state.

## Independence and authority reconstruction

Reconstruct applicable D1-D4/current project authority independently. Use prior Reviews, workplans, qualification
records, preservation maps, historical-capability records, and PEM only as evidence/hypothesis inputs.

Do not inherit P11 NO-PASS conclusions, P12 repair-author conclusions, obligation matrices, test decomposition, or
green CI as semantic acceptance.

Perform the Serious Challenge pass before ordinary D4 findings. Reopen D3 only for a true accepted-authority defect.

## Mandatory B65-P11-1 repair falsification

P12 was created to repair:

**B65-P11-1 — non-shallow Git state can still be mistaken for complete canonical ancestry.**

Inspect the real production resolver and actual call path in exact P12. Do not rely only on authored tests.

P12's intended repair is:

- historical path absence is distinguished from unreadable/unavailable object state;
- replacement refs do not redefine release-history authority;
- deprecated graft traversal overlays do not redefine release-history authority;
- canonical parent identities come from raw commit objects;
- missing commit/tree/blob/path evidence needed by a negative ancestry claim fails closed;
- readable alternates/promisor-backed objects may remain usable when Git can actually resolve them;
- a genuine pre-owner conclusion is allowed only after the complete canonical parent graph has been traversed.

At minimum independently falsify:

1. non-shallow missing historical owner blob;
2. non-shallow missing historical owner tree/path object;
3. standard shallow boundary hiding owner introduction;
4. shallow missing merge-parent lineage;
5. active replacement ref hiding owner introduction;
6. deprecated graft hiding owner introduction;
7. readable alternate object store;
8. partial/promisor object availability where supported;
9. complete-history genuine first owner introduction;
10. complete-history genuine pre-owner merge parent plus governed feature lineage;
11. visible post-introduction deletion/restoration;
12. reversed merge-parent order;
13. reversed relevant timestamps;
14. multiple commits while owner absent;
15. same-lineage deletion followed by committed reintroduction;
16. working-tree transition against committed owner-present HEAD;
17. linear committed transition;
18. evidence-only descendants;
19. consecutive material transitions;
20. equivalent and divergent owner-present parents;
21. traversal-stack/sibling-enumeration independence;
22. stale/sibling/wrong-ancestry recovery;
23. complete later recovery followed by legal descendant mapping.

Construct at least one fresh holdout beyond the authored P12 tests.

Explicitly answer whether all P12 tests and normal CI could remain green while the production resolver still
overclaims a negative ancestry result, omits a governed lineage, or validates the wrong temporal transaction.

Do not introduce branch/default/latest/timestamp/parent-order/traversal-order/candidate-identity authority.

## Re-falsify historical blocker families

Proportionately re-falsify current owners for:

- B65-P11-1 canonical ancestry/readability completeness;
- B65-P10-1 incomplete ancestry vs genuine pre-owner;
- B65-P9-1 governed deletion vs pre-owner ancestry;
- B65-P8-1 predecessor resolution / merge ordering;
- B65-P7-1 transition continuity and recovery lineage;
- B65-P6-1 strict root-state parser convergence;
- B65-P6-2 canonical semantic-version/history ordering;
- B65-P5-1 duplicate-key root ambiguity;
- B65-P5-2 candidate/history succession;
- B65-P4-1 evidence-front-matter ambiguity;
- B65-P3-1 exact Review/ratification subject binding;
- B65-P3-2 current representation convergence;
- B65-P2-1/B65-R2 mutable lifecycle duplication;
- B65-P2-2/B65-R1 immutable evidence applicability;
- B65-R3 predecessor-version gating.

## Full assembled-candidate Review

Independently re-establish:

- Serious Challenge status;
- DF-1 through DF-4;
- local-compliance/global-failure trajectories;
- out-of-matrix abstraction adequacy;
- qualification-method limits;
- fresh machine/state/topology/schema/generated and prose-semantic mutants;
- P65-1 through P65-6 causal usefulness;
- Protocol 6.4 -> 6.5 preservation;
- historical capability preservation from Protocol 5.13-5.16 and 6.0-6.4;
- frozen historical profile/prompt identity;
- current source/generated/package/reference convergence;
- evidence applicability/staleness;
- simplicity/total-system complexity;
- Protocol 7 D3/D4 isolation;
- SSDP self-application.

Capability, not obsolete wording or historical mechanism identity, is the preservation oracle.

## Evidence boundaries

Exact P12 normal workflow:

`36121450601`

Binding descendant:

`dc1595219ebfd76ee2451b406a549a4a012370e0`

Binding workflow:

`36121601230`

Durable bounded evidence:

- `qualification/ssdp65/P12-REPAIR-QUALIFICATION.md`
- `qualification/ssdp65/P12-FREEZE-BINDING.md`
- `qualification/ssdp65/P12-BINDING-QUALIFICATION.md`
- `qualification/ssdp65/INDEPENDENT-REVIEW-2026-09-25-PROTOCOL-6.5-P11-NO-PASS.md`
- `qualification/ssdp65/HISTORICAL-CAPABILITY-PRESERVATION-REVIEW-2026-09-25-P9.md`

These establish only their discriminated mechanical/lifecycle/historical properties. They do not establish semantic
Review PASS.

## Disposition boundary

PASS means only:

`P12 is technically eligible for stakeholder ratification.`

PASS does not ratify Protocol 6.5, publish public fallback, establish recovery, change accepted-current, merge PR #33,
or mutate Protocol 7 D3/D4.

If a genuine semantic blocker survives, preserve P12 immutably, publish NO-PASS, reopen at the earliest owner, and
require another candidate identity for semantic repair.
