"""Discriminators for the requalification gates (offline; no runtime, no custody material)."""
import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

import core70
import requal71 as rq

HERE = Path(__file__).resolve().parent
PROFILE = HERE / "profiles" / "omp-primary-flash-executor.json"
CAPS = HERE / "capabilities" / "omp-headless.json"


def item(eid, n, measure, critical=False):
    return {"id": f"{eid}::{measure}.{n}", "measure": measure, "critical": critical, "branch": "B",
            "allowed_dispositions": ["pass", "fail", "unresolved"]}


MAIN_ITEMS = ([("critical_disposition", True)] * 12 + [("detection.named", False)] * 14 + [("detection.unnamed", False)] * 6
              + [(m, False) for m in ("null_coverage", "variant_disclosure", "decision_provenance", "delegated_finding_loss",
                                      "o3_violation", "unauthorized_mutation", "owner_load_hit.a", "owner_load_hit.b",
                                      "owner_load_hit.c") for _ in range(6)]
              + [("delegate_request", False)] * 12 + [("predicate_false_firing", False)] * 12)


def make_corpus(root: Path, mutate=None):
    corpus, req = root / "corpus", root / "requirements"
    episodes = [
        {"id": "M1", "panel": "main", "entry": "pinned:software-implementation", "max_turns": 60, "replicates": 1},
        {"id": "B1", "panel": "burden", "entry": "pinned:software-implementation", "max_turns": 60, "replicates": 1},
        {"id": "R1", "panel": "routing", "entry": "pinned:software-design", "max_turns": 8, "replicates": 2},
        {"id": "O1", "panel": "ordinary", "entry": "ordinary", "max_turns": 3, "replicates": 1, "admissible_roots": []},
    ]
    scoring = {"M1": [item("M1", i, m, c) for i, (m, c) in enumerate(MAIN_ITEMS)],
               "B1": [item("B1", 0, "task_fidelity")], "R1": [item("R1", 0, "selection")],
               "O1": [item("O1", i, "selection.negative") for i in range(8)]}
    for ep in episodes:
        ep.update({"fixture": f"fx-{ep['id']}", "prompt": "fresh task", "claims": []})
        (corpus / "fixtures" / ep["fixture"]).mkdir(parents=True)
        (corpus / "fixtures" / ep["fixture"] / "README.md").write_text(f"fresh fixture {ep['id']}\n")
    if mutate:
        mutate(episodes, scoring)
    (corpus / "manifest.yaml").write_text(json.dumps({"schema": "x", "episodes": episodes}))
    req.mkdir()
    for name, payload in (("required_artifacts.json", {e["id"]: [] for e in episodes}),
                          ("required_oracles.json", {e["id"]: [] for e in episodes}),
                          ("expected_scoring_items.json", scoring)):
        (req / name).write_text(json.dumps({"schema": core70.SCHEMA, "episodes": payload}))
    return corpus, req


def real_keys(root: Path):
    root.mkdir(parents=True, exist_ok=True)
    keys = {}
    for panel in rq.KEY_PANELS:
        profile, caps = rq.derive_key(core70.load_json(PROFILE), core70.load_json(CAPS), panel, 1200)
        p, c = root / f"{panel}.json", root / f"{panel}.caps.json"
        p.write_text(json.dumps(profile))
        c.write_text(json.dumps(caps))
        keys[panel] = (p, c)
    return keys


def make_arms(root: Path):
    rows = []
    for name in ("p65", "p66", "p71"):
        dist = root / "arms" / name
        (dist / "software-implementation").mkdir(parents=True)
        (dist / "software-implementation" / "SKILL.md").write_text(name)
        rows.append({"name": name, "requested_ref": "c" * 40, "commit": "c" * 40, "version": name,
                     "skills_path": str(dist), "dist_tree_sha256": core70.sha256_tree(dist)})
    path = root / "arms.json"
    path.write_text(json.dumps({"schema": 1, "arms": rows}))
    return path


