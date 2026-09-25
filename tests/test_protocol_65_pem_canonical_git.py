from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source"
sys.path.insert(0, str(SOURCE))

import project_engineering_memory as pem  # noqa: E402


class Protocol65PemCanonicalGitTests(unittest.TestCase):
    def _run(self, root: Path, *args: str, input_bytes: bytes | None = None) -> str:
        proc = subprocess.run(
            ["git", "-C", str(root), *args],
            input=input_bytes,
            check=True,
            capture_output=True,
        )
        return proc.stdout.decode("utf-8").strip()

    def _init(self, root: Path) -> None:
        self._run(root, "init", "-q")
        self._run(root, "config", "user.name", "PEM Canonical Git Test")
        self._run(root, "config", "user.email", "pem-canonical@example.invalid")

    def _commit(self, root: Path, message: str) -> str:
        self._run(root, "add", "-A")
        self._run(root, "commit", "-q", "-m", message)
        return self._run(root, "rev-parse", "HEAD")

    def _doc(self, root: Path, accepted: str) -> pem.PemDocument:
        return pem.PemDocument(
            root=root / "PROJECT-ENGINEERING-MEMORY.md",
            metadata={
                "repository": "local",
                "accepted_base": {"project_state": accepted},
            },
            families={},
            notices={},
            sources={},
            root_text="",
        )

    def _siblings(self, root: Path) -> tuple[str, str, str]:
        (root / "owner.md").write_text(
            "CANONICAL OWNER\ncanonical-anchor\n",
            encoding="utf-8",
        )
        base = self._commit(root, "base")
        self._run(root, "checkout", "-q", "-b", "left")
        (root / "left.txt").write_text("left\n", encoding="utf-8")
        left = self._commit(root, "left")
        self._run(root, "checkout", "-q", "-b", "right", base)
        (root / "right.txt").write_text("right\n", encoding="utf-8")
        right = self._commit(root, "right")
        return base, left, right

    def _replace_parent(self, root: Path, replaced: str, parent: str) -> None:
        tree = self._run(root, "rev-parse", f"{replaced}^{{tree}}")
        replacement = self._run(
            root,
            "commit-tree",
            tree,
            "-p",
            parent,
            "-m",
            "replacement parent",
        )
        self._run(root, "replace", replaced, replacement)

    def _write_graft(self, root: Path, commit: str, parent: str) -> None:
        git_dir = Path(self._run(root, "rev-parse", "--git-dir"))
        if not git_dir.is_absolute():
            git_dir = root / git_dir
        grafts = git_dir / "info" / "grafts"
        grafts.parent.mkdir(parents=True, exist_ok=True)
        grafts.write_text(f"{commit} {parent}\n", encoding="utf-8")

    def test_authority_binding_rejects_replace_rewritten_sibling(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self._init(root)
            _, left, right = self._siblings(root)
            self._replace_parent(root, right, left)
            self.assertEqual(
                subprocess.run(
                    [
                        "git",
                        "-C",
                        str(root),
                        "merge-base",
                        "--is-ancestor",
                        left,
                        right,
                    ]
                ).returncode,
                0,
            )
            with self.assertRaisesRegex(pem.PemError, "not contained"):
                pem._validate_owner_binding(
                    f"local@{left}:owner.md",
                    self._doc(root, right),
                    "authority owner",
                )

    def test_authority_binding_rejects_graft_rewritten_sibling(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self._init(root)
            _, left, right = self._siblings(root)
            self._write_graft(root, right, left)
            self.assertEqual(
                subprocess.run(
                    [
                        "git",
                        "-C",
                        str(root),
                        "--no-replace-objects",
                        "merge-base",
                        "--is-ancestor",
                        left,
                        right,
                    ]
                ).returncode,
                0,
            )
            with self.assertRaisesRegex(pem.PemError, "not contained"):
                pem._validate_owner_binding(
                    f"local@{left}:owner.md",
                    self._doc(root, right),
                    "authority owner",
                )

    def test_evidence_locator_reads_canonical_bytes_under_replace(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self._init(root)
            (root / "evidence.md").write_text(
                "CANONICAL\ncanonical-anchor\n",
                encoding="utf-8",
            )
            canonical = self._commit(root, "canonical evidence")
            (root / "evidence.md").write_text("FORGED\n", encoding="utf-8")
            forged = self._commit(root, "forged replacement")
            self._run(root, "replace", canonical, forged)

            route = pem.parse_evidence_route(
                f"local@{canonical}:evidence.md#canonical-anchor"
            )
            self.assertEqual(
                pem.evidence_route_health(
                    route,
                    self._doc(root, forged),
                ),
                (
                    "HEALTHY",
                    "commit, repository path, and stable locator resolve",
                ),
            )

    def test_repair_acceptance_containment_rejects_overlay(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self._init(root)
            (root / "acceptance.md").write_text("placeholder\n", encoding="utf-8")
            base = self._commit(root, "base")
            self._run(root, "checkout", "-q", "-b", "left")
            (root / "left.txt").write_text("left\n", encoding="utf-8")
            left = self._commit(root, "left acceptance")
            self._run(root, "checkout", "-q", "-b", "right", base)
            (root / "right.txt").write_text("right\n", encoding="utf-8")
            right = self._commit(root, "right accepted project")
            self._replace_parent(root, right, left)

            route = pem.parse_evidence_route(f"local@{left}:acceptance.md")
            with self.assertRaisesRegex(pem.PemError, "not contained"):
                pem._validate_repair_acceptance_routes(
                    [route],
                    self._doc(root, right),
                    root,
                    "commit:" + ("a" * 40),
                    "recurrence",
                )

    def test_patch_id_is_stable_under_replacement_object(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self._init(root)
            (root / "value.txt").write_text("base\n", encoding="utf-8")
            self._commit(root, "base")
            (root / "value.txt").write_text(
                "canonical change\n",
                encoding="utf-8",
            )
            event = self._commit(root, "event")
            expected = pem._git_patch_id(root, event)
            self.assertIsNotNone(expected)

            (root / "value.txt").write_text(
                "replacement change\n",
                encoding="utf-8",
            )
            forged = self._commit(root, "forged")
            self._run(root, "replace", event, forged)
            self.assertEqual(pem._git_patch_id(root, event), expected)

    def test_readable_alternate_store_remains_usable(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            source = Path(td) / "source"
            shared = Path(td) / "shared"
            source.mkdir()
            self._init(source)
            (source / "owner.md").write_text("owner\nanchor\n", encoding="utf-8")
            accepted = self._commit(source, "accepted")
            subprocess.run(
                ["git", "clone", "-q", "--shared", str(source), str(shared)],
                check=True,
            )
            route = pem.parse_evidence_route(
                f"local@{accepted}:owner.md#anchor"
            )
            self.assertEqual(
                pem.evidence_route_health(
                    route,
                    self._doc(shared, accepted),
                )[0],
                "HEALTHY",
            )


    def test_movable_branch_revision_never_becomes_durable_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self._init(root)
            (root / "owner.md").write_text("owner\nanchor\n", encoding="utf-8")
            base = self._commit(root, "base owner")
            self._run(root, "branch", "durable-owner", base)
            (root / "later.txt").write_text("later\n", encoding="utf-8")
            accepted = self._commit(root, "accepted descendant")

            raw = "local@durable-owner:owner.md#anchor"
            route = pem.parse_evidence_route(raw)
            self.assertEqual(
                pem.evidence_route_health(route, self._doc(root, accepted))[0],
                "REVIEW_REQUIRED",
            )
            with self.assertRaisesRegex(pem.PemError, "not mechanically healthy"):
                pem._validate_owner_binding(raw, self._doc(root, accepted), "authority owner")

            self._run(root, "branch", "-f", "durable-owner", accepted)
            self.assertEqual(
                pem.evidence_route_health(route, self._doc(root, accepted))[0],
                "REVIEW_REQUIRED",
            )

    def test_movable_tag_revision_never_becomes_durable_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self._init(root)
            (root / "evidence.md").write_text("evidence\nanchor\n", encoding="utf-8")
            base = self._commit(root, "base evidence")
            self._run(root, "tag", "moving-evidence", base)
            (root / "later.txt").write_text("later\n", encoding="utf-8")
            accepted = self._commit(root, "accepted descendant")

            route = pem.parse_evidence_route("local@moving-evidence:evidence.md#anchor")
            self.assertEqual(
                pem.evidence_route_health(route, self._doc(root, accepted))[0],
                "REVIEW_REQUIRED",
            )
            self._run(root, "tag", "-f", "moving-evidence", accepted)
            self.assertEqual(
                pem.evidence_route_health(route, self._doc(root, accepted))[0],
                "REVIEW_REQUIRED",
            )

    def test_repair_acceptance_rejects_movable_revision(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self._init(root)
            (root / "acceptance.md").write_text("placeholder\n", encoding="utf-8")
            base = self._commit(root, "acceptance base")
            self._run(root, "branch", "moving-acceptance", base)
            (root / "later.txt").write_text("later\n", encoding="utf-8")
            accepted = self._commit(root, "accepted descendant")
            route = pem.parse_evidence_route("local@moving-acceptance:acceptance.md")
            with self.assertRaisesRegex(pem.PemError, "not resolvable"):
                pem._validate_repair_acceptance_routes(
                    [route],
                    self._doc(root, accepted),
                    root,
                    "commit:" + ("a" * 40),
                    "recurrence",
                )

    def test_directory_path_is_not_a_file_evidence_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self._init(root)
            (root / "evidence").mkdir()
            (root / "evidence" / "record.md").write_text("record\n", encoding="utf-8")
            accepted = self._commit(root, "directory evidence")
            route = pem.parse_evidence_route(f"local@{accepted}:evidence")
            health, reason = pem.evidence_route_health(route, self._doc(root, accepted))
            self.assertEqual(health, "UNAVAILABLE")
            self.assertIn("not a file/blob", reason)

    def test_repository_route_rejects_backslash_path_syntax(self) -> None:
        with self.assertRaisesRegex(pem.PemError, "POSIX syntax"):
            pem.parse_evidence_route(
                "local@" + ("a" * 40) + r":evidence\\record.md"
            )

    def test_observation_correction_requires_durable_healthy_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self._init(root)
            (root / "correction.md").write_text("correction\n", encoding="utf-8")
            base = self._commit(root, "correction evidence")
            self._run(root, "branch", "moving-correction", base)
            (root / "later.txt").write_text("later\n", encoding="utf-8")
            accepted = self._commit(root, "accepted descendant")

            old = {"observation": "old"}
            old_hash = __import__("hashlib").sha256(b"old").hexdigest()
            new = {
                "observation": "new",
                "observation_correction": {
                    "previous_sha256": old_hash,
                    "previous_observation": "old",
                    "corrected_observation": "new",
                    "reason": "clerical correction",
                    "evidence": ["local@moving-correction:correction.md"],
                },
            }
            error = pem._validate_observation_correction(
                "event-1",
                ("FF-001", "O01", old),
                ("FF-001", "O01", new),
                self._doc(root, accepted),
            )
            self.assertIsNotNone(error)
            self.assertIn("not mechanically healthy", error)


if __name__ == "__main__":
    unittest.main()
