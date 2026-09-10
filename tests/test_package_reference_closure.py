from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source"
sys.path.insert(0, str(SOURCE))
import build_skills  # noqa: E402
import validate_packages  # noqa: E402


class PackageReferenceClosureTests(unittest.TestCase):
    def test_every_built_bundle_has_closed_local_markdown_routes(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "dist"
            build_skills.build(out)
            for skill_name, _, _ in build_skills.all_specs():
                files = validate_packages.directory_files(out / "skills" / skill_name)
                self.assertEqual([], validate_packages.validate_packaged_markdown_links(files), skill_name)

    def test_nested_dangling_markdown_route_is_rejected(self) -> None:
        files = {
            "SKILL.md": b"# Example\n\n[packaged](references/a.md)\n",
            "references/a.md": b"# A\n\n[missing](scientific-technical-writing.md)\n",
        }
        errors = validate_packages.validate_packaged_markdown_links(files)
        self.assertTrue(any("local Markdown route is not packaged" in error for error in errors), errors)

    def test_documentation_route_packages_writing_owner_transitively(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "dist"
            build_skills.build(out)
            for skill_name, spec, _ in build_skills.all_specs():
                if "documentation-and-evidence.md" not in set(spec["references"]):
                    continue
                files = validate_packages.directory_files(out / "skills" / skill_name)
                self.assertIn("references/documentation-and-evidence.md", files, skill_name)
                self.assertIn("references/scientific-technical-writing.md", files, skill_name)
                self.assertEqual([], validate_packages.validate_packaged_markdown_links(files), skill_name)


class PackageReferenceReachabilityTests(unittest.TestCase):
    def test_unreachable_packaged_markdown_resource_is_rejected(self) -> None:
        files = {
            "SKILL.md": b"# Example\n",
            "references/unrelated.md": b"# Unrelated\n",
        }
        errors = validate_packages.validate_packaged_markdown_links(files)
        self.assertTrue(any("not reachable from SKILL.md" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
