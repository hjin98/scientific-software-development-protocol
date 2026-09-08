"""O9 -- web/local privacy and remote truthfulness at the RenderedPrompt boundary.

Every assertion here inspects the *final artifact*, not an intermediate record,
because that artifact is what a user pastes into a web agent.
"""

from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

from sdp_orchestrator.core import errors as E
from sdp_orchestrator.core.application import create_application
from sdp_orchestrator.core.records import (
    ApplicationRequest,
    ObservationPolicy,
    ProjectKey,
    PromptExecutionMode,
    PromptPreparationRequest,
    PromptRenderRequest,
    ProjectObservation,
    RemoteRepositoryRef,
    RemoteEvidence,
    RemoteMode,
    StageSelector,
)

from ._support import commit_all, config_text, git, init_bare, init_repo, write_workplan

DISTINCTIVE = "zq7-private-marker-path"
SECRET = "tok3n-should-never-appear"


class PrivacyBase(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name) / DISTINCTIVE
        self.root.mkdir(parents=True)
        self.addCleanup(self._tmp.cleanup)
        self.repo = init_repo(self.root / "repo")
        write_workplan(self.repo, "workplans/active/WP.md", workplan_id="WP", target_branch="main")
        commit_all(self.repo, "add workplan")
        self.config = self.root / "config.toml"
        self._write_config()

    def _write_config(self, **kwargs: object) -> None:
        self.config.write_text(config_text(self.repo, **kwargs), encoding="utf-8")  # type: ignore[arg-type]

    def _origin(self, url: str | None = None, *, push: bool = True) -> Path:
        origin = init_bare(self.root / "origin")
        git(self.repo, "remote", "add", "origin", url or str(origin))
        if push:
            git(self.repo, "push", "--quiet", "-u", "origin", "main")
        return origin

    def render(
        self,
        mode=PromptExecutionMode.WEB,
        *,
        remote=RemoteMode.USE_CACHED_REMOTE,
        max_remote_staleness_seconds: int | None = None,
        stage="implementation",
        **kwargs,
    ):
        application = create_application(ApplicationRequest(config_path=str(self.config)))
        prepared = application.core().prepare(
            PromptPreparationRequest(
                project=ProjectKey("demo"),
                stage=StageSelector(stage),
                policy=ObservationPolicy(
                    remote_mode=remote,
                    max_remote_staleness_seconds=max_remote_staleness_seconds,
                ),
                **kwargs,
            )
        )
        return application.core().render(
            PromptRenderRequest(prepared=prepared, prompt_execution_mode=mode)
        )


