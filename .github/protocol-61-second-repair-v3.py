from __future__ import annotations

from pathlib import Path

base_path = Path('.github/protocol-61-second-repair.py')
text = base_path.read_text(encoding='utf-8')

injected = r'''

def patch_transitive_package_closure() -> None:
    builder_path = Path('source/build_skills.py')
    builder = builder_path.read_text(encoding='utf-8')
    if 'import urllib.parse\n' not in builder:
        builder = builder.replace('import re\n', 'import re\nimport urllib.parse\n', 1)
    if 'LOCAL_MARKDOWN_LINK_RE =' not in builder:
        anchor = 'DIRECT_ROUTE_RE = re.compile(r"\\]\\((?P<kind>references|templates)/(?P<name>[A-Za-z0-9_.-]+\\.md)\\)")\n'
        addition = anchor + 'LOCAL_MARKDOWN_LINK_RE = re.compile(r"\\[[^\\]]+\\]\\(([^)]+)\\)")\nURI_SCHEME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")\n'
        if anchor not in builder:
            raise RuntimeError('builder regex anchor missing')
        builder = builder.replace(anchor, addition, 1)

    helper = r'''

def _transitive_payload(spec: dict) -> list[tuple[str, Path]]:
    """Return the finite local-Markdown closure of direct SKILL activation seeds."""
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
'''
    if 'def _transitive_payload(' not in builder:
        anchor = '\ndef entries(skill_name: str, spec: dict, kind: str) -> list[tuple[str, Path]]:\n'
        if anchor not in builder:
            raise RuntimeError('builder entries anchor missing')
        builder = builder.replace(anchor, helper + anchor, 1)
    old = '''    out += [(f"references/{name}", SHARED / "references" / name) for name in spec["references"]]\n    out += [(f"templates/{name}", SHARED / "templates" / name) for name in spec["templates"]]\n    return out\n'''
    new = '''    out += _transitive_payload(spec)\n    return out\n'''
    if old in builder:
        builder = builder.replace(old, new, 1)
    elif 'out += _transitive_payload(spec)' not in builder:
        raise RuntimeError('builder direct-payload anchor missing')
    builder_path.write_text(builder, encoding='utf-8')

    validator_path = Path('source/validate_packages.py')
    validator = validator_path.read_text(encoding='utf-8')
    old_direct = '''    packaged_routes = {\n        rel for rel in files\n        if (rel.startswith("references/") or rel.startswith("templates/")) and rel.endswith(".md")\n    }\n    for rel in sorted(packaged_routes - direct_links):\n        errors.append(f"packaged resource is not directly Markdown-linked from SKILL.md: {rel}")\n'''
    if old_direct in validator:
        validator = validator.replace(old_direct, '', 1)
    stronger = r'''
def validate_packaged_markdown_links(files: dict[str, bytes]) -> list[str]:
    """Validate local Markdown closure and reachability from the SKILL entrypoint."""
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

'''
    start = validator.find('def validate_packaged_markdown_links(')
    end = validator.find('def validate_agent_yaml(', start)
    if start < 0 or end < 0:
        raise RuntimeError('validator closure function anchors missing')
    validator = validator[:start] + stronger + validator[end:]
    validator_path.write_text(validator, encoding='utf-8')

    test_path = Path('tests/test_package_reference_closure.py')
    test = test_path.read_text(encoding='utf-8')
    if 'test_unreachable_packaged_markdown_resource_is_rejected' not in test:
        addition = r'''

class PackageReferenceReachabilityTests(unittest.TestCase):
    def test_unreachable_packaged_markdown_resource_is_rejected(self) -> None:
        files = {
            "SKILL.md": b"# Example\n",
            "references/unrelated.md": b"# Unrelated\n",
        }
        errors = validate_packages.validate_packaged_markdown_links(files)
        self.assertTrue(any("not reachable from SKILL.md" in error for error in errors), errors)
'''
        test = test.replace('\n\nif __name__ == "__main__":\n', addition + '\n\nif __name__ == "__main__":\n', 1)
    test_path.write_text(test, encoding='utf-8')

    tooling_path = Path('tests/test_protocol_tooling.py')
    tooling = tooling_path.read_text(encoding='utf-8')
    tooling = tooling.replace('any("not directly Markdown-linked" in error for error in errors)', 'any("not reachable from SKILL.md" in error for error in errors)')
    tooling_path.write_text(tooling, encoding='utf-8')
'''

anchor = '\ndef build_and_validate(dist_tmp: str, *, regenerate_snapshot: bool) -> None:\n'
if anchor not in text:
    raise RuntimeError('repair-script injection anchor missing')
text = text.replace(anchor, injected + anchor, 1)
text = text.replace('patch_stage_a()\nbuild_and_validate(', 'patch_stage_a()\npatch_transitive_package_closure()\nbuild_and_validate(', 1)
text = text.replace(
    "run('git', 'rm', '.github/workflows/protocol-61-second-repair.yml', '.github/protocol-61-second-repair.py')",
    "run('git', 'rm', '.github/workflows/protocol-61-second-repair.yml', '.github/protocol-61-second-repair.py', '.github/protocol-61-second-repair-v3.py', 'workplans/active/.protocol-61-second-repair-diagnostic.txt')",
    1,
)
exec_path = Path('/tmp/protocol-61-second-repair-v3-exec.py')
exec_path.write_text(text, encoding='utf-8')
compile(text, str(exec_path), 'exec')
exec(compile(text, str(exec_path), 'exec'), {'__name__': '__main__', '__file__': str(exec_path)})
