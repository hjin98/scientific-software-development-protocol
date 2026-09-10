from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def norm(text: str) -> str:
    return text.lower().replace("**", "").replace("`", "")


def paragraph_containing(text: str, needle: str) -> str:
    for paragraph in text.split("\n\n"):
        if needle.lower() in paragraph.lower():
            return paragraph
    raise AssertionError(f"no paragraph contains {needle!r}")


def mutate_paragraph(text: str, needle: str, contradiction: str) -> str:
    paragraph = paragraph_containing(text, needle)
    return text.replace(paragraph, paragraph.rstrip() + " " + contradiction.strip(), 1)


def negative_pipeline_holds(text: str) -> bool:
    paragraph = norm(paragraph_containing(text, "mandatory three-tool pipeline"))
    if "a mandatory three-tool pipeline is required" in paragraph or "form a mandatory three-tool pipeline" in paragraph:
        return False
    return "without becoming a mandatory three-tool pipeline" in paragraph


ANTI_GAMING = (
    "excessive filtering",
    "assume",
    "over-narrow strategies",
    "exclusions",
    "health-check suppression",
    "disabled useful phases",
    "removed deadlines",
    "reduced exploration",
)


def hypothesis_anti_gaming_holds(text: str) -> bool:
    paragraph = norm(paragraph_containing(text, "health-check suppression"))
    if "solely to make a property green" not in paragraph or "do not use" not in paragraph:
        return False
    if not all(item in paragraph for item in ANTI_GAMING):
        return False
    return not any(
        re.search(rf"{re.escape(item)}.{{0,40}}(?:may|should|can|is permitted to|are allowed to).{{0,40}}solely to make a property green", paragraph)
        for item in ANTI_GAMING
    )


def hypothesis_settings_holds(text: str) -> bool:
    value = norm(text)
    return (
        "change settings when project/test semantics justify it" in value
        and "required coverage remains intact" in value
        and "required coverage is optional" not in value
        and "required coverage may then be discarded" not in value
    )


def root_router_holds(text: str) -> bool:
    value = norm(text)
    leaves = ("tool-serena.md", "tool-semgrep.md", "tool-hypothesis.md", "tool-codeql.md")
    return (
        "references/tool-assisted-engineering.md" in value
        and "relation" in value
        and all(f"references/{leaf}" not in value for leaf in leaves)
    )


def common_router_holds(text: str) -> bool:
    value = norm(text)
    required = (
        "relation under the current material claim",
        "literal/path/text relation -> ordinary repository search/read",
        "symbol owner/definition/reference/caller relation -> serena",
        "ast/syntax/structural relation -> semgrep",
        "broad python input/state invariant -> hypothesis",
        "interprocedural flow/taint/source-to-sink relation -> codeql",
        "security task is not automatically a codeql task",
        "forbidden-call pattern is structural",
        "multi-function untrusted-source-to-dangerous-sink claim is interprocedural data flow",
        "minimum set of capabilities",
        "decompose a multi-relation claim",
        "available, current, supported, and directly models the claim",
        "presumptively use it",
        "fall back for a concrete reason",
        "familiarity with grep/read/shell/tests is not itself a fallback reason",
        "specialized tools are bounded models",
        "state negative/completeness claims no more broadly than",
        "cross-check dynamic dispatch",
        "runtime-only behavior",
    )
    forbidden = (
        "all security tasks always route to codeql",
        "security always means codeql",
        "specialized analyzer output is exhaustive",
        "familiarity with grep/read/shell/tests is a valid fallback reason",
    )
    return all(item in value for item in required) and not any(item in value for item in forbidden)


def specialist_owner_holds(name: str, text: str) -> bool:
    value = norm(text)
    required = {
        "serena": (
            "semantic repository intake, navigation, reference discovery",
            "literal strings, filenames, configuration, generated/external surfaces",
            "cheap non-mutating availability/capability probe",
            "presumptively use serena",
            "cross-check semantic results",
        ),
        "semgrep": (
            "relation under the claim is structural",
            "do not route a purely literal lookup through semgrep",
            "do not use semgrep as a substitute for interprocedural/data-flow analysis",
            "cheap non-mutating capability probe when practical",
            "known-positive and known-negative",
            "actual scan contract",
        ),
        "hypothesis": (
            "meaningful input or state space",
            "small deterministic examples and already-exhaustive finite cases do not require hypothesis",
            "required coverage remains intact",
            "health-check suppression",
            "solely to make a property green",
        ),
        "codeql": (
            "optional specialist analyzer, not a generic security gate",
            "generic protocol validity does not require local codeql",
            "do not route a purely structural pattern to codeql",
            "security task is not automatically a codeql task",
            "runtime/dynamic/plugin/external-consumer behavior outside the database model",
        ),
    }
    return all(item in value for item in required[name])


