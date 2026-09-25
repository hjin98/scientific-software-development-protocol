---
kind: ssdp65-p12-repair-qualification
status: repair-complete-candidate-frozen
protocol_version: 6.4.0
target_protocol_version: 6.5.0
p0: 55c085261eb827e3047637d045a8e6917ea6b962
failed_p11: 6352accc7962fc188976fc1bcea5e081681d99c5
p12: c6a0e9b2ad54fd2cea39bc9a4a1a480c0b9c25f6
exact_p12_pr_run: 36121450601
binding_descendant: dc1595219ebfd76ee2451b406a549a4a012370e0
binding_run: 36121601230
date: 2026-09-25
d3_reopened: false
serious_challenge: none
p11_review: qualification/ssdp65/INDEPENDENT-REVIEW-2026-09-25-PROTOCOL-6.5-P11-NO-PASS.md
---

# Protocol 6.5 P12 Repair Qualification

## Scope and identity

This record qualifies the bounded D4 repair ordered by the fresh independent P11 Review.

- accepted control P0: `55c085261eb827e3047637d045a8e6917ea6b962`
- immutable failed P11: `6352accc7962fc188976fc1bcea5e081681d99c5`
- immutable replacement P12: `c6a0e9b2ad54fd2cea39bc9a4a1a480c0b9c25f6`
- exact-P12 normal workflow: `36121450601`
- later binding descendant: `dc1595219ebfd76ee2451b406a549a4a012370e0`
- binding workflow: `36121601230`

Accepted Protocol 6.5 D3 was not reopened and no Serious Challenge was raised.

## B65-P11-1 closure

P11 failed closed for standard shallow repositories but still treated
`git rev-parse --is-shallow-repository=false` as sufficient support for a negative ancestry claim. It also collapsed
any failed historical `git show <ref>:PROTOCOL-RELEASE-STATE.yaml` into path absence.

P12 removes that shortcut at the existing D4 owner.

Historical owner classification now requires:

1. canonical raw commit ancestry, with replacement objects disabled;
2. parent identities parsed from raw commit-object headers, so local replacement refs and deprecated `info/grafts`
   traversal overlays cannot rewrite release authority;
3. canonical tree membership checked separately from content readability;
4. genuine owner absence only when the tree is readable and the path entry is absent;
5. fail-closed behavior if a required commit, tree, path object, or owner content cannot be resolved/read;
6. a negative genuine-pre-owner conclusion only after the complete canonical parent graph has been traversed.

This is a bounded replacement of the former negative-proof mechanism. It introduces no second state owner, registry,
transition mirror, topology service, compatibility layer, candidate-specific policy, timestamp policy, branch policy,
or default/latest authority.

## Fresh real-Git owner-path evidence

Exact P12 adds production-resolver holdouts for:

- non-shallow missing historical owner blob: fail closed;
- non-shallow missing historical tree: fail closed;
- replacement-ref ancestry that hides owner introduction from ordinary traversal: canonical ancestry still identifies
  the governed lineage;
- deprecated graft ancestry that hides owner introduction from ordinary traversal: canonical raw-parent ancestry still
  identifies the governed lineage;
- readable alternate object store: remains admissible; governed history is resolved through the alternate rather than
  rejected merely because storage is non-local.

Existing controls remain active for:

- both P11 shallow-history negatives;
- genuine complete-history first owner introduction;
- genuine pre-owner merge ancestry;
- visible owner deletion/reintroduction;
- reversed merge-parent order and timestamps;
- prolonged owner absence;
- same-lineage deletion/reintroduction;
- ordinary linear transitions;
- evidence-only descendants;
- consecutive transitions;
- equivalent/divergent owner-present parents;
- transition continuity, recovery lineage, canonical semantic versions, strict YAML parsing, and exact
  Review/ratification evidence binding.

## Mechanical evidence

Exact-P12 run `36121450601` passed:

- repository release-state validation;
- project engineering memory validation;
- complete protocol regression including all new canonical-ancestry/object-availability holdouts;
- canonical package build;
- independent generated-package validation;
- committed distribution parity;
- whitespace validation;
- Protocol 6.5 snapshot parity;
- complete Orchestrator Core acceptance.

Binding run `36121601230` passed the same build/Core gates with exact P12 bound in the sole mutable release-state
owner at Review `NOT_RUN`.

## Candidate boundary

P12 is frozen at `c6a0e9b2ad54fd2cea39bc9a4a1a480c0b9c25f6`.

Any later semantic mutation creates another candidate identity and invalidates P12-specific Review applicability.
Later descendants may carry lifecycle/qualification evidence only.

This record establishes mechanical repair qualification. It is not independent semantic Review PASS, stakeholder
ratification, public-fallback publication, recovery establishment, accepted-current cutover, PR merge, or Protocol 7
mutation.
