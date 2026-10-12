# D4 package-access ledger: final clean functional PASS closeout

Governing SSDP **6.6.0**; Protocol 7.0 **NON-QUALIFIED**. Author: root D4 implementation agent. The implementer cannot accept its own work. Baseline HEAD `3ca1891a0415ace6026bfb452377a557bc6947d6`; proposed candidate is the uncommitted 6-file working delta bound in `delta-t7-final.patch` and `identity-closed.json`.

## Verdict and boundary

**Independent text Review R2 PASS** and **independent code Review R5 bounded functional PASS** are complete. No surviving blocking code finding or Serious Challenge was demonstrated after independent reconstruction, the R3 and R4 executable counterexamples, root repairs, and complete affected regression. This constitutes a clean, verified functional implementation stopping boundary for D4.

This report documents development evidence and reviewer verification; it is **not** acceptance of a production premise witness, executor rehearsal, runner/profile/transform admission, or qualification. Those required gates remain open.

## Realized decisions and repairs

1. **Route (iii) unverified pairing gate**: The stakeholder reopened D3 to fail closed for route (iii) when request pairing is unverified (`D3-PACKAGE-ACCESS-UNVERIFIED-PAIRING-FAIL-CLOSURE-2026-10-05.md`, SHA `c2f7a3a348a9e9e1ef448b81e0db456e4e6720afdd5994f14b22068035edee9c`). In `eval/package_ledger.py:account`, route (iii) requires nonempty list-of-dict request metadata, all pairing flags literally `True`, and valid integer or `None` positions (excluding `bool`). Malformed, missing, or unverified pairing denies only route (iii); native, delivery, path-linked routes and owner positive evidence remain available. `eval/core70.py` binds the clarification and independent text R2 report.
2. **R3-B1 standing-failure tally repair**: Review R3 demonstrated that scored inadmissible standing replacements lost critical failure tallies. `eval/batch_assess70.py:score_slots` retains definite failures from `original_dispositions` when scored dispositions are absent, without scoring retained passes.
3. **R4-B1 T7 critical unresolved block repair**: Review R4 demonstrated that a T7 owner-only critical unresolved rerun disposition could disappear from scoring, allowing a false critical-criterion PASS. `batch_assess70.py:score_slots` retains critical unresolved judgments once; `aggregate_assessments` carries them into the existing `no critical failure` criterion as UNRESOLVED (with definite FAIL precedence). Noncritical unresolved judgments bind through original slot frozen item/opportunity part/criterion. Unmapped blocks raise `ContractError`. Owner-floor facts and original T7 burden slot remain unchanged.

## Hash-bound assembly

The candidate delta consists of six modified files over baseline HEAD `3ca1891a0415ace6026bfb452377a557bc6947d6`. All 12 assembly and authority files, plus the final R5 review report, were verified unchanged:

