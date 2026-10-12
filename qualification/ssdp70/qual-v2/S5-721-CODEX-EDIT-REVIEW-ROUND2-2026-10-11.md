# SSDP 7.2.1 S3 independent edit review, round 2 — NO-PASS

Date: 2026-10-11. Governing protocol: SSDP 6.6.0; same independent Codex software-design reviewer, no candidate authorship. Exact final candidate: `9ffe093269a1e9f7d8819450ed5ea488e9b26920`, branch `ssdp-7.2.1-reduction`, worktree `.claude/worktrees/agent-a2ab8c24b157a8fe2`.

## Decision and stop condition

**NO-PASS**, solely for two unclosed documentary claims in root `CHANGELOG.md`. No Serious Challenge to the ratified minimum. Both executable/semantic repairs and the six-entrypoint reduction condition PASS; final required mechanical acceptance also PASS. That bounded result does not close S3/Go or confer qualification, ratification or release promotion.

The one permitted repair round has been used. Return this second NO-PASS to the stakeholder under the plan's stop rule. This reviewer neither authorizes another repair nor changes candidate prose. README closeout may remain deferred to freeze under the brief, but the brief does not defer CHANGELOG reconciliation.

1. **Unclosed compatibility claim — `CHANGELOG.md:23`.** It still says the 7.2 profile declares 7.2.1 and “still resolves 7.2.0 and 7.2”. The actual owner now correctly raises `core.protocol.incompatible` for exact `7.2.0`, resolving only `7.2.1` and the two-part `7.2` patch-line alias. First review expressly required reconciling this claim as a consequence of the profile repair. Leaving it is material current compatibility misinformation.
2. **Unclosed size claim — `CHANGELOG.md:21`.** It still says documentation shrinks 29 B and maintenance audit grows 37 B. Final measured reductions are 77 B and 11 B respectively; role sections shrink 143–157 B. This line records the superseded round-1 candidate rather than the current capability delta and contradicts the repaired every-entrypoint reduction condition.

A concrete narrow correction for stakeholder consideration is to reconcile those two lines to the final measured table and exact-version rejection below. No source/doctrine rewrite, new mechanism or qualification run is necessary to correct those facts; the reviewer has not made those edits or authorized another round.

## First-round defect disposition

**Profile executable defect: corrected — PASS.** `SSDP72_COMPATIBLE_PROTOCOL_VERSIONS` is now `("7.2.1", "7.2")`; exact `7.2.0` is absent. Independent execution of the real `profile_id_for_version` confirms exact `7.2.0` raises `OrchestratorError`, code `core.protocol.incompatible`. Both supported declarations resolve the actual packaged descriptor to version `7.2.1`. The new `test_exact_patch_version_never_adopts_another_patch` rejects exact 7.2.0 and iterates all supported exact three-part declarations through `protocol_source.resolve_packaged`, requiring the returned descriptor version to equal the declaration. This tests real profile selection and real packaged descriptor loading, not a stand-in. The frozen 7.2.0 candidate is left immutable; fail-closed unsupported resolution does not claim that candidate is qualified or accepted.

**Every-entrypoint reduction defect: corrected — PASS.** The shared Scope paragraph shrinks 48 B without deleting a frozen meaning. It preserves the full inclusion/exclusion predicate and inclusion list, scope reevaluation on a newly material effect, trigger-specific duty applicability, change-only relief plus delegated-answer/gap exceptions, completeness of consumed obligations, optional owner depth and its recommended points. Audit now shrinks 11 B rather than growing 37 B. The new strict entrypoint-and-section test binds its comparison to `2dedcfa` for every block-carrying skill, asserting actual UTF-8 lengths. It adds a sensor for the explicit acceptance condition rather than weakening a semantic floor.

## Lossless O-3, owner consistency and form — PASS

