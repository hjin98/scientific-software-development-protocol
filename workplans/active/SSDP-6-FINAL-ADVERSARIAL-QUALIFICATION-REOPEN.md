---
kind: protocol-major-revision-review-reopen
workplan_id: SSDP-6-FINAL-ADVERSARIAL-QUALIFICATION-REOPEN
reopens_workplan: SSDP-6-RECURSIVE-ABSTRACTION-REALIZATION-SCIENTIFIC-SOFTWARE-PROTOCOL
protocol_version: 6.0.0
status: active
opened_date: 2026-09-09
reviewed_candidate_commit: f18f87c788162d048cd3292ad6712ec91f159bf4
review_verdict: no-pass
active_serious_challenge: none
blocking_owner: D4 acceptance / Protocol self-qualification
---

# SSDP 6 Final Adversarial Qualification — Review Reopen

## 1. Why this workplan is reopened

The current Protocol 6 implementation is conceptually coherent and the previously identified Protocol 5 inheritance/consolidation defects are repaired. Canonical `source/`, generated distributions, the Protocol 6 profile/snapshot, immutable Protocol 5.16 recovery, repository regression tests, package/parity checks, and Orchestrator Core acceptance are green on reviewed candidate `f18f87c788162d048cd3292ad6712ec91f159bf4`.

Final Review nevertheless returns **NO-PASS** because one explicit parent-workplan release predicate is not evidenced as executed: the **new adversarial behavioral qualification**.

The parent transition workplan requires Protocol 6 to pass adversarial behavioral scenarios rather than only static/source-structure checks, and its atomic closeout requires both repository tests **and** the new behavioral qualification before final release acceptance. The current `qualification/ssdp6/SCENARIOS.md` defines 69 decision-oriented scenarios and explicitly states that static repository tests establish only protocol/source structure. Current hosted CI runs repository unit tests, package build/validation/parity, snapshot parity, Orchestrator Core acceptance, and whitespace checks, but it does not execute those 69 scenarios through an actual Protocol 6 role/workflow decision surface.

Therefore the previous archived closeout is insufficient as final acceptance evidence even though its underlying Protocol 6 semantics remain current and no Serious Challenge is active.

This file reopens only the unresolved **qualification and final-acceptance surface**. It does **not** reactivate the archived transition authority as a parallel current control plane. Current Protocol 6 semantics remain owned by canonical `source/`; the archived parent and its two accepted amendments remain historical transition evidence.

## 2. Governing invariants

1. **Behavior, not wording, is the oracle.** Qualification must establish the intended routing, authority ownership, challenge/status behavior, anti-counterfeit rules, proportionality, bounded invalidation, simplification, and Protocol 5.16 isolation represented by the scenario set. Equivalent wording is admissible.
2. **Static/source tests are insufficient for this gate.** They remain necessary supporting evidence but do not substitute for decision-level behavioral qualification.
3. **Do not manufacture a pass.** Do not weaken a scenario expectation, change a required outcome, skip a failing scenario, or reinterpret failure merely to match current implementation unless independent review establishes that the scenario itself contradicts current accepted Protocol 6 authority.
4. **Use the real Protocol 6 semantic owner.** Qualification must exercise the actual current role/workflow skill behavior that would govern a user request, not a reimplementation of the expected decision in the test harness.
5. **Preserve historical isolation.** Protocol 5.16 scenarios must resolve through the immutable 5.16 source/profile path; current Protocol 6 scenarios must use Protocol 6 source/profile semantics.
6. **Prefer minimum machinery.** Use an existing capable harness/evaluation route where practical. Do not create a permanent qualification framework, registry, compatibility layer, or new lifecycle stage merely to record this evidence.

## 3. Required repair and evidence

### A. Execute the complete current SSDP 6 behavioral qualification set

Run **all 69 scenarios** in `qualification/ssdp6/SCENARIOS.md` against the current candidate through an actual Protocol 6 role/workflow decision surface capable of reading the current skills and required references.

For each scenario preserve enough inspectable evidence to establish:

- scenario number/title;
- candidate commit SHA;
- Protocol/profile identity actually selected;
- harness/model/agent configuration used for the run;
- scenario input or equivalent bounded prompt/context;
- expected governed decision/result class;
- observed decision/result class;
- PASS/FAIL and concise semantic rationale;
- raw output or a durable pointer to raw output when needed to inspect a failure.

