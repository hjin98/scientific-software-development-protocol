"""Measure Protocol 7 generated entrypoint additions against the immutable 6.6 dist (evidence tooling).

Gross added bytes are the generated lines absent from the 6.6 generated entrypoint, excluding the
version stamp and description line, which are reported separately (SD-B target accounting, workplan
section 8.3). Each added block is attributed to R1/R2 (routing line), the clause heading, or its
numbered element. The delegate-request block (Protocol 7.1) holds the relocated delegate-request
sentences of elements 1-3, so each of its lines is attributed to the element whose sentences it carries:
the lead line, Findings and Realized-results questions to element 1, Variants to element 2, Tensions to
element 3, and the gap rule to elements 1 and 2 together (it carries both elements' unanswered-part
rules). The per-element SD-B attribution is confirmed by a context that did not author the wording.
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import subprocess
from pathlib import Path

SKILLS = (
    "scientific-formulation",
    "numerical-algorithm-design",
    "software-design",
    "software-implementation",
    "software-documentation",
    "software-maintenance-audit",
    "repository-hygiene",
)
VERSION_RE = re.compile(r"\b\d+\.\d+\.\d+\b")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-ref", required=True)
    parser.add_argument("--dist", type=Path, required=True, help="generated skills root (dist/skills)")
    args = parser.parse_args()
    report = {}
    for name in SKILLS:
        base = subprocess.check_output(["git", "show", f"{args.base_ref}:dist/skills/{name}/SKILL.md"]).decode()
        new = (args.dist / name / "SKILL.md").read_text(encoding="utf-8")
        norm = lambda text: VERSION_RE.sub("X.Y.Z", text)  # noqa: E731
        base_lines, new_lines = norm(base).splitlines(keepends=True), norm(new).splitlines(keepends=True)
        added, removed = [], []
        for op, i1, i2, j1, j2 in difflib.SequenceMatcher(a=base_lines, b=new_lines, autojunk=False).get_opcodes():
            if op in {"replace", "delete"}:
                removed += base_lines[i1:i2]
            if op in {"replace", "insert"}:
                added += new_lines[j1:j2]
        desc_new = next((line for line in added if line.startswith("description: ")), None)
        desc_old = next((line for line in removed if line.startswith("description: ")), None)
        body_removed = [line for line in removed if not line.startswith("description: ")]
        attribution: dict[str, int] = {}
        for line in added:
            if line.startswith("description: "):
                continue
            if line.startswith("- scientific inspectability ->") or line.startswith("scientific inspectability ->"):
                key = "R1+R2 routing line"
            elif line.startswith("## Scientific completion"):
                key = "clause heading"
            elif line.startswith(("**When you delegate.**", "- **Findings", "- **Realized results")):
                key = "element 1 (delegate block)"
            elif line.startswith("- **Variants"):
                key = "element 2 (delegate block)"
            elif line.startswith("- **Tensions"):
                key = "element 3 (delegate block)"
            elif line.startswith("Report each part the delegate leaves unanswered"):
                key = "elements 1+2 (delegate block gap rule)"
            elif re.match(r"^[1-7]\. ", line):
                key = f"element {line[0]}"
            else:
                key = "framing (blank lines)" if not line.strip() else "UNATTRIBUTED"
            attribution[key] = attribution.get(key, 0) + len(line.encode())
        report[name] = {
            "base_bytes": len(base.encode()),
            "generated_bytes": len(new.encode()),
            "gross_added_bytes_excluding_description": sum(attribution.values()),
            "description_delta_bytes": (len(desc_new.encode()) - len(desc_old.encode())) if desc_new and desc_old else 0,
            "removed_or_reworded_body_lines": len(body_removed),
            "attribution_bytes": dict(sorted(attribution.items())),
        }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
