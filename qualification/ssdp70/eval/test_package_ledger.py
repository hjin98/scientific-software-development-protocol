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



TEST_PARAMETERS = {**pl.PARAMETERS, "clock_tolerance_ns": 0}

def bracketed(ledger):
    if not isinstance(ledger["events"],list):
        return ledger
    stamps = sorted({e["first_ns"] for e in ledger["events"]})
    beats = []
    for t in sorted({t for stamp in stamps for t in (stamp-1,stamp+1)}):
            beats.append({"index": len(beats), "before_ns": t, "after_ns": t, "before_mono_ns": t, "after_mono_ns": t})
    if not beats:
        beats = [{"index": i, "before_ns": t, "after_ns": t, "before_mono_ns": t, "after_mono_ns": t} for i,t in enumerate((0,10000))]
    for e in ledger["events"]:
        e["interval"] = next(i for i,b in enumerate(beats) if b["before_ns"] == e["first_ns"]-1)
    ledger.update(parameters=TEST_PARAMETERS, heartbeats=beats)
    return ledger

def led(opens, *, cut=1000, extra=None, **overrides):
    """Ledger with explicit (t_ns, rel, flags) rows over the standard tree."""
    tree = {"a/SKILL.md": len(SKILL_A), "a/references/owner.md": len(OWNER), "a/references/other.md": len(OTHER),
            "b/SKILL.md": len("---\nname: b\n---\n# B\n")}
    rows = [{"first_ns": t, "last_ns": t, "count": 1, "rel": rel, "dir": False,
             "flags": flags or ["open", "access", "close_nowrite"]} for t, rel, flags in opens]
    ledger = {"schema": pl.SCHEMA, "mechanism": pl.MECHANISM, "root": "x", "established": True, "error": None,
              "tree_files": tree, "overflow": False, "events": rows + list(extra or [])}
    ledger.update(overrides)
    return bracketed(ledger)


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
        return pl.account(ledger, cut, events, self.root, parameters=TEST_PARAMETERS)

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
    return bracketed(ledger)


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
        kw.setdefault("request_records", [{"t_ns": 1000, "pairing_verified": True, "monotonic_ns": 1000, "position": min((e["sequence"] for e in events), default=1)}])
        return pl.account(overlap_ledger(opens), 1000, events, self.root, mount=MOUNT, parameters=TEST_PARAMETERS, owner_name="owner.md", **kw)

    def test_shared_kernel_block_in_an_entrypoint_does_not_explain_a_size_probe_of_a_reference(self):
        result = self.account([(2000, "x/SKILL.md"), (2001, "x/references/ref.md")],
                              [event(3, ENTRY_X, command=f"cat {MOUNT}/x/SKILL.md"),
                               event(4, "1234 size", command=f"wc -c {MOUNT}/x/references/ref.md")])
        self.assertFalse(result["exact"])
        self.assertEqual([u["file"] for u in result["unexplained"]], ["x/references/ref.md"])
        self.assertEqual(sorted(result["consumed_files"]), ["x/SKILL.md"])

    def test_byte_identical_twin_shown_for_another_path_does_not_explain_the_unshown_twin(self):
        result = self.account([(2000, "y/references/owner.md"), (2001, "x/references/owner.md")],
                              [event(5, "".join(TWIN.splitlines(True)[:6]), command=f"head {MOUNT}/y/references/owner.md"),
                               event(6, "30 lines", command=f"wc -l {MOUNT}/x/references/owner.md")])
        self.assertFalse(result["exact"])
        self.assertEqual(result["supplied"]["y/references/owner.md"]["sequences"], [5])
        self.assertNotIn("x/references/owner.md", result["supplied"])
        self.assertTrue(result["owner_floor_exact"])  # window blocks no-read, not byte explanation

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
                              [event(5, "".join(TWIN.splitlines(True)[:6]), command=f"cat {MOUNT}/xy/references/owner.md; echo {MOUNT}/zy/references/owner.md")])
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
                                    [event(4, ENTRY_Y, command=f"cat {MOUNT}/y/SKILL.md")], self.root, mount=MOUNT, parameters=TEST_PARAMETERS)
                self.assertEqual(result["consumed_files"], {"y/SKILL.md": len(ENTRY_Y.encode())})

    def test_skew_moves_a_non_entrypoint_open_only_to_the_stricter_class(self):
        result = pl.account(overlap_ledger([(999, "x/references/ref.md")]), 1000, [event(4, REF, command=f"cat {MOUNT}/x/references/ref.md")],
                            self.root, mount=MOUNT, parameters=TEST_PARAMETERS)
        self.assertFalse(result["exact"])
        self.assertEqual(result["unexplained"][0]["phase"], "pre-request0")

    def test_reopening_the_delivered_entrypoint_is_explained_by_delivery(self):
        result = pl.account(overlap_ledger([(2000, "x/SKILL.md")]), 1000, [event(3, "99 bytes", command=f"wc -c {MOUNT}/x/SKILL.md")],
                            self.root, mount=MOUNT, parameters=TEST_PARAMETERS, delivered={"x/SKILL.md"})
        self.assertTrue(result["exact"], result["reasons"])
        self.assertEqual(result["explained_by_delivery"], ["x/SKILL.md"])
        undelivered = pl.account(overlap_ledger([(2000, "y/SKILL.md")]), 1000, [event(3, "99 bytes")], self.root, mount=MOUNT, parameters=TEST_PARAMETERS,
                                 delivered={"x/SKILL.md"})
        self.assertFalse(undelivered["exact"])

    def test_entrypoint_only_run_with_exact_ledger_is_exact_and_names_no_opened_file(self):
        result = pl.account(overlap_ledger([(10, "x/SKILL.md"), (11, "y/SKILL.md")]), 1000, [], self.root, mount=MOUNT, parameters=TEST_PARAMETERS,
                            delivered={"x/SKILL.md"}, owner_name="owner.md")
        self.assertTrue(result["exact"], result["reasons"])
        self.assertEqual(result["consumed_files"], {})
        self.assertTrue(result["owner_floor_exact"])

    def test_unrelated_unexplained_file_leaves_the_owner_question_exact(self):
        result = pl.account(overlap_ledger([(2000, "x/references/ref.md")]), 1000, [event(2, "n/a", command="wc -c ref.md")],
                            self.root, mount=MOUNT, parameters=TEST_PARAMETERS, owner_name="owner.md")
        self.assertFalse(result["exact"])
        self.assertTrue(result["owner_floor_exact"])
        for broken in (overlap_ledger([], overflow=True),):
            with self.subTest(broken=str(broken)[-60:]):
                self.assertFalse(pl.account(broken, 1000, [event(2, "n/a", command="x")], self.root, mount=MOUNT, parameters=TEST_PARAMETERS,
                                            owner_name="owner.md")["owner_floor_exact"])


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
        self.assertGreaterEqual(len(opens), 1)
        self.assertGreaterEqual(sum(r["count"] for r in opens), 400)
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