Detailed independent baseline meaning-by-meaning owner is the first review `/tmp/ssdp721-edit-review.md`, its 44 surviving rows and two removal dispositions under ratified workplan M1–M10. That review remains applicable to unchanged meanings on the unchanged routes. This round reconstructs the delta and rechecks all generated mapping/subset coverage in final acceptance; it does not treat implementer phrase pins as semantic authority.

Exactly four phrase pins changed:

| Mapping row | Final consumed phrase | Independent disposition |
|---|---|---|
| R1.exclusion | “Small deterministic local work is included; skip only tooling, infrastructure, editorial work or utilities that cannot materially affect those outputs, retained evidence or interpretation” | PASS. Removal of commas does not weaken the governed exclusion limit; size/determinism/locality still do not independently authorize exclusion. |
| R1.reevaluation | “Re-evaluate scope if a new effect may change it.” | PASS. The effect remains the applicability-changing trigger; no unconditional reread or new obligation. |
| R2.depth | “These checks are complete; the [owner](references/scientific-inspectability-and-initiative.md) is optional depth (definitions, examples), most useful before consequential judgments over realized results, D1-D3 authority work or gate evidence.” | PASS. Same explicit consumed completeness, optionality, locator and recommended points. |
| L.change-only | “Each duty follows its trigger; a change realizing no results owes no null and, finding nothing, adds nothing except answers its delegator asked for and gaps owed for its delegates.” | PASS. Same trigger applicability and relief; no checklist order or finish-all-items framing. |

The matching inherited sensor is reworded to the new exact token; its negative mutation now checks that bytes actually changed before asserting rejection. No predicate, frozen floor, acceptance threshold, frozen rubric or scientific meaning was relaxed. Delegate questions, same-surface variant-question/Persistence references, duty subsets, removed reader/question proposals, materiality-basis widening, O1 authority-authoring requirement and owner statements near lines 71/367 remain unchanged from the independently reviewed round 1. No meaning moved into cold owner depth, no observed-failure coaching added, no new upstream default chosen.

## Candidate/integration identity and independent boundaries

Reviewed the final repair diff against `60b89e2`, the final full source delta against `24518df5627bea00c1d84708acfd26cf2c4edb41`, generated outputs and governing mapping/test definitions. Full source delta still consists of the protocol version, builder dependency comment, Scientific checks fragment and scientific-inspectability owner. Final `git diff eeef4638 HEAD -- source dist` is empty: tooling integration preserves the implementer's source and distribution bytes. Worktree is clean. Accepted 6.6 Orchestrator resources are byte-identical to `22f4bdba`.

Did not read campaign/evaluator data, other S5/S4 reports, OMP workspace, custody or Claude auto-memory. Integrated tooling semantics have a separate independent review; this edit review does not substitute for that owner's approval. Final root regression includes the actual integrated measurement consumer and mapping sensors. No candidate code/prose was authored by this reviewer.

## Final byte accounting

UTF-8 generated entrypoint bytes / Scientific checks section bytes, excluding section trailing newlines. 6.6 section absent = 0. Every final entrypoint and section is strictly smaller than frozen 7.2.0.

| Skill | 6.6 entry/section | 7.2.0 entry/section | Final 7.2.1 entry/section | Delta vs 7.2.0 |
|---|---:|---:|---:|---:|
| scientific-formulation | 6317/0 | 16512/10193 | 16369/10050 | -143/-143 |
| numerical-algorithm-design | 6559/0 | 16754/10193 | 16611/10050 | -143/-143 |
| software-design | 8397/0 | 17905/9506 | 17748/9349 | -157/-157 |
| software-implementation | 7057/0 | 15799/8526 | 15643/8370 | -156/-156 |
| software-documentation | 6264/0 | 11591/5325 | 11514/5248 | -77/-77 |
| software-maintenance-audit | 5837/0 | 9842/4003 | 9831/3992 | -11/-11 |

Baselines: accepted 6.6 `22f4bdba53795da3a6f13f162529f3a843fc37ae`; frozen non-governing/non-qualified 7.2.0 `2dedcfa3408f62bc11a696ac3776183a87b40438`. Full measurements including all three baselines and per-entrypoint SHA-256: `/tmp/ssdp721-round2-bytes.json`.

