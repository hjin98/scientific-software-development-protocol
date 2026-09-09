from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class ProxyProofAcceptanceContractTests(unittest.TestCase):
    def test_testing_reference_is_canonical_proxy_proof_owner(self) -> None:
        text = read("source/shared/references/testing-and-validation.md").lower()
        for phrase in (
            "semantic owner under acceptance",
            "allowed test-double boundary",
            "proxy-proof acceptance",
            "could this evidence remain green",
            "cannot close the owner claim",
            "not a global ban on mocks or fakes",
        ):
            self.assertIn(phrase, text)

    def test_historical_proxy_substitutions_remain_rejected(self) -> None:
        text = read("source/shared/references/testing-and-validation.md").lower()
        for phrase in (
            "mocks, stubs, monkeypatches",
            "directly invokes a downstream helper",
            "seeds post-decision or post-transition state",
            "replaces durable/project persistence",
            "reimplements production compatibility",
            "helper-produced plan/result",
        ):
            self.assertIn(phrase, text)

    def test_bounded_fakes_below_real_owner_remain_valid(self) -> None:
        testing = read("source/shared/references/testing-and-validation.md").lower()
        implementation = read("source/roles/software-implementation/SKILL.md").lower()
        self.assertIn("bounded deterministic fixtures remain preferred", testing)
        self.assertIn("expensive ml/scientific training or prediction", testing)
        self.assertIn("bounded test doubles remain valid below or outside", implementation)
        self.assertIn("production-scale execution", testing)

    def test_unavailable_required_owner_boundary_is_not_proxy_passed(self) -> None:
        testing = read("source/shared/references/testing-and-validation.md").lower()
        implementation = read("source/roles/software-implementation/SKILL.md").lower()
        self.assertIn("unavailable/blocking", testing)
        self.assertIn("unavailable/blocking", implementation)
        self.assertIn("silently proxy-passing", implementation)

    def test_entrypoints_keep_only_salient_owner_trigger(self) -> None:
        design = read("source/roles/software-design/SKILL.md").lower()
        implementation = read("source/roles/software-implementation/SKILL.md").lower()
        for text in (design, implementation):
            self.assertIn("semantic owner", text)
            self.assertIn("references/testing-and-validation.md", text)
            self.assertIn("could remain green", text)
        self.assertIn("applicable accepted parent/cycle-scoped claim and the real semantic owner/path", design)
        self.assertIn("real semantic owner/path of the final accepted realization", implementation)

    def test_workplan_boundary_is_conditional_not_ceremonial(self) -> None:
        workflow = read("source/shared/references/workflow-and-workplans.md").lower()
        template = read("source/shared/templates/implementation_workplan_template.md").lower()
        self.assertIn("when material acceptance depends", workflow)
        self.assertIn("real production owner/consumer boundary", workflow)
        self.assertIn("acceptance boundary", template)
        self.assertIn("when proxy acceptance is a material risk", template)
        self.assertIn("attach only when material", template)

    def test_delegated_owner_replacement_remaps_acceptance_without_freezing_old_owner(self) -> None:
        testing = read("source/shared/references/testing-and-validation.md").lower()
        workflow = read("source/shared/references/workflow-and-workplans.md").lower()
        template = read("source/shared/templates/implementation_workplan_template.md").lower()
        implementation = read("source/roles/software-implementation/SKILL.md").lower()
        self.assertIn("acceptance does **not** make that lower-level owner durable authority", testing)
        self.assertIn("equivalent owner `b`", testing)
        self.assertIn("reconcile the acceptance mapping to the new real owner", testing)
        self.assertIn("accepted-current domain authority", workflow)
        self.assertIn("merely the current delegated realization", template)
        self.assertIn("final accepted realization", implementation)
        self.assertIn("do not treat that remapping as proxy-passing or design reopening", implementation)

    def test_targeted_guardrails_do_not_create_global_anti_mock_framework(self) -> None:
        text = read("source/shared/references/testing-and-validation.md").lower()
        self.assertIn("robust inexpensive structural/negative check", text)
        self.assertIn("do not require universal ast scanning", text)
        self.assertIn("global monkeypatch ban", text)
        self.assertIn("new anti-mocking framework", text)


if __name__ == "__main__":
    unittest.main()