class Protocol513OracleFamilyClosureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.roles = {
            "design": read("source/roles/software-design/SKILL.md"),
            "implementation": read("source/roles/software-implementation/SKILL.md"),
        }
        self.common = read("source/shared/references/tool-assisted-engineering.md")
        self.specialists = {
            "serena": read("source/shared/references/tool-serena.md"),
            "semgrep": read("source/shared/references/tool-semgrep.md"),
            "hypothesis": read("source/shared/references/tool-hypothesis.md"),
            "codeql": read("source/shared/references/tool-codeql.md"),
        }

    def test_current_hierarchical_routing_chain_is_accepted(self) -> None:
        for name, role in self.roles.items():
            with self.subTest(role=name):
                self.assertTrue(root_router_holds(role))
        self.assertTrue(common_router_holds(self.common))
        self.assertTrue(negative_pipeline_holds(self.common))
        for name, text in self.specialists.items():
            with self.subTest(owner=name):
                self.assertTrue(specialist_owner_holds(name, text))
        self.assertTrue(hypothesis_anti_gaming_holds(self.specialists["hypothesis"]))
        self.assertTrue(hypothesis_settings_holds(self.specialists["hypothesis"]))

    def test_flat_root_leaf_routing_regression_is_rejected(self) -> None:
        for name, role in self.roles.items():
            with self.subTest(role=name):
                self.assertFalse(root_router_holds(role + "\nRead [CodeQL](references/tool-codeql.md)."))
                self.assertFalse(root_router_holds(role.replace("references/tool-assisted-engineering.md", "references/tool-codeql.md")))

    def test_relation_class_inversions_are_rejected_at_canonical_router(self) -> None:
        mutations = (
            "All security tasks always route to CodeQL.",
            "Security always means CodeQL.",
            "Specialized analyzer output is exhaustive.",
            "Familiarity with Grep/Read/shell/tests is a valid fallback reason.",
        )
        for contradiction in mutations:
            with self.subTest(contradiction=contradiction):
                self.assertFalse(common_router_holds(self.common + "\n" + contradiction))

    def test_common_router_requires_every_preserved_relation_class(self) -> None:
        anchors = (
            "literal/path/text relation -> ordinary repository search/read",
            "symbol owner/definition/reference/caller relation -> Serena",
            "AST/syntax/structural relation -> Semgrep",
            "broad Python input/state invariant -> Hypothesis",
            "interprocedural flow/taint/source-to-sink relation -> CodeQL",
        )
        self.assertTrue(common_router_holds(self.common))
        for anchor in anchors:
            with self.subTest(anchor=anchor):
                self.assertFalse(common_router_holds(self.common.replace(anchor, "", 1)))

    def test_mandatory_pipeline_inversion_is_rejected(self) -> None:
        self.assertTrue(negative_pipeline_holds(self.common))
        mutated = mutate_paragraph(self.common, "mandatory three-tool pipeline", "A mandatory three-tool pipeline is required.")
        self.assertFalse(negative_pipeline_holds(mutated))

    def test_hypothesis_anti_gaming_inversions_are_rejected(self) -> None:
        text = self.specialists["hypothesis"]
        self.assertTrue(hypothesis_anti_gaming_holds(text))
        for mechanism in ANTI_GAMING:
            mutated = mutate_paragraph(text, "health-check suppression", f"{mechanism} may be used solely to make a property green.")
            with self.subTest(mechanism=mechanism):
                self.assertFalse(hypothesis_anti_gaming_holds(mutated))

    def test_hypothesis_settings_inversion_is_rejected(self) -> None:
        text = self.specialists["hypothesis"]
        self.assertTrue(hypothesis_settings_holds(text))
        mutated = text + "\nRequired coverage may then be discarded."
        self.assertFalse(hypothesis_settings_holds(mutated))

    def test_specialized_owner_boundaries_remain_distinct(self) -> None:
        serena = norm(self.specialists["serena"])
        semgrep = norm(self.specialists["semgrep"])
        hypothesis = norm(self.specialists["hypothesis"])
        codeql = norm(self.specialists["codeql"])
        self.assertIn("ordinary-search territory", serena)
        self.assertIn("structural", semgrep)
        self.assertIn("interprocedural/data-flow", semgrep)
        self.assertIn("broad/combinatorial", hypothesis)
        self.assertIn("interprocedural", codeql)
        self.assertIn("structural pattern", codeql)

    def test_model_limit_cross_check_stays_proportionate(self) -> None:
        self.assertIn("when those can hide material dependencies", norm(self.common))
        self.assertIn("do not invoke another tool merely to duplicate evidence", norm(self.common))
        mutated = self.common + "\nSpecialized analyzer output is exhaustive and never needs material cross-checking."
        self.assertFalse(common_router_holds(mutated))


if __name__ == "__main__":
    unittest.main()
