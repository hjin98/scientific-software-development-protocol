---
kind: ssdp65-p9-repair-qualification
status: repair-complete-candidate-frozen
protocol_version: 6.4.0
target_protocol_version: 6.5.0
p0: 55c085261eb827e3047637d045a8e6917ea6b962
failed_p8: ed782ccad73b43c9052ecc926177c36846b9328d
p9: fb347272c70b6225743fdc99e9bec8b4197aad49
exact_p9_pr_run: 36091484812
date: 2026-09-24
d3_reopened: false
serious_challenge: none
---

# Protocol 6.5 P9 Repair Qualification

## Scope and identity

This record qualifies the bounded D4 repair ordered by the fresh independent P8 Review.

- accepted control P0: `55c085261eb827e3047637d045a8e6917ea6b962`
- immutable failed P8: `ed782ccad73b43c9052ecc926177c36846b9328d`
- immutable replacement candidate P9: `fb347272c70b6225743fdc99e9bec8b4197aad49`
- exact-P9 normal PR qualification: run `36091484812`

Accepted P65 D3 was not reopened and no Serious Challenge was raised.

## B65-P8-1 closure — ancestry-boundary transition resolution

The existing `source/release_state.py` owner no longer uses global path-log ordering to select one alleged predecessor.

The production resolver now:

- compares an uncommitted root-state edit directly with committed HEAD state;
- for a committed state, inspects direct Git parent topology;
- traverses ancestry only through parents whose parsed root release state is semantically equal to the current state;
- stops at the first differing release-state snapshot on each lineage;
- validates the current state against every materially distinct predecessor boundary found;
- deduplicates equivalent parent-boundary states;
- ignores parent lineages that predate introduction of the root release-state owner.

This preserves the latest material transition across evidence-only descendants while preventing a later-dated sibling merge parent from substituting for another materially applicable predecessor.

## Fresh real-owner topology evidence

The exact P9 regression exercises the real resolver with temporary Git repositories:

- working-tree change versus HEAD;
- linear committed transition;
- evidence-only descendant after a transition;
- date-reordered divergent merge parents where one predecessor admits the current state and another exposes historical deletion;
- equivalent merge-parent lineages;
- synthetic PR merge with a base parent predating the root release-state owner.

The known P7/P8 transition, recovery-lineage, parser, semver, evidence-subject, historical-continuity, terminal-state, generated-parity, frozen-resource, and preservation suites remain active.

## Exact-P9 mechanical evidence

Normal PR workflow run `36091484812` on exact P9 passed both jobs completely:

- repository release-state validation;
- Project Engineering Memory validation;
- complete protocol regression, including the real Git topology holdouts;
- canonical package build;
- independent package validation;
- committed distribution parity;
- whitespace validation;
- packaged Protocol 6.5 snapshot parity;
- complete Orchestrator Core acceptance suite.

This is structural/executable qualification only. It is not independent semantic Review PASS.

## Candidate boundary

P9 is frozen at `fb347272c70b6225743fdc99e9bec8b4197aad49`.

This later lifecycle descendant binds P9 with Review `NOT_RUN`. Any material semantic mutation after P9 creates another candidate identity and invalidates P9-specific Review/qualification applicability.
