---
kind: ssdp65-p11-repair-qualification
status: repair-complete-candidate-frozen
protocol_version: 6.4.0
target_protocol_version: 6.5.0
p0: 55c085261eb827e3047637d045a8e6917ea6b962
failed_p10: 275b23bfa45cc72145d2079c8d945a6ff5a5c216
p11: 6352accc7962fc188976fc1bcea5e081681d99c5
exact_p11_pr_run: 36103358186
binding_descendant: 0490ecb0c685b403df78f62f143896c44c078d68
binding_run: 36103484871
date: 2026-09-25
d3_reopened: false
serious_challenge: none
p10_review: qualification/ssdp65/INDEPENDENT-REVIEW-2026-09-25-PROTOCOL-6.5-P10-NO-PASS.md
---

# Protocol 6.5 P11 Repair Qualification

## Scope and identity

This record qualifies the bounded D4 repair ordered by the fresh independent P10 Review.

- accepted control P0: `55c085261eb827e3047637d045a8e6917ea6b962`
- immutable failed P10: `275b23bfa45cc72145d2079c8d945a6ff5a5c216`
- immutable replacement P11: `6352accc7962fc188976fc1bcea5e081681d99c5`
- exact-P11 normal workflow: `36103358186`
- later binding descendant: `0490ecb0c685b403df78f62f143896c44c078d68`
- binding workflow: `36103484871`

Accepted Protocol 6.5 D3 was not reopened and no Serious Challenge was raised.

## B65-P10-1 closure

P10's positive ancestry classification was correct when a governed owner was visible, but its negative inference
treated an empty exact-path history result as proof that the lineage had never contained
`PROTOCOL-RELEASE-STATE.yaml`. That claim is unsound in shallow/incomplete Git history.

P11 changes only the existing D4 ancestry classifier. After the exact-path owner-history search finds no visible
governed owner, the resolver asks Git whether the repository is shallow.

- visible governed owner -> governed lineage, unchanged;
- no visible owner + complete/non-shallow repository -> genuinely pre-owner remains admissible;
- no visible owner + shallow repository -> explicit validation error / fail closed;
- ancestry-completeness query failure or unrecognized result -> fail closed.

The repair does not select predecessors and introduces no timestamp, branch-name, default/latest, sibling-order,
traversal-order, registry, state mirror, topology service, compatibility layer, or candidate-specific policy.

## Fresh real-owner topology evidence

Exact P11 adds real temporary-Git production-resolver holdouts for:

- governed owner introduction hidden beyond a depth-1 shallow boundary, followed by visible owner deletion and
  working-tree reintroduction: fail closed;
- governed owner introduction hidden beyond a depth-2 shallow boundary on a missing merge-parent lineage: fail closed.

Existing complete-history controls remain active for:

- genuine first owner introduction from pre-owner HEAD;
- genuine pre-owner merge lineage plus governed feature lineage;
- visible owner deletion/restoration;
- reversed merge-parent order and timestamps;
- prolonged owner absence;
- same-lineage deletion/reintroduction;
- linear, evidence-only, consecutive, equivalent and divergent owner-present ancestry;
- transition continuity, recovery lineage, canonical semantic versions, and exact Review/ratification evidence binding.

## Mechanical evidence

Exact-P11 run `36103358186` passed:

- repository release-state validation;
- PEM validation;
- complete protocol regression, including both fresh shallow-history holdouts;
- canonical skill-package build;
- independent generated-package validation;
- committed distribution parity;
- whitespace validation;
- Protocol 6.5 snapshot parity;
- complete Orchestrator Core acceptance.

Binding run `36103484871` passed the same complete build/Core gates with exact P11 bound in the root release-state
owner at Review `NOT_RUN`.

## Candidate boundary

P11 is frozen at `6352accc7962fc188976fc1bcea5e081681d99c5`.

Any later semantic mutation creates another candidate identity and invalidates P11-specific Review applicability.
Later descendants may carry lifecycle/qualification evidence only.

This record establishes mechanical repair qualification. It is not independent semantic Review PASS, stakeholder
ratification, public-fallback publication, recovery establishment, accepted-current cutover, PR merge, or Protocol 7
mutation.
