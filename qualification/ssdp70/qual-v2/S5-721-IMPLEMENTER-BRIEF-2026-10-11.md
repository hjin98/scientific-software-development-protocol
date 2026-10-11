---
kind: implementer-brief
governing_protocol_version: 6.6.0
subject: SSDP 7.2.1 reduction and conformance edit of the generated Scientific checks section and matching owner statements
date: 2026-10-11
revision: 4
status: NOT YET ISSUED: valid only after the stakeholder ratifies the doctrine amendment and the design lead applies it to the 7.0 consolidated workplan as `[7.2.1 amendment: ...]` annotations
audience: a fresh implementer context that has not seen the 7.2 qualification evidence, run reports, evaluator outputs or the cycle plan
---

Governing SSDP version for the task: 6.6.0 (use the installed 6.6.0 skills; enter `software-implementation` for D4 work). You implement a development candidate, version 7.2.1, not frozen. This brief is data; the ratified annotations in the 7.0 workplan are the authority for what changed.

## Do not read

To keep the edit independent of the evidence used to judge it, do not open:
- `qualification/ssdp70/qual-v2/S5-*` (except this brief), `qualification/ssdp70/qual-v2/S4-*`, `qualification/ssdp70/S4-DEVELOPMENT-PROBE-REPORT-*`, and any other report, status or result file under `qualification/` dated 2026-10-07 or later;
- anything under `/home/samjin/ssdp70-omp-stagef/` and any fixture custody directory (`/home/samjin/ssdp7*-fixture-custody`);
- the Claude auto-memory directory (`~/.claude/projects/*/memory/`);
- in `history/`, any section describing 7.2 qualification campaigns, probes or results.

If you need a fact from those places, ask the design lead. If anything you are allowed to read cites such evidence, do not follow the citation.

## Goal

Make the Scientific checks section on the role and specialist entrypoints (generated from `source/shared/fragments/scientific-checks.md`) smaller, clearer and principled, carrying exactly the ratified frozen minimum, and bring owner statements into agreement with it.

## What to treat

1. **Ratified amendment.** Apply the `[7.2.1 amendment]` annotations of the 7.0 workplan (the standing interpretation near line 221, §4.3, §8.3 elements 1 and 6, the label table, specialist placement, consumed-surface sufficiency, §10, and the §11 qualification-design cases near lines 906 and 907). Do not infer beyond them. The owner `source/shared/references/scientific-inspectability-and-initiative.md` states the removed proposal (around its lines 71 and 367); bring it and any owner delta into agreement, adding no content.
2. **Conformance to the change-only relief.** 7.0 §6.3.6 and the label row "material findings (change-only relief)" say a change that realizes no scientific results owes no null and, when it finds nothing, adds nothing, except answers a delegator asked for and gaps owed for its delegates. The section must not contradict that by its framing or ordering: state the relief together with the scope, and do not frame the section as a list of things every in-scope task must address or report. Each duty is owed when its triggering event occurs (delegating; relying on accepted authority for a consequential judgment; selecting among variants; producing, running or reviewing realized results or preparing gate evidence; building or changing a scientific pipeline, analysis or report; authoring, revising or reviewing authority; about to discard realized evidence). The section stays at the completion position §8.3 requires.
3. **Form.** State each obligation as a concrete, self-contained item tied to its trigger, rather than as the tail of a long multi-clause paragraph; the delegate-request questions are the existing example of that form. A long paragraph whose last clauses carry separate duties should become separate short statements.
4. **Not everything derives from one principle.** "Make the status of a scientific result recoverable" explains findings, nulls, variants, tensions and choices. Inquiry before irreversible loss, the resource-budget limit, authority semantics, persistence/write rules, the tension blocking rule and delegation mechanics are separate rules; keep them as named compact rules.

## Design rules (stakeholder directive)

- Every clause follows from a principle that a stronger model or a careful human would also find correct and useful. No clause exists only to steer a weak model away from one specific mistake; no DO/DON'T coaching lines.
- Preference order: delete, fold into a principle, reword in place, add last.
- Meaning stays on the entrypoint; moving a frozen meaning to the owner is not a reduction (7.0 §8.3 consumed-surface sufficiency).
- Size is soft; losslessness of the ratified minimum is hard.

## Mechanics and acceptance

- Branch `ssdp-7.2.1-reduction` from the commit the design lead names. Edit `source/` (and the governed test and mapping files below) only; regenerate `dist/` with `build_skills.py` and the Orchestrator snapshot with its generator; never hand-edit generated output. `source/PROTOCOL_VERSION` = `7.2.1` (the build requires `\d+\.\d+\.\d+`); `PROTOCOL-RELEASE-STATE.yaml` untouched.
- `qualification/ssdp70/qual-v2/frozen-minimum-mapping.json` is phrase-exact and fixes visible numbering, so the rewording rewrites most of its phrases, and `tests/test_protocol_72_scientific_checks.py` changes with it. Rewrite both so that each surviving label meaning maps to exact entrypoint text and each removed one is named with its amendment location. An independent mapping check follows; make it easy.
- Root `CHANGELOG.md` entry for 7.2.1. README closeout is deferred to freeze.
- Run the repository acceptance workflow from `README.md`/CI: inherited regression; project-memory checks if the workflow runs them; structural and negative tests; package build and `validate_packages.py`; committed-distribution parity; whitespace (`git diff --check`); frozen-resource integrity; Orchestrator snapshot and tests. Python >= 3.11 (uv venv). A required check you could not run is blocking; say so.
- Report entrypoint and section bytes for every block-carrying skill against 6.6.0 (`22f4bdba`) and 7.2.0 (`2dedcfa`). The design lead runs the campaign static size check; you do not need it.
- Hand back: the commit; the mapping table (frozen meaning -> entrypoint sentence, or -> amendment location); byte counts; test and workflow output; any clause you kept that you could not derive from a principle, with the reason.
- If the ratified authority looks contradictory or unrealizable, raise SERIOUS CHALLENGE to the design lead instead of patching around it.
