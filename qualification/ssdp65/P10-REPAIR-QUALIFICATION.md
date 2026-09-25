---
kind: ssdp65-p10-repair-qualification
status: repair-complete-candidate-frozen
protocol_version: 6.4.0
target_protocol_version: 6.5.0
p0: 55c085261eb827e3047637d045a8e6917ea6b962
failed_p9: fb347272c70b6225743fdc99e9bec8b4197aad49
p10: 275b23bfa45cc72145d2079c8d945a6ff5a5c216
exact_p10_pr_run: 36098785911
binding_descendant: 82949a0c8325fce602c39fb3dfdab56352d94b73
binding_run: 36098950938
date: 2026-09-25
d3_reopened: false
serious_challenge: none
historical_preservation_review: qualification/ssdp65/HISTORICAL-CAPABILITY-PRESERVATION-REVIEW-2026-09-25-P9.md
---

# Protocol 6.5 P10 Repair Qualification

## Scope and identity

This record qualifies the bounded D4 repair ordered by the fresh independent P9 Review.

- accepted control P0: `55c085261eb827e3047637d045a8e6917ea6b962`
- immutable failed P9: `fb347272c70b6225743fdc99e9bec8b4197aad49`
- immutable replacement P10: `275b23bfa45cc72145d2079c8d945a6ff5a5c216`
- exact-P10 normal workflow: `36098785911`
- later binding descendant: `82949a0c8325fce602c39fb3dfdab56352d94b73`
- binding workflow: `36098950938`

Accepted P65 D3 was not reopened and no Serious Challenge was raised.

## B65-P9-1 closure

P9 conflated two histories:

1. a lineage that genuinely predates introduction of root `PROTOCOL-RELEASE-STATE.yaml`;
2. a lineage that was already governed and later deleted that sole owner.

P10 repairs the existing production ancestry classifier without introducing a second authority.

The resolver now has distinct outcomes for:

- valid parsed governed state;
- explicit owner-path absence;
- malformed/unreadable state that already fails validation.

For an absent HEAD or parent boundary, P10 performs a bounded ancestry-history query for the exact owner path. It treats the lineage as genuinely pre-owner only when no ancestor commit contains a parseable owner state. If the lineage previously contained the owner, current absence is rejected as governed owner deletion/reintroduction.

The ancestry-history query is existential only. It does not select a predecessor, does not use timestamp order, branch name, default/latest ref, sibling order, or traversal-stack order, and therefore does not reintroduce B65-P8-1.

## Fresh real-owner topology evidence

Exact P10 includes real temporary-Git production-resolver cases for:

- governed owner -> sibling deletion -> owner-restoring merge: reject;
- both merge-parent orders: reject;
- both relevant parent timestamp orderings: reject;
- multiple commits while the owner remains absent: reject;
- same-lineage delete -> committed reintroduction: reject;
- long genuinely pre-owner lineage + governed feature merge: pass;
- all prior P9 owner-present linear/evidence-only/divergent/equivalent/synthetic-PR controls remain active.

The later binding descendant adds evidence-only tests for the new explicit HEAD-missing path:

- working-tree first introduction from genuinely pre-owner HEAD: pass;
- working-tree reintroduction after governed deletion: reject.

These later tests do not mutate P10 production semantics.

## Mechanical evidence

Exact-P10 run `36098785911` passed:

- repository release-state validation;
- PEM validation;
- complete protocol regression;
- canonical skill-package build;
- independent package validation;
- committed distribution parity;
- whitespace validation;
- Protocol 6.5 snapshot parity;
- complete Orchestrator Core acceptance.

Binding run `36098950938` passed the same complete build/Core gates with P10 bound in root release state and the two additional evidence-only working-tree controls present.

## Historical preservation

The prior historical-capability review found no additional doctrine loss beyond B65-P9-1.

P10 changes only `source/release_state.py` production semantics relative to P9. The universal kernel, current canonical prompts, generated 6.5 prompts, historical supported profile/prompt resources, PEM doctrine, D1-D4 doctrine, Lossless Representation/progressive disclosure, Protocol 6.4 formal-definition doctrine, and Protocol 7 D3/D4 design remain outside the semantic repair surface.

The active inherited historical regression modules remain exercised by full test discovery in both exact-P10 and binding runs.

## Candidate boundary

P10 is frozen at `275b23bfa45cc72145d2079c8d945a6ff5a5c216`.

Any later semantic mutation creates another candidate identity and invalidates P10-specific Review applicability. Later descendants may carry qualification/lifecycle evidence only.

This record establishes mechanical repair qualification. It is not independent semantic Review PASS, stakeholder ratification, public-fallback publication, recovery establishment, accepted-current cutover, PR merge, or Protocol 7 mutation.
