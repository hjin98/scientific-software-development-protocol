#!/usr/bin/env python3
"""Independently validate generated Protocol skill bundles and compatibility adapters."""

from __future__ import annotations

import argparse
import json
import posixpath
import re
import urllib.parse
import zipfile
from pathlib import Path, PurePosixPath

import yaml

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "source"
PROTOCOL_VERSION = (SOURCE / "PROTOCOL_VERSION").read_text(encoding="utf-8").strip()
MAX_SKILL_ZIP_BYTES = 25 * 1024 * 1024
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
SAFE_RESOURCE_LINK_RE = re.compile(r"^(?:references|templates)/[A-Za-z0-9_.-]+\.md$")
RESOURCE_NAMESPACE_RE = re.compile(r"(^|[\\/])(?:references|templates)(?:[\\/]|$)")
URI_SCHEME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
WINDOWS_ABSOLUTE_RE = re.compile(r"^[A-Za-z]:[\\/]")
STANDARD_FRONTMATTER_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}


def canonical_skills() -> dict[str, tuple[str, Path]]:
    found: dict[str, tuple[str, Path]] = {}
    for kind, parent in (("role", SOURCE / "roles"), ("specialist", SOURCE / "specialists")):
        if not parent.is_dir():
            continue
        for path in sorted(parent.iterdir()):
            if path.is_dir() and (path / "SKILL.md").is_file():
                found[path.name] = (kind, path)
    return found