| File | SHA-256 |
|---|---|
| `qualification/ssdp70/eval/package_ledger.py` | `d8c408eda659cd4a8515a3f5db882077d3e089ee3d556caef0c32102c61eac39` |
| `qualification/ssdp70/eval/core70.py` | `6d40340ee7bbdbb130f22ea6e1c0067294353ad3bc7c88efceacc32f3fdb84bd` |
| `qualification/ssdp70/eval/test_package_ledger.py` | `906751dcc856e63631ea875e95a7ba8b6def672ec08549f8fdc6f65a91298755` |
| `qualification/ssdp70/eval/test_activation_accounting.py` | `b59e97feda838e34c2b65923b25f0de534cea90534060e11a821f99b94692553` |
| `qualification/ssdp70/eval/batch_assess70.py` | `2850d8aad354845e88b4391039fc5b74c547fa5f710d77a39bcadfd7bfdee6f5` |
| `qualification/ssdp70/eval/test_batch_cli.py` | `e41c27ccd244f2ffc06431664f35356a91728422073a785397700c9f14c31bf8` |
| `qualification/ssdp70/D3-PACKAGE-ACCESS-LEDGER-OBSERVATION-DECISION-2026-10-04.md` | `fccb9a3a44afd89338eb19c8b3238a9943fab7c88ee694428dc7d6ce124fd783` |
| `qualification/ssdp70/D3-PACKAGE-ACCESS-PREMISE-CLOSURE-2026-10-04.md` | `5f713e2bd816950a2fd0962c6732242631295b3416387beb761c8b40906a3316` |
| `qualification/ssdp70/PROTOCOL-7.0-EVALUATION-AND-QUALIFICATION-CONTRACT.md` | `c08a3e658a69714dc55218943f1d4fc3763f1d0ded4bbf70fdb06e7df08e1920` |
| `qualification/ssdp70/D3-PACKAGE-ACCESS-WINDOW-AND-REPLACEMENT-CLARIFICATION-2026-10-05.md` | `b7bead4ecb139732683d1919740a19ce3342740f2e8dace00781d4159c99e87f` |
| `qualification/ssdp70/D3-PACKAGE-ACCESS-UNVERIFIED-PAIRING-FAIL-CLOSURE-2026-10-05.md` | `c2f7a3a348a9e9e1ef448b81e0db456e4e6720afdd5994f14b22068035edee9c` |
| `qualification/ssdp70/INDEPENDENT-D3-WINDOW-REPLACEMENT-PAIRING-TEXT-REVIEW-2026-10-05-R2.md` | `670e03fd8fbb80c194e21a72e50fc22b1214fdf077744031bb74f34488e7f6f6` |
| `qualification/ssdp70/INDEPENDENT-D4-PACKAGE-ACCESS-IMPLEMENTATION-REVIEW-2026-10-05-R5.md` | `702e08da0bb344b96c3134c7fd22e9e8d0566a2e3df0026ccb0b138a12933677` |

## Executed evidence summary

| Suite / Check | Result |
|---|---|
| `test_activation_accounting` (repetition 1 & 2 concurrent) | **24/24 passed, no skips** |
| `test_omp_integration` (repetition 1 & 2 concurrent) | **54/54 passed, no skips** |
| Focused suite (`test_package_ledger`, `test_batch_cli`, `test_package_premise`) | **113 passed, no skips** |
| Complete affected nonruntime eval modules | **343 passed, no skips** |
| Root regression (`discover -s tests`) | **407 passed, 3 skipped** (remote public-fallback checks: not run) |
| Nine independent direct discriminators | **9 passed** |
| Real OMP path-only and package-scan trajectories | **2 passed** |
| Absent-disposition production-shape scorer probes (T1, T7) | **passed** |
| `git diff --check` | **clean** |

All tests executed with real OMP 18.0.11 (`6054460b...`), Python 3.10.12, and local deterministic stand-in provider under authorized short-lived isolated test environments.

## Open gates outside D4

The following gates remain required before qualification or production admission:
- Independent pre-run completeness checker.
- Executor rehearsal with real provider latency, full package shapes, and honest forms.
- Measurement of partial replacement, unverified pairing, line truncation, bracket width, and R4-1 lost replacement rates.
- Frozen N and instantiated 0.8 target.
- F-5 premise qualification.
- Production premise witness with independent construction/exclusion warrant.
- Frozen byte-disparity bound.
- Stakeholder ratification and runner/profile/transform admission.

## Working tree and protected files

- Exactly six tracked files modified in working tree (`package_ledger.py`, `core70.py`, `test_package_ledger.py`, `test_activation_accounting.py`, `batch_assess70.py`, `test_batch_cli.py`).
- Untracked D3, review, and evidence records preserved.
- Eight out-of-scope untracked files remain untouched (`STAKEHOLDER-DECISION-2026-10-04-PROTOCOL-7.0-STAGE7-OPTION1-CLAIM-SCOPED-ADMISSION.md`, `eval/adapters/omp_eval.py`, `eval/capabilities/omp-evaluator-readonly.json`, `eval/evaluator_admission.py`, `eval/profiles/omp-evaluator-readonly.json`, `eval/profiles/omp-evaluator-readonly.template.json`, `eval/test_omp_eval.py`, `eval/write_oracles.py`).
- No commit or push performed without explicit user authorization.
