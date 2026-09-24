---
kind: ssdp65-p5-repair-qualification
status: repair-complete-candidate-frozen
protocol_version: 6.4.0
target_protocol_version: 6.5.0
p0: 55c085261eb827e3047637d045a8e6917ea6b962
failed_p1: b565e28aeacea002cefe27e6b9594fe99d653c0a
failed_p2: e8edb353e172aef933ed5e58eeabe897d0cc98d1
failed_p3: 89ccc71a7b0e9458a3e77306be2a773d4059f0f2
failed_p4: 43ff4273fbdaf46b9677cffdb091b741ce754a7d
p5: d2d672a3e814438fb618f901137f88c8698a205d
exact_p5_pr_run: 36047926253
date: 2026-09-24
d3_reopened: false
serious_challenge: none
---

# Protocol 6.5 P5 Repair Qualification

## 1. Scope and identity

This record qualifies the bounded D4 repair ordered by the fresh independent P4 Review.

- accepted control P0: 55c085261eb827e3047637d045a8e6917ea6b962
- immutable failed P1: b565e28aeacea002cefe27e6b9594fe99d653c0a
- immutable failed P2: e8edb353e172aef933ed5e58eeabe897d0cc98d1
- immutable failed P3: 89ccc71a7b0e9458a3e77306be2a773d4059f0f2
- immutable failed P4: 43ff4273fbdaf46b9677cffdb091b741ce754a7d
- replacement immutable candidate P5: d2d672a3e814438fb618f901137f88c8698a205d
- exact-P5 normal PR qualification: run 36047926253

P1-P4 remain immutable failed Review subjects. No prior Review verdict transfers to P5. The accepted P65 D3 design was not reopened and no Serious Challenge was raised.

## 2. B65-P4-1 closure

The repair alters only the existing release-state evidence parser/binder plus focused tests.

Evidence front matter now uses a SafeLoader subclass that rejects duplicate mapping keys before semantic binding. This closes duplicate candidate_ref, duplicate semantic_ref, and duplicate status last-key-wins ambiguity.

Explicit candidate subject fields are detected by key presence. If candidate_ref or semantic_ref is present, each must be a nonempty lowercase 40-hex candidate commit; both must agree when present together. Empty, null, or malformed explicit fields reject and cannot be rescued by legacy pN metadata.

Legacy compatibility remains generic: only when explicit subject keys are absent, the highest present numeric pN generation is the candidate subject. An invalid or empty highest generation rejects rather than silently falling back to a lower historical candidate. No P1-P5 special case was added.

Arbitrary Review and stakeholder-ratification prose remains outside machine semantic judgment.

## 3. Focused falsification

Focused tests now cover both Review and terminal ratification for:

- exact candidate/disposition;
- wrong candidate;
- disposition mismatch;
- explicit-vs-historical conflict;
- conflicting explicit subject fields;
- duplicate candidate_ref;
- duplicate semantic_ref;
- duplicate status;
- empty/null/malformed explicit subject with matching historical pN;
- lower/higher pN coexistence;
- empty higher-generation pN;
- future p5 generation;
- wrong repository;
- unsafe path;
- missing commit/path.

The new tests exercise the real shared parser/binder rather than a separate proxy predicate.

## 4. Exact-P5 mechanical evidence

Normal repository PR workflow run 36047926253 evaluated exact P5 and passed both jobs completely:

- release-state validation;
- Project Engineering Memory validation;
- complete inherited protocol regression;
- canonical skill package build;
- independent package validation;
- committed distribution semantic parity;
- whitespace;
- packaged Protocol 6.5 snapshot parity;
- Orchestrator Core acceptance.

This establishes only the executable/structural properties those oracles discriminate. It is not independent semantic Review PASS.

## 5. Preservation and applicability

The changed surface does not alter D1, D2, accepted D3, formal-definition doctrine, current evidence doctrine, package/profile semantics, PEM schema, or Protocol 7 D3/D4.

P4-specific whole-candidate Review remains historical. Still-applicable unchanged-surface evidence may be reused only after identity/applicability inspection, including the P4 current-representation convergence result and frozen historical resource checks.

## 6. Candidate boundary

P5 is frozen at d2d672a3e814438fb618f901137f88c8698a205d.

P5 itself records the completed P4 NO-PASS lifecycle state and does not self-name as current candidate. This later descendant binds P5 in PROTOCOL-RELEASE-STATE.yaml.

Fresh independent Review begins NOT_RUN; stakeholder ratification remains NOT_REQUESTED; public fallback and recovery remain UNAVAILABLE; accepted-current remains Protocol 6.4.

Any material semantic mutation after P5 creates another candidate identity and invalidates P5-specific Review/qualification applicability.
