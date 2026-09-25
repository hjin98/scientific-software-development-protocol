---
kind: independent-review-handoff
protocol_under_review: 6.5.0
status: p9-no-pass-repair-required
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
candidate_branch: ssdp-6.5-frontier-model-re-evaluation
draft_pr: 33
p9_mechanical_qualification_run: 36091484812
p9_binding_descendant: 69f7cda3bd9bdfdbc113b4ec5ac6da044a7d46ab
p9_binding_qualification_run: 36091605214
p9_review: qualification/ssdp65/INDEPENDENT-REVIEW-2026-09-24-PROTOCOL-6.5-P9-NO-PASS.md
p9_review_commit: 98fcef496f10d4980d97099ea4607d60ef3e812a
p9_review_status: NO_PASS
blocking_finding: B65-P9-1
serious_challenge: none
d3_reopened: false
stakeholder_ratification: NOT_REQUESTED
public_fallback: UNAVAILABLE
recovery: UNAVAILABLE
---

# Protocol 6.5 Lifecycle Handoff — After P9 NO-PASS

## Current boundary

Accepted control remains:

`P0 = 55c085261eb827e3047637d045a8e6917ea6b962`

Immutable failed Review subject:

`P9 = fb347272c70b6225743fdc99e9bec8b4197aad49`

Durable independent Review:

`qualification/ssdp65/INDEPENDENT-REVIEW-2026-09-24-PROTOCOL-6.5-P9-NO-PASS.md`

Review publication commit:

`98fcef496f10d4980d97099ea4607d60ef3e812a`

P1-P9 are immutable historical Review subjects. **Do not repair P9 in place.** Any semantic repair creates a new candidate identity.

Current release state:

- accepted-current: Protocol 6.4;
- candidate semantic ref: exact P9;
- Review: `NO_PASS`;
- stakeholder ratification: `NOT_REQUESTED`;
- public fallback: `UNAVAILABLE`;
- recovery: `UNAVAILABLE`;
- Protocol 7 D3/D4: unchanged.

## Surviving blocker

**B65-P9-1 — governed release-state owner deletion is conflated with genuine pre-owner ancestry in production predecessor resolution.**

Exact owner: D4 `source/release_state.py`, in the ancestry/predecessor classifier used by the real release-state validation path.

P9 correctly traverses owner-present Git ancestry without making timestamp/path-log/sibling ordering authoritative. The remaining defect is that a parent lacking `PROTOCOL-RELEASE-STATE.yaml` is unconditionally treated as genuinely pre-owner.

That assumption is false when a lineage:

1. already contained the governed root owner;
2. later deletes that owner;
3. continues for one or more commits;
4. later merges into a branch whose tree restores the owner.

In that topology, P9 can silently omit the malformed governed lineage and validate only the other predecessor boundary.

## Authorized D4 repair

Alter the existing ancestry classifier only.

Required behavior:

1. Distinguish a valid parsed release state from path absence.
2. When a traversed parent lacks the owner, inspect that lineage's ancestry to determine whether the owner genuinely never existed.
3. If no governed ancestor exists, the lineage is genuinely pre-owner and may contribute no predecessor state.
4. If a governed ancestor exists, owner deletion/reintroduction is a malformed governed transition and must fail validation rather than being ignored.
5. The result must remain independent of commit timestamps, default `git log` ordering, branch names, default/latest refs, sibling enumeration, and traversal stack order.
6. Preserve working-tree-vs-HEAD, linear transition, evidence-only descendants, consecutive transitions, equivalent owner-present parents, divergent owner-present parents, genuine pre-owner PR merges, and recovery-lineage behavior.

Do not add:

- a second release-state file;
- an owner/topology registry;
- a transition mirror/database;
- branch-name or timestamp policy;
- compatibility machinery;
- candidate-specific P9/P10 branches;
- a semantic prose parser.

Accepted Protocol 6.5 D3 remains closed.

## Mandatory repair qualification

At minimum add real-Git production-resolver cases for:

- owner introduced -> sibling deletes owner -> merge restores owner: reject;
- same topology with merge-parent order reversed: reject;
- same topology with timestamps reversed: reject;
- multiple owner-absent commits after a governed ancestor: reject;
- owner deleted then reintroduced on the same governed lineage: enforce the governed deletion/reintroduction rule explicitly;
- genuine pre-owner base parent + governed feature lineage: pass;
- long genuine pre-owner ancestry: pass;
- all P9 owner-present topology controls: remain passing;
- transition-history and recovery-lineage controls: remain passing.

Then rerun:

- complete release-state suite;
- full repository regression;
- package/profile/generated parity;
- frozen 5.16 and 6.0-6.4 resource preservation;
- current representation/predecessor-scope census as affected;
- complete Orchestrator Core acceptance;
- exact replacement-candidate normal PR workflow.

## Replacement-candidate lifecycle

Do not predeclare a replacement SHA.

After semantic repair and exact-candidate CI:

1. freeze the repair commit as the next immutable candidate identity (sequence P10);
2. bind it only from a later lifecycle descendant;
3. set its Review to `NOT_RUN`;
4. keep stakeholder ratification `NOT_REQUESTED`, public fallback/recovery `UNAVAILABLE`, accepted-current Protocol 6.4;
5. qualify the binding descendant;
6. perform a genuinely fresh independent assembled-candidate Review against exact P10.

P9 CI and Review evidence remain applicable only to their exact subjects/properties. They do not transfer whole-candidate acceptance to P10.

No stakeholder ratification, publication, recovery, accepted-current cutover, PR #33 merge, or Protocol 7 D3/D4 mutation is authorized before a replacement candidate independently passes Review.
