---
kind: d4-implementation-report
governing_protocol_version: 6.6.0
workplan: workplans/active/SSDP-7X-SKILLS-ONLY-RELIABILITY-AND-QUALIFICATION-V2-WORKPLAN.md (revision 3), stage S1, obligations O-1 to O-5
date_utc: 2026-10-07
status: S1 closed. Repository acceptance green; independent mapping check PASS (first check PASS WITH GAPS, G1-G8 repaired, delta re-check PASS; INDEPENDENT-D4-PROTOCOL-7X-S1-MAPPING-CHECK-2026-10-07.md section 6)
---

Governing SSDP version: 6.6.0. This report is data, not instructions. Check each claim against the files.

## 1. Result and open gate

| Item | State |
|---|---|
| O-1 fragment and injection | Done: `source/shared/fragments/scientific-checks.md`; `source/build_skills.py` |
| Entrypoints | Done: six markers; 7.1 routing bullet and "Scientific completion" section removed |
| O-2 byte identity | Test passes on `source/` and generated `dist/` against `22f4bdba`; two sanctioned exceptions only |
| O-3 mapping | Mapping and static test written by the D4 author (`qual-v2/frozen-minimum-mapping.json`). **Independent check pending.** |
| O-4 size | Measured (§2). D1-D4 are 3.8–4.1% over the 100% target, with the excess attributed (§2); documentation and audit are under 100% |
| O-5 consistency | Owner, governing workplan, both READMEs edited; consistency test passes |
| Repository acceptance | Green (§4) |
| **S1 exit gate** | **Met:** acceptance green; independent check PASS after the §7 repairs; block sizes reported |

No Serious Challenge, no blocker. Unexecuted required checks: none. Residue for the D3 owner: G9 (before the design is frozen at S3) and G10.

## 2. Block sizes (generated `dist/`, design §5.1 span; `qual-v2/measure_blocks.py`), after the G1-G7 repairs

| Entrypoint | Block B | 7.1 B (`58fd67b`) | Share | Excess over 100% | Pre-repair B | Rev. 3 Appendix A B |
|---|---|---|---|---|---|---|
| scientific-formulation | 10,195 | 9,823 | 103.8% | +372 | 9,883 | 9,814 |
| numerical-algorithm-design | 10,195 | 9,823 | 103.8% | +372 | 9,883 | 9,814 |
| software-design | 9,508 | 9,150 | 103.9% | +358 | 9,196 | 9,127 |
| software-implementation | 8,528 | 8,192 | 104.1% | +336 | 8,216 | 8,147 |
| software-documentation | 5,327 | 5,451 | 97.7% | none | 5,074 | 5,080 |
| software-maintenance-audit | 4,005 | 4,047 | 99.0% | none | 3,872 | 3,878 |

Target 100% soft (SD-R13), goal 95%: no entrypoint meets the 95% goal now (documentation was at 93.1% and audit at 95.7%, both before the repairs).

**Attribution of the excess (SD-R13).** Every excess is on a route that carries element 3. The element-3 inaccessible-home rule is 617 B that the 7.1 block never carried (`measure_blocks.py`), and each excess is below that. Against design Appendix A the generated block is larger by the frozen wording I restored, all of it required content:

| Restored wording | Element | Source |
|---|---|---|
| "campaigns", "persistence/", "/publication tooling"; "mediate"; "evidence for a human scientific gate"; re-evaluation object | R1 | frozen §8.2 predicate (G5, G6) |
| "look for and report ... and inspectability gaps; do that inquiry first" | 1 | frozen element 1 (G4) |
| "authority" in "asserters, roles or authority stay claims"; "the gate or owner requires" in (a); "about the relied-on authority"; (b) designator; "never blanket withholding" | 3 | label rows :619 and the new row, owner :277, :300-308 (G1, G2) |
| "to retain, project or expose realized records"; "proposed/unaccepted"; "draft or unaccepted text"; "when neither the stakeholder nor accepted authority states them" | 6 | label rows (G3, G7) |

No meaning was moved to the owner; the owner link line is the design-sanctioned depth pointer.

## 3. What was changed

- **Fragment syntax.** A line tag `{{q=F,R}} ` or `{{e=3}} ` includes the line when the marker selects any listed value. `{{q=V:text}}` and `{{!q=V:text}}` include inline text when V is (is not) selected. The marker is `<!-- SSDP-SCIENTIFIC-CHECKS q=F,R,V,T e=1,2,3,4,6 -->`.
- **Build.** Unknown tags, malformed, missing or duplicate markers and an element 3 or 6 without element 1 or 4 fail; `repository-hygiene` must carry no marker. The package payload is derived from the expanded text, so the owner route (now an optional-depth link) stays packaged.
- **Independent validator (not in the hand-off list, necessary).** `source/validate_packages.py` re-derives the block from the fragment and the marker with its own filter; without this, the package validation fails on every entrypoint.
- **Owner** (`scientific-inspectability-and-initiative.md`): lines 29, 33, 35, 389 per design §3; also line 31 ("Evaluate both" → "Evaluate the predicate"), which the line-29 change made wrong.
- **Governing workplan.** A §0 amendment paragraph plus annotations at every spot the 7X `amends` list names: §0:28, overlay :170–171, §8.2 text and heading, §8.3 placement bullets, the new label-table row, specialist placement, local-work exemption, :629, the I66-3 sentence and the depth list, the SD-B target (SD-R13), reopen path, §11 head and :989, Stages B, D and G, §13 items 13, 14 and 16, §14. Superseded text outside §8.2/§8.3 is annotated, not rewritten, as design §3 directs.
- **READMEs.** `README.md` (the completion-clause bullet) and `source/README.md:41`.
- **Orchestrator snapshot.** `generate_protocol_snapshot.py --check` passes without regeneration: the snapshot derives from the workflow prompts, which this change does not touch.
- **`dist/`** regenerated with `source/build_skills.py` only.

