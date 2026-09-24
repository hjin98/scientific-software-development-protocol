---
kind: independent-review-handoff
protocol_under_review: 6.5.0
status: ready
accepted_control_p0: 55c085261eb827e3047637d045a8e6917ea6b962
immutable_candidate_p1: b565e28aeacea002cefe27e6b9594fe99d653c0a
candidate_branch: ssdp-6.5-frontier-model-re-evaluation
draft_pr: 33
p1_mechanical_qualification_run: 35985871148
authoring_context_verdict: none
stakeholder_ratification: NOT_REQUESTED
---

# Independent Review Handoff — Protocol 6.5

## 1. Review target and independence contract

Perform a **fresh independent assembled-candidate Review** of immutable Protocol 6.5 candidate:

```text
P1 = b565e28aeacea002cefe27e6b9594fe99d653c0a
```

against accepted Protocol 6.4 control:

```text
P0 = 55c085261eb827e3047637d045a8e6917ea6b962
```

Review P1 itself, not the mutable branch head, PR diff, implementation summary, prior diagnostic verdicts, CI status, or author conclusions.

The reviewer/context MUST NOT have authored P1. Reconstruct applicable authority independently. Prior Opus 5.5 diagnostic, GPT-5.6 Sol historical Review corpus, cross-model adjudication, workplans, preservation map, CI and this handoff are evidence to challenge, not conclusions to inherit.

Different model-family evidence is useful corroboration but does not replace authorship/conclusion independence.

## 2. Governing materials to reconstruct

At minimum read/reconstruct from P1:

1. current D1-D4 role owners and universal kernel;
2. `workplans/active/SSDP-6.5-FRONTIER-MODEL-RE-EVALUATION.md`;
3. `workplans/active/SSDP-6.5-D3-D4-IMPLEMENTATION-HANDOFF.md`;
4. `qualification/ssdp65/PHASE-IV-V-DESIGN-CLOSURE.md`;
5. `qualification/ssdp65/BENCHMARK-AND-EVALUATION-DESIGN.md`;
6. `qualification/ssdp65/PROTOCOL-6.4-TO-6.5-PRESERVATION-MAP.md`;
7. `qualification/ssdp65/P1-PREFREEZE-READINESS.md`;
8. `PROTOCOL-RELEASE-STATE.yaml` from the binding descendant only for mutable lifecycle state; candidate semantics remain P1;
9. self-hosted `PROJECT-ENGINEERING-MEMORY.md` and `history/SEMANTIC_EVOLUTION.md`;
10. accepted Protocol 6.4 consolidated workplan and final Review evidence as preservation baseline.

Do not use repository default/latest as a semantic-version oracle.

## 3. Evidence already available, with bounded claims

### Exact P1 mechanical qualification

Draft PR #33 evaluated exact P1 in normal repository workflow run `35985871148` after the branch-only implementation workflow had been removed.

Observed:
- build job PASS;
- release-state validation PASS;
- PEM validation PASS;
- inherited protocol regression PASS;
- canonical package build + independent validation PASS;
- committed distribution parity PASS;
- whitespace PASS;
- packaged 6.5 snapshot parity PASS;
- Orchestrator Core PASS.

This establishes the properties those executable oracles discriminate. It does **not** establish arbitrary prose semantic adequacy or engineering-outcome superiority.

### Earlier implementation evidence

Run `35985539212` is the final full branch implementation run immediately before freeze and also passed all implementation gates. Earlier failed runs are retained as development evidence and must not be rewritten into passes.

## 4. Mandatory Phase VII semantic falsification

Use fresh reasoning rather than the author's obligation matrix as your search boundary.

### 4.1 Admitted defect families

Attempt to falsify closure of all four:

- **DF-1** release-state/version lifecycle ownership;
- **DF-2** qualification/Review epistemology;
- **DF-3** meta-control semantics/governance;
- **DF-4** representation/schema/convergence self-application.

For each, inspect actual owners and actual assembled behavior. A local test that passes its own model is not enough.

### 4.2 Local-compliance/global-failure search

Construct plausible trajectories where every obvious local rule appears satisfied while a protected global invariant fails. Include at least:

- conflicting or stale lifecycle projections;
- exact-wording/proxy oracle that passes while canonical meaning is defective;
- false Serious Challenge or missed Serious Challenge;
- semantic mutation disguised as clarification;
- accepted PEM/history/derived view acting as hidden authority;
- lower-layer implementation strengthening or narrowing upstream meaning;
- generated/profile/package consistency masking wrong canonical semantics.

Record either surviving counterexamples or the exact falsification attempt and why none survived.

### 4.3 Out-of-matrix abstraction-adequacy pass

Temporarily ignore the author workplan, preservation matrix and known defect list. Reconstruct global invariants from current owners and search for at least one material defect class not represented by the author's matrix. The requirement is to attempt the search, not to invent a finding.

Explicitly challenge the **qualification method itself**: identify any claim that exceeds what its oracle/method can discriminate.

### 4.4 Fresh post-freeze semantic mutation/counterexample set