The harness need not reproduce exact phrasing. It must allow an independent reviewer to determine whether the actual Protocol 6 behavior satisfied the governed scenario.

If the required skill/workflow decision surface cannot be executed in the available environment, record the qualification as **unavailable/blocking** rather than proxy-passing it with static text checks.

### B. Repair semantic failures at their canonical owner

For any failed scenario:

1. identify the earliest owning Protocol 6 semantic surface (`source/roles`, canonical shared reference, canonical workflow prompt/profile source, or Orchestrator Core when routing implementation itself is defective);
2. determine whether the failure is ordinary realization nonconformance or a genuine Serious Challenge to accepted Protocol 6 authority;
3. for ordinary nonconformance, alter/remove/rewire the canonical owner with the minimum justified change; do not add a wrapper, compatibility runtime, duplicate policy, registry, or special-case layer when the existing owner can be corrected directly;
4. if accepted authority itself appears materially false, contradictory, ambiguous, inadequate, or unrealizable, stop normal closure and raise the Serious Challenge under Protocol 6 rather than editing the oracle to fit the candidate;
5. regenerate all affected derived distributions/snapshots after canonical-source mutation;
6. rerun the failed scenario family and then the complete 69-scenario qualification set on the final candidate.

### C. Re-establish assembled implementation acceptance after any repair

After the behavioral qualification is green on the final candidate, run the complete existing hosted acceptance surface on the same candidate:

- repository protocol regression tests;
- canonical skill package build;
- independent package validation;
- committed distribution parity;
- Protocol 6 packaged snapshot parity;
- full Orchestrator Core acceptance suite;
- immutable Protocol 5.16 recovery/profile tests;
- `git diff --check` or the repository-equivalent whitespace check.

A required check that does not execute remains blocking.

### D. Fresh final Review / Challenge Pass

Perform a fresh independent final Review after the qualification evidence and any resulting repairs are complete. The reviewer must:

- inspect the behavioral-qualification result set rather than accepting a summary count alone;
- inspect any failed-then-repaired scenario families and their canonical-owner changes;
- reconcile the final candidate against the parent workplan, Revision 1, Revision 2, and current canonical Protocol 6 authority;
- confirm no Protocol 5 dual-current control plane was reintroduced;
- confirm no qualification-only wrapper or duplicated authority was introduced;
- run the bounded Protocol 6 Challenge Pass;
- return Pass only when no genuine blocker or active Serious Challenge remains.

## 4. Acceptance criteria for re-closeout

This reopen closes only when all of the following are true on one final candidate SHA:

- all 69 current SSDP 6 behavioral qualification scenarios have actually executed through a real Protocol 6 role/workflow decision surface and pass semantically;
- any qualification-discovered defects are repaired at their canonical owner without weakening accepted semantics or adding unjustified machinery;
- canonical source and every committed/generated derivative are coherent;
- the existing repository and Orchestrator Core acceptance surfaces execute and pass after the last material repair;
- immutable Protocol 5.16 recovery remains unchanged and independently testable;
- a fresh independent final Review / Challenge Pass finds no genuine blocker and no active Serious Challenge;
- this active reopen workplan is then archived as completed with the final candidate SHA and evidence summary.

## 5. Explicit non-goals

- Do not redesign the D1-D4 recursive abstraction-realization theory without new Serious-Challenge evidence.
- Do not reopen Revision 1 or Revision 2 merely because this acceptance evidence was missing.
- Do not create a fifth authority-bearing role, new universal claim/evidence database, permanent qualification registry, or parallel Protocol 5 compatibility control plane.
- Do not require production-scale scientific workloads when a bounded decision scenario establishes the protocol behavior.
- Do not require exact wording or model determinism where the governed semantic decision is correct.
- Do not merge the SSDP 6 transition solely because repository/Core CI is green while this behavioral qualification remains unexecuted.

## 6. Review disposition

```text
SERIOUS CHALLENGE: NONE
FINAL REVIEW: NO-PASS
BLOCKER: REQUIRED SSDP 6 ADVERSARIAL BEHAVIORAL QUALIFICATION HAS NOT BEEN SHOWN TO EXECUTE AND PASS
EARLIEST OWNER: D4 acceptance / Protocol self-qualification
REOPEN SCOPE: behavioral qualification -> any discovered canonical-owner repairs -> assembled acceptance -> fresh final Review
```
