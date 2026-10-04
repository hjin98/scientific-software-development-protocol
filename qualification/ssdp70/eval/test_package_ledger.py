"""Package-access ledger and exact accounting discriminators (D3-PACKAGE-ACCESS-LEDGER-OBSERVATION-DECISION).

The watcher tests use the real kernel mechanism and a real sandboxed reader through a read-only bind.
The accounting tests feed the production `account` function ledgers produced by that watcher;
only the model-visible tool-result events are constructed. The assembled OMP path is in
test_activation_accounting.py.
"""
import copy
import json
import os
import shutil
import subprocess
import tempfile
import time
import unittest
from pathlib import Path

import package_ledger as pl

SKILL_A = "---\nname: a\n---\n# A\nentrypoint text line one\nentrypoint text line two\n"
OWNER = "\n".join(f"owner line {i} with enough distinctive words to matter" for i in range(40)) + "\n"
OTHER = "\n".join(f"other reference line {i} unrelated wording" for i in range(30)) + "\n"


def bwrap_usable():
    return shutil.which("bwrap") is not None and subprocess.run(
        ["bwrap", "--unshare-user", "--ro-bind", "/usr", "/usr", "--ro-bind", "/lib64", "/lib64", "--symlink", "usr/bin", "/bin",
         "--symlink", "usr/lib", "/lib", "/bin/true"], capture_output=True).returncode == 0


def make_tree(root: Path):
    (root / "a" / "references").mkdir(parents=True)
    (root / "b").mkdir()
    (root / "a" / "SKILL.md").write_text(SKILL_A)
    (root / "a" / "references" / "owner.md").write_text(OWNER)
    (root / "a" / "references" / "other.md").write_text(OTHER)
    (root / "b" / "SKILL.md").write_text("---\nname: b\n---\n# B\n")


def sandbox_read(root: Path, command: str) -> None:
    subprocess.run(["bwrap", "--unshare-user", "--unshare-pid", "--ro-bind", "/usr", "/usr", "--ro-bind", "/lib64", "/lib64",
                    "--symlink", "usr/bin", "/bin", "--symlink", "usr/lib", "/lib", "--ro-bind", str(root), "/opt/ssdp/skills",
                    "--proc", "/proc", "--dev", "/dev", "/bin/sh", "-c", command], capture_output=True, check=True)


def event(sequence, text, *, kind="tool_action", seen=True):
    return {"sequence": sequence, "kind": kind, "status": "result",
            "payload": {"result_status": "result", "result_content": text, "result_seen_by_model": seen,
                        "semantic_capability_classes": ["process_execution"]}}


def led(opens, *, cut=1000, extra=None, **overrides):
    """Ledger with explicit (t_ns, rel, flags) rows over the standard tree."""
    tree = {"a/SKILL.md": len(SKILL_A), "a/references/owner.md": len(OWNER), "a/references/other.md": len(OTHER),
            "b/SKILL.md": 22}
    rows = [{"t_ns": t, "rel": rel, "dir": False, "flags": flags or ["open", "access", "close_nowrite"]}
            for t, rel, flags in opens]
    ledger = {"schema": pl.SCHEMA, "mechanism": pl.MECHANISM, "root": "x", "established": True, "error": None,
              "tree_files": tree, "overflow": False, "events": rows + list(extra or [])}
    ledger.update(overrides)
    return ledger


