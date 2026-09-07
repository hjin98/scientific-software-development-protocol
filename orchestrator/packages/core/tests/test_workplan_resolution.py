"""O4 -- workplan catalog, current-authority evidence, and every stage policy."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from sdp_orchestrator.core import _errors as E
from sdp_orchestrator.core import _workplans as W
from sdp_orchestrator.core._limits import MAX_WORKPLAN_BYTES
from sdp_orchestrator.core._records import LifecycleState, StageRef, WorkplanPolicy

from ._support import init_repo, write_workplan

STAGE = StageRef(profile_id="sdp-protocol-5.16", protocol_version="5.16.0", stage_key="implementation")


def _stage(key: str) -> StageRef:
    return StageRef(profile_id="sdp-protocol-5.16", protocol_version="5.16.0", stage_key=key)


class CatalogBase(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)
        self.repo = init_repo(self.root / "repo")

    def catalog(self):
        return W.build_catalog(self.repo)

    def by_path(self, relative: str):
        for entry in self.catalog():
            if entry.relative_path == relative:
                return entry
        self.fail(f"{relative} is not in the catalog")


class CatalogDiscoveryTests(CatalogBase):
    def test_active_and_archive_are_both_cataloged(self) -> None:
        write_workplan(self.repo, "workplans/active/A.md", workplan_id="A")
        write_workplan(self.repo, "workplans/archive/B.md", workplan_id="B", status="completed")
        states = {
            entry.descriptor.ref.workplan_id: entry.descriptor.ref.lifecycle_state
            for entry in self.catalog()
        }
        self.assertEqual(states["A"], LifecycleState.ACTIVE)
        self.assertEqual(states["B"], LifecycleState.ARCHIVE)

    def test_nested_authority_documents_are_cataloged(self) -> None:
        write_workplan(self.repo, "workplans/archive/G/AUTHORITY.md", workplan_id="G")
        self.assertTrue(any(e.relative_path.endswith("G/AUTHORITY.md") for e in self.catalog()))

    def test_files_outside_the_workplan_roots_are_ignored(self) -> None:
        write_workplan(self.repo, "docs/NOT-A-WORKPLAN.md", workplan_id="X")
        self.assertEqual(self.catalog(), ())

    def test_non_workplan_suffixes_are_ignored(self) -> None:
        (self.repo / "workplans/active").mkdir(parents=True)
        (self.repo / "workplans/active/notes.yaml").write_text("a: 1\n", encoding="utf-8")
        self.assertEqual(self.catalog(), ())

    def test_symlink_escaping_the_repository_is_not_followed(self) -> None:
        outside = self.root / "outside.md"
        outside.write_text("---\nworkplan_id: OUT\n---\n", encoding="utf-8")
        (self.repo / "workplans/active").mkdir(parents=True)
        (self.repo / "workplans/active/link.md").symlink_to(outside)
        self.assertEqual(self.catalog(), ())

    def test_symlink_inside_the_repository_is_followed(self) -> None:
        write_workplan(self.repo, "workplans/archive/real.md", workplan_id="R", status="completed")
        (self.repo / "workplans/active").mkdir(parents=True)
        (self.repo / "workplans/active/link.md").symlink_to(self.repo / "workplans/archive/real.md")
        self.assertEqual(len(self.catalog()), 2)

    def test_oversized_document_is_reported_not_parsed(self) -> None:
        path = self.repo / "workplans/active/huge.md"
        path.parent.mkdir(parents=True)
        path.write_text("x" * (MAX_WORKPLAN_BYTES + 1), encoding="utf-8")
        entry = self.by_path("workplans/active/huge.md")
        self.assertFalse(entry.declared_id)
        self.assertTrue(entry.descriptor.diagnostics)

    def test_malformed_frontmatter_yields_incomplete_identity(self) -> None:
        path = self.repo / "workplans/active/bad.md"
        path.parent.mkdir(parents=True)
        path.write_text("---\nworkplan_id: [unclosed\n---\nbody\n", encoding="utf-8")
        entry = self.by_path("workplans/active/bad.md")
        self.assertFalse(entry.descriptor.ref.semantic_identity_complete)

    def test_document_without_frontmatter_is_selectable_by_path_only(self) -> None:
        path = self.repo / "workplans/active/plain.md"
        path.parent.mkdir(parents=True)
        path.write_text("# plain workplan\n", encoding="utf-8")
        entry = self.by_path("workplans/active/plain.md")
        self.assertFalse(entry.declared_id)
        self.assertFalse(entry.descriptor.ref.semantic_identity_complete)


class IdentityTests(CatalogBase):
    def test_lifecycle_only_change_preserves_semantic_identity(self) -> None:
        write_workplan(self.repo, "workplans/active/A.md", workplan_id="A", status="active")
        before = self.by_path("workplans/active/A.md").descriptor.ref
        write_workplan(self.repo, "workplans/active/A.md", workplan_id="A", status="frozen")
        after = self.by_path("workplans/active/A.md").descriptor.ref
        self.assertEqual(before.semantic_digest, after.semantic_digest)
        self.assertNotEqual(before.artifact_digest, after.artifact_digest)

    def test_body_change_changes_semantic_identity(self) -> None:
        write_workplan(self.repo, "workplans/active/A.md", workplan_id="A", body="one\n")
        before = self.by_path("workplans/active/A.md").descriptor.ref
        write_workplan(self.repo, "workplans/active/A.md", workplan_id="A", body="two\n")
        self.assertNotEqual(
            before.semantic_digest, self.by_path("workplans/active/A.md").descriptor.ref.semantic_digest
        )

    def test_unknown_frontmatter_key_participates_conservatively(self) -> None:
        write_workplan(self.repo, "workplans/active/A.md", workplan_id="A")
        before = self.by_path("workplans/active/A.md").descriptor.ref
        write_workplan(
            self.repo, "workplans/active/A.md", workplan_id="A", extra={"frozen_authority": "X"}
        )
        self.assertNotEqual(
            before.semantic_digest, self.by_path("workplans/active/A.md").descriptor.ref.semantic_digest
        )

    def test_exclusion_list_is_finite_and_lifecycle_only(self) -> None:
        self.assertNotIn("protocol_version", W.SEMANTIC_EXCLUDED_KEYS)
        self.assertNotIn("target_branch", W.SEMANTIC_EXCLUDED_KEYS)
        self.assertIn("status", W.SEMANTIC_EXCLUDED_KEYS)

    def test_lifecycle_inconsistency_is_reported(self) -> None:
        write_workplan(self.repo, "workplans/archive/A.md", workplan_id="A", status="active")
        entry = self.by_path("workplans/archive/A.md")
        self.assertFalse(entry.descriptor.ref.lifecycle_consistent)

    def test_scheme_is_versioned(self) -> None:
        write_workplan(self.repo, "workplans/active/A.md", workplan_id="A")
        ref = self.by_path("workplans/active/A.md").descriptor.ref
        self.assertEqual(ref.semantic_digest.canonicalization_scheme, "sdp.workplan-semantic.v1")
        self.assertEqual(ref.artifact_digest.canonicalization_scheme, "sdp.workplan-artifact.v1")


class CurrentAuthorityTests(CatalogBase):
    def test_parent_workplan_pointer_establishes_supersession(self) -> None:
        write_workplan(self.repo, "workplans/archive/A.md", workplan_id="A", status="completed")
        write_workplan(
            self.repo,
            "workplans/archive/A/AUTHORITY.md",
            workplan_id="A",
            status="completed",
            extra={"parent_workplan": "../A.md"},
        )
        current = [e for e in self.catalog() if e.descriptor.is_current_authority]
        self.assertEqual([e.relative_path for e in current], ["workplans/archive/A/AUTHORITY.md"])

    def test_revision_chain_selects_the_unsuperseded_revision(self) -> None:
        write_workplan(
            self.repo, "workplans/archive/A.md", workplan_id="A", status="completed",
            extra={"revision": 2},
        )
        for revision in (3, 4):
            write_workplan(
                self.repo,
                f"workplans/archive/A/AUTHORITY_REVISION_{revision}.md",
                workplan_id="A",
                status="completed",
                extra={"parent_workplan": "../A.md", "revision": revision,
                       "supersedes_revision": revision - 1},
            )
        current = [e.relative_path for e in self.catalog() if e.descriptor.is_current_authority]
        self.assertEqual(current, ["workplans/archive/A/AUTHORITY_REVISION_4.md"])

    def test_duplicate_ids_without_evidence_are_ambiguous(self) -> None:
        write_workplan(self.repo, "workplans/active/one.md", workplan_id="A")
        write_workplan(self.repo, "workplans/active/two.md", workplan_id="A")
        self.assertFalse(any(e.descriptor.is_current_authority for e in self.catalog()))
        with self.assertRaises(E.OrchestratorError) as caught:
            W.resolve(
                self.catalog(), stage=STAGE, policy=WorkplanPolicy.REQUIRED, selector="A", branch=None
            )
        self.assertEqual(caught.exception.code, E.WORKPLAN_AMBIGUOUS)

    def test_ambiguous_group_is_still_selectable_by_exact_path(self) -> None:
        write_workplan(self.repo, "workplans/active/one.md", workplan_id="A")
        write_workplan(self.repo, "workplans/active/two.md", workplan_id="A")
        resolution = W.resolve(
            self.catalog(),
            stage=STAGE,
            policy=WorkplanPolicy.REQUIRED,
            selector="workplans/active/two.md",
            branch=None,
        )
        self.assertEqual(resolution.workplan.path, "workplans/active/two.md")


class StagePolicyTests(CatalogBase):
    def _resolve(self, stage_key: str, policy: WorkplanPolicy, **kwargs):
        return W.resolve(
            self.catalog(),
            stage=_stage(stage_key),
            policy=policy,
            selector=kwargs.get("selector"),
            branch=kwargs.get("branch"),
        )

    def test_implementation_uses_target_branch_binding(self) -> None:
        write_workplan(self.repo, "workplans/active/A.md", workplan_id="A", target_branch="feature/x")
        write_workplan(self.repo, "workplans/active/B.md", workplan_id="B", target_branch="other")
        resolution = self._resolve("implementation", WorkplanPolicy.REQUIRED, branch="feature/x")
        self.assertEqual(resolution.workplan.workplan_id, "A")
        self.assertEqual(resolution.selection_basis, "current_branch_target_branch_binding")

    def test_implementation_falls_back_to_the_sole_active_plan(self) -> None:
        write_workplan(self.repo, "workplans/active/A.md", workplan_id="A")
        resolution = self._resolve("implementation", WorkplanPolicy.REQUIRED, branch="main")
        self.assertEqual(resolution.selection_basis, "sole_active_workplan")

    def test_implementation_is_ambiguous_with_several_active_plans(self) -> None:
        write_workplan(self.repo, "workplans/active/A.md", workplan_id="A")
        write_workplan(self.repo, "workplans/active/B.md", workplan_id="B")
        with self.assertRaises(E.OrchestratorError) as caught:
            self._resolve("implementation", WorkplanPolicy.REQUIRED, branch="main")
        self.assertEqual(caught.exception.code, E.WORKPLAN_AMBIGUOUS)

    def test_duplicate_target_branch_bindings_are_ambiguous(self) -> None:
        write_workplan(self.repo, "workplans/active/A.md", workplan_id="A", target_branch="b")
        write_workplan(self.repo, "workplans/active/B.md", workplan_id="B", target_branch="b")
        with self.assertRaises(E.OrchestratorError) as caught:
            self._resolve("implementation", WorkplanPolicy.REQUIRED, branch="b")
        self.assertEqual(caught.exception.code, E.WORKPLAN_AMBIGUOUS)

    def test_implementation_without_any_active_plan_fails(self) -> None:
        with self.assertRaises(E.OrchestratorError) as caught:
            self._resolve("implementation", WorkplanPolicy.REQUIRED, branch="main")
        self.assertEqual(caught.exception.code, E.WORKPLAN_NOT_FOUND)

    def test_archive_only_plans_are_not_implicitly_active(self) -> None:
        write_workplan(self.repo, "workplans/archive/A.md", workplan_id="A", status="completed")
        with self.assertRaises(E.OrchestratorError) as caught:
            self._resolve("implementation", WorkplanPolicy.REQUIRED, branch="main")
        self.assertEqual(caught.exception.code, E.WORKPLAN_NOT_FOUND)

    def test_new_task_design_does_not_capture_a_sole_active_plan(self) -> None:
        """Counterfactual required by O4: Design must not silently adopt an unrelated plan."""

        write_workplan(self.repo, "workplans/active/UNRELATED.md", workplan_id="UNRELATED")
        resolution = self._resolve("design", WorkplanPolicy.EXPLICIT_ONLY, branch="main")
        self.assertIsNone(resolution.workplan)
        self.assertEqual(resolution.selection_basis, "no_explicit_authority_supplied")

    def test_explicit_only_stages_accept_an_explicit_target(self) -> None:
        write_workplan(self.repo, "workplans/active/A.md", workplan_id="A")
        for stage_key in ("baseline", "design", "verification", "stabilization", "closeout"):
            resolution = self._resolve(stage_key, WorkplanPolicy.EXPLICIT_ONLY, selector="A")
            self.assertEqual(resolution.workplan.workplan_id, "A", stage_key)

    def test_explicit_only_stages_return_no_plan_without_a_selector(self) -> None:
        write_workplan(self.repo, "workplans/active/A.md", workplan_id="A")
        for stage_key in ("baseline", "verification", "stabilization", "closeout"):
            self.assertIsNone(
                self._resolve(stage_key, WorkplanPolicy.EXPLICIT_ONLY, branch="main").workplan,
                stage_key,
            )

    def test_alignment_requires_an_exact_selector(self) -> None:
        write_workplan(self.repo, "workplans/active/A.md", workplan_id="A")
        with self.assertRaises(E.OrchestratorError) as caught:
            self._resolve("alignment", WorkplanPolicy.EXPLICIT_REQUIRED, branch="main")
        self.assertEqual(caught.exception.code, E.WORKPLAN_REQUIRED)

    def test_health_audit_rejects_a_workplan_selector(self) -> None:
        write_workplan(self.repo, "workplans/active/A.md", workplan_id="A")
        with self.assertRaises(E.OrchestratorError) as caught:
            self._resolve("health-audit", WorkplanPolicy.DISALLOWED, selector="A")
        self.assertEqual(caught.exception.code, E.WORKPLAN_DISALLOWED)

    def test_health_audit_selects_nothing_without_a_selector(self) -> None:
        write_workplan(self.repo, "workplans/active/A.md", workplan_id="A")
        resolution = self._resolve("health-audit", WorkplanPolicy.DISALLOWED, branch="main")
        self.assertIsNone(resolution.workplan)

    def test_unknown_selector_fails(self) -> None:
        with self.assertRaises(E.OrchestratorError) as caught:
            self._resolve("implementation", WorkplanPolicy.REQUIRED, selector="ABSENT")
        self.assertEqual(caught.exception.code, E.WORKPLAN_NOT_FOUND)

    def test_path_traversal_selector_does_not_escape(self) -> None:
        write_workplan(self.repo, "workplans/active/A.md", workplan_id="A")
        with self.assertRaises(E.OrchestratorError) as caught:
            self._resolve("implementation", WorkplanPolicy.REQUIRED, selector="../../etc/passwd")
        self.assertEqual(caught.exception.code, E.WORKPLAN_NOT_FOUND)

    def test_selection_is_never_fuzzy(self) -> None:
        write_workplan(self.repo, "workplans/active/A.md", workplan_id="ALPHA-ONE")
        with self.assertRaises(E.OrchestratorError):
            self._resolve("implementation", WorkplanPolicy.REQUIRED, selector="ALPHA")


if __name__ == "__main__":
    unittest.main()
