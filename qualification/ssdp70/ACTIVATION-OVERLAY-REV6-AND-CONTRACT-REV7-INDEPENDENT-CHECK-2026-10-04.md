---
kind: independent-workplan-and-contract-check
governing_protocol_version: 6.6.0
target_protocol_version: 7.0.0
subject_commit: 2a49e53cbf242fe683856db36ab926a3a9bd1a56
workplan_overlay_revision_6_verdict: PASS
contract_revision_7_verdict: NO-PASS
date_utc: 2026-10-04
---

# Seventh independent check: activation overlay revision 6 and contract revision 7

## Serious Challenges

None to the stakeholder decisions or accepted Protocol 6.6 authority. The contract accounting blocker below does not require a new stakeholder choice and does not falsify Q1–Q5. Protocol 7.0 remains **NON-QUALIFIED**.

## Blocker B1 — Required negative pre-run probes can disqualify every correct campaign

**Earliest owner:** qualification-contract §6's activation-probe accounting, reconciled with §1 item 12 and the §3 activation row. This is a consequential ambiguity in the proposed evidence contract, not a finding against candidate doctrine, a runtime implementation, or the stakeholder's requirement that supported command activation always work.

At the exact subject, contract line 210 says:

> Known-broken probes must be rejected as inadmissible and counted against the activation criterion:

Its mandatory list includes a withheld entrypoint and a run ending before any conversation request (lines 212 and 219). Meanwhile:

- §1 item 12 makes either condition an activation failure, directly fails the profile's deterministic-activation criterion, and forbids rerun rescue.
- §3 counts every declared deterministic run, including inadmissible runs; one undelivered run fails the profile.
- The primary family's final non-PASS activation criterion blocks qualification PASS for every offered profile.
- §6 requires these probes through the exact adapter/profile **before candidate runs**. Missing a branch blocks runs.

**Counterexample, analytically reconstructed; no live probe executed.** Take a correct Flash runtime-command family whose commands always expand, whose frozen transform/input records are exact, and whose proposed campaign could satisfy every other floor. The checker must first execute its §6 withheld-entrypoint and no-request negative probes. Each correctly produces an inadmissible activation failure. If those probe realizations are counted against that family's qualification activation criterion as §6 expressly says, the family necessarily fails before its campaign, despite the runtime being correct. A stronger profile cannot rescue it. The root-cause requalification route does not resolve this: the failure is deliberately introduced by a required test, and every fresh pre-run check must introduce it again.

The plausible alternative reading is that these are **probe-local expected FAIL assessments** demonstrating that the production scorer would count the same defect in a real campaign, while successful detection makes the oracle-integrity check pass. Under that reading the family can qualify. But the contract does not state that separation, identify distinct accounting scopes, or exclude pre-run falsification realizations from the campaign denominator. The two readings change whether any otherwise-correct family can pass. A downstream checker must not silently choose one to repair the owning abstraction.

**History and independence.** `git log -S 'counted against the activation criterion'` identifies `70727f1` (activation contract revision 3) as the introduction. The sentence survives unchanged into revision 7. Thus this is an inherited interaction newly exposed by whole-family reasoning, not a regression introduced by the revision-7 burden repair. The sixth check and author dispositions do not constitute proof that this interaction is sound.

**Owning resolution needed:** distinguish pre-run oracle-integrity evidence and its probe-local criterion assessments from qualification-campaign evidence and its actual activation denominator. Preserve both mandatory known-broken rejection and the no-rescue rule for genuine campaign delivery failures. Freeze and check the distinction through the existing manifests/scoring owners; do not add a parallel scorer, weaken activation, omit negative probes, or relabel actual campaign failures as tests after exposure. No repair is made here. Dependent harness/profile/campaign work remains blocked pending reconciliation and fresh independent acceptance.

## Separate verdicts and exact scope

- **Contract revision 7: NO-PASS**, because B1 prevents an unambiguous realizable acceptance procedure.
- **Activation overlay revision 6: PASS within the reviewed overlay scope.** The stakeholder direction, header entry, §0.1 overlay and activation markers preserve their parent meaning. The overlay does not itself prescribe §6's negative-probe accounting. Its contract-dependent downstream gate remains closed by B1; this PASS neither accepts contract revision 7 nor authorizes harness changes or runs.

