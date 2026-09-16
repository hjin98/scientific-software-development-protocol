from __future__ import annotations

import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def norm(text: str) -> str:
    return text.lower().replace("`", "").replace("**", "")


def front_matter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    block = text.split("---\n", 2)[1]
    result: dict[str, str] = {}
    for line in block.splitlines():
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip().strip('"').strip("'")
    return result


def protocol64_authority_index_state(text: str) -> dict[str, str]:
    start_marker = "## Protocol 6.4 current design handoff"
    end_marker = "## Protocol 7.0 current design handoff"
    start = text.find(start_marker)
    end = text.find(end_marker, start + len(start_marker)) if start >= 0 else -1
    if start < 0 or end < 0:
        return {}
    section = text[start:end]
    match = re.search(r"Current disposition:\s*```text\n(.*?)\n```", section, re.DOTALL)
    if not match:
        return {}
    state: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        state[key.strip()] = value.strip()
    return state


def protocol64_stage_e_phase(state: dict[str, str]) -> str | None:
    review = state.get("STAGE E INDEPENDENT REVIEW", "")
    if review.startswith("NO-PASS") and "REPAIR REQUIRED" in review and "FRESH REVIEW REQUIRED" in review:
        return "repair-required"
    if review == "REPAIR COMPLETE / EXACT-TARGET QUALIFICATION REQUIRED":
        return "repair-complete"
    if review == "REVIEW READY / FRESH REVIEW REQUIRED":
        return "review-ready"
    if review == "PASS / STAGE F AUTHORIZED":
        return "pass"
    return None


def protocol64_lifecycle_state_ok(state: dict[str, str]) -> bool:
    phase = protocol64_stage_e_phase(state)
    stable = bool(
        state.get("IMPLEMENTATION / STAGE C QUALIFICATION") == "COMPLETE / QUALIFIED"
        and state.get("STAGE D PUBLIC BOOTSTRAP")
        == "PUBLISHED / AUTHORIZED - e09a9d1480211eea2d16d722182bb5c6de1bee12"
        and state.get("CURRENT ACCEPTED DOCUMENT-CONTROLLED BASELINE") == "Protocol 6.3"
        and phase is not None
    )
    if not stable:
        return False
    if phase == "pass":
        return bool(
            state.get("PROTOCOL 6.4 RECOVERY") == "UNAVAILABLE PENDING STAGE F RECOVERY PUBLICATION"
            and state.get("STAGE F") == "AUTHORIZED"
        )
    return bool(
        state.get("PROTOCOL 6.4 RECOVERY") == "UNAVAILABLE PENDING INDEPENDENT REVIEW PASS"
        and state.get("STAGE F") == "BLOCKED"
    )


def protocol64_handoff_lifecycle_ok(state: dict[str, str], handoff_meta: dict[str, str]) -> bool:
    phase = protocol64_stage_e_phase(state)
    if phase is None:
        return False

    binding_state = handoff_meta.get("review_target_binding_state")
    target = handoff_meta.get("assembled_review_target", "")
    qualification = handoff_meta.get("assembled_review_target_ci", "")
    if phase == "repair-complete":
        binding_ok = bool(
            binding_state == "pending-descendant-handoff"
            and target == "PENDING_DESCENDANT_HANDOFF"
            and qualification == "PENDING_EXACT_TARGET_CI"
        )
    else:
        binding_ok = bool(
            binding_state == "bound"
            and re.fullmatch(r"[0-9a-f]{40}", target)
            and re.fullmatch(r"[0-9]+", qualification)
        )
    if not binding_ok:
        return False

    if phase == "pass":
        return bool(
            handoff_meta.get("protocol_64_recovery") == "unavailable_pending_stage_f_recovery_publication"
            and handoff_meta.get("stage_f") == "authorized"
        )
    return bool(
        handoff_meta.get("protocol_64_recovery") == "unavailable_pending_independent_review"
        and handoff_meta.get("stage_f") == "blocked_pending_independent_review"
    )


def markdown_fences_well_formed(text: str) -> bool:
    active: tuple[str, int] | None = None
    for line in text.splitlines():
        if active is None:
            match = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
            if match:
                fence = match.group(1)
                active = (fence[0], len(fence))
            continue

        char, minimum = active
        candidate = re.match(rf"^ {{0,3}}({re.escape(char)}{{{minimum},}})(.*)$", line)
        if not candidate:
            continue
        if candidate.group(2).strip():
            return False
        active = None
    return active is None


