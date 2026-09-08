"""O3 -- real Git worktree/remote observation against real temporary repositories.

The production observer is the acceptance owner here. In particular, the
non-mutation claim is proved by snapshotting every mutable Git surface (worktree
content, index, HEAD, local refs, remote-tracking refs, reflogs) before and after
observation and requiring byte equality.
"""

from __future__ import annotations

import hashlib
import os
import shlex
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from sdp_orchestrator.core import errors as E
from sdp_orchestrator.core.git import (
    _BoundedRunError,
    _git_env,
    identify_worktree,
    list_remotes,
    observe,
    run_bounded,
    select_remote,
    working_tree_identity,
)
from sdp_orchestrator.core.records import RemoteEvidence, RemoteMode

from ._support import commit_all, git, init_repo


def _tree_snapshot(root: Path) -> dict[str, str]:
    """Hash every file under ``root`` including the Git directory."""

    digests: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            digests[str(path.relative_to(root))] = "link:" + os.readlink(path)
            continue
        if not path.is_file():
            continue
        try:
            digests[str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()
        except OSError:  # pragma: no cover - transient files
            digests[str(path.relative_to(root))] = "unreadable"
    return digests


class ObservationBase(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)
        self.repo = init_repo(self.root / "repo")


class WorktreeIdentityTests(ObservationBase):
    def test_alias_paths_map_to_one_worktree_key(self) -> None:
        alias = self.root / "alias"
        alias.symlink_to(self.repo)
        self.assertEqual(
            identify_worktree(self.repo).worktree_key,
            identify_worktree(alias).worktree_key,
        )

    def test_subdirectory_resolves_to_the_worktree_root(self) -> None:
        nested = self.repo / "a" / "b"
        nested.mkdir(parents=True)
        self.assertEqual(
            identify_worktree(nested).toplevel, identify_worktree(self.repo).toplevel
        )

    def test_linked_worktree_is_a_distinct_key_sharing_the_repository(self) -> None:
        linked = self.root / "linked"
        git(self.repo, "worktree", "add", "--quiet", "-b", "side", str(linked))
        primary = identify_worktree(self.repo)
        secondary = identify_worktree(linked)
        self.assertNotEqual(primary.worktree_key, secondary.worktree_key)
        self.assertEqual(primary.repository_id, secondary.repository_id)

    def test_non_repository_path_is_rejected(self) -> None:
        plain = self.root / "plain"
        plain.mkdir()
        with self.assertRaises(E.OrchestratorError) as caught:
            identify_worktree(plain)
        self.assertEqual(caught.exception.code, E.REPOSITORY_INVALID)

    def test_key_does_not_expose_the_local_path(self) -> None:
        identity = identify_worktree(self.repo)
        self.assertNotIn(str(self.repo), str(identity.worktree_key))
        self.assertNotIn(str(self.repo), identity.repository_id)

    def test_ambient_git_semantic_overrides_do_not_redirect_observation(self) -> None:
        other = init_repo(self.root / "other")
        with patch.dict(
            os.environ,
            {
                "GIT_DIR": str(other / ".git"),
                "GIT_WORK_TREE": str(other),
                "GIT_INDEX_FILE": str(other / ".git" / "index"),
                "GIT_OBJECT_DIRECTORY": str(other / ".git" / "objects"),
            },
            clear=False,
        ):
            identity = identify_worktree(self.repo)
        self.assertEqual(identity.toplevel, self.repo.resolve())
        self.assertNotIn("GIT_DIR", _git_env())

    def test_git_executable_overrides_are_not_inherited(self) -> None:
        self.assertNotIn("GIT_SSH", _git_env())
        self.assertNotIn("GIT_SSH_COMMAND", _git_env())
        self.assertNotIn("GIT_SSH_VARIANT", _git_env())

    def test_git_executable_override_is_not_executed_by_remote_query(self) -> None:
        """Exercise the real refresh path while an ambient helper is armed."""

        marker = self.root / "ambient-ssh-helper-ran"
        helper = self.root / "ambient-ssh-helper"
        helper.write_text(
            "#!/bin/sh\n"
            f"printf invoked > {shlex.quote(str(marker))}\n"
            "exit 0\n",
            encoding="utf-8",
        )
        helper.chmod(0o700)
        git(self.repo, "remote", "add", "origin", "ssh://127.0.0.1:1/unused.git")

        with patch.dict(os.environ, {"GIT_SSH_COMMAND": str(helper)}, clear=False):
            observed = observe(
                identify_worktree(self.repo),
                remote_mode=RemoteMode.REFRESH_REMOTE,
                configured_remote_name=None,
            )

        self.assertFalse(marker.exists(), "the ambient Git SSH helper must not run")
        self.assertTrue(
            any("bounded remote query" in note for note in observed.diagnostics),
            observed.diagnostics,
        )

    def test_subprocess_stdout_and_stderr_are_bounded_during_collection(self) -> None:
        command = [sys.executable, "-c", "import sys; sys.stdout.write('x' * 100000)"]
        with self.assertRaises(_BoundedRunError) as caught:
            run_bounded(command, timeout=5, max_output_bytes=1024, env={"PATH": os.environ["PATH"]})
        self.assertEqual(caught.exception.reason, "output")

        command = [sys.executable, "-c", "import sys; sys.stderr.write('x' * 100000)"]
        with self.assertRaises(_BoundedRunError) as caught:
            run_bounded(command, timeout=5, max_output_bytes=1024, env={"PATH": os.environ["PATH"]})
        self.assertEqual(caught.exception.reason, "output")


class WorkingTreeIdentityTests(ObservationBase):
    def test_clean_tree_has_no_digest(self) -> None:
        digest, complete = working_tree_identity(self.repo)
        self.assertIsNone(digest)
        self.assertTrue(complete)

    def test_dirty_content_changes_the_digest_at_the_same_path(self) -> None:
        target = self.repo / "file.txt"
        target.write_text("one\n", encoding="utf-8")
        first, _ = working_tree_identity(self.repo)
        target.write_text("two\n", encoding="utf-8")
        second, _ = working_tree_identity(self.repo)
        self.assertIsNotNone(first)
        self.assertNotEqual(first, second)

    def test_identical_dirty_content_is_stable(self) -> None:
        (self.repo / "file.txt").write_text("same\n", encoding="utf-8")
        first, _ = working_tree_identity(self.repo)
        second, _ = working_tree_identity(self.repo)
        self.assertEqual(first, second)

    def test_staged_and_untracked_content_both_participate(self) -> None:
        (self.repo / "untracked.txt").write_text("u\n", encoding="utf-8")
        untracked_only, _ = working_tree_identity(self.repo)
        git(self.repo, "add", "untracked.txt")
        staged, _ = working_tree_identity(self.repo)
        self.assertNotEqual(untracked_only, staged)

    def test_staged_blob_changes_participate_when_worktree_bytes_do_not(self) -> None:
        target = self.repo / "staged.txt"
        target.write_text("base\n", encoding="utf-8")
        git(self.repo, "add", "staged.txt")
        git(self.repo, "commit", "--quiet", "-m", "staged base")

        target.write_text("worktree\n", encoding="utf-8")
        git(self.repo, "add", "staged.txt")
        first, complete = working_tree_identity(self.repo)

        alternate = self.root / "alternate.txt"
        alternate.write_text("index-only\n", encoding="utf-8")
        blob = git(self.repo, "hash-object", "-w", str(alternate))
        alternate.unlink()
        git(self.repo, "update-index", "--cacheinfo", f"100644,{blob},staged.txt")
        second, second_complete = working_tree_identity(self.repo)

        self.assertTrue(complete)
        self.assertTrue(second_complete)
        self.assertNotEqual(first, second)
        self.assertEqual(target.read_text(encoding="utf-8"), "worktree\n")

    def test_mode_only_staged_changes_participate(self) -> None:
        git(self.repo, "config", "core.filemode", "true")
        target = self.repo / "mode.txt"
        target.write_text("same\n", encoding="utf-8")
        git(self.repo, "add", "mode.txt")
        git(self.repo, "commit", "--quiet", "-m", "mode")

        target.chmod(0o755)
        git(self.repo, "add", "mode.txt")
        first, first_complete = working_tree_identity(self.repo)
        target.chmod(0o644)
        git(self.repo, "add", "mode.txt")
        second, second_complete = working_tree_identity(self.repo)

        self.assertTrue(first_complete and second_complete)
        self.assertNotEqual(first, second)

    def test_non_utf8_dirty_path_is_structured_without_encoding_failure(self) -> None:
        raw_name = b"non-utf8-\xff.txt"
        raw_path = os.path.join(os.fsencode(self.repo), raw_name)
        fd = os.open(raw_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
        try:
            os.write(fd, b"payload\n")
        finally:
            os.close(fd)
        self.addCleanup(lambda: os.unlink(raw_path) if os.path.exists(raw_path) else None)

        digest, complete = working_tree_identity(self.repo)

        self.assertIsNotNone(digest)
        self.assertTrue(complete)

    def test_aggregate_dirty_content_budget_marks_identity_incomplete(self) -> None:
        (self.repo / "large-enough.txt").write_text("0123456789", encoding="utf-8")
        with patch("sdp_orchestrator.core.git.MAX_DIRTY_CONTENT_BYTES", 1):
            digest, complete = working_tree_identity(self.repo)
        self.assertIsNotNone(digest)
        self.assertFalse(complete)

    def test_embedded_repository_directory_marks_identity_incomplete(self) -> None:
        """Git reports an embedded repository as one directory entry.

        There is no safe bounded content identity for it, so the candidate is
        marked incomplete rather than fingerprinted optimistically.
        """

        init_repo(self.repo / "embedded")
        digest, complete = working_tree_identity(self.repo)
        self.assertIsNotNone(digest)
        self.assertFalse(complete)

    @unittest.skipIf(os.geteuid() == 0, "root can read mode-000 files")
    def test_unreadable_file_marks_identity_incomplete(self) -> None:
        target = self.repo / "locked.txt"
        target.write_text("secret\n", encoding="utf-8")
        target.chmod(0o000)
        self.addCleanup(target.chmod, 0o644)
        digest, complete = working_tree_identity(self.repo)
        self.assertIsNotNone(digest)
        self.assertFalse(complete)

    def test_scheme_is_versioned(self) -> None:
        (self.repo / "file.txt").write_text("x\n", encoding="utf-8")
        digest, _ = working_tree_identity(self.repo)
        self.assertEqual(digest.canonicalization_scheme, "sdp.git-working-tree.v1")


class RemoteSelectionTests(ObservationBase):
    def _add(self, name: str, url: str) -> None:
        git(self.repo, "remote", "add", name, url)

    def test_configured_remote_name_wins(self) -> None:
        self._add("origin", "https://example.invalid/a.git")
        self._add("fork", "https://example.invalid/b.git")
        selected = select_remote(self.repo, configured_name="fork", branch="main")
        self.assertEqual(selected.remote_name, "fork")

    def test_unknown_configured_remote_fails(self) -> None:
        self._add("origin", "https://example.invalid/a.git")
        with self.assertRaises(E.OrchestratorError) as caught:
            select_remote(self.repo, configured_name="absent", branch="main")
        self.assertEqual(caught.exception.code, E.REMOTE_UNAVAILABLE)

    def test_branch_upstream_remote_precedes_origin(self) -> None:
        self._add("origin", "https://example.invalid/a.git")
        self._add("upstream", "https://example.invalid/b.git")
        git(self.repo, "config", "branch.main.remote", "upstream")
        self.assertEqual(
            select_remote(self.repo, configured_name=None, branch="main").remote_name, "upstream"
        )

    def test_origin_precedes_other_remotes(self) -> None:
        self._add("origin", "https://example.invalid/a.git")
        self._add("zeta", "https://example.invalid/b.git")
        self.assertEqual(
            select_remote(self.repo, configured_name=None, branch="main").remote_name, "origin"
        )

    def test_sole_remote_is_selected(self) -> None:
        self._add("only", "https://example.invalid/a.git")
        self.assertEqual(
            select_remote(self.repo, configured_name=None, branch="main").remote_name, "only"
        )

    def test_multiple_remotes_without_evidence_are_ambiguous(self) -> None:
        self._add("alpha", "https://example.invalid/a.git")
        self._add("beta", "https://example.invalid/b.git")
        with self.assertRaises(E.OrchestratorError) as caught:
            select_remote(self.repo, configured_name=None, branch="main")
        self.assertEqual(caught.exception.code, E.REMOTE_AMBIGUOUS)

    def test_no_remote_is_reported_as_unavailable(self) -> None:
        with self.assertRaises(E.OrchestratorError) as caught:
            select_remote(self.repo, configured_name=None, branch="main")
        self.assertEqual(caught.exception.code, E.REMOTE_UNAVAILABLE)

    def test_credential_userinfo_is_stripped(self) -> None:
        self._add("origin", "https://alice:s3cret@example.invalid/a.git")
        selected = select_remote(self.repo, configured_name=None, branch="main")
        self.assertNotIn("s3cret", selected.sanitized_repository)
        self.assertIn("<redacted>", selected.sanitized_repository)
        self.assertTrue(selected.web_addressable)

    def test_scp_style_ssh_remote_is_web_addressable(self) -> None:
        self._add("origin", "git@example.invalid:owner/repo.git")
        selected = select_remote(self.repo, configured_name=None, branch="main")
        self.assertEqual(selected.scheme, "ssh")
        self.assertTrue(selected.web_addressable)

    def test_file_url_remote_is_local_only(self) -> None:
        self._add("origin", f"file://{self.repo}")
        selected = select_remote(self.repo, configured_name=None, branch="main")
        self.assertEqual(selected.scheme, "file")
        self.assertFalse(selected.web_addressable)

    def test_filesystem_path_remote_is_local_only(self) -> None:
        self._add("origin", str(self.root / "other"))
        selected = select_remote(self.repo, configured_name=None, branch="main")
        self.assertEqual(selected.scheme, "path")
        self.assertFalse(selected.web_addressable)

    def test_remote_listing_is_complete(self) -> None:
        self._add("a", "https://example.invalid/a.git")
        self._add("b", "https://example.invalid/b.git")
        self.assertEqual(sorted(list_remotes(self.repo)), ["a", "b"])


class CandidateObservationTests(ObservationBase):
    def _observe(self, mode: RemoteMode = RemoteMode.LOCAL_ONLY, remote_name=None):
        return observe(
            identify_worktree(self.repo), remote_mode=mode, configured_remote_name=remote_name
        )

    def test_branch_and_head_are_reported(self) -> None:
        candidate = self._observe().candidate
        self.assertEqual(candidate.branch, "main")
        self.assertFalse(candidate.detached)
        self.assertEqual(candidate.head_commit, git(self.repo, "rev-parse", "HEAD"))

    def test_detached_head_is_reported(self) -> None:
        head = git(self.repo, "rev-parse", "HEAD")
        git(self.repo, "checkout", "--quiet", "--detach", head)
        candidate = self._observe().candidate
        self.assertTrue(candidate.detached)
        self.assertIsNone(candidate.branch)

    def test_local_only_gathers_no_remote_evidence(self) -> None:
        result = self._observe(RemoteMode.LOCAL_ONLY)
        self.assertIsNone(result.remote)
        self.assertIs(result.candidate.remote_evidence, RemoteEvidence.NONE)
        self.assertIsNone(result.candidate.upstream_ref)

    def test_cached_remote_reads_existing_tracking_refs(self) -> None:
        origin = init_repo(self.root / "origin")
        git(self.repo, "remote", "add", "origin", str(origin))
        git(self.repo, "push", "--quiet", "-u", "origin", "main")
        result = self._observe(RemoteMode.USE_CACHED_REMOTE)
        self.assertEqual(result.candidate.upstream_ref, "origin/main")
        self.assertIs(result.candidate.remote_evidence, RemoteEvidence.CACHED)
        self.assertEqual(
            result.candidate.observed_remote_commit, git(self.repo, "rev-parse", "HEAD")
        )

    def test_refresh_remote_queries_without_mutating_tracking_refs(self) -> None:
        origin = init_repo(self.root / "origin")
        git(self.repo, "remote", "add", "origin", str(origin))
        git(self.repo, "push", "--quiet", "-u", "origin", "main")
        # Advance the remote behind our back; the tracking ref stays stale.
        (origin / "extra.txt").write_text("x\n", encoding="utf-8")
        remote_head = commit_all(origin, "advance")
        cached = git(self.repo, "rev-parse", "origin/main")

        result = self._observe(RemoteMode.REFRESH_REMOTE)
        self.assertIs(result.candidate.remote_evidence, RemoteEvidence.REFRESHED)
        self.assertEqual(result.candidate.observed_remote_commit, remote_head)
        self.assertEqual(
            git(self.repo, "rev-parse", "origin/main"),
            cached,
            "refresh_remote must not update remote-tracking refs",
        )

    def test_missing_upstream_is_diagnosed_not_invented(self) -> None:
        git(self.repo, "remote", "add", "origin", "https://example.invalid/a.git")
        result = self._observe(RemoteMode.USE_CACHED_REMOTE)
        self.assertIsNone(result.candidate.observed_remote_commit)
        self.assertIs(result.candidate.remote_evidence, RemoteEvidence.NONE)

    def test_ambiguous_remote_is_a_diagnostic_not_a_hard_failure(self) -> None:
        git(self.repo, "remote", "add", "alpha", "https://example.invalid/a.git")
        git(self.repo, "remote", "add", "beta", "https://example.invalid/b.git")
        result = self._observe(RemoteMode.USE_CACHED_REMOTE)
        self.assertIsNone(result.remote)
        self.assertTrue(any("remote.ambiguous" in note for note in result.diagnostics))

    def test_dirty_content_marks_the_candidate(self) -> None:
        (self.repo / "dirty.txt").write_text("d\n", encoding="utf-8")
        self.assertIsNotNone(self._observe().candidate.working_tree_digest)


class NonMutationTests(ObservationBase):
    """The central invariant: observation changes nothing in the target."""

    def _assert_unchanged(self, mode: RemoteMode) -> None:
        before = _tree_snapshot(self.repo)
        observe(
            identify_worktree(self.repo), remote_mode=mode, configured_remote_name=None
        )
        self.assertEqual(before, _tree_snapshot(self.repo))

    def test_local_only_observation_mutates_nothing(self) -> None:
        (self.repo / "dirty.txt").write_text("d\n", encoding="utf-8")
        self._assert_unchanged(RemoteMode.LOCAL_ONLY)

    def test_cached_remote_observation_mutates_nothing(self) -> None:
        origin = init_repo(self.root / "origin")
        git(self.repo, "remote", "add", "origin", str(origin))
        git(self.repo, "push", "--quiet", "-u", "origin", "main")
        self._assert_unchanged(RemoteMode.USE_CACHED_REMOTE)

    def test_refresh_remote_observation_mutates_nothing(self) -> None:
        origin = init_repo(self.root / "origin")
        git(self.repo, "remote", "add", "origin", str(origin))
        git(self.repo, "push", "--quiet", "-u", "origin", "main")
        (origin / "extra.txt").write_text("x\n", encoding="utf-8")
        commit_all(origin, "advance")
        self._assert_unchanged(RemoteMode.REFRESH_REMOTE)

    def test_head_and_branch_survive_observation(self) -> None:
        head_before = git(self.repo, "rev-parse", "HEAD")
        branch_before = git(self.repo, "rev-parse", "--abbrev-ref", "HEAD")
        observe(
            identify_worktree(self.repo),
            remote_mode=RemoteMode.LOCAL_ONLY,
            configured_remote_name=None,
        )
        self.assertEqual(head_before, git(self.repo, "rev-parse", "HEAD"))
        self.assertEqual(branch_before, git(self.repo, "rev-parse", "--abbrev-ref", "HEAD"))


if __name__ == "__main__":
    unittest.main()