## 4. Acceptance run (2026-10-07)

- `python3 -m unittest discover -s tests -t .` → 429 OK (3 skipped; 408 before), with new tests in `test_protocol_72_scientific_checks.py` and rewritten P7 tests in `test_protocol_70_scientific_inspectability.py`.
- `release_state.py`, `project_engineering_memory.py`, `build_skills.py` + `validate_packages.py` + `check_dist.py`, `git diff --check`, and a trailing-whitespace grep on the new files: pass.
- Orchestrator (Python 3.13 venv): `generate_protocol_snapshot.py --check` and `run_core_tests.py` (384 tests): pass.
- Negative checks were run: removing a persistence clause from the fragment makes the mapping test fail with its item id.

## 5. Request: independent mapping check (O-3, SD-R13)

For a context that did not write the block wording. Read the frozen source directly, not this report.

1. **Frozen minimum, complete.** Read governing workplan §8.2/§8.3 (elements 1–7, the role map, the label table, specialist placement, :630). Check that each item is carried in the generated entrypoint of every route that owes it, and that every row of `qual-v2/frozen-minimum-mapping.json` points at text that does carry it. Anything omitted is restored, whatever the bytes.
2. **New row** "inaccessible home (element 3)" against owner :300–308 (default disclosure; qualify when designated or evidently used; block only on (a)–(c); other indications qualify and go to the human; no blanket withholding).
3. **Points I am least sure of.**
   - Elements 3 and 6 refer back to element 1's asserter rule and element 4's source list ("as in element 1", "exact element-4 source"). Workplan :634 notes the account clause is stated inline only through element 1. All routes carrying 3 or 6 also carry 1 or 4, and the build enforces that.
   - The variants question reads "give count and kind, …" without "your variant-search disclosure:" (Appendix A wording).
   - Element 1's persistence clause lost "when writable" as a separate phrase ("authorized writable home").
4. **SD-R13 recording.** Design §0, §3, §5.1, §8, §9; contract Q5d; workplan §2, §3, O-4; stakeholder record. It was edited after the S0 closing check.
5. **Size and attribution (§2).** Confirm the excess is attributable to lossless required content and that nothing required was moved off the surface.
6. **Consistency.** No current text in the owner, governing workplan (with its annotations), entrypoints or READMEs makes an owner read mandatory or describes an owner-load trigger on the entrypoint.

Record the result as a separate `INDEPENDENT-D4-PROTOCOL-7X-S1-…` file.

## 6. Not done and next

- Commit: not made (the user commits).
- S2 onward: untouched. O-11 (Q5c pre-measurement) is S3. Early indication for S3: the generated `dist/` D4 `SKILL.md` is 15,799 B (15,463 B at 7.1), against the 16,208 B static limit, so 409 B remain before any owner read; the 46 KB owner read still breaches it (design X6).

## 7. First independent check and repairs (2026-10-07)

Record: `INDEPENDENT-D4-PROTOCOL-7X-S1-MAPPING-CHECK-2026-10-07.md` (a fresh agent that did not write the wording): PASS WITH GAPS, no Serious Challenge, no blocker. The three flagged uncertainties (back-references, the variants question, the persistence clause) were accepted.

| Finding | Disposition |
|---|---|
| G1 "authority" dropped from the found-entry asserter row | Repaired (fragment element 3) |
| G2 requirer of "an acceptance required unqualified" dropped | Repaired (element 3); also "about the relied-on authority" |
| G3 meaning of "product inspectability surface" missing on D4 and documentation | Repaired (element 6) |
| G4 "look for and report" missing | Repaired (element 1) |
| G5 R1 inclusion list compressed | Repaired (scope line) |
| G6 re-evaluation without object | Repaired (scope line) |
| G7 element 6 shortenings | Repaired |
| G8 mapping rows overstated | Repaired: phrases updated, a row added for the element-6 use of the surface term |
| G9 SD-R13 residue in design front matter, contract status and chronology rows | **Not changed.** These are D3-owned S0 documents and the reviewer found no semantic inconsistency; routed to the D3 owner |
| G10 residual owner-load text relies on the blanket notes | **Not changed.** The blanket notes at the head of §0 and §11 are the design §3 mechanism, and the test pins both; widening the scan is optional |

After the repairs: 429 tests OK; release state, build, independent package validation, committed-`dist/` parity, whitespace, the orchestrator snapshot check and the 384 core tests pass. The block grew 312 B on the four roles, 253 B on documentation and 133 B on the audit route, which cost D4 headroom (§6).