def qf_a(c):
    if c.get("foundational"):
        return True
    if not c.get("defined") or c.get("hidden_root") or c.get("conflict"):
        return False
    if c.get("kind") == "imported":
        required = ("meaning", "source", "locator", "assumptions", "variant", "source_version")
        return bool(
            all(c.get(k) for k in required)
            and c.get("version_matches")
            and c.get("support_assessed")
            and c.get("supported")
        )
    return c.get("kind") in {"project", "primitive", "binder"}


def qf_b(c):
    owners = c.get("owners", ())
    return bool(owners) and (len(owners) == 1 or c.get("equivalence") or c.get("adjudication"))


def qf_c(c):
    return bool(
        not c.get("ambiguous_shadowing")
        and not c.get("provenance_role_conflated")
        and not (c.get("primitive") and not c.get("signature"))
        and not (c.get("binder") and not (c.get("scope") and c.get("domain")))
        and c.get("availability_basis")
        and c.get("role")
    )


def qf_d(c):
    return not c.get("inconsistent") and not c.get("laundered_truth") and set(c.get("claims", ())) <= set(c.get("warranted", ()))


def qf_e(c):
    if not all(c.get(k) for k in ("domain", "relation", "logic", "totality")):
        return False
    return bool(
        not c.get("undefined_operator")
        and not c.get("branch_ambiguous")
        and not c.get("state_time_order_ambiguous")
        and (not c.get("piecewise") or c.get("piecewise_closed"))
        and (not c.get("choice") or c.get("selection"))
        and (not c.get("physical") or c.get("units"))
    )


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
    required_subject_classes = {"definition", "theorem_result", "assumption", "algorithm", "contract"}
    if not bool(c.get("endpoints") and c.get("direct_complete")):
        return False
    if required_subject_classes - set(c.get("subject_classes", ())):
        return False
    if c.get("relation_kind") != "USES_DEFINITION" or c.get("edge_basis") != "semantic_meaning_prerequisite":
        return False
    if c.get("uses_definition") != (c.get("subject"), c.get("prerequisite")):
        return False
    if c.get("impact_from") != c.get("prerequisite"):
        return False
    if c.get("subject") not in set(c.get("impact_dependents", ())):
        return False
    return not (c.get("independence") and not c.get("scope_complete")) and not (c.get("cycle") and not c.get("composite"))


def qf_i(c):
    return bool(c.get("roots")) and not any(c.get(k) for k in ("cycle", "empirical_as_proof", "citation_authority", "evidence_from_use_only"))


def qf_j(c):
    return bool(c.get("source") and c.get("support_not_force")) and not (c.get("binding") and not c.get("authority")) and not (c.get("transformed") and not c.get("lineage")) and not c.get("floating_latest") and not c.get("external_instruction")


def qf_k(c):
    return bool(c.get("snapshot")) and not c.get("label_equivalence") and not c.get("editable_alias") and not (c.get("split_merge") and not c.get("lineage")) and not (c.get("changed") and not c.get("impact"))


def qf_l(c):
    return bool(c.get("upstream_route")) and not any(c.get(k) for k in ("upstream_depends_on_d4", "decorative_freeze", "downstream_strengthening"))


def qf_m(c):
    return bool(
        c.get("source")
        and c.get("loaded")
        and c.get("required_owner")
        and c.get("loaded_owner") == c.get("required_owner")
        and not c.get("edge_activates")
    )


def qf_n(c):
    return bool(c.get("rendered")) and not (c.get("term") and not c.get("defined")) and not (c.get("abbrev") and not c.get("expanded")) and not c.get("example_authority")


def qf_o(c):
    defects = ("frozen_mutation", "generated_mismatch", "bootstrap_self_name", "bootstrap_mutable", "schema_bump", "early_recovery", "protocol7_d3")
    return bool(c.get("parity")) and not any(c.get(k) for k in defects)


def qf_p(c):
    return bool(
        c.get("snapshot_complete")
        and c.get("history")
        and c.get("current_handoff")
        and c.get("baseline_consistent")
        and c.get("target_binding")
        and c.get("qualification_binding")
        and c.get("lifecycle_index_current")
        and not c.get("stale_lifecycle_state")
        and not c.get("amendment_replay")
    )


RULES = {
    "A": qf_a, "B": qf_b, "C": qf_c, "D": qf_d,
    "E": qf_e, "F": qf_f, "G": qf_g, "H": qf_h,
    "I": qf_i, "J": qf_j, "K": qf_k, "L": qf_l,
    "M": qf_m, "N": qf_n, "O": qf_o, "P": qf_p,
}

