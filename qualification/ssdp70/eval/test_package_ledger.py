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

import core70
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


def event(sequence, text, *, kind="tool_action", seen=True, command=None, req=None):
    return {"sequence": sequence, "kind": kind, "status": "result",
            "payload": {"result_status": "result", "result_content": text, "result_seen_by_model": seen,
                        "result_request_index": req,
                        "input": {"command": command or "cat something"},
                        "semantic_capability_classes": ["process_execution"]}}


def led(opens, *, cut=1000, extra=None, **overrides):
    """Ledger with explicit (t_ns, rel, flags) rows over the standard tree."""
    tree = {"a/SKILL.md": len(SKILL_A), "a/references/owner.md": len(OWNER), "a/references/other.md": len(OTHER),
            "b/SKILL.md": 22}
    rows = [{"first_ns": t, "last_ns": t, "count": 1, "rel": rel, "dir": False,
             "flags": flags or ["open", "access", "close_nowrite"]} for t, rel, flags in opens]
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
        for extra in ({"read_errors": ["OSError: boom"]}, {"rows_truncated": True}):
            with self.subTest(extra=extra):
                self.assertFalse(self.account(led([], **extra), [])["exact"])
        for flag in ("modify", "unmount", "ignored", "delete", "attrib", "create"):
            with self.subTest(flag=flag):
                ledger = led([], extra=[{"first_ns": 1500, "last_ns": 1500, "count": 1, "rel": "a/SKILL.md", "dir": False, "flags": [flag]}])
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
        ledger = led([], extra=[{"first_ns": 2000, "last_ns": 2000, "count": 1, "rel": "a/references", "dir": True, "flags": ["open", "access", "close_nowrite"]}])
        result = self.account(ledger, [event(2, "other.md\nowner.md")])
        self.assertTrue(result["exact"], result["reasons"])
        self.assertEqual(result["consumed_files"], {})


# Package with the properties of the shipped one: byte-identical twins across roots, a shared block
# between an entrypoint and a reference, and a tiny version file contained in other files.
KERNEL = "shared kernel block: route each change to its earliest affected owner and never silently change an upstream contract\n"
TWIN = "\n".join(f"twin owner line {i} with enough distinctive words to matter" for i in range(30)) + "\n"
REF = KERNEL + "\n".join(f"reference only line {i} with distinctive wording" for i in range(30)) + "\n"
ENTRY_X = "---\nname: x\n---\n# X\n" + KERNEL + "entry x text\n"
ENTRY_Y = "---\nname: y\n---\n# Y\n" + KERNEL + "entry y text\n"
FILES = {"x/SKILL.md": ENTRY_X, "x/PROTOCOL_VERSION": "7.0.0\n", "x/references/ref.md": REF, "x/references/owner.md": TWIN,
         "y/SKILL.md": ENTRY_Y, "y/PROTOCOL_VERSION": "7.0.0\n", "y/references/owner.md": TWIN}
MOUNT = "/opt/ssdp/skills"


def overlap_ledger(opens, **overrides):
    tree = {rel: len(text.encode()) for rel, text in FILES.items()}
    rows = [{"first_ns": t, "last_ns": t, "count": 1, "rel": rel, "dir": False, "flags": ["open", "access", "close_nowrite"]}
            for t, rel in opens]
    ledger = {"schema": pl.SCHEMA, "mechanism": pl.MECHANISM, "root": "x", "established": True, "error": None,
              "tree_files": tree, "overflow": False, "events": rows}
    ledger.update(overrides)
    return ledger


