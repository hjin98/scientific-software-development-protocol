#!/usr/bin/env python3
"""Build portable skill directory bundles and ZIPs from canonical protocol source."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SHARED = ROOT / "shared"
ROLES = ROOT / "roles"
SPECIALISTS = ROOT / "specialists"
PROTOCOL_VERSION = (ROOT / "PROTOCOL_VERSION").read_text(encoding="utf-8").strip()

CORE = [
    "workflow-and-workplans.md",
    "testing-and-validation.md",
    "protocol-versioning-and-compatibility.md",
]
FOUNDATION = ["abstraction-and-realization.md"]
ROLE_CONDITIONAL = [
    "convergence-and-cycle-economy.md",
    "long-horizon-code-health.md",
]
LANGUAGE_PROFILES = [
    "language-profiles.md",
    "python-engineering.md",
    "cpp-engineering.md",
]
TOOL_METHODS = [
    "tool-assisted-engineering.md",
    "tool-serena.md",
    "tool-semgrep.md",
    "tool-hypothesis.md",
    "tool-codeql.md",
]
CROSS_CUTTING = [
    "configuration-and-policy.md",
    "concurrency-and-orchestration.md",
    "security-and-trust-boundaries.md",
]
ENGINEERING_FITNESS = [
    "performance-and-parallelism.md",
    "storage-and-io.md",
    "scientific-software.md",
]

ROLE_SPECS = {
    "scientific-formulation": {
        "role": "d1-scientific-formulation",
        "references": FOUNDATION + CORE + [
            "scientific-formulation.md",
            "scientific-software.md",
            "scientific-technical-writing.md",
            "documentation-and-evidence.md",
        ],
        "templates": [
            "abstraction_realization_change_plan_template.md",
            "scientific_method_paper_template.md",
        ],
    },
    "numerical-algorithm-design": {
        "role": "d2-numerical-algorithm-design",
        "references": FOUNDATION + CORE + [
            "numerical-algorithm-design.md",
            "scientific-software.md",
            "performance-and-parallelism.md",
        ],
        "templates": [
            "abstraction_realization_change_plan_template.md",
            "numerical_algorithmic_method_paper_template.md",
        ],
    },
    "software-design": {
        "role": "d3-software-design",
        "references": FOUNDATION + CORE + ROLE_CONDITIONAL + LANGUAGE_PROFILES + [
            "architecture-and-design.md",
            "scientific-formulation.md",
            "numerical-algorithm-design.md",
            "documentation-and-evidence.md",
            "specification-and-implementation.md",
            "release-and-distribution.md",
            "repository-intake.md",
        ] + TOOL_METHODS + CROSS_CUTTING + ENGINEERING_FITNESS,
        "templates": [
            "implementation_workplan_template.md",
            "abstraction_realization_change_plan_template.md",
        ],
    },
    "software-implementation": {
        "role": "d4-software-implementation",
        "references": FOUNDATION + CORE + ROLE_CONDITIONAL + LANGUAGE_PROFILES + [
            "architecture-and-design.md",
            "scientific-formulation.md",
            "numerical-algorithm-design.md",
            "debugging-and-state-recovery.md",
            "documentation-and-evidence.md",
            "specification-and-implementation.md",
            "release-and-distribution.md",
            "repository-intake.md",
            "git-and-version-control.md",
        ] + TOOL_METHODS + CROSS_CUTTING + ENGINEERING_FITNESS,
        "templates": [],
    },
}

SPECIALIST_SPECS = {
    "software-documentation": {
        "specialty": "documentation",
        "references": CORE + [
            "architecture-and-design.md",
            "documentation-and-evidence.md",
            "documentation-maintenance.md",
            "scientific-technical-writing.md",
            "specification-and-implementation.md",
            "release-and-distribution.md",
            "security-and-trust-boundaries.md",
        ] + ENGINEERING_FITNESS,
        "templates": [],
    },
    "repository-hygiene": {
        "specialty": "repository-hygiene",
        "references": CORE + [
            "git-and-version-control.md",
            "documentation-and-evidence.md",
            "release-and-distribution.md",
            "repository-intake.md",
            "security-and-trust-boundaries.md",
            "storage-and-io.md",
        ],
        "templates": [],
    },
    "software-maintenance-audit": {
        "specialty": "maintenance-audit",
        "references": CORE + [
            "long-horizon-code-health.md",
            "architecture-and-design.md",
            "git-and-version-control.md",
            "repository-intake.md",
            "tool-assisted-engineering.md",
            "convergence-and-cycle-economy.md",
            "documentation-and-evidence.md",
            "scientific-software.md",
        ],
        "templates": [],
    },
}

NAME_RE = re.compile(r"(?m)^name:\s*([a-z0-9]+(?:-[a-z0-9]+)*)\s*$")


def skill_root(skill_name: str, kind: str) -> Path:
    if kind == "role":
        return ROLES / skill_name
    if kind == "specialist":
        return SPECIALISTS / skill_name
    raise ValueError(f"unknown skill kind: {kind!r}")


def entries(skill_name: str, spec: dict, kind: str) -> list[tuple[str, Path]]:
    skill = skill_root(skill_name, kind)
    out = [
        ("SKILL.md", skill / "SKILL.md"),
        ("agents/openai.yaml", skill / "agents" / "openai.yaml"),
        ("PROTOCOL_VERSION", ROOT / "PROTOCOL_VERSION"),
    ]
    out += [(f"references/{name}", SHARED / "references" / name) for name in spec["references"]]
    out += [(f"templates/{name}", SHARED / "templates" / name) for name in spec["templates"]]
    return out


def validate_registry(root: Path, specs: dict, kind: str) -> None:
    actual = {
        p.name
        for p in root.iterdir()
        if p.is_dir() and (p / "SKILL.md").is_file()
    } if root.is_dir() else set()
    expected = set(specs)
    if actual != expected:
        raise SystemExit(f"{kind} registry mismatch: expected={sorted(expected)} actual={sorted(actual)}")

    for skill_name, spec in specs.items():
        skill = skill_root(skill_name, kind) / "SKILL.md"
        match = NAME_RE.search(skill.read_text(encoding="utf-8"))
        if match is None or match.group(1) != skill_name:
            raise SystemExit(f"{skill}: frontmatter name mismatch")
        for _, path in entries(skill_name, spec, kind):
            if not path.is_file():
                raise SystemExit(f"missing package source: {path}")


def validate() -> None:
    if not re.fullmatch(r"\d+\.\d+\.\d+", PROTOCOL_VERSION):
        raise SystemExit(f"invalid protocol version: {PROTOCOL_VERSION!r}")
    validate_registry(ROLES, ROLE_SPECS, "role")
    validate_registry(SPECIALISTS, SPECIALIST_SPECS, "specialist")


def build_one(skill_name: str, spec: dict, kind: str, stage: Path) -> Path:
    root = stage / skill_name
    root.mkdir(parents=True, exist_ok=True)
    for rel, src in entries(skill_name, spec, kind):
        dst = root / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        text = src.read_text(encoding="utf-8").replace(
            "REPLACE_WITH_SKILL_PROTOCOL_VERSION", PROTOCOL_VERSION
        )
        dst.write_text(text, encoding="utf-8")

    manifest = {"protocol_version": PROTOCOL_VERSION, "skill_name": skill_name}
    if kind == "role":
        manifest["role"] = spec["role"]
    else:
        manifest["kind"] = "specialist"
        manifest["specialty"] = spec["specialty"]
    (root / "protocol-manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return root


def zip_tree(src_root: Path, zip_path: Path) -> None:
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        base = src_root.parent
        for path in sorted(p for p in src_root.rglob("*") if p.is_file()):
            zf.write(path, path.relative_to(base).as_posix())


def all_specs() -> list[tuple[str, dict, str]]:
    return [
        *[(name, spec, "role") for name, spec in ROLE_SPECS.items()],
        *[(name, spec, "specialist") for name, spec in SPECIALIST_SPECS.items()],
    ]


def build(output: Path) -> None:
    validate()
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    skills_output = output / "skills"
    skills_output.mkdir()

    for skill_name, spec, kind in all_specs():
        root = build_one(skill_name, spec, kind, skills_output)
        zip_tree(root, output / f"{skill_name}.zip")

    all_names = [name for name, _, _ in all_specs()]
    (output / "BUILD_INDEX.json").write_text(
        json.dumps(
            {
                "protocol_version": PROTOCOL_VERSION,
                "runtime_root": "skills",
                "skills": all_names,
                "lifecycle_roles": list(ROLE_SPECS),
                "specialists": list(SPECIALIST_SPECS),
            },
            indent=2,
            sort_keys=True,
        ) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT.parent / "dist")
    args = parser.parse_args()
    build(args.output.resolve())
    for skill_name, _, _ in all_specs():
        print(args.output.resolve() / "skills" / skill_name)
        print(args.output.resolve() / f"{skill_name}.zip")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