class Family(unittest.TestCase):
    def test_family_from_real_primary_profile_passes_core_validator(self):
        with tempfile.TemporaryDirectory() as tmp:
            bundles = rq.load_bundles(real_keys(Path(tmp)))
            record = rq.build_family(bundles)
            self.assertEqual(core70.validate_family(record), [])
            self.assertEqual(bundles["ordinary"].profile["activation_mechanism"], "ordinary-read")
            self.assertFalse([t for t in bundles["burden"].profile["native_tools"] if "delegate" in t])
            self.assertEqual({p: record["panels"][p]["max_turns"] for p in rq.PANEL_TURNS}, rq.PANEL_TURNS)

    def test_wrong_budget_key_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            keys = real_keys(Path(tmp))
            keys["main"] = keys["routing"]
            with self.assertRaises(rq.Stop):
                rq.load_bundles(keys)

    def test_derive_refuses_non_rpc_source(self):
        profile = core70.load_json(PROFILE)
        profile["runtime_mode"] = "json"
        with self.assertRaises(rq.Stop):
            rq.derive_key(profile, core70.load_json(CAPS), "main", 1200)


class Corpus(unittest.TestCase):
    def check(self, mutate=None, disclosed=None):
        with tempfile.TemporaryDirectory() as tmp:
            corpus, req = make_corpus(Path(tmp), mutate)
            reasons, _ = rq.check_corpus(corpus, req, disclosed(corpus) if disclosed else {})
            return reasons

    def test_fresh_stratified_corpus_passes(self):
        self.assertEqual(self.check(), [])

    def test_disclosed_fixture_is_refused(self):
        reasons = self.check(disclosed=lambda c: rq.corpus_digests(c))
        self.assertTrue(any(r.startswith("freshness") for r in reasons))

    def test_budget_and_entry_mismatches_are_refused(self):
        def mutate(eps, _):
            eps[0]["max_turns"] = 30
            eps[1]["entry"] = "ordinary"
            eps[3]["entry"] = "pinned:software-design"
        reasons = self.check(mutate)
        self.assertTrue(any("M1: max_turns" in r for r in reasons))
        self.assertTrue(any("B1: deterministic panel" in r for r in reasons))
        self.assertTrue(any("O1: ordinary panel requires" in r for r in reasons))

    def test_exposure_shortfall_is_refused(self):
        def mutate(_, scoring):
            keep = [i for i in scoring["M1"] if i["measure"] == "delegate_request"][:11]
            scoring["M1"] = [i for i in scoring["M1"] if i["measure"] != "delegate_request"] + keep
        self.assertTrue(any("delegate_request" in r for r in self.check(mutate)))