class WebAddressabilityTests(PrivacyBase):
    def test_web_render_requires_known_target_existence(self) -> None:
        self._origin("https://example.invalid/owner/repo.git", push=False)
        with self.assertRaises(E.OrchestratorError) as caught:
            self.render()
        self.assertEqual(caught.exception.code, E.REMOTE_TARGET_UNAVAILABLE)

    def test_local_only_observation_cannot_establish_a_web_target(self) -> None:
        self._origin("https://example.invalid/owner/repo.git", push=False)
        with self.assertRaises(E.OrchestratorError) as caught:
            self.render(remote=RemoteMode.LOCAL_ONLY)
        self.assertEqual(caught.exception.code, E.REMOTE_TARGET_UNAVAILABLE)

    def test_cached_tracking_evidence_admits_a_web_render(self) -> None:
        self._origin()
        # A filesystem origin is not web-addressable; retarget to an https URL
        # while keeping the tracking ref that proves the branch exists.
        git(self.repo, "remote", "set-url", "origin", "https://example.invalid/owner/repo.git")
        rendered = self.render()
        self.assertIs(rendered.snapshot.remote_evidence, RemoteEvidence.CACHED)
        self.assertIn("https://example.invalid/owner/repo.git", rendered.prompt_text)
        self.assertIn("freshness not re-queried", rendered.prompt_text)

    def test_selected_fork_does_not_inherit_origin_upstream_evidence(self) -> None:
        fork = init_bare(self.root / "fork")
        self._origin()
        git(self.repo, "remote", "set-url", "origin", "https://example.invalid/origin.git")
        git(self.repo, "remote", "add", "fork", str(fork))
        git(self.repo, "remote", "set-url", "fork", "https://example.invalid/fork.git")
        self._write_config(remote_name="fork")

        application = create_application(ApplicationRequest(config_path=str(self.config)))
        prepared = application.core().prepare(
            PromptPreparationRequest(
                project=ProjectKey("demo"),
                stage=StageSelector("implementation"),
                policy=ObservationPolicy(remote_mode=RemoteMode.USE_CACHED_REMOTE),
            )
        )
        self.assertEqual(prepared.observation.selected_remote.remote_name, "fork")
        self.assertEqual(prepared.observation.candidate.upstream_ref, "origin/main")
        self.assertIsNone(prepared.observation.candidate.observed_remote_commit)
        with self.assertRaises(E.OrchestratorError) as caught:
            application.core().render(
                PromptRenderRequest(
                    prepared=prepared, prompt_execution_mode=PromptExecutionMode.WEB
                )
            )
        self.assertEqual(caught.exception.code, E.REMOTE_TARGET_UNAVAILABLE)

    def test_selected_fork_uses_its_cached_same_branch_target(self) -> None:
        fork = init_bare(self.root / "fork")
        self._origin()
        git(self.repo, "remote", "set-url", "origin", "https://example.invalid/origin.git")
        git(self.repo, "remote", "add", "fork", str(fork))
        git(self.repo, "push", "--quiet", "fork", "main")
        git(self.repo, "remote", "set-url", "fork", "https://example.invalid/fork.git")
        self._write_config(remote_name="fork")

        rendered = self.render()

        self.assertIn("https://example.invalid/fork.git (branch main", rendered.prompt_text)
        self.assertNotIn("https://example.invalid/origin.git", rendered.prompt_text)

    def test_explicit_freshness_rejects_age_unknown_cached_evidence(self) -> None:
        self._origin()
        git(self.repo, "remote", "set-url", "origin", "https://example.invalid/owner/repo.git")
        with self.assertRaises(E.OrchestratorError) as caught:
            self.render(max_remote_staleness_seconds=60)
        self.assertEqual(caught.exception.code, E.REMOTE_STALE)

    def test_refreshed_evidence_carries_a_real_age_for_the_freshness_bound(self) -> None:
        from sdp_orchestrator.core.git import identify_worktree, observe
        from sdp_orchestrator.core.render import build_snapshot

        self._origin()
        result = observe(
            identify_worktree(self.repo),
            remote_mode=RemoteMode.REFRESH_REMOTE,
            configured_remote_name=None,
        )
        self.assertIs(result.candidate.remote_evidence, RemoteEvidence.REFRESHED)
        self.assertIsNotNone(result.candidate.remote_observed_at)
        observation = ProjectObservation(
            project_key=ProjectKey("demo"),
            worktree_key=identify_worktree(self.repo).worktree_key,
            candidate=result.candidate,
            selected_remote=RemoteRepositoryRef(
                remote_name="origin",
                sanitized_repository="https://example.invalid/owner/repo.git",
                scheme="https",
                web_addressable=True,
            ),
            policy=ObservationPolicy(
                remote_mode=RemoteMode.REFRESH_REMOTE,
                max_remote_staleness_seconds=60,
            ),
            local_repo_root=str(self.repo),
        )
        snapshot = build_snapshot(observation, PromptExecutionMode.WEB)
        self.assertIs(snapshot.remote_evidence, RemoteEvidence.REFRESHED)

    def test_refreshed_evidence_is_labelled_distinctly(self) -> None:
        self._origin()
        rendered = self.render(mode=PromptExecutionMode.LOCAL, remote=RemoteMode.REFRESH_REMOTE)
        self.assertIs(rendered.snapshot.remote_evidence, RemoteEvidence.REFRESHED)

    def test_dirty_worktree_blocks_web_mode(self) -> None:
        self._origin()
        git(self.repo, "remote", "set-url", "origin", "https://example.invalid/owner/repo.git")
        (self.repo / "dirty.txt").write_text("d\n", encoding="utf-8")
        with self.assertRaises(E.OrchestratorError) as caught:
            self.render()
        self.assertEqual(caught.exception.code, E.PROMPT_MODE_INVALID)

    def test_local_ahead_of_remote_blocks_web_mode(self) -> None:
        self._origin()
        git(self.repo, "remote", "set-url", "origin", "https://example.invalid/owner/repo.git")
        (self.repo / "extra.txt").write_text("x\n", encoding="utf-8")
        commit_all(self.repo, "local ahead")
        with self.assertRaises(E.OrchestratorError) as caught:
            self.render()
        self.assertEqual(caught.exception.code, E.REMOTE_STALE)

    def test_remote_ahead_of_local_blocks_web_mode(self) -> None:
        self._origin()
        # Publish one more commit, then move the local branch back: the remote is
        # now genuinely ahead of the candidate.
        (self.repo / "remote.txt").write_text("r\n", encoding="utf-8")
        commit_all(self.repo, "published")
        git(self.repo, "push", "--quiet", "origin", "main")
        git(self.repo, "reset", "--quiet", "--hard", "HEAD~1")
        git(self.repo, "remote", "set-url", "origin", "https://example.invalid/owner/repo.git")
        with self.assertRaises(E.OrchestratorError) as caught:
            self.render(remote=RemoteMode.USE_CACHED_REMOTE)
        self.assertEqual(caught.exception.code, E.REMOTE_STALE)

    def test_absent_remote_branch_blocks_web_mode(self) -> None:
        """A branch that does not exist on the remote is never rendered as a web target.

        Offline, a remote cannot be both reachable and web-addressable, so this is
        proved in two parts. The real production observer establishes the fact
        (the refreshed query finds no branch); the render policy is then applied
        to that real observation with only the remote's URL classification
        substituted -- a classification with its own real-remote coverage in
        ``test_git_observation``.
        """

        from sdp_orchestrator.core.git import identify_worktree, observe
        from sdp_orchestrator.core.records import (
            ProjectObservation,
            RemoteRepositoryRef,
        )
        from sdp_orchestrator.core.render import build_snapshot

        origin = self._origin()
        git(origin, "branch", "-m", "main", "renamed")

        result = observe(
            identify_worktree(self.repo),
            remote_mode=RemoteMode.REFRESH_REMOTE,
            configured_remote_name=None,
        )
        self.assertIs(result.candidate.remote_evidence, RemoteEvidence.REFRESHED)
        self.assertIsNone(
            result.candidate.observed_remote_commit,
            "a refreshed query must report the branch as absent, not assume it exists",
        )

        observation = ProjectObservation(
            project_key=ProjectKey("demo"),
            worktree_key=identify_worktree(self.repo).worktree_key,
            candidate=result.candidate,
            selected_remote=RemoteRepositoryRef(
                remote_name="origin",
                sanitized_repository="https://example.invalid/owner/repo.git",
                scheme="https",
                web_addressable=True,
            ),
            policy=ObservationPolicy(remote_mode=RemoteMode.REFRESH_REMOTE),
            local_repo_root=str(self.repo),
        )
        with self.assertRaises(E.OrchestratorError) as caught:
            build_snapshot(observation, PromptExecutionMode.WEB)
        self.assertEqual(caught.exception.code, E.REMOTE_TARGET_UNAVAILABLE)

    def test_detached_head_blocks_web_mode(self) -> None:
        self._origin()
        git(self.repo, "remote", "set-url", "origin", "https://example.invalid/owner/repo.git")
        git(self.repo, "checkout", "--quiet", "--detach", "HEAD")
        with self.assertRaises(E.OrchestratorError) as caught:
            self.render()
        self.assertEqual(caught.exception.code, E.REMOTE_TARGET_UNAVAILABLE)

    def test_file_remote_is_rejected_for_web_mode(self) -> None:
        self._origin(push=False)
        git(self.repo, "remote", "set-url", "origin", f"file://{self.root / 'origin'}")
        with self.assertRaises(E.OrchestratorError) as caught:
            self.render()
        self.assertEqual(caught.exception.code, E.REMOTE_LOCAL_ONLY)

    def test_filesystem_path_remote_is_rejected_for_web_mode(self) -> None:
        self._origin()
        with self.assertRaises(E.OrchestratorError) as caught:
            self.render()
        self.assertEqual(caught.exception.code, E.REMOTE_LOCAL_ONLY)

    def test_no_remote_at_all_is_reported(self) -> None:
        with self.assertRaises(E.OrchestratorError) as caught:
            self.render()
        self.assertEqual(caught.exception.code, E.REMOTE_UNAVAILABLE)

    def test_ambiguous_remotes_are_reported_not_guessed(self) -> None:
        git(self.repo, "remote", "add", "alpha", "https://example.invalid/a.git")
        git(self.repo, "remote", "add", "beta", "https://example.invalid/b.git")
        with self.assertRaises(E.OrchestratorError) as caught:
            self.render()
        self.assertEqual(caught.exception.code, E.REMOTE_AMBIGUOUS)

    def test_configured_remote_name_disambiguates(self) -> None:
        self._origin()
        git(self.repo, "remote", "set-url", "origin", "https://example.invalid/owner/repo.git")
        git(self.repo, "remote", "add", "fork", "https://example.invalid/fork.git")
        self._write_config(remote_name="origin")
        self.assertIn("owner/repo.git", self.render().prompt_text)


