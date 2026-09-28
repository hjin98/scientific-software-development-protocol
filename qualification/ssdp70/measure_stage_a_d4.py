"""Measure the Stage A D4 entrypoint draft against an immutable 6.6 ref."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


def fenced_section(document: str, heading: str) -> str:
    after_heading = document.split(f"## {heading}\n", 1)[1]
    return after_heading.split("```text\n", 1)[1].split("\n```", 1)[0]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-ref", required=True)
    parser.add_argument("--draft", type=Path, required=True)
    parser.add_argument("--assembled", type=Path, required=True)
    args = parser.parse_args()

    base = subprocess.check_output(
        ["git", "show", f"{args.source_ref}:dist/skills/software-implementation/SKILL.md"]
    ).decode("utf-8")
    draft = args.draft.read_text(encoding="utf-8")
    description = fenced_section(draft, "Description amendment")
    route = fenced_section(draft, "Routing line — R1 and R2")
    clause = fenced_section(draft, "Completion/report clause — elements 1, 2, 3, 4 and 6")

    description_line = next(line for line in base.splitlines() if line.startswith("description: "))
    assembled = base.replace(description_line, f"description: {description}", 1)
    anchor = "A first clean local defect under sufficient authority loads none of these owners; ordinary hyperlinks and package membership are not activation commands."
    assert assembled.count(anchor) == 1
    assembled = assembled.replace(anchor, f"{route}\n\n{anchor}", 1)
    assert assembled.count("## Challenge and completion") == 1
    assembled = assembled.replace("## Challenge and completion", f"{clause}\n\n## Challenge and completion", 1)
    payload = assembled.encode("utf-8")
    args.assembled.write_bytes(payload)

    base_bytes = len(base.encode("utf-8"))
    addition_bytes = len((route + "\n\n" + clause + "\n\n").encode("utf-8"))
    description_delta = len(description.encode("utf-8")) - len(description_line.removeprefix("description: ").encode("utf-8"))
    assert len(payload) == base_bytes + addition_bytes + description_delta
    print(json.dumps({
        "source_ref": args.source_ref,
        "baseline_bytes": base_bytes,
        "description_delta_bytes": description_delta,
        "routing_added_bytes": len((route + "\n\n").encode("utf-8")),
        "element_added_bytes": {
            line.split(".", 1)[0]: len((line + "\n").encode("utf-8"))
            for line in clause.splitlines() if line[:1] in "12346" and line[1:2] == "."
        },
        "completion_added_bytes_including_heading_and_framing": len((clause + "\n\n").encode("utf-8")),
        "gross_addition_bytes": addition_bytes,
        "assembled_bytes": len(payload),
        "assembled_sha256": hashlib.sha256(payload).hexdigest(),
        "historical_t1_t8_planning_cap_bytes": 9196,
        "predeclared_margin_bytes": 512,
        "historical_t1_t8_planning_static_limit_bytes": 8684,
    }, indent=2))


if __name__ == "__main__":
    main()