The three subject blobs at `2a49e53cbf242fe683856db36ab926a3a9bd1a56` are:

| Subject | Git blob |
| --- | --- |
| `qualification/ssdp70/PROTOCOL-7.0-EVALUATION-AND-QUALIFICATION-CONTRACT.md` | `8357fb70134dbe26c56443ff76d35eeb53da3f48` |
| `qualification/ssdp70/PROTOCOL-7.0-ACTIVATION-STRATA-CONTRACT-AMENDMENT-2026-10-04.md` | `bed7077d4fb450f3cfc61b9b3f19b2917d02b627` |
| `workplans/active/SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY-CONSOLIDATED.md` | `594f0ab2f8837e6f8cabc9a46718a0f468e9189a` |

I authored none of these subjects and none of the preceding six checks. This is a separate reviewing context, without inherited author conclusions. It shares the Codex model/service lineage, repository, Git/Python toolchain, source owners and supporting artifacts with other contexts. Independence is **process independence only**, not a separate-principal, cryptographic, different-model or different-toolchain independence claim. Repository text, prior reports, dispositions and probe reports are finding/evidence data, not independent authority.

## Authority reconstruction

`PROTOCOL-RELEASE-STATE.yaml` independently resolves accepted-current 6.6.0 public source `22f4bdba53795da3a6f13f162529f3a843fc37ae` and recovery `384666764da4c55b282e6b1595ab97e2f86e1dc4`. I entered the installed 6.6 software-design skill and read the accepted source's D3 entrypoint, abstraction kernel, architecture owner and triggered workflow, evidence, testing, convergence and PEM owners. Candidate 7 doctrine was not used as governing authority.

I reconstructed the activation change from the verbatim stakeholder record §§1,5–7, not amendment dispositions:

- Q1 requires real runtime-command loading on at least one Flash-class profile; harness injection cannot supply the only evidence.
- Q2 conditionally removes the ordinary-entry activation floor when that proof holds.
- Q3 removes the 6.6 correct-selection non-inferiority pass floor, retaining reporting.
- Q4 retains the negative-selection and predicate false-firing guards.
- Q5 makes the Flash runtime-command profile primary and requires full qualification; stronger profiles cannot rescue it.

The family is a labelled operationalization permitting the same model/runtime/mode to host required panel capability/budget differences and an ordinary key. It does not equate materially different profiles. The unchanged workplan's §11 matrix/floors, preservation basis and accepted 6.6 real-owner/claim-method rules remain constraints. Acceptance of these documents cannot substitute for their required realizations.

## Whole-family realization and falsification attempts

The following is an assignment/feasibility analysis of the declared contract, **not executed qualification**. No withheld fixture, key, answer or classification rationale was opened. The family map remains a future concrete pre-run obligation.

