---
kind: ssdp65-p13-repair-qualification
status: repair-complete-candidate-frozen
protocol_version: 6.4.0
target_protocol_version: 6.5.0
p0: 55c085261eb827e3047637d045a8e6917ea6b962
failed_p12: c6a0e9b2ad54fd2cea39bc9a4a1a480c0b9c25f6
failed_prospective_repair: e01a1e7e63072b15ddbe72a226f3a4deffafc9f7
p13: 05a2b62550adadf271a27f6555da7173902c491c
exact_p13_pr_run: 36127313841
binding_descendant: 7e5e5fa68179f9b1d85ed7ab672e6333d99a1e67
binding_run: 36127440732
date: 2026-09-25
d3_reopened: false
serious_challenge: none
p12_review: qualification/ssdp65/INDEPENDENT-REVIEW-2026-09-25-PROTOCOL-6.5-P12-NO-PASS.md
---

# Protocol 6.5 P13 Repair Qualification

## Scope and identity

This record qualifies the bounded D4 repair ordered by the fresh independent P12 Review.

- accepted control P0: `55c085261eb827e3047637d045a8e6917ea6b962`
- immutable failed P12: `c6a0e9b2ad54fd2cea39bc9a4a1a480c0b9c25f6`
- failed prospective repair: `e01a1e7e63072b15ddbe72a226f3a4deffafc9f7`
- immutable replacement P13: `05a2b62550adadf271a27f6555da7173902c491c`
- exact-P13 normal workflow: `36127313841`
- binding descendant: `7e5e5fa68179f9b1d85ed7ab672e6333d99a1e67`
- binding workflow: `36127440732`

Accepted Protocol 6.5 D3 was not reopened and no Serious Challenge was raised.

## B65-P12-1 closure

All release-history ancestry predicates now derive ancestry from canonical raw commit-parent objects. The production
ancestor check no longer delegates authority to overlay-sensitive `git merge-base --is-ancestor`.

Fresh real-Git holdouts establish that:

- an active `git replace` ref can make ordinary Git traversal report a false sibling-ancestor relation, while the
  production canonical predicate rejects it;
- deprecated `info/grafts` can likewise rewrite ordinary traversal, while the production canonical predicate rejects
  it;
- the real recovery-lineage consumer rejects a replacement-rewritten sibling recovery;
- immutable Review evidence content remains bound to the canonical commit bytes under a replacement ref.

Exact immutable evidence, version, recovery-state, and transition-state reads use `--no-replace-objects`.

## B65-P12-2 closure

The release-state resolver now performs a canonical path-presence continuity pass over reachable HEAD ancestry before
transition interpretation. Governance is propagated forward over the canonical DAG. A commit lacking
`PROTOCOL-RELEASE-STATE.yaml` after any parent lineage was already governed emits a fatal validation error.

This closes the fresh P12 trajectory:

```text
A(owner) -> D(owner absent) -> B(owner reintroduced) -> C(later material state) -> evidence-only descendant
```

The malformed A -> D -> B interval remains visible and fatal at C and after evidence-only descendants.

The resolver still preserves independently discoverable predecessor states while recording the fatal continuity error,
retaining prior diagnostic behavior for malformed merge histories.

## Prospective-repair reconciliation

The first prospective repair `e01a1e7...` passed repository release-state validation and Orchestrator Core but failed
full protocol regression because it unnecessarily short-circuited predecessor diagnostics after detecting invalid
history.

That commit was never frozen as a candidate.

P13 narrows the concretization: continuity remains fatal, while predecessor discovery continues for diagnostic and
transition evidence. Exact-P13 run `36127313841` passed the complete workflow.

## Mechanical evidence

Exact-P13 run `36127313841` passed:

- repository release-state validation;
- project engineering memory validation;
- complete protocol regression, including the fresh canonical-ancestry and later-transition-laundering holdouts;
- canonical skill-package build;
- independent generated-package validation;
- committed distribution parity;
- whitespace validation;
- Protocol 6.5 snapshot parity;
- complete Orchestrator Core acceptance.

Binding run `36127440732` passed the same build/Core gates with exact P13 bound in the sole mutable release-state
owner at Review `NOT_RUN`.

## Candidate boundary

P13 is frozen at `05a2b62550adadf271a27f6555da7173902c491c`.

Any semantic mutation creates another candidate identity. Later descendants may carry lifecycle/qualification evidence
only.

This record is mechanical repair qualification, not independent semantic Review PASS, stakeholder ratification,
publication, recovery establishment, accepted-current cutover, PR merge, or Protocol 7 mutation.
