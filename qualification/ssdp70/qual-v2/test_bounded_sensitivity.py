"""Bounded-sensitivity analysis (bounded_sensitivity.py): fillings, determinism, classification and the C(c)-first refusal."""
import argparse
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bounded_sensitivity as bs
import h4


class Fillings(unittest.TestCase):
    unresolved = {"cand": ["r-p72::a", "r-p72::b"], "b1": ["r-p66::a"], "b2": ["r-p66b::c"]}

    def test_fill_covers_every_unresolved_item_and_never_overwrites_a_resolved_one(self):
        out = bs.fill({"x::y": "pass"}, self.unresolved, lambda arm, key: "fail" if arm == "cand" else "pass")
        self.assertEqual(out, {"x::y": "pass", "r-p72::a": "fail", "r-p72::b": "fail", "r-p66::a": "pass", "r-p66b::c": "pass"})
        with self.assertRaises(ValueError):
            bs.fill({"r-p66::a": "pass"}, self.unresolved, lambda arm, key: "pass")

    def test_corners_are_the_four_b1_b2_combinations_with_the_candidate_fixed_at_pass(self):
        labels, seen = [], set()
        for label, choose in bs.corner_fillings():
            labels.append(label)
            seen.add((choose("b1", "k"), choose("b2", "k"), choose("cand", "k")))
        self.assertEqual(len(labels), 4)
        self.assertEqual(seen, {(a, b, "pass") for a in ("pass", "fail") for b in ("pass", "fail")})

    def test_random_fillings_are_reproducible_and_vary(self):
        a = [bs.random_chooser(bs.SEED, i)("b1", "r::k") for i in range(60)]
        b = [bs.random_chooser(bs.SEED, i)("b1", "r::k") for i in range(60)]
        self.assertEqual(a, b)
        self.assertEqual(set(a), {"pass", "fail"})
        self.assertEqual(bs.random_chooser(bs.SEED, 0, ("b1", "b2"))("cand", "r::k"), "pass")      # arms outside the set are fixed at pass

    def test_classification(self):
        P, F = h4.PASS, h4.FAIL
        self.assertEqual(bs.classify(P, P), "ROBUST PASS")
        self.assertEqual(bs.classify(F, F), "ROBUST FAIL")
        self.assertEqual(bs.classify(F, P), "FRAGILE")
        self.assertEqual(bs.classify(h4.PENDING, h4.PENDING), "ROBUST FAIL")                      # only PASS counts as a pass


class GatesNeedCcFirst(unittest.TestCase):
    def analysis(self):
        an = bs.Analysis.__new__(bs.Analysis)
        an.a = argparse.Namespace(random=3)
        an.base, an.unresolved = {"a::b": "pass"}, {"b1": ["r::k"]}
        return an

    def test_gates_are_refused_without_an_established_current_cc(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            an = self.analysis()
            an.record_for = lambda choose: self.fail("no record may be built before C(c) is established")
            self.assertEqual(bs.gates_stage(an, out), {"refused": True})                           # no cc.json
            (out / "cc.json").write_text(json.dumps({"established": False, "identity": an.identity()}))
            self.assertEqual(bs.gates_stage(an, out), {"refused": True})                           # not established
            (out / "cc.json").write_text(json.dumps({"established": True, "identity": {"seed": 1}}))
            self.assertEqual(bs.gates_stage(an, out), {"refused": True})                           # stale inputs


if __name__ == "__main__":
    unittest.main()
