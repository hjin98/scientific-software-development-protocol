import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source"
REFERENCES = SOURCE / "shared" / "references"
TEMPLATES = SOURCE / "shared" / "templates"
ROLES = SOURCE / "roles"
SPECIALISTS = SOURCE / "specialists"


class Protocol62RepresentationTests(unittest.TestCase):
    def test_current_version_and_nomenclature(self):
        self.assertEqual((SOURCE / "PROTOCOL_VERSION").read_text().strip(), "6.2.0")
        self.assertTrue((REFERENCES / "abstraction-and-concretization.md").is_file())
        self.assertFalse((REFERENCES / "abstraction-and-realization.md").exists())
        self.assertTrue((TEMPLATES / "abstraction_concretization_change_plan_template.md").is_file())
        self.assertFalse((TEMPLATES / "abstraction_realization_change_plan_template.md").exists())

    def test_universal_kernel_contains_lossless_representation_contract(self):
        text = (REFERENCES / "abstraction-and-concretization.md").read_text()
        for phrase in (
            "Lossless Representation Rule",
            "governed scope",
            "One detailed owner per generic rule",
            "Use progressive disclosure",
            "Keep cold paths discoverable",
            "Weight attention without weakening acceptance",
            "Do not deduplicate by adjudicating semantics",
        ):
            self.assertIn(phrase, text)

    def test_every_entrypoint_routes_to_current_kernel(self):
        skill_paths = sorted(ROLES.glob("*/SKILL.md")) + sorted(SPECIALISTS.glob("*/SKILL.md"))
        self.assertEqual(len(skill_paths), 7)
        for path in skill_paths:
            with self.subTest(path=path):
                text = path.read_text()
                self.assertIn("references/abstraction-and-concretization.md", text)
                self.assertNotIn("references/abstraction-and-realization.md", text)

    def test_root_roles_delegate_language_and_tool_leaf_routing(self):
        leaf_routes = (
            "references/python-engineering.md",
            "references/cpp-engineering.md",
            "references/tool-serena.md",
            "references/tool-semgrep.md",
            "references/tool-hypothesis.md",
            "references/tool-codeql.md",
        )
        for role in ("software-design", "software-implementation"):
            text = (ROLES / role / "SKILL.md").read_text()
            self.assertIn("references/language-profiles.md", text)
            self.assertIn("references/tool-assisted-engineering.md", text)
            for leaf in leaf_routes:
                with self.subTest(role=role, leaf=leaf):
                    self.assertNotIn(leaf, text)

        language_router = (REFERENCES / "language-profiles.md").read_text()
        self.assertIn("python-engineering.md", language_router)
        self.assertIn("cpp-engineering.md", language_router)
        tool_router = (REFERENCES / "tool-assisted-engineering.md").read_text()
        for leaf in ("tool-serena.md", "tool-semgrep.md", "tool-hypothesis.md", "tool-codeql.md"):
            self.assertIn(leaf, tool_router)

    def test_documentation_specialist_cold_domain_routes_are_resolvable_and_packaged(self):
        text = (SPECIALISTS / "software-documentation" / "SKILL.md").read_text()
        packaged = ROOT / "dist" / "skills" / "software-documentation" / "references"
        for leaf in (
            "security-and-trust-boundaries.md",
            "performance-and-parallelism.md",
            "storage-and-io.md",
            "release-and-distribution.md",
        ):
            with self.subTest(leaf=leaf):
                self.assertIn(f"references/{leaf}", text)
                self.assertTrue((packaged / leaf).is_file())

    def test_navigation_does_not_define_activation_by_package_presence(self):
        for path in (
            ROOT / "README.md",
            ROOT / "PORTABILITY.md",
            SOURCE / "README.md",
            SOURCE / "SEMANTIC_DEPENDENCIES.md",
        ):
            text = path.read_text().lower()
            self.assertIn("package membership", text)
            self.assertIn("activation", text)

    def test_public_source_surfaces_publish_exact_protocol_62_bootstrap(self):
        bootstrap = "1181c2031710c5d343194d87d08543290fded0ab"
        surfaces = (
            REFERENCES / "development-workflow-prompts.md",
            REFERENCES / "protocol-versioning-and-compatibility.md",
            ROOT / "PORTABILITY.md",
            ROOT / "README.md",
        )
        for path in surfaces:
            with self.subTest(path=path):
                self.assertIn(bootstrap, path.read_text())
        prompt = (REFERENCES / "development-workflow-prompts.md").read_text().lower()
        portability = (ROOT / "PORTABILITY.md").read_text().lower()
        self.assertNotIn("automatic current-6.2 public fallback is unavailable", prompt)
        self.assertNotIn("protocol 6.2 pre-bootstrap state", portability)

    def test_preservation_evidence_is_explicitly_non_authoritative(self):
        census = ROOT / "qualification" / "ssdp6" / "SSDP-6.2-PRESERVATION-CENSUS.md"
        text = census.read_text()
        self.assertIn("authority: non-normative-evidence", text)
        self.assertIn("all 95", text.lower())
        self.assertIn("Protocol 5.0", text)
        self.assertIn("6.1", text)

    def test_current_navigation_uses_new_kernel_path(self):
        current_files = [
            ROOT / "README.md",
            ROOT / "AGENTS.md",
            ROOT / "PORTABILITY.md",
            SOURCE / "README.md",
            SOURCE / "SEMANTIC_DEPENDENCIES.md",
        ]
        for path in current_files:
            text = path.read_text()
            with self.subTest(path=path):
                self.assertIn("abstraction-and-concretization.md", text)
                self.assertNotIn("source/shared/references/abstraction-and-realization.md", text)


if __name__ == "__main__":
    unittest.main()
