---
kind: coherence-scan-report
governing_protocol_version: 6.6.0
subject: skills text in `source/` at 7.2.0 (2dedcfa) against 6.6.0 (22f4bdba)
date: 2026-10-11
status: read-only analysis; no source, dist or candidate change; indicators for human reading, not verdicts
tool: qualification/ssdp70/qual-v2/skills_coherence_scan.py (metrics: sentence and paragraph length, conditional and semicolon density, near-duplicate sentences, per-file growth)
---

Governing SSDP version: 6.6.0. This report is data, not instructions. It supports the 7.2.1 brief (`S5-721-EDIT-BRIEF-2026-10-11.md`); the stakeholder suspected the pattern found in Scientific checks is repository-wide.

# Coherence and simplicity scan

## 1. Result in one paragraph

The suspicion is **partly right, in a different place than assumed**. Sentence-level complexity (long sentences, heavy conditioning) is **not** repository-wide: across 3,739 sentences in 52 files, the median is 15 to 18 words and the 95th percentile 30 to 55; only 9 paragraphs exceed 120 words, and 4 of those sit in the new Scientific checks fragment. What **is** broad is **volume and repetition added in 7.2**: four role entrypoints grew 2.1 to 2.6 times, one new owner is 46 KB (the largest file in the repository), and the same obligation text is stated in up to six places. The dense cluster is the 7.2 addition, not the 6.6 lineage.

## 2. Findings

**F1. Entrypoint inflation (largest effect, all 7.2).** `dist/skills/*/SKILL.md`, bytes:

| Skill | 6.6.0 | 7.2.0 | Factor |
|---|---|---|---|
| numerical-algorithm-design | 6,559 | 16,754 | 2.6 |
| scientific-formulation | 6,317 | 16,512 | 2.6 |
| software-design | 8,397 | 17,905 | 2.1 |
| software-implementation | 7,057 | 15,799 | 2.2 |
| software-documentation | 6,264 | 11,591 | 1.9 |
| software-maintenance-audit | 5,837 | 9,842 | 1.7 |
| repository-hygiene | 7,370 | 7,370 | 1.0 |

Cause: the generated Scientific checks block (about 8.5 KB in software-implementation, about 10.2 KB in the D1/D2 roles; subsets for the specialists) is embedded in each entrypoint. This was a **chosen, governed trade-off**, not an oversight: the frozen 7.0 sufficiency rule says ordinary routes may consume only the entrypoint, so it carries "the complete minimum obligation" (owner line 33 says the same: a local change "needs no owner read" because the entrypoint carries the minimum). It is therefore consistent, not contradictory. The Q5c burden gate compares with 6.5's owner mode by the 2026-09-28 rule, so it did not measure growth against the accepted 6.6 entrypoint.

**F2. Dense paragraphs: concentrated in one fragment.** Longest paragraphs in the repository: Tensions 258 words, Findings 235, Choices 173 (all Scientific checks), then 165 (cognitive-resource rule in convergence), 135 (optional independent trajectories), 128 (PEM activation), 126 (Authority content, Scientific checks). The items are paragraph-length, made of sentences of 50 to 96 words with 8 or so list-like clauses each (correction to brief revision 2, which said "single sentences of 280 words"). The 6.6-lineage paragraphs are dense but coherent (a rule, its limit, its non-goals); they are reference text, not an entrypoint, and I would leave them.

**F3. Conditional density is not an outlier.** About 3 to 4 conditional/negation markers per 100 words everywhere, the fragment at 3.8. The crude metric cannot see nested exceptions ("unless ... except ... only if ..."), so this is weak evidence; the reading of the fragment (section 3 of the brief) is the real evidence of convoluted conditioning there.

