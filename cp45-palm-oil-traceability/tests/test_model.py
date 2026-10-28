"""Unit tests for the cost-benefit / Monte Carlo engine (src/palm_oil_traceability_model.py)."""
import unittest

import numpy as np

import _paths  # noqa: F401
import palm_oil_traceability_model as M


class DeterministicModel(unittest.TestCase):
    def test_headline_numbers_match_report(self):
        # Unilever / Wilmar blockchain NPV benefit vs status quo, USD m (report Table 5.5)
        self.assertAlmostEqual(M.deterministic("ULVR", "Base")["BC"]["benefit"], 16.0, delta=0.1)
        self.assertAlmostEqual(M.deterministic("WIL", "Severe")["BC"]["benefit"], 470.5, delta=0.5)
        self.assertAlmostEqual(M.deterministic("NESN", "Adverse")["DB"]["benefit"], 96.0, delta=0.6)

    def test_traceability_pays_in_every_scenario(self):
        for pk in M.PROFILES:
            for scn in M.SCEN:
                d = M.deterministic(pk, scn)
                self.assertGreater(d["DB"]["benefit"], 0, (pk, scn, "DB"))
                self.assertGreater(d["BC"]["benefit"], 0, (pk, scn, "BC"))

    def test_benefit_rises_with_regulatory_risk(self):
        for pk, pf in M.PROFILES.items():
            for opt in ("DB", "BC"):
                lo = M.deterministic(pk, "Base", {"all": dict(p_reg=pf["p_reg"] * 0.5)})[opt]["benefit"]
                hi = M.deterministic(pk, "Base", {"all": dict(p_reg=pf["p_reg"] * 2.0)})[opt]["benefit"]
                self.assertGreater(hi, lo)

    def test_status_quo_carries_no_programme_cost(self):
        pf = M.PROFILES["ULVR"]
        prm = dict(r=M.G["r"], fine=M.G["fine"], q=M.G["q"], pi=M.G["pi"], c0=M.G["c0"], p_reg=pf["p_reg"], p_ctrv=pf["p_ctrv"],
                   eff=M.OPTIONS["SQ"]["eff"], cmax=None, ramp=1.0)
        out = M.pv_total(pf, "SQ", prm, np.ones(M.G["horizon"]))
        self.assertEqual(float(out["pv_prog"]), 0.0)
        self.assertAlmostEqual(float(out["pv_total"]), float(out["pv_loss"]))

    def test_break_even_multiplier_is_a_fraction_of_regulatory_loss(self):
        for pk in M.PROFILES:
            k = M.deterministic(pk, "Base")["BC"]["breakeven_k"]
            self.assertTrue(0.0 <= k <= 1.0)


class MonteCarlo(unittest.TestCase):
    def test_reproducible_with_seed(self):
        a = M.monte_carlo("ULVR", "Mixed", n=2000, seed=7)
        b = M.monte_carlo("ULVR", "Mixed", n=2000, seed=7)
        c = M.monte_carlo("ULVR", "Mixed", n=2000, seed=8)
        np.testing.assert_array_equal(a["BC"], b["BC"])
        self.assertFalse(np.array_equal(a["BC"], c["BC"]))

    def test_common_random_numbers_and_regime_ordering(self):
        base = M.monte_carlo("WIL", "Base", n=4000)
        severe = M.monte_carlo("WIL", "Severe", n=4000)
        self.assertGreater(severe["DB"].mean(), base["DB"].mean())
        self.assertGreater(severe["BC"].mean(), base["BC"].mean())

    def test_summary_shape(self):
        s = M.mc_summary()
        self.assertEqual(len(s), 3 * 4 * 2)                       # firms x regimes x options
        mixed = s[(s.regime == "Mixed") & (s.option == "BC")]
        self.assertTrue(((mixed.p_BC_beats_DB > 0.30) & (mixed.p_BC_beats_DB < 0.45)).all())   # report: 35-42%


class MarketAnalytics(unittest.TestCase):
    def test_price_window_and_volatility(self):
        px = M.price_frame()
        self.assertEqual(str(px.index.min().date()), "2026-08-17")
        self.assertEqual(str(px.index.max().date()), "2026-10-15")
        self.assertAlmostEqual(M.CPO_SIGMA, 0.1705, places=3)      # report Table 5.2: 17.05% a year

    def test_no_correlation_claims_beyond_the_noise_band(self):
        st = M.market_analytics(M.price_frame())
        for c in ("WIL", "NESN", "ULVR"):
            band = 2 / np.sqrt(st.loc[c, "n_pairs_vs_CPO"])
            self.assertLess(abs(st.loc[c, "corr_vs_CPO"]), band)   # all three are statistically indistinguishable from zero


class CoverageGrid(unittest.TestCase):
    def test_grid_monotone(self):
        g = M.coverage_exclusion_grid("ULVR")
        self.assertTrue((np.diff(g.values, axis=0) <= 1e-12).all())    # more coverage -> lower substitution cost
        self.assertTrue((np.diff(g.values, axis=1) >= -1e-12).all())   # more exclusion -> higher cost
        self.assertAlmostEqual(g.loc["100%"].max(), 0.0, places=9)     # fully traceable supply needs no substitution


if __name__ == "__main__":
    unittest.main()
