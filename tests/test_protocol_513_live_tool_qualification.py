from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8").lower()


class Protocol513LiveToolQualificationTests(unittest.TestCase):
    def test_portability_separates_static_reference_and_live_tool_routing_claims(self) -> None:
        text = read("PORTABILITY.md")
        self.assertIn("reference-routing sentinel", text)
        self.assertIn("tool-routing qualification", text)
        self.assertIn("static package/routing validation", text)
        self.assertIn("cannot prove", text)
        self.assertIn("named harness/model/install mode", text)
        self.assertIn("do not infer another environment from one run", text)

    def test_live_scenarios_cover_each_specialized_class_and_non_silent_fallback(self) -> None:
        text = read("qualification/tool-routing/SCENARIOS.md")
        for phrase in (
            "serena initiating regression",
            "semgrep structural-variant scenario",
            "hypothesis property/state scenario",
            "codeql interprocedural-flow scenario",
            "direct tool-specific reference read",
            "specialized tool invocation or concrete permitted fallback",
            "silent preference for built-in",
            "not a permitted fallback",
        ):
            self.assertIn(phrase, text)

    def test_live_qualification_does_not_infer_unrun_harness_tool_combinations(self) -> None:
        portability = read("PORTABILITY.md")
        scenarios = read("qualification/tool-routing/SCENARIOS.md")
        self.assertIn("do not infer another environment from one run", portability)
        self.assertIn("never generalize one result to another harness/model/tool combination", scenarios)
        self.assertIn("unqualified", scenarios)

    def test_serena_scenario_is_the_initiating_regression(self) -> None:
        text = read("qualification/tool-routing/SCENARIOS.md")
        self.assertIn("minimum live regression", text)
        self.assertIn("definition/semantic owner", text)
        self.assertIn("callers/references", text)
        self.assertIn("symbol/reference/caller", text)
        self.assertIn("references/tool-serena.md", text)
        self.assertIn("serena semantic", text)


if __name__ == "__main__":
    unittest.main()
