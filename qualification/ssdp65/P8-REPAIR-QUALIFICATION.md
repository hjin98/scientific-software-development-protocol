---
kind: ssdp65-p8-repair-qualification
status: repair-complete-candidate-frozen
protocol_version: 6.4.0
target_protocol_version: 6.5.0
p0: 55c085261eb827e3047637d045a8e6917ea6b962
failed_p7: 133c747a1f9ab4372c9e1af7a7e9666316dc892b
superseded_implementation_attempt: dd9eb66548112bbb027cd70ad1f697634db13bb0
p8: ed782ccad73b43c9052ecc926177c36846b9328d
exact_p8_pr_run: 36067942018
date: 2026-09-24
d3_reopened: false
serious_challenge: none
---

# Protocol 6.5 P8 Repair Qualification

## Scope and identity

This record qualifies the bounded D4 repair ordered by the fresh independent P7 Review.

- accepted control P0: `55c085261eb827e3047637d045a8e6917ea6b962`
- immutable failed P7: `133c747a1f9ab4372c9e1af7a7e9666316dc892b`
- superseded implementation attempt: `dd9eb66548112bbb027cd70ad1f697634db13bb0`
- immutable replacement candidate P8: `ed782ccad73b43c9052ecc926177c36846b9328d`
- exact-P8 normal PR qualification: run `36067942018`

P1-P7 remain immutable historical Review subjects. Accepted P65 D3 was not reopened and no Serious Challenge was raised.

## B65-P7-1 closure — transition and recovery lineage

The existing `source/release_state.py` owner now validates both snapshot coherence and the temporal relation between governed release-state snapshots.

Transition closure:

- accepted-current identity cannot be rewritten while the version is unchanged;
- existing historical mappings cannot be deleted or rewritten;
- history cannot grow without accepted-current advancement;
- accepted-current advancement must promote the immediately previous completed candidate;
- the previous accepted-current mapping must move unchanged into historical;
- unrelated historical insertion during cutover rejects.

Recovery-lineage closure:

- recovery must descend from the semantic candidate;
- Review evidence must descend from the semantic candidate;
- ratification evidence must follow Review evidence;
- recovery must follow the Review/ratification lineage;
- the state publishing the recovery mapping must descend from the recovery target;
- the recovery target's own root release state must already contain the exact candidate, PASS evidence, RATIFIED evidence, and exact public fallback while recovery is still UNAVAILABLE.

The transition baseline is resolved from Git history of the sole root `PROTOCOL-RELEASE-STATE.yaml`; no second state representation or transition registry was introduced.

## Fresh focused holdouts

The exact P8 regression includes:

- real immutable P6 used as an invalid stale recovery for P7;
- same-version accepted-current identity rewrite;
- historical deletion;
- historical rewrite;
- historical insertion without cutover;
- accepted-current cutover missing the prior accepted mapping;
- accepted-current cutover with a mutated prior accepted mapping;
- accepted-current cutover whose accepted recovery differs from the prior candidate;
- incomplete prior candidate closure;
- a positive complete pre-mapping recovery snapshot.

Existing parser, duplicate-key, canonical-version, history-order, candidate-succession, evidence-subject, terminal-equality, generated-parity, and preservation suites remain active.

## Exact-P8 mechanical evidence

Normal PR workflow run `36067942018` on exact P8 passed both jobs completely:

- repository release-state validation;
- Project Engineering Memory validation;
- complete protocol regression;
- canonical package build;
- independent package validation;
- committed distribution parity;
- whitespace validation;
- packaged Protocol 6.5 snapshot parity;
- complete Orchestrator Core acceptance suite.

This is structural/executable qualification only. It is not independent semantic Review PASS.

## Candidate boundary

P8 is frozen at `ed782ccad73b43c9052ecc926177c36846b9328d`.

This later descendant binds P8 in the sole mutable release-state owner with Review `NOT_RUN`, ratification `NOT_REQUESTED`, public fallback `UNAVAILABLE`, recovery `UNAVAILABLE`, and accepted-current Protocol 6.4.

Any material semantic mutation after P8 creates another candidate identity and invalidates P8-specific Review/qualification applicability.