class SupplyIdentifiesTheOpenedFile(unittest.TestCase):
    """Content shown for one file must not explain an open of a different file (review SC-1)."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        for rel, text in FILES.items():
            (self.root / rel).parent.mkdir(parents=True, exist_ok=True)
            (self.root / rel).write_text(text)

    def tearDown(self):
        self.tmp.cleanup()

    def account(self, opens, events, **kw):
        return pl.account(overlap_ledger(opens), 1000, events, self.root, mount=MOUNT, owner_name="owner.md", **kw)

    def test_shared_kernel_block_in_an_entrypoint_does_not_explain_a_size_probe_of_a_reference(self):
        result = self.account([(2000, "x/SKILL.md"), (2001, "x/references/ref.md")],
                              [event(3, ENTRY_X, command=f"cat {MOUNT}/x/SKILL.md"),
                               event(4, "1234 size", command=f"wc -c {MOUNT}/x/references/ref.md")])
        self.assertFalse(result["exact"])
        self.assertEqual([u["file"] for u in result["unexplained"]], ["x/references/ref.md"])
        self.assertEqual(sorted(result["consumed_files"]), ["x/SKILL.md"])

    def test_byte_identical_twin_shown_for_another_path_does_not_explain_the_unshown_twin(self):
        result = self.account([(2000, "y/references/owner.md"), (2001, "x/references/owner.md")],
                              [event(5, TWIN, command=f"cat {MOUNT}/y/references/owner.md"),
                               event(6, "30 lines", command=f"wc -l {MOUNT}/x/references/owner.md")])
        self.assertFalse(result["exact"])
        self.assertEqual(result["supplied"]["y/references/owner.md"]["sequences"], [5])
        self.assertNotIn("x/references/owner.md", result["supplied"])
        self.assertFalse(result["owner_read_exact"])           # an unexplained owner copy blocks the owner question

    def test_twins_each_shown_by_an_action_naming_them_are_both_supplied(self):
        result = self.account([(2000, "y/references/owner.md"), (2001, "x/references/owner.md")],
                              [event(5, TWIN + TWIN, command=f"cat {MOUNT}/y/references/owner.md {MOUNT}/x/references/owner.md")])
        self.assertTrue(result["exact"], result["reasons"])
        self.assertEqual(result["consumed_files"], {"y/references/owner.md": len(TWIN), "x/references/owner.md": len(TWIN)})

    def test_tiny_file_is_not_explained_by_any_output_that_contains_its_text(self):
        result = self.account([(2000, "x/PROTOCOL_VERSION")], [event(2, "python 3.11; protocol 7.0.0 ok", command="python3 -V")])
        self.assertFalse(result["exact"])
        named = self.account([(2000, "x/PROTOCOL_VERSION")], [event(2, "7.0.0\n", command=f"cat {MOUNT}/x/PROTOCOL_VERSION")])
        self.assertTrue(named["exact"], named["reasons"])

    def test_path_prefix_is_a_boundary_not_a_substring(self):
        result = self.account([(2000, "y/references/owner.md")],
                              [event(5, TWIN, command=f"cat {MOUNT}/xy/references/owner.md; echo {MOUNT}/zy/references/owner.md")])
        self.assertFalse(result["exact"])

    def test_distinctive_partial_block_still_supplies_without_naming_the_path(self):
        head = "".join(REF.splitlines(True)[3:12])        # lines unique to the reference
        result = self.account([(2000, "x/references/ref.md")], [event(7, head, command="head -n 12 references/ref.md")])
        self.assertTrue(result["exact"], result["reasons"])
        self.assertEqual(result["supplied"]["x/references/ref.md"]["match"], "partial")


class PhaseAndDelivery(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        for rel, text in FILES.items():
            (self.root / rel).parent.mkdir(parents=True, exist_ok=True)
            (self.root / rel).write_text(text)

    def tearDown(self):
        self.tmp.cleanup()

    def test_clock_skew_cannot_undercount_a_supplied_entrypoint(self):
        # A model read of another root's SKILL.md whose ledger stamp lands before the cut (clock step back).
        for stamp in (2000, 999):
            with self.subTest(stamp=stamp):
                result = pl.account(overlap_ledger([(stamp, "y/SKILL.md")]), 1000,
                                    [event(4, ENTRY_Y, command=f"cat {MOUNT}/y/SKILL.md")], self.root, mount=MOUNT)
                self.assertEqual(result["consumed_files"], {"y/SKILL.md": len(ENTRY_Y.encode())})

    def test_skew_moves_a_non_entrypoint_open_only_to_the_stricter_class(self):
        result = pl.account(overlap_ledger([(999, "x/references/ref.md")]), 1000, [event(4, REF, command=f"cat {MOUNT}/x/references/ref.md")],
                            self.root, mount=MOUNT)
        self.assertFalse(result["exact"])
        self.assertEqual(result["unexplained"][0]["phase"], "pre-request0")

    def test_reopening_the_delivered_entrypoint_is_explained_by_delivery(self):
        result = pl.account(overlap_ledger([(2000, "x/SKILL.md")]), 1000, [event(3, "99 bytes", command=f"wc -c {MOUNT}/x/SKILL.md")],
                            self.root, mount=MOUNT, delivered={"x/SKILL.md"})
        self.assertTrue(result["exact"], result["reasons"])
        self.assertEqual(result["explained_by_delivery"], ["x/SKILL.md"])
        undelivered = pl.account(overlap_ledger([(2000, "y/SKILL.md")]), 1000, [event(3, "99 bytes")], self.root, mount=MOUNT,
                                 delivered={"x/SKILL.md"})
        self.assertFalse(undelivered["exact"])

    def test_entrypoint_only_run_with_exact_ledger_is_exact_and_names_no_opened_file(self):
        result = pl.account(overlap_ledger([(10, "x/SKILL.md"), (11, "y/SKILL.md")]), 1000, [], self.root, mount=MOUNT,
                            delivered={"x/SKILL.md"}, owner_name="owner.md")
        self.assertTrue(result["exact"], result["reasons"])
        self.assertEqual(result["consumed_files"], {})
        self.assertTrue(result["owner_read_exact"])

    def test_unrelated_unexplained_file_leaves_the_owner_question_exact(self):
        result = pl.account(overlap_ledger([(2000, "x/references/ref.md")]), 1000, [event(2, "n/a", command="wc -c ref.md")],
                            self.root, mount=MOUNT, owner_name="owner.md")
        self.assertFalse(result["exact"])
        self.assertTrue(result["owner_read_exact"])
        for broken in (overlap_ledger([], overflow=True), overlap_ledger([(2000, "x/references/owner.md")])):
            with self.subTest(broken=str(broken)[-60:]):
                self.assertFalse(pl.account(broken, 1000, [event(2, "n/a", command="x")], self.root, mount=MOUNT,
                                            owner_name="owner.md")["owner_read_exact"])


class OwnerReadTimeIsAccessNotDisplay(unittest.TestCase):
    """Revision 3 (review N-1): an owner open before R2 cannot hide behind a later full display."""
    STAMPS = {0: 900, 1: 2500, 2: 3000, 3: 4000}

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        for rel, text in FILES.items():
            (self.root / rel).parent.mkdir(parents=True, exist_ok=True)
            (self.root / rel).write_text(text)

    def tearDown(self):
        self.tmp.cleanup()

    def account(self, opens, events, stamps="default"):
        return pl.account(overlap_ledger(opens), 1000, events, self.root, mount=MOUNT, owner_name="owner.md",
                          request_stamps=self.STAMPS if stamps == "default" else stamps)

    def hidden_then_shown(self):
        opens = [(2000, "x/references/owner.md"), (3500, "x/references/owner.md")]
        events = [event(4, "30 owner.md", command=f"wc -l {MOUNT}/x/references/owner.md", req=1),
                  event(9, TWIN, command=f"cat {MOUNT}/x/references/owner.md", req=3)]
        return opens, events

    def test_unshown_open_before_r2_bounds_the_owner_read_before_the_later_display(self):
        opens, events = self.hidden_then_shown()
        result = self.account(opens, events)
        self.assertTrue(result["owner_read_exact"], result["reasons"])
        self.assertEqual(result["supplied"]["x/references/owner.md"]["sequences"], [9])
        self.assertEqual(result["owner_access"]["x/references/owner.md"]["sequence"], 4)

    def test_same_open_without_request_stamps_makes_the_owner_question_inexact(self):
        opens, events = self.hidden_then_shown()
        result = self.account(opens, events, stamps=None)
        self.assertFalse(result["owner_read_exact"])
        self.assertEqual(result["owner_access_unresolved"], ["x/references/owner.md"])

    def test_non_owner_opens_add_no_owner_access_and_do_not_disturb_it(self):
        result = self.account([(2000, "x/references/ref.md")], [event(4, REF, command=f"cat {MOUNT}/x/references/ref.md", req=1)])
        self.assertEqual(result["owner_access"], {})
        self.assertTrue(result["owner_read_exact"])

    def test_open_after_the_last_request_is_bounded_by_the_end_of_the_trace(self):
        result = self.account([(5000, "x/references/owner.md")], [event(4, TWIN, command=f"cat {MOUNT}/x/references/owner.md", req=3)])
        self.assertEqual(result["owner_access"]["x/references/owner.md"]["basis"], "after-last-request")

    def test_owner_copies_have_one_recognition_rule(self):
        self.assertTrue(pl.is_owner_copy("y/references/owner.md", "owner.md"))
        self.assertTrue(pl.is_owner_copy("owner.md", "owner.md"))
        self.assertFalse(pl.is_owner_copy("y/references/owner.md.bak", "owner.md"))
        self.assertFalse(pl.is_owner_copy("y/references/owner.md", None))


class ClaimGateRequiresDeliveryProof(unittest.TestCase):
    def test_failed_delivery_is_not_admitted_by_an_exact_ledger(self):
        root = {"kind": "root_selection", "status": "error", "sequence": 1,
                "payload": {"resolved_package_identity": {"package_sha256": "a" * 64}, "delivery": {"delivered": False}}}
        self.assertTrue(core70.validate_claim_observability([root], ["t7-burden"], [], ledger_exact=True))
        root["payload"]["delivery"]["delivered"] = True
        self.assertEqual(core70.validate_claim_observability([root], ["t7-burden"], [], ledger_exact=True), [])


class WatcherBoundsItsRecord(unittest.TestCase):
    def test_repeated_events_fold_into_bounded_rows_and_read_errors_are_recorded(self):
        tmp = tempfile.TemporaryDirectory()
        root = Path(tmp.name)
        (root / "a").mkdir()
        (root / "a" / "f").write_text("x")
        watch = pl.LedgerWatcher(root).start()
        self.assertTrue(watch.established, watch.error)
        for _ in range(500):
            (root / "a" / "f").read_bytes()
        time.sleep(0.1)
        record = watch.stop()
        opens = [r for r in record["events"] if r["rel"] == "a/f" and "open" in r["flags"]]
        self.assertEqual(len(opens), 1)
        self.assertGreaterEqual(opens[0]["count"], 400)
        self.assertLessEqual(opens[0]["first_ns"], opens[0]["last_ns"])
        self.assertFalse(record["read_errors"])
        broken = pl.LedgerWatcher(root)
        broken.fd = 987654                       # an unexpected kernel read failure (EBADF)
        self.assertFalse(broken._drain_once())
        self.assertTrue(broken._read_errors)
        tmp.cleanup()


class ClaimGateHonoursAnExactLedger(unittest.TestCase):
    ROOT = {"kind": "root_selection", "status": "observed", "payload": {"resolved_package_identity": {"sha": "x"}}}

    def test_entrypoint_only_burden_claim_needs_an_exact_ledger_and_a_resolved_root(self):
        claims = ["active-byte burden"]
        self.assertTrue(core70.validate_claim_observability([self.ROOT], claims))
        self.assertEqual(core70.validate_claim_observability([self.ROOT], claims, ledger_exact=True), [])
        self.assertTrue(core70.validate_claim_observability([], claims, ledger_exact=True))   # no resolved root

    def test_owner_read_claim_is_not_satisfied_by_an_exact_ledger_alone(self):
        self.assertTrue(core70.validate_claim_observability([self.ROOT], ["owner-read"], ledger_exact=True))


if __name__ == "__main__":
    unittest.main()
