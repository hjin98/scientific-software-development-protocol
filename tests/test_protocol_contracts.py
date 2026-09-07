from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class ProtocolContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.design = read("source/roles/software-design/SKILL.md").lower()
        self.implementation = read("source/roles/software-implementation/SKILL.md").lower()
        self.workflow = read("source/shared/references/workflow-and-workplans.md").lower()
        self.architecture = read("source/shared/references/architecture-and-design.md").lower()
        self.convergence = read("source/shared/references/convergence-and-cycle-economy.md").lower()
        self.template = read("source/shared/templates/implementation_workplan_template.md").lower()
        self.versioning = read("source/shared/references/protocol-versioning-and-compatibility.md").lower()

    def test_protocol_516_identity_and_two_role_lifecycle(self) -> None:
        self.assertEqual("5.16.0", read("source/PROTOCOL_VERSION").strip())
        source_readme = read("source/README.md").lower()
        root_readme = read("README.md").lower()
        self.assertIn("software development protocol 5.16", source_readme)
        self.assertIn("current protocol version: **5.16**", root_readme)
        self.assertIn("protocol 5.16 is a backward-compatible", self.versioning)
        for historical in (
            "protocol 5.15 is a backward-compatible",
            "protocol 5.14 is a backward-compatible",
            "protocol 5.13 is a backward-compatible",
            "protocol 5.12 is a backward-compatible",
            "protocol 5.11 is a backward-compatible",
            "protocol 5.10 is a backward-compatible",
            "protocol 5.9 is a backward-compatible",
        ):
            self.assertIn(historical, self.versioning)
        self.assertIn("software-design -> software-implementation", source_readme)

    def test_governing_hierarchy_and_product_truth_remain_entrypoint_critical(self) -> None:
        hierarchy = "product engineering fitness > minimum justified product/system complexity > development economy"
        for text in (self.design, self.implementation):
            self.assertIn(hierarchy, text)
            self.assertIn("stakeholder", text)
            self.assertIn("truthful non-closure", text)
        self.assertIn("non-adversarially", self.design)
        self.assertIn("counterfeit completion", self.implementation)

    def test_tier1_problem_and_frozen_architecture_are_distinct_from_tier2_solution(self) -> None:
        for text in (self.design, self.architecture):
            self.assertIn("intrinsic product/problem", text)
            self.assertIn("frozen high-level architecture", text)
            self.assertIn("delegated solution", text)
        self.assertIn("tier 2 — delegated solution space", self.design)
        self.assertIn("tier 2: delegated solution machinery", self.architecture)
        self.assertIn("correctness of a currently used mechanism is not evidence of necessity", self.architecture)

    def test_implementation_history_cannot_promote_solution_to_invariant(self) -> None:
        for text in (self.design, self.implementation, self.architecture):
            self.assertIn("dependency", text)
            self.assertIn("tests", text)
            self.assertIn("documentation", text)
        self.assertIn("do not promote implementation machinery into tier 1", self.design)
        self.assertIn("implementation history does not promote machinery into tier 1", self.implementation)
        self.assertIn("acquire tier-1 authority", self.architecture)

    def test_solution_created_problem_can_be_removed_instead_of_patched(self) -> None:
        self.assertIn("a problem created only by the current tier-2 realization is itself a tier-2 problem", self.design)
        self.assertIn("a problem caused only by the current realization is a tier-2 problem", self.implementation)
        self.assertIn("solution-created problems are not product invariants", self.architecture)
        self.assertIn("removes one representation", self.architecture)

    def test_active_simplicity_is_mandatory_on_structural_complexity_evidence(self) -> None:
        for text in (self.design, self.implementation, self.architecture):
            self.assertIn("mandatory before another additive durable repair", text)
        self.assertIn("before another additive durable repair", self.convergence)
        self.assertIn("mandatory", self.convergence)
        for phrase in ("repeated patches", "duplicated", "wrappers", "fallbacks", "materially simpler"):
            self.assertIn(phrase, self.architecture)
        self.assertIn("remove / narrow / alter / consolidate / refactor", self.architecture)
        self.assertIn("genuinely missing required capability", self.architecture)

    def test_justified_abstraction_and_explicit_promotion_survive(self) -> None:
        self.assertIn("one canonical mechanism", self.architecture)
        self.assertIn("reduces total system complexity", self.architecture)
        self.assertIn("promotion from tier 2 to frozen architecture requires explicit design acceptance", self.architecture)
        self.assertIn("explicit design decision", self.design)

    def test_affected_surface_is_not_requirement_surface(self) -> None:
        for text in (self.design, self.implementation, self.workflow):
            self.assertIn("affected-surface", text)
        self.assertIn("affected-surface expansion is not requirement expansion", self.workflow)
        self.assertIn("does not itself create a new product requirement", self.implementation)
        self.assertIn("does not by itself create a new product capability", self.workflow)

    def test_minimum_known_contract_is_narrowed_to_parent_authority(self) -> None:
        for text in (self.design, self.implementation, self.workflow):
            self.assertIn("minimum known contract, not a ceiling", text)
            self.assertIn("newly discovered affected behavior", text)
        self.assertIn("discovery does not mint new product requirements", self.design)
        self.assertIn("discovery does not mint a new product requirement", self.implementation)
        self.assertNotIn("required implementation consequence is not optional advice", self.workflow)

    def test_workplan_template_forces_problem_architecture_solution_boundary(self) -> None:
        for heading in (
            "objective / problem invariants / non-goals",
            "frozen high-level architecture and engineering envelope",
            "implementation obligations and delegated solution space",
            "implementation authority",
            "affected surface and task-specific acceptance",
            "implementation sequence and genuine redesign / simplification triggers",
        ):
            self.assertIn(heading, self.template)
        self.assertIn("what high-level architecture is deliberately frozen", self.template)
        self.assertIn("which details are intentionally **not** frozen", self.template)
        self.assertIn("what existing machinery/state/path should be removed", self.template)
        self.assertNotIn("## conditional convergence guidance", self.template)
        self.assertNotIn("## handoff closure", self.template)

    def test_frozen_architecture_stability_and_bounded_reopen_are_preserved(self) -> None:
        self.assertIn("material redesign", self.implementation)
        self.assertIn("representative measurement invalidating a premise", self.implementation)
        self.assertIn("reopen only the affected surface", self.implementation)
        self.assertIn("do not reopen unrelated design", self.implementation)
        self.assertIn("cycle-scoped frozen architecture", self.architecture)

    def test_convergence_is_subordinate_to_simplicity_not_mechanism_preservation(self) -> None:
        self.assertIn("recurrence is evidence about the shared owner/mechanism", self.architecture)
        self.assertIn("it is not evidence that the current realization should survive", self.architecture)
        self.assertIn("first clean local defect remains local", self.convergence)
        self.assertIn("material sibling recurrence", self.convergence)
        self.assertIn("re-derive and simplify the tier-2 realization", self.convergence)
        self.assertIn("tier-1 correctness claim is finite/exhaustive", self.convergence)
        self.assertIn("do not require completion of an existing \"canonical realization\"", self.convergence)

    def test_proxy_proof_and_functional_acceptance_remain_intact(self) -> None:
        testing = read("source/shared/references/testing-and-validation.md").lower()
        self.assertIn("semantic owner under acceptance", testing)
        self.assertIn("proxy-proof acceptance", testing)
        self.assertIn("stage-local affected regression", self.implementation)
        self.assertIn("complete affected-surface regression", self.implementation)
        self.assertIn("integration/end-to-end", self.implementation)
        self.assertIn("production qualification is separate", self.implementation)

    def test_snapshot_complete_handoff_and_revision_economy_remain_intact(self) -> None:
        self.assertIn("snapshot-complete", self.workflow)
        self.assertIn("snapshot-loss counterfactual", self.workflow)
        self.assertIn("workplan/design deficiency", self.implementation)
        self.assertIn("ordinary implementation attempts and review cycles do not require a numbered authority revision", self.convergence)

    def test_protocol_513_tool_routing_is_preserved(self) -> None:
        for text in (self.design, self.implementation):
            self.assertIn("classify each material engineering question by the relation under the claim, not once per task", text)
            for ref in ("tool-serena.md", "tool-semgrep.md", "tool-hypothesis.md", "tool-codeql.md"):
                line = next(line for line in text.splitlines() if ref in line)
                self.assertIn("must read", line)
            self.assertIn("cheap non-mutating capability probe", text)
            self.assertIn("presumptively use it", text)
            self.assertIn("concrete fallback", text)

    def test_acceptance_evidence_does_not_promote_tier2_owner(self) -> None:
        testing = read("source/shared/references/testing-and-validation.md").lower()
        self.assertIn("actual production owner", testing)
        self.assertIn("does **not** become frozen", testing)
        self.assertIn("local reconciliation, not proxy-passing", testing)
        self.assertIn("exact owner/path identity is binding only when", testing)
        self.assertIn("do not elevate a delegated tier-2 owner into frozen authority", self.workflow)
        self.assertIn("do not freeze a tier-2 owner merely because current acceptance executes it", self.template)

    def test_no_new_simplicity_bureaucracy_is_implied(self) -> None:
        combined = "\n".join((self.design, self.implementation, self.workflow, self.architecture, self.convergence, self.template))
        for forbidden in (
            "simplicity score",
            "complexity ledger",
            "mandatory refactoring report",
            "deletion quota",
        ):
            self.assertNotIn(forbidden, combined)
        self.assertIn("not a line-count rule", self.implementation)
        self.assertIn("not a required persistent artifact", self.workflow)


if __name__ == "__main__":
    unittest.main()
