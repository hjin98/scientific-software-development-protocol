"""Arms specification and replicate command sets (arms_spec.py): the 72b defaults reproduce byte-identically, the 7.2.1 mapping runs through plan,
check-plan, verify, pair_order and the evaluator driver, and a second main-panel replicate is a second identical command set keyed by command.

Offline only: no provider, no credential, no custody store. Some tests read the retained 72b campaign directory read-only (skipped without it).
Run: python3 -m pytest -q -p no:anyio qualification/ssdp70/qual-v2
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock

import yaml

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
EVAL = REPO / "qualification" / "ssdp70" / "eval"
sys.path[:0] = [str(HERE), str(EVAL)]
import arms_spec  # noqa: E402
import campaign_assess as ca  # noqa: E402
import test_build_campaign_record as tb  # noqa: E402  (module attribute access only: its TestCase classes must not be collected here)

CAMPAIGN = Path.home() / "ssdp70-omp-stagef/qualification/campaign-72-20261008"
S4 = Path.home() / "ssdp70-omp-stagef/qualification/s4-20261007"
BASELINE = "24518df"                                  # the tooling before the arms specification
SPEC721 = {"schema": 1,
           "arms": [{"name": "p721", "ref": "a" * 40, "version": "7.2.1", "label": "cand", "assessed": True},
                    {"name": "p72aa", "ref": arms_spec.CANDIDATE_REF, "version": "7.2.0", "label": "b1", "assessed": True},
                    {"name": "p65", "ref": arms_spec.OLD_REF, "version": "6.5.0", "label": "b65"}],
           "panels": {"main": {"arms": ["p721", "p72aa"], "replicates": 2}, "routing": {"arms": ["p721", "p72aa"]},
                      "versioning": {"arms": ["p721", "p72aa"]}, "burden": {"arms": ["p721", "p72aa", "p65"]},
                      "sentinels": {"arms": ["p721", "p72aa"]}, "unversioned": {"arms": ["p721", "p72aa"]}}}


def run(*args, **kw):
    return subprocess.run([sys.executable, *map(str, args)], capture_output=True, text=True, **kw)


def baseline_file(rel: str) -> str | None:
    p = subprocess.run(["git", "-C", str(REPO), "show", f"{BASELINE}:qualification/ssdp70/qual-v2/{rel}"], capture_output=True, text=True)
    return p.stdout if p.returncode == 0 else None


class SpecUnits(unittest.TestCase):
    def test_defaults_are_the_72b_campaign(self):
        spec = arms_spec.load(None)
        self.assertEqual(arms_spec.name_of(spec), {"cand": "p72", "b1": "p66", "b2": "p66b", "b65": "p65"})
        self.assertEqual(arms_spec.assessed(spec), ("p72", "p66", "p66b"))
        self.assertEqual(arms_spec.panel_arms(spec, "main"), ["p72", "p66", "p66b"])
        self.assertEqual(arms_spec.panel_arms(spec, "burden-add"), ["p72", "p65"])
        self.assertEqual([arms_spec.panel_sets(spec, p) for p in spec["panels"]], [1] * len(spec["panels"]))
        with tempfile.TemporaryDirectory() as t:
            self.assertEqual(arms_spec.load(Path(t)), spec)               # no file in the work directory: the defaults

    def test_malformed_specifications_are_refused(self):
        def bad(change):
            spec = json.loads(json.dumps(SPEC721))
            change(spec)
            with self.assertRaises(arms_spec.SpecError):
                arms_spec.validate(spec)
        bad(lambda s: s["arms"][1].update(label="cand"))                    # two cand arms
        bad(lambda s: s["arms"][1].update(label="b9"))                      # not an h4 label
        bad(lambda s: s["arms"][1].update(name="p721"))                     # duplicate name
        bad(lambda s: s["arms"].pop(0))                                     # no cand
        bad(lambda s: s["panels"]["main"].update(arms=["p721", "p66"]))    # an arm outside the specification
        bad(lambda s: s["panels"]["main"].update(replicates=0))
        bad(lambda s: s["panels"]["main"].update(replicates=True))
        bad(lambda s: s["panels"].update({"main-add": {"arms": ["p721"]}}))
        bad(lambda s: s.update(schema=2))
        self.assertEqual(arms_spec.validate(SPEC721)["panels"]["routing"]["replicates"], 1)

    def test_run_ids_are_bare_in_set_zero_and_command_qualified_after(self):
        self.assertEqual(arms_spec.run_id("EP-001-p721-r0", "main-c01", 0), "EP-001-p721-r0")
        self.assertEqual(arms_spec.run_id("EP-001-p721-r0", "main-c09", 1), "main-c09/EP-001-p721-r0")
        self.assertEqual(arms_spec.run_id("EP-001-p721-r0", None, 1), "EP-001-p721-r0")


@unittest.skipUnless((CAMPAIGN / "declaration.effective.json").exists() and baseline_file("build_campaign_record.py"),
                     "72b campaign directory or the baseline tooling commit not on this host")
class CampaignRecordReproduces(unittest.TestCase):
    """Without an arms specification the builder produces the 72b campaign record, audit and console output byte for byte."""

    GATE_MAP = {"q2_owed": ["delegate_request"], "q2_unowed": {"id_prefixes": ["delegate_request.unowed"]},
                "q3": {"tension_report": "tension", "detection.unnamed": "finding"}, "q4b": ["claim_integrity"],
                "q4c": ["unauthorized_mutation"], "q4d": {"measures": ["null_coverage"]}}

    def build(self, tool: Path, out: Path):
        out.mkdir()
        (out / "map.json").write_text(json.dumps(self.GATE_MAP))
        arms = json.loads((CAMPAIGN / "arms" / "arms.json").read_text())["arms"]
        cmd = [tool, "--declaration", CAMPAIGN / "declaration.effective.json", "--map", out / "map.json", "--allow-unresolved",
               "--audit", out / "audit.json", "--out", out / "rec.json"]
        for r in sorted((CAMPAIGN / "runs").glob("*")):
            cmd += ["--runs", r]
        for x in arms:
            cmd += ["--subject-commit", f"{x['name']}={x['commit']}"]
        p = run(*cmd)
        return p.returncode, p.stdout, (out / "audit.json").read_bytes(), (out / "rec.json").read_bytes()

    def test_builder_output_is_byte_identical_to_the_baseline(self):
        with tempfile.TemporaryDirectory() as t:
            t = Path(t)
            (t / "old").mkdir()
            (t / "old" / "build_campaign_record.py").write_text(baseline_file("build_campaign_record.py"))
            for dep in ("h4.py", "operating_characteristics.py"):
                (t / "old" / dep).symlink_to(HERE / dep)
            old = self.build(t / "old" / "build_campaign_record.py", t / "out-old")
            new = self.build(HERE / "build_campaign_record.py", t / "out-new")
            self.assertEqual(old[0], new[0])
            self.assertEqual(json.loads(old[1])["declared"], 640)         # the whole 72b slot declaration, 640 built runs
            self.assertEqual(old[1:], new[1:])

    @unittest.skipUnless((CAMPAIGN / "evaluations" / "mimo-1-rerun-1").is_dir() and baseline_file("campaign_assess.py"), "72b evaluations not on this host")
    def test_collected_dispositions_and_the_record_built_from_them_are_byte_identical(self):
        with tempfile.TemporaryDirectory() as t:
            t = Path(t)
            mirror = t / "mirror" / "qualification" / "ssdp70"                # the baseline driver in a mirror layout, so its EVAL resolves
            (mirror / "qual-v2").mkdir(parents=True)
            (mirror / "qual-v2" / "campaign_assess.py").write_text(baseline_file("campaign_assess.py"))
            (mirror / "eval").symlink_to(EVAL)
            outs = {}
            for tag, tool in (("old", mirror / "qual-v2" / "campaign_assess.py"), ("new", HERE / "campaign_assess.py")):
                p = run(tool, "collect", CAMPAIGN, "--out", t / f"{tag}.json", "--assessment-root", CAMPAIGN / "evaluations/mimo-1",
                        "--rerun-root", CAMPAIGN / "evaluations/mimo-1-rerun-1")
                outs[tag] = (p.returncode, p.stdout, (t / f"{tag}.json").read_bytes())
            self.assertEqual(outs["old"], outs["new"])
            self.assertGreater(len(json.loads(outs["new"][2])), 1000)
            (t / "old").mkdir()
            (t / "old" / "build_campaign_record.py").write_text(baseline_file("build_campaign_record.py"))
            for dep in ("h4.py", "operating_characteristics.py"):
                (t / "old" / dep).symlink_to(HERE / dep)
            records = []
            for tool in (t / "old" / "build_campaign_record.py", HERE / "build_campaign_record.py"):
                out = t / ("out-" + tool.parent.name)
                out.mkdir()
                (out / "map.json").write_text(json.dumps(self.GATE_MAP))
                cmd = [tool, "--declaration", CAMPAIGN / "declaration.effective.json", "--map", out / "map.json", "--allow-unresolved",
                       "--dispositions", t / "new.json", "--audit", out / "audit.json", "--out", out / "rec.json"]
                for r in sorted((CAMPAIGN / "runs").glob("*")):
                    cmd += ["--runs", r]
                for x in json.loads((CAMPAIGN / "arms" / "arms.json").read_text())["arms"]:
                    cmd += ["--subject-commit", f"{x['name']}={x['commit']}"]
                p = run(*cmd)
                records.append((p.returncode, p.stdout, (out / "rec.json").read_bytes()))
            self.assertEqual(records[0], records[1])


@unittest.skipUnless((CAMPAIGN / "campaign-identity.json").exists() and (S4 / "routes").exists(), "campaign directory not on this host")
class Fixture(unittest.TestCase):
    """A work directory with the 72b executor key, a synthetic arms manifest and the retained S4 route corpus (3 main, burden, one add-on)."""

    def setUp(self):
        self.t = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.t, True)
        self.work = self.t / "work"
        self.work.mkdir()
        shutil.copytree(CAMPAIGN / "keys", self.work / "keys")
        manifest = yaml.safe_load((S4 / "routes/corpus/manifest.yaml").read_text())
        for e in manifest["episodes"]:
            e["panel"] = {"T1-r01": "main", "T1-r02": "main", "T1-r03": "main", "T7-r05": "burden-add", "T8-r01": "sentinels"}.get(e["id"], "burden")
        self.episodes = [e["id"] for e in manifest["episodes"]]
        self.corpus = self.t / "corpus"
        shutil.copytree(S4 / "routes/corpus", self.corpus)
        (self.corpus / "manifest.yaml").write_text(yaml.safe_dump(manifest))
        self.flags = self.t / "flags.json"
        self.flags.write_text(json.dumps({"T1-r01": {"delegate": True, "non_owed": False, "scored": True},
                                          "T1-r02": {"delegate": False, "non_owed": True, "scored": True},
                                          "T1-r03": {"delegate": False, "non_owed": True, "scored": True}}))
        self.args = ["--work", self.work, "--corpus", self.corpus, "--requirements", S4 / "routes/requirements",
                     "--oracles", S4 / "routes/oracles", "--slot-flags", self.flags]

    def arms_721(self):
        """arms.json for the 7.2.1 mapping, rows renamed from the 72b manifest (valid package digests, distinct candidate commit)."""
        rows = {r["name"]: r for r in json.loads((CAMPAIGN / "arms" / "arms.json").read_text())["arms"]}
        out = []
        for name, src, commit in (("p721", "p72", "a" * 40), ("p72aa", "p72", arms_spec.CANDIDATE_REF), ("p65", "p65", arms_spec.OLD_REF)):
            out.append(dict(rows[src], name=name, commit=commit, requested_ref=commit))
        (self.work / "arms").mkdir()
        (self.work / "arms" / "arms.json").write_text(json.dumps({"schema": 1, "repo": str(REPO), "arms": out}))
        (self.work / arms_spec.SPEC_NAME).write_text(json.dumps(SPEC721))

    def plan(self):
        p = run(HERE / "prepare_campaign.py", "plan", *self.args)
        self.assertEqual(p.returncode, 0, p.stderr)
        return json.loads((self.work / "commands.json").read_text())["commands"], json.loads((self.work / "declaration.json").read_text())


class PlanReproduces(Fixture):
    def test_default_plan_is_byte_identical_to_the_baseline_and_to_the_explicit_72b_specification(self):
        text = baseline_file("prepare_campaign.py")
        if text is None:
            self.skipTest("baseline tooling commit not available")
        (self.work / "arms").symlink_to(CAMPAIGN / "arms")
        old_root = self.t / "old"                                    # the baseline script in a mirror layout, so its REPO and EVAL resolve
        (old_root / "qualification/ssdp70/qual-v2").mkdir(parents=True)
        (old_root / "qualification/ssdp70/qual-v2/prepare_campaign.py").write_text(text)
        for d in ("eval", "s4"):
            (old_root / "qualification/ssdp70" / d).symlink_to(REPO / "qualification/ssdp70" / d)
        old_work = self.t / "old-work"
        shutil.copytree(self.work, old_work, symlinks=True)
        args_old = [old_work if x == self.work else x for x in self.args]
        p = run(old_root / "qualification/ssdp70/qual-v2/prepare_campaign.py", "plan", *args_old)
        self.assertEqual(p.returncode, 0, p.stderr)
        p = run(HERE / "prepare_campaign.py", "plan", *self.args)
        self.assertEqual(p.returncode, 0, p.stderr)
        explicit = self.t / "explicit-work"
        shutil.copytree(self.work, explicit, symlinks=True)
        for f in ("commands.json", "declaration.json", "expected-runs.json"):
            (explicit / f).unlink()
        (explicit / arms_spec.SPEC_NAME).write_text(json.dumps(arms_spec.DEFAULT_SPEC))
        p = run(HERE / "prepare_campaign.py", "plan", *[explicit if x == self.work else x for x in self.args])
        self.assertEqual(p.returncode, 0, p.stderr)
        for f in ("commands.json", "declaration.json", "expected-runs.json"):
            mine = (self.work / f).read_text()
            theirs = (old_work / f).read_text().replace(str(old_work), str(self.work)).replace(str(old_root), str(REPO))
            self.assertEqual(mine, theirs, f)
            self.assertEqual(mine, (explicit / f).read_text().replace(str(explicit), str(self.work)), f)
        p = run(HERE / "prepare_campaign.py", "check-plan", "--work", self.work)
        self.assertEqual(p.returncode, 0, p.stdout)


class Mapping721(Fixture):
    """p721 -> cand, p72aa -> b1, p65 -> b65, with a second main-panel replicate as a second identical command set."""

    def setUp(self):
        super().setUp()
        self.arms_721()

    def test_plan_declares_the_label_mapping_and_a_second_identical_main_command_set(self):
        plan, decl = self.plan()
        self.assertEqual(decl["arms"], {"cand": "p721", "b1": "p72aa", "b65": "p65"})
        by_key = {c["key"]: c for c in plan}
        main = [c for c in plan if c["panel"] == "main"]
        self.assertEqual([(c["key"], c.get("set")) for c in main], [("main-c01", 0), ("main-c02", 1)])
        self.assertEqual(by_key["main-c02"]["replicate_of"], "main-c01")
        self.assertEqual(by_key["main-c01"]["arms"], ["p721", "p72aa"])
        strip = lambda c: [v for i, v in enumerate(c["argv"]) if i == 0 or c["argv"][i - 1] != "--out"]  # noqa: E731
        self.assertEqual(strip(by_key["main-c01"]), strip(by_key["main-c02"]))
        self.assertNotEqual(by_key["main-c01"]["argv"], by_key["main-c02"]["argv"])      # only the output directory differs
        self.assertEqual([c["arms"] for c in plan if c["panel"] == "burden"], [["p721", "p72aa", "p65"]] * 2)
        self.assertEqual([c["arms"] for c in plan if c["panel"] == "sentinels"], [["p721", "p72aa"]])
        slots = [x for x in decl["slots"] if x["panel"] == "main" and x["episode"] == "T1-r01"]
        self.assertEqual(sorted((x["arm"], x["replicate"], x.get("run_replicate"), x["command"]) for x in slots),
                         [("b1", 0, None, "main-c01"), ("b1", 1, 0, "main-c02"), ("cand", 0, None, "main-c01"), ("cand", 1, 0, "main-c02")])
        self.assertEqual(sum(c["runs"] for c in main), 12)                                # 3 episodes x 2 arms x 2 sets
        p = run(HERE / "prepare_campaign.py", "check-plan", "--work", self.work)
        self.assertEqual(p.returncode, 0, p.stdout)

    def test_check_plan_refuses_a_replicate_set_that_is_not_identical_or_not_in_the_specification(self):
        self.plan()
        path = self.work / "commands.json"
        good = path.read_text()
        data = json.loads(good)
        next(c for c in data["commands"] if c["key"] == "main-c02")["argv"].append("--only")
        next(c for c in data["commands"] if c["key"] == "main-c02")["argv"].append("T1-r03")
        path.write_text(json.dumps(data))
        p = run(HERE / "prepare_campaign.py", "check-plan", "--work", self.work)
        self.assertEqual(p.returncode, 2)
        self.assertIn("not an identical repeat", p.stdout)
        data = json.loads(good)
        data["commands"] = [c for c in data["commands"] if c["key"] != "main-c02"]
        path.write_text(json.dumps(data))
        p = run(HERE / "prepare_campaign.py", "check-plan", "--work", self.work)
        self.assertIn("replicate sets [0] differ from the specification", p.stdout)
        smaller = json.loads(json.dumps(SPEC721))
        smaller["arms"].pop()                                                                             # p65 dropped from the specification
        smaller["panels"]["burden"]["arms"] = ["p721", "p72aa"]
        (self.work / arms_spec.SPEC_NAME).write_text(json.dumps(smaller))
        path.write_text(good)
        p = run(HERE / "prepare_campaign.py", "check-plan", "--work", self.work)
        self.assertEqual(p.returncode, 2)
        self.assertIn("not in the arms specification", p.stdout)

    def test_check_plan_refuses_an_omitted_panel_arm_even_with_matching_slots(self):
        self.plan()
        path = self.work / "commands.json"
        plan = json.loads(path.read_text())
        for command in plan["commands"]:
            if command["panel"] == "burden":
                command["arms"].remove("p72aa")
                argv = command["argv"]
                i = next(i for i, value in enumerate(argv) if value == "--arm" and argv[i + 1] == "p72aa")
                del argv[i:i + 2]
                command["runs"] = command["runs"] // 3 * 2
        path.write_text(json.dumps(plan))
        path = self.work / "declaration.json"
        decl = json.loads(path.read_text())
        decl["slots"] = [s for s in decl["slots"] if not (s["panel"] == "burden" and s["arm"] == "b1")]
        path.write_text(json.dumps(decl))
        p = run(HERE / "prepare_campaign.py", "check-plan", "--work", self.work)
        self.assertEqual(p.returncode, 2)
        self.assertIn("panel arms differ", p.stdout)
        import campaign_run
        self.assertIn("panel arms differ", campaign_run.spec_problem(self.work))

    def test_check_corpus_counts_runs_per_arm_across_replicate_sets(self):
        p = run(HERE / "prepare_campaign.py", "check-corpus", *self.args)
        self.assertEqual(p.returncode, 0, p.stdout)
        self.assertEqual(json.loads(p.stdout)["summary"]["by_panel(episodes,runs_per_arm)"]["main"], [3, 6])

    def test_runner_status_shows_the_set_and_refuses_arms_outside_the_specification(self):
        self.plan()
        p = run(HERE / "campaign_run.py", self.work, "status")
        self.assertIn("main-c02", p.stdout)
        self.assertIn("set 1", p.stdout)
        data = json.loads((self.work / "commands.json").read_text())
        data["commands"][0]["arms"] = ["p72"]
        (self.work / "commands.json").write_text(json.dumps(data))
        env = {"PATH": "/usr/bin:/bin", "SSDP70_OMP_PROVIDER_CREDENTIAL": "x"}
        p = subprocess.run([sys.executable, HERE / "campaign_run.py", str(self.work), "start", "1"], capture_output=True, text=True, env=env)
        self.assertEqual(p.returncode, 2)
        self.assertIn("outside the arms specification", p.stderr)

    def test_the_identity_binds_the_specification_and_refresh_refuses_a_changed_one(self):
        import prepare_campaign
        sha = prepare_campaign.sha
        ident = {"candidate_ref": "HEAD", "arms": {r["name"]: {"dist_tree_sha256": r["dist_tree_sha256"]}
                                                   for r in json.loads((self.work / "arms" / "arms.json").read_text())["arms"]},
                 "executor_profile_sha256": sha(self.work / "keys" / "omp-primary-flash-executor-main.json"),
                 "arms_spec_sha256": sha(self.work / arms_spec.SPEC_NAME)}
        for k in ("repo_head", "harness_sha256", "assess_sha256", "builder_sha256", "h4_sha256", "prepare_campaign_sha256"):
            ident[k] = "old"
        (self.work / "campaign-identity.json").write_text(json.dumps(ident))
        with contextlib.redirect_stdout(io.StringIO()):
            prepare_campaign.cmd_refresh_identity(types.SimpleNamespace(work=self.work))
        refreshed = json.loads((self.work / "campaign-identity.json").read_text())
        self.assertEqual(refreshed["arms_spec_module_sha256"], sha(HERE / "arms_spec.py"))
        self.assertEqual(refreshed["arms_spec_sha256"], sha(self.work / arms_spec.SPEC_NAME))
        (self.work / arms_spec.SPEC_NAME).write_text(json.dumps(dict(SPEC721, arms=[dict(SPEC721["arms"][0], version="7.2.2"), *SPEC721["arms"][1:]])))
        with self.assertRaisesRegex(SystemExit, "arms specification differs"):
            prepare_campaign.cmd_refresh_identity(types.SimpleNamespace(work=self.work))

    # -- the offline dry run: synthetic run directories for every declared slot ------------------------------------------------------

    def fill_runs(self, decl, plan, skip=()):
        import prepare_campaign
        key = prepare_campaign.executor(self.work).profile_key_sha256
        arms = {r["name"]: r for r in json.loads((self.work / "arms" / "arms.json").read_text())["arms"]}
        by_key = {c["key"]: c for c in plan}
        delegate_items = {k: v for k, v in tb.Synthetic().all_items().items()}
        plain_items = {k: v for k, v in delegate_items.items() if k != "REQ.1"}
        made = []
        for x in decl["slots"]:
            c = by_key[x["command"]]
            arm = decl["arms"][x["arm"]]
            name = f"{x['episode']}-{arm}-r{x.get('run_replicate', x['replicate'])}"
            if (x["command"], name) in skip:
                continue
            index = self.episodes.index(x["episode"])
            order = list(c["arms"]) if (index + x.get("run_replicate", 0)) % 2 == 0 else list(reversed(c["arms"]))
            items = (delegate_items if x.get("delegate") else plain_items) if x["panel"] == "main" else {}
            tb.fake_run(self.work / "runs" / x["command"], name, items=items, pair=order, profile_key_sha256=key,
                        subject_commit=arms[arm]["commit"])
            made.append((x["command"], name))
        return made

    def verify(self, *extra):
        (self.work / "gate-map.json").write_text(json.dumps(tb.MAP))
        return run(HERE / "prepare_campaign.py", "verify", "--work", self.work, "--map", self.work / "gate-map.json", *extra)

    def audit(self):
        return json.loads((self.work / "campaign-verify.json").read_text())

    def test_dry_run_plan_check_plan_verify_and_pair_order_accept_the_second_replicate(self):
        plan, decl = self.plan()
        made = self.fill_runs(decl, plan)
        self.assertEqual(len(made), len(decl["slots"]))
        main_names = [n for c, n in made if c.startswith("main-c")]
        self.assertEqual(len(main_names), 12)
        self.assertEqual(len(set(main_names)), 6)                    # six run names for twelve runs: the second replicate repeats them
        p = self.verify()
        self.assertIn(p.returncode, (0, 4), p.stdout + p.stderr)
        audit = self.audit()
        self.assertEqual(audit["findings"], [], audit["findings"])
        self.assertEqual((audit["declared"], audit["built"]), (len(decl["slots"]), len(decl["slots"])))
        self.assertEqual(audit["by_arm"]["cand"], {"admissible": 3 * 2 + len([1 for x in decl["slots"] if x["panel"] != "main" and x["arm"] == "cand"])})
        pair = audit["pair_order"]
        self.assertTrue(pair["checked"])
        self.assertEqual(sorted(pair["by_set"]), ["0", "1"])         # alternation is audited inside each replicate set
        for counts in pair["by_set"].values():
            self.assertLessEqual(abs(counts["p721"] - counts["p72aa"]), 1)
        self.assertEqual(sum(pair["first_arm"].values()), sum(sum(v.values()) for v in pair["by_set"].values()))

    def test_h4_live_q5c_and_the_t7_add_on_rule_run_unchanged_on_the_721_mapping(self):
        import h4
        plan, decl = self.plan()
        self.fill_runs(decl, plan)
        self.assertEqual(self.verify().returncode, 0)
        cmd = [HERE / "build_campaign_record.py", "--declaration", self.work / "declaration.effective.json", "--map", self.work / "gate-map.json",
               "--allow-unresolved", "--out", self.work / "record.json"]
        for r in sorted((self.work / "runs").glob("*")):
            cmd += ["--runs", r]
        for x in json.loads((self.work / "arms" / "arms.json").read_text())["arms"]:
            cmd += ["--subject-commit", f"{x['name']}={x['commit']}"]
        self.assertEqual(run(*cmd).returncode, 0)
        rec = json.loads((self.work / "record.json").read_text())
        self.assertEqual({r["arm"] for r in rec["runs"]}, {"cand", "b1", "b65"})
        result = h4.q5c(h4.Campaign(rec))
        self.assertEqual(result["status"], h4.PASS, result)
        self.assertEqual(sorted(result["routes"]), ["T1", "T7", "T8"])
        self.assertTrue(all(len([o for o in h4.Campaign(rec).obs(a, "Q5c") if o["route"] == "T7"]) >= 3 for a in ("cand", "b65")))
        # the pre-registered rule: a T7 candidate set that mixes read modes is pending until seven pairs exist
        for run_dir in sorted((self.work / "runs").glob("burden-c*/T7-*-p721-r0"))[:2]:
            s = json.loads((run_dir / "summary.json").read_text())
            s["ssdp_read_mode"] = "owner"
            (run_dir / "summary.json").write_text(json.dumps(s))
        self.assertEqual(run(*cmd).returncode, 0)
        pending = h4.q5c(h4.Campaign(json.loads((self.work / "record.json").read_text())))
        self.assertEqual((pending["status"], pending["routes"]["T7"]["status"]), (h4.PENDING, h4.PENDING), pending)

    def test_dry_run_missing_misplaced_and_extra_replicate_runs_are_integrity_findings(self):
        plan, decl = self.plan()
        self.fill_runs(decl, plan, skip={("main-c02", "T1-r02-p721-r0")})
        p = self.verify()
        self.assertEqual(p.returncode, 3, p.stdout)
        findings = self.audit()["findings"]
        self.assertIn({"kind": "INTEGRITY", "what": "declared slot has no original run", "run": "main-c02/T1-r02-p721-r0"}, findings)
        # the same run directory under a command that does not declare it is a stray run, and the slot stays unfilled
        shutil.copytree(self.work / "runs" / "main-c01" / "T1-r02-p721-r0", self.work / "runs" / "main-c09" / "T1-r02-p721-r0")
        p = self.verify()
        self.assertEqual(p.returncode, 3)
        findings = self.audit()["findings"]
        self.assertIn({"kind": "INTEGRITY", "what": "undeclared run", "run": "T1-r02-p721-r0", "command": ["main-c09"]}, findings)
        self.assertIn("declared slot has no original run", {f["what"] for f in findings})

    def test_dry_run_pooled_alternation_across_sets_is_not_a_finding(self):
        plan, decl = self.plan()
        self.fill_runs(decl, plan)
        self.assertEqual(self.verify().returncode, 0)
        pair = self.audit()["pair_order"]
        pooled = abs(pair["first_arm"]["p721"] - pair["first_arm"]["p72aa"])
        self.assertLessEqual(pooled, 2 * max(abs(c["p721"] - c["p72aa"]) for c in pair["by_set"].values()))


# -- the real harness and the real assessor on two runs that share one run identity -----------------------------------------------------

class HarnessSharedIdentity(unittest.TestCase):
    """Two distinct runs of one episode and arm (command main-c01 and main-c02, both replicate 0) share one run identity. The real harness writes them,
    the real assess70 assesses them in separate assessment passes, campaign_assess collects them keyed by (command, run) and the builder consumes them."""

    ARMS = ("p721", "p72aa")

    def setUp(self):
        import harness70
        import test_harness_integration as thi
        self.harness70, self.thi = harness70, thi
        self.h = thi.HarnessIntegration("test_probe_run_produces_complete_admissible_integrity_bound_evidence")
        self.h.setUp()
        self.addCleanup(self.h.tearDown)
        self.work = self.h.root / "work"
        (self.work / "authorizations").mkdir(parents=True)
        (self.work / "authorizations" / "evaluator-full.ok").write_text("ok")
        (self.work / arms_spec.SPEC_NAME).write_text(json.dumps(dict(SPEC721, panels={"main": {"arms": list(self.ARMS), "replicates": 2}})))
        commands = []
        for k, key in enumerate(("main-c01", "main-c02")):
            commands.append({"key": key, "panel": "main", "arms": list(self.ARMS), "runs": 2, "conditional": False, "episodes": 1, "set": k,
                             **({"replicate_of": "main-c01"} if k else {})})
        (self.work / "commands.json").write_text(json.dumps({"commands": commands}))
        self.identities = {}
        for key in ("main-c01", "main-c02"):
            for arm in self.ARMS:
                self.run_one(key, arm)

    def run_one(self, key, arm):
        h = self.h
        row = dict(h.arm, name=arm, requested_ref=arm, commit=arm)
        kw = dict(corpus=h.corpus, episode=h.episode, arm=row, arms_manifest_sha256="arms", dist=h.dist, profile_bundle=h.bundle,
                  profile_path=h.profile_path, capability_path=h.cap_path, requirements=h.requirements, requirements_root=h.req_root,
                  adapter_module=self.thi.FakeAdapter, oracles=h.oracles.parent, mode="probe")
        identity = self.harness70.run_identity(**kw, rep=0, pair_order=list(self.ARMS))
        out = self.work / "runs" / key / f"E1-{arm}-r0"
        out.parent.mkdir(parents=True, exist_ok=True)
        summary = self.harness70.run_episode(**kw, out=out, identity=identity, pair_order=list(self.ARMS))
        self.assertEqual(summary["evidence_state"], "COMPLETE_ADMISSIBLE")
        self.identities[(key, arm)] = identity["identity_sha256"]

    def assess_args(self, root):
        profile, caps = self.h.evaluator_material("1")
        (self.h.root / "keys-root" / "E1").mkdir(parents=True, exist_ok=True)
        return argparse.Namespace(work=self.work, panels=["main"], assessment_root=root, format_rerun_of=None, limit=None, parallel=1,
                                  evaluator_profile=profile, evaluator_capabilities=caps, keys_root=self.h.root / "keys-root", shared_rubric=None,
                                  rerun_root=None, out=self.h.root / "dispositions.json", evidence_out=self.h.root / "evidence.json")

    def fake_assess_process(self, cmd, capture_output=True, text=True):
        import assess70
        argv = cmd[2:]
        with mock.patch.object(assess70, "load_adapter", return_value=self.thi.FakeEvaluator), contextlib.redirect_stdout(io.StringIO()):
            code = assess70.main([*argv, "--adapter", "fake"])
        return types.SimpleNamespace(returncode=code, stderr="", stdout="")

    def authorize(self, root, profile):
        root.mkdir(parents=True, exist_ok=True)
        sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()  # noqa: E731
        (root / "PASS-AUTHORIZATION.json").write_text(json.dumps({
            "phase": "full", "assess_sha256": sha(EVAL / "assess70.py"), "core_sha256": sha(EVAL / "core70.py"),
            "assessment_evidence_sha256": sha(EVAL / "assessment_evidence.py"), "driver_sha256": sha(ca.__file__), "profile_sha256": sha(profile)}))

    def test_two_runs_share_one_run_identity_and_both_are_assessed_and_collected_by_command(self):
        for arm in self.ARMS:
            self.assertEqual(self.identities[("main-c01", arm)], self.identities[("main-c02", arm)])      # one run identity, two runs
        root = self.work / "evaluations" / "pass-1"
        args = self.assess_args(root)
        self.authorize(root, args.evaluator_profile)
        with mock.patch.dict(os.environ, {"SSDP70_OMP_PROVIDER_CREDENTIAL": "x"}), mock.patch.object(ca.subprocess, "run", self.fake_assess_process), \
                contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(ca.cmd_run(args), 0, out.getvalue())
        for key in ("main-c01", "main-c02"):
            for arm in self.ARMS:
                a = json.loads((root / key / f"E1-{arm}-r0" / "assessment.json").read_text())
                self.assertEqual(a["assessment_status"], "VALID")
        ids = {json.loads((root / k / f"E1-{arm}-r0" / "assessment-identity.json").read_text())["run_identity_sha256"] for k in ("main-c01", "main-c02")
               for arm in self.ARMS[:1]}
        self.assertEqual(len(ids), 1)                                  # the assessor sees the same run identity twice and keeps the passes apart
        with contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(ca.cmd_collect(args), 0, out.getvalue())
        disp = json.loads(args.out.read_text())
        self.assertEqual(sorted(disp), sorted([f"E1-{a}-r0::i1" for a in self.ARMS] + [f"main-c02/E1-{a}-r0::i1" for a in self.ARMS]))
        self.assertEqual(set(json.loads(args.evidence_out.read_text())), set(disp))
        self.assertEqual(json.loads(out.getvalue())["admissible_runs"], 4)
        # a second pass over the same runs does not re-assess: the (command, run) outputs exist
        with mock.patch.dict(os.environ, {"SSDP70_OMP_PROVIDER_CREDENTIAL": "x"}), mock.patch.object(ca.subprocess, "run", self.fake_assess_process), \
                contextlib.redirect_stdout(io.StringIO()) as out:
            ca.cmd_run(args)
        self.assertIn("0 runs to assess", out.getvalue())
        self.build_record(disp)

    def build_record(self, disp):
        decl = {"slots": [{"episode": "E1", "arm": label, "replicate": k, "panel": "main", "command": f"main-c0{k + 1}", "scored": True,
                           **({"set": k, "run_replicate": 0} if k else {})}
                          for k in (0, 1) for label in ("cand", "b1")],
                "arms": {"cand": "p721", "b1": "p72aa"}, "execution_mode": "probe", "purpose": "development", "unchecked_profile": True,
                "no_activation_arms": list(self.ARMS), "check_pair_order": True}
        (self.h.root / "decl.json").write_text(json.dumps(decl))
        # the harness fixture scores one critical item, so every gate maps that measure and no slot is a delegate episode
        gate_map = {"q2_owed": ["critical"], "q2_unowed": {"measures": ["critical"]}, "q3": {"critical": "tension"}, "q4b": ["critical"],
                    "q4c": ["critical"], "q4d": {"measures": ["critical"]}}
        (self.h.root / "map.json").write_text(json.dumps(gate_map))
        (self.h.root / "disp.json").write_text(json.dumps(disp))
        cmd = [HERE / "build_campaign_record.py", "--declaration", self.h.root / "decl.json", "--map", self.h.root / "map.json",
               "--runs", self.work / "runs" / "main-c01", "--runs", self.work / "runs" / "main-c02", "--dispositions", self.h.root / "disp.json",
               "--allow-unchecked-subject", "--allow-unresolved", "--out", self.h.root / "rec.json", "--audit", self.h.root / "audit.json"]
        p = run(*cmd)
        audit = json.loads((self.h.root / "audit.json").read_text())
        self.assertEqual((p.returncode, audit["findings"]), (0, []), p.stdout)
        rec = json.loads((self.h.root / "rec.json").read_text())
        self.assertEqual(sorted(r["run"] for r in rec["runs"]), sorted(["E1-p721-r0", "E1-p72aa-r0", "main-c02/E1-p721-r0", "main-c02/E1-p72aa-r0"]))
        for r in rec["runs"]:                                             # each run read its own evaluator disposition: the critical item passed
            self.assertEqual([o for o in r["obs"] if o["g"] == "Q4a"], [{"g": "Q4a", "err": 0, "item": "i1"}], r["run"])
        self.assertEqual(audit["pair_order"]["by_set"], {"0": {"p721": 1}, "1": {"p721": 1}})
        return rec


if __name__ == "__main__":
    unittest.main()