class WebLeakageTests(PrivacyBase):
    def _web_prompt(self) -> str:
        self._origin()
        git(self.repo, "remote", "set-url", "origin", "https://example.invalid/owner/repo.git")
        return self.render().prompt_text

    def test_web_prompt_contains_no_local_paths(self) -> None:
        text = self._web_prompt()
        self.assertNotIn(DISTINCTIVE, text)
        self.assertNotIn(str(self.repo), text)
        self.assertNotIn(str(self.config), text)

    def test_web_prompt_contains_no_credential_material(self) -> None:
        self._origin()
        git(
            self.repo,
            "remote",
            "set-url",
            "origin",
            f"https://alice:{SECRET}@example.invalid/owner/repo.git",
        )
        text = self.render().prompt_text
        self.assertNotIn(SECRET, text)
        self.assertIn("<redacted>", text)

    def test_web_prompt_does_not_include_ambient_environment_values(self) -> None:
        os.environ["SDP_TEST_AMBIENT_SECRET"] = SECRET
        self.addCleanup(os.environ.pop, "SDP_TEST_AMBIENT_SECRET", None)
        self.assertNotIn(SECRET, self._web_prompt())

    def test_web_prompt_protocol_source_stays_agent_facing(self) -> None:
        """A local render source must never become the agent's PROTOCOL_SOURCE."""

        local_root = self.root / "protocol-checkout"
        (local_root / "source/shared/references").mkdir(parents=True)
        (local_root / "source/PROTOCOL_VERSION").write_text("5.16.0\n", encoding="utf-8")
        (local_root / "source/shared/references/development-workflow-prompts.md").write_text(
            (Path(__file__).resolve().parents[2]
             / "source/shared/references/development-workflow-prompts.md").read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        self._write_config(local_root=local_root)
        self._origin()
        git(self.repo, "remote", "set-url", "origin", "https://example.invalid/owner/repo.git")
        rendered = self.render()
        self.assertIn("PROTOCOL_SOURCE = AUTO_LOCAL_FIRST", rendered.prompt_text)
        self.assertNotIn(str(local_root), rendered.prompt_text)
        self.assertEqual(rendered.prompt_text.count("protocol-checkout"), 0)

    def test_ssh_remote_is_rendered_without_alteration_of_its_user(self) -> None:
        self._origin()
        git(self.repo, "remote", "set-url", "origin", "git@example.invalid:owner/repo.git")
        self.assertIn("git@example.invalid:owner/repo.git", self.render().prompt_text)

    def test_web_prompt_reports_the_exact_candidate_commit(self) -> None:
        text = self._web_prompt()
        self.assertIn(git(self.repo, "rev-parse", "HEAD"), text)


class LocalModeTests(PrivacyBase):
    def test_local_prompt_may_reference_the_authorized_worktree(self) -> None:
        text = self.render(mode=PromptExecutionMode.LOCAL, remote=RemoteMode.LOCAL_ONLY).prompt_text
        self.assertIn(str(self.repo), text)

    def test_local_prompt_states_worktree_cleanliness_truthfully(self) -> None:
        clean = self.render(mode=PromptExecutionMode.LOCAL, remote=RemoteMode.LOCAL_ONLY)
        self.assertIn("working tree clean", clean.prompt_text)
        (self.repo / "dirty.txt").write_text("d\n", encoding="utf-8")
        dirty = self.render(mode=PromptExecutionMode.LOCAL, remote=RemoteMode.LOCAL_ONLY)
        self.assertIn("uncommitted changes", dirty.prompt_text)

    def test_local_prompt_excludes_ambient_environment_values(self) -> None:
        os.environ["SDP_TEST_AMBIENT_SECRET"] = SECRET
        self.addCleanup(os.environ.pop, "SDP_TEST_AMBIENT_SECRET", None)
        text = self.render(mode=PromptExecutionMode.LOCAL, remote=RemoteMode.LOCAL_ONLY).prompt_text
        self.assertNotIn(SECRET, text)

    def test_local_prompt_does_not_carry_credential_remotes(self) -> None:
        git(
            self.repo, "remote", "add", "origin",
            f"https://alice:{SECRET}@example.invalid/owner/repo.git",
        )
        text = self.render(mode=PromptExecutionMode.LOCAL, remote=RemoteMode.USE_CACHED_REMOTE).prompt_text
        self.assertNotIn(SECRET, text)

    def test_detached_head_renders_in_local_mode(self) -> None:
        git(self.repo, "checkout", "--quiet", "--detach", "HEAD")
        text = self.render(mode=PromptExecutionMode.LOCAL, remote=RemoteMode.LOCAL_ONLY).prompt_text
        self.assertIn("detached HEAD", text)


class ExplicitUserTextTests(PrivacyBase):
    """Explicit user-authored text is intentional content, not scanned material."""

    def test_user_task_text_is_rendered_verbatim(self) -> None:
        text = self.render(
            mode=PromptExecutionMode.LOCAL,
            remote=RemoteMode.LOCAL_ONLY,
            stage="design",
            first_task="migrate the ingest path in /srv/app",
        ).prompt_text
        self.assertIn("migrate the ingest path in /srv/app", text)

    def test_explicit_protocol_source_override_is_honoured(self) -> None:
        text = self.render(
            mode=PromptExecutionMode.LOCAL,
            remote=RemoteMode.LOCAL_ONLY,
            input_overrides=(("PROTOCOL_SOURCE", "https://example.invalid/protocol"),),
        ).prompt_text
        self.assertIn("PROTOCOL_SOURCE = https://example.invalid/protocol", text)


if __name__ == "__main__":
    unittest.main()
