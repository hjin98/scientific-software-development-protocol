# D4 package-access ledger: provisional realization and Serious Challenge

Written 2026-10-04 America/Chicago (diagnostic run 2026-10-05 UTC). Governing SSDP **6.6.0**. Protocol 7.0 remains **NON-QUALIFIED**. **D4 completion: BLOCKED / NO-PASS. No independent implementation Review or admission is claimed.**

## Serious Challenge — earliest affected owner D3, item 8 / case (z)

The accepted decision requires mechanical verification that no byte-identical package copy is reachable elsewhere in the sandbox **“in any encoding.”** Case (z) extends the premise check to package, fixtures, workspace, stub/MCP results and task text. Neither the decision nor the contract delegation specifies the reconstruction relation or the acceptable evidence that closes this universal negative for a sandbox retaining arbitrary process/code execution. A finite decoder list is a narrower rule; a whole-owner-line scan is also a narrower rule. D4 is not authorized to select either as the acceptance criterion.

**Observed counterexample to a line/ordinary-file scan being sufficient:** a deliberately invalid fixture carries a base85-encoded, keyed-XOR tar archive containing the entire installed package. A workspace Python program reverses these transformations, extracts the owner bytes in memory, and prints their length only. Every one of its 238 regular files reconstructs byte-for-byte identically to the actual installed package, verified from the retained fixture and installed tree. The fixture has no whole owner line at or above the 48-byte floor. The process opens the fixture payload, not the watched installed-package inodes. Its result contains no owner-class supply.

Through **real OMP → trusted observer → harness/core**, this diagnostic produced:

| Field | Diagnostic value |
|---|---|
| Raw run evidence state | `COMPLETE_ADMISSIBLE` |
| Byte exactness | `true` |
| Published active bytes | `14454` (delivered root only) |
| Owner floor exactness | `true` |
| Owner opens / positive evidence | both empty |
| Production `owner_floor_state` with independently declared no R2 | `PASS` |

These values are **not an accepted result**: the fixture violates the required premise, and the draft does not yet implement its check. This is not evidence that heartbeat ordering fails, that the accepted clean fixtures contain copies, or that all mechanical verification is impossible. It establishes that premise verification is causally necessary and that a familiar text scan cannot supply its warrant. The full arbitrary-encoding closure obligation is materially under-specified for D4.

**Requested D3 disposition:** state the precise reconstruction/closure predicate and the permitted verification witness for all reachable input sources, including executable decoders and runtime/tool-result sources; state the treatment of undecidable or unrecognized cases. If a constructive, frozen-source provenance argument is sufficient, identify its required scope and evidence. If a bounded family of encodings is intended, D3 must own that restriction. Clarify whether the prohibition includes independently encoded owner files as well as an entire package tree. Prefer the smallest governed text clarification; this handoff proposes no new observer mechanism, principal, channel, sandbox restriction, or accepted rule. Passed documents and hashes remain untouched. The user-authorized stop on materially ambiguous/inadequate authority and the governing D4 skill's Challenge rule apply.

This Challenge is routed by this durable handoff; no external message or independent reviewer execution was performed. Resume dependent realization only after the owner resolves it under the governing authority and the revised applicability is established.

## Authority and exact identities

- D3 revision 8: `qualification/ssdp70/D3-PACKAGE-ACCESS-LEDGER-OBSERVATION-DECISION-2026-10-04.md`, SHA-256 `fccb9a3a44afd89338eb19c8b3238a9943fab7c88ee694428dc7d6ce124fd783`, accepted bytes at commit `07a4bb0d2093605425374ac3102c6ac04dbe1652`.
- Contract revision 15: `qualification/ssdp70/PROTOCOL-7.0-EVALUATION-AND-QUALIFICATION-CONTRACT.md`, SHA-256 `c08a3e658a69714dc55218943f1d4fc3763f1d0ded4bbf70fdb06e7df08e1920`.
- Governing closeout: `qualification/ssdp70/PACKAGE-ACCESS-LEDGER-DECISION-CLOSEOUT-2026-10-04.md`; workplan: `workplans/active/SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY-CONSOLIDATED.md`.
- Root release-state lookup: accepted-current 6.6.0, public source `22f4bdba53795da3a6f13f162529f3a843fc37ae`, recovery `384666764da4c55b282e6b1595ab97e2f86e1dc4` (not inferred from development HEAD).
- Development HEAD `c4b8781bfa5764a406758130d21e934ecf3662c8`, HEAD tree `a3efc6c70514e7d81b621b713c5e610ee67d6b03`, branch `ssdp-7.0-scientific-epistemic-closure`.
- Tracked working-tree manifest SHA-256 `f8b8fa7744c503ec1a3ebf917b36883e12650e51179a4c95ad1a387c1b35cee1`; draft patch SHA-256 `4d027e37ada78e60f7177c08798808c8bc54635cf05aa869a916f9ec232bb8ae`. These identify the uncommitted code, not merely the old HEAD tree. See `execution-tree-binding.json`, `tracked-worktree-manifest.json`, `implementation-draft.patch`.
- Exact OMP executable `/home/samjin/.local/bin/omp`, 18.0.11, SHA-256 `6054460b29e9bad5eba78336f291e1979c2fa0a5cd96fc2d92afd666cc681d26`.

