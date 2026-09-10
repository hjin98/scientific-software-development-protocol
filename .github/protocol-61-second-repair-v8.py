from __future__ import annotations

from pathlib import Path
import subprocess


def replace_once(path: str, old: str, new: str, label: str) -> None:
    p = Path(path)
    text = p.read_text(encoding='utf-8')
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f'{label}: expected one anchor, found {count}')
    p.write_text(text.replace(old, new, 1), encoding='utf-8')


# Revision 1 changed package membership from direct-only payload to bounded
# transitive payload while preserving SKILL.md direct links as the activation
# contract. These two older tests must therefore interrogate activation routes,
# not infer routing from payload presence.
old_511 = '''        with tempfile.TemporaryDirectory() as tmp:\n            dist = Path(tmp) / "dist"\n            build_skills.build(dist)\n            for role in ("software-design", "software-implementation"):\n                for name in TOOL_FILES:\n                    self.assertTrue((dist / "skills" / role / "references" / name).is_file())\n            for role in ("scientific-formulation", "numerical-algorithm-design"):\n                for name in DIRECT_TOOL_FILES:\n                    self.assertFalse((dist / "skills" / role / "references" / name).exists())\n            for specialist in ("software-documentation", "repository-hygiene"):\n                for name in TOOL_FILES:\n                    self.assertFalse((dist / "skills" / specialist / "references" / name).exists())\n            audit_root = dist / "skills" / "software-maintenance-audit" / "references"\n            self.assertTrue((audit_root / "tool-assisted-engineering.md").is_file())\n            for name in DIRECT_TOOL_FILES:\n                self.assertFalse((audit_root / name).exists())\n'''
new_511 = '''        # Package payload may now contain transitive local-Markdown dependencies.\n        # Progressive disclosure is governed by the direct SKILL.md activation\n        # routes asserted above, not by absence of transitively required payload.\n        with tempfile.TemporaryDirectory() as tmp:\n            dist = Path(tmp) / "dist"\n            build_skills.build(dist)\n            for role in ("software-design", "software-implementation"):\n                for name in TOOL_FILES:\n                    self.assertTrue((dist / "skills" / role / "references" / name).is_file())\n            audit_root = dist / "skills" / "software-maintenance-audit" / "references"\n            self.assertTrue((audit_root / "tool-assisted-engineering.md").is_file())\n'''
replace_once('tests/test_protocol_511_tool_assistance.py', old_511, new_511, 'Protocol 5.11 progressive-disclosure oracle')

old_515 = '''    def test_real_package_builder_carries_only_routed_profile_payload(self) -> None:\n        routed = language_route_links(self.design_path)\n        with tempfile.TemporaryDirectory() as td:\n            out = Path(td) / "dist"\n            subprocess.run([sys.executable, str(ROOT / "source/build_skills.py"), "--output", str(out)], cwd=ROOT, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)\n            for role in ("software-design", "software-implementation"):\n                refs = {p.name for p in (out / "skills" / role / "references").iterdir() if p.is_file()}\n                self.assertTrue(routed <= refs, (role, sorted(routed - refs)))\n            for specialist in ("software-documentation", "repository-hygiene", "software-maintenance-audit"):\n                refs = {p.name for p in (out / "skills" / specialist / "references").iterdir() if p.is_file()}\n                self.assertTrue(routed.isdisjoint(refs), (specialist, sorted(routed & refs)))\n'''
new_515 = '''    def test_real_package_builder_carries_routed_profiles_without_promoting_transitive_payload(self) -> None:\n        routed = language_route_links(self.design_path)\n        with tempfile.TemporaryDirectory() as td:\n            out = Path(td) / "dist"\n            subprocess.run([sys.executable, str(ROOT / "source/build_skills.py"), "--output", str(out)], cwd=ROOT, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)\n            for role in ("software-design", "software-implementation"):\n                refs = {p.name for p in (out / "skills" / role / "references").iterdir() if p.is_file()}\n                self.assertTrue(routed <= refs, (role, sorted(routed - refs)))\n\n        # Under bounded transitive package closure, payload presence is not an\n        # activation route. Specialists must still omit language profiles from\n        # their direct SKILL.md routing contract unless that role explicitly owns\n        # a language-profile decision.\n        for specialist in ("software-documentation", "repository-hygiene", "software-maintenance-audit"):\n            direct = {Path(link).name for link in LINK_RE.findall(read(f"source/specialists/{specialist}/SKILL.md"))}\n            self.assertTrue(routed.isdisjoint(direct), (specialist, sorted(routed & direct)))\n'''
replace_once('tests/test_protocol_515_language_profiles.py', old_515, new_515, 'Protocol 5.15 package-routing oracle')

# Ensure the successful runner removes every temporary transport/diagnostic file
# accumulated during the web-only repair attempts. This changes only transport
# residue, not Protocol source semantics.
base = Path('.github/protocol-61-second-repair.py')
text = base.read_text(encoding='utf-8')
old_cleanup = "run('git', 'rm', '.github/workflows/protocol-61-second-repair.yml', '.github/protocol-61-second-repair.py')"
new_cleanup = "run('git', 'rm', '-f', '--ignore-unmatch', '.github/workflows/protocol-61-second-repair.yml', '.github/workflows/protocol-61-second-repair-v8.yml', '.github/protocol-61-second-repair.py', '.github/protocol-61-second-repair-v3.py', '.github/protocol-61-second-repair-v4.py', '.github/protocol-61-second-repair-v5.py', '.github/protocol-61-second-repair-v6.py', '.github/protocol-61-second-repair-v7.py', '.github/protocol-61-second-repair-v8.py', 'workplans/active/.protocol-61-second-repair-diagnostic.txt', 'workplans/active/.protocol-61-second-repair-diagnostic-v3.txt', 'workplans/active/.protocol-61-second-repair-diagnostic-v4.txt', 'workplans/active/.protocol-61-second-repair-diagnostic-v5.txt', 'workplans/active/.protocol-61-second-repair-diagnostic-v6.txt', 'workplans/active/.protocol-61-second-repair-diagnostic-v7.txt', 'workplans/active/.protocol-61-second-repair-diagnostic-v8.txt')"
if old_cleanup not in text:
    raise RuntimeError('base cleanup anchor missing')
base.write_text(text.replace(old_cleanup, new_cleanup, 1), encoding='utf-8')

subprocess.run(['python', '.github/protocol-61-second-repair-v7.py'], check=True)
