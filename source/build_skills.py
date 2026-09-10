#!/usr/bin/env python3
"""Build portable skill directory bundles and ZIPs from canonical protocol source."""

from __future__ import annotations

import argparse
import json
import re
import urllib.parse
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SHARED = ROOT / "shared"
ROLES = ROOT / "roles"
SPECIALISTS = ROOT / "specialists"
PROTOCOL_VERSION = (ROOT / "PROTOCOL_VERSION").read_text(encoding="utf-8").strip()

ROLE_SPECS = {
    "scientific-formulation": {"role": "d1-scientific-formulation"},
    "numerical-algorithm-design": {"role": "d2-numerical-algorithm-design"},
    "software-design": {"role": "d3-software-design"},
    "software-implementation": {"role": "d4-software-implementation"},
}

SPECIALIST_SPECS = {
    "software-documentation": {"specialty": "documentation"},
    "repository-hygiene": {"specialty": "repository-hygiene"},
    "software-maintenance-audit": {"specialty": "maintenance-audit"},
}

DIRECT_ROUTE_RE = re.compile(r"\]\((?P<kind>references|templates)/(?P<name>[A-Za-z0-9_.-]+\.md)\)")
LOCAL_MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
URI_SCHEME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")


def _direct_payload(root: Path, skill_name: str) -> tuple[list[str], list[str]]:
    """Derive package payload directly from the skill's explicit Markdown routes."""
    text = (root / skill_name / "SKILL.md").read_text(encoding="utf-8")
    references: list[str] = []
    templates: list[str] = []
    for match in DIRECT_ROUTE_RE.finditer(text):
        target = references if match.group("kind") == "references" else templates
        name = match.group("name")
        if name not in target:
            target.append(name)
    return references, templates


for _name, _spec in ROLE_SPECS.items():
    _spec["references"], _spec["templates"] = _direct_payload(ROLES, _name)
for _name, _spec in SPECIALIST_SPECS.items():
    _spec["references"], _spec["templates"] = _direct_payload(SPECIALISTS, _name)


NAME_RE = re.compile(r"(?m)^name:\s*([a-z0-9]+(?:-[a-z0-9]+)*)\s*$")


def skill_root(skill_name: str, kind: str) -> Path:
    if kind == "role":
        return ROLES / skill_name
    if kind == "specialist":
        return SPECIALISTS / skill_name
    raise ValueError(f"unknown skill kind: {kind!r}")



def _transitive_payload(spec: dict) -> list[tuple[str, Path]]:
    'Return the finite local-Markdown closure of direct SKILL activation seeds.'
    seeds = [
        *[(f"references/{name}", SHARED / "references" / name) for name in spec["references"]],
        *[(f"templates/{name}", SHARED / "templates" / name) for name in spec["templates"]],
    ]
    shared_root = SHARED.resolve()
    found: dict[str, Path] = {}
    queue = list(seeds)
    while queue:
        rel, src = queue.pop(0)
        if rel in found:
            continue
        if not src.is_file():
            raise SystemExit(f"missing package source: {src}")
        found[rel] = src
        text = src.read_text(encoding="utf-8")
        for raw_target in LOCAL_MARKDOWN_LINK_RE.findall(text):
            target = raw_target.strip()
            if not target or target.startswith("#"):
                continue
            decoded = urllib.parse.unquote(target)
            if URI_SCHEME_RE.match(decoded) or decoded.startswith("//"):
                continue
            path_part = decoded.split("#", 1)[0].split("?", 1)[0]
            if not path_part or not path_part.lower().endswith(".md"):
                continue
            if decoded != target:
                raise SystemExit(f"encoded local Markdown package route is not allowed: {src}: {target}")
            resolved = (src.parent / path_part).resolve()
            try:
                shared_rel = resolved.relative_to(shared_root)
            except ValueError as exc:
                raise SystemExit(f"local Markdown package route escapes shared root: {src}: {target}") from exc
            if not shared_rel.parts or shared_rel.parts[0] not in {"references", "templates"}:
                raise SystemExit(f"local Markdown package route is outside packageable roots: {src}: {target}")
            next_rel = shared_rel.as_posix()
            if next_rel not in found:
                queue.append((next_rel, resolved))
    return list(found.items())

def entries(skill_name: str, spec: dict, kind: str) -> list[tuple[str, Path]]:
    skill = skill_root(skill_name, kind)
    out = [
        ("SKILL.md", skill / "SKILL.md"),
        ("agents/openai.yaml", skill / "agents" / "openai.yaml"),
        ("PROTOCOL_VERSION", ROOT / "PROTOCOL_VERSION"),
    ]
    out += _transitive_payload(spec)
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