class Revision8OwnerEvidence(PhaseAndDelivery):
    def account(self, opens, events, **kwargs):
        kwargs.setdefault("request_records", [{"t_ns": 1000, "monotonic_ns": 1000, "position": min((e["sequence"] for e in events), default=1), "pairing_verified": True}])
        return pl.account(overlap_ledger(opens), 1000, events, self.root, mount=MOUNT,
                          parameters=TEST_PARAMETERS, owner_name="owner.md", **kwargs)

    def test_l_m_n_t_display_sequence_survives_lost_observation(self):
        events = [event(4, "30 lines"), event(9, TWIN)]
        for ledger in (None, overlap_ledger([(2000,"x/references/owner.md")], overflow=True)):
            result = pl.account(ledger, 1000, events, self.root, owner_name="owner.md", parameters=TEST_PARAMETERS)
            self.assertEqual([r["sequence"] for r in result["owner_read_observed"]], [9])
            self.assertFalse(result["owner_floor_exact"])
        result = self.account([(2000,"x/references/owner.md")], events)
        self.assertEqual([r["sequence"] for r in result["owner_read_observed"]], [9])
        self.assertEqual(result["owner_open_windows"][0]["window"]["start"], 4)

    def test_w_distinct_line_quantum_error_status_prefixes_and_chunks(self):
        lines = TWIN.splitlines()
        one = "one very long owner line " + "x"*300
        for rel in ("x/references/owner.md", "y/references/owner.md"):
            (self.root/rel).write_text(TWIN+one+"\n")
        for text in (one, "\n".join([lines[0]]*7), "\n".join(lines[:2])):
            r = pl.account(None, 1000, [event(3,text)], self.root, owner_name="owner.md", parameters=TEST_PARAMETERS)
            self.assertEqual(r["owner_read_observed"], [])
            self.assertEqual([v["sequence"] for v in r["owner_minor_exposure"]], [3])
        e = event(7, "\n".join(f"file:{i}:{line}" for i,line in enumerate(lines[:6])))
        e["status"] = e["payload"]["result_status"] = "error"
        r = pl.account(None, 1000, [e], self.root, owner_name="owner.md", parameters=TEST_PARAMETERS)
        self.assertEqual([v["sequence"] for v in r["owner_read_observed"]], [7])
        self.assertEqual(r["owner_minor_exposure"], [])

    def test_o_r_x_trace_order_windows_late_drain_background_and_fallback(self):
        events = [event(i,"nothing") for i in range(1,11)]
        requests = [{"t_ns": t, "pairing_verified": True, "monotonic_ns": t, "position": pos} for t,pos in ((1000,1),(1500,4),(3000,8))]
        r = self.account([(2000,"x/references/owner.md"),(5000,"x/references/owner.md")],events, request_records=requests)
        self.assertEqual([v["window"]["start"] for v in r["owner_open_windows"]], [4,8])
        requests[1]["position"] = 1
        r = self.account([(2000,"x/references/owner.md")],events, request_records=requests)
        self.assertEqual(r["owner_open_windows"][0]["window"]["start"],1)
        requests[1]["t_ns"] = 500
        r = self.account([(2000,"x/references/owner.md")],events, request_records=requests)
        self.assertFalse(r["owner_floor_exact"])
        self.assertEqual(r["owner_open_windows"][0]["window"]["start"],1)

    def test_p_q_clock_divergence_gap_and_width_never_hide_supply(self):
        for kind in ("clock", "gap", "width", "ends"):
            ledger = overlap_ledger([(2000,"x/references/owner.md"),(4000,"x/references/owner.md")])
            if kind == "clock":
                ledger["heartbeats"][0]["before_mono_ns"] -= 100
            elif kind == "gap":
                ledger["parameters"] = {**TEST_PARAMETERS,"heartbeat_gap_bound_ns":1}
            elif kind == "width":
                ledger["parameters"] = {**TEST_PARAMETERS,"bracket_width_bound_ns":1}
            else:
                ledger["heartbeats"] = []
            r = pl.account(ledger,1000,[event(9,TWIN)],self.root,owner_name="owner.md",parameters=ledger["parameters"])
            self.assertFalse(r["owner_floor_exact"],kind)
            self.assertEqual([v["sequence"] for v in r["owner_read_observed"]],[9])

    def test_s_whole_file_twin_in_window_but_never_partial_or_shared_block(self):
        for text,exact in ((TWIN,True),("\n".join(TWIN.splitlines()[:6]),False),(KERNEL,False)):
            r = self.account([(2000,"x/references/owner.md")],[event(4,text)])
            self.assertEqual(r["exact"],exact,r["reasons"])
            if exact:
                self.assertEqual(r["supplied"]["x/references/owner.md"]["routes"],["whole-file-in-window"])

    def test_k_basename_is_the_only_copy_rule(self):
        self.assertTrue(pl.is_owner_copy("x/references/owner.md","owner.md"))
        self.assertFalse(pl.is_owner_copy("x/references/owner.md.bak","owner.md"))
        from adapters import omp
        fake={"kind":"resource_access","status":"result","sequence":5,
              "payload":{"result_status":"result","resource_identity":"owner.md.bak",
              "consumed_resource":{"match":"exact","package_relative_path":"references/owner.md.bak"}}}
        self.assertEqual(omp.owner_reads([fake],"owner.md"),[])
        fake["payload"]["consumed_resource"]["package_relative_path"]="references/owner.md"
        self.assertEqual(omp.owner_reads([fake],"owner.md"),[5])