## Fresh final assembled acceptance — PASS

Executed independently on final HEAD, with root uv `.venv/bin/python` Python 3.13.14. Approved read-only network escalation used for required public immutable-source and isolated-build dependency checks; no denial was bypassed.

- Inherited protocol regression, `SSDP_VALIDATE_PUBLIC_FALLBACK=1`: **438 tests, OK**, no skips (`/tmp/ssdp721-round2-regression.log`). Includes mapping, strict six-surface reduction, structural/negative qualification and inherited immutable-source checks.
- Orchestrator Core full acceptance: **385 tests across 12 modules, OK** (`/tmp/ssdp721-round2-core.log`), including installed wheel/sdist real product checks and new exact-version/packaged-owner negative test.
- Canonical package build: PASS (`/tmp/ssdp721-round2-build.log`); independent validation: PASS (`/tmp/ssdp721-round2-packages.log`); committed distribution parity: PASS (`/tmp/ssdp721-round2-parity.log`). Build output `/tmp/ssdp721-round2-dist`.
- Release-state validation: PASS, coherent (`/tmp/ssdp721-round2-release.log`). Root release state remains unchanged; accepted identities were not guessed from branch/default.
- PEM schema/publication: PASS, five families/zero notices (`/tmp/ssdp721-round2-pem.log`), a required mechanical repository check rather than historical semantic-guidance activation.
- Canonical Orchestrator snapshot `--check`: PASS (`/tmp/ssdp721-round2-snapshot.log`), including frozen 5.16/6.0–6.6/7.1 integrity. Accepted 6.6 resource diff empty.
- Full patch `git diff --check 24518df HEAD`: PASS. Source/distribution identity against implementer `eeef4638`: PASS, empty diff.

No additional broad tests are warranted after these passes. No required acceptance check is unexecuted. The two documentary assertions remain outside those mechanical sensors' proof scope and remain blocking despite passing tests.

Design-lead supplied updated static/Q5c evidence for actual final extractor + `prepare_campaign static`: PASS, `/tmp/ssdp721-static-9ffe093/static-premeasurement.json`; Q5d 24 tests OK. D4 entry-only 15,643 B versus 16,208 B (565 B headroom); workflow mode 35,950 B versus 49,864 B (13,914 B headroom). Optional owner-read outside-mode total 61,724 B versus 16,208 B is explicitly disclosed, outside the accepted enumerated-mode pass. This is supplied bounded static evidence, not this reviewer's independent live campaign, and establishes no qualification/outcome/admission/ratification claim.

## Final reviewed hashes

- `source/shared/fragments/scientific-checks.md`: `595ea342c87b8d65222da827618716cde9092004441e471ad9b3ddf77817ff55`
- `source/shared/references/scientific-inspectability-and-initiative.md`: `d8f36b23e8770f7213265ee3414a4e34e46e746e391e43a837b3f5af924e9d9b`
- `qualification/ssdp70/qual-v2/frozen-minimum-mapping.json`: `a3c93aaa49899f12570a5df46cecc3475612351f6d5c13ea8a8a8c15b5083979`
- `orchestrator/src/sdp_orchestrator/core/profile.py`: `6e66404b2a15b76354575e0034431fcfa2266d0d25b53a4a0d132a6b77b65b47`
- `tests/test_protocol_72_scientific_checks.py`: `5f06e650dcea73c243ff0d77abbd01f126fdc21cac2e5b5bb71b487a33c8c9ae`
- `orchestrator/tests/test_ssdp6_profiles.py`: `7aad6f67a2175782186150f6755136c1066b5e8bcbbd4aadb79fd062d51413ad`
- `CHANGELOG.md`: `828181b4e94a0852a7dc29c09091ef9b9f0a5199b1105be92e3901c0e1885d0d`
