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

# The entry contract is owned by the kernel's "Pre-routing safety kernel" block and the
# versioning owner's marked entry step; the build inlines only those two into every entrypoint
# at ENTRY_PLACEHOLDER so the surface a portable runtime actually consumes carries them. The
# rest of the universal kernel stays a conditional owner, routed by KERNEL_ROUTE: its predicate
# is identical for every skill, so it is generated here once instead of copied per skill.
ENTRY_PLACEHOLDER = "<!-- SSDP-ENTRY-CONTRACT -->"
ENTRY_REFERENCES = ("abstraction-and-concretization.md", "protocol-versioning-and-compatibility.md")
VERSION_STEP_RE = re.compile(r"<!-- ssdp-entry-version-step:begin -->\n(.*?)\n<!-- ssdp-entry-version-step:end -->", re.S)
INVARIANT_RE = re.compile(r"^## Pre-routing safety kernel\n.*?^```text\n(.*?)^```", re.S | re.M)
SIBLING_LINK_RE = re.compile(r"\]\(([A-Za-z0-9_.-]+\.md)\)")
KERNEL_ROUTE = (
    "**Pre-routing safety kernel** ([universal kernel](references/abstraction-and-concretization.md) owns it and"
    " any materiality, authority/delegation, simplicity, proportional-rigor, verification/Challenge,"
    " representation or SSDP self-development question):"
)


def entry_contract(kernel: str, versioning: str) -> str:
    step, invariant = VERSION_STEP_RE.search(versioning), INVARIANT_RE.search(kernel)
    if step is None or invariant is None:
        raise SystemExit("entry contract owners lack the version step markers or the pre-routing safety kernel block")
    return (
        "## Entry contract\n\n"
        + SIBLING_LINK_RE.sub(r"](references/\1)", step.group(1))
        + "\n\n" + KERNEL_ROUTE + "\n\n```text\n"
        + invariant.group(1)
        + "```"
    )


# The scientific checks section is generated from one tagged fragment. An entrypoint carries
# CHECKS_MARKER with the delegate questions (q) and elements (e) its role map assigns; the build
# injects exactly those fragment lines at the marker, so the six blocks cannot drift. A line tag
# `{{q=F,R}} ` or `{{e=3}} ` includes the line when the marker selects any listed value; an inline
# `{{q=V:text}}` (or `{{!q=V:text}}`) includes text only when V is (is not) selected.
CHECKS_MARKER = "<!-- SSDP-SCIENTIFIC-CHECKS"
CHECKS_MARKER_RE = re.compile(r"<!-- SSDP-SCIENTIFIC-CHECKS q=([A-Z](?:,[A-Z])*) e=([0-9](?:,[0-9])*) -->")
CHECKS_FRAGMENT = SHARED / "fragments" / "scientific-checks.md"
CHECKS_QUESTIONS = "FRVT"
CHECKS_ELEMENTS = "1234567"
CHECKS_REQUIRES = {"3": "1", "6": "4"}  # element 3 and 6 refer back to element 1's asserter rule and 4's source list
NO_CHECKS_SKILLS = {"repository-hygiene"}
CHECKS_LINE_TAG_RE = re.compile(r"^\{\{([qe])=([A-Za-z0-9,]+)\}\} ")
CHECKS_INLINE_RE = re.compile(r"\{\{(!?)q=([A-Za-z0-9,]+):(.*?)\}\}")


def _checks_values(kind: str, raw: str, where: str) -> set[str]:
    vocabulary = CHECKS_QUESTIONS if kind == "q" else CHECKS_ELEMENTS
    values = raw.split(",")
    unknown = [v for v in values if v not in vocabulary]
    if unknown:
        raise SystemExit(f"{where}: unknown scientific-checks {kind} tag {unknown}")
    return set(values)


def checks_selection(text: str, where: str) -> tuple[set[str], set[str]] | None:
    """Parse the entrypoint's one marker; None when it has none, SystemExit when malformed or duplicated."""
    if CHECKS_MARKER not in text:
        return None
    if text.count(CHECKS_MARKER) != 1:
        raise SystemExit(f"{where}: entrypoint must contain at most one {CHECKS_MARKER} marker")
    match = CHECKS_MARKER_RE.search(text)
    if match is None:
        raise SystemExit(f"{where}: malformed {CHECKS_MARKER} marker")
    questions = _checks_values("q", match.group(1), where)
    elements = _checks_values("e", match.group(2), where)
    for need_by, need in CHECKS_REQUIRES.items():
        if need_by in elements and need not in elements:
            raise SystemExit(f"{where}: element {need_by} refers back to element {need}, which the marker omits")
    return questions, elements