No commit, push, runner/profile/transform admission, qualification campaign, custody access, or release-state edit was performed. The eight pre-existing out-of-scope untracked files remain untouched. Canonical source/generated distributions were not edited. PEM stayed cold.

## Diagnostic custody and reproduction

`encoded-package-run/` is an unchanged copy of the development run at `/tmp/s70h/ssdp70-omp-stagef/qualification/OMP-STANDIN-20261005T025110Z-c4b8781bfa57-028bbc4b93e7/run`. Its run identity is `8879791e51bed31ba8a01a211eb68799dc7c10b579b551970ef80773cd83b370`. Its purpose is development/probe, never qualification. The provider is the local stand-in only; OMP, observer, containment, normalizer, harness and core are real owners. The rig uses its fixed harmless `SENTINEL` credential; no real provider credential was accessed. Observer request headers retain authorization dispositions/digests rather than a raw Authorization value. The diagnostic source and logs were screened on that basis before persistence.

`encoded-package-verification.json` independently compares decoded archive member hashes against the run's installed tree; it records all 238 matched members. `encoded-package-proof.json` records the observed results. The exact encoded payload SHA-256 is `f1c11197ba7a288218fdfcfa0c1343d076e32e06bdd983c1425aab6e658c2b40`; decoded archive SHA-256 `4f272078abeeb1dc8e4c79ad9821cc82e56a8019cd5e87795cbc056dbf487127`; owner SHA-256 `370802006b9cd11f0d77f67d0891eb0c0d075878432b13546064377925027140`. No fixture was relabeled as honest or admitted.

Reproduce with the retained `encoded-package-probe.py` from this repository checkout, `PYTHONDONTWRITEBYTECODE=1`, `SSDP70_OMP_EXE=/home/samjin/.local/bin/omp`, and short scratch `HOME=/tmp/s70h`. Scratch HOME needs `ssdp70-omp-stagef/runtime-closures` pointing at the existing immutable runtime closures. The rig writes a fresh unique run directory; do not overwrite retained evidence. Local TCP stand-in execution requires the same sandbox escalation used for authorized real-runtime tests. Tar metadata/run identities change on a fresh reproduction; compare reconstructed member bytes and observed behavior, not the fresh archive identity to this old identity.

The earlier owner-only encoded probe is retained separately in `encoded-copy-proof.json` and its script; it is not substituted for the stronger full-package demonstration. `background-proof.json` retains a separate development probe: an actual in-flight background owner open receives a window containing the following R2 turn and therefore remains UNRESOLVED. Earlier background attempts used a wrong scratch path and showed no actual owner open; they are not supporting evidence. Their scratch runs were preserved, not erased.

## Provisional implementation surface

The ten modified tracked eval files are preserved as an **unfinished draft**. Production ownership remains in `package_ledger.py`, `adapters/omp.py`, `harness70.py`, `core70.py`, `assess70.py` and `batch_assess70.py`; request-clock capture is in `evidence70.py`. Changes include same-instance heartbeats and per-interval row folding, bracket/window accounting, distinct-line owner supply and minor exposure, separate byte/owner exactness, always-published positive evidence, basename matching, observer monotonic request stamps, request-pairing verification, a derived supervisor event/recomputation path, and initial claim/replacement/T7 plumbing. Tests in `test_package_ledger.py`, `test_batch_cli.py`, and `test_activation_accounting.py` are also provisional.