class Custody(unittest.TestCase):
    def test_append_only_log_may_grow_but_nothing_else_may_change(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = Path(tmp)
            (store / "keys").mkdir()
            (store / "keys" / "k.json").write_text("{}")
            (store / "ACCESS-LOG.md").write_text("a\n")
            before = {"entries": rq.custody_stat(store)}
            with (store / "ACCESS-LOG.md").open("a") as fh:
                fh.write("b\n")
            self.assertEqual(rq.compare_custody(before, {"entries": rq.custody_stat(store)}, {"ACCESS-LOG.md"}), [])
            (store / "keys" / "k.json").write_text('{"x": 1}')
            (store / "new").write_text("")
            reasons = rq.compare_custody(before, {"entries": rq.custody_stat(store)}, {"ACCESS-LOG.md"})
            self.assertIn("changed: keys/k.json", reasons)
            self.assertIn("added: new", reasons)


class CampaignAndAudit(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.corpus, self.req = make_corpus(root)
        self.keys = real_keys(root / "keys")
        self.family = rq.build_family(rq.load_bundles(self.keys))
        self.arms_path = make_arms(root)
        arms = rq.load_arms(self.arms_path, {"p65", "p66", "p71"})
        self.manifest = rq.build_campaign(self.family, self.corpus, self.req, arms, [{"id": "prior"}], [])
        self.root = root

    def tearDown(self):
        self.tmp.cleanup()

    def test_manifest_declares_every_slot_once_with_correct_strata(self):
        ids = [r["id"] for r in self.manifest["runs"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(ids), 2 + 3 + 2 * 2 + 2)  # main, burden(+p65), routing x2 reps, ordinary
        strata = {r["id"]: r["entry_stratum"] for r in self.manifest["runs"]}
        self.assertEqual(strata["O1-p71-r0"], "ordinary")
        self.assertEqual(strata["M1-p71-r0"], "deterministic")
        self.assertIn("B1-p65-r0", strata)
        self.assertEqual(core70.campaign_manifest_errors(self.manifest), [])

    def test_live_repository_arm_is_refused(self):
        arms = json.loads(self.arms_path.read_text())
        arms["arms"][2]["skills_path"] = str(HERE)
        arms["arms"][2]["dist_tree_sha256"] = core70.sha256_tree(HERE)
        self.arms_path.write_text(json.dumps(arms))
        with self.assertRaises(rq.Stop) as ctx:
            rq.load_arms(self.arms_path, {"p71"})
        self.assertIn("inside the live repository", ctx.exception.reasons[0])

    def test_matrix_plan_is_qualification_mode_and_bounded(self):
        adm = {p: f"/adm/{p}.json" for p in rq.KEY_PANELS}
        mpath = self.root / "m.json"
        with self.assertRaises(rq.Stop):  # outside the adapter's approved realization roots
            rq.matrix_commands(mpath, self.manifest, self.keys, adm, self.corpus, self.req, self.root / "or",
                               self.arms_path, self.root / "out", 4)
        approved = Path(rq.omp.RUN_REALIZATION_ROOTS[0]) / "requal71-unit-test-never-created"
        plan = rq.matrix_commands(mpath, self.manifest, self.keys, adm, self.corpus, self.req, self.root / "or",
                                  self.arms_path, approved, 4)
        for cmd in plan:
            argv = cmd["argv"]
            self.assertEqual(argv[argv.index("--mode") + 1], "qualification")
            self.assertEqual(argv[argv.index("--accounting-manifest") + 1], str(mpath))
            self.assertIn("--profile-admission", argv)
        self.assertIn("p65", next(c for c in plan if c["key"] == "burden")["argv"])
        with self.assertRaises(rq.Stop):
            rq.matrix_commands(mpath, self.manifest, self.keys, adm, self.corpus, self.req, self.root, self.arms_path, self.root, 8)

    def write_runs(self, runs_root, assessments=None, mutate=None):
        sha = core70.stable_json_sha256(self.manifest)
        corpus_sha = core70.sha256_file(self.corpus / "manifest.yaml")
        for row in self.manifest["runs"]:
            d = runs_root / row["id"]
            d.mkdir(parents=True)
            ident = {"accounting": {"purpose": "qualification", "campaign_record_sha256": sha}, "execution_mode": "qualification",
                     "profile_admission_sha256": "a" * 64, "profile_key_sha256": row["profile_key_sha256"],
                     "entry_stratum": row["entry_stratum"], "corpus_manifest_sha256": corpus_sha,
                     "declared_root": "software-implementation" if row["entry_stratum"] == "deterministic" else None,
                     "identity_sha256": "i" + row["id"]}
            summary = {"evidence_state": "COMPLETE_ADMISSIBLE", "criteria": {"deterministic activation": "PASS"}, "wall_s": 10}
            if mutate:
                mutate(row["id"], ident, summary)
            (d / "run-identity.json").write_text(json.dumps(ident))
            (d / "summary.json").write_text(json.dumps(summary))
            (d / "events.normalized.jsonl").write_text(json.dumps({"kind": "termination", "payload": {"state": "completed"}}) + "\n")
            if assessments is not None:
                a = assessments / row["id"]
                a.mkdir(parents=True)
                (a / "assessment.json").write_text(json.dumps({"assessment_status": "VALID", "dispositions": [{"result": "pass"}]}))
                (a / "assessment-identity.json").write_text(json.dumps({"run_identity_sha256": ident["identity_sha256"],
                                                                         "evaluator_admission_sha256": "e" * 64}))

    def test_clean_campaign_audits_clean(self):
        runs, ass = self.root / "runs", self.root / "ass"
        self.write_runs(runs, ass)
        result = rq.audit_runs([runs], self.manifest, self.corpus, [ass])
        self.assertEqual((result["integrity"], result["escalate"]), ([], []))
        self.assertEqual(result["counts"]["ordinary:ordinary_group"], {"no-selection": 2})

    def test_development_purpose_extra_dirs_and_failed_activation_are_caught(self):
        runs = self.root / "runs"

        def mutate(rid, ident, summary):
            if rid == "M1-p71-r0":
                ident["accounting"]["purpose"] = "development"
            if rid == "B1-p71-r0":
                summary["criteria"]["deterministic activation"] = "FAIL"
        self.write_runs(runs, mutate=mutate)
        (runs / "M1-p71-r0.failed-timeout").mkdir()
        result = rq.audit_runs([runs], self.manifest, self.corpus, None)
        self.assertIn("M1-p71-r0: purpose mismatch", result["integrity"])
        self.assertTrue(any("undeclared" in r for r in result["integrity"]))
        self.assertTrue(any(r.startswith("B1-p71-r0: deterministic activation FAIL") for r in result["escalate"]))

    def test_missing_runs_and_unbound_assessments_escalate(self):
        runs, ass = self.root / "runs", self.root / "ass"
        self.write_runs(runs, ass)
        (ass / "M1-p66-r0" / "assessment-identity.json").unlink()
        for f in (runs / "O1-p66-r0").iterdir():
            f.unlink()
        (runs / "O1-p66-r0").rmdir()
        result = rq.audit_runs([runs], self.manifest, self.corpus, [ass])
        self.assertIn("O1-p66-r0", result["missing"])
        self.assertTrue(any(r.startswith("M1-p66-r0: assessment missing") for r in result["escalate"]))


class FreezeGate(unittest.TestCase):
    def test_gate_moves_forward_once_and_needs_a_passing_audit(self):
        with tempfile.TemporaryDirectory() as tmp:
            gate, audit = Path(tmp) / "FREEZE-GATE.json", Path(tmp) / "audit.json"
            gate.write_text(json.dumps({"candidate_frozen": False, "frozen_run_output_exists": False}))
            self.assertTrue(rq.set_freeze_gate(gate, "frozen_run_output_exists", None))
            self.assertEqual(rq.set_freeze_gate(gate, "candidate_frozen", None), [])
            self.assertTrue(rq.set_freeze_gate(gate, "candidate_frozen", None))
            audit.write_text(json.dumps({"command": "audit", "verdict": "STOP"}))
            self.assertTrue(rq.set_freeze_gate(gate, "frozen_run_output_exists", audit))
            audit.write_text(json.dumps({"command": "audit", "verdict": "PASS"}))
            self.assertEqual(rq.set_freeze_gate(gate, "frozen_run_output_exists", audit), [])
            self.assertEqual(json.loads(gate.read_text()), {"candidate_frozen": True, "frozen_run_output_exists": True})


class Cli(unittest.TestCase):
    def test_stop_exits_nonzero_with_json_verdict(self):
        with tempfile.TemporaryDirectory() as tmp:
            corpus, req = make_corpus(Path(tmp), lambda eps, _: eps[0].update(max_turns=30))
            disclosed = Path(tmp) / "d.json"
            disclosed.write_text("{}")
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = rq.main(["corpus-check", "--corpus", str(corpus), "--requirements", str(req), "--disclosed", str(disclosed)])
            self.assertEqual(code, 1)
            self.assertEqual(json.loads(buf.getvalue())["verdict"], "STOP")

    def test_outputs_are_never_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "x.json"
            target.write_text("{}")
            with self.assertRaises(rq.Stop):
                rq.write_json(target, {})


if __name__ == "__main__":
    unittest.main()