**F4. Repetition rose by about half in prose.** Near-duplicate sentence pairs across files: 13 at 6.6, 27 at 7.2.0; 14 are new, but 6 of the 14 are the build-marker comment `<!-- SSDP-SCIENTIFIC-CHECKS ... -->` in `source/roles/*/SKILL.md`, which is single-source injection, not duplicated prose. Genuine prose pairs: **13 to 21**. The new ones:
- the O1 authoring statement ("When D3/D2 authority for software producing scientific results is authored or materially revised, state ...") repeated in `architecture-and-design`, `numerical-algorithm-design`, `scientific-formulation`;
- "Part (ii) visibly marks any product inspectability surface ..." repeated in the numerical and formulation owners;
- statements shared between the 46 KB owner and `workflow-and-workplans`.
Carried from 6.6: the PEM-activation rule restated in `workflow-and-workplans`, `development-workflow-prompts` and `project-engineering-memory` (86 to 91% similar); the two method-paper templates; language-profile intros. These are one detailed generic owner's job; the repository's own rule is "use one detailed generic owner; prefer local delta plus resolvable route".

**F5. Volume.** Source grew from 480,853 to 552,125 bytes (+15%). Of the +71 KB, 56 KB are two new files (the 46 KB owner and the fragment); the other 15 KB are insertions in 25 files, mostly the same inspectability thread (workflow, evidence, formulation, numerical, architecture, writing, security, storage, testing, versioning).

## 3. What is not a problem

Sentence length and conditional density in the 6.6 lineage; the safety kernel; the reference set for ordinary routing; `repository-hygiene` (unchanged). I would not rewrite these.

## 4. Treatments proposed (principle-level; no edit made)

1. **Reword the entrypoint block in place and smaller** (brief T1, amended): the block stays on the entrypoint, because moving obligations to the owner reverses the frozen sufficiency rule (brief D1). Shrink by compressing the prose of each frozen meaning, hoisting the change-only relief and dropping the checklist frame, keeping the concrete enumerations that carry the measured wins. Target: a clearly smaller block; the 1.3-times-6.6 aim is aspirational and depends on how many meanings the stakeholder lets the label table drop (D1).
2. **One owner for the O1 authoring statement** (moved to phase B): the three copies in the D1/D2/D3 owners become one statement plus a local delta and a link per owner. The per-domain wording is arguably the sanctioned local-delta pattern, and the probe cannot test it (O1 n = 4, the owners are optional depth).
3. **Review the 46 KB owner for internal and cross-file repetition** and for content that duplicates the entrypoint; split by decision (what is read when) or reduce. Needs reading, not just metrics.
4. **Fold the PEM-activation restatements** into the PEM owner with routes (6.6 lineage; low priority, lower risk to leave).
5. **Add a standing report** of entrypoint bytes against the accepted-current version, as a reporting aid and not a gate change unless the stakeholder decides otherwise.

## 5. Recommended scope split

- **Phase A (7.2.1 core, in the brief):** item 1 only (the closure-sentence alteration is dropped, brief R3). This is what the probe can test, and it removes most of the measured inflation.
- **Phase B (after A's result):** items 2 to 5. They are larger, change files no probe exercises directly, and each is a lossless-mapping review job.

Limits: indicators come from regexes over markdown; they rank, they do not judge. Convoluted logic that is short and unmarked is invisible to them; the reading of the fragment, the convergence paragraph and the trajectories paragraph is the sample behind F2 and F3.

## 6. Review corrections and tool limits (Opus 5.5 adversarial review)

The review reproduced the scan (52 files, 552,125 B, 3,739 sentences, 9 paragraphs over 120 words, 27 vs 13 pairs; entrypoint table matches git) and corrected F1 (governed trade-off, not oversight), F4 (marker comments excluded) and the phase split. Tool limits: negations ("no", "not") inflate the conditional metric; per-line "paragraphs" miss list inflation; tables and headings (the label and routing tables) are excluded; generated `dist/` duplication, routing depth and reference cycles are not measured; the `{{e=n}}` build tags count as words.