def render_checks(fragment: str, questions: set[str], elements: set[str], where: str = "scientific-checks") -> str:
    """Return the fragment lines the selection includes, with every tag stripped."""
    out: list[str] = []
    for number, line in enumerate(fragment.rstrip("\n").split("\n"), 1):
        tag = CHECKS_LINE_TAG_RE.match(line)
        if tag is not None:
            chosen = questions if tag.group(1) == "q" else elements
            wanted = _checks_values(tag.group(1), tag.group(2), f"{where}:{number}")
            if not wanted & chosen:
                continue
            line = line[tag.end():]

        def inline(match: re.Match) -> str:
            wanted = _checks_values("q", match.group(2), f"{where}:{number}")
            return match.group(3) if bool(wanted & questions) != bool(match.group(1)) else ""

        line = CHECKS_INLINE_RE.sub(inline, line)
        if "{{" in line or "}}" in line:
            raise SystemExit(f"{where}:{number}: malformed scientific-checks tag")
        out.append(line)
    return "\n".join(out)


def validate_checks_fragment(fragment: str) -> None:
    """Every tag is in the vocabulary and every question and element has a carrier line."""
    seen = {"q": set(), "e": set()}
    for number, line in enumerate(fragment.split("\n"), 1):
        tag = CHECKS_LINE_TAG_RE.match(line)
        if tag is not None:
            seen[tag.group(1)] |= _checks_values(tag.group(1), tag.group(2), f"scientific-checks:{number}")
        for match in CHECKS_INLINE_RE.finditer(line):
            seen["q"] |= _checks_values("q", match.group(2), f"scientific-checks:{number}")
    for kind, vocabulary in (("q", CHECKS_QUESTIONS), ("e", CHECKS_ELEMENTS)):
        if seen[kind] != set(vocabulary):
            raise SystemExit(f"scientific-checks fragment {kind} tags {sorted(seen[kind])} do not cover {sorted(vocabulary)}")
    render_checks(fragment, set(CHECKS_QUESTIONS), set(CHECKS_ELEMENTS))


def expand_checks(text: str, fragment: str, where: str) -> str:
    """Replace the entrypoint's marker with its generated block; entrypoints without one are unchanged."""
    selection = checks_selection(text, where)
    if selection is None:
        return text
    return CHECKS_MARKER_RE.sub(lambda _: render_checks(fragment, *selection, where=where), text, count=1)


DIRECT_ROUTE_RE = re.compile(r"\]\((?P<kind>references|templates)/(?P<name>[A-Za-z0-9_.-]+\.md)\)")
LOCAL_MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
URI_SCHEME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")


def _direct_payload(root: Path, skill_name: str) -> tuple[list[str], list[str]]:
    """Derive package payload directly from the skill's explicit Markdown routes."""
    skill = root / skill_name / "SKILL.md"
    text = expand_checks(skill.read_text(encoding="utf-8"), CHECKS_FRAGMENT.read_text(encoding="utf-8"), str(skill))
    references: list[str] = []
    templates: list[str] = []
    references.extend(ENTRY_REFERENCES)
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
        if skill.read_text(encoding="utf-8").count(ENTRY_PLACEHOLDER) != 1:
            raise SystemExit(f"{skill}: entrypoint must contain exactly one {ENTRY_PLACEHOLDER}")
        carries = checks_selection(skill.read_text(encoding="utf-8"), str(skill)) is not None
        if carries == (skill_name in NO_CHECKS_SKILLS):
            raise SystemExit(
                f"{skill}: " + (f"{skill_name} must not contain a {CHECKS_MARKER} marker" if carries
                               else f"entrypoint must contain exactly one {CHECKS_MARKER} marker")
            )
        for _, path in entries(skill_name, spec, kind):
            if not path.is_file():
                raise SystemExit(f"missing package source: {path}")


def validate() -> None:
    if not re.fullmatch(r"\d+\.\d+\.\d+", PROTOCOL_VERSION):
        raise SystemExit(f"invalid protocol version: {PROTOCOL_VERSION!r}")
    validate_checks_fragment(CHECKS_FRAGMENT.read_text(encoding="utf-8"))
    validate_registry(ROLES, ROLE_SPECS, "role")
    validate_registry(SPECIALISTS, SPECIALIST_SPECS, "specialist")


def build_one(skill_name: str, spec: dict, kind: str, stage: Path) -> Path:
    root = stage / skill_name
    root.mkdir(parents=True, exist_ok=True)
    for rel, src in entries(skill_name, spec, kind):
        dst = root / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        text = src.read_text(encoding="utf-8")
        if rel == "SKILL.md":
            text = expand_checks(text, CHECKS_FRAGMENT.read_text(encoding="utf-8"), str(src))
            text = text.replace(ENTRY_PLACEHOLDER, entry_contract(
                (SHARED / "references" / ENTRY_REFERENCES[0]).read_text(encoding="utf-8"),
                (SHARED / "references" / ENTRY_REFERENCES[1]).read_text(encoding="utf-8"),
            ))
        text = text.replace("REPLACE_WITH_SKILL_PROTOCOL_VERSION", PROTOCOL_VERSION)
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
