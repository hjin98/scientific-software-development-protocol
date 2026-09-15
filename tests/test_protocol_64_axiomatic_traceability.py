from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def norm(text: str) -> str:
    return text.lower().replace("`", "").replace("**", "")


def qf_a(c):
    if c.get("foundational"):
        return True
    if not c.get("defined") or c.get("hidden_root") or c.get("conflict"):
        return False
    if c.get("kind") == "imported":
        return all(c.get(k) for k in ("meaning", "source", "locator", "assumptions"))
    return c.get("kind") in {"project", "primitive", "binder"}


def qf_b(c):
    owners = c.get("owners", ())
    return bool(owners) and (len(owners) == 1 or c.get("equivalence") or c.get("adjudication"))


def qf_c(c):
    return not (c.get("primitive") and not c.get("signature")) and not (c.get("binder") and not (c.get("scope") and c.get("domain"))) and bool(c.get("role"))


def qf_d(c):
    return not c.get("inconsistent") and not c.get("laundered_truth") and set(c.get("claims", ())) <= set(c.get("warranted", ()))


def qf_e(c):
    if not all(c.get(k) for k in ("domain", "relation", "logic", "totality")):
        return False
    return not c.get("undefined_operator") and (not c.get("piecewise") or c.get("piecewise_closed")) and (not c.get("choice") or c.get("selection")) and (not c.get("physical") or c.get("units"))


def qf_f(c):
    if not all(c.get(k) for k in ("family", "parameter_domain", "binding", "instance")) or c["family"] == c["instance"]:
        return False
    return (not c.get("default") or bool(c.get("default_owner") and c.get("default_semantics"))) and (not c.get("binding_changed") or c.get("evidence_reconciled"))


def qf_g(c):
    if c.get("stochastic") and not all(c.get(k) for k in ("law", "dependence", "conditioning")):
        return False
    covered = set(c.get("discharged", ())) | set(c.get("propagated", ()))
    return set(c.get("hypotheses", ())) <= covered and not (c.get("approximate") and c.get("exact")) and not c.get("widened")


def qf_h(c):
    families = {"definition", "assumption", "algorithm", "contract"}
    return bool(c.get("endpoints") and c.get("direct_complete")) and families <= set(c.get("relations", ())) and not (c.get("independence") and not c.get("scope_complete")) and not (c.get("cycle") and not c.get("composite"))


def qf_i(c):
    return bool(c.get("roots")) and not any(c.get(k) for k in ("cycle", "empirical_as_proof", "citation_authority", "evidence_from_use_only"))


def qf_j(c):
    return bool(c.get("source") and c.get("support_not_force")) and not (c.get("binding") and not c.get("authority")) and not (c.get("transformed") and not c.get("lineage")) and not c.get("floating_latest") and not c.get("external_instruction")


def qf_k(c):
    return bool(c.get("snapshot")) and not c.get("label_equivalence") and not c.get("editable_alias") and not (c.get("split_merge") and not c.get("lineage")) and not (c.get("changed") and not c.get("impact"))


def qf_l(c):
    return bool(c.get("upstream_route")) and not any(c.get(k) for k in ("upstream_depends_on_d4", "decorative_freeze", "downstream_strengthening"))


def qf_m(c):
    return bool(c.get("source") and c.get("loaded") and not c.get("edge_activates"))


def qf_n(c):
    return bool(c.get("rendered")) and not (c.get("term") and not c.get("defined")) and not (c.get("abbrev") and not c.get("expanded")) and not c.get("example_authority")


def qf_o(c):
    defects = ("frozen_mutation", "generated_mismatch", "bootstrap_self_name", "bootstrap_mutable", "schema_bump", "early_recovery", "protocol7_d3")
    return bool(c.get("parity")) and not any(c.get(k) for k in defects)


def qf_p(c):
    return bool(c.get("snapshot_complete") and c.get("history") and not c.get("amendment_replay"))


