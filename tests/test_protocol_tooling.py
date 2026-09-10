from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source"
sys.path.insert(0, str(SOURCE))

import build_skills  # noqa: E402
import check_dist  # noqa: E402
import validate_packages  # noqa: E402


def rewrite_zip(path: Path, transform) -> None:
    with zipfile.ZipFile(path, "r") as zf:
        members = [(info.filename, zf.read(info.filename)) for info in zf.infolist()]
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for name, data in transform(members):
            zf.writestr(name, data)


class ProtocolToolingTests(unittest.TestCase):
    def test_build_and_validate_packages(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dist = Path(tmp) / "dist"
            build_skills.build(dist)
            self.assertEqual([], validate_packages.validate(dist))

    def test_build_emits_unpacked_and_zip_runtime_forms(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dist = Path(tmp) / "dist"
            build_skills.build(dist)
            for skill in build_skills.ROLE_SPECS | build_skills.SPECIALIST_SPECS:
                self.assertTrue((dist / "skills" / skill / "SKILL.md").is_file())
                self.assertTrue((dist / f"{skill}.zip").is_file())

    def test_implementation_package_contains_cross_cutting_references_and_openai_adapter(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dist = Path(tmp) / "dist"
            build_skills.build(dist)
            with zipfile.ZipFile(dist / "software-implementation.zip", "r") as zf:
                names = set(zf.namelist())
            prefix = "software-implementation/"
            required = {
                prefix + "agents/openai.yaml",
                prefix + "references/configuration-and-policy.md",
                prefix + "references/concurrency-and-orchestration.md",
                prefix + "references/security-and-trust-boundaries.md",
                prefix + "references/repository-intake.md",
                prefix + "references/git-and-version-control.md",
            }
            self.assertTrue(required <= names, required - names)

    def test_generic_core_validation_does_not_require_openai_adapter(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dist = Path(tmp) / "dist"
            build_skills.build(dist)
            root = dist / "skills" / "software-design"
            files = validate_packages.directory_files(root)
            files.pop("agents/openai.yaml")
            errors = validate_packages.validate_core_bundle(
                files, "software-design", "role", SOURCE / "roles/software-design"
            )
            self.assertEqual([], errors)

    def test_repository_adapter_validation_rejects_missing_openai_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dist = Path(tmp) / "dist"
            build_skills.build(dist)
            package = dist / "software-design.zip"

            def without_agent(members):
                return [(name, data) for name, data in members if not name.endswith("agents/openai.yaml")]

            rewrite_zip(package, without_agent)
            errors = validate_packages.validate(dist)
            self.assertTrue(any("OpenAI adapter missing" in error for error in errors), errors)

    def test_validator_rejects_broken_direct_reference_route(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dist = Path(tmp) / "dist"
            build_skills.build(dist)
            package = dist / "software-design.zip"

            def add_bad_route(members):
                out = []
                for name, data in members:
                    if name.endswith("/SKILL.md"):
                        data += b"\nRead [missing](references/not-packaged.md).\n"
                    out.append((name, data))
                return out

            rewrite_zip(package, add_bad_route)
            errors = validate_packages.validate(dist)
            self.assertTrue(any("routed resource is not packaged" in error for error in errors), errors)

    def test_validator_rejects_packaged_unlinked_reference(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dist = Path(tmp) / "dist"
            build_skills.build(dist)
            package = dist / "software-design.zip"

            def add_unlinked(members):
                members.append(("software-design/references/unlinked.md", b"sentinel\n"))
                return members

            rewrite_zip(package, add_unlinked)
            errors = validate_packages.validate(dist)
            self.assertTrue(any("not reachable from SKILL.md" in error for error in errors), errors)

    def test_frontmatter_accepts_standard_optional_field(self) -> None:
        text = "---\nname: sample-skill\ndescription: Portable sample.\nlicense: MIT\nmetadata:\n  owner: test\n---\nbody\n"
        errors, _ = validate_packages.validate_frontmatter(text, "sample-skill")
        self.assertEqual([], errors)

    def test_frontmatter_rejects_nonportable_name(self) -> None:
        text = "---\nname: Bad_Name\ndescription: Sample.\n---\nbody\n"
        errors, _ = validate_packages.validate_frontmatter(text, "Bad_Name")
        self.assertTrue(any("kebab-case" in error for error in errors), errors)

    def test_dist_parity_detects_modified_zip_member(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            expected = Path(tmp) / "expected"
            committed = Path(tmp) / "committed"
            build_skills.build(expected)
            shutil.copytree(expected, committed)
            package = committed / "software-implementation.zip"

            def modify_skill(members):
                out = []
                for name, data in members:
                    if name.endswith("/SKILL.md"):
                        data += b"\n# tampered\n"
                    out.append((name, data))
                return out

            rewrite_zip(package, modify_skill)
            errors = check_dist.compare(expected, committed)
            self.assertTrue(any("semantic package mismatch" in error for error in errors), errors)

    def test_dist_parity_detects_modified_unpacked_member(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            expected = Path(tmp) / "expected"
            committed = Path(tmp) / "committed"
            build_skills.build(expected)
            shutil.copytree(expected, committed)
            skill = committed / "skills/software-design/SKILL.md"
            skill.write_text(skill.read_text(encoding="utf-8") + "\n# tampered\n", encoding="utf-8")
            errors = check_dist.compare(expected, committed)
            self.assertTrue(any("distribution mismatch" in error for error in errors), errors)

    def test_dist_parity_ignores_zip_metadata_when_contents_match(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            expected = Path(tmp) / "expected"
            committed = Path(tmp) / "committed"
            build_skills.build(expected)
            shutil.copytree(expected, committed)
            package = committed / "software-design.zip"
            rewrite_zip(package, lambda members: members)
            self.assertEqual([], check_dist.compare(expected, committed))

    def test_build_index_matches_protocol_version_and_runtime_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dist = Path(tmp) / "dist"
            build_skills.build(dist)
            index = json.loads((dist / "BUILD_INDEX.json").read_text(encoding="utf-8"))
            version = (SOURCE / "PROTOCOL_VERSION").read_text(encoding="utf-8").strip()
            self.assertEqual(version, index["protocol_version"])
            self.assertEqual("skills", index["runtime_root"])


if __name__ == "__main__":
    unittest.main()