BASE = {
    "A": {"kind": "imported", "defined": True, "meaning": True, "source": True, "locator": True, "assumptions": True, "variant": "theorem-v2", "source_version": "2026-edition", "version_matches": True, "support_assessed": True, "supported": True},
    "B": {"owners": ("D2:estimator",)},
    "C": {"primitive": True, "signature": True, "availability_basis": "PROJECT_DECLARED", "role": "CONJECTURE"},
    "D": {"claims": ("exists",), "warranted": ("exists",)},
    "E": {"domain": True, "relation": True, "logic": True, "totality": True},
    "F": {"family": "F", "parameter_domain": True, "binding": True, "instance": "F_theta"},
    "G": {"hypotheses": ("H1",), "discharged": ("H1",)},
    "H": {"endpoints": True, "direct_complete": True, "subject_classes": ("definition", "theorem_result", "assumption", "algorithm", "contract"), "relation_kind": "USES_DEFINITION", "edge_basis": "semantic_meaning_prerequisite", "subject": "algorithm-A", "prerequisite": "definition-X", "uses_definition": ("algorithm-A", "definition-X"), "impact_from": "definition-X", "impact_dependents": ("algorithm-A",)},
    "I": {"roots": ("premise",)},
    "J": {"source": True, "support_not_force": True},
    "K": {"snapshot": True},
    "L": {"upstream_route": True},
    "M": {"source": True, "loaded": True, "required_owner": ("D1:observable", "6.4.0"), "loaded_owner": ("D1:observable", "6.4.0")},
    "N": {"rendered": True},
    "O": {"parity": True},
    "P": {"snapshot_complete": True, "history": True, "current_handoff": True, "baseline_consistent": True, "target_binding": True, "qualification_binding": True, "lifecycle_index_current": True},
}

NEGATIVE = {
    "A": ({"defined": False}, {"conflict": True}, {"locator": False}, {"version_matches": False}, {"support_assessed": False}, {"supported": False}),
    "B": ({"owners": ("one", "two")}, {"owners": ()}),
    "C": ({"signature": False}, {"binder": True, "scope": "local", "domain": False}, {"ambiguous_shadowing": True}, {"provenance_role_conflated": True}, {"availability_basis": None}),
    "D": ({"warranted": ()}, {"laundered_truth": True}, {"inconsistent": True}),
    "E": ({"relation": False}, {"logic": False}, {"totality": False}, {"undefined_operator": True}, {"branch_ambiguous": True}, {"state_time_order_ambiguous": True}, {"choice": True, "selection": False}, {"piecewise": True, "piecewise_closed": False}, {"physical": True, "units": False}),
    "F": ({"instance": "F"}, {"default": True, "default_owner": None, "default_semantics": True}, {"binding_changed": True, "evidence_reconciled": False}),
    "G": ({"stochastic": True, "law": True, "dependence": False, "conditioning": True}, {"discharged": (), "propagated": ()}, {"approximate": True, "exact": True}, {"widened": True}),
    "H": ({"subject_classes": ("definition", "assumption", "algorithm", "contract")}, {"subject_classes": ("definition",)}, {"uses_definition": ("definition-X", "algorithm-A")}, {"impact_dependents": ()}, {"independence": True, "scope_complete": False}, {"cycle": True, "composite": False}, {"edge_basis": "hyperlink"}, {"edge_basis": "import_graph"}, {"edge_basis": "call_graph"}, {"edge_basis": "evidence_dependency"}, {"edge_basis": "execution_dependency"}),
    "I": ({"cycle": True}, {"empirical_as_proof": True}, {"citation_authority": True}, {"evidence_from_use_only": True}),
    "J": ({"binding": True, "authority": False}, {"transformed": True, "lineage": False}, {"floating_latest": True}, {"external_instruction": True}),
    "K": ({"snapshot": False}, {"label_equivalence": True}, {"editable_alias": True}, {"changed": True, "impact": False}, {"split_merge": True, "lineage": False}),
    "L": ({"upstream_route": False}, {"upstream_depends_on_d4": True}, {"decorative_freeze": True}, {"downstream_strengthening": True}),
    "M": ({"loaded": False}, {"edge_activates": True}, {"loaded_owner": ("D1:observable", "6.3.0")}, {"loaded_owner": ("D1:similarly-named-observable", "6.4.0")}),
    "N": ({"term": True, "defined": False}, {"abbrev": True, "expanded": False}, {"rendered": False}, {"example_authority": True}),
    "O": ({"frozen_mutation": True}, {"generated_mismatch": True}, {"bootstrap_self_name": True}, {"schema_bump": True}, {"early_recovery": True}, {"protocol7_d3": True}),
    "P": ({"amendment_replay": True}, {"snapshot_complete": False}, {"current_handoff": False}, {"baseline_consistent": False}, {"target_binding": False}, {"qualification_binding": False}, {"lifecycle_index_current": False}, {"stale_lifecycle_state": True}),
}


class Protocol64AxiomaticTraceabilityQualificationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.kernel = read("source/shared/references/abstraction-and-concretization.md")
        self.writing = read("source/shared/references/scientific-technical-writing.md")
        self.evidence = read("source/shared/references/evidence-evolution-and-dependencies.md")
        self.versioning = read("source/shared/references/protocol-versioning-and-compatibility.md")
        self.prompts = read("source/shared/references/development-workflow-prompts.md")
        self.semantic_dependencies = read("source/SEMANTIC_DEPENDENCIES.md")
        self.readme = read("README.md")
        self.authority_index = read("workplans/active/SSDP-6.1-7.0-WORKPLAN-AUTHORITY-INDEX.md")

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
        self.assertTrue(qf_c({"binder": True, "scope": "sum-body", "domain": True, "availability_basis": "PROJECT_DECLARED", "role": "LOCAL_BINDER"}))
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
            "stored edge direction is subject -> prerequisite",
            "reverse traversal",
        ):
            self.assertIn(phrase, evidence)
        self.assertIn("stored relation direction is therefore subject -> prerequisite", kernel)
        self.assertIn("stored relation as subject -> prerequisite", writing)
        semantic_dependencies = norm(self.semantic_dependencies)
        self.assertIn("stored as subject -> prerequisite", semantic_dependencies)
        self.assertIn("reverse traversal", semantic_dependencies)
        self.assertIn("stored uses_definition direction is subject -> prerequisite", norm(self.prompts))

    def test_qf64_n_real_markdown_fence_integrity(self) -> None:
        surfaces = [
            ROOT / "source/shared/references/abstraction-and-concretization.md",
            ROOT / "source/shared/references/evidence-evolution-and-dependencies.md",
            ROOT / "source/shared/references/scientific-technical-writing.md",
            ROOT / "source/shared/references/protocol-versioning-and-compatibility.md",
            ROOT / "source/shared/references/development-workflow-prompts.md",
            ROOT / "source/SEMANTIC_DEPENDENCIES.md",
            ROOT / "workplans/archive/SSDP-6.4-AXIOMATIC-FORMAL-DEFINITION-AND-SEMANTIC-TRACEABILITY-CONSOLIDATED.md",
        ]
        for path in surfaces:
            with self.subTest(path=str(path.relative_to(ROOT))):
                self.assertTrue(markdown_fences_well_formed(path.read_text(encoding="utf-8")))

        malformed = "before\n```text\nvalue\n``` trailing prose\nafter\n"
        self.assertFalse(markdown_fences_well_formed(malformed))

    def test_qf64_o_candidate_lifecycle_preserves_bootstrap_recovery_separation(self) -> None:
        versioning = norm(self.versioning)
        self.assertIn("protocol 6.4 is accepted-current", versioning)
        self.assertIn("6.4.0 public-source bootstrap -> e09a9d1480211eea2d16d722182bb5c6de1bee12", versioning)
        self.assertIn("independent assembled-candidate review", versioning)
        self.assertIn("CURRENT_PROTOCOL = 6.4.0", self.prompts)
        self.assertIn("CURRENT_PUBLIC_REF = e09a9d1480211eea2d16d722182bb5c6de1bee12", self.prompts)
        self.assertIn("6.4.0  -> 74bc572ef516cae417437a2027eeff52a2e25c15", self.versioning)
        rev4 = read("workplans/active/SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-4-PROTOCOL-6.3-INHERITANCE-RECONCILIATION.md")
        self.assertIn("d3_architecture_mutation: none", rev4)
        self.assertIn("PROTOCOL 7 D4 IMPLEMENTATION: NOT AUTHORIZED", rev4)

    def test_qf64_p_closeout_archives_snapshot(self) -> None:
        self.assertEqual(sorted((ROOT / "workplans/active").glob("SSDP-6.4*.md")), [])
        archived=ROOT/"workplans/archive/SSDP-6.4-AXIOMATIC-FORMAL-DEFINITION-AND-SEMANTIC-TRACEABILITY-CONSOLIDATED.md"
        self.assertTrue(archived.is_file())
        self.assertIn("STAGE F: PASS", archived.read_text())

    def test_automation_boundary_does_not_counterfeit_semantic_review(self) -> None:
        kernel, writing, evidence = map(norm, (self.kernel, self.writing, self.evidence))
        self.assertIn("derived review and impact aids, not authority", kernel)
        self.assertIn("semantic/editorial checks, not a mandate for new registries or checker frameworks", writing)
        self.assertIn("not a required universal machine graph/database", evidence)


if __name__ == "__main__":
    unittest.main()