def parse_frontmatter(text: str) -> tuple[dict[str, object], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("SKILL.md must start with YAML frontmatter")
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration as exc:
        raise ValueError("SKILL.md frontmatter is not terminated") from exc
    source = "\n".join(lines[1:end])
    try:
        parsed = yaml.safe_load(source)
    except yaml.YAMLError as exc:
        raise ValueError(f"SKILL.md frontmatter is invalid YAML: {exc}") from exc
    if not isinstance(parsed, dict):
        raise ValueError("SKILL.md frontmatter must be a YAML mapping")
    if not all(isinstance(key, str) for key in parsed):
        raise ValueError("SKILL.md frontmatter keys must be strings")
    return parsed, "\n".join(lines[end + 1 :])


def validate_frontmatter(text: str, skill_name: str) -> tuple[list[str], str]:
    errors: list[str] = []
    try:
        frontmatter, body = parse_frontmatter(text)
    except ValueError as exc:
        return [str(exc)], ""
    unknown = set(frontmatter) - STANDARD_FRONTMATTER_KEYS
    if unknown:
        errors.append(f"unsupported non-portable frontmatter keys: {sorted(unknown)}")
    name = frontmatter.get("name")
    if not isinstance(name, str) or not name:
        errors.append("frontmatter name must be a non-empty string")
    elif len(name) > 64 or not NAME_RE.fullmatch(name):
        errors.append("frontmatter name violates portable kebab-case/64-character constraint")
    elif name != skill_name:
        errors.append("frontmatter name mismatch")
    description = frontmatter.get("description")
    if not isinstance(description, str) or not description:
        errors.append("frontmatter description must be a non-empty string")
    elif len(description) > 1024:
        errors.append("frontmatter description exceeds 1024 characters")
    if "license" in frontmatter and not isinstance(frontmatter["license"], str):
        errors.append("frontmatter license must be a string")
    if "compatibility" in frontmatter:
        compatibility = frontmatter["compatibility"]
        if not isinstance(compatibility, str) or not compatibility:
            errors.append("frontmatter compatibility must be a non-empty string")
        elif len(compatibility) > 500:
            errors.append("frontmatter compatibility exceeds 500 characters")
    if "metadata" in frontmatter:
        metadata = frontmatter["metadata"]
        if not isinstance(metadata, dict):
            errors.append("frontmatter metadata must be a mapping")
        else:
            for key, value in metadata.items():
                if not isinstance(key, str) or not isinstance(value, str):
                    errors.append("frontmatter metadata keys and values must be strings")
                    break
    if "allowed-tools" in frontmatter:
        allowed_tools = frontmatter["allowed-tools"]
        if not isinstance(allowed_tools, str) or not allowed_tools.strip():
            errors.append("frontmatter allowed-tools must be a non-empty space-separated string")
    return errors, body


def validate_resource_routes(body: str, files: dict[str, bytes]) -> list[str]:
    errors: list[str] = []
    direct_links: set[str] = set()
    for raw_target in MARKDOWN_LINK_RE.findall(body):
        target = raw_target.strip()
        if not target or target.startswith("#"):
            continue
        decoded = urllib.parse.unquote(target)
        normalized_for_namespace = decoded
        if decoded.lower().startswith("file:"):
            normalized_for_namespace = decoded[5:]
        elif re.match(r"^[A-Za-z]:", decoded):
            normalized_for_namespace = decoded[2:]
        addresses_resource_namespace = bool(RESOURCE_NAMESPACE_RE.search(normalized_for_namespace))
        if (decoded.lower().startswith("file:") or re.match(r"^[A-Za-z]:", decoded)) and addresses_resource_namespace:
            errors.append(f"unsafe or non-portable resource route: {target}")
            continue
        if URI_SCHEME_RE.match(decoded):
            continue
        if not addresses_resource_namespace:
            continue
        if decoded != target:
            errors.append(f"encoded resource route is not allowed: {target}")
            continue
        if not SAFE_RESOURCE_LINK_RE.fullmatch(target):
            errors.append(f"unsafe or non-portable resource route: {target}")
            continue
        direct_links.add(target)
        if target not in files:
            errors.append(f"routed resource is not packaged: {target}")
    return errors




def validate_packaged_markdown_links(files: dict[str, bytes]) -> list[str]:
    'Validate local Markdown closure and reachability from the SKILL entrypoint.'
    errors: list[str] = []
    edges: dict[str, set[str]] = {}
    for rel, data in sorted(files.items()):
        if not rel.endswith(".md"):
            continue
        edges.setdefault(rel, set())
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError as exc:
            errors.append(f"{rel}: not UTF-8: {exc}")
            continue
        for raw_target in MARKDOWN_LINK_RE.findall(text):
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
                errors.append(f"{rel}: encoded local Markdown route is not allowed: {target}")
                continue
            if path_part.startswith("/") or WINDOWS_ABSOLUTE_RE.match(path_part):
                errors.append(f"{rel}: unsafe local Markdown route: {target}")
                continue
            normalized = posixpath.normpath(posixpath.join(posixpath.dirname(rel), path_part))
            if normalized == ".." or normalized.startswith("../"):
                errors.append(f"{rel}: local Markdown route escapes bundle: {target}")
                continue
            edges[rel].add(normalized)
            if normalized not in files:
                errors.append(f"{rel}: local Markdown route is not packaged: {target} -> {normalized}")

    reachable = {"SKILL.md"}
    queue = ["SKILL.md"]
    while queue:
        rel = queue.pop(0)
        for target in sorted(edges.get(rel, set())):
            if target in files and target not in reachable:
                reachable.add(target)
                queue.append(target)
    packaged_resources = {
        rel for rel in files
        if (rel.startswith("references/") or rel.startswith("templates/")) and rel.endswith(".md")
    }
    for rel in sorted(packaged_resources - reachable):
        errors.append(f"packaged Markdown resource is not reachable from SKILL.md: {rel}")
    return errors

def validate_agent_yaml(text: str) -> list[str]:
    errors: list[str] = []
    if not re.search(r"(?m)^interface:\s*$", text):
        errors.append("missing interface mapping")
    if not re.search(r"(?m)^\s+display_name:\s*.+$", text):
        errors.append("missing display_name")
    if not re.search(r"(?m)^\s+short_description:\s*.+$", text):
        errors.append("missing short_description")
    return errors


def directory_files(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(p for p in root.rglob("*") if p.is_file())
    }


def zip_files(path: Path, skill_name: str) -> tuple[dict[str, bytes], list[str]]:
    errors: list[str] = []
    files: dict[str, bytes] = {}
    try:
        with zipfile.ZipFile(path, "r") as zf:
            names = zf.namelist()
            if len(names) != len(set(names)):
                errors.append("duplicate ZIP members")
            prefix = f"{skill_name}/"
            for name in names:
                posix = PurePosixPath(name)
                if posix.is_absolute() or ".." in posix.parts:
                    errors.append(f"unsafe ZIP member {name!r}")
                    continue
                if not name.startswith(prefix):
                    errors.append(f"ZIP member is outside single {skill_name}/ root: {name!r}")
                    continue
                rel = name[len(prefix):]
                if rel and not name.endswith("/"):
                    files[rel] = zf.read(name)
    except (OSError, zipfile.BadZipFile) as exc:
        errors.append(f"invalid ZIP: {exc}")
    return files, errors


def expected_canonical_bytes(rel: str, source_root: Path) -> bytes | None:
    if rel == "SKILL.md":
        path = source_root / "SKILL.md"
    elif rel == "agents/openai.yaml":
        path = source_root / "agents/openai.yaml"
    elif rel.startswith("references/") or rel.startswith("templates/"):
        path = SOURCE / "shared" / rel
    else:
        return None
    if not path.is_file():
        return None
    return path.read_bytes().replace(
        b"REPLACE_WITH_SKILL_PROTOCOL_VERSION", PROTOCOL_VERSION.encode("utf-8")
    )


def validate_core_bundle(files: dict[str, bytes], skill_name: str, kind: str, source_root: Path) -> list[str]:
    errors: list[str] = []
    required = {"SKILL.md", "PROTOCOL_VERSION", "protocol-manifest.json"}
    for rel in sorted(required - set(files)):
        errors.append(f"generic core missing required member {rel}")
    if required - set(files):
        return errors

    try:
        skill_text = files["SKILL.md"].decode("utf-8")
    except UnicodeDecodeError as exc:
        return [f"SKILL.md is not UTF-8: {exc}"]
    fm_errors, body = validate_frontmatter(skill_text, skill_name)
    errors.extend(f"SKILL.md: {error}" for error in fm_errors)

    canonical_skill = expected_canonical_bytes("SKILL.md", source_root)
    if canonical_skill is None or files["SKILL.md"] != canonical_skill:
        errors.append("SKILL.md differs from canonical source")

    try:
        packaged_version = files["PROTOCOL_VERSION"].decode("utf-8").strip()
    except UnicodeDecodeError as exc:
        errors.append(f"PROTOCOL_VERSION is not UTF-8: {exc}")
        packaged_version = ""
    if packaged_version != PROTOCOL_VERSION:
        errors.append("protocol version mismatch")

    try:
        manifest = json.loads(files["protocol-manifest.json"].decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        errors.append(f"invalid protocol manifest: {exc}")
        manifest = {}
    if manifest.get("protocol_version") != PROTOCOL_VERSION:
        errors.append("manifest protocol_version mismatch")
    if manifest.get("skill_name") != skill_name:
        errors.append("manifest skill_name mismatch")
    if kind == "role" and not manifest.get("role"):
        errors.append("role package missing manifest role")
    if kind == "specialist" and manifest.get("kind") != "specialist":
        errors.append("specialist package missing manifest kind")

    errors.extend(validate_resource_routes(body, files))
    errors.extend(validate_packaged_markdown_links(files))
    packaged_routes = {
        rel for rel in files
        if (rel.startswith("references/") or rel.startswith("templates/")) and rel.endswith(".md")
    }
    for rel in sorted(packaged_routes):
        expected = expected_canonical_bytes(rel, source_root)
        if expected is None:
            errors.append(f"packaged resource has no canonical source: {rel}")
        elif files[rel] != expected:
            errors.append(f"packaged resource differs from canonical source: {rel}")
    return errors


def validate_openai_adapter(files: dict[str, bytes], source_root: Path) -> list[str]:
    rel = "agents/openai.yaml"
    if rel not in files:
        return ["OpenAI adapter missing agents/openai.yaml"]
    expected = expected_canonical_bytes(rel, source_root)
    if expected is None or files[rel] != expected:
        return ["OpenAI adapter differs from canonical source"]
    try:
        return [f"OpenAI adapter {error}" for error in validate_agent_yaml(files[rel].decode("utf-8"))]
    except UnicodeDecodeError as exc:
        return [f"OpenAI adapter is not UTF-8: {exc}"]


def validate(dist: Path) -> list[str]:
    errors: list[str] = []
    skills = canonical_skills()
    if not dist.is_dir():
        return [f"distribution directory is missing: {dist}"]

    index_path = dist / "BUILD_INDEX.json"
    if not index_path.is_file():
        return ["BUILD_INDEX.json is missing"]
    try:
        index = json.loads(index_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return [f"BUILD_INDEX.json is invalid: {exc}"]
    if index.get("protocol_version") != PROTOCOL_VERSION:
        errors.append("BUILD_INDEX protocol_version mismatch")
    if index.get("runtime_root") != "skills":
        errors.append("BUILD_INDEX runtime_root must be 'skills'")
    if set(index.get("skills", [])) != set(skills):
        errors.append("BUILD_INDEX skill set does not match canonical source")

    expected_top_files = {"BUILD_INDEX.json", *(f"{name}.zip" for name in skills)}
    actual_top_files = {path.name for path in dist.iterdir() if path.is_file()}
    if actual_top_files != expected_top_files:
        errors.append(
            f"distribution top-level file set mismatch: expected={sorted(expected_top_files)} actual={sorted(actual_top_files)}"
        )
    actual_top_dirs = {path.name for path in dist.iterdir() if path.is_dir()}
    if actual_top_dirs != {"skills"}:
        errors.append(f"distribution top-level directory set mismatch: expected=['skills'] actual={sorted(actual_top_dirs)}")

    skills_root = dist / "skills"
    if not skills_root.is_dir():
        return errors + ["unpacked runtime root dist/skills is missing"]
    runtime_dirs = {path.name for path in skills_root.iterdir() if path.is_dir()}
    if runtime_dirs != set(skills):
        errors.append(f"runtime skill set mismatch: expected={sorted(skills)} actual={sorted(runtime_dirs)}")

    for skill_name, (kind, source_root) in skills.items():
        dir_root = skills_root / skill_name
        dir_files = directory_files(dir_root) if dir_root.is_dir() else {}
        for error in validate_core_bundle(dir_files, skill_name, kind, source_root):
            errors.append(f"skills/{skill_name}: {error}")
        for error in validate_openai_adapter(dir_files, source_root):
            errors.append(f"skills/{skill_name}: {error}")

        package = dist / f"{skill_name}.zip"
        if not package.is_file():
            errors.append(f"{skill_name}.zip is missing")
            continue
        if package.stat().st_size > MAX_SKILL_ZIP_BYTES:
            errors.append(f"{package.name}: exceeds 25 MB skill package limit")
        zip_map, zip_errors = zip_files(package, skill_name)
        errors.extend(f"{package.name}: {error}" for error in zip_errors)
        for error in validate_core_bundle(zip_map, skill_name, kind, source_root):
            errors.append(f"{package.name}: {error}")
        for error in validate_openai_adapter(zip_map, source_root):
            errors.append(f"{package.name}: {error}")
        if dir_files != zip_map:
            missing = sorted(set(dir_files) - set(zip_map))
            extra = sorted(set(zip_map) - set(dir_files))
            changed = sorted(rel for rel in set(dir_files) & set(zip_map) if dir_files[rel] != zip_map[rel])
            errors.append(f"{skill_name}: unpacked/ZIP bundle mismatch: missing={missing} extra={extra} changed={changed}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dist", type=Path, required=True)
    args = parser.parse_args()
    errors = validate(args.dist.resolve())
    if errors:
        for error in errors:
            print(error)
        return 1
    print("all generated Protocol skill directory bundles and ZIPs are structurally valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