class WatcherUsesRealKernelObservation(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "skills"
        make_tree(self.root)

    def tearDown(self):
        self.tmp.cleanup()

    def record(self, command):
        watch = pl.LedgerWatcher(self.root).start()
        self.assertTrue(watch.established, watch.error)
        sandbox_read(self.root, command)
        time.sleep(0.05)
        return watch.stop()

    @unittest.skipUnless(bwrap_usable(), "bwrap unusable")
    def test_sandboxed_process_reads_are_recorded_through_a_read_only_bind(self):
        record = self.record("cat /opt/ssdp/skills/a/references/owner.md >/dev/null; wc -c /opt/ssdp/skills/a/SKILL.md >/dev/null; ls /opt/ssdp/skills/a >/dev/null")
        files = {}
        for row in record["events"]:
            if not row["dir"] and row["rel"] in record["tree_files"]:
                files.setdefault(row["rel"], set()).update(row["flags"])
        self.assertIn("access", files["a/references/owner.md"])
        self.assertIn("open", files["a/SKILL.md"])
        self.assertNotIn("access", files["a/SKILL.md"])      # wc -c opens but reads no content
        self.assertNotIn("a/references/other.md", files)     # never opened => exactly not read
        self.assertNotIn("b/SKILL.md", files)
        self.assertFalse(record["overflow"])
        self.assertEqual(record["tree_files"]["a/SKILL.md"], len(SKILL_A))

    def test_unestablished_ledger_and_mutation_make_observation_inexact(self):
        missing = pl.LedgerWatcher(self.root / "absent").start()
        self.assertFalse(missing.established)
        self.assertFalse(pl.account(missing.stop(), None, [], self.root)["exact"])
        watch = pl.LedgerWatcher(self.root).start()
        (self.root / "a" / "references" / "other.md").write_text("changed")
        time.sleep(0.05)
        record = watch.stop()
        result = pl.account(record, None, [], self.root)
        self.assertFalse(result["exact"])
        self.assertTrue(any("changed or lost" in r for r in result["reasons"]), result["reasons"])


class AccountingFailsClosed(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        make_tree(self.root)

    def tearDown(self):
        self.tmp.cleanup()

    def account(self, ledger, events, cut=1000):
        return pl.account(ledger, cut, events, self.root)

    def test_cat_of_owner_is_exact_and_attributed(self):
        ledger = led([(10, "a/SKILL.md", None), (11, "b/SKILL.md", None), (2000, "a/references/owner.md", None)])
        result = self.account(ledger, [event(7, OWNER)])
        self.assertTrue(result["exact"], result["reasons"])
        self.assertEqual(result["supplied"]["a/references/owner.md"]["sequences"], [7])
        self.assertEqual(result["consumed_files"], {"a/references/owner.md": len(OWNER)})
        self.assertEqual(result["opened_pre_request0"], ["a/SKILL.md", "b/SKILL.md"])

    def test_unexplained_post_request_open_is_inexact_and_names_the_file(self):
        ledger = led([(2000, "a/references/owner.md", None)])
        for output in ("40\n", "sha256 digest", "", "b3duZXIgbGluZQ=="):
            with self.subTest(output=output):
                result = self.account(ledger, [event(3, output)])
                self.assertFalse(result["exact"])
                self.assertEqual([u["file"] for u in result["unexplained"]], ["a/references/owner.md"])

    def test_output_not_seen_by_the_model_is_not_supply(self):
        ledger = led([(2000, "a/references/owner.md", None)])
        self.assertFalse(self.account(ledger, [event(3, OWNER, seen=False)])["exact"])

    def test_contiguous_forms_of_supply(self):
        ledger = led([(2000, "a/references/owner.md", None)])
        head = "".join(OWNER.splitlines(True)[:6])
        numbered = "".join(f"{i + 1:6d}\t{line}" for i, line in enumerate(OWNER.splitlines(True)))
        for name, text, match in (("exact", "--- begin ---\n" + OWNER + "--- end ---", "exact"), ("head", head, "partial"),
                                  ("cat -n", numbered, "exact")):
            with self.subTest(name):
                result = self.account(ledger, [event(4, text)])
                self.assertTrue(result["exact"], result["reasons"])
                self.assertEqual(result["supplied"]["a/references/owner.md"]["match"], match)
        # grep-like output shows distinctive source lines: content did reach the model (partial supply).
        scattered = "\n".join(f"{i + 1}:{l}" for i, l in enumerate(OWNER.splitlines()) if i % 7 == 0)
        grep_like = self.account(ledger, [event(4, scattered)])
        self.assertTrue(grep_like["exact"], grep_like["reasons"])
        self.assertEqual(grep_like["supplied"]["a/references/owner.md"]["match"], "partial")
        # Fragments too short to be distinctive (counts, one word, a short prefix) do not explain an open.
        for fragment in ("owner", "owner line 3", "40 lines", "owner line 1 with"):
            with self.subTest(fragment=fragment):
                self.assertFalse(self.account(ledger, [event(4, fragment)])["exact"])

    def test_pre_request_opens_other_than_entrypoints_are_unexplained(self):
        ledger = led([(10, "a/references/owner.md", None)])
        result = self.account(ledger, [])
        self.assertFalse(result["exact"])
        self.assertEqual(result["unexplained"][0]["phase"], "pre-request0")
        ok = self.account(led([(10, "a/SKILL.md", None), (11, "b/SKILL.md", None)]), [])
        self.assertTrue(ok["exact"], ok["reasons"])

    def test_run_without_request_zero_treats_every_open_as_runtime_startup(self):
        result = pl.account(led([(2000, "a/references/owner.md", None)]), None, [], self.root)
        self.assertFalse(result["exact"])
        self.assertEqual(result["unexplained"][0]["phase"], "pre-request0")

    def test_ledger_loss_overflow_and_absence_are_inexact(self):
        for bad in (None, led([], overflow=True), led([], established=False, error="boom"), led([], schema=99), led([], events="x"),
                    led([], mechanism="other")):
            with self.subTest(bad=str(bad)[:40]):
                self.assertFalse(self.account(bad, [])["exact"])
        for flag in ("modify", "unmount", "ignored", "delete", "attrib", "create"):
            with self.subTest(flag=flag):
                ledger = led([], extra=[{"t_ns": 1500, "rel": "a/SKILL.md", "dir": False, "flags": [flag]}])
                self.assertFalse(self.account(ledger, [])["exact"])

    def test_native_consumption_must_agree_with_the_ledger(self):
        native = {"sequence": 9, "kind": "resource_access", "status": "result",
                  "payload": {"result_status": "result", "result_content": "1#AB:x", "result_seen_by_model": True,
                              "consumed_resource": {"logical_root": "a", "package_relative_path": "references/owner.md",
                                                    "match": "exact"}}}
        self.assertFalse(self.account(led([]), [native])["exact"])  # model consumed it; ledger saw no open
        agreed = self.account(led([(2000, "a/references/owner.md", None)]), [native])
        self.assertTrue(agreed["exact"], agreed["reasons"])
        self.assertEqual(agreed["supplied"]["a/references/owner.md"]["sequences"], [9])

    def test_directory_listing_alone_reads_no_package_content(self):
        ledger = led([], extra=[{"t_ns": 2000, "rel": "a/references", "dir": True, "flags": ["open", "access", "close_nowrite"]}])
        result = self.account(ledger, [event(2, "other.md\nowner.md")])
        self.assertTrue(result["exact"], result["reasons"])
        self.assertEqual(result["consumed_files"], {})


if __name__ == "__main__":
    unittest.main()
