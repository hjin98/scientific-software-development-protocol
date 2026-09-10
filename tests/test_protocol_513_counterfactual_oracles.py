from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def norm(text: str) -> str:
    return text.lower().replace("**", "").replace("`", "")


def directional(text: str, required: tuple[str, ...], forbidden: tuple[str, ...]) -> bool:
    value = norm(text)
    return all(item in value for item in required) and not any(item in value for item in forbidden)


def check_pair(test: unittest.TestCase, predicate, positive: str, contradiction: str) -> None:
    test.assertTrue(predicate(positive), f"positive rejected by {predicate.__name__}")
    test.assertFalse(predicate(positive + " " + contradiction), f"contradiction accepted by {predicate.__name__}")


def root_dispatch_holds(text: str) -> bool:
    value = norm(text)
    leaves = ("tool-serena.md", "tool-semgrep.md", "tool-hypothesis.md", "tool-codeql.md")
    return (
        "references/tool-assisted-engineering.md" in value
        and "relation" in value
        and all(f"references/{leaf}" not in value for leaf in leaves)
        and "ordinary hyperlinks" in value
        and "activation" in value
    )


def concern_dispatch_holds(text: str) -> bool:
    return directional(
        text,
        (
            "relation under the current material claim",
            "literal/path/text relation -> ordinary repository search/read",
            "symbol owner/definition/reference/caller relation -> serena",
            "ast/syntax/structural relation -> semgrep",
            "broad python input/state invariant -> hypothesis",
            "interprocedural flow/taint/source-to-sink relation -> codeql",
            "a security task is not automatically a codeql task",
            "a forbidden-call pattern is structural",
            "multi-function untrusted-source-to-dangerous-sink claim is interprocedural data flow",
            "decompose a multi-relation claim",
            "minimum set of capabilities",
        ),
        (
            "all security tasks always route to codeql",
            "security always means codeql",
            "a forbidden-call pattern must use codeql",
            "source-to-sink is merely structural and should use semgrep",
        ),
    )


def fallback_holds(text: str) -> bool:
    return directional(
        text,
        (
            "available, current, supported, and directly models the claim",
            "presumptively use it",
            "fall back for a concrete reason",
            "familiarity with grep/read/shell/tests is not itself a fallback reason",
        ),
        (
            "familiarity with grep/read/shell/tests is a valid fallback reason",
            "skip the specialized capability merely because built-in tools are familiar",
        ),
    )


def pipeline_holds(text: str) -> bool:
    return directional(
        text,
        ("without becoming a mandatory three-tool pipeline",),
        (
            "a mandatory three-tool pipeline is required",
            "form a mandatory three-tool pipeline",
            "must use a mandatory three-tool pipeline",
        ),
    )


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
    value = norm(text)
    if "do not use" not in value or "solely to make a property green" not in value:
        return False
    if not all(item in value for item in ANTI_GAMING):
        return False
    return not any(
        phrase in value
        for item in ANTI_GAMING
        for phrase in (
            f"{item} is permitted solely to make a property green",
            f"{item} may be used solely to make a property green",
            f"{item} are allowed solely to make a property green",
            f"{item} is allowed solely to make a property green",
        )
    )


def hypothesis_settings_holds(text: str) -> bool:
    return directional(
        text,
        ("change settings when project/test semantics justify it", "required coverage remains intact"),
        (
            "required coverage is optional",
            "required coverage need not remain intact",
            "change settings when project/test semantics do not justify it",
        ),
    )


def codeql_optional_holds(text: str) -> bool:
    return directional(
        text,
        ("optional specialist analyzer, not a generic security gate", "generic protocol validity does not require local codeql"),
        ("generic protocol validity requires local codeql", "codeql is required for every task", "codeql is required for every security task"),
    )


def codeql_database_holds(text: str) -> bool:
    return directional(
        text,
        ("invalidate/rebuild", "changed source", "generated code", "build configuration", "dependency resolution", "do not reuse stale database results"),
        ("reuse stale database results after changed source", "stale database results are acceptable"),
    )


def codeql_custom_query_holds(text: str) -> bool:
    return directional(
        text,
        ("acceptance-critical custom query", "known-positive and known-negative", "before trusting its positive or zero result"),
        ("an acceptance-critical custom query may skip validation", "trust an acceptance-critical custom query without validation"),
    )


def codeql_zero_holds(text: str) -> bool:
    return directional(
        text,
        ("0 results or 0 alerts outcome is meaningful only relative to the actual database and query contract", "zero findings are not proof of absence outside that contract"),
        ("zero findings are proof of absence outside that contract", "0 results prove absence everywhere"),
    )


def codeql_provenance_holds(text: str) -> bool:
    return directional(
        text,
        (
            "local/external codeql execution",
            "github-managed codeql execution",
            "github code-scanning result/alert surface",
            "uploading sarif from the same local codeql run does not create a second analyzer execution",
            "only a separately executed github-managed/ci analysis is an independent run",
            "that exact required check must execute on the intended candidate/configuration",
            "a local run does not silently substitute for a required github-managed check",
        ),
        (
            "uploading sarif creates independent github-managed execution",
            "a local run substitutes for a required github-managed check",
            "stale hosted evidence is acceptable",
        ),
    )


def codeql_build_trust_holds(text: str) -> bool:
    return directional(
        text,
        ("treat this as privileged execution", "trust, supply-chain, resource, and subprocess rules", "avoid executing untrusted build hooks without an appropriate trust decision", "bound cpu/ram/disk/wall time"),
        ("codeql may execute untrusted build hooks without a trust decision", "build hooks do not require a trust decision"),
    )


