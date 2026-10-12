---
kind: static-premeasurement
governing_protocol_version: 6.6.0
subject: generated 7.2.0 installed D4 entrypoint (`dist/skills/software-implementation/SKILL.md`) and its owners
rule: contract v2 Q5c; design §8 (the 2026-09-28 rule, applied to 7.2.0 by SD-R12); workplan O-11
date_utc: 2026-10-07
result: NO STATIC BREACH under the rule as written; three named risks and one accounting caveat go to the stakeholder as design X6 (section 3)
---

Governing SSDP version: 6.6.0. Measurement record, data not instructions.

## 1. Rule and inputs

- **Rule.** On each of T1, T7 and T8 the candidate's median consumed bytes (6.6 `entry_and_burden` accounting: the whole installed `SKILL.md` plus SSDP files read) are at most 2.0 × the accepted 6.5 median in the same run mode, and the generated entrypoint leaves the predeclared 512 B static margin. The static pre-measurement covers the generated D4 entrypoint and every owner that 6.5 or 6.6 read on these routes, in each observed mode.
- **6.5 baseline (historical planning figures, `STAGE-A-STATIC-PREMEASUREMENT.md`; the live campaign uses fresh paired 6.5 runs).** T1 and T8 observed the entrypoint-only mode, 8,360 B. T7 observed the entrypoint-only mode (8,360 B) and the workflow-owner mode (25,188 B, a 16,828 B owner addition).
- **Candidate sizes (generated `dist/`, 7.2.0).** D4 entrypoint 15,799 B (7.1: 15,463 B; 6.6: 7,057 B). Workflow owner 20,307 B (6.6: 17,743 B). Scientific-inspectability owner 46,131 B.

## 2. Result per route and mode

| Route and mode | Candidate B | Cap = 2.0 × 6.5 median | Limit with 512 B margin | Headroom | Verdict |
|---|---|---|---|---|---|
| T1 and T8, entrypoint-only (6.5: 8,360) | 15,799 | 16,720 | 16,208 | 409 | OK |
| T7, entrypoint-only (6.5: 8,360) | 15,799 | 16,720 | 16,208 | 409 | OK |
| T7, workflow-owner mode (6.5: 25,188) | 36,106 | 50,376 | 49,864 | 13,758 | OK |

The three rows are the observed modes of the 6.5 and 6.6 runs on these routes, so the rule as written has no breach.

## 3. Risks outside the rule's enumerated modes (design X6, for the stakeholder before any campaign)

| Case | Candidate B | Limit | Over by | Why it matters |
|---|---|---|---|---|
| T1 or T8 run that also reads the scientific-inspectability owner | 61,930 | 16,208 | 45,722 | 7.2 makes the owner optional depth, but an agent that reads it on a T1/T8 run breaches the entrypoint-only cap, and a median run that reads it fails Q5c |
| T7 candidate run in workflow-owner mode against a 6.5 median in entrypoint-only mode | 36,106 | 16,208 | 19,898 | the median rule compares arms, not modes; the T7 mode-replication rule (add pairs while either arm is mixed, up to seven) and the matched-mode report exist for this |
| T7 workflow-owner mode plus the scientific-inspectability owner | 82,237 | 49,864 | 32,373 | as the first row |

The consumed-bytes count is conservative: a shell command that names the package counts every file it can reach, so one `ls` or `grep -r` of the package root counts every installed skill (about 2774 KB), and so does any command whose text merely contains `/opt` or `ssdp` (it could assemble the path); a run that only lists the package can therefore breach Q5c on accounting alone, and S4 reports the shell-counted share of each run's bytes. S4 measures the owner-read fraction on T1/T7/T8 and estimates P(Q5c pass). The headroom in the entrypoint-only mode is 409 B; any further growth of the D4 entrypoint spends it directly. Required meaning is never moved off the surface to meet this (design X6).

## 4. Reproduction

```
python3 source/build_skills.py            # regenerates dist/
wc -c dist/skills/software-implementation/SKILL.md \
      dist/skills/software-implementation/references/workflow-and-workplans.md \
      dist/skills/software-implementation/references/scientific-inspectability-and-initiative.md
```
The caps use the 6.5 figures above; 16,208 = 2 × 8,360 − 512 and 49,864 = 2 × 25,188 − 512.