Author a fresh set after seeing P1, independent of P1 authoring. Arbitrary prose semantic mutants are judged by semantic Review; machine-readable/state/schema/generated mutants use executable oracles. Include meaning-preserving paraphrase controls where wording is not itself a contract.

Do not optimize for a mutation-detection percentage by inventing a prose theorem prover or exact-string pins.

## 5. P65-1..P65-6 ablation obligations

For each principle, remove/weaken only that principle conceptually or in an isolated test candidate and ask whether its motivating counterexample reappears.

- **P65-1 Self-application:** can SSDP exempt its own qualification/release artifacts and thereby admit proxy/self-approval failure?
- **P65-2 State/semantics separation:** can immutable versioned semantics become stale after lifecycle transition while package parity stays green?
- **P65-3 Evidence-claim congruence:** can a fixture/phrase oracle pass while the claimed canonical semantic property is false?
- **P65-4 Review abstraction adequacy:** can the author matrix pass while an unmodeled global invariant fails?
- **P65-5 Minimal meta-governance:** can materiality/Challenge/independence/ratification/accepted-PEM ambiguity change disposition?
- **P65-6 Integrated current representation:** can amendment replay, stale labels or duplicated current truth create conflicting owners or unnecessary hot context?

An ablation PASS means the principle is causally useful on its motivating case or a holdout; otherwise recommend removal/compression.

## 6. Targeted P0/P1 behavior comparison

Because 6.5 is an intelligence-uplift release, execute matched P0/P1 trials on at least four difficult tasks spanning:

1. lifecycle/current-state drift;
2. proxy/oracle adequacy;
3. authority/Challenge routing;
4. mature-system simplification/review convergence.

Use identical task, repository snapshot, model, tools and budget per pair. Record exact model identifier/date and trajectory evidence. Replicate only stochastic/ambiguous cases where another realization can change the bounded conclusion.

Use GPT-5.6 Sol as historical/control model when available. Opus 5.5/frontier paired trials are valuable when resource permits; if unavailable, state that limitation and make no quantitative cross-frontier performance claim.

Reserve at least one holdout/novel task family not used to design P1. Follow the preregistration and its dated benchmark-defect amendment; do not move criteria because P1 performs poorly.

## 7. Simplicity and preservation falsification

Independently verify rather than merely trust reported counts:

- P0/P1 always-loaded kernel/context words;
- duplicated generic rule/value copies;
- release lifecycle/state projections;
- exact-string semantic pins;
- current-owner/schema duplications;
- frozen 5.16-6.4 profile/resource identities;
- full 6.4 -> 6.5 preservation/supersession map, including P64-A..P64-O, QF64 semantic capabilities and F64 falsification capabilities.

A smaller representation is not automatically better; any compression that loses a validated protection is a blocker.

## 8. Review disposition

### Serious Challenge

Raise **SERIOUS CHALLENGE** first only if accepted P0/upstream authority itself has a concrete materially consequential contradiction, ambiguity, inadequacy, incompatibility or unrealizability. Do not use Challenge for ordinary P1 defects.

### Blocking finding

A genuine P1 blocker must identify:

```text
finding
-> exact owner
-> violated invariant
-> counterexample/evidence
-> consequence
-> smallest owning-layer repair
-> affected qualification to rerun
```

Prefer removal/rewiring/owner correction over patches, wrappers, duplicate state or special-case machinery.

### PASS

PASS only if:
- no genuine blocking semantic/preservation/qualification defect survives;
- required Phase VII checks are executed rather than assumed;
- P1 preservation is lossless or explicitly justified where superseded;
- P0/P1 comparison satisfies the preregistered acceptance rule;
- limitations are stated honestly.

A Review PASS means **technical eligibility only**. Do not ratify Protocol 6.5, publish its public fallback, establish recovery, change accepted-current, merge the draft PR, or update Protocol 7 inheritance. Those are later lifecycle steps.

## 9. Required outputs

Write durable evidence under `qualification/ssdp65/`:

1. Phase VII qualification/results record with exact P0/P1/model/tool identities and limitations;
2. fresh mutation/counterexample set and outcomes;
3. P65-1..P65-6 ablation record;
4. targeted P0/P1 behavior-comparison record;
5. independent assembled-candidate Review with PASS / NO-PASS and precise blockers if any.

If blockers exist, reopen the active 6.5 workplan with exact owning-layer repair instructions and do not mutate P1; repairs create a new candidate identity.

If no blocker remains, leave `PROTOCOL-RELEASE-STATE.yaml` candidate Review state ready for a later binding descendant to publish the Review evidence. Do not self-ratify.

## 10. Known limitations carried into Review

- second contemporary frontier diagnostic was waived for this cycle due resource limits; do not claim two-frontier diagnostic replication;
- authoring context cannot serve as the independent final reviewer;
- downstream mdstats history HO3 was not available during the preregistration unless separately supplied now;
- mechanical CI cannot establish arbitrary prose semantics;
- branch head after this handoff is a lifecycle descendant, not P1.