class Protocol513CounterfactualOracleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.design = read("source/roles/software-design/SKILL.md")
        self.implementation = read("source/roles/software-implementation/SKILL.md")
        self.common = read("source/shared/references/tool-assisted-engineering.md")
        self.hypothesis = read("source/shared/references/tool-hypothesis.md")
        self.codeql = read("source/shared/references/tool-codeql.md")

    def test_actual_canonical_source_preserves_distributed_oracles(self) -> None:
        for role in (self.design, self.implementation):
            self.assertTrue(root_dispatch_holds(role))
        self.assertTrue(concern_dispatch_holds(self.common))
        self.assertTrue(fallback_holds(self.common))
        self.assertTrue(pipeline_holds(self.common))
        self.assertTrue(hypothesis_anti_gaming_holds(self.hypothesis))
        self.assertTrue(hypothesis_settings_holds(self.hypothesis))
        self.assertTrue(codeql_optional_holds(self.codeql))
        self.assertTrue(codeql_database_holds(self.codeql))
        self.assertTrue(codeql_custom_query_holds(self.codeql))
        self.assertTrue(codeql_zero_holds(self.codeql))
        self.assertTrue(codeql_provenance_holds(self.codeql))
        self.assertTrue(codeql_build_trust_holds(self.codeql))

    def test_root_dispatch_rejects_flat_leaf_reintroduction(self) -> None:
        for role in (self.design, self.implementation):
            self.assertFalse(root_dispatch_holds(role + "\nRead [CodeQL](references/tool-codeql.md)."))
            self.assertFalse(root_dispatch_holds(role.replace("references/tool-assisted-engineering.md", "references/tool-codeql.md")))

    def test_relation_first_overlap_polarity(self) -> None:
        positive = (
            "Classify the relation under the current material claim. Literal/path/text relation -> ordinary repository search/read. "
            "Symbol owner/definition/reference/caller relation -> Serena. AST/syntax/structural relation -> Semgrep. "
            "Broad Python input/state invariant -> Hypothesis. Interprocedural flow/taint/source-to-sink relation -> CodeQL. "
            "A security task is not automatically a CodeQL task: a forbidden-call pattern is structural, while a multi-function "
            "untrusted-source-to-dangerous-sink claim is interprocedural data flow. Decompose a multi-relation claim and choose the minimum set of capabilities."
        )
        check_pair(self, concern_dispatch_holds, positive, "All security tasks always route to CodeQL.")

    def test_fallback_polarity_preserves_concrete_fallbacks(self) -> None:
        positive = (
            "When the specialized capability is available, current, supported, and directly models the claim, presumptively use it. "
            "Fall back for a concrete reason such as unsupported language. Familiarity with Grep/Read/shell/tests is not itself a fallback reason."
        )
        check_pair(self, fallback_holds, positive, "Familiarity with Grep/Read/shell/tests is a valid fallback reason.")

    def test_pipeline_polarity(self) -> None:
        positive = "The tools can reinforce one another without becoming a mandatory three-tool pipeline."
        check_pair(self, pipeline_holds, positive, "A mandatory three-tool pipeline is required.")

    def test_hypothesis_anti_gaming_polarity(self) -> None:
        positive = (
            "Do not use excessive filtering or assume, over-narrow strategies, exclusions, health-check suppression, "
            "disabled useful phases, removed deadlines, or reduced exploration solely to make a property green."
        )
        self.assertTrue(hypothesis_anti_gaming_holds(positive))
        for mechanism in ANTI_GAMING:
            with self.subTest(mechanism=mechanism):
                self.assertFalse(hypothesis_anti_gaming_holds(positive + f" {mechanism} may be used solely to make a property green."))

    def test_hypothesis_settings_polarity(self) -> None:
        positive = "Change settings when project/test semantics justify it and required coverage remains intact."
        check_pair(self, hypothesis_settings_holds, positive, "Required coverage is optional.")

    def test_codeql_directional_oracles_reject_inversions(self) -> None:
        checks = (
            (codeql_optional_holds, "CodeQL is an optional specialist analyzer, not a generic security gate. Generic protocol validity does not require local CodeQL.", "Generic protocol validity requires local CodeQL."),
            (codeql_database_holds, "Invalidate/rebuild for changed source, generated code, build configuration, or dependency resolution. Do not reuse stale database results.", "Reuse stale database results after changed source."),
            (codeql_custom_query_holds, "For an acceptance-critical custom query, use known-positive and known-negative validation before trusting its positive or zero result.", "An acceptance-critical custom query may skip validation."),
            (codeql_zero_holds, "A 0 results or 0 alerts outcome is meaningful only relative to the actual database and query contract; zero findings are not proof of absence outside that contract.", "Zero findings are proof of absence outside that contract."),
            (codeql_provenance_holds, "Distinguish local/external CodeQL execution, GitHub-managed CodeQL execution, and GitHub code-scanning result/alert surface. Uploading SARIF from the same local CodeQL run does not create a second analyzer execution; only a separately executed GitHub-managed/CI analysis is an independent run. When that hosted check is required, that exact required check must execute on the intended candidate/configuration; a local run does not silently substitute for a required GitHub-managed check.", "A local run substitutes for a required GitHub-managed check."),
            (codeql_build_trust_holds, "Treat this as privileged execution under trust, supply-chain, resource, and subprocess rules. Avoid executing untrusted build hooks without an appropriate trust decision and bound CPU/RAM/disk/wall time.", "CodeQL may execute untrusted build hooks without a trust decision."),
        )
        for predicate, positive, contradiction in checks:
            with self.subTest(predicate=predicate.__name__):
                check_pair(self, predicate, positive, contradiction)


if __name__ == "__main__":
    unittest.main()