RULES = {
    "A": qf_a, "B": qf_b, "C": qf_c, "D": qf_d,
    "E": qf_e, "F": qf_f, "G": qf_g, "H": qf_h,
    "I": qf_i, "J": qf_j, "K": qf_k, "L": qf_l,
    "M": qf_m, "N": qf_n, "O": qf_o, "P": qf_p,
}

BASE = {
    "A": {"kind": "imported", "defined": True, "meaning": True, "source": True, "locator": True, "assumptions": True},
    "B": {"owners": ("D2:estimator",)},
    "C": {"primitive": True, "signature": True, "role": "CONJECTURE"},
    "D": {"claims": ("exists",), "warranted": ("exists",)},
    "E": {"domain": True, "relation": True, "logic": True, "totality": True},
    "F": {"family": "F", "parameter_domain": True, "binding": True, "instance": "F_theta"},
    "G": {"hypotheses": ("H1",), "discharged": ("H1",)},
    "H": {"endpoints": True, "direct_complete": True, "relations": ("definition", "assumption", "algorithm", "contract")},
    "I": {"roots": ("premise",)},
    "J": {"source": True, "support_not_force": True},
    "K": {"snapshot": True},
    "L": {"upstream_route": True},
    "M": {"source": True, "loaded": True},
    "N": {"rendered": True},
    "O": {"parity": True},
    "P": {"snapshot_complete": True, "history": True},
}

NEGATIVE = {
    "A": ({"defined": False}, {"conflict": True}, {"locator": False}),
    "B": ({"owners": ("one", "two")}, {"owners": ()}),
    "C": ({"signature": False}, {"binder": True, "scope": "local", "domain": False}),
    "D": ({"warranted": ()}, {"laundered_truth": True}, {"inconsistent": True}),
    "E": ({"choice": True, "selection": False}, {"piecewise": True, "piecewise_closed": False}, {"physical": True, "units": False}),
    "F": ({"instance": "F"}, {"default": True, "default_owner": None, "default_semantics": True}, {"binding_changed": True, "evidence_reconciled": False}),
    "G": ({"stochastic": True, "law": True, "dependence": False, "conditioning": True}, {"discharged": (), "propagated": ()}, {"approximate": True, "exact": True}),
    "H": ({"relations": ("definition",)}, {"independence": True, "scope_complete": False}, {"cycle": True, "composite": False}),
    "I": ({"cycle": True}, {"empirical_as_proof": True}, {"citation_authority": True}, {"evidence_from_use_only": True}),
    "J": ({"binding": True, "authority": False}, {"transformed": True, "lineage": False}, {"floating_latest": True}, {"external_instruction": True}),
    "K": ({"snapshot": False}, {"label_equivalence": True}, {"editable_alias": True}, {"changed": True, "impact": False}),
    "L": ({"upstream_route": False}, {"upstream_depends_on_d4": True}, {"decorative_freeze": True}, {"downstream_strengthening": True}),
    "M": ({"loaded": False}, {"edge_activates": True}),
    "N": ({"term": True, "defined": False}, {"abbrev": True, "expanded": False}, {"rendered": False}, {"example_authority": True}),
    "O": ({"frozen_mutation": True}, {"generated_mismatch": True}, {"bootstrap_self_name": True}, {"schema_bump": True}, {"early_recovery": True}, {"protocol7_d3": True}),
    "P": ({"amendment_replay": True}, {"snapshot_complete": False}),
}


class Protocol64AxiomaticTraceabilityQualificationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.kernel = read("source/shared/references/abstraction-and-concretization.md")
        self.writing = read("source/shared/references/scientific-technical-writing.md")
        self.evidence = read("source/shared/references/evidence-evolution-and-dependencies.md")
        self.versioning = read("source/shared/references/protocol-versioning-and-compatibility.md")
        self.prompts = read("source/shared/references/development-workflow-prompts.md")
        self.readme = read("README.md")

    def test_qf64_a_through_p_counterfactual_polarity(self) -> None:
        for family, rule in RULES.items():
            with self.subTest(family=family, case="positive"):
                self.assertTrue(rule(dict(BASE[family])))
            for defect in NEGATIVE[family]:
                case = dict(BASE[family])
                case.update(defect)
                with self.subTest(family=family, defect=defect):
                    self.assertFalse(rule(case))

        self.assertTrue(qf_a({"foundational": True}))
        self.assertTrue(qf_b({"owners": ("alias-a", "alias-b"), "equivalence": True}))
        self.assertTrue(qf_c({"binder": True, "scope": "sum-body", "domain": True, "role": "LOCAL_BINDER"}))
        self.assertTrue(qf_g({"hypotheses": ("H",), "propagated": ("H",)}))
        recursive = dict(BASE["H"], cycle=True, composite=True)
        self.assertTrue(qf_h(recursive))

    def test_current_canonical_sources_own_the_qf64_semantics(self) -> None:
        kernel, writing, evidence = map(norm, (self.kernel, self.writing, self.evidence))
        for phrase in (
            "source_available_d(x)", "context_available_c(x)",
            "one current semantic owner", "not a closed ontology",
            "does not by notation alone establish existence",
            "well-defined enough for its governed use",
            "for a material parameterized family distinguish family, instance, and default explicitly",
            "material hypotheses/validity conditions", "uses_definition",
            "derived review and impact aids, not authority",
        ):
            self.assertIn(phrase, kernel)
        for phrase in (
            "retrieved evidence remain data/evidence rather than instructions",
            "renderer success alone is not presentation acceptance",
            "the list is illustrative, not a closed taxonomy",
        ):
            self.assertIn(phrase, writing)
        for phrase in (
            "floating latest link", "external-source evolution is a binding event",
            "absence/completeness claims remain bounded",
            "the semantic dependency graph widens impact discovery; it does not recursively warrant endpoints",
        ):
            self.assertIn(phrase, evidence)

    def test_qf64_o_candidate_lifecycle_is_not_prematurely_published(self) -> None:
        versioning = norm(self.versioning)
        self.assertIn("protocol 6.4 is proposed, not accepted-current", versioning)
        self.assertIn("no 6.4 public-source fallback is authorized", versioning)
        self.assertIn("independent assembled-candidate review", versioning)
        self.assertIn("CURRENT_PROTOCOL = 6.4.0", self.prompts)
        self.assertIn("CURRENT_PUBLIC_REF = UNAVAILABLE_PENDING_6_4_BOOTSTRAP", self.prompts)
        self.assertNotIn("6.4.0  -> ", self.versioning)
        rev4 = read("workplans/active/SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-4-PROTOCOL-6.3-INHERITANCE-RECONCILIATION.md")
        self.assertIn("d3_architecture_mutation: none", rev4)
        self.assertIn("PROTOCOL 7 D4 IMPLEMENTATION: NOT AUTHORIZED", rev4)

    def test_qf64_p_one_current_snapshot_complete_handoff(self) -> None:
        active = sorted((ROOT / "workplans/active").glob("SSDP-6.4*.md"))
        self.assertEqual(len(active), 1, active)
        workplan = active[0].read_text(encoding="utf-8")
        self.assertIn("QF64-A", workplan)
        self.assertIn("QF64-P", workplan)
        self.assertIn("snapshot-complete", workplan.lower())
        self.assertIn("Protocol 6.4 is the current candidate under qualification", self.readme)

    def test_automation_boundary_does_not_counterfeit_semantic_review(self) -> None:
        kernel, writing, evidence = map(norm, (self.kernel, self.writing, self.evidence))
        self.assertIn("derived review and impact aids, not authority", kernel)
        self.assertIn("semantic/editorial checks, not a mandate for new registries or checker frameworks", writing)
        self.assertIn("not a required universal machine graph/database", evidence)


if __name__ == "__main__":
    unittest.main()