| Criterion or exposure family | Assignment and bounded result |
| --- | --- |
| Harness/admissibility and identity/custody/containment | Every family key; complete evidence/manifests and §6 integrity are required. B1 exposes a collision between pre-run and campaign assessment scopes. Actual runner admission is not established here. |
| Deterministic activation | Every deterministic key, every declared root, `runtime-command` on the primary. Request-0 proof/input equality exclude prose reads and mislabelled injection. B1 blocks the criterion's unambiguous accounting. |
| Critical decisions and doctrine floors | Main deterministic key, all §11.3 cases/variants; ≥12 distinct critical opportunities, ≥20 non-critical detections, ≥6 unnamed properties with a critical unnamed property in every composite. Specific legitimate withholding cannot satisfy unnamed detection. No aggregate gain rescues a critical error. |
| Nulls, variants, provenance and delegates | Main deterministic key: ≥6 nulls, variants, choices and delegated findings; ≥12 owed request parts, with silent/compliant/rename/compaction/chained/review coverage. No-delegation T1/T7/T8 is no longer assigned these obligations. |
| O3/mutation, claim integrity and false surfacing | Main deterministic key: ≥6 O3 and unauthorized-mutation opportunities each; zero claim-integrity violations; ≥20 finding assertions for the bounded non-critical false-surfacing rate. Required capabilities/containment remain real-owner gates. |
| 6.6 preservation | P01–P19 (38 paired runs/arm), T2/T3 (two each), T4–T6 (8 paired episodes), and three R2 classes (≥6 distinct opportunities each) can use declared deterministic panel keys. R2 authoring and acceptance-review exposure and zero pre-R2 owner reads remain binding. |
| Ordinary reporting and Q4 negatives | One ordinary key: 32 paired S01–S11/H01–H05 episodes; ≥8 near-boundary negatives; ≥3 episodes/arm for every new activation class. Correct selection is report-only, negative-selection floors remain mandatory. |
| Predicate/owner false activation | All family keys contribute pooled counts; ≥12 predicate-excluded opportunities must exist on deterministic keys alone. Zero owner false activation and the predicate count bound cannot be improved by adding clean runs. Other profiles use their own scored counts. |
| Burden | T1/T7/T8 deterministic key: fixed-cost/no-lookup tests, three initial pairs with bounded T7 extension. Main key: class-iii/new-class active material, delegate burden, zero unowed reads/probes and report/time medians. This closes the sixth check's misplaced-burden defect structurally. |
| Comparative claim | Main deterministic key; paired opportunity minima, ≥15 percentage points and ≥3 additional correct independent opportunities, no impermissible decline and noise/cluster assessment. Named-only claim limits do not waive the separate unnamed floor. |
| Human trial | Main-key outputs, exactly one unseen fixture/arm, ≥20 routine and ≥4 critical questions/arm; primary-only legibility claim. A permitted non-discriminating repeat cannot erase an observed failure. |

The revised map now covers every ordered criterion and requires assignment of every remaining part, exposure and report measure. Its fixed campaign serialization/digests, pre-run reproduction and run/assessment bindings prevent retrospective map substitution. These are coherent **structural requirements**, not proof that any concrete family or corpus meets them.

**Cross-profile rescue:** attempted substituting a stronger-model gain, missing Flash burden, underexposed Flash ordinary negatives, an unresolved human trial, and a profile unable to expose a required property. The final-primary-criterion rule blocks all these. Changing/re-keying the family has declared review/identity/disclosure requirements; it cannot silently remove the failure.

**Mechanism/input bypass:** attempted body injection labelled runtime-command, later model reading, wrong-root/transform text, auxiliary-request reclassification, configuration/environment-carried skill text and an adapter assertion without observer request 0. Input-template equality, frozen request classification, channel/config checks, full transform matching and request-0 evidence reject these as specified. They still require real-path implementation/pre-run proof; no implementation claim follows from this inspection.

**Claim-limit interactions:** predeclared descriptive-only routes below three episodes do not grant a median claim; named-only comparative scope does not remove the unnamed absolute floor; a non-primary deterministic-key PASS expressly omits ordinary-selection and human-legibility claims while retaining its own predicate/owner guards. Missing mandatory exposure or inability to observe a required property remains non-PASS. Those exceptions do not resolve B1's pre-run/campaign accounting collision.

**Out-of-matrix adequacy:** B1 is outside the planted scientific-case matrix: every oracle could correctly score its scientific cases and detect every deliberately broken activation probe, yet the assembled procedure still has incompatible qualification outcomes. Thus matrix completeness/hash binding alone cannot establish acceptance-procedure adequacy. On finding this decision-changing blocker, further live/statistical/source-harness exploration was neither authorized nor useful for the current verdict and stopped.

## Sixth-check disposition, gaps and minors

The sixth check was read as finding data. Independently reconstructed closure:

- Its B1: the main-key/T1 split now assigns all burden parts, including delegate minima, where they can occur.
- G1/G2/G4: non-primary claim limits, campaign/family provenance and permitted descriptive/named-only limits are explicit.
- G3: the workplan root-selection evidence marker now restricts the weaker native alternative to ordinary entry and routes deterministic proof to request 0 plus runtime input.
- Budget schedules, §7 permitted repeats, re-key scope and prompt-bearing variables are now specified.

