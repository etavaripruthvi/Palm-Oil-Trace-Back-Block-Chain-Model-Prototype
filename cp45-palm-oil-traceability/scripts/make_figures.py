"""Regenerate all 18 report figures into figures/ (also writes power.json, fine_rob.json and impact.json to data/derived/).

Requires data/derived/nums.json (run scripts/compute_numbers.py first).
"""
import runpy
import time
from pathlib import Path
from _bootstrap import ROOT

STEPS = ["make_figs_diagnostics.py",   # f01-f07, f14, f16  (margins, prices, ESG, Scope 3, SPLC, news, SPOEI heat map, leverage, power)
         "make_figs_scenarios.py",     # f09-f13, f15       (scenario NPV, cost decomposition, Monte Carlo, tornado, coverage grid, risk-return)
         "make_fig_architecture.py",   # f08                (permissioned architecture diagram)
         "make_fig_spoei_gap.py",      # f17                (what drives Wilmar's SPOEI premium)
         "make_fig_heatmap.py"]        # f18                (risk-cost heat map)

if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    for step in STEPS:
        t0 = time.time()
        runpy.run_path(str(here / step), run_name="__main__")
        print(f"[{step}] {time.time() - t0:.1f}s")
    print("figures written to", ROOT / "figures")
