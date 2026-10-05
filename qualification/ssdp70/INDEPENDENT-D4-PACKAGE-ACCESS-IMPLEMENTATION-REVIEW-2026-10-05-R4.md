# Independent D4 package-access implementation Review R4

Governing SSDP **6.6.0**; Protocol 7.0 **NON-QUALIFIED**. Independent `code_review` context. Append-only successor to R3; neither report is admission or qualification authority.

## Verdict

**NO-PASS.** R3-B1 is repaired by the owner-local selected-run fallback, which preserves retained fail judgments without admitting retained pass/unresolved judgments as doctrine scores. A second, independently demonstrated blocker remains: **R4-B1, a T7 owner-only rerun's unresolved critical judgment disappears and the critical criterion can falsely PASS**. No overall qualification PASS was manufactured; the false criterion PASS is demonstrated directly through the real slot/part scorer. Stop-first-blocker applied; runtime repetitions remain incomplete.

No Serious Challenge is required for the demonstrated code defect: clarification B.2 is coherent and requires a block in a replacement to stand for the slot, which stays non-PASS or unresolved whatever the evidence state. Known limitation 3 records the current omission, but its accompanying factual assertion that none of these limitations creates a false PASS is refuted by this probe. A factual limitation does not authorize overriding B.2. If the authority owner intends that exception normatively, it must reopen/adjudicate that conflict rather than accept the current false criterion PASS.

## R4-B1 and executable witness

Earliest owner: `qualification/ssdp70/eval/batch_assess70.py:score_slots`, T7 owner-only `owner_scored` override and standing-failure loop. The override copies only `owner_floor_state`. The outside-scored-slot loop retains only `fail` dispositions. Consequently an unresolved critical judgment in the standing T7 owner-only rerun reaches neither `aggregate_parts`' critical opportunities nor a critical-unresolved criterion guard.

Input distinction matters: the original T7 run has exact bytes and `COMPLETE_ADMISSIBLE` evidence, all other doctrine judgments pass, but its owner floor is independently UNRESOLVED. This is permitted by the two-question split: an explained owner open not provably after R2 can leave the owner floor unresolved while bytes are exact. A T7 owner-only rerun resolves that owner question as PASS but carries an unresolved critical disposition. `blocks_rerun` correctly declares this a block and sets `standing_failure: true`. It cannot subsequently vanish from the governed criterion.

Executable probe retained at `package-access-ledger-d4-20261005-review-r4-partial/t7probe.py`, SHA-256 **34c4f58ff3bb969ee9c8e791013af8df9637a78e7c21d0daf6038a7a06d061f5**. Output `t7probe.json`. Run from final candidate's `qualification/ssdp70/eval` with `PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 python3 <probe-path>`.

The script reuses `SlotScoringComposition` only for fixture construction and calls the actual `score_slots` and `aggregate_parts`. It augments the synthetic declaration with three clean runs per arm and twelve critical opportunities per arm bound to distinct original run IDs, then supplies:

```python
original_overrides = {
    "evidence_state": "COMPLETE_ADMISSIBLE", "qualification_outcome": "PASS",
    "criteria": {"harness/admissibility": "PASS", "deterministic activation": "PASS"},
    "resource_observation": {"exact": True},
    "dispositions": [{"item": "i1", "critical": True, "measure": "critical", "result": "pass"}]}
owner_replacement = {
    "dispositions": [{"item": "i1", "critical": True, "measure": "critical", "result": "unresolved"}]}
```

The original's owner floor remains UNRESOLVED from the fixture. Its summary is set to the corresponding exact 14,000-byte burden value. Observed output: replacement `scored: true`, `standing_failure: true`; **critical part PASS, candidate 12/12 pass and zero unresolved**; owner part PASS; fixed-cost part PASS; harness/admissibility PASS; candidate disposition tally 12 pass, 0 fail, 0 unresolved. The unresolved critical rerun judgment is absent. A prior probe with byte-inexact original remained unresolved through T7 pair-addition and harness guards; that form alone did not demonstrate a false PASS. The exact-byte original discriminates the defect.

This is a synthetic production-function counterexample, not independent opportunity custody, a real provider campaign or qualification evidence. It demonstrates the protected scoring invariant and its omission; no substitute scorer or overall all-criterion PASS is used. Minimal repair belongs to the existing slot/criterion owner: retain a standing T7 critical-unresolved block in the corresponding final non-PASS criterion without changing the original burden median or admitting non-failing inadmissible doctrine measurements. No new replacement eligibility or rerun rule is implied.

## Candidate binding and evidence

Reviewed six-file assembly: baseline `3ca1891a0415ace6026bfb452377a557bc6947d6` plus the four exact uncommitted file hashes and unchanged authorities bound in R3, plus:

- `eval/batch_assess70.py`: `6d9602f68ecf6941e6046464aeb930c2b759ad301c17976fb6a9be27fc061b0e`;
- `eval/test_batch_cli.py`: `bae644e958cab40d25511073c390ffc0a668e8280afc92cdad11e1f82f215f0d`.

Both new hashes and repair diff independently checked/copied. The R3 candidate remains separately identified; this report does not relabel its earlier evidence. Original R3 logs preserved in `package-access-ledger-d4-20261005-review-r3-partial`; repaired-candidate partial logs/probe preserved in `package-access-ledger-d4-20261005-review-r4-partial`.

Runtime repetitions on this assembly were concurrent through the real OMP/observer/adapter/harness/core and local stand-in only, using fifteen workers (4+4 activation, 3+4 integration) and distinct short scratch homes. At blocker stop: activation **22/24 completed, all 22 passed** in each repetition; integration **21/54 completed, all 21 passed** in repetition 1 and **30/54 completed, all 30 passed** in repetition 2. These are partial completions, not suite PASS. Reviewer-owned process group `721533` stopped with TERM, scratch homes removed. Full affected runtime repetitions, fast independent full regression and remaining targeted falsification are required but unexecuted/incomplete. No provider rehearsal/credential use, code/authority edits, commit/push or old-evidence rewrite occurred.

## Remaining scope and independence

The R3 canonical reconstruction, exact unchanged D3/contract bindings and common-mode limits remain applicable. R4-1 observation-bound dispositions remains the stakeholder-retained availability limitation; no replacement-eligibility change is proposed. Unbound declared runs remain a custodian/pre-run-checker completeness obligation, not evidence that such a frozen production manifest has been admitted. The newly executed T7 case refutes only known limitation 3's harmlessness assertion. Production premise admission, all-arm executor rehearsal, frozen N/0.8 arithmetic and disparity bound remain separate open gates. Protocol source/distribution unchanged; no release qualification is claimed. Shared model family, code corpus and fixture rig constrain independence; expected non-PASS follows canonical B.2 rather than author test expectations. No scientific results were produced or interpreted; PEM remained cold for this owner-local review. Prior memory was search-only as disclosed in R3.