class HeartbeatKernelBoundary(unittest.TestCase):
    def test_p_r_u_x_two_directories_intervals_bound_and_bracket_ends(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            for name in ('a','b'):
                (root/name).mkdir(); (root/name/'f').write_text(name)
            w = pl.LedgerWatcher(root).start()
            self.assertTrue(w.established,w.error)
            (root/'a/f').read_bytes()
            time.sleep(.12)
            (root/'b/f').read_bytes()
            time.sleep(.12)
            (root/'a/f').read_bytes()
            ledger = w.stop()
            opens = [r for r in ledger['events'] if 'open' in r['flags'] and not r['dir']]
            self.assertGreaterEqual(len({r['interval'] for r in opens}),3)
            self.assertEqual([r['index'] for r in ledger['heartbeats']],list(range(len(ledger['heartbeats']))))
            brackets,reasons = pl.timing(ledger,[],ledger['parameters'])
            self.assertEqual(reasons,[])
            for r in opens:
                self.assertIn(r['interval'],brackets)
                self.assertFalse(brackets[r['interval']]['timing_loss'])
            small = pl.LedgerWatcher(root,{**pl.PARAMETERS,'row_bound':1}).start()
            (root/'a/f').read_bytes(); (root/'b/f').read_bytes()
            record=small.stop()
            self.assertTrue(record['rows_truncated'])
            self.assertLessEqual(len(record['events']),1)

class OwnerFloorProductionOwner(unittest.TestCase):
    def test_l_m_o_p_q_t_w_y_decisions_and_positive_exception(self):
        positive={'owner_floor_exact':False,'owner_read_observed':[{'sequence':3}], 'owner_minor_exposure':[], 'owner_open_windows':[]}
        self.assertEqual(core70.owner_floor_state(positive,5,r2_adjudicated=True),'FAIL')
        self.assertEqual(core70.owner_floor_state(positive,2,r2_adjudicated=True),'UNRESOLVED')
        self.assertEqual(core70.owner_floor_state(positive,5),'UNRESOLVED')
        for start,state in ((4,'UNRESOLVED'),(5,'UNRESOLVED'),(6,'PASS')):
            a={**positive,'owner_floor_exact':True,'owner_read_observed':[{'sequence':7}],
               'owner_open_windows':[{'window':{'start':start,'end':9}}]}
            self.assertEqual(core70.owner_floor_state(a,5,r2_adjudicated=True),state)
        a={**positive,'owner_floor_exact':True,'owner_read_observed':[],'owner_minor_exposure':[{'sequence':1}]}
        self.assertEqual(core70.owner_floor_state(a,5,r2_adjudicated=True),'UNRESOLVED')


class ReviewDiscriminators(PhaseAndDelivery):
    """Independent-review B-2: predicates that named acceptance cases depend on and no test could flip."""
    def account(self, opens, events, **kwargs):
        kwargs.setdefault("request_records", [{"t_ns": 1000, "monotonic_ns": 1000, "position": min((e["sequence"] for e in events), default=1), "pairing_verified": True}])
        return pl.account(overlap_ledger(opens), 1000, events, self.root, mount=MOUNT,
                          parameters=TEST_PARAMETERS, owner_name="owner.md", **kwargs)

    def test_unverified_pairing_never_explains_a_twin_from_whole_trace_content(self):
        good = {"t_ns": 1000, "monotonic_ns": 1000, "position": None, "pairing_verified": True}
        cases = [None, [], "malformed", [None], [good, None]]
        cases += [[{k: v for k, v in good.items() if k != "pairing_verified"}]]
        cases += [[{**good, "pairing_verified": v}] for v in (False, None, "true", 1)]
        cases += [[good, {**good, "pairing_verified": False}]]
        cases += [[{**good, "position": v}] for v in (True, "3", [])]
        for records in cases:
            with self.subTest(records=records):
                r = self.account([(2000, "x/references/owner.md")], [event(3, TWIN)], request_records=records)
                self.assertFalse(r["route_iii_available"])
                self.assertFalse(r["exact"], r)
                self.assertIsNone(r["active_ssdp_bytes"])
                self.assertEqual([u["file"] for u in r["unexplained"]], ["x/references/owner.md"])
                self.assertTrue(r["owner_read_observed"])
                self.assertEqual(core70.owner_floor_state(r, 5, r2_adjudicated=True), "FAIL")
        r = self.account([(2000, "x/references/owner.md")], [event(3, TWIN)], request_records=[good])
        self.assertTrue(r["exact"], r["reasons"])
        self.assertEqual(r["supplied"]["x/references/owner.md"]["routes"], ["whole-file-in-window"])

    def test_unverified_pairing_preserves_distinctive_and_path_linked_supply(self):
        for rel, text, command, route in (
                ("x/references/ref.md", REF, "cat nonliteral", "distinctive"),
                ("x/references/owner.md", TWIN, f"cat {MOUNT}/x/references/owner.md", "path-linked")):
            with self.subTest(route=route):
                r = self.account([(2000, rel)], [event(3, text, command=command)], request_records=[])
                self.assertFalse(r["route_iii_available"])
                self.assertTrue(r["exact"], r["reasons"])
                self.assertEqual(r["supplied"][rel]["routes"], [route])

    def test_s_whole_file_shown_outside_the_candidate_window_does_not_explain_the_open(self):
        requests = [{"t_ns": 1000, "pairing_verified": True, "monotonic_ns": 1000, "position": 1}, {"t_ns": 2500, "pairing_verified": True, "monotonic_ns": 2500, "position": 8}]
        outside = [event(i, "nothing") for i in range(1, 11)]
        outside[2] = event(3, TWIN)
        inside = [event(i, "nothing") for i in range(1, 11)]
        inside[8] = event(9, TWIN)
        r = self.account([(3000, "x/references/owner.md")], outside, request_records=requests)
        self.assertEqual(r["owner_open_windows"][0]["window"]["start"], 8)
        self.assertFalse(r["exact"], r["reasons"])
        r = self.account([(3000, "x/references/owner.md")], inside, request_records=requests)
        self.assertTrue(r["exact"], r["reasons"])

    def test_owner_line_floor_is_inclusive_at_exactly_the_floor(self):
        for width, positive in ((48, True), (47, False)):
            lines = [f"{i:02d}" + "a" * (width - 2) for i in range(6)]
            for rel in ("x/references/owner.md", "y/references/owner.md"):
                (self.root / rel).write_text("\n".join(lines) + "\n")
            r = pl.account(None, 1000, [event(3, "\n".join(lines))], self.root, owner_name="owner.md", parameters=TEST_PARAMETERS)
            self.assertEqual(bool(r["owner_read_observed"]), positive, width)
            self.assertEqual(r["owner_minor_exposure"], [])

    def test_native_owner_read_below_the_quantum_is_a_positive_and_scores_fail_before_r2(self):
        native = {"kind": "resource_access", "status": "result", "sequence": 3, "event_id": "e3",
                  "payload": {"result_status": "result", "consumed_resource": {"match": "partial", "package_relative_path": "x/references/owner.md"}}}
        r = pl.account(None, 1000, [native], self.root, owner_name="owner.md", parameters=TEST_PARAMETERS)
        self.assertEqual([v["sequence"] for v in r["owner_read_observed"]], [3])
        self.assertEqual(r["owner_read_observed"][0]["source"], "native-read")
        self.assertEqual(core70.owner_floor_state(r, 5, r2_adjudicated=True), "FAIL")

    def test_s_window_ends_before_the_first_event_of_the_next_request(self):
        requests = [{"t_ns": 1000, "pairing_verified": True, "monotonic_ns": 1000, "position": 1}, {"t_ns": 2500, "pairing_verified": True, "monotonic_ns": 2500, "position": 8}]
        for seq, exact in ((7, True), (8, False)):
            events = [event(i, "nothing") for i in range(1, 11)]
            events[seq - 1] = event(seq, TWIN)
            r = self.account([(1500, "x/references/owner.md")], events, request_records=requests)
            window = r["owner_open_windows"][0]["window"]
            self.assertEqual((window["start"], window["end"]), (1, 7))
            self.assertEqual(r["exact"], exact, (seq, r["reasons"]))

    def test_results_not_shown_to_the_model_are_never_owner_evidence(self):
        for seen in (False, None):
            r = pl.account(None, 1000, [event(3, TWIN, seen=seen)], self.root, owner_name="owner.md", parameters=TEST_PARAMETERS)
            self.assertEqual((r["owner_read_observed"], r["owner_minor_exposure"]), ([], []), seen)

    def test_owner_open_without_any_request_record_is_timing_loss_for_the_floor(self):
        r = self.account([(2000, "x/references/owner.md")], [event(4, "nothing")], request_records=[])
        self.assertFalse(r["owner_floor_exact"])
        self.assertTrue(any("request" in reason for reason in r["timing_reasons"] + r["reasons"]), (r["timing_reasons"], r["reasons"]))

    def test_k_ledger_and_adapter_agree_on_every_native_owner_read_target_form(self):
        from adapters import omp
        def native(**payload):
            return {"kind": "resource_access", "status": "result", "sequence": 5, "event_id": "e5",
                    "payload": {"result_status": "result", **payload}}
        forms = (
            {"consumed_resource": {"match": "exact", "package_relative_path": "x/references/owner.md"}},
            {"consumed_resource": {"match": "partial"}, "resolved_resource_path": "/opt/ssdp/skills/x/references/owner.md"},
            {"consumed_resource": {"match": "exact"}, "resource_identity": "x/references/owner.md:10-20"},
            {"consumed_resource": {"match": "partial", "package_relative_path": "x/references/owner.md:raw"}},
        )
        for payload in forms:
            event_ = native(**payload)
            ledger = pl.account(None, 1000, [event_], self.root, owner_name="owner.md", parameters=TEST_PARAMETERS)
            self.assertEqual([r["sequence"] for r in ledger["owner_read_observed"]], [5], payload)
            self.assertEqual(omp.owner_reads([event_], "owner.md"), [5], payload)
        for payload in ({"consumed_resource": {"match": "none", "package_relative_path": "x/references/owner.md"}},
                        {"consumed_resource": {"match": "exact", "package_relative_path": "x/references/owner.md.bak"}},
                        {"consumed_resource": {"match": "exact", "package_relative_path": "x/references/other.md"}}):
            event_ = native(**payload)
            ledger = pl.account(None, 1000, [event_], self.root, owner_name="owner.md", parameters=TEST_PARAMETERS)
            self.assertEqual(ledger["owner_read_observed"], [], payload)
            self.assertEqual(omp.owner_reads([event_], "owner.md"), [], payload)

    def test_owner_read_claim_family_needs_evidence_except_the_absence_claim(self):
        needs = "owner-read claim has no successful resource-access result evidence"
        for claim in ("owner-read", "t7-owner-read", "owner-read-mode", "Owner-Read-Hit"):
            self.assertIn(needs, core70.validate_claim_observability([], [claim]), claim)
        self.assertNotIn(needs, core70.validate_claim_observability([], ["owner-read-absence"]))

    def test_s_unpositioned_later_request_bounds_nothing_so_an_honest_text_final_turn_stays_explained(self):
        # A text-only final turn has no tool event, hence no position (None): it bounds nothing from above.
        requests = [{"t_ns": 1000, "pairing_verified": True, "monotonic_ns": 1000, "position": 2}, {"t_ns": 1500, "pairing_verified": True, "monotonic_ns": 1500, "position": None}]
        for shown, exact in ((3, True), (1, False)):                       # whole file shown after / before the window start
            events = [event(i, "nothing") for i in range(1, 6)]
            events[shown - 1] = event(shown, TWIN)
            r = self.account([(1200, "x/references/owner.md")], events, request_records=requests)
            window = r["owner_open_windows"][0]["window"]
            self.assertEqual((window["start"], window["end"]), (2, 5))
            self.assertEqual(r["exact"], exact, (shown, r["reasons"]))

    def test_s_unpositioned_or_absent_earlier_request_starts_at_the_trace_start_and_the_end_is_still_bounded(self):
        for earlier in ([], [{"t_ns": 1000, "pairing_verified": True, "monotonic_ns": 1000, "position": None}]):
            requests = earlier + [{"t_ns": 2500, "pairing_verified": True, "monotonic_ns": 2500, "position": 8}]
            for seq, exact in ((5, True), (9, False)):
                events = [event(i, "nothing") for i in range(1, 11)]
                events[seq - 1] = event(seq, TWIN)
                r = self.account([(1500, "x/references/owner.md")], events, request_records=requests)
                window = r["owner_open_windows"][0]["window"]
                self.assertEqual((window["start"], window["end"]), (1, 7), earlier)
                self.assertEqual(r["exact"], exact, (seq, earlier))

    def test_s_inconsistent_positions_make_an_empty_window_the_whole_trace(self):
        requests = [{"t_ns": 1000, "pairing_verified": True, "monotonic_ns": 1000, "position": 8}, {"t_ns": 1500, "pairing_verified": True, "monotonic_ns": 1500, "position": 3}]
        events = [event(i, "nothing") for i in range(1, 11)]
        r = self.account([(1200, "x/references/owner.md")], events, request_records=requests)
        window = r["owner_open_windows"][0]["window"]
        self.assertEqual((window["start"], window["end"]), (1, 10))

class RealWatcherOverflow(unittest.TestCase):
    @unittest.skipUnless(bwrap_usable(), "bwrap unusable")
    def test_u_subject_volume_overflow_is_recorded_by_the_real_watcher_and_makes_account_inexact(self):
        import threading
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "skills"
            make_tree(root)
            watch = pl.LedgerWatcher(root).start()
            self.assertTrue(watch.established, watch.error)
            gate, original = threading.Event(), watch._drain_once
            watch._drain_once = lambda: (gate.wait(), original())[1]
            for _ in range(7000):               # alternating files defeat kernel event coalescing
                (root / "a" / "references" / "owner.md").read_bytes()
                (root / "a" / "references" / "other.md").read_bytes()
            gate.set()
            record = watch.stop()
            self.assertTrue(record["overflow"])
            result = pl.account(record, None, [], root)
            self.assertFalse(result["exact"])
            self.assertTrue(any("overflow" in reason for reason in result["reasons"]), result["reasons"])


class TimingBracketEdgesAreConservative(unittest.TestCase):
    """Independent-review B-2 (M5, M13, M26, M27): the synthetic helper sets before == after for every heartbeat,
    which hides the edge definitions. Distinct pre/post-write stamps make each one observable."""
    PARAMS = {**pl.PARAMETERS, "clock_tolerance_ns": 7, "bracket_width_bound_ns": 10**9, "heartbeat_gap_bound_ns": 10**9}

    @staticmethod
    def beat(i, before, width=10, drift=0):
        return {"index": i, "before_ns": before + drift, "after_ns": before + width + drift,
                "before_mono_ns": before, "after_mono_ns": before + width}

    def test_p_x_lower_edge_precedes_the_earlier_write_and_upper_edge_follows_the_later_write_with_tolerance(self):
        ledger = {"heartbeats": [self.beat(0, 1000), self.beat(1, 2000)]}
        brackets, reasons = pl.timing(ledger, [], self.PARAMS)
        self.assertEqual(reasons, [])
        self.assertEqual((brackets[0]["lower_ns"], brackets[0]["upper_ns"]), (1000 - 7, 2010 + 7))

    def test_p_divergence_taints_every_later_bracket_not_only_the_adjacent_one(self):
        ledger = {"heartbeats": [self.beat(0, 1000), self.beat(1, 2000, drift=500), self.beat(2, 3000), self.beat(3, 4000)]}
        brackets, reasons = pl.timing(ledger, [], self.PARAMS)
        self.assertTrue(any("clock divergence" in r for r in reasons))
        self.assertEqual([brackets[i]["timing_loss"] for i in sorted(brackets)], [True, True, True])
        clean, none = pl.timing({"heartbeats": [self.beat(i, 1000 * (i + 1)) for i in range(4)]}, [], self.PARAMS)
        self.assertEqual(none, [])
        self.assertFalse(any(b["timing_loss"] for b in clean.values()))

    def test_x_decreasing_request_stamps_are_timing_loss_even_when_consistent_with_the_baseline(self):
        ledger = {"heartbeats": [self.beat(0, 1000), self.beat(1, 2000)]}
        ordered = [{"t_ns": 1500, "pairing_verified": True, "monotonic_ns": 1500}, {"t_ns": 1800, "pairing_verified": True, "monotonic_ns": 1800}]
        self.assertEqual(pl.timing(ledger, ordered, self.PARAMS)[1], [])
        for decreasing in ([{"t_ns": 1800, "pairing_verified": True, "monotonic_ns": 1800}, {"t_ns": 1500, "pairing_verified": True, "monotonic_ns": 1500}],
                           [{"t_ns": 1500, "pairing_verified": True, "monotonic_ns": 1800}, {"t_ns": 1800, "pairing_verified": True, "monotonic_ns": 1500}][::-1]):
            brackets, reasons = pl.timing(ledger, decreasing, self.PARAMS)
            self.assertIn("request stamps decrease or disagree with heartbeat baseline", reasons)
            self.assertTrue(all(b["timing_loss"] for b in brackets.values()))
