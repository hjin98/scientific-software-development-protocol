---
kind: ssdp63-bootstrap-qualification-result
protocol_version: 6.3.0
profile_id: ssdp-protocol-6.3
public_source_bootstrap: 1484c1d3caa49d87cc15bc52a5e775399c1dae1b
publication_mapping_commit: d9d5ca5611bb703ec704c6e7e95a090491f7eac3
generated_descendant_commit: 0c1854aea07a719e606d6fab69382a1f546c36bb
clean_evidence_head: 2812c170a30783e3c2d585e14161eb6141bd27c7
accepted_current_protocol: 6.2.0
accepted_current_recovery: b59adc77efe6951912cfd705cc43830c58ca27d0
protocol_63_recovery: unavailable_pending_full_qualification_and_independent_review
executor_model: GPT-5.6 Sol
date: 2026-09-11
result: PASS_BOOTSTRAP_LIFECYCLE_ONLY
independent_review: pending
authority: non-normative-qualification-evidence
---

# Protocol 6.3 Public-Source Bootstrap Qualification

## Disposition

**PASS for the Protocol 6.3 public-source bootstrap lifecycle only.** This record does not establish full Protocol 6.3 qualification, independent Review PASS, recovery, accepted-current status, or `main` cutover. Protocol 6.2 remains accepted-current at recovery `b59adc77efe6951912cfd705cc43830c58ca27d0`.

The version-bound Protocol 6.3 public fallback is now the exact immutable ancestor:

```text
1484c1d3caa49d87cc15bc52a5e775399c1dae1b
```

That bootstrap snapshot intentionally does not self-name. Its identity is published only by later descendant mapping commit `d9d5ca5611bb703ec704c6e7e95a090491f7eac3`.

## Evidence chain

1. **Bootstrap snapshot readiness — `1484c1d3caa49d87cc15bc52a5e775399c1dae1b`.** Ordinary PR CI had already passed repository regressions, canonical package build, standalone package validation, committed `dist` parity, generated Protocol 6.3 snapshot parity, and the complete Orchestrator Core suite before the snapshot was selected as bootstrap.
2. **Independent exact-ref realization — `9a53d71c52d0c01687d982d5117f02922187ed46`, run `34613097899`.** `tests/test_protocol_63_bootstrap.py` fetched the immutable `1484...` source directly from the public repository, confirmed `6.3.0`, confirmed self-reference-safe pre-mapping state, exercised PEM schema/validator surfaces, and traversed role/reference Markdown closure including the PEM route. Both ordinary repository/package and Core jobs passed.
3. **Self-reference-safe publication — `d9d5ca5611bb703ec704c6e7e95a090491f7eac3`.** A later descendant published `6.3.0 public-source bootstrap -> 1484...` in the versioning/portability/prompt/navigation surfaces, retained the exact 6.2 mapping independently, and left Protocol 6.3 recovery unavailable.
4. **Generated descendants — `0c1854aea07a719e606d6fab69382a1f546c36bb`.** `dist/` and `ssdp-protocol-6.3` mapping-bearing snapshot bytes were regenerated from canonical source rather than hand-edited.
5. **Assembled publication gate — workflow run `34614466927`.** Focused public-source/version tests passed before publication; after regeneration the full repository unittest discovery, temporary canonical package build, standalone package validation, committed `dist` parity, generated snapshot parity, complete Orchestrator Core acceptance suite, and whitespace check all passed before the mapping/generated commits were pushed.
6. **Clean-head ordinary CI — `2812c170a30783e3c2d585e14161eb6141bd27c7`, run `34614684594`.** After all temporary bootstrap workflows were removed, ordinary PR CI passed both jobs. The build job passed source regression, package build, independent package validation, committed `dist` parity, and whitespace validation; the Core job passed packaged snapshot parity and the complete Core acceptance suite.

## Falsification history retained

Publication was not forced through earlier red gates. Two pre-publication attempts stopped before push when inherited tests still encoded the pre-bootstrap sentinel or when a required `self-reference-safe source snapshot` distinction had been compressed away. A later assembled diagnostic showed every product gate green except Core containment, where the temporary `.github/scripts/publish_ssdp63_bootstrap.py` diagnostic helper itself violated the orchestrator containment rule. The helper was removed before the successful publication gate. These failed attempts are historical diagnostic evidence, not acceptance evidence.

## Remaining lifecycle boundary

This PASS closes only the 6.3 public-source bootstrap/profile/generated-artifact publication portion of Stage E. The following remain open and therefore block Protocol 6.3 acceptance/recovery:

- complete T40-T120 preservation/qualification closure;
- fresh inherited scenarios 1-115 against the assembled 6.3 candidate;
- Q63-01 through Q63-79 with discriminating counterfactuals;
- F63-A through F63-BJ plus the four inherited Challenge falsification passes;
- affected prior requalifications/static sensors with correct static-vs-live claim scope;
- independent assembled-candidate D3/Protocol Review;
- only after Review PASS, immutable 6.3 recovery selection, later recovery mapping, regenerated descendant acceptance, PEM/HAS/lifecycle reconciliation, and workplan closeout.

A missing required Stage-F case remains **not passed**.