**Do not use this draft for qualification.** In addition to the upstream premise boundary, known unfinished D4 work includes:

- Finish malformed-artifact/schema fail-closed handling, pin accepted D3 provenance rather than deriving a current-file digest with an old commit, and enforce ledger-event recomputation even when required artifacts/events are missing.
- Reconcile the request-position primitive precisely at the first tool-call/result event (including final no-tool turns); finish retries, parallel R2, compaction and mismatch production discriminators.
- Finish core claim gates and typed independent R2/replacement adjudication validation. Positive evidence, negative conclusions and observed-content meaning must remain separate.
- Finish replacement obligation enforcement and original disclosure, overflow-cause adjudication, per-question availability without a byte bound, and T7 median/owner-floor-only bookkeeping. In particular, known resolved owner results and unknown-value T7 route resolution must not be overwritten by a generic run-level inadmissibility gate.
- Implement the entire premise check only after the owner supplies its closure criterion; current code does not reject the deliberately encoded fixture.
- Exercise all accepted cases at the real production path, then independent Review and pre-run checker handoff. Green synthetic/real-kernel helpers are not substitutes.

## Evidence and outstanding acceptance

Final draft **bounded regression: 57 tests OK**, command `python3 -m unittest test_package_ledger test_batch_cli test_harness_integration`, under `qualification/ssdp70/eval`. Hash-bound output and command/time record: `bounded-regression.log` / `bounded-regression.json`; code/tree binding above. `git diff --check` was clean before this new handoff was added; final preservation verification is recorded separately.

Earlier intermediate executions (not final acceptance; no standalone hash-bound log retained for those executions) were: requested non-runtime eval set 278 OK; root tests 407 OK with 3 skipped; one real-runtime test method covering all seven declared roots and injected delivery 1 test OK; package-ledger/unit iterations and targeted same-response/background probes. They do not close the final affected regression, and the skipped root checks are not PASS.

**Required but NOT RUN / NOT COMPLETE, all blocking D4 completion:**

- Complete real OMP → observer → harness/core → scorer acceptance for **every case (a)–(z)**. No case is declared accepted from this draft. New unit tests directly explore portions of (k)–(t), (w), (x), (y), and real-kernel heartbeat/row-bound portions of (p), (r), (u), (x); those are narrower evidence only. Case (z) is blocked on the Challenge above.
- Each new discriminator against pre-change code: not run; none is claimed to satisfy the counterfactual requirement.
- Complete updated `test_activation_accounting` and `test_omp_integration` real-runtime suites, including the new partial/error/quantum/mid-run forms: not run at the final draft.
- Complete requested final non-runtime eval regression, stage-F regressions and root regression: not rerun after the last code edits. The earlier 3 skipped root tests remain unexecuted and their applicability/reasons are not yet closed.
- Production replacement/T7/byte-bound acceptance and caps: incomplete.
- Mechanical premise checking and regeneration invalidation: incomplete.
- Independent implementation Review: not initiated; implementer cannot accept this work.
- Independent checker executor rehearsal, all three arm package shapes/common honest forms, bracket-width distributions and per-question rates: not run (checker-owned).
- Frozen run count N and instantiated 0.8 target: unavailable; gate unmet.
- F-5, stakeholder ratification, runner/profile/transform admission and any qualification: remain open; none performed.

## Preserved text deltas and checker brief

The passed contract/D3/workplan were not edited. At the next governed revision retain these existing non-blocking text dispositions: effect (d) means a censored burden sample neutral on outcome; align effect (f) with the no-ledger bullet; state the T7 owner-floor rerun cap unit (per affected original run, at most twice); clarify per-question availability when a byte bound is absent, minor-exposure placement, and request-position versus same-response wording; reduce repeated 256-byte rules to the canonical pointer. Monotonic request stamping is implemented provisionally and still needs full production acceptance.

After the Challenge is resolved and implementation independently passes, the checker brief must include: above-quantum keyword grep as intended pre-R2 FAIL; R2 as a parallel action; pairing mismatch; full and owner-only copies with computational encodings; same-response owner load; non-literal `PROTOCOL_VERSION`; retries; compaction/long-session rescan; and supervisor contention. Rehearsal remains independent and must freeze common honest forms, per-arm package identities, N/target and all gate parameters before admission.
