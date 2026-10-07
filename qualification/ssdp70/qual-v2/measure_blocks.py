#!/usr/bin/env python3
"""Measure each generated Scientific checks block against its Protocol 7.1 block (workplan 7X O-4, SD-R13).

Span (design section 5.1): the UTF-8 bytes, newlines included, of the lines the generated
`dist/skills/<name>/SKILL.md` adds relative to the `22f4bdba` generated entrypoint, excluding the
front-matter `description:` line and the generated `**Governing version.**` line. The 7.1 reference is
the same measure at `58fd67b`. The target is 100% (soft, SD-R13) and 95% is the goal; losslessness is
the hard condition, so any excess over 100% must be attributable to required content the 7.1 block
did not carry: the element-3 inaccessible-home rule (the one new label-table row). Per-part bytes
attribute the block to scope, delegate lines, the gap rule and each element.
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import subprocess
from pathlib import Path

ACCEPTED_66 = "22f4bdba53795da3a6f13f162529f3a843fc37ae"
SKILLS_WITH_BLOCK = (
    "scientific-formulation",
    "numerical-algorithm-design",
    "software-design",
    "software-implementation",
    "software-documentation",
    "software-maintenance-audit",
)
REFERENCE_71_BYTES = {  # `58fd67b`, same span
    "scientific-formulation": 9823,
    "numerical-algorithm-design": 9823,
    "software-design": 9150,
    "software-implementation": 8192,
    "software-documentation": 5451,
    "software-maintenance-audit": 4047,
}
NEW_REQUIRED_RE = re.compile(r"An inaccessible or unsearchable home.*?never blanket withholding\.")
GOVERNING_LINE = "**Governing version.**"


def added_lines(base: str, new: str) -> list[str]:
    base_lines, new_lines = base.splitlines(keepends=True), new.splitlines(keepends=True)
    added: list[str] = []
    for op, _, _, j1, j2 in difflib.SequenceMatcher(a=base_lines, b=new_lines, autojunk=False).get_opcodes():
        if op in {"replace", "insert"}:
            added += new_lines[j1:j2]
    return [line for line in added if not line.startswith(("description:", GOVERNING_LINE))]


def part(line: str) -> str:
    stripped = line.strip()
    if not stripped:
        return "framing (blank lines)"
    if stripped.startswith("## Scientific checks"):
        return "framing (heading)"
    if stripped.startswith("**Scope.**"):
        return "scope and depth line (R1, R2)"
    if stripped.startswith("**If you delegate**"):
        return "delegate lead"
    if stripped.startswith('- "Report your'):
        return "delegate question F (findings)"
    if stripped.startswith('- "Did your work, including any tools or agents you launched, produce'):
        return "delegate question R (realized results)"
    if stripped.startswith('- "Did your work, including any tools or agents you launched, evaluate'):
        return "delegate question V (variants)"
    if stripped.startswith("- Only if it relies"):
        return "delegate question T (tensions)"
    if stripped.startswith("Report each unanswered part"):
        return "gap rule"
    if stripped.startswith("**Before you finish"):
        return "framing (element lead)"
    match = re.match(r"^([1-7])\. ", stripped)
    return f"element {match.group(1)}" if match else "UNATTRIBUTED"


def measure(dist_skills: Path, base_ref: str = ACCEPTED_66) -> dict:
    report: dict = {}
    for name, reference in REFERENCE_71_BYTES.items():
        base = subprocess.check_output(["git", "show", f"{base_ref}:dist/skills/{name}/SKILL.md"]).decode("utf-8")
        added = added_lines(base, (dist_skills / name / "SKILL.md").read_text(encoding="utf-8"))
        parts: dict[str, int] = {}
        for line in added:
            parts[part(line)] = parts.get(part(line), 0) + len(line.encode())
        total = sum(parts.values())
        new_required = sum(len(m.group(0).encode()) for m in NEW_REQUIRED_RE.finditer("".join(added)))
        report[name] = {
            "block_bytes": total,
            "reference_71_bytes": reference,
            "share_percent": round(100 * total / reference, 1),
            "excess_over_100_percent": max(0, total - reference),
            "new_required_content_bytes": new_required,
            "bytes_to_95_percent_goal": max(0, total - int(0.95 * reference)),
            "parts": parts,
        }
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--dist", type=Path, required=True, help="generated skills root (dist/skills)")
    parser.add_argument("--base-ref", default=ACCEPTED_66)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = measure(args.dist, args.base_ref)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
        return
    print(f"{'entrypoint':30s} {'block B':>8s} {'7.1 B':>7s} {'share':>7s} {'excess':>7s} {'new-required B':>15s}")
    for name, row in report.items():
        print(f"{name:30s} {row['block_bytes']:8d} {row['reference_71_bytes']:7d} {row['share_percent']:6.1f}% "
              f"{row['excess_over_100_percent']:7d} {row['new_required_content_bytes']:15d}")


if __name__ == "__main__":
    main()
