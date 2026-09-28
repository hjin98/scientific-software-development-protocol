---
kind: independent-wording-attribution-check
governing_protocol_version: 6.6.0
target_protocol_version: 7.0.0
stage: D
result: NO-PASS
---

# Stage D independent wording and attribution check — NO-PASS

**Independence and custody.** This context did not author the workplan, the candidate source or its wording. It worked read-only except for this record and read nothing under `/home/samjin/ssdp70-fixture-custody/`. Accepted 6.6 semantics were resolved from `22f4bdba53795da3a6f13f162529f3a843fc37ae`. The governing handoff was the workplan at SHA-256 `66f29437af5bde3381a66c8a7609ef3ee87b230f32c210eb7fbf1858e22d78b1`. The subject is HEAD `980ec182` plus the uncommitted working-tree entrypoint and route deltas. During this check another context changed Stage E files (`development-workflow-prompts.md`, `protocol-versioning-and-compatibility.md`, the orchestrator and tests). Those files are outside this subject and were not checked. The hashes below were re-verified unchanged at the end of the check.

**Subjects (SHA-256).** Entrypoints:

- `scientific-formulation/SKILL.md`: `d2812b3c…0402a5`
- `numerical-algorithm-design/SKILL.md`: `d524b059…d85b65`
- `software-design/SKILL.md`: `2873bcc2…c5713e`
- `software-implementation/SKILL.md`: `3ecdcf44…6f27`
- `software-documentation/SKILL.md`: `e35e0170…712a`
- `software-maintenance-audit/SKILL.md`: `b6cc80e5…fe9`
- `repository-hygiene/SKILL.md`: `17511a2f…87ca3` (unchanged from 6.6)

Owner `scientific-inspectability-and-initiative.md`: `b71daa8c…0bf29d` (46,421 B).

Deltas:

- `scientific-formulation.md`: `246cef46…6f99`
- `numerical-algorithm-design.md`: `f41f73eb…f267`
- `architecture-and-design.md`: `06a7f931…cfd6`
- `evidence-evolution-and-dependencies.md`: `8fe20778…d001d`
- `scientific-technical-writing.md`: `eb74ad7b…3406`
- `workflow-and-workplans.md`: `7a6261b7…c399a1`
- `storage-and-io.md`: `4934dacc…b053`
- `configuration-and-policy.md`: `904a4a58…414b`
- `testing-and-validation.md`: `ad94b0a9…c044c0`
- `security-and-trust-boundaries.md`: `ffc00932…be54`
- `concurrency-and-orchestration.md`: `a6a0c196…e8`
- change-plan template: `1df40936…23855`
- workplan template: `0fcd90ff…e5590`

Full hashes are reproducible with `sha256sum` on these paths.

## Findings

**SERIOUS CHALLENGE:** none.

**BLOCKING (fix before the Stage F freeze)**

- **B1. Element 5 drops the marking duty.** The entrypoints for `scientific-formulation` and `numerical-algorithm-design` say "an agent's assessment stays proposed until the revision's acceptance considers it".
  - Frozen element 5 says "an agent's assessment **marked** proposed until the revision's acceptance considers it". §8.3 consumed-surface sufficiency repeats "an agent's assessment marked proposed (element 5)".
  - "Stays proposed" states a status. It does not require the record or the gate evidence to show that status visibly. A gate could therefore receive an unmarked agent assessment (§6.6).
  - The owner's "stays proposed" follows §6.4 and is fine. On the consumed surface, however, the element is weakened.
  - Minimal fix: "an agent's assessment is marked proposed until …" (about +4 B). No other wording needs to change.

**MINOR**

- **m1. Non-required example in element 5 (43 B).** "(for D1, the D2 authority concretizing it)" is an owner example from §6.4. It is outside frozen element 5 and outside the label table. Remove it, or add it to the label table through a governed change.
- **m2. Element 5 narrows the asserter explanation.** The parenthetical "(the committing account does not show this)" is narrower than the row "the account or identity it is written or committed through does not show this". The operative duty to state the asserter in the record's content is intact. Suggested wording: "(the writing or committing account does not show this)".
- **m3. The owner restates the workflow owner's Channel C contract.** Its "Human gate evidence" section lists the Channel C contract that §3.2 assigns to the workflow owner as a REFINES row. The owner does say the contract "lives in the workflow owner", and nothing contradicts it. The summary is weaker, though: it omits "including those marked inapplicable" and "mere reachability … does not satisfy". Reducing it to a route would remove a drift risk. The inquiry-status bullet repeats the evidence delta in the same way. Stage G should confirm that neither is a second definition.
- **m4. Owner omissions.**
  - §6.2.1 "A human's exploratory choice may be unaccepted" is dropped. "Separate dimensions" implies it only implicitly.
  - The non-goals omit "profile schema" and "implement the Protocol 8 deterministic orchestrator" from §9.