**Minor m1:** the paragraph immediately after overlay item 6 still calls the contract realization “revision 6” and the latest check “overlay revision 4 and contract revision 5.” It conflicts with the leading revision-6 overlay/revision-7 contract summaries. The leading exact subjects and routes make the intended current boundary recoverable, so this is a stale navigation/disposition summary rather than an additional blocker. Reconcile it with the owning repair, without replaying the historical amendment chain.

No other material gap was established before stopping at B1. This is not an exhaustive absence assertion. Custody-audit/admission changes and untracked Stage 7 option-1 material are separate, unresolved scope; this review neither accepts nor rejects them.

## Convergence and project-memory applicability

The repair closes the existing mapping mechanism rather than adding another one. B1 shows the next useful action is a bounded simplification/re-derivation of **evidence accounting scope**: distinguish integrity probes, campaign runs, their assessments and their aggregation, then reconcile the existing map/manifests. Another isolated wording exception or scorer wrapper would preserve the common cause. Keep Q1–Q5 and hard activation unchanged. Review count does not force acceptance.

The workplan-bound integrated PEM base is `2585b73f00420daca185a4fbb9ac42a79473eda1`, independently verified as an ancestor of designated `main`. Its PEM blob equals subject HEAD and main (`1561797125622f355f84eb27319f87e8fa4227d9`); no overlay is composed. Repository-aware validation returned five families, zero notices. Canonical metadata for all five families was searched, including entries absent from a hot-only view. Stale 6.5 front matter and partial history remain limitations, not absence evidence.

```yaml
pem_basis:
  accepted_project_state: 2585b73f00420daca185a4fbb9ac42a79473eda1
  accepted_pem: "hjin98/scientific-software-development-protocol@2585b73f00420daca185a4fbb9ac42a79473eda1:PROJECT-ENGINEERING-MEMORY.md"
  candidate_overlay_semantic_candidate: NONE
has:
  - id: DS-001
    disposition: APPLICABLE
    reason: Correct matrix/hash/scorer checks cannot prove assembled acceptance-procedure adequacy; used only as an independently checked evidence-method hypothesis.
  - id: PC-001
    disposition: NOT_APPLICABLE
    reason: This document-only review does not mutate historical resources or claim their behavioral qualification.
  - id: FF-001
    disposition: NOT_APPLICABLE
    reason: No immutable semantic/public-source publication occurs.
  - id: SP-001
    disposition: NOT_APPLICABLE
    reason: No source-routing repair or package regeneration occurs.
  - id: SP-002
    disposition: NOT_APPLICABLE
    reason: No bootstrap or recovery publication occurs.
```

PEM supplies no normative force and is not updated.

## Executed, reused and missing checks

**Executed:** Git status/exact-commit/blob resolution; accepted release-state source resolution; read contract §§1–8, stakeholder §§1–7 and amendment record; sixth finding record; focused `b9f23d7..2a49e53` contract/overlay delta; overlay/header/activation-marker and surrounding entry/evidence statements; unchanged preservation basis and relevant workplan floors; accepted 6.6 D3/kernel and triggered concern reads; bounded analytical whole-family/criterion/exposure mapping and bypass counterexamples above; `git log -S` for B1 origin; PEM base ancestry/blob comparisons, canonical metadata search and `python3 source/project_engineering_memory.py PROJECT-ENGINEERING-MEMORY.md` (valid, five families/zero notices); `git diff --check b9f23d7 2a49e53` (clean).

**Reused as data only:** sixth-check findings and public probe descriptions. No preceding PASS, test count, runtime probe, author disposition or report was imported as exact-subject acceptance evidence. No new runtime-command behavior was verified here.

**Not executed / not established:** any live run; observer/input/transform adapter realization; profile/family freeze and real §6 canary/negative integrity suite; actual corpus classification/exposure and every withheld branch; admission/custody/access audit; qualification scoring; statistical adequacy/noise discrimination; human trial; full regression/package/parity/snapshot/frozen-resource checks. The subjects/report are prose-only and no source/generated descendant is changed; broad software acceptance would not resolve B1. Prior suite skips remain unexecuted evidence, not PASS.

No withheld store or answer material was opened. No doctrine, harness, profile, frozen tree, subject, existing evidence or untracked file was edited. Only this requested review record is written; root owns its authorized commit. **Contract-dependent work must stop at NO-PASS.**
