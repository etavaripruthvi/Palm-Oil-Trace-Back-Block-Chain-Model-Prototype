"""The shipped data/derived/*.json files must be exactly what the code produces (same seed, same inputs)."""
import json
import math
import unittest

import _paths
from _paths import DERIVED
import palm_oil_traceability_model as M
import compute_extras


def load(name):
    with open(DERIVED / name) as fh:
        return json.load(fh)


def close(a, b, tol=1e-9):
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(close(a[k], b[k], tol) for k in a)
    if isinstance(a, (list, tuple)):
        return len(a) == len(b) and all(close(x, y, tol) for x, y in zip(a, b))
    if isinstance(a, float) and math.isnan(a):
        return isinstance(b, float) and math.isnan(b)
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return math.isclose(a, b, rel_tol=tol, abs_tol=tol)
    return a == b


class Derived(unittest.TestCase):
    def test_parity_points(self):
        self.assertTrue(close(compute_extras.parity_points(), load("parity2.json")))

    def test_staged_strategy(self):
        self.assertTrue(close(compute_extras.staged_strategy(), load("staged.json")))

    def test_deterministic_results(self):
        nums = load("nums.json")
        for pk in M.PROFILES:
            for scn in M.SCEN:
                self.assertTrue(close(M.deterministic(pk, scn), nums["det"][f"{pk}_{scn}"]), (pk, scn))

    def test_monte_carlo_summary(self):
        recomputed = M.mc_summary().to_dict("records")
        self.assertTrue(close(recomputed, load("nums.json")["mc"]))

    def test_headline_claims_in_the_text(self):
        nums, parity = load("nums.json"), load("parity2.json")
        base = nums["score"]["base"]                                 # ULVR, NESN, WIL
        self.assertEqual([round(x, 1) for x in base], [53.0, 39.9, 63.5])
        self.assertTrue(base[2] > base[0] > base[1])                 # Wilmar > Unilever > Nestle
        self.assertAlmostEqual(parity["ULVR"]["preg_mult"], 1.82, places=2)
        self.assertAlmostEqual(parity["WIL"]["preg_mult"], 2.09, places=2)
        self.assertLess(parity["NESN"]["preg_mult"], 1.0)            # Nestle is already past parity at base inputs
        # ledger cost can fall 3-11% (Wilmar, Unilever) and still tie with the database
        self.assertAlmostEqual(1 - parity["ULVR"]["cost_mult"], 0.107, places=2)
        self.assertAlmostEqual(1 - parity["WIL"]["cost_mult"], 0.030, places=2)


if __name__ == "__main__":
    unittest.main()