- **m5. List numbering differs when rendered.** Numbered items with gaps (1, 4, 6) render as 1, 2, 3 in Markdown. The raw text is correct, and §8.3 permits non-reproduced order.

**Verified**

- All seven element texts, R1/R2 and the heading are byte-identical across the entrypoints that carry them. The D4 additions are byte-identical to the Stage A checked draft.
- Placement is as frozen:
  - elements 1–4 and 6 in all four roles;
  - element 5 only in D1/D2;
  - element 7 only in D1/D2/D3;
  - documentation carries R1/R2 and elements 1, 4 and 6;
  - audit carries R1/R2 and elements 1 and 4;
  - hygiene carries nothing.
- No 6.6 body text was removed or reworded (0 lines per the measurement script). The only 6.6 wording change is the D4 description.
- "The predicate above" and "the clause below" resolve in every entrypoint. The specialists' routing lines are unbulleted prose, which matches their routing paragraphs.
- Element 7 carries all frozen parts: the material-realized-record row and the product-inspectability-surface row inline, "None material" and "agent reports only/None", the acceptance-review checks (unmarked requirements, wrongly classified marks), and the O3 limit ("binds only after the stakeholder or task authority accepts it").
- Element 5 carries the applicability-assessment row, predecessor identity, record plus gate evidence, and the content-stated human/AI/which-agent asserter. Its "also search" relies on element 3's identity search, which is present on both D1/D2 routes, as the frozen text does.
- §8.2 predicate and trigger are verbatim in the owner. The §15 route-limitation bounds and adoption are all present.
- The D1/D2/D3 deltas carry §7 fully and route O1 to the owner. The evidence, writing and workflow deltas and the templates match §3.2 and Stage C. The five one-line routes add no parallel definition.

## Gross additions (generated, vs 6.6 `22f4bdba` dist; version stamp and description excluded)

| Entrypoint | R1+R2 | Head | E1 | E2 | E3 | E4 | E5 | E6 | E7 | Blank | Total | Desc Δ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| scientific-formulation | 950 | 83 | 2070 | 764 | 1396 | 510 | 687 | 1403 | 957 | 9 | 8829 | 0 |
| numerical-algorithm-design | 950 | 83 | 2070 | 764 | 1396 | 510 | 687 | 1403 | 957 | 9 | 8829 | 0 |
| software-design | 950 | 83 | 2070 | 764 | 1396 | 510 | – | 1403 | 957 | 8 | 8141 | 0 |
| software-implementation | 950 | 83 | 2070 | 764 | 1396 | 510 | – | 1403 | – | 7 | 7183 | +91 |
| software-documentation | 948 | 83 | 2070 | – | – | 510 | – | 1403 | – | 5 | 5019 | 0 |
| software-maintenance-audit | 948 | 83 | 2070 | – | – | 510 | – | – | – | 4 | 3615 | 0 |
| repository-hygiene | – | – | – | – | – | – | – | – | – | – | 0 | 0 |

**Attribution of the newly checked elements.**

- E5 sentences:
  - search (185 B): e5, including the 43 B non-required example (m1);
  - record plus assessment (281 B): e5 plus the applicability row;
  - asserter plus proposed status (215 B): e5 plus the written-record asserter row (see B1 and m2).
- E7 sentences:
  - authoring (596 B): e7 plus the material-realized-record and product-inspectability-surface rows;
  - acceptance review (356 B): e7 plus the O3 limit.

Every total exceeds the 1,000 B SD-B target. Apart from m1 (43 B), the excess is attributable to lossless required elements, R1/R2 and the label meanings they use.

Generated D4 entrypoint: 14,331 B. The backstop disposition belongs to the stakeholder records and is not assessed here.

Measured with `source/build_skills.py` into a scratch dir, then `measure_entrypoint_additions.py` (`59a571a0…`).

**Owner size.** The owner is 46.4 KB, against about 47 KB of workplan doctrine. It is a close compression of §3.1, §4–§7, §8.2, §9–§10 and §15, and it is not disproportionate. The only clearly redundant text is the m3 restatement (about 0.7 KB).

## Disposition

NO-PASS on B1 alone. It is a one-word repair to element 5 in two role entrypoints. After that repair, and ideally m1 and m2, the losslessness and attribution check can be re-confirmed by a narrow recheck of element 5 only. The minor findings do not block the Stage F freeze. They are recorded for the author and for Stage G.
