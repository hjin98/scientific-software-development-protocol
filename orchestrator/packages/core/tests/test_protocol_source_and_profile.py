"""O5 -- canonical extraction, packaged parity, profile conservatism, source coherence."""

from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from sdp_orchestrator.core import _errors as E
from sdp_orchestrator.core import _profile as P
from sdp_orchestrator.core import _protocolsrc as PS
from sdp_orchestrator.core._canonical import CANONICAL_STAGES, parse_document
from sdp_orchestrator.core._config import ProtocolSourceSection

from ._support import CANONICAL_PROMPTS, REPO_ROOT

CANONICAL_TEXT = CANONICAL_PROMPTS.read_text(encoding="utf-8")
PACKAGED_DIR = (
    Path(PS.__file__).parent / "resources" / "protocol" / P.PROFILE_ID
)


class CanonicalExtractionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.document = parse_document(CANONICAL_TEXT)

    def test_every_canonical_stage_is_extracted_from_real_source(self) -> None:
        self.assertEqual(
            sorted(self.document.stages), sorted(key for _, key, _ in CANONICAL_STAGES)
        )

    def test_each_body_is_the_literal_fenced_block_of_its_heading(self) -> None:
        for _, key, title in CANONICAL_STAGES:
            body = self.document.stages[key].body
            self.assertIn("INPUTS", body)
            self.assertNotIn("```", body)
            marker = f"## {self.document.stages[key].heading_number}. {title}"
            self.assertIn(marker, CANONICAL_TEXT)
            self.assertIn(body, CANONICAL_TEXT, f"{key} body must be literal source text")

    def test_bodies_are_pairwise_distinct(self) -> None:
        bodies = [stage.body for stage in self.document.stages.values()]
        self.assertEqual(len(bodies), len(set(bodies)))

    def test_missing_stage_heading_is_incoherent(self) -> None:
        broken = CANONICAL_TEXT.replace("## 4. Verification", "## 4. Verifications")
        with self.assertRaises(E.OrchestratorError) as caught:
            parse_document(broken)
        self.assertEqual(caught.exception.code, E.PROTOCOL_SOURCE_INCOHERENT)

    def test_two_text_blocks_under_one_heading_is_incoherent(self) -> None:
        broken = CANONICAL_TEXT.replace(
            "## 8. Closeout\n", "## 8. Closeout\n\n```text\nextra\n```\n", 1
        )
        with self.assertRaises(E.OrchestratorError) as caught:
            parse_document(broken)
        self.assertEqual(caught.exception.code, E.PROTOCOL_SOURCE_INCOHERENT)

    def test_duplicate_stage_heading_is_incoherent(self) -> None:
        broken = CANONICAL_TEXT + "\n\n## 2. Implementation\n\n```text\nINPUTS\nX = [y]\n\nbody\n```\n"
        with self.assertRaises(E.OrchestratorError) as caught:
            parse_document(broken)
        self.assertEqual(caught.exception.code, E.PROTOCOL_SOURCE_INCOHERENT)

    def test_oversized_source_is_rejected(self) -> None:
        from sdp_orchestrator.core._limits import MAX_PROTOCOL_SOURCE_BYTES

        with self.assertRaises(E.OrchestratorError) as caught:
            parse_document("x" * (MAX_PROTOCOL_SOURCE_BYTES + 1))
        self.assertEqual(caught.exception.code, E.PROTOCOL_UNAVAILABLE)

    def test_unclassified_input_is_rejected_rather_than_rendered_blank(self) -> None:
        broken = CANONICAL_TEXT.replace(
            "VERIFICATION_SCOPE = [", "TOTALLY_NEW_INPUT = [x]\nVERIFICATION_SCOPE = [", 1
        )
        with self.assertRaises(E.OrchestratorError) as caught:
            P.build_profile(parse_document(broken))
        self.assertEqual(caught.exception.code, E.PROTOCOL_SOURCE_INCOHERENT)


