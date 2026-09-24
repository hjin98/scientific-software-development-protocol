---
kind: ssdp65-p7-repair-qualification
status: repair-complete-candidate-frozen
protocol_version: 6.4.0
target_protocol_version: 6.5.0
p0: 55c085261eb827e3047637d045a8e6917ea6b962
failed_p6: dd06da8136416e67644586c44880b466f982b8ff
p7: 133c747a1f9ab4372c9e1af7a7e9666316dc892b
exact_p7_pr_run: 36058860629
date: 2026-09-24
d3_reopened: false
serious_challenge: none
---

# Protocol 6.5 P7 Repair Qualification

## Scope and identity

This record qualifies the bounded D4 repair ordered by the fresh independent P6 Review.

- accepted control P0: `55c085261eb827e3047637d045a8e6917ea6b962`
- immutable failed P6: `dd06da8136416e67644586c44880b466f982b8ff`
- replacement immutable candidate P7: `133c747a1f9ab4372c9e1af7a7e9666316dc892b`
- exact-P7 normal PR qualification: run `36058860629`
- superseded implementation attempt `91a3ecb5e64d609f72dc8c03194b22e299ef88bd` failed protocol regression because one rewired test shadowed the imported release-state module; P7 contains only the corrective test binding on top of that repair.

P1-P6 remain immutable historical Review subjects. Accepted P65 D3 was not reopened and no Serious Challenge was raised.

## B65-P6-1 closure — one root-state parser semantics

All mechanical consumers of root `PROTOCOL-RELEASE-STATE.yaml` in the repository Python test surface now route through the existing `source/release_state.py::load()` owner path.

A complete exact-P7 Python census found no remaining ordinary `yaml.safe_load` of the root release-state file. Unrelated YAML parsing remains unchanged.

The repair adds no wrapper, parser service, state mirror, registry, or compatibility path.

Fresh structural holdouts using the exact strict-loader construction confirmed:

- ordinary mapping aliases remain legal;
- duplicate keys inside an anchored mapping reject recursively;
- YAML merge-key syntax fails closed under the strict owner loader rather than being normalized by a different parser.

The existing root duplicate-key matrix and Review/ratification front-matter matrix remain applicable and passed in exact-P7 repository regression.

## B65-P6-2 closure — historical ordering and canonical version identity

The existing release-state validator now uses one canonical ASCII three-component numeric version grammar:

`0|[1-9][0-9]*` for each component.

Consequences:

- leading-zero spellings such as `06.5.0`, `6.05.0`, and `6.5.00` reject;
- Unicode decimal-digit spellings reject;
- multi-digit components such as `6.10.0` remain valid and compare numerically;
- candidate/history collision uses numeric tuple identity after canonical validation;
- every historical version must be strictly older than `accepted_current.version`;
- accepted-current equality remains excluded from history;
- the existing complete terminal `accepted_current == candidate` predicate remains unchanged;
- future patch/minor/major successors remain generic.

A real-ref holdout places P6 `dd06da8136416e67644586c44880b466f982b8ff` and binding descendant `758490c11f90b587c7dfaadddab958751f2881c9`, both declaring Protocol 6.5, into `historical["6.5.0"]` while accepted-current is still 6.4 and candidate is 6.6. Exact-P7 validation rejects that state because historical 6.5 is not older than accepted-current 6.4 while the refs themselves remain version-correct.

## Exact-P7 mechanical evidence

Normal PR workflow run `36058860629` on exact P7 passed:

- repository release-state validation;
- Project Engineering Memory validation;
- complete protocol regression;
- canonical package build;
- independent package validation;
- committed distribution parity;
- whitespace validation;
- packaged Protocol 6.5 snapshot parity;
- complete Orchestrator Core acceptance suite.

This establishes only the executable/structural properties those oracles discriminate. It is not independent semantic Review PASS.

## Applicability and preservation

The repair changes only:

- existing D4 release-state version/history validation;
- existing tests that consume the root release-state owner;
- focused lifecycle qualification.

No D1, D2, accepted P65 D3, formal-definition doctrine, PEM schema, generated package/profile semantics, frozen prior-version resources, or Protocol 7 D3/D4 authority is changed.

The exact P0/P6 frozen-resource and current-representation evidence remains reusable only where unchanged-surface applicability is independently re-established by the next Review.

## Candidate boundary

P7 is frozen at `133c747a1f9ab4372c9e1af7a7e9666316dc892b`.

P7 itself still contains the prior P6 NO-PASS lifecycle state and does not self-name as active candidate. A later descendant binds P7 in `PROTOCOL-RELEASE-STATE.yaml`.

Fresh independent Review begins `NOT_RUN`; stakeholder ratification remains `NOT_REQUESTED`; public fallback and recovery remain `UNAVAILABLE`; accepted-current remains Protocol 6.4.

Any material semantic mutation after P7 creates another candidate identity and invalidates P7-specific Review/qualification applicability.