class PackagedSnapshotTests(unittest.TestCase):
    """The packaged snapshot is a derivative, proved reproducible from canonical source."""

    def test_packaged_prompts_are_byte_identical_to_canonical_source(self) -> None:
        self.assertEqual(
            (PACKAGED_DIR / "prompts.md").read_text(encoding="utf-8"), CANONICAL_TEXT
        )

    def test_packaged_profile_is_the_reproducible_derivative(self) -> None:
        expected = P.profile_to_json(P.build_profile(parse_document(CANONICAL_TEXT)).descriptor)
        self.assertEqual((PACKAGED_DIR / "profile.json").read_text(encoding="utf-8"), expected)

    def test_generator_check_mode_agrees(self) -> None:
        script = REPO_ROOT / "orchestrator/scripts/generate_protocol_snapshot.py"
        result = subprocess.run(  # noqa: S603
            [__import__("sys").executable, str(script), "--check"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_packaged_profile_contains_no_prompt_prose(self) -> None:
        """Prose has exactly one authority; the profile is control metadata only."""

        payload = json.loads((PACKAGED_DIR / "profile.json").read_text(encoding="utf-8"))
        serialized = json.dumps(payload)
        for _, key, _ in CANONICAL_STAGES:
            body = parse_document(CANONICAL_TEXT).stages[key].body
            for line in body.splitlines():
                if len(line) > 60:
                    self.assertNotIn(line, serialized)

    def test_packaged_snapshot_resolves_without_configuration(self) -> None:
        resolved = PS.resolve_packaged()
        self.assertEqual(resolved.source.kind, "packaged")
        self.assertIsNone(resolved.mutable_identity)
        self.assertEqual(len(resolved.snapshot.bodies), len(CANONICAL_STAGES))

    def test_tampered_packaged_profile_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fake = Path(tmp) / P.PROFILE_ID
            shutil.copytree(PACKAGED_DIR, fake)
            payload = json.loads((fake / "profile.json").read_text(encoding="utf-8"))
            payload["stages"][0]["role_owner"] = "tampered"
            (fake / "profile.json").write_text(json.dumps(payload), encoding="utf-8")

            original = PS._packaged_dir
            PS._packaged_dir = lambda profile_id: fake  # type: ignore[assignment]
            try:
                with self.assertRaises(E.OrchestratorError) as caught:
                    PS.resolve_packaged()
            finally:
                PS._packaged_dir = original  # type: ignore[assignment]
        self.assertEqual(caught.exception.code, E.PROTOCOL_SOURCE_INCOHERENT)


class ProfileConservatismTests(unittest.TestCase):
    def setUp(self) -> None:
        self.descriptor = P.build_profile(parse_document(CANONICAL_TEXT)).descriptor

    def test_optional_routing_stays_ambiguous_rather_than_deterministic(self) -> None:
        """Protocol 5.16 leaves the stage after a passing Review context-dependent."""

        targets = [
            t.to_stage.stage_key
            for t in self.descriptor.transitions
            if t.from_stage.stage_key == "review" and t.trigger_key == "pass"
        ]
        self.assertGreater(len(targets), 1, "a single edge here would invent authority")
        self.assertEqual(sorted(targets), ["closeout", "stabilization", "verification"])

    def test_every_transition_trigger_is_a_recognized_outcome(self) -> None:
        outcomes = {
            stage.stage.stage_key: set(stage.recognized_outcomes)
            for stage in self.descriptor.stages
        }
        for transition in self.descriptor.transitions:
            self.assertIn(
                transition.trigger_key, outcomes[transition.from_stage.stage_key]
            )

    def test_terminal_outcomes_are_marked_terminal(self) -> None:
        terminal = [t for t in self.descriptor.transitions if t.terminal]
        self.assertTrue(terminal)
        self.assertTrue(all(t.to_stage is None for t in terminal))

    def test_workplan_policies_match_the_frozen_stage_table(self) -> None:
        expected = {
            "baseline": "explicit_only",
            "design": "explicit_only",
            "implementation": "required",
            "review": "required",
            "verification": "explicit_only",
            "stabilization": "explicit_only",
            "alignment": "explicit_required",
            "health-audit": "disallowed",
            "closeout": "explicit_only",
        }
        actual = {
            stage.stage.stage_key: stage.workplan_policy.value
            for stage in self.descriptor.stages
        }
        self.assertEqual(actual, expected)

    def test_stage_refs_are_profile_bound(self) -> None:
        for stage in self.descriptor.stages:
            self.assertEqual(stage.stage.profile_id, P.PROFILE_ID)
            self.assertEqual(stage.stage.protocol_version, P.PROFILE_PROTOCOL_VERSION)

    def test_unknown_stage_selector_fails(self) -> None:
        with self.assertRaises(E.OrchestratorError) as caught:
            P.resolve_stage_key(self.descriptor, "deploy")
        self.assertEqual(caught.exception.code, E.STAGE_UNKNOWN)

    def test_alias_resolves_through_the_profile(self) -> None:
        self.assertEqual(
            P.resolve_stage_key(self.descriptor, "health_audit").stage_key, "health-audit"
        )

    def test_profile_json_round_trips(self) -> None:
        self.assertEqual(
            P.profile_from_json(P.profile_to_json(self.descriptor)), self.descriptor
        )


class LocalSourceTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)
        self._materialize("5.16.0", CANONICAL_TEXT)

    def _materialize(self, version: str, prompts: str) -> None:
        (self.root / "source/shared/references").mkdir(parents=True, exist_ok=True)
        (self.root / PS.CANONICAL_VERSION_RELPATH).write_text(version + "\n", encoding="utf-8")
        (self.root / PS.CANONICAL_PROMPTS_RELPATH).write_text(prompts, encoding="utf-8")

    def test_compatible_local_source_takes_precedence(self) -> None:
        resolved = PS.resolve(
            ProtocolSourceSection(local_root=str(self.root)), profile_id=P.PROFILE_ID
        )
        self.assertEqual(resolved.source.kind, "local")
        self.assertIsNotNone(resolved.mutable_identity)

    def test_incompatible_local_version_fails_rather_than_defaulting(self) -> None:
        self._materialize("5.9.0", CANONICAL_TEXT)
        with self.assertRaises(E.OrchestratorError) as caught:
            PS.resolve(ProtocolSourceSection(local_root=str(self.root)), profile_id=P.PROFILE_ID)
        self.assertEqual(caught.exception.code, E.PROTOCOL_INCOMPATIBLE)

    def test_missing_local_file_is_unavailable(self) -> None:
        (self.root / PS.CANONICAL_PROMPTS_RELPATH).unlink()
        with self.assertRaises(E.OrchestratorError) as caught:
            PS.resolve(ProtocolSourceSection(local_root=str(self.root)), profile_id=P.PROFILE_ID)
        self.assertEqual(caught.exception.code, E.PROTOCOL_UNAVAILABLE)

    def test_changed_local_source_changes_identity(self) -> None:
        before = PS.resolve(
            ProtocolSourceSection(local_root=str(self.root)), profile_id=P.PROFILE_ID
        )
        self._materialize("5.16.0", CANONICAL_TEXT + "\n<!-- edited -->\n")
        after = PS.resolve(
            ProtocolSourceSection(local_root=str(self.root)), profile_id=P.PROFILE_ID
        )
        self.assertNotEqual(before.source.identity, after.source.identity)

    def test_unknown_profile_id_is_incompatible(self) -> None:
        with self.assertRaises(E.OrchestratorError) as caught:
            PS.resolve(None, profile_id="sdp-protocol-9.9")
        self.assertEqual(caught.exception.code, E.PROTOCOL_INCOMPATIBLE)

    def test_remote_is_off_by_default(self) -> None:
        with self.assertRaises(E.OrchestratorError) as caught:
            PS.resolve_remote(ProtocolSourceSection(allow_remote=False))
        self.assertEqual(caught.exception.code, E.PROTOCOL_UNAVAILABLE)


class RemoteSourceTests(unittest.TestCase):
    """Remote reads use a real Git transport against a local bare repository."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

        from ._support import commit_all, git, init_repo

        self.upstream = init_repo(self.root / "upstream")
        (self.upstream / "source/shared/references").mkdir(parents=True)
        (self.upstream / PS.CANONICAL_VERSION_RELPATH).write_text("5.16.0\n", encoding="utf-8")
        (self.upstream / PS.CANONICAL_PROMPTS_RELPATH).write_text(CANONICAL_TEXT, encoding="utf-8")
        self.commit = commit_all(self.upstream, "protocol")
        self.git = git

    def _section(self, ref: str = "main") -> ProtocolSourceSection:
        return ProtocolSourceSection(
            allow_remote=True, remote_repository=str(self.upstream), remote_ref=ref
        )

    def test_explicit_ref_resolves_once_to_an_immutable_commit(self) -> None:
        resolved = PS.resolve_remote(self._section())
        self.assertEqual(resolved.source.kind, "remote")
        self.assertEqual(resolved.source.resolved_ref, self.commit)
        self.assertEqual(resolved.source.requested_ref, "main")
        self.assertIsNone(resolved.mutable_identity)

    def test_all_files_come_from_the_pinned_identity(self) -> None:
        resolved = PS.resolve_remote(self._section())
        names = {name for name, _ in resolved.source.content_digests}
        self.assertEqual(names, {"PROTOCOL_VERSION", PS.CANONICAL_PROMPTS_RELPATH})

    def test_absent_ref_is_unavailable(self) -> None:
        with self.assertRaises(E.OrchestratorError) as caught:
            PS.resolve_remote(self._section("no-such-ref"))
        self.assertEqual(caught.exception.code, E.PROTOCOL_UNAVAILABLE)

    def test_incompatible_remote_version_fails(self) -> None:
        from ._support import commit_all

        (self.upstream / PS.CANONICAL_VERSION_RELPATH).write_text("5.9.0\n", encoding="utf-8")
        commit_all(self.upstream, "downgrade")
        with self.assertRaises(E.OrchestratorError) as caught:
            PS.resolve_remote(self._section())
        self.assertEqual(caught.exception.code, E.PROTOCOL_INCOMPATIBLE)

    def test_missing_required_file_is_incoherent(self) -> None:
        from ._support import commit_all

        (self.upstream / PS.CANONICAL_PROMPTS_RELPATH).unlink()
        commit_all(self.upstream, "remove prompts")
        with self.assertRaises(E.OrchestratorError) as caught:
            PS.resolve_remote(self._section())
        self.assertEqual(caught.exception.code, E.PROTOCOL_SOURCE_INCOHERENT)


if __name__ == "__main__":
    unittest.main()
